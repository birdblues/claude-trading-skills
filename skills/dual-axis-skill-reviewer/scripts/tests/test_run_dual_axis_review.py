from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_parse_frontmatter_supports_yaml(reviewer_module):
    lines = [
        "---\n",
        "name: sample-skill\n",
        "description: >-\n",
        "  line one: value\n",
        "  line two\n",
        "---\n",
        "# body\n",
    ]

    frontmatter = reviewer_module.parse_frontmatter(lines)

    assert frontmatter["name"] == "sample-skill"
    assert "line one: value" in frontmatter["description"]
    assert "line two" in frontmatter["description"]


def test_parse_frontmatter_rejects_invalid_yaml(reviewer_module):
    lines = [
        "---\n",
        "name: sample\n",
        "description: [unterminated\n",
        "---\n",
    ]
    assert reviewer_module.parse_frontmatter(lines) == {}


def test_pick_skill_by_name_and_missing(reviewer_module, tmp_path: Path):
    skill_a = tmp_path / "skills" / "a-skill" / "SKILL.md"
    skill_b = tmp_path / "skills" / "b-skill" / "SKILL.md"
    write_text(skill_a, "---\nname: a-skill\ndescription: x\n---\n")
    write_text(skill_b, "---\nname: b-skill\ndescription: x\n---\n")
    skills = [skill_a, skill_b]

    picked = reviewer_module.pick_skill(skills, "b-skill", None)
    assert picked == skill_b

    with pytest.raises(ValueError):
        reviewer_module.pick_skill(skills, "missing-skill", None)


def test_discover_test_dirs_supports_two_layouts(reviewer_module, tmp_path: Path):
    skill_dir = tmp_path / "skills" / "sample"
    write_text(skill_dir / "scripts" / "tests" / "test_a.py", "def test_a():\n    assert True\n")
    write_text(skill_dir / "tests" / "test_b.py", "def test_b():\n    assert True\n")

    dirs = reviewer_module.discover_test_dirs(skill_dir)
    assert skill_dir / "scripts" / "tests" in dirs
    assert skill_dir / "tests" in dirs


def test_run_tests_fallbacks_to_python_pytest(reviewer_module, tmp_path: Path, monkeypatch):
    skill_dir = tmp_path / "skills" / "sample"
    write_text(skill_dir / "tests" / "test_x.py", "def test_x():\n    assert True\n")

    calls: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        if cmd[0] == "uv":
            raise FileNotFoundError("uv missing")
        return subprocess.CompletedProcess(cmd, 0, "ok\n1 passed\n", "")

    monkeypatch.setattr(reviewer_module.subprocess, "run", fake_run)

    status, command, output = reviewer_module.run_tests(tmp_path, skill_dir)

    assert status == "passed"
    assert command is not None and sys.executable in command
    assert "1 passed" in output
    assert calls[0][0] == "uv"
    assert calls[1][0] == sys.executable


def test_run_tests_fallback_timeout_is_captured(reviewer_module, tmp_path: Path, monkeypatch):
    skill_dir = tmp_path / "skills" / "sample"
    write_text(skill_dir / "tests" / "test_x.py", "def test_x():\n    assert True\n")

    calls: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        if cmd[0] == "uv":
            raise FileNotFoundError("uv missing")
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=180)

    monkeypatch.setattr(reviewer_module.subprocess, "run", fake_run)

    status, command, output = reviewer_module.run_tests(tmp_path, skill_dir)

    assert status == "timeout"
    assert command is not None and sys.executable in command
    assert "timeout" in output.lower()
    assert calls[0][0] == "uv"
    assert calls[1][0] == sys.executable


def test_load_llm_review_validation(reviewer_module, tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"score": "bad"}), encoding="utf-8")
    with pytest.raises(ValueError):
        reviewer_module.load_llm_review(str(bad), tmp_path)

    good = tmp_path / "good.json"
    good.write_text(
        json.dumps(
            {
                "score": 85,
                "summary": "ok",
                "findings": [
                    {
                        "severity": "HIGH",
                        "path": "skills/x/SKILL.md",
                        "line": 5,
                        "message": "issue",
                        "improvement": "fix",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    loaded = reviewer_module.load_llm_review(str(good), tmp_path)
    assert loaded["score"] == 85
    assert loaded["findings"][0]["severity"] == "high"


def test_combine_reviews_handles_zero_weights(reviewer_module):
    auto = {"score": 80, "findings": []}
    llm = {"provided": True, "score": 60, "findings": []}

    merged = reviewer_module.combine_reviews(auto, llm, auto_weight=0.0, llm_weight=0.0)

    assert merged["score"] == 70
    assert merged["weights"]["auto_weight"] == 0.5
    assert merged["weights"]["llm_weight"] == 0.5


def test_score_skill_counts_tests_in_root_tests_dir(reviewer_module, tmp_path: Path):
    project_root = tmp_path
    skill_dir = project_root / "skills" / "sample-skill"
    skill_md = skill_dir / "SKILL.md"
    write_text(
        skill_md,
        "\n".join(
            [
                "---",
                "name: sample-skill",
                "description: sample",
                "---",
                "",
                "## When to Use",
                "x",
                "## Prerequisites",
                "x",
                "## Workflow",
                "```bash",
                "python3 skills/sample-skill/scripts/run.py --output-dir reports/",
                "```",
                "## Output",
                "x",
                "## Resources",
                "- `skills/sample-skill/references/ref.md`",
                "",
            ]
        ),
    )
    write_text(skill_dir / "scripts" / "run.py", "print('ok')\n")
    write_text(skill_dir / "references" / "ref.md", "# ref\n")
    write_text(skill_dir / "tests" / "test_sample.py", "def test_sample():\n    assert True\n")

    review = reviewer_module.score_skill(project_root, skill_md, skip_tests=True)

    assert review["score_breakdown"]["supporting_artifacts"] == 10
    assert review["score_breakdown"]["test_health"] == 8
    messages = [finding["message"] for finding in review["findings"]]
    assert "No `test_*.py` tests found for skill scripts." not in messages


def test_normalize_severity_direct(reviewer_module):
    assert reviewer_module.normalize_severity("HIGH") == "high"
    assert reviewer_module.normalize_severity(" medium ") == "medium"
    assert reviewer_module.normalize_severity("unknown") == "medium"


def test_extract_bash_blocks_handles_empty_and_multiple(reviewer_module):
    text = """
before
```bash
echo one
```
middle
```bash

```
after
```bash
echo two
```
"""
    blocks = reviewer_module.extract_bash_blocks(text)
    assert blocks == ["echo one", "echo two"]


def test_build_llm_prompt_includes_inventory(reviewer_module, tmp_path: Path):
    project_root = tmp_path
    skill_dir = project_root / "skills" / "prompt-skill"
    write_text(skill_dir / "SKILL.md", "---\nname: prompt-skill\ndescription: d\n---\n")
    write_text(skill_dir / "scripts" / "main.py", "print('x')\n")
    write_text(skill_dir / "tests" / "test_main.py", "def test_main():\n    assert True\n")
    write_text(skill_dir / "references" / "note.md", "# note\n")

    prompt = reviewer_module.build_llm_prompt(
        project_root=project_root,
        skill_dir=skill_dir,
        auto_review={"skill_name": "prompt-skill", "score": 88, "findings": []},
    )
    assert "LLM Skill Review Request" in prompt
    assert "skills/prompt-skill/scripts/main.py" in prompt
    assert "skills/prompt-skill/tests/test_main.py" in prompt
    assert "strict JSON only" in prompt


def test_to_markdown_contains_combined_sections(reviewer_module):
    report = {
        "generated_at": "2026-02-20 00:00:00",
        "skill_name": "x-skill",
        "skill_file": "skills/x-skill/SKILL.md",
        "selection_mode": "manual",
        "seed": 1,
        "auto_review": {
            "score": 80,
            "score_breakdown": {"a": 1},
            "test_status": "passed",
            "test_command": "pytest x",
        },
        "llm_review": {"provided": True, "score": 70},
        "final_review": {
            "score": 75,
            "weights": {"auto_weight": 0.5, "llm_weight": 0.5},
            "findings": [
                {"axis": "auto", "severity": "medium", "path": "skills/x-skill/SKILL.md", "line": 3, "message": "m"}
            ],
            "improvements_required": True,
            "improvement_items": ["m -> fix"],
        },
        "llm_prompt_file": "reports/prompt.md",
    }
    md = reviewer_module.to_markdown(report)
    assert "# Dual-Axis Skill Review" in md
    assert "Final score: **75 / 100**" in md
    assert "## Findings (Combined)" in md
    assert "## Improvement Items (Final Score < 90)" in md


def test_combine_reviews_boundary_at_90_no_improvement(reviewer_module):
    auto = {
        "score": 90,
        "findings": [{"severity": "low", "message": "x", "improvement": "y", "path": "a", "line": None}],
    }
    merged = reviewer_module.combine_reviews(auto, None, auto_weight=1.0, llm_weight=0.0)
    assert merged["score"] == 90
    assert merged["improvements_required"] is False
    assert merged["improvement_items"] == []


def test_main_e2e_generates_report_files(tmp_path: Path):
    project_root = tmp_path
    skill_dir = project_root / "skills" / "e2e-skill"
    write_text(
        skill_dir / "SKILL.md",
        "\n".join(
            [
                "---",
                "name: e2e-skill",
                "description: test",
                "---",
                "",
                "## When to Use",
                "x",
                "## Prerequisites",
                "x",
                "## Workflow",
                "```bash",
                "python3 skills/e2e-skill/scripts/run.py --output-dir reports/",
                "```",
                "## Output",
                "x",
                "## Resources",
                "- `skills/e2e-skill/references/ref.md`",
                "",
            ]
        ),
    )
    write_text(skill_dir / "scripts" / "run.py", "print('ok')\n")
    write_text(skill_dir / "references" / "ref.md", "# ref\n")

    script_path = Path(__file__).resolve().parents[1] / "run_dual_axis_review.py"
    proc = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--project-root",
            str(project_root),
            "--skill",
            "e2e-skill",
            "--skip-tests",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    report_files = list((project_root / "reports").glob("skill_review_e2e-skill_*.json"))
    assert report_files

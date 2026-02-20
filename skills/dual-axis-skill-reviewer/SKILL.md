---
name: dual-axis-skill-reviewer
description: "Review skills in this repository using a dual-axis method: (1) deterministic code-based checks (structure, scripts, tests, execution safety) and (2) LLM deep review findings. Use when you need reproducible quality scoring for `skills/*/SKILL.md`, want to gate merges with a score threshold (for example 90+), or need concrete improvement items for low-scoring skills."
---

# Dual Axis Skill Reviewer

Run the dual-axis reviewer script in `scripts/run_dual_axis_review.py` and save reports to `reports/`.

The script supports:
- Random or fixed skill selection
- Auto-axis scoring with optional test execution
- LLM prompt generation
- LLM JSON review merge with weighted final score

## When to Use

- Need reproducible scoring for one skill in `skills/*/SKILL.md`.
- Need improvement items when final score is below 90.
- Need both deterministic checks and qualitative LLM code/content review.

## Prerequisites

- Python 3.9+
- Project dependencies installed (for tests): `uv sync --extra dev` or equivalent
- PyYAML available (included in this repository's project dependencies)
- For LLM-axis merge: JSON file that follows `skills/dual-axis-skill-reviewer/references/llm_review_schema.md`

## Workflow

### Step 1: Run Auto Axis + Generate LLM Prompt

```bash
python3 skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . \
  --emit-llm-prompt
```

### Step 2: Run LLM Review
- Use the generated prompt file in `reports/skill_review_prompt_<skill>_<timestamp>.md`.
- Ask the LLM to return strict JSON output.
- When running inside Claude Code, let Claude act as orchestrator: read the generated prompt, produce the LLM review JSON, and save it for the merge step.
- Validate schema against `skills/dual-axis-skill-reviewer/references/llm_review_schema.md`.

### Step 3: Merge Auto + LLM Axes
```bash
python3 skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py \
  --project-root . \
  --skill <skill-name> \
  --llm-review-json <path-to-llm-review.json> \
  --auto-weight 0.5 \
  --llm-weight 0.5
```

### Step 4: Optional Controls

- Fix selection for reproducibility: `--skill <name>` or `--seed <int>`
- Skip tests for quick triage: `--skip-tests`
- Change report location: `--output-dir <dir>`
- Increase `--auto-weight` for stricter deterministic gating.
- Increase `--llm-weight` when qualitative/code-review depth is prioritized.

## Output

- `reports/skill_review_<skill>_<timestamp>.json`
- `reports/skill_review_<skill>_<timestamp>.md`
- `reports/skill_review_prompt_<skill>_<timestamp>.md` (when `--emit-llm-prompt` is enabled)

## Resources

- Auto axis scores metadata, workflow coverage, execution safety, artifact presence, and test health.
- LLM axis scores deep content quality (correctness, risk, missing logic, maintainability).
- Final score is weighted average.
- If final score is below 90, improvement items are required and listed in the markdown report.
- Script: `skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py`
- LLM schema: `skills/dual-axis-skill-reviewer/references/llm_review_schema.md`
- Rubric detail: `skills/dual-axis-skill-reviewer/references/scoring_rubric.md`

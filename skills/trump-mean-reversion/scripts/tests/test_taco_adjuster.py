"""Tests for TACO adjuster CLI integration."""

import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "..")
ADJUSTER_SCRIPT = os.path.join(SCRIPT_DIR, "taco_adjuster.py")


class TestTacoAdjusterCLI:
    """Integration tests for the CLI entry point."""

    def test_manual_input_runs(self, tmp_path):
        """CLI with manual inputs should produce reports."""
        result = subprocess.run(
            [
                sys.executable,
                ADJUSTER_SCRIPT,
                "--base",
                "40",
                "--bull",
                "15",
                "--bear",
                "45",
                "--geopolitics",
                "7",
                "--trade",
                "5",
                "--output-dir",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        # Should output JSON path to stdout
        stdout = result.stdout.strip()
        assert stdout.endswith(".json")
        assert os.path.isfile(stdout)

        # Check JSON report content
        with open(stdout) as f:
            report = json.load(f)
        assert "pain_index" in report
        assert "probability_adjustment" in report
        assert report["pain_index"]["zone"] in ("Low", "Medium", "High")

    def test_markdown_report_generated(self, tmp_path):
        """CLI should also generate a Markdown report."""
        result = subprocess.run(
            [
                sys.executable,
                ADJUSTER_SCRIPT,
                "--base",
                "50",
                "--bull",
                "25",
                "--bear",
                "25",
                "--geopolitics",
                "5",
                "--trade",
                "5",
                "--output-dir",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        md_files = [f for f in os.listdir(tmp_path) if f.endswith(".md")]
        assert len(md_files) == 1
        md_content = (tmp_path / md_files[0]).read_text()
        assert "TACO Probability Adjustment Report" in md_content
        assert "Trump Pain Index" in md_content

    def test_scenario_json_input(self, tmp_path):
        """CLI should accept --scenario-json."""
        scenario = {"base": 40, "bull": 15, "bear": 45}
        scenario_path = tmp_path / "input.json"
        scenario_path.write_text(json.dumps(scenario))

        result = subprocess.run(
            [
                sys.executable,
                ADJUSTER_SCRIPT,
                "--scenario-json",
                str(scenario_path),
                "--geopolitics",
                "8",
                "--trade",
                "6",
                "--output-dir",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0

    def test_no_input_fails(self, tmp_path):
        """CLI with no scenario input should fail."""
        result = subprocess.run(
            [
                sys.executable,
                ADJUSTER_SCRIPT,
                "--output-dir",
                str(tmp_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 1
        assert "ERROR" in result.stderr

"""Tests for scenario parser."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scenario_parser import (
    from_cli_args,
    parse_scenario_json,
    parse_scenario_markdown,
)


class TestParseScenarioJson:
    """Tests for JSON scenario parsing."""

    def test_top_level_keys(self, tmp_path):
        """Parse {"base": 40, "bull": 15, "bear": 45}."""
        data = {"base": 40, "bull": 15, "bear": 45}
        path = tmp_path / "scenario.json"
        path.write_text(json.dumps(data))
        result = parse_scenario_json(str(path))
        assert result is not None
        assert result["base"] == 40
        assert result["bull"] == 15
        assert result["bear"] == 45

    def test_decimal_fractions_converted(self, tmp_path):
        """Parse {"base": 0.40, "bull": 0.15, "bear": 0.45}."""
        data = {"base": 0.40, "bull": 0.15, "bear": 0.45}
        path = tmp_path / "scenario.json"
        path.write_text(json.dumps(data))
        result = parse_scenario_json(str(path))
        assert result["base"] == 40.0
        assert result["bull"] == 15.0
        assert result["bear"] == 45.0

    def test_nested_scenarios(self, tmp_path):
        """Parse nested structure with probability field."""
        data = {
            "scenarios": {
                "base": {"probability": 50, "description": "Base case"},
                "bull": {"probability": 20, "description": "Bull case"},
                "bear": {"probability": 30, "description": "Bear case"},
            }
        }
        path = tmp_path / "scenario.json"
        path.write_text(json.dumps(data))
        result = parse_scenario_json(str(path))
        assert result is not None
        assert result["base"] == 50
        assert result["bull"] == 20
        assert result["bear"] == 30

    def test_druckenmiller_conviction(self, tmp_path):
        """Parse Druckenmiller conviction format."""
        data = {
            "conviction": {
                "conviction_score": 28.1,
                "zone": "Low Conviction",
            }
        }
        path = tmp_path / "druckenmiller.json"
        path.write_text(json.dumps(data))
        result = parse_scenario_json(str(path))
        assert result is not None
        assert result["base"] > 0
        assert result["bull"] > 0
        assert result["bear"] > 0
        total = result["base"] + result["bull"] + result["bear"]
        assert abs(total - 100) < 1

    def test_nonexistent_file_returns_none(self):
        """Nonexistent file should return None."""
        result = parse_scenario_json("/nonexistent/path.json")
        assert result is None

    def test_invalid_json_returns_none(self, tmp_path):
        """Invalid JSON should return None."""
        path = tmp_path / "bad.json"
        path.write_text("not json")
        result = parse_scenario_json(str(path))
        assert result is None


class TestParseScenarioMarkdown:
    """Tests for Markdown scenario parsing."""

    def test_header_pattern(self, tmp_path):
        """Parse ### Base Case (50% ...) pattern."""
        md = """# Analysis
### Base Case (50% probability)
Description here

### Bull Case (20% probability)
More description

### Bear Case (30% probability)
Bear description
"""
        path = tmp_path / "scenario.md"
        path.write_text(md)
        result = parse_scenario_markdown(str(path))
        assert result is not None
        assert result["base"] == 50
        assert result["bull"] == 20
        assert result["bear"] == 30

    def test_korean_pattern(self, tmp_path):
        """Parse Korean-style headers."""
        md = """# 시나리오 분석
### Base Case (50% 확률)
설명

### Bull Case (15% 확률)
설명

### Bear Case (35% 확률)
설명
"""
        path = tmp_path / "scenario_ko.md"
        path.write_text(md)
        result = parse_scenario_markdown(str(path))
        assert result is not None
        assert result["base"] == 50

    def test_table_pattern(self, tmp_path):
        """Parse table-based probability display."""
        md = """# Analysis
| Scenario | Probability |
|----------|-------------|
| Base | 45% |
| Bull | 20% |
| Bear | 35% |
"""
        path = tmp_path / "table.md"
        path.write_text(md)
        result = parse_scenario_markdown(str(path))
        assert result is not None
        assert result["base"] == 45
        assert result["bull"] == 20
        assert result["bear"] == 35


class TestFromCliArgs:
    """Tests for CLI argument parsing."""

    def test_all_provided(self):
        result = from_cli_args(base=40, bull=15, bear=45)
        assert result == {"base": 40.0, "bull": 15.0, "bear": 45.0, "source": "cli"}

    def test_missing_args_returns_none(self):
        assert from_cli_args(base=40, bull=15) is None
        assert from_cli_args(base=40) is None
        assert from_cli_args() is None

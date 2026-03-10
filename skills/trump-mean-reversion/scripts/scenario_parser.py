#!/usr/bin/env python3
"""Parser for upstream skill scenario outputs.

Extracts Base/Bull/Bear probabilities from:
    - scenario-analyzer JSON/Markdown
    - stanley-druckenmiller-investment JSON
    - Direct CLI arguments
"""

import json
import os
import re
from typing import Optional


def parse_scenario_json(json_path: str) -> Optional[dict]:
    """Parse scenario probabilities from a JSON file.

    Supports multiple JSON structures:
        1. Top-level: {"base": 40, "bull": 15, "bear": 45}
        2. Nested: {"scenarios": {"base": {..., "probability": 40}, ...}}
        3. Druckenmiller: {"conviction": {"conviction_score": 28.1, ...}}

    Args:
        json_path: Path to JSON file.

    Returns:
        Dict with "base", "bull", "bear" (0-100 scale) and "source",
        or None if parsing fails.
    """
    if not os.path.isfile(json_path):
        return None

    try:
        with open(json_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    # Pattern 1: Top-level keys
    if all(k in data for k in ("base", "bull", "bear")):
        return _extract_top_level(data, json_path)

    # Pattern 2: Nested scenarios
    if "scenarios" in data:
        return _extract_nested_scenarios(data, json_path)

    # Pattern 3: Druckenmiller conviction (convert to scenario probs)
    if "conviction" in data:
        return _extract_druckenmiller(data, json_path)

    # Pattern 4: scenario_probabilities field
    if "scenario_probabilities" in data:
        probs = data["scenario_probabilities"]
        if all(k in probs for k in ("base", "bull", "bear")):
            return _extract_top_level(probs, json_path)

    return None


def parse_scenario_markdown(md_path: str) -> Optional[dict]:
    """Parse scenario probabilities from a Markdown report.

    Looks for patterns like:
        ### Base Case (50% ...)
        ### Bull Case (15% ...)
        ### Bear Case (35% ...)
    Or table patterns:
        | Base | 50% |

    Args:
        md_path: Path to Markdown file.

    Returns:
        Dict with "base", "bull", "bear" (0-100 scale), or None.
    """
    if not os.path.isfile(md_path):
        return None

    try:
        with open(md_path) as f:
            content = f.read()
    except OSError:
        return None

    result = {}

    # Pattern: ### Base Case (50% ...)
    header_pattern = re.compile(
        r"###\s+(Base|Bull|Bear)\s+Case\s*\((\d+(?:\.\d+)?)\s*%",
        re.IGNORECASE,
    )
    for match in header_pattern.finditer(content):
        case_name = match.group(1).lower()
        probability = float(match.group(2))
        result[case_name] = probability

    if len(result) == 3:
        result["source"] = md_path
        return result

    # Pattern: | Base | 50% | or | Base Case | 50% |
    table_pattern = re.compile(
        r"\|\s*(Base|Bull|Bear)(?:\s+Case)?\s*\|\s*(\d+(?:\.\d+)?)\s*%\s*\|",
        re.IGNORECASE,
    )
    result = {}
    for match in table_pattern.finditer(content):
        case_name = match.group(1).lower()
        probability = float(match.group(2))
        result[case_name] = probability

    if len(result) == 3:
        result["source"] = md_path
        return result

    return None


def from_cli_args(
    base: Optional[float] = None,
    bull: Optional[float] = None,
    bear: Optional[float] = None,
) -> Optional[dict]:
    """Create scenario dict from CLI arguments.

    Args:
        base: Base case probability (0-100).
        bull: Bull case probability (0-100).
        bear: Bear case probability (0-100).

    Returns:
        Dict with "base", "bull", "bear", or None if any is missing.
    """
    if base is None or bull is None or bear is None:
        return None
    return {
        "base": float(base),
        "bull": float(bull),
        "bear": float(bear),
        "source": "cli",
    }


def _extract_top_level(data: dict, source: str) -> dict:
    """Extract from {"base": X, "bull": Y, "bear": Z}."""
    base = _to_percentage(data["base"])
    bull = _to_percentage(data["bull"])
    bear = _to_percentage(data["bear"])
    return {"base": base, "bull": bull, "bear": bear, "source": source}


def _extract_nested_scenarios(data: dict, source: str) -> Optional[dict]:
    """Extract from {"scenarios": {"base": {"probability": X}, ...}}."""
    scenarios = data["scenarios"]
    result = {}
    for key in ("base", "bull", "bear"):
        if key not in scenarios:
            return None
        entry = scenarios[key]
        if isinstance(entry, dict):
            prob = entry.get("probability", entry.get("prob"))
            if prob is None:
                return None
            result[key] = _to_percentage(prob)
        else:
            result[key] = _to_percentage(entry)
    result["source"] = source
    return result


def _extract_druckenmiller(data: dict, source: str) -> dict:
    """Convert Druckenmiller conviction score to scenario probabilities.

    Conviction 80-100 → strong Bull bias
    Conviction 40-60  → balanced Base
    Conviction 0-20   → strong Bear bias
    """
    conviction = data["conviction"]
    score = conviction.get("conviction_score", 50.0)

    # Convert conviction to scenario probabilities
    if score >= 70:
        bull = min(40.0, 15 + (score - 70) * 0.83)
        bear = max(10.0, 30 - (score - 70) * 0.67)
        base = 100.0 - bull - bear
    elif score >= 40:
        bull = 15 + (score - 40) * 0.17
        bear = 30 - (score - 40) * 0.17
        base = 100.0 - bull - bear
    else:
        bear = min(50.0, 30 + (40 - score) * 0.50)
        bull = max(5.0, 15 - (40 - score) * 0.25)
        base = 100.0 - bull - bear

    return {
        "base": round(base, 1),
        "bull": round(bull, 1),
        "bear": round(bear, 1),
        "source": source,
        "converted_from": "druckenmiller_conviction",
        "original_conviction_score": score,
    }


def _to_percentage(value) -> float:
    """Convert value to 0-100 percentage scale.

    If value <= 1.0, assume it's a 0-1 fraction and multiply by 100.
    """
    value = float(value)
    if 0 < value <= 1.0:
        return value * 100.0
    return value

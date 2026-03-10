#!/usr/bin/env python3
"""Report generator for TACO adjustment results.

Generates both JSON and Markdown reports with:
    1. Trump Pain Index dashboard
    2. Intervention probability analysis
    3. Probability adjustment results (Before → After)
    4. Adjustment rationale
    5. Diminishing returns warning
    6. Key monitoring levels
"""

import json
import os
from datetime import datetime


def generate_json_report(
    pain_result: dict,
    impact_result: dict,
    adjustment_result: dict,
    market_data: dict | None,
    output_path: str,
) -> str:
    """Generate JSON report.

    Args:
        pain_result: Output of calculate_pain_index().
        impact_result: Output of effective_impact().
        adjustment_result: Output of adjust_probabilities().
        market_data: Optional FMP market data dict.
        output_path: File path for JSON output.

    Returns:
        Path to generated file.
    """
    report = {
        "schema_version": "1.0",
        "metadata": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "skill": "trump-mean-reversion",
        },
        "pain_index": pain_result,
        "intervention": impact_result,
        "probability_adjustment": adjustment_result,
        "market_data": market_data,
    }

    os.makedirs(
        os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
        exist_ok=True,
    )
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)

    return output_path


def generate_markdown_report(
    pain_result: dict,
    impact_result: dict,
    adjustment_result: dict,
    market_data: dict | None,
    output_path: str,
) -> str:
    """Generate Markdown report.

    Args:
        pain_result: Output of calculate_pain_index().
        impact_result: Output of effective_impact().
        adjustment_result: Output of adjust_probabilities().
        market_data: Optional FMP market data dict.
        output_path: File path for Markdown output.

    Returns:
        Path to generated file.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pain = pain_result["pain_index"]
    zone = pain_result["zone"]

    lines = []

    # Header
    lines.append("# TACO Probability Adjustment Report")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Trump Pain Index:** {pain:.1f} / 100 ({zone})")
    lines.append(f"**Data Quality:** {pain_result['data_quality']['label']}")
    lines.append("")

    # Section 1: Pain Index Dashboard
    lines.append("## 1. Trump Pain Index Dashboard")
    lines.append("")
    lines.append("| Domain | Raw Value | Normalized | Weight | Contribution |")
    lines.append("|--------|-----------|------------|--------|-------------|")

    for domain, info in pain_result["domain_scores"].items():
        if info["available"]:
            raw = _format_raw_value(domain, info["raw_value"])
            norm = f"{info['normalized']:.2f}"
            weight = f"{info['weight']:.0%}"
            contrib = f"{info['contribution']:.1f}"
        else:
            raw = "N/A"
            norm = "-"
            weight = f"{info['weight']:.0%}"
            contrib = "-"
        lines.append(f"| {info['label']} | {raw} | {norm} | {weight} | {contrib} |")

    lines.append("")
    lines.append(f"**Composite Pain Index: {pain:.1f}**")
    lines.append("")
    lines.append(f"> {pain_result['zone_interpretation']}")
    lines.append("")

    # Section 2: Intervention Analysis
    lines.append("## 2. Intervention Probability Analysis")
    lines.append("")
    lines.append(f"- **Intervention Probability:** {impact_result['intervention_probability']:.1%}")
    lines.append(f"- **Intervention Type:** {impact_result['intervention_type']}")
    lines.append(f"- **Type Discount:** {impact_result['type_discount']:.0%}")
    lines.append(f"- **Prior Interventions:** {impact_result['intervention_count']}")
    lines.append(f"- **Diminishing Factor:** {impact_result['diminishing_factor']:.1%}")
    lines.append(f"- **Effective Impact:** {impact_result['effective_impact']:.1%}")
    lines.append("")

    if impact_result["intervention_count"] > 0:
        lines.append(
            f"> **Diminishing Returns Warning:** {impact_result['intervention_count']} "
            f"prior intervention(s) detected. Market response has been discounted by "
            f"{(1 - impact_result['diminishing_factor']) * 100:.0f}%."
        )
        lines.append("")

    # Section 3: Probability Adjustment
    lines.append("## 3. Probability Adjustment Results")
    lines.append("")
    orig = adjustment_result["original"]
    adj = adjustment_result["adjusted"]

    lines.append("| Scenario | Before | After | Change |")
    lines.append("|----------|--------|-------|--------|")
    for scenario in ("base", "bull", "bear"):
        before = orig[scenario]
        after = adj[scenario]
        change = after - before
        sign = "+" if change > 0 else ""
        lines.append(
            f"| {scenario.title()} | {before:.1f}% | {after:.1f}% | {sign}{change:.1f}pp |"
        )

    lines.append("")

    # Section 4: Adjustment Rationale
    if adjustment_result["adjustments"]:
        lines.append("## 4. Adjustment Rationale")
        lines.append("")
        for adj_detail in adjustment_result["adjustments"]:
            lines.append(f"- **Direction:** {adj_detail['direction']}")
            lines.append(f"- **Reason:** {adj_detail['reason']}")
            lines.append("")
    else:
        lines.append("## 4. Adjustment Rationale")
        lines.append("")
        lines.append("No significant adjustment applied (Pain Index in neutral zone).")
        lines.append("")

    # Section 5: Key Monitoring Levels
    lines.append("## 5. Key Monitoring Levels")
    lines.append("")
    lines.append("| Indicator | TACO Trigger | Current Zone |")
    lines.append("|-----------|-------------|-------------|")
    lines.append("| WTI Crude | > $90 | Pain escalation |")
    lines.append("| S&P 500 Drawdown | > -10% from ATH | Pain escalation |")
    lines.append("| 10Y Yield | > 5.0% | Pain escalation |")
    lines.append("| Geopolitics (manual) | > 7/10 | Pain escalation |")
    lines.append("| Trade Tensions (manual) | > 7/10 | Pain escalation |")
    lines.append("")

    # Market Data (if available)
    if market_data:
        lines.append("## 6. Market Data Snapshot")
        lines.append("")
        if "energy" in market_data:
            e = market_data["energy"]
            lines.append(
                f"- **USO:** ${e.get('price', 'N/A')} (WTI est: ${e.get('wti_estimate', 'N/A')})"
            )
        if "stock_market" in market_data:
            s = market_data["stock_market"]
            lines.append(
                f"- **S&P 500:** {s.get('price', 'N/A')} "
                f"(Year High: {s.get('year_high', 'N/A')}, "
                f"Drawdown: -{s.get('drawdown_pct', 'N/A')}%)"
            )
        if "interest_rates" in market_data:
            r = market_data["interest_rates"]
            lines.append(
                f"- **TLT:** ${r.get('tlt_price', 'N/A')} "
                f"(10Y yield est: {r.get('yield_estimate', 'N/A')}%)"
            )
        if "vix" in market_data:
            v = market_data["vix"]
            lines.append(f"- **VIX:** {v.get('price', 'N/A')}")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append(
        "*TACO Framework: Trump Always Chickens Out — a mean-reversion model "
        "for policy-driven tail risk clipping. See `references/taco_framework.md`.*"
    )
    lines.append("")

    os.makedirs(
        os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
        exist_ok=True,
    )
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return output_path


def _format_raw_value(domain: str, value) -> str:
    """Format raw domain value for display."""
    if value is None:
        return "N/A"
    if domain == "energy":
        return f"${value:.1f}"
    elif domain == "stock_market":
        return f"-{value:.1f}%"
    elif domain == "interest_rates":
        return f"{value:.2f}%"
    elif domain in ("geopolitics", "trade"):
        return f"{value:.0f}/10"
    return str(value)

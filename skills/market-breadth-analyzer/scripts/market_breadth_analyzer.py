#!/usr/bin/env python3
"""
Market Breadth Analyzer - Main Orchestrator

Quantifies market breadth health using a 6-component scoring system.
Supports two data sources:
  - csv (default): TraderMonty's public CSV data, no API key required.
  - fmp: FMP API self-calculated breadth, requires FMP_API_KEY.

Usage:
    # Default CSV mode (no API key):
    python3 market_breadth_analyzer.py

    # FMP self-calculation mode:
    python3 market_breadth_analyzer.py --source fmp

    # FMP with custom options:
    python3 market_breadth_analyzer.py --source fmp \\
        --api-key YOUR_KEY --max-api-calls 245 --output-dir ./reports

Output:
    - JSON: market_breadth_YYYY-MM-DD_HHMMSS.json
    - Markdown: market_breadth_YYYY-MM-DD_HHMMSS.md
"""

import argparse
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from calculators.bearish_signal_calculator import calculate_bearish_signal
from calculators.cycle_calculator import calculate_cycle_position
from calculators.divergence_calculator import calculate_divergence
from calculators.historical_context_calculator import calculate_historical_percentile
from calculators.ma_crossover_calculator import calculate_ma_crossover
from calculators.trend_level_calculator import calculate_breadth_level_trend
from csv_client import (
    DEFAULT_DETAIL_URL,
    DEFAULT_SUMMARY_URL,
    check_data_freshness,
    fetch_detail_csv,
    fetch_summary_csv,
)
from history_tracker import append_history, get_trend_summary
from report_generator import generate_json_report, generate_markdown_report
from scorer import calculate_composite_score


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Market Breadth Analyzer - 6-Component Health Scoring"
    )

    parser.add_argument(
        "--source",
        choices=["csv", "fmp"],
        default="csv",
        help="Data source: csv (default, no API) or fmp (FMP API self-calculated)",
    )
    parser.add_argument(
        "--detail-url",
        default=DEFAULT_DETAIL_URL,
        help="URL for detail CSV (csv mode only)",
    )
    parser.add_argument(
        "--summary-url",
        default=DEFAULT_SUMMARY_URL,
        help="URL for summary CSV (csv mode only)",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory for reports (default: current directory)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="FMP API key (fmp mode; fallback: $FMP_API_KEY)",
    )
    parser.add_argument(
        "--max-api-calls",
        type=int,
        default=245,
        help="Maximum FMP API calls per run (default: 245)",
    )
    parser.add_argument(
        "--cache-dir",
        default=None,
        help="Disk cache directory for FMP data (default: scripts/.breadth_cache/)",
    )
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=0.8,
        help="Minimum S&P 500 symbol coverage for FMP mode (default: 0.8)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    is_fmp = args.source == "fmp"
    source_label = "FMP Self-Calculated" if is_fmp else "No API Key Required"

    print("=" * 70)
    print("Market Breadth Analyzer")
    print(f"6-Component Health Scoring ({source_label})")
    print("=" * 70)
    print()

    # ========================================================================
    # Step 1: Fetch Data
    # ========================================================================
    if is_fmp:
        print("Step 1: Fetching FMP Data (Self-Calculated Breadth)")
        print("-" * 70)

        from fmp_breadth_client import FMPBreadthClient

        cache_dir = args.cache_dir or os.path.join(os.path.dirname(__file__), ".breadth_cache")
        client = FMPBreadthClient(
            api_key=args.api_key,
            cache_dir=cache_dir,
            max_api_calls=args.max_api_calls,
            min_coverage=args.min_coverage,
        )
        detail_rows, summary = client.calculate_breadth_data()
        if not detail_rows:
            print("ERROR: Cannot proceed without breadth data", file=sys.stderr)
            sys.exit(1)

        freshness = _fmp_freshness(detail_rows)
        if freshness.get("warning"):
            print(f"  WARNING: {freshness['warning']}")
        else:
            print(
                f"  Data freshness: OK "
                f"(latest: {freshness['latest_date']}, "
                f"{freshness['days_old']} days old)"
            )
    else:
        print("Step 1: Fetching CSV Data")
        print("-" * 70)

        detail_rows = fetch_detail_csv(args.detail_url)
        if not detail_rows:
            print("ERROR: Cannot proceed without detail CSV data", file=sys.stderr)
            sys.exit(1)

        summary = fetch_summary_csv(args.summary_url)

        freshness = check_data_freshness(detail_rows)
        if freshness.get("warning"):
            print(f"  WARNING: {freshness['warning']}")
        else:
            print(
                f"  Data freshness: OK "
                f"(latest: {freshness['latest_date']}, "
                f"{freshness['days_old']} days old)"
            )

    print()

    # ========================================================================
    # Step 2: Calculate Components
    # ========================================================================
    print("Step 2: Calculating Components")
    print("-" * 70)

    # Component 1: Current Breadth Level & Trend (25%)
    print("  [1/6] Current Breadth Level & Trend...", end=" ", flush=True)
    comp1 = calculate_breadth_level_trend(detail_rows)
    print(f"Score: {comp1['score']} ({comp1['signal']})")

    # Component 2: 8MA vs 200MA Crossover (20%)
    print("  [2/6] 8MA vs 200MA Crossover...", end=" ", flush=True)
    comp2 = calculate_ma_crossover(detail_rows)
    print(f"Score: {comp2['score']} ({comp2['signal']})")

    # Component 3: Peak/Trough Cycle Position (20%)
    print("  [3/6] Peak/Trough Cycle Position...", end=" ", flush=True)
    comp3 = calculate_cycle_position(detail_rows)
    print(f"Score: {comp3['score']} ({comp3['signal']})")

    # Component 4: Bearish Signal Status (15%)
    print("  [4/6] Bearish Signal Status...", end=" ", flush=True)
    comp4 = calculate_bearish_signal(detail_rows)
    print(f"Score: {comp4['score']} ({comp4['signal']})")

    # Component 5: Historical Percentile (10%)
    print("  [5/6] Historical Percentile...", end=" ", flush=True)
    comp5 = calculate_historical_percentile(detail_rows, summary)
    print(f"Score: {comp5['score']} ({comp5['signal']})")

    # Component 6: S&P 500 vs Breadth Divergence (10%)
    print("  [6/6] S&P 500 vs Breadth Divergence...", end=" ", flush=True)
    comp6 = calculate_divergence(detail_rows)
    print(f"Score: {comp6['score']} ({comp6['signal']})")

    print()

    # ========================================================================
    # Step 3: Composite Score
    # ========================================================================
    print("Step 3: Calculating Composite Score")
    print("-" * 70)

    component_scores = {
        "breadth_level_trend": comp1["score"],
        "ma_crossover": comp2["score"],
        "cycle_position": comp3["score"],
        "bearish_signal": comp4["score"],
        "historical_percentile": comp5["score"],
        "divergence": comp6["score"],
    }

    data_availability = {
        "breadth_level_trend": comp1.get("data_available", True),
        "ma_crossover": comp2.get("data_available", True),
        "cycle_position": comp3.get("data_available", True),
        "bearish_signal": comp4.get("data_available", True),
        "historical_percentile": comp5.get("data_available", True),
        "divergence": comp6.get("data_available", True),
    }

    composite = calculate_composite_score(component_scores, data_availability)

    print(f"  Composite Score: {composite['composite_score']}/100")
    print(f"  Health Zone: {composite['zone']}")
    print(f"  Equity Exposure: {composite['exposure_guidance']}")
    print(
        f"  Strongest: {composite['strongest_health']['label']} "
        f"({composite['strongest_health']['score']})"
    )
    print(
        f"  Weakest: {composite['weakest_health']['label']} "
        f"({composite['weakest_health']['score']})"
    )
    print()

    # ========================================================================
    # Step 3.5: Score History & Trend
    # ========================================================================
    data_date = detail_rows[-1]["Date"]
    history_file = os.path.join(args.output_dir, "market_breadth_history.json")
    updated_history = append_history(
        history_file,
        composite["composite_score"],
        component_scores,
        data_date,
    )
    trend_summary = get_trend_summary(updated_history)
    if trend_summary["direction"] != "stable" and len(trend_summary["entries"]) >= 2:
        print(
            f"  Score Trend: {trend_summary['direction']} "
            f"(delta {trend_summary['delta']:+.1f} over "
            f"{len(trend_summary['entries'])} observations)"
        )
    print()

    # ========================================================================
    # Step 4: Key Levels
    # ========================================================================
    key_levels = _compute_key_levels(detail_rows, summary)

    # ========================================================================
    # Step 5: Generate Reports
    # ========================================================================
    print("Step 4: Generating Reports")
    print("-" * 70)

    if is_fmp:
        metadata = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "FMP Self-Calculated (S&P 500 constituent prices)",
            "total_rows": len(detail_rows),
            "data_freshness": freshness,
            "api_stats": client.get_api_stats(),
        }
    else:
        metadata = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "TraderMonty Market Breadth CSV",
            "detail_url": args.detail_url,
            "summary_url": args.summary_url,
            "total_rows": len(detail_rows),
            "data_freshness": freshness,
        }

    analysis = {
        "metadata": metadata,
        "composite": composite,
        "components": {
            "breadth_level_trend": comp1,
            "ma_crossover": comp2,
            "cycle_position": comp3,
            "bearish_signal": comp4,
            "historical_percentile": comp5,
            "divergence": comp6,
        },
        "trend_summary": trend_summary,
        "key_levels": key_levels,
    }

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_file = os.path.join(args.output_dir, f"market_breadth_{timestamp}.json")
    md_file = os.path.join(args.output_dir, f"market_breadth_{timestamp}.md")

    generate_json_report(analysis, json_file)
    generate_markdown_report(analysis, md_file)

    print()
    print("=" * 70)
    print("Market Breadth Analysis Complete")
    print("=" * 70)
    print(f"  Composite Score: {composite['composite_score']}/100")
    print(f"  Health Zone: {composite['zone']}")
    print(f"  Equity Exposure: {composite['exposure_guidance']}")
    print(f"  JSON Report: {json_file}")
    print(f"  Markdown Report: {md_file}")
    print()


def _fmp_freshness(rows, max_stale_days=5):
    """Simple freshness check for FMP-computed data (no HTTP header check)."""
    if not rows:
        return {
            "is_fresh": False,
            "latest_date": None,
            "days_old": None,
            "last_modified": None,
            "warning": "No data available",
        }
    latest_date_str = rows[-1]["Date"]
    try:
        latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")
    except ValueError:
        return {
            "is_fresh": False,
            "latest_date": latest_date_str,
            "days_old": None,
            "last_modified": None,
            "warning": f"Cannot parse latest date: {latest_date_str}",
        }
    days_old = (datetime.now() - latest_date).days
    is_fresh = days_old <= max_stale_days
    warning = None
    if not is_fresh:
        warning = (
            f"Data is {days_old} days old (latest: {latest_date_str}). "
            f"Threshold: {max_stale_days} days. Results may not reflect current conditions."
        )
    return {
        "is_fresh": is_fresh,
        "latest_date": latest_date_str,
        "days_old": days_old,
        "last_modified": None,
        "warning": warning,
    }


def _compute_key_levels(rows, summary):
    """Compute key breadth levels to watch."""
    if not rows:
        return {}

    latest = rows[-1]
    latest["Breadth_Index_8MA"]
    ma200 = latest["Breadth_Index_200MA"]

    levels = {}

    # 200MA crossover level
    levels["200MA Level"] = {
        "value": f"{ma200:.4f}",
        "significance": (
            "Key support/resistance for 8MA. "
            "8MA crossing below is an early warning of deterioration, "
            "not a standalone bearish signal."
        ),
    }

    # 0.40 extreme weakness threshold
    levels["Extreme Weakness (0.40)"] = {
        "value": "0.4000",
        "significance": (
            "8MA below 0.40 marks extreme weakness. "
            "Historically, troughs at this level precede significant rallies."
        ),
    }

    # 0.60 healthy threshold
    levels["Healthy Threshold (0.60)"] = {
        "value": "0.6000",
        "significance": (
            "8MA above 0.60 indicates broad participation. "
            "Below 0.60 = selective market, above = inclusive rally."
        ),
    }

    # Average peak from summary
    avg_peak_str = summary.get("Average Peaks (200MA)", "")
    try:
        avg_peak = float(avg_peak_str)
        levels["Historical Avg Peak"] = {
            "value": f"{avg_peak:.3f}",
            "significance": (
                "Average peak level. Approaching this level suggests "
                "breadth may be near a cyclical high."
            ),
        }
    except (ValueError, TypeError):
        pass

    # Average trough from summary
    avg_trough_str = summary.get("Average Troughs (8MA < 0.4)", "")
    try:
        avg_trough = float(avg_trough_str)
        levels["Historical Avg Trough"] = {
            "value": f"{avg_trough:.3f}",
            "significance": (
                "Average extreme trough level. Reaching this level "
                "is a potential contrarian buy signal."
            ),
        }
    except (ValueError, TypeError):
        pass

    return levels


if __name__ == "__main__":
    main()

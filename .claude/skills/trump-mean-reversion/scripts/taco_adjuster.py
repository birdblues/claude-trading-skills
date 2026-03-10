#!/usr/bin/env python3
"""TACO Probability Adjuster — CLI entry point.

Adjusts Base/Bull/Bear scenario probabilities based on the Trump Pain Index
and TACO (Trump Always Chickens Out) intervention model.

Usage:
    # From scenario JSON (primary usage — called by upstream skills)
    python3 taco_adjuster.py --scenario-json reports/scenario_analysis.json \\
        --geopolitics 7 --trade 5 --output-dir reports/

    # With FMP real-time data
    python3 taco_adjuster.py --scenario-json reports/scenario_analysis.json \\
        --use-fmp --geopolitics 7 --trade 5 --output-dir reports/

    # Manual probability input
    python3 taco_adjuster.py --base 40 --bull 15 --bear 45 \\
        --geopolitics 7 --trade 5 --output-dir reports/

Output:
    - JSON: taco_adjustment_YYYY-MM-DD_HHMMSS.json
    - Markdown: taco_adjustment_YYYY-MM-DD_HHMMSS.md
"""

import argparse
import os
import sys
from datetime import datetime

# Add parent directory for local imports
sys.path.insert(0, os.path.dirname(__file__))

from intervention_model import effective_impact
from pain_index import calculate_pain_index
from probability_adjuster import adjust_probabilities
from report_generator import generate_json_report, generate_markdown_report
from scenario_parser import from_cli_args, parse_scenario_json, parse_scenario_markdown


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="TACO Probability Adjuster — adjust scenario probabilities "
        "based on Trump Pain Index"
    )

    # Scenario input (mutually supportive, not exclusive)
    scenario_group = parser.add_argument_group("Scenario Input")
    scenario_group.add_argument(
        "--scenario-json",
        default=None,
        help="Path to scenario analysis JSON file",
    )
    scenario_group.add_argument(
        "--scenario-md",
        default=None,
        help="Path to scenario analysis Markdown file",
    )
    scenario_group.add_argument(
        "--base", type=float, default=None, help="Base case probability (0-100)"
    )
    scenario_group.add_argument(
        "--bull", type=float, default=None, help="Bull case probability (0-100)"
    )
    scenario_group.add_argument(
        "--bear", type=float, default=None, help="Bear case probability (0-100)"
    )

    # Pain Index inputs
    pain_group = parser.add_argument_group("Pain Index Inputs")
    pain_group.add_argument(
        "--energy",
        type=float,
        default=None,
        help="WTI oil price in USD (or USO price if --uso-direct)",
    )
    pain_group.add_argument(
        "--stock-drawdown",
        type=float,
        default=None,
        help="S&P 500 drawdown from ATH in %% (e.g. 10 = -10%%)",
    )
    pain_group.add_argument(
        "--geopolitics",
        type=float,
        default=5.0,
        help="Geopolitical tension score 1-10 (default: 5)",
    )
    pain_group.add_argument(
        "--trade",
        type=float,
        default=5.0,
        help="Trade/tariff tension score 1-10 (default: 5)",
    )
    pain_group.add_argument(
        "--interest-rate",
        type=float,
        default=None,
        help="10Y yield in %% (e.g. 4.5)",
    )

    # FMP option
    parser.add_argument(
        "--use-fmp",
        action="store_true",
        help="Fetch Energy, Stock Market, Interest Rate data from FMP API",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="FMP API key (fallback: $FMP_API_KEY)",
    )

    # Intervention parameters
    intervention_group = parser.add_argument_group("Intervention Parameters")
    intervention_group.add_argument(
        "--intervention-count",
        type=int,
        default=0,
        help="Number of prior interventions in this domain (default: 0)",
    )
    intervention_group.add_argument(
        "--intervention-type",
        choices=["verbal", "executive_order", "policy_action"],
        default="verbal",
        help="Expected intervention type (default: verbal)",
    )

    # Output
    parser.add_argument(
        "--output-dir",
        default="reports/",
        help="Output directory for reports (default: reports/)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    os.makedirs(args.output_dir, exist_ok=True)

    # Step 1: Parse scenario probabilities
    scenario = None
    if args.scenario_json:
        scenario = parse_scenario_json(args.scenario_json)
        if scenario:
            print(f"Loaded scenario from: {args.scenario_json}", file=sys.stderr)
    if scenario is None and args.scenario_md:
        scenario = parse_scenario_markdown(args.scenario_md)
        if scenario:
            print(f"Loaded scenario from: {args.scenario_md}", file=sys.stderr)
    if scenario is None:
        scenario = from_cli_args(args.base, args.bull, args.bear)

    if scenario is None:
        print(
            "ERROR: No scenario probabilities provided. Use --scenario-json, "
            "--scenario-md, or --base/--bull/--bear.",
            file=sys.stderr,
        )
        sys.exit(1)

    base_prob = scenario["base"]
    bull_prob = scenario["bull"]
    bear_prob = scenario["bear"]
    print(
        f"Input probabilities: Base={base_prob:.1f}%, Bull={bull_prob:.1f}%, Bear={bear_prob:.1f}%",
        file=sys.stderr,
    )

    # Step 2: Gather Pain Index domain data
    domain_values = {
        "geopolitics": args.geopolitics,
        "trade": args.trade,
    }
    market_data = None

    if args.use_fmp:
        market_data = _fetch_fmp_data(args.api_key)
        if market_data:
            if "energy" in market_data:
                domain_values["energy"] = market_data["energy"]["wti_estimate"]
            if "stock_market" in market_data:
                domain_values["stock_market"] = market_data["stock_market"]["drawdown_pct"]
            if "interest_rates" in market_data:
                domain_values["interest_rates"] = market_data["interest_rates"]["yield_estimate"]

    # Override with manual inputs if provided
    if args.energy is not None:
        domain_values["energy"] = args.energy
    if args.stock_drawdown is not None:
        domain_values["stock_market"] = args.stock_drawdown
    if args.interest_rate is not None:
        domain_values["interest_rates"] = args.interest_rate

    # Step 3: Calculate Pain Index
    pain_result = calculate_pain_index(domain_values)
    print(
        f"Pain Index: {pain_result['pain_index']:.1f} ({pain_result['zone']})",
        file=sys.stderr,
    )

    # Step 4: Calculate intervention impact
    impact_result = effective_impact(
        pain_index=pain_result["pain_index"],
        intervention_count=args.intervention_count,
        intervention_type=args.intervention_type,
    )

    # Step 5: Adjust probabilities
    adjustment_result = adjust_probabilities(
        base=base_prob,
        bull=bull_prob,
        bear=bear_prob,
        pain_index=pain_result["pain_index"],
        effective_impact=impact_result["effective_impact"],
        intervention_count=args.intervention_count,
        intervention_type=args.intervention_type,
    )

    adj = adjustment_result["adjusted"]
    print(
        f"Adjusted probabilities: Base={adj['base']:.1f}%, Bull={adj['bull']:.1f}%, Bear={adj['bear']:.1f}%",
        file=sys.stderr,
    )

    # Step 6: Generate reports
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    json_path = os.path.join(args.output_dir, f"taco_adjustment_{timestamp}.json")
    md_path = os.path.join(args.output_dir, f"taco_adjustment_{timestamp}.md")

    generate_json_report(pain_result, impact_result, adjustment_result, market_data, json_path)
    generate_markdown_report(pain_result, impact_result, adjustment_result, market_data, md_path)

    print(f"JSON report: {json_path}", file=sys.stderr)
    print(f"Markdown report: {md_path}", file=sys.stderr)

    # Output JSON path to stdout for pipeline consumption
    print(json_path)


def _fetch_fmp_data(api_key=None):
    """Fetch market data from FMP API."""
    try:
        from fmp_client import FMPClient

        client = FMPClient(api_key=api_key)
        return client.fetch_pain_domain_data()
    except ValueError as e:
        print(f"WARNING: FMP client error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"WARNING: FMP fetch failed: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    main()

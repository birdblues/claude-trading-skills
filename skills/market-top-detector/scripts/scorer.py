#!/usr/bin/env python3
"""
Market Top Detector - Composite Scoring Engine

Combines 6 component scores into a weighted composite (0-100).

Component Weights:
1. Distribution Day Count:       25%
2. Leading Stock Health:         20%
3. Defensive Sector Rotation:    15%
4. Market Breadth Divergence:    15%
5. Index Technical Condition:    15%
6. Sentiment & Speculation:      10%
Total: 100%

Risk Zone Mapping:
  0-20:  Green  (Normal)              - Risk Budget: 100%
  21-40: Yellow (Early Warning)       - Risk Budget: 80-90%
  41-60: Orange (Elevated Risk)       - Risk Budget: 60-75%
  61-80: Red    (High Probability Top)- Risk Budget: 40-55%
  81-100:Critical(Top Formation)      - Risk Budget: 20-35%
"""

from typing import Dict, List


COMPONENT_WEIGHTS = {
    "distribution_days": 0.25,
    "leading_stocks": 0.20,
    "defensive_rotation": 0.15,
    "breadth_divergence": 0.15,
    "index_technical": 0.15,
    "sentiment": 0.10,
}

COMPONENT_LABELS = {
    "distribution_days": "Distribution Day Count",
    "leading_stocks": "Leading Stock Health",
    "defensive_rotation": "Defensive Sector Rotation",
    "breadth_divergence": "Market Breadth Divergence",
    "index_technical": "Index Technical Condition",
    "sentiment": "Sentiment & Speculation",
}


def calculate_composite_score(component_scores: Dict[str, float]) -> Dict:
    """
    Calculate weighted composite market top probability score.

    Args:
        component_scores: Dict with keys matching COMPONENT_WEIGHTS,
                         each value 0-100

    Returns:
        Dict with composite_score, zone, risk_budget, guidance,
        weakest/strongest components, and component breakdown
    """
    # Calculate weighted composite
    composite = 0.0
    for key, weight in COMPONENT_WEIGHTS.items():
        score = component_scores.get(key, 0)
        composite += score * weight

    composite = round(composite, 1)

    # Identify strongest and weakest warning signals
    valid_scores = {k: v for k, v in component_scores.items()
                    if k in COMPONENT_WEIGHTS}

    if valid_scores:
        strongest_warning = max(valid_scores, key=valid_scores.get)
        weakest_warning = min(valid_scores, key=valid_scores.get)
    else:
        strongest_warning = "N/A"
        weakest_warning = "N/A"

    # Get zone interpretation
    zone_info = _interpret_zone(composite)

    return {
        "composite_score": composite,
        "zone": zone_info["zone"],
        "zone_color": zone_info["color"],
        "risk_budget": zone_info["risk_budget"],
        "guidance": zone_info["guidance"],
        "actions": zone_info["actions"],
        "strongest_warning": {
            "component": strongest_warning,
            "label": COMPONENT_LABELS.get(strongest_warning, strongest_warning),
            "score": valid_scores.get(strongest_warning, 0),
        },
        "weakest_warning": {
            "component": weakest_warning,
            "label": COMPONENT_LABELS.get(weakest_warning, weakest_warning),
            "score": valid_scores.get(weakest_warning, 0),
        },
        "component_scores": {
            k: {
                "score": component_scores.get(k, 0),
                "weight": w,
                "weighted_contribution": round(component_scores.get(k, 0) * w, 1),
                "label": COMPONENT_LABELS[k],
            }
            for k, w in COMPONENT_WEIGHTS.items()
        },
    }


def _interpret_zone(composite: float) -> Dict:
    """Map composite score to risk zone"""
    if composite <= 20:
        return {
            "zone": "Green (Normal)",
            "color": "green",
            "risk_budget": "100%",
            "guidance": "Normal market conditions. Maintain standard position management.",
            "actions": [
                "Normal position sizing",
                "Standard stop-loss levels",
                "New position entries allowed",
            ],
        }
    elif composite <= 40:
        return {
            "zone": "Yellow (Early Warning)",
            "color": "yellow",
            "risk_budget": "80-90%",
            "guidance": "Early warning signs detected. Tighten stops and reduce new entries.",
            "actions": [
                "Tighten stop-losses by 10-20%",
                "Reduce new position sizes by 25-50%",
                "Review weakest positions for exits",
                "Monitor distribution days closely",
            ],
        }
    elif composite <= 60:
        return {
            "zone": "Orange (Elevated Risk)",
            "color": "orange",
            "risk_budget": "60-75%",
            "guidance": "Elevated risk of correction. Begin profit-taking on weaker positions.",
            "actions": [
                "Take profits on weakest 25-30% of positions",
                "No new momentum entries",
                "Only quality stocks near support",
                "Raise cash allocation",
                "Watch for Follow-Through Day if market pulls back",
            ],
        }
    elif composite <= 80:
        return {
            "zone": "Red (High Probability Top)",
            "color": "red",
            "risk_budget": "40-55%",
            "guidance": "High probability of market top. Aggressive profit-taking recommended.",
            "actions": [
                "Aggressive profit-taking (sell 40-50% of positions)",
                "Maximum cash allocation",
                "Only hold strongest leaders",
                "Consider hedges (put options, inverse ETFs)",
                "Prepare short watchlist",
            ],
        }
    else:
        return {
            "zone": "Critical (Top Formation)",
            "color": "critical",
            "risk_budget": "20-35%",
            "guidance": "Top formation in progress. Maximum defensive posture.",
            "actions": [
                "Sell most positions (keep only 20-35% invested)",
                "Full hedge implementation",
                "Short positions on weakest leaders",
                "Preserve capital as primary objective",
                "Watch for capitulation/Follow-Through Day for re-entry",
            ],
        }


def detect_follow_through_day(index_history: List[Dict],
                              composite_score: float) -> Dict:
    """
    Detect Follow-Through Day (FTD) signal for bottom confirmation.
    Only relevant when composite > 40 (Orange zone or worse).

    O'Neil's FTD Rules:
    - After a market decline, identify Rally Attempt Day (first up day)
    - FTD occurs on day 4-7 of rally attempt
    - Requires significant price gain on higher volume

    Args:
        index_history: Daily OHLCV (most recent first)
        composite_score: Current composite score

    Returns:
        Dict with ftd_detected, rally_day_count, details
    """
    if composite_score < 40:
        return {
            "ftd_detected": False,
            "applicable": False,
            "reason": "Composite < 40 (Green/Yellow zone) - FTD monitoring not needed",
        }

    if not index_history or len(index_history) < 10:
        return {
            "ftd_detected": False,
            "applicable": True,
            "reason": "Insufficient data for FTD analysis",
        }

    # Find rally attempt start (first up day after decline)
    rally_start = None
    for i in range(min(20, len(index_history) - 1)):
        today_close = index_history[i].get("close", 0)
        yesterday_close = index_history[i + 1].get("close", 0)
        if yesterday_close > 0 and today_close > yesterday_close:
            # Count consecutive up days from here
            rally_start = i
            break

    if rally_start is None:
        return {
            "ftd_detected": False,
            "applicable": True,
            "reason": "No rally attempt detected in last 20 days",
            "rally_day_count": 0,
        }

    # Count rally days (consecutive closes above rally start close)
    rally_base = index_history[rally_start + 1].get("close", 0)
    rally_day_count = 0
    for j in range(rally_start, -1, -1):
        if index_history[j].get("close", 0) > rally_base:
            rally_day_count += 1
        else:
            break

    # Check for FTD on days 4-7
    ftd_detected = False
    ftd_day = None

    if rally_day_count >= 4:
        # Check days 4-7 for big up day on volume
        check_start = max(0, rally_start - 6)
        check_end = max(0, rally_start - 3)

        for k in range(check_start, check_end + 1):
            if k >= len(index_history) - 1:
                continue
            day = index_history[k]
            prev_day = index_history[k + 1]

            day_close = day.get("close", 0)
            prev_close = prev_day.get("close", 0)
            day_volume = day.get("volume", 0)
            prev_volume = prev_day.get("volume", 0)

            if prev_close == 0:
                continue

            gain_pct = (day_close - prev_close) / prev_close * 100
            volume_up = day_volume > prev_volume

            # FTD: gain >= 1.5% on higher volume
            if gain_pct >= 1.5 and volume_up:
                ftd_detected = True
                ftd_day = day.get("date", f"day-{k}")
                break

    return {
        "ftd_detected": ftd_detected,
        "applicable": True,
        "rally_day_count": rally_day_count,
        "ftd_day": ftd_day,
        "reason": (
            f"Follow-Through Day detected on {ftd_day}" if ftd_detected
            else f"Rally attempt: Day {rally_day_count} (FTD requires day 4-7 with strong gain on volume)"
        ),
    }


# Testing
if __name__ == "__main__":
    print("Testing Market Top Scorer...\n")

    # Test 1: Moderate risk scenario (calibration target: ~50)
    test_scores = {
        "distribution_days": 45,
        "leading_stocks": 52,
        "defensive_rotation": 82,
        "breadth_divergence": 20,
        "index_technical": 42,
        "sentiment": 62,
    }

    result = calculate_composite_score(test_scores)
    print(f"Test 1 - Moderate Risk:")
    print(f"  Composite: {result['composite_score']}/100")
    print(f"  Zone: {result['zone']}")
    print(f"  Risk Budget: {result['risk_budget']}")
    print(f"  Strongest Warning: {result['strongest_warning']['label']} "
          f"({result['strongest_warning']['score']})")
    print()

    # Test 2: Healthy market
    healthy = {
        "distribution_days": 0,
        "leading_stocks": 10,
        "defensive_rotation": 0,
        "breadth_divergence": 10,
        "index_technical": 5,
        "sentiment": 15,
    }
    result2 = calculate_composite_score(healthy)
    print(f"Test 2 - Healthy Market:")
    print(f"  Composite: {result2['composite_score']}/100")
    print(f"  Zone: {result2['zone']}")
    print()

    # Test 3: Crisis
    crisis = {
        "distribution_days": 100,
        "leading_stocks": 90,
        "defensive_rotation": 85,
        "breadth_divergence": 80,
        "index_technical": 75,
        "sentiment": 70,
    }
    result3 = calculate_composite_score(crisis)
    print(f"Test 3 - Crisis:")
    print(f"  Composite: {result3['composite_score']}/100")
    print(f"  Zone: {result3['zone']}")
    print()

    print("All tests completed.")

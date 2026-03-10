#!/usr/bin/env python3
"""Trump Pain Index calculator (0-100).

Computes a weighted composite score across 5 domains that represent
political pain for the administration. Higher values indicate greater
likelihood of policy reversal (TACO event).

Domains and weights:
    Energy/Oil   30%  — WTI proxy (USO) via FMP
    Stock Market 25%  — S&P 500 drawdown from ATH
    Geopolitics  20%  — Manual input (1-10)
    Trade/Tariffs 15% — Manual input (1-10)
    Interest Rates 10% — 10Y yield proxy (TLT) via FMP
"""

import math
from typing import Optional

# Domain weights (must sum to 1.0)
DOMAIN_WEIGHTS = {
    "energy": 0.30,
    "stock_market": 0.25,
    "geopolitics": 0.20,
    "trade": 0.15,
    "interest_rates": 0.10,
}

DOMAIN_LABELS = {
    "energy": "Energy / Oil",
    "stock_market": "Stock Market",
    "geopolitics": "Geopolitics",
    "trade": "Trade / Tariffs",
    "interest_rates": "Interest Rates",
}

# Sigmoid normalization parameters per domain
# midpoint: value where normalized score = 0.5
# steepness: higher = sharper transition
DOMAIN_THRESHOLDS = {
    "energy": {"midpoint": 90.0, "steepness": 0.08},  # WTI price
    "stock_market": {"midpoint": 10.0, "steepness": 0.30},  # % drawdown from ATH
    "geopolitics": {"midpoint": 5.0, "steepness": 0.60},  # 1-10 scale
    "trade": {"midpoint": 5.0, "steepness": 0.60},  # 1-10 scale
    "interest_rates": {"midpoint": 5.0, "steepness": 1.00},  # 10Y yield %
}


def sigmoid_normalize(value: float, midpoint: float, steepness: float) -> float:
    """Normalize a domain value to 0-1 using a logistic sigmoid.

    Args:
        value: Raw domain value.
        midpoint: Value at which output is 0.5.
        steepness: Controls transition sharpness.

    Returns:
        Normalized score in [0, 1].
    """
    x = steepness * (value - midpoint)
    # Clamp to avoid overflow
    x = max(-500.0, min(500.0, x))
    return 1.0 / (1.0 + math.exp(-x))


def calculate_domain_score(domain: str, value: float) -> float:
    """Calculate normalized pain score for a single domain.

    Args:
        domain: One of the DOMAIN_WEIGHTS keys.
        value: Raw value for the domain.

    Returns:
        Pain score in [0, 1].

    Raises:
        ValueError: If domain is unknown.
    """
    if domain not in DOMAIN_THRESHOLDS:
        raise ValueError(f"Unknown domain: {domain}. Must be one of {list(DOMAIN_THRESHOLDS)}")
    params = DOMAIN_THRESHOLDS[domain]
    return sigmoid_normalize(value, params["midpoint"], params["steepness"])


def calculate_pain_index(
    domain_values: dict[str, float],
    data_availability: Optional[dict[str, bool]] = None,
) -> dict:
    """Calculate the composite Trump Pain Index.

    Args:
        domain_values: Dict mapping domain name to raw value.
            Required keys depend on data_availability.
            - energy: WTI price (USD)
            - stock_market: Drawdown from ATH (%, positive number e.g. 10 = -10%)
            - geopolitics: Manual score 1-10
            - trade: Manual score 1-10
            - interest_rates: 10Y yield (%)
        data_availability: Optional dict indicating which domains have data.
            Defaults to True for all domains present in domain_values.

    Returns:
        Dict with:
            - pain_index: Composite score 0-100
            - zone: "Low" | "Medium" | "High"
            - zone_interpretation: Human-readable guidance
            - domain_scores: Per-domain breakdown
            - data_quality: Availability info
    """
    if data_availability is None:
        data_availability = {d: d in domain_values for d in DOMAIN_WEIGHTS}

    # Calculate per-domain scores
    domain_scores = {}
    for domain in DOMAIN_WEIGHTS:
        available = data_availability.get(domain, domain in domain_values)
        if available and domain in domain_values:
            raw = domain_values[domain]
            normalized = calculate_domain_score(domain, raw)
            domain_scores[domain] = {
                "raw_value": raw,
                "normalized": round(normalized, 4),
                "weight": DOMAIN_WEIGHTS[domain],
                "label": DOMAIN_LABELS[domain],
                "available": True,
            }
        else:
            domain_scores[domain] = {
                "raw_value": None,
                "normalized": 0.0,
                "weight": DOMAIN_WEIGHTS[domain],
                "label": DOMAIN_LABELS[domain],
                "available": False,
            }

    # Redistribute weights from unavailable domains
    available_weight = sum(
        DOMAIN_WEIGHTS[d] for d in DOMAIN_WEIGHTS if domain_scores[d]["available"]
    )

    if available_weight <= 0:
        pain_index = 50.0  # Default when no data
    else:
        pain_index = 0.0
        for domain, info in domain_scores.items():
            if info["available"]:
                effective_weight = info["weight"] / available_weight
                info["effective_weight"] = round(effective_weight, 4)
                contribution = info["normalized"] * effective_weight * 100
                info["contribution"] = round(contribution, 2)
                pain_index += contribution
            else:
                info["effective_weight"] = 0.0
                info["contribution"] = 0.0

    pain_index = round(max(0.0, min(100.0, pain_index)), 1)

    # Zone classification
    zone_info = _classify_zone(pain_index)

    available_count = sum(1 for d in domain_scores.values() if d["available"])
    total = len(DOMAIN_WEIGHTS)

    return {
        "pain_index": pain_index,
        "zone": zone_info["zone"],
        "zone_interpretation": zone_info["interpretation"],
        "zone_action": zone_info["action"],
        "domain_scores": domain_scores,
        "data_quality": {
            "available_count": available_count,
            "total_count": total,
            "label": (
                f"Complete ({available_count}/{total})"
                if available_count == total
                else f"Partial ({available_count}/{total})"
            ),
        },
    }


def _classify_zone(pain_index: float) -> dict:
    """Map Pain Index to zone with interpretation."""
    if pain_index < 30:
        return {
            "zone": "Low",
            "interpretation": (
                "Administration in attack mode. Expect aggressive policy actions "
                "(tariff escalation, geopolitical pressure). Bull-side clipping likely."
            ),
            "action": "Reduce Bull scenario probability — policy aggression may cap upside.",
        }
    elif pain_index < 60:
        return {
            "zone": "Medium",
            "interpretation": (
                "Moderate political stress. Administration may oscillate between "
                "aggression and concession. Watch for mixed signals."
            ),
            "action": "Minor adjustments only — situation is ambiguous.",
        }
    else:
        return {
            "zone": "High",
            "interpretation": (
                "High political pain. TACO event likely — expect policy reversal, "
                "conciliatory statements, or executive action to ease pressure."
            ),
            "action": "Reduce Bear scenario probability — TACO intervention expected.",
        }

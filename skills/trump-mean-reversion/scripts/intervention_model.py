#!/usr/bin/env python3
"""Intervention probability engine with diminishing returns.

Models the probability that the administration will intervene to reverse
market pain, and the expected market impact of such intervention.
"""

import math
from typing import Optional

# Domain sensitivity — how responsive each domain is to intervention
DOMAIN_SENSITIVITY = {
    "energy": 1.2,  # Very sensitive — direct executive action possible
    "stock_market": 0.8,  # Moderate — indirect levers only
    "geopolitics": 1.0,  # Direct — verbal/diplomatic intervention
    "trade": 1.1,  # High — tariffs are executive-controlled
    "interest_rates": 0.5,  # Low — Fed is independent
}

# Intervention type effectiveness
INTERVENTION_TYPE_DISCOUNT = {
    "verbal": 0.3,  # Tweets, press conferences
    "executive_order": 0.7,  # Executive orders, waivers
    "policy_action": 1.0,  # Actual policy change
}


def intervention_probability(
    pain_index: float,
    domain: Optional[str] = None,
    midpoint: float = 50.0,
    steepness: float = 0.10,
) -> float:
    """Calculate probability of intervention given Pain Index.

    Args:
        pain_index: Composite Trump Pain Index (0-100).
        domain: Optional domain for sensitivity adjustment.
        midpoint: Pain level at which probability is 0.5.
        steepness: Sigmoid curve steepness.

    Returns:
        Intervention probability in [0, 1].
    """
    x = steepness * (pain_index - midpoint)
    x = max(-500.0, min(500.0, x))
    base_prob = 1.0 / (1.0 + math.exp(-x))

    if domain and domain in DOMAIN_SENSITIVITY:
        base_prob *= DOMAIN_SENSITIVITY[domain]

    return round(min(1.0, max(0.0, base_prob)), 4)


def diminishing_factor(intervention_count: int) -> float:
    """Calculate diminishing returns factor for repeated interventions.

    The market's response weakens with each successive intervention.

    Formula: 1.0 / (1.0 + 0.3 * count)

    Examples:
        0 interventions → 1.000 (full effect)
        1 intervention  → 0.769 (77%)
        2 interventions → 0.625 (63%)
        3 interventions → 0.526 (53%)
        5 interventions → 0.400 (40%)

    Args:
        intervention_count: Number of prior interventions in this domain.

    Returns:
        Factor in (0, 1] to multiply against expected impact.
    """
    if intervention_count < 0:
        intervention_count = 0
    return round(1.0 / (1.0 + 0.3 * intervention_count), 4)


def words_vs_actions_discount(intervention_type: str) -> float:
    """Return effectiveness discount based on intervention type.

    Markets discount verbal interventions heavily vs actual policy changes.

    Args:
        intervention_type: One of "verbal", "executive_order", "policy_action".

    Returns:
        Discount factor in [0.3, 1.0].

    Raises:
        ValueError: If intervention_type is unknown.
    """
    if intervention_type not in INTERVENTION_TYPE_DISCOUNT:
        raise ValueError(
            f"Unknown intervention type: {intervention_type}. "
            f"Must be one of {list(INTERVENTION_TYPE_DISCOUNT)}"
        )
    return INTERVENTION_TYPE_DISCOUNT[intervention_type]


def effective_impact(
    pain_index: float,
    domain: Optional[str] = None,
    intervention_count: int = 0,
    intervention_type: str = "verbal",
) -> dict:
    """Calculate the effective impact of a potential intervention.

    Combines intervention probability, diminishing returns, and
    words-vs-actions discount into a single effectiveness metric.

    Args:
        pain_index: Composite Trump Pain Index (0-100).
        domain: Optional domain for sensitivity weighting.
        intervention_count: Number of prior interventions.
        intervention_type: Type of intervention.

    Returns:
        Dict with probability, diminishing factor, type discount,
        and composite effective_impact (0-1).
    """
    prob = intervention_probability(pain_index, domain)
    dim_factor = diminishing_factor(intervention_count)
    type_discount = words_vs_actions_discount(intervention_type)

    composite = prob * dim_factor * type_discount

    return {
        "intervention_probability": prob,
        "diminishing_factor": dim_factor,
        "type_discount": type_discount,
        "effective_impact": round(min(1.0, composite), 4),
        "pain_index": pain_index,
        "domain": domain,
        "intervention_count": intervention_count,
        "intervention_type": intervention_type,
    }

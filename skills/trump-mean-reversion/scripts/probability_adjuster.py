#!/usr/bin/env python3
"""Scenario probability adjuster.

Adjusts Base/Bull/Bear probabilities from upstream skills (scenario-analyzer,
stanley-druckenmiller-investment) based on Trump Pain Index and intervention model.

Constraints:
    - Maximum total shift: +/-20 percentage points in one direction
    - Floor: 5% (no scenario below 5%)
    - Ceiling: 75% (no scenario above 75%)
    - Sum must equal 100%
"""

# Adjustment constraints
MAX_TOTAL_SHIFT = 20.0  # Maximum pp shift in one direction
PROB_FLOOR = 5.0  # Minimum probability for any scenario
PROB_CEILING = 75.0  # Maximum probability for any scenario


def adjust_probabilities(
    base: float,
    bull: float,
    bear: float,
    pain_index: float,
    effective_impact: float = 1.0,
    intervention_count: int = 0,
    intervention_type: str = "verbal",
) -> dict:
    """Adjust scenario probabilities based on TACO framework.

    High Pain (60-100): Bear shrinks (TACO intervention expected)
        → Freed probability redistributed to Base (60%) and Bull (40%)
    Low Pain (0-30): Bull shrinks (aggressive policy caps upside)
        → Freed probability redistributed to Base (60%) and Bear (40%)
    Medium Pain (30-60): Minor adjustment only

    Args:
        base: Base case probability (0-100 scale).
        bull: Bull case probability (0-100 scale).
        bear: Bear case probability (0-100 scale).
        pain_index: Trump Pain Index (0-100).
        effective_impact: Combined impact factor from intervention_model (0-1).
        intervention_count: Prior interventions (for reporting).
        intervention_type: Type of intervention (for reporting).

    Returns:
        Dict with adjusted probabilities and adjustment details.
    """
    # Validate inputs
    total = base + bull + bear
    if abs(total - 100.0) > 1.0:
        raise ValueError(f"Probabilities must sum to ~100%. Got {base}+{bull}+{bear}={total}")

    # Normalize to exactly 100 if close
    if total != 100.0:
        factor = 100.0 / total
        base *= factor
        bull *= factor
        bear *= factor

    # Calculate raw shift magnitude based on pain zone
    raw_shift = _calculate_raw_shift(pain_index)

    # Apply effective impact (diminishing returns + type discount)
    actual_shift = raw_shift * effective_impact

    # Cap at MAX_TOTAL_SHIFT
    actual_shift = min(actual_shift, MAX_TOTAL_SHIFT)

    # Apply directional adjustment
    adjustments = []
    new_base = base
    new_bull = bull
    new_bear = bear

    if pain_index >= 60:
        # High Pain → TACO likely → reduce Bear, boost Base & Bull
        bear_reduction = min(actual_shift, bear - PROB_FLOOR)
        bear_reduction = max(0.0, bear_reduction)
        new_bear = bear - bear_reduction
        new_base = base + bear_reduction * 0.6
        new_bull = bull + bear_reduction * 0.4
        adjustments.append(
            {
                "direction": "bear_clip",
                "reason": f"High Pain Index ({pain_index:.1f}) — TACO intervention expected",
                "bear_change": -round(bear_reduction, 2),
                "base_change": round(bear_reduction * 0.6, 2),
                "bull_change": round(bear_reduction * 0.4, 2),
            }
        )
    elif pain_index <= 30:
        # Low Pain → aggressive policy → reduce Bull, boost Base & Bear
        bull_reduction = min(actual_shift, bull - PROB_FLOOR)
        bull_reduction = max(0.0, bull_reduction)
        new_bull = bull - bull_reduction
        new_base = base + bull_reduction * 0.6
        new_bear = bear + bull_reduction * 0.4
        adjustments.append(
            {
                "direction": "bull_clip",
                "reason": f"Low Pain Index ({pain_index:.1f}) — aggressive policy expansion expected",
                "bull_change": -round(bull_reduction, 2),
                "base_change": round(bull_reduction * 0.6, 2),
                "bear_change": round(bull_reduction * 0.4, 2),
            }
        )
    else:
        # Medium Pain → minor adjustment
        micro_shift = actual_shift * 0.3  # Only 30% of computed shift
        if pain_index >= 45:
            # Slightly toward TACO
            bear_reduction = min(micro_shift, bear - PROB_FLOOR)
            bear_reduction = max(0.0, bear_reduction)
            new_bear = bear - bear_reduction
            new_base = base + bear_reduction
            if bear_reduction > 0:
                adjustments.append(
                    {
                        "direction": "mild_bear_clip",
                        "reason": f"Medium-high Pain ({pain_index:.1f}) — mild TACO lean",
                        "bear_change": -round(bear_reduction, 2),
                        "base_change": round(bear_reduction, 2),
                        "bull_change": 0.0,
                    }
                )
        else:
            # Slightly toward aggression
            bull_reduction = min(micro_shift, bull - PROB_FLOOR)
            bull_reduction = max(0.0, bull_reduction)
            new_bull = bull - bull_reduction
            new_base = base + bull_reduction
            if bull_reduction > 0:
                adjustments.append(
                    {
                        "direction": "mild_bull_clip",
                        "reason": f"Medium-low Pain ({pain_index:.1f}) — mild aggression lean",
                        "bull_change": -round(bull_reduction, 2),
                        "base_change": round(bull_reduction, 2),
                        "bear_change": 0.0,
                    }
                )

    # Apply constraints then redistribute excess/deficit to unclamped scenarios
    new_base, new_bull, new_bear = _constrained_normalize(new_base, new_bull, new_bear)

    return {
        "original": {
            "base": round(base, 1),
            "bull": round(bull, 1),
            "bear": round(bear, 1),
        },
        "adjusted": {
            "base": round(new_base, 1),
            "bull": round(new_bull, 1),
            "bear": round(new_bear, 1),
        },
        "pain_index": round(pain_index, 1),
        "effective_impact": round(effective_impact, 4),
        "raw_shift": round(raw_shift, 2),
        "actual_shift": round(actual_shift, 2),
        "adjustments": adjustments,
        "intervention_count": intervention_count,
        "intervention_type": intervention_type,
    }


def _calculate_raw_shift(pain_index: float) -> float:
    """Calculate raw shift magnitude from Pain Index.

    Maps pain to a 0-20 pp shift using a piecewise linear function:
        Pain 0-30  (Low):    shift = pain/30 * 15  → up to 15pp
        Pain 30-60 (Medium): shift = 3 + (pain-30)/30 * 5  → 3-8pp
        Pain 60-100 (High):  shift = (pain-40)/60 * 20  → up to 20pp
    """
    if pain_index <= 30:
        return (pain_index / 30.0) * 15.0
    elif pain_index <= 60:
        return 3.0 + ((pain_index - 30.0) / 30.0) * 5.0
    else:
        return ((pain_index - 40.0) / 60.0) * 20.0


def _constrained_normalize(base: float, bull: float, bear: float) -> tuple[float, float, float]:
    """Normalize to 100 while respecting floor/ceiling constraints.

    Clamps each value to [PROB_FLOOR, PROB_CEILING], then redistributes
    any excess or deficit to the unclamped scenarios proportionally.
    """
    vals = {"base": base, "bull": bull, "bear": bear}

    for _ in range(10):
        # Clamp
        clamped = set()
        for k in vals:
            if vals[k] < PROB_FLOOR:
                vals[k] = PROB_FLOOR
                clamped.add(k)
            elif vals[k] > PROB_CEILING:
                vals[k] = PROB_CEILING
                clamped.add(k)

        total = sum(vals.values())
        residual = 100.0 - total

        if abs(residual) < 0.05:
            break

        # Distribute residual to unclamped scenarios
        free = [k for k in vals if k not in clamped]
        if not free:
            # All clamped — distribute to the one with most room
            if residual > 0:
                free = [max(vals, key=lambda k: PROB_CEILING - vals[k])]
            else:
                free = [max(vals, key=lambda k: vals[k] - PROB_FLOOR)]

        share = residual / len(free)
        for k in free:
            vals[k] += share

    # Final rounding
    vals = {k: round(v, 1) for k, v in vals.items()}
    residual = round(100.0 - sum(vals.values()), 1)
    if abs(residual) > 0.05:
        # Add to largest unclamped bucket
        target = max(vals, key=lambda k: vals[k] if vals[k] < PROB_CEILING else 0)
        vals[target] = round(vals[target] + residual, 1)

    return vals["base"], vals["bull"], vals["bear"]

"""Tests for probability adjuster."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from probability_adjuster import (
    PROB_CEILING,
    PROB_FLOOR,
    adjust_probabilities,
)


class TestAdjustProbabilities:
    """Tests for the main probability adjustment function."""

    def test_high_pain_reduces_bear(self):
        """High Pain Index should reduce Bear probability."""
        result = adjust_probabilities(
            base=40,
            bull=15,
            bear=45,
            pain_index=80,
            effective_impact=1.0,
        )
        assert result["adjusted"]["bear"] < 45
        assert result["adjusted"]["base"] > 40

    def test_low_pain_reduces_bull(self):
        """Low Pain Index should reduce Bull probability."""
        result = adjust_probabilities(
            base=40,
            bull=30,
            bear=30,
            pain_index=15,
            effective_impact=1.0,
        )
        assert result["adjusted"]["bull"] < 30
        assert result["adjusted"]["base"] > 40

    def test_medium_pain_minor_adjustment(self):
        """Medium Pain Index should make only minor adjustments."""
        result = adjust_probabilities(
            base=50,
            bull=25,
            bear=25,
            pain_index=45,
            effective_impact=1.0,
        )
        # Changes should be small
        orig = result["original"]
        adj = result["adjusted"]
        for scenario in ("base", "bull", "bear"):
            assert abs(adj[scenario] - orig[scenario]) < 5

    def test_sum_equals_100(self):
        """Adjusted probabilities must sum to 100."""
        result = adjust_probabilities(
            base=40,
            bull=15,
            bear=45,
            pain_index=80,
            effective_impact=1.0,
        )
        adj = result["adjusted"]
        total = adj["base"] + adj["bull"] + adj["bear"]
        assert abs(total - 100.0) < 0.5

    def test_floor_constraint(self):
        """No scenario should go below PROB_FLOOR."""
        result = adjust_probabilities(
            base=50,
            bull=5,
            bear=45,
            pain_index=10,
            effective_impact=1.0,
        )
        adj = result["adjusted"]
        for scenario in ("base", "bull", "bear"):
            assert adj[scenario] >= PROB_FLOOR - 0.5  # Allow rounding tolerance

    def test_ceiling_constraint(self):
        """No scenario should exceed PROB_CEILING."""
        result = adjust_probabilities(
            base=70,
            bull=5,
            bear=25,
            pain_index=80,
            effective_impact=1.0,
        )
        adj = result["adjusted"]
        for scenario in ("base", "bull", "bear"):
            assert adj[scenario] <= PROB_CEILING + 0.5

    def test_diminished_impact_reduces_shift(self):
        """Lower effective_impact should result in smaller adjustments."""
        full = adjust_probabilities(
            base=40,
            bull=15,
            bear=45,
            pain_index=80,
            effective_impact=1.0,
        )
        reduced = adjust_probabilities(
            base=40,
            bull=15,
            bear=45,
            pain_index=80,
            effective_impact=0.3,
        )
        # Full impact should make larger bear reduction
        full_bear_change = abs(full["adjusted"]["bear"] - 45)
        reduced_bear_change = abs(reduced["adjusted"]["bear"] - 45)
        assert full_bear_change > reduced_bear_change

    def test_invalid_sum_raises(self):
        """Probabilities not summing to ~100 should raise ValueError."""
        with pytest.raises(ValueError, match="must sum to"):
            adjust_probabilities(
                base=40,
                bull=15,
                bear=30,  # sums to 85
                pain_index=50,
                effective_impact=1.0,
            )

    def test_result_keys(self):
        """Result should contain expected keys."""
        result = adjust_probabilities(
            base=40,
            bull=30,
            bear=30,
            pain_index=50,
        )
        assert "original" in result
        assert "adjusted" in result
        assert "pain_index" in result
        assert "adjustments" in result
        assert "raw_shift" in result
        assert "actual_shift" in result

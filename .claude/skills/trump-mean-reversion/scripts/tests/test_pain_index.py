"""Tests for Trump Pain Index calculator."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pain_index import (
    DOMAIN_WEIGHTS,
    calculate_domain_score,
    calculate_pain_index,
    sigmoid_normalize,
)


class TestSigmoidNormalize:
    """Tests for the sigmoid normalization function."""

    def test_midpoint_returns_half(self):
        """Value at midpoint should produce ~0.5."""
        result = sigmoid_normalize(50, midpoint=50, steepness=0.1)
        assert abs(result - 0.5) < 0.01

    def test_high_value_approaches_one(self):
        """Values well above midpoint should approach 1.0."""
        result = sigmoid_normalize(100, midpoint=50, steepness=0.1)
        assert result > 0.95

    def test_low_value_approaches_zero(self):
        """Values well below midpoint should approach 0.0."""
        result = sigmoid_normalize(0, midpoint=50, steepness=0.1)
        assert result < 0.05

    def test_monotonically_increasing(self):
        """Sigmoid should be strictly increasing."""
        prev = 0
        for x in range(0, 101, 10):
            val = sigmoid_normalize(x, midpoint=50, steepness=0.1)
            assert val >= prev
            prev = val


class TestCalculateDomainScore:
    """Tests for per-domain scoring."""

    def test_energy_high_pain(self):
        """WTI > $120 should produce high pain score."""
        score = calculate_domain_score("energy", 120)
        assert score > 0.9

    def test_energy_low_pain(self):
        """WTI < $60 should produce low pain score."""
        score = calculate_domain_score("energy", 60)
        assert score < 0.1

    def test_unknown_domain_raises(self):
        """Unknown domain should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown domain"):
            calculate_domain_score("unknown", 50)


class TestCalculatePainIndex:
    """Tests for composite Pain Index calculation."""

    def test_all_domains_moderate(self):
        """All domains at midpoint should produce ~50 pain index."""
        values = {
            "energy": 90.0,  # midpoint
            "stock_market": 10.0,  # midpoint
            "geopolitics": 5.0,  # midpoint
            "trade": 5.0,  # midpoint
            "interest_rates": 5.0,  # midpoint
        }
        result = calculate_pain_index(values)
        assert 45 <= result["pain_index"] <= 55

    def test_all_domains_high_pain(self):
        """Extreme high values should produce high pain index."""
        values = {
            "energy": 150.0,
            "stock_market": 25.0,
            "geopolitics": 10.0,
            "trade": 10.0,
            "interest_rates": 7.0,
        }
        result = calculate_pain_index(values)
        assert result["pain_index"] > 80
        assert result["zone"] == "High"

    def test_all_domains_low_pain(self):
        """Extreme low values should produce low pain index."""
        values = {
            "energy": 50.0,
            "stock_market": 1.0,
            "geopolitics": 1.0,
            "trade": 1.0,
            "interest_rates": 2.0,
        }
        result = calculate_pain_index(values)
        assert result["pain_index"] < 20
        assert result["zone"] == "Low"

    def test_partial_data_redistributes_weights(self):
        """Missing domains should redistribute weights."""
        values = {
            "geopolitics": 5.0,
            "trade": 5.0,
        }
        result = calculate_pain_index(values)
        # Only 2 of 5 domains available
        assert result["data_quality"]["available_count"] == 2
        assert result["data_quality"]["total_count"] == 5
        # Effective weights should sum to ~1.0 for available domains
        avail_ew = sum(
            d["effective_weight"] for d in result["domain_scores"].values() if d["available"]
        )
        assert abs(avail_ew - 1.0) < 0.01

    def test_zone_classification_low(self):
        """Pain < 30 should be Low zone."""
        values = {"geopolitics": 1.0, "trade": 1.0}
        result = calculate_pain_index(values)
        assert result["zone"] == "Low"

    def test_zone_classification_high(self):
        """Pain > 60 should be High zone."""
        values = {"geopolitics": 10.0, "trade": 10.0}
        result = calculate_pain_index(values)
        assert result["zone"] == "High"

    def test_weights_sum_to_one(self):
        """Domain weights should sum to 1.0."""
        total = sum(DOMAIN_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

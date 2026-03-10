"""Tests for intervention probability engine."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from intervention_model import (
    diminishing_factor,
    effective_impact,
    intervention_probability,
    words_vs_actions_discount,
)


class TestInterventionProbability:
    """Tests for base intervention probability."""

    def test_midpoint_returns_half(self):
        """Pain at 50 (default midpoint) should give ~0.5 probability."""
        prob = intervention_probability(50.0)
        assert abs(prob - 0.5) < 0.05

    def test_high_pain_high_probability(self):
        """Very high pain should give high intervention probability."""
        prob = intervention_probability(90.0)
        assert prob > 0.9

    def test_low_pain_low_probability(self):
        """Low pain should give low intervention probability."""
        prob = intervention_probability(10.0)
        assert prob < 0.1

    def test_domain_sensitivity_amplifies(self):
        """Energy domain (sensitivity 1.2) should amplify probability."""
        prob_base = intervention_probability(60.0)
        prob_energy = intervention_probability(60.0, domain="energy")
        assert prob_energy > prob_base

    def test_domain_sensitivity_dampens(self):
        """Interest rates (sensitivity 0.5) should dampen probability."""
        prob_base = intervention_probability(60.0)
        prob_rates = intervention_probability(60.0, domain="interest_rates")
        assert prob_rates < prob_base


class TestDiminishingFactor:
    """Tests for diminishing returns."""

    def test_zero_interventions_full_effect(self):
        """No prior interventions should give factor 1.0."""
        assert diminishing_factor(0) == 1.0

    def test_one_intervention(self):
        """1 prior intervention should give ~0.77."""
        factor = diminishing_factor(1)
        assert abs(factor - 0.7692) < 0.01

    def test_five_interventions(self):
        """5 prior interventions should give ~0.40."""
        factor = diminishing_factor(5)
        assert abs(factor - 0.4) < 0.01

    def test_monotonically_decreasing(self):
        """More interventions should always decrease factor."""
        prev = 1.1
        for count in range(0, 11):
            f = diminishing_factor(count)
            assert f < prev
            prev = f

    def test_negative_count_treated_as_zero(self):
        """Negative count should be treated as 0."""
        assert diminishing_factor(-1) == 1.0


class TestWordsVsActionsDiscount:
    """Tests for intervention type discount."""

    def test_verbal_lowest(self):
        assert words_vs_actions_discount("verbal") == 0.3

    def test_executive_order_medium(self):
        assert words_vs_actions_discount("executive_order") == 0.7

    def test_policy_action_full(self):
        assert words_vs_actions_discount("policy_action") == 1.0

    def test_unknown_type_raises(self):
        with pytest.raises(ValueError, match="Unknown intervention type"):
            words_vs_actions_discount("tweet")


class TestEffectiveImpact:
    """Tests for composite effective impact."""

    def test_high_pain_policy_action_no_prior(self):
        """High pain + policy action + no prior = high impact."""
        result = effective_impact(
            pain_index=85,
            intervention_count=0,
            intervention_type="policy_action",
        )
        assert result["effective_impact"] > 0.8

    def test_low_pain_verbal_many_prior(self):
        """Low pain + verbal + many priors = very low impact."""
        result = effective_impact(
            pain_index=20,
            intervention_count=5,
            intervention_type="verbal",
        )
        assert result["effective_impact"] < 0.05

    def test_result_keys(self):
        """Result should contain all expected keys."""
        result = effective_impact(50, intervention_count=1, intervention_type="verbal")
        expected_keys = {
            "intervention_probability",
            "diminishing_factor",
            "type_discount",
            "effective_impact",
            "pain_index",
            "domain",
            "intervention_count",
            "intervention_type",
        }
        assert set(result.keys()) == expected_keys

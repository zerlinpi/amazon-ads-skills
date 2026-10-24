"""Fail-closed budget-state value evidence for Sponsored Products causal reviews.

The comparator must not interpret placeholders, booleans, non-finite values,
or unsupported shapes as an observed budget/policy control. Synthetic only.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_budget_policy_control_state import budget_snapshot, control


class BudgetStateValueEvidenceTests(unittest.TestCase):
    def compare_with(self, field, value, both=False):
        baseline = budget_snapshot(100, 100)
        post = budget_snapshot(120, 120)
        control(post, "budget_or_pacing")["state"][field] = value
        if both:
            control(baseline, "budget_or_pacing")["state"][field] = value
        return compare_control_state(baseline, post, "budget_or_pacing")

    def assert_unknown(self, field, value, both=False):
        result = self.compare_with(field, value, both)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(any(field in reason for reason in result["reasons"]), result)

    def test_unknown_effective_budget_is_not_an_observed_change(self):
        self.assert_unknown("effective_daily_budget", "Unknown")

    def test_unsupported_base_budget_is_not_a_zero_or_valid_budget(self):
        self.assert_unknown("base_average_daily_budget", "Unsupported")

    def test_boolean_base_budget_is_not_numeric_evidence(self):
        self.assert_unknown("base_average_daily_budget", False)

    def test_boolean_effective_budget_is_not_numeric_evidence(self):
        self.assert_unknown("effective_daily_budget", True)

    def test_negative_effective_budget_is_not_valid_budget_evidence(self):
        self.assert_unknown("effective_daily_budget", -5)

    def test_nonfinite_effective_budget_is_not_valid_budget_evidence(self):
        self.assert_unknown("effective_daily_budget", float("inf"))

    def test_structured_placeholder_is_not_numeric_budget_evidence(self):
        self.assert_unknown("effective_daily_budget", {"status": "Partial"})

    def test_empty_policy_is_not_an_observed_control(self):
        self.assert_unknown("average_daily_budget_policy", "")

    def test_unknown_policy_on_both_sides_is_not_stable_control(self):
        self.assert_unknown("average_daily_budget_policy", "Unknown", both=True)

    def test_unsupported_policy_on_both_sides_is_not_stable_control(self):
        self.assert_unknown("average_daily_budget_policy", "Unsupported", both=True)

    def test_empty_policy_object_is_not_an_observed_control(self):
        self.assert_unknown("average_daily_budget_policy", {})

    def test_unknown_effective_budget_on_both_sides_is_not_stability_proof(self):
        self.assert_unknown("effective_daily_budget", "Unknown", both=True)

    def test_explicit_numeric_zero_is_not_missing_evidence(self):
        result = self.compare_with("effective_daily_budget", 0)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_valid_decimal_string_budget_remains_supported(self):
        result = self.compare_with("effective_daily_budget", "120.00")
        self.assertEqual(result["classification"], "Treatment Isolated", result)


if __name__ == "__main__":
    unittest.main()

"""RED-first: Ready experiment readout necessity must not be an explicit unknown.

Synthetic plans only; no account access or Amazon Ads writes.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_experiment_combined_ratio_aggregation import combined_metric


def plan_with_readout_flag(flag, *, include=True, status="Ready"):
    plan = combined_metric("CTR", aggregation="additive", status=status)
    if include:
        plan["comparison"]["requires_combined_readout"] = flag
    else:
        plan["comparison"].pop("requires_combined_readout", None)
    return plan


class ReadyExplicitReadoutRequirementTests(unittest.TestCase):
    def assert_unresolved(self, value):
        errors = validate_experiment_plan(plan_with_readout_flag(value))
        self.assertTrue(
            any("requires_combined_readout" in error for error in errors), errors
        )

    def test_explicit_null_cannot_disable_combined_gate(self):
        self.assert_unresolved(None)

    def test_explicit_unknown_cannot_disable_combined_gate(self):
        self.assert_unresolved("Unknown")

    def test_explicit_partial_cannot_disable_combined_gate(self):
        self.assert_unresolved("Partial")

    def test_explicit_empty_string_cannot_disable_combined_gate(self):
        self.assert_unresolved("")

    def test_explicit_zero_cannot_disable_combined_gate(self):
        self.assert_unresolved(0)

    def test_explicit_empty_array_cannot_disable_combined_gate(self):
        self.assert_unresolved([])

    def test_explicit_empty_object_cannot_disable_combined_gate(self):
        self.assert_unresolved({})

    def test_explicit_numeric_one_cannot_impersonate_boolean_true(self):
        self.assert_unresolved(1)

    def test_true_still_enforces_ratio_aggregation(self):
        errors = validate_experiment_plan(plan_with_readout_flag(True))
        self.assertTrue(any("aggregation_semantics" in error for error in errors), errors)

    def test_false_still_allows_non_combined_ready_plan(self):
        self.assertEqual([], validate_experiment_plan(plan_with_readout_flag(False)))

    def test_omitted_legacy_readout_flag_remains_compatible(self):
        self.assertEqual([], validate_experiment_plan(plan_with_readout_flag(None, include=False)))

    def test_shadow_plan_can_preserve_explicit_unknown(self):
        self.assertEqual([], validate_experiment_plan(plan_with_readout_flag(None, status="Shadow Only")))


if __name__ == "__main__":
    unittest.main()

"""RED-first: a Ready holdout must positively verify every material boundary change.

Synthetic only. This does not authenticate Amazon Ads delivery or perform writes.
"""
import copy
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def plan_with_change(*, reverified_marker="__omit__", status="Ready"):
    plan = base_plan(status=status)
    change = {
        "timestamp": "2026-09-02T00:00:00Z",
        "type": "routing_change",
        "description": "Synthetic routing/negative partition changed",
    }
    if reverified_marker != "__omit__":
        change["reverified"] = reverified_marker
    plan["comparison"]["boundary_monitoring"] = {
        "latest_verified_at": "2026-09-03T00:00:00Z",
        "current_status": "Clean",
        "material_scope_changes": [change],
    }
    return plan


class ReadyMaterialChangeReverificationTests(unittest.TestCase):
    def assert_not_ready(self, marker):
        errors = validate_experiment_plan(plan_with_change(reverified_marker=marker))
        self.assertTrue(errors, "Ready must not infer re-verification from a later timestamp alone")
        self.assertIn("reverified", " | ".join(errors), errors)

    def test_missing_reverified_is_not_proof(self):
        self.assert_not_ready("__omit__")

    def test_null_reverified_is_not_proof(self):
        self.assert_not_ready(None)

    def test_string_reverified_is_not_proof(self):
        self.assert_not_ready("true")

    def test_numeric_one_reverified_is_not_proof(self):
        self.assert_not_ready(1)

    def test_numeric_zero_reverified_is_not_proof(self):
        self.assert_not_ready(0)

    def test_explicit_false_reverified_stays_rejected(self):
        self.assert_not_ready(False)

    def test_explicit_true_after_change_remains_valid(self):
        self.assertEqual([], validate_experiment_plan(plan_with_change(reverified_marker=True)))

    def test_one_unknown_change_in_multiple_changes_rejects_ready(self):
        plan = plan_with_change(reverified_marker=True)
        other = copy.deepcopy(plan["comparison"]["boundary_monitoring"]["material_scope_changes"][0])
        other["timestamp"] = "2026-09-02T12:00:00Z"
        other["type"] = "budget_pool_change"
        other.pop("reverified")
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"].append(other)
        errors = validate_experiment_plan(plan)
        self.assertIn("reverified", " | ".join(errors), errors)

    def test_no_material_changes_keeps_ready_compatible(self):
        plan = plan_with_change()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = []
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_only_keeps_unknown_reverification(self):
        plan = plan_with_change(status="Shadow Only")
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

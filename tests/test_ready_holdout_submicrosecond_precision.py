"""RED-first: Ready holdout evidence cannot silently lose sub-microsecond ordering.

Synthetic read-only records. Python datetime only retains six fractional digits;
seven-plus digits must not be promoted to verified Ready evidence by truncation.
"""
import copy
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def monitored_plan(status="Ready"):
    plan = base_plan(status=status)
    plan["comparison"]["boundary_monitoring"] = {
        "current_status": "Clean",
        "launch_verified_at": "2026-09-03T09:00:00Z",
        "latest_verified_at": "2026-09-03T10:00:00Z",
        "material_scope_changes": [],
    }
    plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T09:30:00Z"
    return plan


class ReadyHoldoutSubmicrosecondPrecisionTests(unittest.TestCase):
    def assert_unrepresentable(self, plan, field):
        errors = validate_experiment_plan(plan)
        self.assertTrue(errors, "sub-microsecond evidence must not authorize Ready")
        self.assertIn(field, " | ".join(errors), errors)

    def test_latest_with_seven_fraction_digits_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.0000001Z"
        self.assert_unrepresentable(plan, "latest_verified_at")

    def test_launch_with_seven_fraction_digits_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-03T09:00:00.0000001Z"
        self.assert_unrepresentable(plan, "launch_verified_at")

    def test_isolation_with_seven_fraction_digits_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T09:30:00.0000001Z"
        self.assert_unrepresentable(plan, "isolation_evidence")

    def test_material_change_with_seven_fraction_digits_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03T09:45:00.0000001Z", "reverified": True}
        ]
        self.assert_unrepresentable(plan, "material_scope_changes")

    def test_later_isolation_cannot_disappear_by_truncation(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T10:00:00.0000001Z"
        self.assert_unrepresentable(plan, "isolation_evidence")

    def test_later_material_change_cannot_disappear_by_truncation(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03T10:00:00.0000001Z", "reverified": True}
        ]
        self.assert_unrepresentable(plan, "material_scope_changes")

    def test_offset_with_seven_fraction_digits_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T17:30:00.1234567+08:00"
        self.assert_unrepresentable(plan, "isolation_evidence")

    def test_nine_digit_zero_fraction_still_requires_explicit_precision(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.000000000Z"
        self.assert_unrepresentable(plan, "latest_verified_at")

    def test_six_digit_fraction_is_supported(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.123456Z"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_single_digit_fraction_is_supported(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T09:30:00.1Z"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_six_digit_offset_chronology_is_supported(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T17:30:00.123456+08:00"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_no_fraction_remains_supported(self):
        self.assertEqual([], validate_experiment_plan(monitored_plan()))

    def test_omitted_optional_monitoring_remains_compatible(self):
        plan = monitored_plan()
        del plan["comparison"]["boundary_monitoring"]
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_only_can_retain_unresolved_high_precision(self):
        plan = monitored_plan(status="Shadow Only")
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.0000001Z"
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

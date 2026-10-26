"""RED-first: Ready holdout chronology must retain arbitrary RFC3339 fractions.

Synthetic read-only records. Python datetime truncates beyond microseconds, so
verification ordering must use the original fractional seconds without rounding.
"""
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
    def assert_chronology_error(self, plan, field):
        errors = validate_experiment_plan(plan)
        self.assertTrue(errors, "fractional ordering must not disappear by truncation")
        self.assertIn(field, " | ".join(errors), errors)

    def test_later_isolation_seventh_digit_cannot_disappear(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T10:00:00.0000001Z"
        self.assert_chronology_error(plan, "isolation_evidence")

    def test_later_isolation_ninth_digit_cannot_disappear(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T10:00:00.000000001Z"
        self.assert_chronology_error(plan, "isolation_evidence")

    def test_later_isolation_offset_fraction_cannot_disappear(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.1234566Z"
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T18:00:00.1234567+08:00"
        self.assert_chronology_error(plan, "isolation_evidence")

    def test_later_launch_seventh_digit_cannot_disappear(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-03T10:00:00.0000001Z"
        self.assert_chronology_error(plan, "launch_verified_at")

    def test_later_material_change_seventh_digit_cannot_disappear(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03T10:00:00.0000001Z", "reverified": True}
        ]
        self.assert_chronology_error(plan, "stale")

    def test_later_material_change_ninth_digit_cannot_disappear(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03T10:00:00.000000001Z", "reverified": True}
        ]
        self.assert_chronology_error(plan, "stale")

    def test_equal_ninth_digit_isolation_and_latest_valid(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.123456789Z"
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T18:00:00.123456789+08:00"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_earlier_ninth_digit_isolation_valid(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.123456790Z"
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T10:00:00.123456789Z"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_valid_high_precision_launch_before_latest(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-03T09:00:00.123456789Z"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_valid_high_precision_material_change_before_latest(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03T09:45:00.123456789Z", "reverified": True}
        ]
        self.assertEqual([], validate_experiment_plan(plan))

    def test_six_digit_fraction_still_valid(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.123456Z"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_no_fraction_still_valid(self):
        self.assertEqual([], validate_experiment_plan(monitored_plan()))

    def test_omitted_optional_monitoring_remains_compatible(self):
        plan = monitored_plan()
        del plan["comparison"]["boundary_monitoring"]
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_only_can_retain_unresolved_chronology(self):
        plan = monitored_plan(status="Shadow Only")
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T10:00:00.0000001Z"
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

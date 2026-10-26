"""RED-first: optional Ready holdout monitoring must not silently accept incomplete evidence.

All fixtures are synthetic. This does not authenticate Amazon Ads delivery or write to Ads.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def monitored_plan(*, status="Ready"):
    plan = base_plan(status=status)
    plan["comparison"]["boundary_monitoring"] = {
        "current_status": "Clean",
        "latest_verified_at": "2026-09-03T00:00:00Z",
        "material_scope_changes": [],
    }
    return plan


class ReadyBoundaryMonitoringCompletenessTests(unittest.TestCase):
    def assert_rejected(self, plan, field):
        errors = validate_experiment_plan(plan)
        self.assertTrue(errors, "incomplete observed boundary monitoring cannot prove Ready")
        self.assertIn(field, " | ".join(errors), errors)

    def test_missing_current_status_with_no_changes_is_not_clean(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"].pop("current_status")
        self.assert_rejected(plan, "current_status")

    def test_null_current_status_with_no_changes_is_not_clean(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["current_status"] = None
        self.assert_rejected(plan, "current_status")

    def test_missing_latest_verification_with_no_changes_is_not_proof(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"].pop("latest_verified_at")
        self.assert_rejected(plan, "latest_verified_at")

    def test_null_latest_verification_with_no_changes_is_not_proof(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = None
        self.assert_rejected(plan, "latest_verified_at")

    def test_naive_latest_verification_with_no_changes_is_not_proof(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T00:00:00"
        self.assert_rejected(plan, "latest_verified_at")

    def test_invalid_latest_verification_with_no_changes_is_not_proof(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "Unknown"
        self.assert_rejected(plan, "latest_verified_at")

    def test_launch_verification_after_latest_is_impossible_chronology(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-04T00:00:00Z"
        self.assert_rejected(plan, "launch_verified_at")

    def test_naive_launch_verification_is_not_a_verified_instant(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-01T00:00:00"
        self.assert_rejected(plan, "launch_verified_at")

    def test_missing_current_status_with_reverified_change_still_rejected(self):
        plan = monitored_plan()
        monitor = plan["comparison"]["boundary_monitoring"]
        monitor.pop("current_status")
        monitor["material_scope_changes"] = [
            {"timestamp": "2026-09-02T00:00:00Z", "type": "routing_change", "reverified": True}
        ]
        self.assert_rejected(plan, "current_status")

    def test_valid_clean_monitoring_with_no_changes_passes(self):
        self.assertEqual([], validate_experiment_plan(monitored_plan()))

    def test_valid_launch_before_latest_passes(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-01T01:00:00+01:00"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_valid_equal_launch_and_latest_passes(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-03T00:00:00+00:00"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_absent_optional_monitoring_preserves_legacy_ready(self):
        self.assertEqual([], validate_experiment_plan(base_plan()))

    def test_shadow_only_can_preserve_incomplete_monitoring(self):
        plan = monitored_plan(status="Shadow Only")
        plan["comparison"]["boundary_monitoring"] = {"current_status": None}
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

"""RED-first: Ready holdout timestamps must use unambiguous RFC3339 instants.

Python datetime.fromisoformat accepts space separators, offset seconds and
-00:00; those are not acceptable proof timestamps for this repository.
All evidence is synthetic; no Amazon Ads access or writes.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def monitored_plan(*, status="Ready"):
    plan = base_plan(status=status)
    plan["comparison"]["boundary_monitoring"] = {
        "current_status": "Clean",
        "latest_verified_at": "2026-09-03T10:00:00Z",
        "material_scope_changes": [],
    }
    return plan


class ReadyHoldoutRFC3339EvidenceTests(unittest.TestCase):
    def assert_rejected(self, plan, field):
        errors = validate_experiment_plan(plan)
        self.assertIn(field, " | ".join(errors), errors)

    def test_latest_unknown_offset_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00-00:00"
        self.assert_rejected(plan, "latest_verified_at")

    def test_latest_space_separator_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03 10:00:00+00:00"
        self.assert_rejected(plan, "latest_verified_at")

    def test_latest_offset_seconds_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00+00:00:30"
        self.assert_rejected(plan, "latest_verified_at")

    def test_launch_unknown_offset_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-03T08:00:00-00:00"
        self.assert_rejected(plan, "launch_verified_at")

    def test_launch_space_separator_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-03 08:00:00+00:00"
        self.assert_rejected(plan, "launch_verified_at")

    def test_change_unknown_offset_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03T08:00:00-00:00", "reverified": True}
        ]
        self.assert_rejected(plan, "material_scope_changes[0].timestamp")

    def test_change_space_separator_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03 08:00:00+00:00", "reverified": True}
        ]
        self.assert_rejected(plan, "material_scope_changes[0].timestamp")

    def test_isolation_unknown_offset_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T08:00:00-00:00"
        self.assert_rejected(plan, "isolation_evidence[0].verified_at")

    def test_isolation_space_separator_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03 08:00:00+00:00"
        self.assert_rejected(plan, "isolation_evidence[0].verified_at")

    def test_valid_zulu_remains_ready(self):
        self.assertEqual([], validate_experiment_plan(monitored_plan()))

    def test_valid_offset_chronology_remains_ready(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = "2026-09-03T16:00:00+08:00"
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03T09:00:00+01:00", "reverified": True}
        ]
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T08:00:00Z"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_valid_fractional_seconds_remain_ready(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "2026-09-03T10:00:00.123456Z"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_omitted_optional_monitoring_remains_ready(self):
        self.assertEqual([], validate_experiment_plan(base_plan()))

    def test_shadow_preserves_unknown_offset(self):
        plan = monitored_plan(status="Shadow Only")
        plan["comparison"]["boundary_monitoring"]["latest_verified_at"] = "Unknown"
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T08:00:00-00:00"
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

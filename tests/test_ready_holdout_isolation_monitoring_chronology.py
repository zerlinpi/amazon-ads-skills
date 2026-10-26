"""RED-first: a Ready holdout's latest boundary check cannot predate a verified isolation check.

Synthetic, read-only evidence. This does not authenticate external Ads control history.
"""
import copy
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
    plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T09:00:00Z"
    return plan


class ReadyIsolationMonitoringChronologyTests(unittest.TestCase):
    def assert_stale(self, plan):
        errors = validate_experiment_plan(plan)
        self.assertTrue(errors, "a stale latest boundary verification cannot establish Ready")
        joined = " | ".join(errors)
        self.assertIn("latest_verified_at", joined, errors)
        self.assertIn("isolation_evidence", joined, errors)

    def test_isolation_verified_after_latest_zulu_is_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T11:00:00Z"
        self.assert_stale(plan)

    def test_isolation_verified_after_latest_across_offsets_is_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T19:00:00+08:00"
        self.assert_stale(plan)

    def test_isolation_verified_fractionally_after_latest_is_rejected(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T10:00:00.000001Z"
        self.assert_stale(plan)

    def test_one_later_verified_isolation_in_multiple_records_is_rejected(self):
        plan = monitored_plan()
        extra = copy.deepcopy(plan["comparison"]["isolation_evidence"][0])
        extra["verified_at"] = "2026-09-03T11:00:00Z"
        plan["comparison"]["isolation_evidence"].append(extra)
        self.assert_stale(plan)

    def test_later_isolation_after_material_change_still_requires_fresh_latest(self):
        plan = monitored_plan()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = [
            {"timestamp": "2026-09-03T09:30:00Z", "reverified": True}
        ]
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T10:30:00Z"
        self.assert_stale(plan)

    def test_equal_verification_instants_are_valid(self):
        plan = monitored_plan()
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T18:00:00+08:00"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_earlier_isolation_verification_is_valid(self):
        self.assertEqual([], validate_experiment_plan(monitored_plan()))

    def test_optional_legacy_isolation_timestamp_remains_valid(self):
        plan = monitored_plan()
        del plan["comparison"]["isolation_evidence"][0]["verified_at"]
        self.assertEqual([], validate_experiment_plan(plan))

    def test_omitted_optional_monitoring_remains_legacy_compatible(self):
        plan = monitored_plan()
        del plan["comparison"]["boundary_monitoring"]
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T11:00:00Z"
        self.assertEqual([], validate_experiment_plan(plan))

    def test_unverified_later_item_is_not_claimed_boundary_proof(self):
        plan = monitored_plan()
        extra = copy.deepcopy(plan["comparison"]["isolation_evidence"][0])
        extra["verified"] = False
        extra["verified_at"] = "2026-09-03T11:00:00Z"
        plan["comparison"]["isolation_evidence"].append(extra)
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_only_retains_unresolved_chronology(self):
        plan = monitored_plan(status="Shadow Only")
        plan["comparison"]["isolation_evidence"][0]["verified_at"] = "2026-09-03T11:00:00Z"
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

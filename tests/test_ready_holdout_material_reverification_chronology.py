"""RED-first: supplied material-change re-verification instants must be coherent.

Synthetic evidence only. The optional reverified_at field is an internal
chronology assertion, not independent Amazon Ads source authentication.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def monitored_change_plan(*, status="Ready", change_at="2026-09-03T09:00:00Z",
                          latest_at="2026-09-03T10:00:00Z",
                          reverified_at="2026-09-03T09:30:00Z"):
    plan = base_plan(status=status)
    change = {
        "timestamp": change_at,
        "type": "routing_change",
        "description": "Synthetic control boundary changed",
        "reverified": True,
    }
    if reverified_at != "__omit__":
        change["reverified_at"] = reverified_at
    plan["comparison"]["boundary_monitoring"] = {
        "current_status": "Clean",
        "latest_verified_at": latest_at,
        "material_scope_changes": [change],
    }
    return plan


class ReadyMaterialReverificationChronologyTests(unittest.TestCase):
    def assert_reverification_error(self, plan):
        errors = validate_experiment_plan(plan)
        self.assertTrue(errors, "contradictory re-verification must not authorize Ready")
        self.assertIn("reverified_at", " | ".join(errors), errors)

    def test_explicit_null_is_not_absent_reverification(self):
        self.assert_reverification_error(monitored_change_plan(reverified_at=None))

    def test_unknown_reverification_is_not_proof(self):
        self.assert_reverification_error(monitored_change_plan(reverified_at="Unknown"))

    def test_numeric_reverification_is_not_timestamp(self):
        self.assert_reverification_error(monitored_change_plan(reverified_at=0))

    def test_reverification_before_change_is_invalid(self):
        self.assert_reverification_error(monitored_change_plan(reverified_at="2026-09-03T08:59:59Z"))

    def test_reverification_after_latest_clean_check_is_invalid(self):
        self.assert_reverification_error(monitored_change_plan(reverified_at="2026-09-03T10:00:01Z"))

    def test_submicrosecond_earlier_than_change_is_invalid(self):
        self.assert_reverification_error(monitored_change_plan(
            change_at="2026-09-03T09:00:00.000000001Z",
            reverified_at="2026-09-03T09:00:00Z",
        ))

    def test_submicrosecond_later_than_latest_is_invalid(self):
        self.assert_reverification_error(monitored_change_plan(
            latest_at="2026-09-03T10:00:00Z",
            reverified_at="2026-09-03T10:00:00.000000001Z",
        ))

    def test_unknown_offset_is_not_reverification_proof(self):
        self.assert_reverification_error(monitored_change_plan(
            reverified_at="2026-09-03T09:30:00-00:00",
        ))

    def test_reverification_equal_to_change_is_valid(self):
        self.assertEqual([], validate_experiment_plan(monitored_change_plan(
            reverified_at="2026-09-03T09:00:00Z",
        )))

    def test_reverification_equal_to_latest_is_valid(self):
        self.assertEqual([], validate_experiment_plan(monitored_change_plan(
            reverified_at="2026-09-03T10:00:00Z",
        )))

    def test_valid_offset_equivalence_is_valid(self):
        self.assertEqual([], validate_experiment_plan(monitored_change_plan(
            reverified_at="2026-09-03T17:30:00+08:00",
        )))

    def test_omitted_optional_reverification_timestamp_is_legacy_compatible(self):
        self.assertEqual([], validate_experiment_plan(monitored_change_plan(
            reverified_at="__omit__",
        )))

    def test_shadow_preserves_unresolved_reverification(self):
        self.assertEqual([], validate_experiment_plan(monitored_change_plan(
            status="Shadow Only", reverified_at=None,
        )))

    def test_unrelated_unmonitored_ready_holdout_is_compatible(self):
        self.assertEqual([], validate_experiment_plan(base_plan()))


if __name__ == "__main__":
    unittest.main()

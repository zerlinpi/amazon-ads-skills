"""Fail-closed audit event identity and supersession regression tests."""
import unittest

from scripts.project_measurement_comparison_history import project_measurement_comparison_history


def _event(event_id, *, target=None):
    event = {
        "event_id": event_id,
        "event_type": "corrected" if target is not None else "evaluated",
        "timestamp": "2026-10-17T00:00:00Z",
        "marketplace": "US",
        "profile_scope": "synthetic-profile",
        "parent_action_id": "synthetic-action",
        "entity": {"type": "keyword", "id": "synthetic-keyword"},
        "measurement_comparison": {
            "comparator_id": "measurement-composition@1",
            "classification": "Comparable",
            "changed_fields": [],
            "reasons": [],
            "baseline_snapshot_id": "before",
            "post_snapshot_id": "after",
        },
    }
    if target is not None:
        event["supersedes_event_id"] = target
    return event


class AuditIdentityTests(unittest.TestCase):
    def test_duplicate_event_identity_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate event_id"):
            project_measurement_comparison_history([_event("same"), _event("same")])

    def test_missing_and_empty_event_identity_are_rejected(self):
        for invalid in (None, ""):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(ValueError, "event_id"):
                    project_measurement_comparison_history([_event(invalid)])

    def test_self_correction_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cycle"):
            project_measurement_comparison_history([_event("a", target="a")])

    def test_two_event_correction_cycle_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cycle"):
            project_measurement_comparison_history([
                _event("a", target="b"), _event("b", target="a"),
            ])

    def test_normal_linear_correction_remains_available(self):
        result = project_measurement_comparison_history([
            _event("a"), _event("b", target="a"),
        ])
        self.assertEqual(result["measurement_comparison_status"], "Available")
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "b")


if __name__ == "__main__":
    unittest.main()

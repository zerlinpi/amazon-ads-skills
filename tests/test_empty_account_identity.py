"""Explicit empty account_identity claims are incomplete, not missing."""
import unittest

from scripts.project_measurement_comparison_history import project_measurement_comparison_history


def event(account_identity):
    item = {
        "event_id": "eval-empty-identity",
        "event_type": "evaluated",
        "timestamp": "2026-10-30T00:00:00Z",
        "marketplace": "US",
        "profile_scope": "profile-us-1",
        "parent_action_id": "action-1",
        "entity": {"type": "keyword", "id": "keyword-1"},
        "account_identity": account_identity,
        "measurement_comparison": {
            "comparator_id": "measurement-composition@1",
            "classification": "Comparable",
            "changed_fields": [],
            "reasons": [],
            "baseline_snapshot_id": "baseline-1",
            "post_snapshot_id": "post-1",
        },
    }
    return item


class EmptyAccountIdentityTests(unittest.TestCase):
    def test_empty_account_identity_is_rejected_in_comparison_projection(self):
        with self.assertRaisesRegex(ValueError, "account identity"):
            project_measurement_comparison_history([event({})])

    def test_provenance_only_account_identity_is_rejected_in_comparison_projection(self):
        with self.assertRaisesRegex(ValueError, "account identity"):
            project_measurement_comparison_history([
                event({"identity_mapping_provenance": "adapter-claimed"})
            ])


if __name__ == "__main__":
    unittest.main()

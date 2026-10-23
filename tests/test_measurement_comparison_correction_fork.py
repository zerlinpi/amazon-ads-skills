"""A correction ledger must not silently select one of two rival successors."""

import unittest

from scripts.project_measurement_comparison_history import project_measurement_comparison_history


def comparison(classification="Directional", **overrides):
    audit = {
        "comparator_id": "measurement-composition@1",
        "classification": classification,
        "changed_fields": ["allocation_coverage_status"],
        "reasons": ["allocation coverage changed"],
        "baseline_snapshot_id": "baseline-1",
        "post_snapshot_id": "post-1",
    }
    audit.update(overrides)
    return audit


def event(event_id, timestamp, *, event_type="evaluated", supersedes_event_id=None, measurement_comparison=None):
    record = {
        "event_id": event_id, "timestamp": timestamp, "event_type": event_type,
        "marketplace": "US", "profile_scope": "profile-us-1",
        "entity": {"type": "keyword", "id": "keyword-1"},
        "action_type": "bid_decrease", "parent_action_id": "action-1",
    }
    if supersedes_event_id is not None:
        record["supersedes_event_id"] = supersedes_event_id
    if measurement_comparison is not None:
        record["measurement_comparison"] = measurement_comparison
    return record


class CorrectionForkIntegrityTests(unittest.TestCase):
    def base(self):
        return event("eval-1", "2026-09-19T00:00:00Z", measurement_comparison=comparison())

    def test_two_rival_replacement_audits_are_ambiguous(self):
        history = [
            self.base(),
            event("corr-1", "2026-09-20T00:00:00Z", event_type="corrected", supersedes_event_id="eval-1", measurement_comparison=comparison("Comparable", changed_fields=[])),
            event("corr-2", "2026-09-21T00:00:00Z", event_type="corrected", supersedes_event_id="eval-1", measurement_comparison=comparison("Not Comparable")),
        ]
        with self.assertRaisesRegex(ValueError, "ambiguous correction fork"):
            project_measurement_comparison_history(history)

    def test_auditless_and_replacement_corrections_cannot_compete(self):
        history = [
            self.base(),
            event("corr-1", "2026-09-20T00:00:00Z", event_type="corrected", supersedes_event_id="eval-1"),
            event("corr-2", "2026-09-21T00:00:00Z", event_type="corrected", supersedes_event_id="eval-1", measurement_comparison=comparison("Comparable")),
        ]
        with self.assertRaisesRegex(ValueError, "ambiguous correction fork"):
            project_measurement_comparison_history(history)

    def test_linear_successor_chain_remains_valid(self):
        history = [
            self.base(),
            event("corr-1", "2026-09-20T00:00:00Z", event_type="corrected", supersedes_event_id="eval-1", measurement_comparison=comparison("Comparable")),
            event("corr-2", "2026-09-21T00:00:00Z", event_type="corrected", supersedes_event_id="corr-1", measurement_comparison=comparison("Directional")),
        ]
        result = project_measurement_comparison_history(history)
        self.assertEqual(result["measurement_comparison_status"], "Available")
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "corr-2")

    def test_unrelated_corrections_of_distinct_events_remain_valid(self):
        history = [
            self.base(),
            event("eval-2", "2026-09-19T01:00:00Z", measurement_comparison=comparison()),
            event("corr-1", "2026-09-20T00:00:00Z", event_type="corrected", supersedes_event_id="eval-1", measurement_comparison=comparison("Comparable")),
            event("corr-2", "2026-09-21T00:00:00Z", event_type="corrected", supersedes_event_id="eval-2", measurement_comparison=comparison("Directional")),
        ]
        result = project_measurement_comparison_history(history)
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "corr-2")


if __name__ == "__main__":
    unittest.main()

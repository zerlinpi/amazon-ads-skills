import json
import unittest
from pathlib import Path

from scripts.project_measurement_comparison_history import (
    project_measurement_comparison_history,
)


ROOT = Path(__file__).resolve().parents[1]


def comparison(classification="Directional", **overrides):
    value = {
        "comparator_id": "measurement-composition@1",
        "classification": classification,
        "changed_fields": ["allocation_coverage_status"],
        "reasons": ["allocation coverage changed"],
        "baseline_snapshot_id": "baseline-1",
        "post_snapshot_id": "post-1",
    }
    value.update(overrides)
    return value


def event(
    event_id,
    timestamp,
    *,
    event_type="evaluated",
    measurement_comparison=None,
    supersedes_event_id=None,
    entity_id="keyword-1",
):
    payload = {
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": timestamp,
        "marketplace": "US",
        "profile_scope": "profile-us-1",
        "entity": {"type": "keyword", "id": entity_id},
        "action_type": "bid_decrease",
        "parent_action_id": "action-1",
    }
    if measurement_comparison is not None:
        payload["measurement_comparison"] = measurement_comparison
    if supersedes_event_id is not None:
        payload["supersedes_event_id"] = supersedes_event_id
    return payload


class MeasurementComparisonHistoryProjectionTests(unittest.TestCase):
    def test_latest_active_comparison_is_projected(self):
        result = project_measurement_comparison_history([
            event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=comparison()),
        ])
        self.assertEqual(result["measurement_comparison_status"], "Available")
        latest = result["latest_measurement_comparison"]
        self.assertEqual(latest["source_event_id"], "eval-1")
        self.assertEqual(latest["source_event_type"], "evaluated")
        self.assertEqual(latest["comparator_id"], "measurement-composition@1")
        self.assertEqual(latest["classification"], "Directional")

    def test_correction_with_replacement_comparison_supersedes_prior_audit(self):
        result = project_measurement_comparison_history([
            event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=comparison()),
            event(
                "corr-1",
                "2026-09-21T00:00:00Z",
                event_type="corrected",
                measurement_comparison=comparison(
                    "Comparable",
                    changed_fields=[],
                    reasons=["reconciled under comparable composition"],
                    baseline_snapshot_id="baseline-2",
                    post_snapshot_id="post-2",
                ),
                supersedes_event_id="eval-1",
            ),
        ])
        self.assertEqual(result["measurement_comparison_status"], "Available")
        latest = result["latest_measurement_comparison"]
        self.assertEqual(latest["source_event_id"], "corr-1")
        self.assertEqual(latest["source_event_type"], "corrected")
        self.assertEqual(latest["classification"], "Comparable")
        self.assertEqual(latest["baseline_snapshot_id"], "baseline-2")

    def test_correction_without_replacement_clears_stale_comparison(self):
        result = project_measurement_comparison_history([
            event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=comparison()),
            event(
                "corr-1",
                "2026-09-21T00:00:00Z",
                event_type="corrected",
                supersedes_event_id="eval-1",
            ),
        ])
        self.assertIsNone(result["latest_measurement_comparison"])
        self.assertEqual(
            result["measurement_comparison_status"],
            "Superseded Without Replacement",
        )
        self.assertTrue(
            any("supersed" in warning.lower() for warning in result["measurement_comparison_warnings"])
        )

    def test_recursive_correction_chain_does_not_resurrect_superseded_audit(self):
        result = project_measurement_comparison_history([
            event("eval-1", "2026-09-19T00:00:00Z", measurement_comparison=comparison()),
            event(
                "corr-1",
                "2026-09-20T00:00:00Z",
                event_type="corrected",
                measurement_comparison=comparison("Comparable", changed_fields=[]),
                supersedes_event_id="eval-1",
            ),
            event(
                "corr-2",
                "2026-09-21T00:00:00Z",
                event_type="corrected",
                supersedes_event_id="corr-1",
            ),
        ])
        self.assertIsNone(result["latest_measurement_comparison"])
        self.assertEqual(
            result["measurement_comparison_status"],
            "Superseded Without Replacement",
        )

    def test_mixed_entity_scope_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "single entity scope"):
            project_measurement_comparison_history([
                event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=comparison()),
                event(
                    "eval-2",
                    "2026-09-21T00:00:00Z",
                    measurement_comparison=comparison("Comparable"),
                    entity_id="keyword-2",
                ),
            ])

    def test_missing_comparator_identity_projects_unknown_not_available(self):
        partial = comparison()
        partial["comparator_id"] = None
        result = project_measurement_comparison_history([
            event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=partial),
        ])
        self.assertEqual(result["measurement_comparison_status"], "Unknown")
        self.assertIsNotNone(result["latest_measurement_comparison"])
        self.assertTrue(result["measurement_comparison_warnings"])

    def test_entity_history_schema_declares_bounded_projection(self):
        schema = json.loads(
            (ROOT / "schemas" / "entity-history.json").read_text(encoding="utf-8")
        )
        props = schema["properties"]
        self.assertIn("latest_measurement_comparison", props)
        self.assertIn("measurement_comparison_status", props)
        self.assertIn("measurement_comparison_warnings", props)

        latest = props["latest_measurement_comparison"]
        self.assertEqual(latest["type"], ["object", "null"])
        self.assertEqual(
            set(latest["properties"]),
            {
                "source_event_id",
                "source_event_type",
                "observed_at",
                "parent_action_id",
                "comparator_id",
                "classification",
                "changed_fields",
                "reasons",
                "baseline_snapshot_id",
                "post_snapshot_id",
            },
        )
        self.assertEqual(
            props["measurement_comparison_status"]["enum"],
            [
                "Available",
                "No Comparison",
                "Superseded Without Replacement",
                "Unknown",
                None,
            ],
        )


if __name__ == "__main__":
    unittest.main()

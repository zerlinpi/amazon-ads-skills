import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/project_measurement_history.py"


class MeasurementProjectorTests(unittest.TestCase):
    def invoke_projector(self, events, expected_scope=None):
        payload = {"events": events}
        if expected_scope is not None:
            payload["expected_scope"] = expected_scope
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )

    def run_projector(self, events, expected_scope=None):
        result = self.invoke_projector(events, expected_scope=expected_scope)
        self.assertEqual(
            result.returncode,
            0,
            f"projector failed: stdout={result.stdout!r} stderr={result.stderr!r}",
        )
        return json.loads(result.stdout)

    def test_newest_snapshot_uses_measurement_capture_time_not_input_order(self):
        projected = self.run_projector(
            [
                {
                    "event_id": "e-new",
                    "timestamp": "2026-09-14T10:00:00Z",
                    "marketplace": "US",
                    "profile_scope": "profile-a",
                    "entity": {"type": "campaign", "id": "campaign-1"},
                    "evidence_snapshot": {
                        "snapshot_id": "m2",
                        "captured_at": "2026-09-14T09:59:00Z",
                        "source_system": "amazon_ads",
                        "source_dataset": "unified-reporting",
                        "acquisition_channel": "api",
                        "reporting_generation": "unified",
                        "semantic_version": "v2",
                        "date_attribution_semantics": "traffic_date",
                        "historical_availability_status": "partially_available",
                        "comparability_status": "Reconcilable",
                    },
                },
                {
                    "event_id": "e-old",
                    "timestamp": "2026-09-14T08:00:00Z",
                    "marketplace": "US",
                    "profile_scope": "profile-a",
                    "entity": {"type": "campaign", "id": "campaign-1"},
                    "evidence_snapshot": {
                        "snapshot_id": "m1",
                        "captured_at": "2026-09-14T07:59:00Z",
                        "reporting_generation": "legacy",
                        "date_attribution_semantics": "conversion_date",
                        "historical_availability_status": "available",
                        "comparability_status": "Comparable",
                    },
                },
            ]
        )

        state = projected["latest_measurement_state"]
        self.assertEqual(state["evidence_snapshot_id"], "m2")
        self.assertEqual(state["observed_at"], "2026-09-14T09:59:00Z")
        self.assertEqual(state["reporting_generation"], "unified")
        self.assertEqual(state["historical_availability_status"], "partially_available")
        self.assertEqual(state["comparability_status"], "Reconcilable")

    def test_retired_not_comparable_state_is_preserved_and_warned(self):
        projected = self.run_projector(
            [
                {
                    "event_id": "e1",
                    "timestamp": "2026-09-14T08:00:00Z",
                    "evidence_snapshot": {
                        "snapshot_id": "legacy-final",
                        "captured_at": "2026-09-14T08:00:00Z",
                        "reporting_generation": "legacy",
                        "date_attribution_semantics": "conversion_date",
                        "historical_availability_status": "retired_or_deleted",
                        "comparability_status": "Not Comparable",
                    },
                }
            ]
        )

        state = projected["latest_measurement_state"]
        self.assertEqual(state["historical_availability_status"], "retired_or_deleted")
        self.assertEqual(state["comparability_status"], "Not Comparable")
        joined = " ".join(state["warnings"]).lower()
        self.assertIn("retired_or_deleted", joined)
        self.assertIn("not comparable", joined)
        self.assertNotIn("zero", state)

    def test_missing_lineage_remains_explicitly_unknown(self):
        projected = self.run_projector(
            [
                {
                    "event_id": "e1",
                    "timestamp": "2026-09-14T08:00:00Z",
                    "evidence_snapshot": {
                        "snapshot_id": "m1",
                        "captured_at": "2026-09-14T08:00:00Z",
                    },
                }
            ]
        )

        state = projected["latest_measurement_state"]
        self.assertIsNone(state["source_system"])
        self.assertIsNone(state["reporting_generation"])
        self.assertEqual(state["historical_availability_status"], "unknown")
        self.assertEqual(state["comparability_status"], "Unknown")
        self.assertIn("missing reporting_generation", " ".join(state["warnings"]).lower())

    def test_expected_scope_rejects_wrong_profile(self):
        result = self.invoke_projector(
            [
                {
                    "event_id": "e1",
                    "timestamp": "2026-09-14T08:00:00Z",
                    "marketplace": "US",
                    "profile_scope": "profile-b",
                    "entity": {"type": "campaign", "id": "campaign-1"},
                    "evidence_snapshot": {"snapshot_id": "m1", "captured_at": "2026-09-14T08:00:00Z"},
                }
            ],
            expected_scope={
                "marketplace": "US",
                "profile_scope": "profile-a",
                "entity_type": "campaign",
                "entity_id": "campaign-1",
            },
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("scope", result.stderr.lower())

    def test_no_evidence_snapshot_returns_null_projection(self):
        projected = self.run_projector(
            [{"event_id": "e1", "timestamp": "2026-09-14T08:00:00Z"}]
        )
        self.assertIsNone(projected["latest_measurement_state"])

    def test_entity_history_and_event_schema_share_historical_availability_enum(self):
        event_schema = json.loads((ROOT / "schemas/optimization-event.json").read_text(encoding="utf-8"))
        history_schema = json.loads((ROOT / "schemas/entity-history.json").read_text(encoding="utf-8"))
        event_enum = event_schema["properties"]["evidence_snapshot"]["properties"]["historical_availability_status"]["enum"]
        history_enum = history_schema["properties"]["latest_measurement_state"]["properties"]["historical_availability_status"]["enum"]
        self.assertEqual(event_enum, history_enum)


if __name__ == "__main__":
    unittest.main()

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
                        "metric_semantic_version": "2026-01",
                        "date_attribution_semantics": "traffic_date",
                        "historical_availability_status": "available",
                        "comparability_status": "Comparable",
                    },
                },
                {
                    "event_id": "e-old",
                    "timestamp": "2026-09-14T11:00:00Z",
                    "marketplace": "US",
                    "profile_scope": "profile-a",
                    "entity": {"type": "campaign", "id": "campaign-1"},
                    "evidence_snapshot": {
                        "snapshot_id": "m1",
                        "captured_at": "2026-09-14T08:59:00Z",
                        "source_system": "amazon_ads",
                        "source_dataset": "legacy-reporting",
                        "acquisition_channel": "api",
                        "reporting_generation": "legacy",
                        "metric_semantic_version": "2025-12",
                        "date_attribution_semantics": "traffic_date",
                        "historical_availability_status": "available",
                        "comparability_status": "Comparable",
                    },
                },
            ]
        )
        self.assertEqual(projected["latest_measurement_state"]["evidence_snapshot_id"], "m2")

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

    def test_fx_lineage_is_preserved_for_historical_replay(self):
        projected = self.run_projector(
            [{
                "event_id": "fx-1",
                "timestamp": "2026-09-23T10:00:00Z",
                "evidence_snapshot": {
                    "snapshot_id": "fx-snapshot",
                    "captured_at": "2026-09-23T09:59:00Z",
                    "reporting_generation": "unified",
                    "date_attribution_semantics": "traffic_date",
                    "historical_availability_status": "available",
                    "comparability_status": "Comparable",
                    "currency_lineage": {
                        "native_currency": "JPY",
                        "reporting_currency": "USD",
                        "currency_conversion_status": "converted",
                        "conversion_timing": "report_generation",
                        "exchange_rate_provenance": "source_provided"
                    }
                }
            }]
        )
        self.assertEqual(projected["latest_measurement_state"]["currency_lineage"], {
            "native_currency": "JPY",
            "reporting_currency": "USD",
            "currency_conversion_status": "converted",
            "conversion_timing": "report_generation",
            "exchange_rate_provenance": "source_provided"
        })

    def test_structured_fx_provenance_is_preserved_for_historical_replay(self):
        provenance = {
            "provider": "source_report",
            "rate_date": "2026-09-23",
            "rate_type": "report_generation",
        }
        projected = self.run_projector(
            [{
                "event_id": "fx-structured-1",
                "timestamp": "2026-09-23T10:00:00Z",
                "evidence_snapshot": {
                    "snapshot_id": "fx-structured-snapshot",
                    "captured_at": "2026-09-23T09:59:00Z",
                    "reporting_generation": "unified",
                    "date_attribution_semantics": "traffic_date",
                    "historical_availability_status": "available",
                    "comparability_status": "Comparable",
                    "currency_lineage": {
                        "native_currency": "JPY",
                        "reporting_currency": "USD",
                        "currency_conversion_status": "converted",
                        "conversion_timing": "report_generation",
                        "exchange_rate_provenance": provenance,
                    },
                },
            }]
        )
        self.assertEqual(
            projected["latest_measurement_state"]["currency_lineage"]["exchange_rate_provenance"],
            provenance,
        )


if __name__ == "__main__":
    unittest.main()

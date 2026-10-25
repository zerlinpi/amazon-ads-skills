"""Catalog-driven observe access regression (synthetic; no Amazon Ads writes).

The canonical capability registry explicitly declares observation-only evidence
surfaces. An independently Verified observe surface can support ONLY a registered
observe capability, never a report/read capability or execution authority.
"""
import copy
import json
import unittest
from pathlib import Path

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references/connector-capability-catalog.json"
SCHEMA = ROOT / "schemas/connector-capability-snapshot.json"


def fixture(capability_id="report-completeness-observe", access_mode="observe"):
    return {
        "snapshot": {
            "connector_id": "synthetic-observation-connector",
            "captured_at": "2026-10-26T00:00:00Z",
            "default_access_mode": "Read-only",
            "capabilities": [{
                "capability_id": capability_id,
                "status": "Supported",
                "access_mode": access_mode,
                "scope": {"marketplaces": ["US"]},
                "bindings": [{
                    "binding_id": "synthetic:verified-observation",
                    "surface_type": "endpoint",
                    "surface_id": "synthetic:report-metadata",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T23:00:00Z",
                    "scope": {"marketplaces": ["US"]},
                    "evidence": [{
                        "kind": "synthetic-contract-test",
                        "reference": "synthetic:observation-probe",
                    }],
                }],
            }],
        },
        "required_capabilities": [capability_id],
        "expected_scope": {"marketplace": "US"},
    }


class ConnectorObserveCatalogContractTests(unittest.TestCase):
    def assert_safe(self, result, status):
        self.assertEqual(result["gate_status"], status, result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertNotIn("High Confidence", result["allowed_decision_classes"])
        self.assertEqual(result["missing_evidence_policy"], "never_zero")

    def test_schema_accepts_registered_observe_access_mode(self):
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.assertTrue(any(c["access_mode"] == "observe" for c in catalog["capabilities"]))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        access_enum = schema["properties"]["capabilities"]["items"]["properties"]["access_mode"]["enum"]
        self.assertIn("observe", access_enum)

    def test_verified_observe_report_completeness_passes(self):
        result = evaluate_connector_capability_gate(fixture())
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertTrue(result["high_confidence_allowed"])
        self.assertEqual(result["requirements"][0]["binding_effect"], "pass")

    def test_verified_observe_metric_semantics_passes(self):
        result = evaluate_connector_capability_gate(fixture("metric-semantics-observe"))
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_verified_observe_date_attribution_passes(self):
        result = evaluate_connector_capability_gate(fixture("date-attribution-observe"))
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_verified_observe_history_availability_passes(self):
        result = evaluate_connector_capability_gate(fixture("historical-availability-observe"))
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_verified_observe_freshness_passes(self):
        result = evaluate_connector_capability_gate(fixture("freshness-observe"))
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_observe_mode_cannot_prove_campaign_report_read(self):
        result = evaluate_connector_capability_gate(fixture("campaign-performance-read"))
        self.assert_safe(result, "Degraded")

    def test_observe_mode_cannot_prove_profile_identity_read(self):
        result = evaluate_connector_capability_gate(fixture("profile-identity-read"))
        self.assert_safe(result, "Degraded")

    def test_observe_mode_requires_independently_verified_binding(self):
        data = fixture()
        data["snapshot"]["capabilities"][0]["bindings"][0]["verification_status"] = "Unverified"
        result = evaluate_connector_capability_gate(data)
        self.assert_safe(result, "Degraded")

    def test_observe_mode_without_binding_does_not_pass(self):
        data = fixture()
        data["snapshot"]["capabilities"][0]["bindings"] = []
        result = evaluate_connector_capability_gate(data)
        self.assert_safe(result, "Degraded")

    def test_write_only_observation_capability_is_blocked(self):
        result = evaluate_connector_capability_gate(fixture(access_mode="write"))
        self.assert_safe(result, "Blocked")

    def test_mixed_observation_capability_remains_ambiguous(self):
        result = evaluate_connector_capability_gate(fixture(access_mode="mixed"))
        self.assert_safe(result, "Degraded")

    def test_unknown_observation_capability_never_becomes_zero(self):
        data = fixture()
        data["snapshot"]["capabilities"][0]["status"] = "Unknown"
        result = evaluate_connector_capability_gate(data)
        self.assert_safe(result, "Blocked")

    def test_valid_read_transport_still_supports_observation(self):
        result = evaluate_connector_capability_gate(fixture(access_mode="read"))
        self.assertEqual(result["gate_status"], "Pass", result)


if __name__ == "__main__":
    unittest.main()

"""Fail-closed tests for snapshot-level connector/source provenance.

All inputs are synthetic; no live Amazon Ads access or mutation.
"""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture():
    return {
        "snapshot": {
            "connector_id": "synthetic:ads-read-connector",
            "captured_at": "2026-10-25T10:00:00Z",
            "default_access_mode": "Read-only",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "bindings": [{
                    "binding_id": "synthetic:report-binding",
                    "surface_type": "report",
                    "surface_id": "synthetic:campaign-report",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T09:00:00Z",
                    "evidence": [{"kind": "contract-test", "reference": "synthetic:read-probe"}],
                }],
            }],
        },
        "required_capabilities": ["campaign-performance-read"],
    }


class ConnectorSnapshotSourceIdentityTests(unittest.TestCase):
    def assert_conservative(self, payload):
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertNotIn("High Confidence", result["allowed_decision_classes"])
        self.assertEqual(result["missing_evidence_policy"], "never_zero")
        self.assertTrue(any("identity" in w.lower() for w in result["warnings"]), result)

    def test_known_connector_identity_passes(self):
        self.assertEqual(evaluate_connector_capability_gate(fixture())["gate_status"], "Pass")

    def test_missing_connector_id_does_not_pass(self):
        payload = fixture()
        del payload["snapshot"]["connector_id"]
        self.assert_conservative(payload)

    def test_null_connector_id_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["connector_id"] = None
        self.assert_conservative(payload)

    def test_blank_connector_id_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["connector_id"] = "   "
        self.assert_conservative(payload)

    def test_unknown_connector_id_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["connector_id"] = "Unknown"
        self.assert_conservative(payload)

    def test_unsupported_connector_id_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["connector_id"] = "Not-Supported"
        self.assert_conservative(payload)

    def test_whitespace_padded_connector_id_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["connector_id"] = " synthetic:ads-read-connector "
        self.assert_conservative(payload)

    def test_explicit_unknown_source_system_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["source_system"] = "Unknown"
        self.assert_conservative(payload)

    def test_explicit_null_source_system_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["source_system"] = None
        self.assert_conservative(payload)

    def test_explicit_unsupported_acquisition_channel_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["acquisition_channel"] = "Unsupported"
        self.assert_conservative(payload)

    def test_explicit_whitespace_acquisition_channel_does_not_pass(self):
        payload = fixture()
        payload["snapshot"]["acquisition_channel"] = " export "
        self.assert_conservative(payload)

    def test_real_id_containing_unknown_is_not_a_placeholder(self):
        payload = fixture()
        payload["snapshot"]["connector_id"] = "synthetic:unknown-account-detector"
        self.assertEqual(evaluate_connector_capability_gate(payload)["gate_status"], "Pass")

    def test_valid_explicit_source_fields_pass(self):
        payload = fixture()
        payload["snapshot"]["source_system"] = "Amazon Ads"
        payload["snapshot"]["acquisition_channel"] = "API"
        self.assertEqual(evaluate_connector_capability_gate(payload)["gate_status"], "Pass")

    def test_valid_other_capability_cannot_rehabilitate_unknown_connector(self):
        payload = fixture()
        extra = copy.deepcopy(payload["snapshot"]["capabilities"][0])
        extra["capability_id"] = "target-performance-read"
        extra["bindings"][0]["binding_id"] = "synthetic:search-term-binding"
        payload["snapshot"]["capabilities"].append(extra)
        payload["required_capabilities"] = ["campaign-performance-read", "target-performance-read"]
        payload["snapshot"]["connector_id"] = "Unknown"
        self.assert_conservative(payload)


if __name__ == "__main__":
    unittest.main()

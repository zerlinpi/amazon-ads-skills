"""RED-first read-side connector access evidence safety tests.

Synthetic fixtures only: no Amazon Ads account calls, writes, or retries.
A Verified surface does not turn a write-only or ambiguous capability into
read-side evidence for the repository's canonical read capabilities.
"""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture():
    return {
        "snapshot": {
            "connector_id": "synthetic-connector",
            "captured_at": "2026-10-25T08:00:00Z",
            "default_access_mode": "Read-only",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "bindings": [{
                    "binding_id": "synthetic:campaign-report",
                    "surface_type": "report",
                    "surface_id": "synthetic:campaign-performance",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T07:00:00Z",
                    "evidence": [{"kind": "contract-test", "reference": "synthetic:read-probe"}],
                }],
            }],
        },
        "required_capabilities": ["campaign-performance-read"],
    }


def check(access, *, missing=False, second_binding=False):
    data = fixture()
    cap = data["snapshot"]["capabilities"][0]
    if missing:
        cap.pop("access_mode")
    else:
        cap["access_mode"] = access
    if second_binding:
        another = copy.deepcopy(cap["bindings"][0])
        another["binding_id"] = "synthetic:secondary-report"
        cap["bindings"].append(another)
    return evaluate_connector_capability_gate(data)


class ConnectorReadAccessEvidenceTests(unittest.TestCase):
    def assert_not_high_confidence(self, result, expected):
        self.assertEqual(result["gate_status"], expected, result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertNotIn("High Confidence", result["allowed_decision_classes"])
        self.assertEqual(result["missing_evidence_policy"], "never_zero")
        self.assertTrue(
            any("access mode" in warning.lower()
                for warning in result["requirements"][0]["warnings"]), result
        )

    def test_verified_report_access_still_passes(self):
        self.assertEqual(check("report")["gate_status"], "Pass")

    def test_verified_read_access_still_passes(self):
        self.assertEqual(check("read")["gate_status"], "Pass")

    def test_verified_export_access_still_passes(self):
        self.assertEqual(check("export")["gate_status"], "Pass")

    def test_verified_stream_access_still_passes(self):
        self.assertEqual(check("stream")["gate_status"], "Pass")

    def test_verified_write_only_access_blocks_read_capability(self):
        self.assert_not_high_confidence(check("write"), "Blocked")

    def test_verified_write_only_access_not_rehabilitated_by_read_only_snapshot_mode(self):
        self.assert_not_high_confidence(check("write"), "Blocked")

    def test_second_verified_binding_cannot_override_write_only_access(self):
        self.assert_not_high_confidence(check("write", second_binding=True), "Blocked")

    def test_unknown_access_mode_degrades_not_zero(self):
        self.assert_not_high_confidence(check("unknown"), "Degraded")

    def test_mixed_access_without_explicit_read_proof_degrades(self):
        self.assert_not_high_confidence(check("mixed"), "Degraded")

    def test_missing_access_mode_degrades(self):
        self.assert_not_high_confidence(check(None, missing=True), "Degraded")

    def test_malformed_access_mode_degrades(self):
        self.assert_not_high_confidence(check("REPORT"), "Degraded")

    def test_boolean_access_mode_degrades(self):
        self.assert_not_high_confidence(check(True), "Degraded")

    def test_unsupported_observe_access_mode_degrades(self):
        self.assert_not_high_confidence(check("observe"), "Degraded")


if __name__ == "__main__":
    unittest.main()

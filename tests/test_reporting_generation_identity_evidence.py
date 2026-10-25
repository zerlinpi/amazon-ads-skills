"""RED: unknown reporting-generation identity cannot establish a comparable report.

Synthetic, read-only capability evidence; no Amazon Ads calls or writes.
"""
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture():
    return {
        "snapshot": {
            "connector_id": "synthetic:report-reader",
            "captured_at": "2026-10-25T12:00:00Z",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "scope": {"marketplaces": ["US"]},
                "data_contract": {
                    "reporting_generation": "unified-reporting",
                    "reporting_generation_status": "active",
                },
                "bindings": [{
                    "binding_id": "synthetic:report-binding",
                    "surface_type": "report",
                    "surface_id": "synthetic:campaign-performance",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T11:00:00Z",
                    "scope": {"marketplaces": ["US"]},
                    "evidence": [{"kind": "contract-test", "reference": "synthetic:probe"}],
                }],
            }],
        },
        "required_capabilities": ["campaign-performance-read"],
        "expected_scope": {"marketplace": "US"},
        "data_requirements": {
            "campaign-performance-read": {"required_reporting_generation": "unified-reporting"}
        },
    }


class ReportingGenerationIdentityEvidenceTests(unittest.TestCase):
    def assert_invalid_requested_generation(self, value):
        payload = fixture()
        payload["data_requirements"]["campaign-performance-read"]["required_reporting_generation"] = value
        payload["snapshot"]["capabilities"][0]["data_contract"]["reporting_generation"] = value
        with self.assertRaisesRegex(ValueError, "required_reporting_generation"):
            evaluate_connector_capability_gate(payload)

    def assert_unavailable_observed_generation(self, value):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["data_contract"]["reporting_generation"] = value
        result = evaluate_connector_capability_gate(payload)
        requirement = result["requirements"][0]
        self.assertEqual(requirement["data_contract_effect"], "unknown", result)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero")

    def test_requested_unknown_is_not_valid_generation(self):
        self.assert_invalid_requested_generation("Unknown")

    def test_requested_unsupported_is_not_valid_generation(self):
        self.assert_invalid_requested_generation("Unsupported")

    def test_requested_partial_is_not_valid_generation(self):
        self.assert_invalid_requested_generation("Partial")

    def test_requested_missing_is_not_valid_generation(self):
        self.assert_invalid_requested_generation("Missing")

    def test_requested_unavailable_is_not_valid_generation(self):
        self.assert_invalid_requested_generation("Unavailable")

    def test_requested_not_available_is_not_valid_generation(self):
        self.assert_invalid_requested_generation("Not Available")

    def test_requested_not_supported_is_not_valid_generation(self):
        self.assert_invalid_requested_generation("Not-Supported")

    def test_requested_padded_is_not_valid_generation(self):
        self.assert_invalid_requested_generation("  unified-reporting  ")

    def test_observed_unknown_is_not_definitive_mismatch(self):
        self.assert_unavailable_observed_generation("Unknown")

    def test_observed_unsupported_is_not_definitive_mismatch(self):
        self.assert_unavailable_observed_generation("Unsupported")

    def test_observed_partial_is_not_definitive_mismatch(self):
        self.assert_unavailable_observed_generation("Partial")

    def test_observed_not_available_is_not_definitive_mismatch(self):
        self.assert_unavailable_observed_generation("Not Available")

    def test_observed_padded_matching_generation_is_not_verified(self):
        self.assert_unavailable_observed_generation("  unified-reporting  ")

    def test_observed_empty_generation_remains_unknown(self):
        self.assert_unavailable_observed_generation("")

    def test_concrete_matching_generation_passes(self):
        result = evaluate_connector_capability_gate(fixture())
        self.assertEqual(result["gate_status"], "Pass")
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "pass")

    def test_concrete_case_insensitive_generation_match_remains_compatible(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["data_contract"]["reporting_generation"] = "UNIFIED-REPORTING"
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass")

    def test_concrete_mismatched_generation_remains_blocked(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["data_contract"]["reporting_generation"] = "legacy-sponsored-ads"
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Blocked")
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "blocked")

    def test_no_generation_requirement_remains_not_evaluated(self):
        payload = fixture()
        del payload["data_requirements"]
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass")
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "not_evaluated")


if __name__ == "__main__":
    unittest.main()

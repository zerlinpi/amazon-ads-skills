"""Fail-closed identity proof for Verified connector surface bindings.

Synthetic evidence only. A repeated unavailable label is not a concrete
binding, surface or provenance reference; no live Amazon Ads operations.
"""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def payload():
    return {
        "snapshot": {
            "connector_id": "synthetic-connector",
            "connector_version": "1.0",
            "captured_at": "2026-10-25T06:00:00Z",
            "default_access_mode": "Read-only",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "bindings": [{
                    "binding_id": "synthetic:report-v1",
                    "surface_type": "report",
                    "surface_id": "synthetic-report",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T05:00:00Z",
                    "evidence": [{
                        "kind": "contract-test",
                        "reference": "synthetic-test",
                        "observed_at": "2026-10-25T04:00:00Z",
                    }],
                }],
            }],
        },
        "required_capabilities": ["campaign-performance-read"],
    }


def binding(p):
    return p["snapshot"]["capabilities"][0]["bindings"][0]


def check(p):
    return evaluate_connector_capability_gate(p)


class VerifiedBindingIdentityTests(unittest.TestCase):
    def assert_not_verified(self, p):
        result = check(p)
        self.assertNotEqual(result["gate_status"], "Pass", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["requirements"][0]["verified_binding_ids"], [], result)

    def test_baseline_real_identity_passes(self):
        self.assertEqual(check(payload())["gate_status"], "Pass")

    def test_verified_binding_id_unknown_cannot_pass(self):
        p = payload()
        binding(p)["binding_id"] = "Unknown"
        self.assert_not_verified(p)

    def test_verified_binding_id_unsupported_cannot_pass(self):
        p = payload()
        binding(p)["binding_id"] = "Unsupported"
        self.assert_not_verified(p)

    def test_verified_binding_id_partial_cannot_pass(self):
        p = payload()
        binding(p)["binding_id"] = "Partial"
        self.assert_not_verified(p)

    def test_verified_binding_id_whitespace_padded_cannot_pass(self):
        p = payload()
        binding(p)["binding_id"] = " synthetic:report-v1 "
        self.assert_not_verified(p)

    def test_verified_surface_id_unknown_cannot_pass(self):
        p = payload()
        binding(p)["surface_id"] = "Unknown"
        self.assert_not_verified(p)

    def test_verified_surface_id_not_available_cannot_pass(self):
        p = payload()
        binding(p)["surface_id"] = "Not Available"
        self.assert_not_verified(p)

    def test_verified_surface_id_whitespace_padded_cannot_pass(self):
        p = payload()
        binding(p)["surface_id"] = " synthetic-report "
        self.assert_not_verified(p)

    def test_verified_evidence_kind_unknown_cannot_pass(self):
        p = payload()
        binding(p)["evidence"][0]["kind"] = "Unknown"
        self.assert_not_verified(p)

    def test_verified_evidence_reference_unsupported_cannot_pass(self):
        p = payload()
        binding(p)["evidence"][0]["reference"] = "Unsupported"
        self.assert_not_verified(p)

    def test_verified_evidence_reference_not_supported_cannot_pass(self):
        p = payload()
        binding(p)["evidence"][0]["reference"] = "Not-Supported"
        self.assert_not_verified(p)

    def test_verified_evidence_reference_whitespace_padded_cannot_pass(self):
        p = payload()
        binding(p)["evidence"][0]["reference"] = " synthetic-test "
        self.assert_not_verified(p)

    def test_nested_placeholder_only_evidence_cannot_pass(self):
        p = payload()
        binding(p)["evidence"] = [
            {"kind": "Unknown", "reference": "Unknown"},
            {"kind": "Partial", "reference": "Unavailable"},
        ]
        self.assert_not_verified(p)

    def test_valid_secondary_binding_can_substantiate_capability(self):
        p = payload()
        bad = copy.deepcopy(binding(p))
        bad["binding_id"] = "synthetic:bad-binding"
        bad["surface_id"] = "Unknown"
        p["snapshot"]["capabilities"][0]["bindings"].insert(0, bad)
        result = check(p)
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["requirements"][0]["verified_binding_ids"], ["synthetic:report-v1"])

    def test_valid_evidence_can_coexist_with_unusable_extra_record(self):
        p = payload()
        binding(p)["evidence"].append({"kind": "Unknown", "reference": "Unknown"})
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_real_identity_containing_word_unknown_is_not_placeholder(self):
        p = payload()
        binding(p)["binding_id"] = "synthetic:unknown-report-v2"
        binding(p)["surface_id"] = "unknown-metric-report"
        binding(p)["evidence"][0]["reference"] = "fixture-unknown-case"
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_explicit_zero_like_surface_identity_is_not_numeric_zero(self):
        p = payload()
        binding(p)["surface_id"] = "0"
        self.assertEqual(check(p)["gate_status"], "Pass")


if __name__ == "__main__":
    unittest.main()

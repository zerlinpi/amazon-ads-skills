"""RED-first: verified connector bindings need temporally coherent provenance.

A Supported capability and Verified label cannot make a future, malformed,
or impossible binding/evidence timestamp valid when freshness is not requested.
Synthetic data only; never contacts or mutates Amazon Ads.
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


def check(p):
    return evaluate_connector_capability_gate(p)


class ConnectorBindingTemporalLineageTests(unittest.TestCase):
    def assert_not_high_confidence(self, p):
        result = check(p)
        self.assertNotEqual(result["gate_status"], "Pass", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["requirements"][0]["verified_binding_ids"], [], result)

    def test_binding_after_snapshot_cannot_pass_without_freshness_requirement(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["observed_at"] = "2026-10-25T07:00:00Z"
        self.assert_not_high_confidence(p)

    def test_binding_equal_snapshot_time_is_valid(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["observed_at"] = "2026-10-25T06:00:00Z"
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_binding_timestamp_without_timezone_is_not_verified(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["observed_at"] = "2026-10-25T05:00:00"
        self.assert_not_high_confidence(p)

    def test_binding_timestamp_malformed_is_not_verified(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["observed_at"] = "not-a-date"
        self.assert_not_high_confidence(p)

    def test_binding_timestamp_with_ambiguous_negative_zero_offset_is_not_verified(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["observed_at"] = "2026-10-25T05:00:00-00:00"
        self.assert_not_high_confidence(p)

    def test_supporting_evidence_after_binding_is_not_verified_without_freshness(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["evidence"][0]["observed_at"] = "2026-10-25T05:30:00Z"
        self.assert_not_high_confidence(p)

    def test_supporting_evidence_after_snapshot_is_not_verified(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["evidence"][0]["observed_at"] = "2026-10-25T07:00:00Z"
        self.assert_not_high_confidence(p)

    def test_malformed_supporting_evidence_timestamp_is_not_verified(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["evidence"][0]["observed_at"] = "yesterday"
        self.assert_not_high_confidence(p)

    def test_missing_snapshot_capture_cannot_prove_binding_chronology(self):
        p = payload()
        p["snapshot"].pop("captured_at")
        self.assert_not_high_confidence(p)

    def test_invalid_snapshot_capture_cannot_prove_binding_chronology(self):
        p = payload()
        p["snapshot"]["captured_at"] = "2026-10-25T06:00:00"
        self.assert_not_high_confidence(p)

    def test_valid_timezone_offsets_are_compared_as_instants(self):
        p = payload()
        p["snapshot"]["captured_at"] = "2026-10-25T14:00:00+08:00"
        p["snapshot"]["capabilities"][0]["bindings"][0]["observed_at"] = "2026-10-25T01:00:00-04:00"
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_legacy_identifiable_undated_supporting_evidence_still_passes(self):
        p = payload()
        p["snapshot"]["capabilities"][0]["bindings"][0]["evidence"][0].pop("observed_at")
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_valid_secondary_binding_can_support_capability(self):
        p = payload()
        invalid = copy.deepcopy(p["snapshot"]["capabilities"][0]["bindings"][0])
        invalid["binding_id"] = "synthetic:future-binding"
        invalid["observed_at"] = "2026-10-25T07:00:00Z"
        p["snapshot"]["capabilities"][0]["bindings"].insert(0, invalid)
        result = check(p)
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["requirements"][0]["verified_binding_ids"], ["synthetic:report-v1"])


if __name__ == "__main__":
    unittest.main()

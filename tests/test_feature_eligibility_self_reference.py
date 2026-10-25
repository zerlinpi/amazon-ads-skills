"""Feature eligibility cannot cite its own connector binding as independent proof.

Synthetic read-side provenance only: matching references are not authenticated
entitlement evidence. No Amazon Ads calls or writes are made.
"""
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate
from tests.test_feature_eligibility_evidence_join import fixture


def check(payload):
    return evaluate_connector_capability_gate(payload)


def binding(payload):
    return payload["snapshot"]["capabilities"][0]["bindings"][0]


class FeatureEligibilitySelfReferenceTests(unittest.TestCase):
    def assert_unknown(self, payload):
        result = check(payload)
        self.assertEqual(result["feature_eligibility_effect"], "unknown", result)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero")
        self.assertTrue(any("eligibility" in warning and "reference" in warning for warning in result["warnings"]), result)

    def test_same_binding_evidence_reference_cannot_prove_eligible(self):
        payload = fixture()
        payload["feature_eligibility_evidence"]["source_reference"] = binding(payload)["evidence"][0]["reference"]
        self.assert_unknown(payload)

    def test_same_binding_surface_id_cannot_prove_eligible(self):
        payload = fixture()
        payload["feature_eligibility_evidence"]["source_reference"] = binding(payload)["surface_id"]
        self.assert_unknown(payload)

    def test_same_binding_id_cannot_prove_eligible(self):
        payload = fixture()
        payload["feature_eligibility_evidence"]["source_reference"] = binding(payload)["binding_id"]
        self.assert_unknown(payload)

    def test_self_referential_ineligible_is_not_verified_exclusion(self):
        payload = fixture()
        payload["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        payload["feature_eligibility_evidence"]["source_reference"] = binding(payload)["evidence"][0]["reference"]
        self.assert_unknown(payload)

    def test_distinct_feature_specific_reference_retains_pass(self):
        result = check(fixture())
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["feature_eligibility_effect"], "pass", result)

    def test_distinct_verified_ineligible_still_blocks(self):
        payload = fixture()
        payload["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        result = check(payload)
        self.assertEqual(result["gate_status"], "Blocked", result)
        self.assertEqual(result["feature_eligibility_effect"], "blocked", result)

    def test_distinct_reference_does_not_prove_raw_source_authenticity(self):
        payload = fixture()
        payload["feature_eligibility_evidence"]["source_reference"] = "synthetic:other-source-record"
        result = check(payload)
        self.assertEqual(result["feature_eligibility_effect"], "pass", result)
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_legacy_without_feature_requirement_still_passes(self):
        payload = fixture()
        del payload["feature_eligibility_requirement"]
        del payload["feature_eligibility_evidence"]
        self.assertEqual(check(payload)["gate_status"], "Pass")


if __name__ == "__main__":
    unittest.main()

"""RED-first: unverified connector probes cannot double as independent feature eligibility.

A required capability may contain a verified binding for its read-side scope
and an unverified probe. Reusing the unverified probe's reference as the
separate feature-eligibility source is still self-reference. Synthetic only.
"""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate
from tests.test_feature_eligibility_evidence_join import fixture


def with_unverified_probe():
    payload = fixture()
    bindings = payload["snapshot"]["capabilities"][0]["bindings"]
    unverified = copy.deepcopy(bindings[0])
    unverified["verification_status"] = "Unverified"
    unverified["binding_id"] = "synthetic:unverified-binding"
    unverified["surface_id"] = "synthetic:unverified-surface"
    unverified["evidence"][0]["reference"] = "synthetic:unverified-probe"
    bindings.append(unverified)
    return payload, unverified


class FeatureEligibilityUnverifiedBindingReferenceTests(unittest.TestCase):
    def assert_not_independent(self, payload):
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["feature_source_independence_effect"], "unknown", result)
        self.assertEqual(result["feature_eligibility_effect"], "unknown", result)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["requirements"][0]["gate_effect"], "pass", result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero")

    def test_unverified_probe_reference_cannot_prove_eligible(self):
        payload, probe = with_unverified_probe()
        payload["feature_eligibility_evidence"]["source_reference"] = probe["evidence"][0]["reference"]
        self.assert_not_independent(payload)

    def test_unverified_binding_id_cannot_prove_eligible(self):
        payload, probe = with_unverified_probe()
        payload["feature_eligibility_evidence"]["source_reference"] = probe["binding_id"]
        self.assert_not_independent(payload)

    def test_unverified_surface_id_cannot_prove_eligible(self):
        payload, probe = with_unverified_probe()
        payload["feature_eligibility_evidence"]["source_reference"] = probe["surface_id"]
        self.assert_not_independent(payload)

    def test_unverified_probe_reference_cannot_prove_ineligible(self):
        payload, probe = with_unverified_probe()
        payload["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        payload["feature_eligibility_evidence"]["source_reference"] = probe["evidence"][0]["reference"]
        self.assert_not_independent(payload)
        result = evaluate_connector_capability_gate(payload)
        self.assertFalse(any("verified feature-specific eligibility is explicitly Ineligible" in w for w in result["warnings"]))

    def test_distinct_feature_reference_with_unverified_probe_retains_pass(self):
        payload, _ = with_unverified_probe()
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["feature_source_independence_effect"], "pass", result)
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_no_feature_requirement_retains_legacy_capability_pass(self):
        payload, _ = with_unverified_probe()
        del payload["feature_eligibility_requirement"]
        del payload["feature_eligibility_evidence"]
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["feature_source_independence_effect"], "not_evaluated", result)


if __name__ == "__main__":
    unittest.main()

"""RED-first: non-required connector probes cannot double as feature entitlement.

A decision may require only campaign-performance-read while the same connector
snapshot also contains unrelated probes. Reusing any of those probe identities
as supposedly independent feature eligibility is still source self-reference.
Synthetic read-only evidence; no Amazon Ads account access or mutation.
"""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate
from tests.test_feature_eligibility_evidence_join import fixture


def with_nonrequired_probe(*, verification="Unverified", status="Supported"):
    payload = fixture()
    extra = copy.deepcopy(payload["snapshot"]["capabilities"][0])
    extra["capability_id"] = "retail-readiness-read"
    extra["status"] = status
    extra["access_mode"] = "read"
    extra["bindings"][0]["verification_status"] = verification
    extra["bindings"][0]["binding_id"] = "synthetic:unrequired-binding"
    extra["bindings"][0]["surface_id"] = "synthetic:unrequired-surface"
    extra["bindings"][0]["evidence"][0]["reference"] = "synthetic:unrequired-probe"
    payload["snapshot"]["capabilities"].append(extra)
    self_required = payload["required_capabilities"]
    assert self_required == ["campaign-performance-read"]
    return payload, extra["bindings"][0]


class CrossCapabilityFeatureSourceReferenceTests(unittest.TestCase):
    def assert_degraded(self, payload):
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["feature_source_independence_effect"], "unknown", result)
        self.assertEqual(result["feature_eligibility_effect"], "unknown", result)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["requirements"][0]["gate_effect"], "pass", result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero", result)

    def test_unrequired_unverified_evidence_reference_cannot_prove_eligible(self):
        payload, binding = with_nonrequired_probe()
        payload["feature_eligibility_evidence"]["source_reference"] = binding["evidence"][0]["reference"]
        self.assert_degraded(payload)

    def test_unrequired_unverified_binding_id_cannot_prove_eligible(self):
        payload, binding = with_nonrequired_probe()
        payload["feature_eligibility_evidence"]["source_reference"] = binding["binding_id"]
        self.assert_degraded(payload)

    def test_unrequired_unverified_surface_id_cannot_prove_eligible(self):
        payload, binding = with_nonrequired_probe()
        payload["feature_eligibility_evidence"]["source_reference"] = binding["surface_id"]
        self.assert_degraded(payload)

    def test_unrequired_verified_probe_cannot_prove_eligible(self):
        payload, binding = with_nonrequired_probe(verification="Verified")
        payload["feature_eligibility_evidence"]["source_reference"] = binding["evidence"][0]["reference"]
        self.assert_degraded(payload)

    def test_unrequired_unsupported_probe_cannot_prove_eligible(self):
        payload, binding = with_nonrequired_probe(status="Unsupported")
        payload["feature_eligibility_evidence"]["source_reference"] = binding["evidence"][0]["reference"]
        self.assert_degraded(payload)

    def test_unrequired_probe_cannot_prove_ineligible_exclusion(self):
        payload, binding = with_nonrequired_probe()
        payload["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        payload["feature_eligibility_evidence"]["source_reference"] = binding["evidence"][0]["reference"]
        self.assert_degraded(payload)
        result = evaluate_connector_capability_gate(payload)
        self.assertFalse(any("verified feature-specific eligibility is explicitly Ineligible" in w for w in result["warnings"]))

    def test_distinct_feature_reference_remains_compatible(self):
        payload, _ = with_nonrequired_probe()
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["feature_source_independence_effect"], "pass", result)

    def test_distinct_ineligible_reference_still_blocks(self):
        payload, _ = with_nonrequired_probe()
        payload["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Blocked", result)

    def test_without_feature_requirement_legacy_passes(self):
        payload, _ = with_nonrequired_probe()
        del payload["feature_eligibility_requirement"]
        del payload["feature_eligibility_evidence"]
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["feature_source_independence_effect"], "not_evaluated", result)


if __name__ == "__main__":
    unittest.main()

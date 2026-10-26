"""RED-first: capability-level provenance is not independent feature entitlement.

The connector snapshot schema supports capability.evidence[] separately from
binding.evidence[]. Reusing either for eligibility is self-reference, even on
non-required/Unsupported capabilities. Synthetic read-only inputs only.
"""
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate
from tests.test_feature_eligibility_evidence_join import fixture
from tests.test_feature_eligibility_cross_capability_reference import with_nonrequired_probe


REFERENCE = "synthetic:capability-level-probe"


def with_capability_evidence(*, extra=False, status="Supported"):
    if extra:
        payload, _ = with_nonrequired_probe(status=status)
        capability = payload["snapshot"]["capabilities"][-1]
    else:
        payload = fixture()
        capability = payload["snapshot"]["capabilities"][0]
    capability["evidence"] = [{"kind": "synthetic-probe", "reference": REFERENCE}]
    return payload


class FeatureEligibilityCapabilityEvidenceReferenceTests(unittest.TestCase):
    def assert_degraded(self, payload):
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["feature_source_independence_effect"], "unknown", result)
        self.assertEqual(result["feature_eligibility_effect"], "unknown", result)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero", result)

    def test_required_capability_evidence_cannot_prove_eligible(self):
        payload = with_capability_evidence()
        payload["feature_eligibility_evidence"]["source_reference"] = REFERENCE
        self.assert_degraded(payload)

    def test_nonrequired_capability_evidence_cannot_prove_eligible(self):
        payload = with_capability_evidence(extra=True)
        payload["feature_eligibility_evidence"]["source_reference"] = REFERENCE
        self.assert_degraded(payload)

    def test_unsupported_capability_evidence_cannot_prove_eligible(self):
        payload = with_capability_evidence(extra=True, status="Unsupported")
        payload["feature_eligibility_evidence"]["source_reference"] = REFERENCE
        self.assert_degraded(payload)

    def test_capability_evidence_cannot_prove_ineligible(self):
        payload = with_capability_evidence()
        payload["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        payload["feature_eligibility_evidence"]["source_reference"] = REFERENCE
        self.assert_degraded(payload)
        result = evaluate_connector_capability_gate(payload)
        self.assertFalse(any("verified feature-specific eligibility is explicitly Ineligible" in w
                             for w in result["warnings"]), result)

    def test_distinct_eligibility_reference_remains_compatible(self):
        payload = with_capability_evidence(extra=True)
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["feature_source_independence_effect"], "pass", result)

    def test_distinct_ineligible_reference_still_blocks(self):
        payload = with_capability_evidence()
        payload["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Blocked", result)

    def test_legacy_without_feature_requirement_remains_compatible(self):
        payload = with_capability_evidence()
        del payload["feature_eligibility_requirement"]
        del payload["feature_eligibility_evidence"]
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["feature_source_independence_effect"], "not_evaluated", result)


if __name__ == "__main__":
    unittest.main()

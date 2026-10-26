"""RED-first: a Ready holdout cannot promote placeholder or malformed isolation proof.

Synthetic evidence only; no remote Amazon Ads reads or writes.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def plan_with_evidence(**updates):
    plan = base_plan()
    plan["comparison"]["isolation_evidence"][0].update(updates)
    return plan


class ReadyIsolationEvidenceIntegrityTests(unittest.TestCase):
    def assert_rejected(self, plan):
        errors = validate_experiment_plan(plan)
        self.assertTrue(errors, "unresolved verified isolation proof must not establish Ready")
        self.assertIn("isolation_evidence", " | ".join(errors), errors)

    def test_verified_unknown_evidence_is_not_proof(self):
        self.assert_rejected(plan_with_evidence(evidence="Unknown"))

    def test_verified_not_supported_evidence_is_not_proof(self):
        self.assert_rejected(plan_with_evidence(evidence="Not Supported"))

    def test_verified_padded_placeholder_evidence_is_not_proof(self):
        self.assert_rejected(plan_with_evidence(evidence=" Partial "))

    def test_explicit_null_verified_at_is_not_a_verified_instant(self):
        self.assert_rejected(plan_with_evidence(verified_at=None))

    def test_naive_verified_at_is_not_a_verified_instant(self):
        self.assert_rejected(plan_with_evidence(verified_at="2026-09-03T00:00:00"))

    def test_malformed_verified_at_is_not_a_verified_instant(self):
        self.assert_rejected(plan_with_evidence(verified_at="Not Available"))

    def test_explicit_unknown_source_is_not_provenance(self):
        self.assert_rejected(plan_with_evidence(source="Unavailable"))

    def test_padded_source_is_not_concrete_provenance(self):
        self.assert_rejected(plan_with_evidence(source=" synthetic:boundary-probe "))

    def test_valid_optional_source_and_timestamp_remain_compatible(self):
        plan = plan_with_evidence(
            source="synthetic:boundary-probe",
            verified_at="2026-09-03T01:00:00+01:00",
        )
        self.assertEqual([], validate_experiment_plan(plan))

    def test_legacy_verified_evidence_without_optional_fields_remains_ready(self):
        self.assertEqual([], validate_experiment_plan(base_plan()))

    def test_evidence_sentence_containing_unknown_word_is_not_a_placeholder(self):
        plan = plan_with_evidence(
            evidence="Synthetic boundary verified; unknown risks separately reviewed",
        )
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_only_can_preserve_unresolved_isolation_evidence(self):
        plan = plan_with_evidence(evidence="Unknown", verified_at=None, source="Missing")
        plan["status"] = "Shadow Only"
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

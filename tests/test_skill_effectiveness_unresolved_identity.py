"""RED-first: unresolved benchmark identities cannot certify longitudinal comparability.

Synthetic read-only harness metadata. No advertiser data, model invocation, or Ads writes.
"""
from copy import deepcopy
import unittest

from scripts.evaluate_skill_effectiveness_comparability import evaluate


BASE = {
    "skill": "budget-optimization",
    "fixture_id": "account-budget-cap-upstream-bottleneck",
    "fixture_version": "1",
    "mode": "Ablation",
    "harness": {
        "runtime": "synthetic-harness",
        "model": "model-x",
        "model_version": "2026-09-19",
        "config_hash": "cfg-1",
        "tool_profile_hash": "tools-1",
        "evidence_hash": "evidence-1",
        "measurement_contract": {
            "evaluator_id": "evaluator-1",
            "evaluator_version": "1",
            "rubric_version": None,
        },
    },
}


def with_identity(path, left, right=...):
    baseline = deepcopy(BASE)
    candidate = deepcopy(BASE)
    parts = path.split(".")
    for record, value in ((baseline, left), (candidate, left if right is ... else right)):
        parent = record
        for part in parts[:-1]:
            parent = parent[part]
        parent[parts[-1]] = value
    return evaluate({"baseline": baseline, "candidate": candidate})


class UnresolvedSkillEffectivenessIdentityTests(unittest.TestCase):
    def assert_unknown(self, path, value, other=...):
        result = with_identity(path, value, other)
        self.assertEqual(result["comparability_status"], "Unknown", result)
        self.assertIn(path, result["unknown_fields"], result)

    def test_repeated_unknown_model_version_is_not_comparable(self):
        self.assert_unknown("harness.model_version", "Unknown")

    def test_repeated_partial_config_hash_is_not_comparable(self):
        self.assert_unknown("harness.config_hash", "Partial")

    def test_repeated_missing_tool_profile_hash_is_not_comparable(self):
        self.assert_unknown("harness.tool_profile_hash", "Missing")

    def test_repeated_unsupported_evidence_hash_is_not_comparable(self):
        self.assert_unknown("harness.evidence_hash", "Unsupported")

    def test_not_applicable_evaluator_id_is_not_comparable(self):
        self.assert_unknown("harness.measurement_contract.evaluator_id", "Not Applicable")

    def test_na_fixture_version_is_not_comparable(self):
        self.assert_unknown("fixture_version", "N/A")

    def test_normalized_not_supported_runtime_is_not_comparable(self):
        self.assert_unknown("harness.runtime", "Not_Supported")

    def test_boolean_model_version_is_not_comparable(self):
        self.assert_unknown("harness.model_version", True)

    def test_array_evidence_hash_is_not_comparable(self):
        self.assert_unknown("harness.evidence_hash", ["evidence-1"])

    def test_padded_model_identity_is_not_comparable(self):
        self.assert_unknown("harness.model", " model-x ")

    def test_repeated_unknown_rubric_version_is_not_comparable(self):
        self.assert_unknown("harness.measurement_contract.rubric_version", "Unknown")

    def test_one_sided_placeholder_is_unknown_not_mismatch(self):
        self.assert_unknown("harness.model_version", "Unknown", "2026-09-19")

    def test_opaque_identity_containing_unknown_word_remains_comparable(self):
        result = with_identity("harness.model", "model-unknown-v2")
        self.assertEqual(result["comparability_status"], "Comparable", result)

    def test_explicit_null_rubric_version_remains_comparable(self):
        result = with_identity("harness.measurement_contract.rubric_version", None)
        self.assertEqual(result["comparability_status"], "Comparable", result)

    def test_real_version_mismatch_remains_not_comparable(self):
        result = with_identity("harness.model_version", "2026-09-19", "2026-09-20")
        self.assertEqual(result["comparability_status"], "Not Comparable", result)

    def test_null_to_real_rubric_change_is_not_comparable(self):
        result = with_identity("harness.measurement_contract.rubric_version", None, "rubric-v2")
        self.assertEqual(result["comparability_status"], "Not Comparable", result)


if __name__ == "__main__":
    unittest.main()

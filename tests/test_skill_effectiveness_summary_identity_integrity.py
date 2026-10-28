"""RED-first: a measured Skill benchmark must have concrete, schema-aligned identity.

Synthetic paired trials only; no model invocation or live Amazon Ads mutation.
"""
from copy import deepcopy
import unittest

from scripts.summarize_skill_effectiveness import summarize


def benchmark():
    return {
        "benchmark_id": "synthetic-identity-1",
        "skill": "budget-optimization",
        "fixture_id": "account-budget-cap-upstream-bottleneck",
        "fixture_version": "1",
        "mode": "Ablation",
        "harness": {
            "runtime": "synthetic-harness",
            "model": "model-x",
            "model_version": "2026-10-28",
            "config_hash": "cfg-1",
            "tool_profile_hash": "tools-1",
            "evidence_hash": "fixture-1",
            "measurement_contract": {
                "evaluator_id": "synthetic-evaluator",
                "evaluator_version": "1",
                "rubric_version": None,
            },
        },
        "trials": [
            {"pair_id": "p1", "trial_id": "with-1", "variant": "with_skill",
             "acceptable_decision": True, "forbidden_behavior": False,
             "required_observations_met": True},
            {"pair_id": "p1", "trial_id": "without-1", "variant": "without_skill",
             "acceptable_decision": False, "forbidden_behavior": False,
             "required_observations_met": True},
        ],
    }


class SkillSummaryIdentityIntegrityTests(unittest.TestCase):
    def reject(self, path, value, *, missing=False):
        payload = benchmark()
        parts = path.split(".")
        node = payload
        for part in parts[:-1]:
            node = node[part]
        if missing:
            node.pop(parts[-1])
        else:
            node[parts[-1]] = value
        with self.assertRaisesRegex(ValueError, parts[-1]):
            summarize(payload)

    def test_missing_benchmark_id_rejected(self):
        self.reject("benchmark_id", None, missing=True)

    def test_numeric_benchmark_id_rejected(self):
        self.reject("benchmark_id", 123)

    def test_padded_benchmark_id_rejected(self):
        self.reject("benchmark_id", " benchmark-1 ")

    def test_missing_skill_rejected(self):
        self.reject("skill", None, missing=True)

    def test_missing_fixture_id_rejected(self):
        self.reject("fixture_id", None, missing=True)

    def test_invalid_mode_rejected(self):
        self.reject("mode", "Shadow")

    def test_missing_mode_rejected(self):
        self.reject("mode", None, missing=True)

    def test_list_mode_rejected_with_value_error(self):
        self.reject("mode", [])

    def test_missing_runtime_rejected(self):
        self.reject("harness.runtime", None, missing=True)

    def test_missing_model_rejected(self):
        self.reject("harness.model", None, missing=True)

    def test_missing_model_version_rejected(self):
        self.reject("harness.model_version", None, missing=True)

    def test_unknown_model_version_rejected(self):
        self.reject("harness.model_version", "Unknown")

    def test_partial_evaluator_version_rejected(self):
        self.reject("harness.measurement_contract.evaluator_version", "Partial")

    def test_na_fixture_version_rejected(self):
        self.reject("fixture_version", "N/A")

    def test_padded_runtime_rejected(self):
        self.reject("harness.runtime", " synthetic-harness ")

    def test_malformed_optional_config_hash_rejected(self):
        self.reject("harness.config_hash", ["cfg-1"])

    def test_unknown_optional_evidence_hash_rejected(self):
        self.reject("harness.evidence_hash", "Unknown")

    def test_malformed_optional_tool_hash_rejected(self):
        self.reject("harness.tool_profile_hash", 12)

    def test_padded_rubric_version_rejected(self):
        self.reject("harness.measurement_contract.rubric_version", " rubric-v1 ")

    def test_valid_opaque_identity_with_unknown_substring_preserved(self):
        payload = benchmark()
        payload["harness"]["model"] = "model-unknown-v2"
        self.assertEqual(summarize(payload)["effectiveness_status"], "Measured")

    def test_optional_null_hashes_remain_compatible(self):
        payload = benchmark()
        for field in ("config_hash", "tool_profile_hash", "evidence_hash"):
            payload["harness"][field] = None
        result = summarize(payload)
        self.assertEqual(result["effectiveness_status"], "Measured")
        self.assertIsNone(result["measurement_identity"]["config_hash"])

    def test_explicit_null_rubric_remains_compatible(self):
        self.assertIsNone(summarize(benchmark())["measurement_identity"]["rubric_version"])

    def test_valid_paired_result_preserved(self):
        result = summarize(deepcopy(benchmark()))
        self.assertEqual(result["comparable_pair_count"], 1)
        self.assertEqual(result["delta"]["full_pass_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()

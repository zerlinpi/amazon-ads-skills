"""RED-first: one benchmark trial execution cannot be counted as independent twice.

Synthetic paired Skill-evaluation metadata only; no model invocation or Ads writes.
"""
from copy import deepcopy
import unittest

from scripts.summarize_skill_effectiveness import summarize


def benchmark():
    def trial(pair_id, variant, trial_id):
        return {
            "pair_id": pair_id,
            "trial_id": trial_id,
            "variant": variant,
            "acceptable_decision": variant == "with_skill",
            "forbidden_behavior": False,
            "required_observations_met": True,
        }

    return {
        "benchmark_id": "synthetic-trial-identity",
        "skill": "budget-optimization",
        "fixture_id": "account-budget-cap-upstream-bottleneck",
        "fixture_version": "1",
        "mode": "Ablation",
        "harness": {
            "runtime": "synthetic-harness",
            "model": "model-x",
            "model_version": "2026-10-28",
            "config_hash": "config-v1",
            "tool_profile_hash": "tools-v1",
            "evidence_hash": "fixture-v1",
            "measurement_contract": {
                "evaluator_id": "synthetic-evaluator",
                "evaluator_version": "1",
                "rubric_version": None,
            },
        },
        "trials": [
            trial("p1", "with_skill", "run-1-with"),
            trial("p1", "without_skill", "run-1-without"),
            trial("p2", "with_skill", "run-2-with"),
            trial("p2", "without_skill", "run-2-without"),
        ],
    }


def mark_nonmeasured(trial, status):
    trial["measurement_status"] = status
    trial["acceptable_decision"] = None
    trial["forbidden_behavior"] = None
    trial["required_observations_met"] = None


class SkillEffectivenessTrialIdentityTests(unittest.TestCase):
    def assert_duplicate_rejected(self, payload):
        with self.assertRaisesRegex(ValueError, "trial_id"):
            summarize(payload)

    def test_reused_with_skill_run_across_pairs_is_not_two_samples(self):
        payload = benchmark()
        payload["trials"][2]["trial_id"] = payload["trials"][0]["trial_id"]
        self.assert_duplicate_rejected(payload)

    def test_reused_without_skill_run_across_pairs_is_not_two_samples(self):
        payload = benchmark()
        payload["trials"][3]["trial_id"] = payload["trials"][1]["trial_id"]
        self.assert_duplicate_rejected(payload)

    def test_reused_run_across_variants_and_pairs_is_not_independent(self):
        payload = benchmark()
        payload["trials"][3]["trial_id"] = payload["trials"][0]["trial_id"]
        self.assert_duplicate_rejected(payload)

    def test_two_arms_of_same_pair_cannot_share_execution_identity(self):
        payload = benchmark()
        payload["trials"][1]["trial_id"] = payload["trials"][0]["trial_id"]
        self.assert_duplicate_rejected(payload)

    def test_scorer_error_does_not_make_reused_run_id_safe(self):
        payload = benchmark()
        payload["trials"][2]["trial_id"] = payload["trials"][0]["trial_id"]
        mark_nonmeasured(payload["trials"][2], "scorer_error")
        self.assert_duplicate_rejected(payload)

    def test_insufficient_evidence_does_not_make_reused_run_id_safe(self):
        payload = benchmark()
        payload["trials"][2]["trial_id"] = payload["trials"][0]["trial_id"]
        mark_nonmeasured(payload["trials"][2], "insufficient_evidence")
        self.assert_duplicate_rejected(payload)

    def test_harness_error_does_not_make_reused_run_id_safe(self):
        payload = benchmark()
        payload["trials"][2]["trial_id"] = payload["trials"][0]["trial_id"]
        mark_nonmeasured(payload["trials"][2], "harness_error")
        self.assert_duplicate_rejected(payload)

    def test_distinct_execution_ids_keep_both_pairs(self):
        result = summarize(benchmark())
        self.assertEqual(result["pair_count"], 2)
        self.assertEqual(result["comparable_pair_count"], 2)
        self.assertEqual(result["with_skill"]["trial_count"], 2)

    def test_same_pair_id_across_two_distinct_arms_is_expected(self):
        payload = benchmark()
        payload["trials"] = payload["trials"][:2]
        result = summarize(payload)
        self.assertEqual(result["pair_count"], 1)
        self.assertEqual(result["comparable_pair_count"], 1)

    def test_excluded_pair_with_distinct_ids_stays_excluded_not_zero(self):
        payload = deepcopy(benchmark())
        mark_nonmeasured(payload["trials"][2], "scorer_error")
        result = summarize(payload)
        self.assertEqual(result["pair_count"], 2)
        self.assertEqual(result["comparable_pair_count"], 1)
        self.assertEqual(result["excluded_pair_count"], 1)


if __name__ == "__main__":
    unittest.main()

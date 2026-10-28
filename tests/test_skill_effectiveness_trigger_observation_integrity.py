"""RED-first: trigger telemetry must not silently drop malformed observations.

Synthetic paired Skill trials only; no real model or Amazon Ads execution.
"""
from copy import deepcopy
import math
import unittest

from scripts.summarize_skill_effectiveness import summarize


def benchmark():
    def trial(pair_id, variant, trial_id, triggered=None):
        return {
            "pair_id": pair_id,
            "trial_id": trial_id,
            "variant": variant,
            "acceptable_decision": variant == "with_skill",
            "forbidden_behavior": False,
            "required_observations_met": True,
            "triggered": triggered,
        }

    return {
        "benchmark_id": "synthetic-trigger-integrity",
        "skill": "budget-optimization",
        "fixture_id": "account-budget-cap-upstream-bottleneck",
        "fixture_version": "1",
        "mode": "Discovery",
        "harness": {
            "runtime": "synthetic-harness",
            "model": "model-x",
            "model_version": "2026-10-28",
            "measurement_contract": {
                "evaluator_id": "synthetic-evaluator",
                "evaluator_version": "1",
                "rubric_version": None,
            },
        },
        "trials": [
            trial("p1", "with_skill", "with-1", True),
            trial("p1", "without_skill", "without-1", False),
            trial("p2", "with_skill", "with-2", False),
            trial("p2", "without_skill", "without-2", True),
        ],
    }


def mark_nonmeasured(trial, status):
    trial["measurement_status"] = status
    trial["acceptable_decision"] = None
    trial["forbidden_behavior"] = None
    trial["required_observations_met"] = None


class TriggerObservationIntegrityTests(unittest.TestCase):
    def reject(self, value, *, status=None):
        payload = benchmark()
        payload["trials"][0]["triggered"] = value
        if status:
            mark_nonmeasured(payload["trials"][0], status)
        with self.assertRaisesRegex(ValueError, "triggered"):
            summarize(payload)

    def test_string_false_rejected(self):
        self.reject("false")

    def test_string_true_rejected(self):
        self.reject("true")

    def test_unknown_placeholder_rejected(self):
        self.reject("Unknown")

    def test_integer_zero_rejected(self):
        self.reject(0)

    def test_integer_one_rejected(self):
        self.reject(1)

    def test_float_zero_rejected(self):
        self.reject(0.0)

    def test_list_rejected(self):
        self.reject([])

    def test_dict_rejected(self):
        self.reject({})

    def test_nonfinite_float_rejected(self):
        self.reject(float("nan"))

    def test_invalid_scorer_error_trial_still_rejected(self):
        self.reject("false", status="scorer_error")

    def test_invalid_harness_error_trial_still_rejected(self):
        self.reject(0, status="harness_error")

    def test_invalid_insufficient_evidence_trial_still_rejected(self):
        self.reject("Partial", status="insufficient_evidence")

    def test_valid_boolean_trigger_rate_has_explicit_observed_denominator(self):
        result = summarize(benchmark())
        self.assertEqual(result["with_skill"]["trigger_rate"], 0.5)
        self.assertEqual(result["without_skill"]["trigger_rate"], 0.5)
        self.assertEqual(result["with_skill"]["trigger_observed_count"], 2)
        self.assertEqual(result["without_skill"]["trigger_observed_count"], 2)

    def test_missing_and_null_trigger_remain_unmeasured_not_zero(self):
        payload = benchmark()
        payload["trials"][0].pop("triggered")
        payload["trials"][2]["triggered"] = None
        result = summarize(payload)
        self.assertIsNone(result["with_skill"]["trigger_rate"])
        self.assertEqual(result["with_skill"]["trigger_observed_count"], 0)
        self.assertEqual(result["with_skill"]["trial_count"], 2)

    def test_partial_observation_uses_only_measured_boolean_denominator(self):
        payload = benchmark()
        payload["trials"][2]["triggered"] = None
        result = summarize(payload)
        self.assertEqual(result["with_skill"]["trigger_rate"], 1.0)
        self.assertEqual(result["with_skill"]["trigger_observed_count"], 1)
        self.assertEqual(result["with_skill"]["trial_count"], 2)

    def test_nonmeasured_pair_excluded_from_trigger_denominator(self):
        payload = deepcopy(benchmark())
        mark_nonmeasured(payload["trials"][2], "scorer_error")
        result = summarize(payload)
        self.assertEqual(result["comparable_pair_count"], 1)
        self.assertEqual(result["with_skill"]["trigger_rate"], 1.0)
        self.assertEqual(result["with_skill"]["trial_count"], 1)

    def test_complete_trigger_coverage_is_explicit(self):
        result = summarize(benchmark())
        self.assertEqual(result["with_skill"]["trigger_observation_status"], "complete")
        self.assertEqual(result["with_skill"]["trigger_observation_coverage"], 1.0)

    def test_partial_and_unmeasured_trigger_coverage_are_explicit(self):
        payload = benchmark()
        payload["trials"][2]["triggered"] = None
        result = summarize(payload)
        self.assertEqual(result["with_skill"]["trigger_observation_status"], "partial")
        self.assertEqual(result["with_skill"]["trigger_observation_coverage"], 0.5)
        payload["trials"][0].pop("triggered")
        result = summarize(payload)
        self.assertEqual(result["with_skill"]["trigger_observation_status"], "unmeasured")
        self.assertEqual(result["with_skill"]["trigger_observation_coverage"], 0.0)


if __name__ == "__main__":
    unittest.main()

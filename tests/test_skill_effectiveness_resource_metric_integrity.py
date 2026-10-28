"""Reject malformed resource measurements before paired Skill-eval summaries.

Synthetic inputs only: no model calls or live Amazon Ads account access.
"""
import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "skill_effectiveness_resource_gate",
    ROOT / "scripts" / "summarize_skill_effectiveness.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def benchmark():
    return {
        "benchmark_id": "synthetic-resource-metrics",
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
            {
                "pair_id": "p1",
                "trial_id": "run-with",
                "variant": "with_skill",
                "acceptable_decision": True,
                "forbidden_behavior": False,
                "required_observations_met": True,
                "tokens": 100,
                "latency_ms": 25.5,
            },
            {
                "pair_id": "p1",
                "trial_id": "run-without",
                "variant": "without_skill",
                "acceptable_decision": False,
                "forbidden_behavior": False,
                "required_observations_met": True,
                "tokens": 90,
                "latency_ms": 24,
            },
        ],
    }


class SkillEffectivenessResourceMetricIntegrityTests(unittest.TestCase):
    def reject(self, field, value, trial_index=0):
        payload = benchmark()
        payload["trials"][trial_index][field] = value
        with self.assertRaisesRegex(ValueError, field):
            MODULE.summarize(payload)

    def test_negative_token_count_rejected(self):
        self.reject("tokens", -1)

    def test_fractional_token_count_rejected(self):
        self.reject("tokens", 1.5)

    def test_boolean_token_count_rejected(self):
        self.reject("tokens", True)

    def test_string_token_count_rejected_not_silently_omitted(self):
        self.reject("tokens", "100")

    def test_nan_token_count_rejected(self):
        self.reject("tokens", float("nan"))

    def test_infinite_token_count_rejected(self):
        self.reject("tokens", float("inf"))

    def test_negative_latency_rejected(self):
        self.reject("latency_ms", -0.01)

    def test_boolean_latency_rejected(self):
        self.reject("latency_ms", False)

    def test_string_latency_rejected_not_silently_omitted(self):
        self.reject("latency_ms", "Unknown")

    def test_nan_latency_rejected(self):
        self.reject("latency_ms", float("nan"))

    def test_infinite_latency_rejected(self):
        self.reject("latency_ms", float("inf"))

    def test_negative_infinite_latency_rejected(self):
        self.reject("latency_ms", float("-inf"))

    def test_invalid_resource_value_on_other_arm_rejected(self):
        self.reject("tokens", -3, trial_index=1)

    def test_valid_zero_tokens_and_fractional_latency_preserved(self):
        payload = benchmark()
        payload["trials"][0]["tokens"] = 0
        payload["trials"][0]["latency_ms"] = 0.125
        result = MODULE.summarize(payload)
        self.assertEqual(result["with_skill"]["mean_tokens"], 0)
        self.assertEqual(result["with_skill"]["mean_latency_ms"], 0.125)

    def test_missing_optional_resource_metrics_remain_null_not_zero(self):
        payload = benchmark()
        for trial in payload["trials"]:
            trial.pop("tokens")
            trial.pop("latency_ms")
        result = MODULE.summarize(payload)
        self.assertIsNone(result["with_skill"]["mean_tokens"])
        self.assertIsNone(result["with_skill"]["mean_latency_ms"])

    def test_explicit_null_optional_metrics_remain_unmeasured(self):
        payload = benchmark()
        payload["trials"][0]["tokens"] = None
        payload["trials"][0]["latency_ms"] = None
        result = MODULE.summarize(payload)
        self.assertIsNone(result["with_skill"]["mean_tokens"])
        self.assertIsNone(result["with_skill"]["mean_latency_ms"])

    def test_invalid_resource_value_on_excluded_pair_still_rejected(self):
        payload = benchmark()
        trial = payload["trials"][0]
        trial["measurement_status"] = "scorer_error"
        trial["acceptable_decision"] = None
        trial["forbidden_behavior"] = None
        trial["required_observations_met"] = None
        trial["latency_ms"] = -4
        with self.assertRaisesRegex(ValueError, "latency_ms"):
            MODULE.summarize(payload)


if __name__ == "__main__":
    unittest.main()

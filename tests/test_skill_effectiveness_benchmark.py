import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/summarize_skill_effectiveness.py"


def valid_payload():
    harness = {
        "runtime": "synthetic-harness",
        "model": "model-x",
        "model_version": "2026-09-17",
        "config_hash": "cfg-1",
        "tool_profile_hash": "tools-1",
        "evidence_hash": "evidence-1",
    }
    pairs = [
        ("p1", True, False, True, False, False, False),
        ("p2", True, False, True, True, False, True),
        ("p3", True, True, True, True, False, False),
    ]
    trials = []
    for pair_id, wa, wf, wr, ba, bf, br in pairs:
        trials.append(
            {
                "pair_id": pair_id,
                "trial_id": f"{pair_id}-with",
                "variant": "with_skill",
                "acceptable_decision": wa,
                "forbidden_behavior": wf,
                "required_observations_met": wr,
                "triggered": True,
                "tokens": 1000,
                "latency_ms": 2000,
            }
        )
        trials.append(
            {
                "pair_id": pair_id,
                "trial_id": f"{pair_id}-without",
                "variant": "without_skill",
                "acceptable_decision": ba,
                "forbidden_behavior": bf,
                "required_observations_met": br,
                "triggered": None,
                "tokens": 800,
                "latency_ms": 1500,
            }
        )
    return {
        "benchmark_id": "b1",
        "skill": "budget-optimization",
        "fixture_id": "account-budget-cap-upstream-bottleneck",
        "mode": "Ablation",
        "harness": harness,
        "trials": trials,
    }


class SkillEffectivenessBenchmarkTests(unittest.TestCase):
    def invoke(self, payload):
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )

    def run_summary(self, payload):
        result = self.invoke(payload)
        self.assertEqual(
            result.returncode,
            0,
            f"summary failed: stdout={result.stdout!r} stderr={result.stderr!r}",
        )
        return json.loads(result.stdout)

    def test_paired_ablation_reports_actual_counts_rates_and_safety(self):
        summary = self.run_summary(valid_payload())

        self.assertEqual(summary["pair_count"], 3)
        self.assertEqual(summary["with_skill"]["trial_count"], 3)
        self.assertEqual(summary["without_skill"]["trial_count"], 3)
        self.assertAlmostEqual(summary["with_skill"]["full_pass_rate"], 2 / 3)
        self.assertAlmostEqual(summary["without_skill"]["full_pass_rate"], 1 / 3)
        self.assertAlmostEqual(summary["delta"]["full_pass_rate"], 1 / 3)
        self.assertAlmostEqual(summary["with_skill"]["forbidden_behavior_rate"], 1 / 3)
        self.assertTrue(summary["safety_violation_present"])
        self.assertEqual(summary["interpretation"], "measured_delta_only_no_significance_claim")

    def test_full_pass_requires_decision_safety_and_required_observations(self):
        payload = valid_payload()
        payload["trials"] = [
            {
                "pair_id": "p1",
                "trial_id": "with",
                "variant": "with_skill",
                "acceptable_decision": True,
                "forbidden_behavior": False,
                "required_observations_met": False,
            },
            {
                "pair_id": "p1",
                "trial_id": "without",
                "variant": "without_skill",
                "acceptable_decision": True,
                "forbidden_behavior": False,
                "required_observations_met": True,
            },
        ]
        summary = self.run_summary(payload)
        self.assertEqual(summary["with_skill"]["full_pass_rate"], 0.0)
        self.assertEqual(summary["without_skill"]["full_pass_rate"], 1.0)

    def test_unpaired_trial_fails_closed(self):
        payload = valid_payload()
        payload["trials"] = payload["trials"][:-1]
        result = self.invoke(payload)
        self.assertEqual(result.returncode, 2)
        self.assertIn("pair", result.stderr.lower())

    def test_duplicate_variant_in_pair_fails_closed(self):
        payload = valid_payload()
        payload["trials"][1]["variant"] = "with_skill"
        result = self.invoke(payload)
        self.assertEqual(result.returncode, 2)
        self.assertIn("pair", result.stderr.lower())


    def test_scorer_error_pair_is_excluded_not_scored_as_zero(self):
        payload = valid_payload()
        for trial in payload["trials"]:
            if trial["pair_id"] == "p3":
                trial["measurement_status"] = "scorer_error"
                trial["acceptable_decision"] = None
                trial["forbidden_behavior"] = None
                trial["required_observations_met"] = None

        summary = self.run_summary(payload)

        self.assertEqual(summary["pair_count"], 3)
        self.assertEqual(summary["comparable_pair_count"], 2)
        self.assertEqual(summary["excluded_pair_count"], 1)
        self.assertEqual(summary["measurement_status_counts"]["scorer_error"], 2)
        self.assertEqual(summary["with_skill"]["trial_count"], 2)
        self.assertEqual(summary["without_skill"]["trial_count"], 2)
        self.assertAlmostEqual(summary["with_skill"]["full_pass_rate"], 1.0)
        self.assertAlmostEqual(summary["without_skill"]["full_pass_rate"], 0.5)
        self.assertEqual(summary["effectiveness_status"], "Measured")

    def test_one_sided_harness_error_excludes_entire_pair_from_delta(self):
        payload = valid_payload()
        for trial in payload["trials"]:
            if trial["pair_id"] == "p2" and trial["variant"] == "without_skill":
                trial["measurement_status"] = "harness_error"
                trial["acceptable_decision"] = None
                trial["forbidden_behavior"] = None
                trial["required_observations_met"] = None

        summary = self.run_summary(payload)

        self.assertEqual(summary["comparable_pair_count"], 2)
        self.assertEqual(summary["excluded_pair_count"], 1)
        self.assertEqual(summary["with_skill"]["trial_count"], 2)
        self.assertEqual(summary["without_skill"]["trial_count"], 2)

    def test_no_measured_pairs_reports_insufficient_evidence_not_zero_quality(self):
        payload = valid_payload()
        for trial in payload["trials"]:
            trial["measurement_status"] = "insufficient_evidence"
            trial["acceptable_decision"] = None
            trial["forbidden_behavior"] = None
            trial["required_observations_met"] = None

        summary = self.run_summary(payload)

        self.assertEqual(summary["comparable_pair_count"], 0)
        self.assertEqual(summary["excluded_pair_count"], 3)
        self.assertEqual(summary["effectiveness_status"], "Insufficient Evidence")
        self.assertIsNone(summary["with_skill"]["full_pass_rate"])
        self.assertIsNone(summary["without_skill"]["full_pass_rate"])
        self.assertIsNone(summary["delta"]["full_pass_rate"])

    def test_schema_defines_provider_neutral_paired_contract(self):
        schema = json.loads((ROOT / "schemas/skill-effectiveness-benchmark.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        trial = schema["properties"]["trials"]["items"]
        self.assertIn("with_skill", trial["properties"]["variant"]["enum"])
        self.assertIn("without_skill", trial["properties"]["variant"]["enum"])
        self.assertIn("forbidden_behavior", trial["required"])
        self.assertIn("required_observations_met", trial["required"])
        self.assertIn("measurement_status", trial["properties"])
        self.assertIn("scorer_error", trial["properties"]["measurement_status"]["enum"])
        self.assertIn("harness_error", trial["properties"]["measurement_status"]["enum"])
        self.assertIn("null", trial["properties"]["acceptable_decision"]["type"])
        self.assertNotIn("prompt", trial["properties"])
        self.assertNotIn("transcript", trial["properties"])


if __name__ == "__main__":
    unittest.main()

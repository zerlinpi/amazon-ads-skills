import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/evaluate_skill_effectiveness_comparability.py"
SCHEMA = ROOT / "schemas/skill-effectiveness-benchmark.json"


def benchmark_payload():
    return {
        "benchmark_id": "b-provenance-1",
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
                "evaluator_id": "amazon-ads-skill-effectiveness",
                "evaluator_version": "1",
                "rubric_version": None,
            },
        },
        "trials": [
            {
                "pair_id": "p1",
                "trial_id": "p1-with",
                "variant": "with_skill",
                "acceptable_decision": True,
                "forbidden_behavior": False,
                "required_observations_met": True,
            },
            {
                "pair_id": "p1",
                "trial_id": "p1-without",
                "variant": "without_skill",
                "acceptable_decision": False,
                "forbidden_behavior": False,
                "required_observations_met": True,
            },
        ],
    }


def run_compare(baseline, candidate):
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps({"baseline": baseline, "candidate": candidate}),
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


class SkillEffectivenessComparabilityTests(unittest.TestCase):
    def test_schema_requires_versioned_fixture_and_measurement_contract(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertIn("fixture_version", schema["required"])
        harness = schema["properties"]["harness"]
        self.assertIn("measurement_contract", harness["required"])
        contract = harness["properties"]["measurement_contract"]
        for field in ("evaluator_id", "evaluator_version", "rubric_version"):
            self.assertIn(field, contract["required"])

    def test_same_measurement_identity_is_comparable(self):
        baseline = benchmark_payload()
        proc = run_compare(baseline, deepcopy(baseline))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["comparability_status"], "Comparable")
        self.assertEqual(out["mismatches"], [])
        self.assertEqual(out["unknown_fields"], [])

    def test_evaluator_version_change_is_not_comparable(self):
        baseline = benchmark_payload()
        candidate = deepcopy(baseline)
        candidate["harness"]["measurement_contract"]["evaluator_version"] = "2"
        proc = run_compare(baseline, candidate)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["comparability_status"], "Not Comparable")
        self.assertIn("harness.measurement_contract.evaluator_version", out["mismatches"])

    def test_rubric_version_change_is_not_comparable(self):
        baseline = benchmark_payload()
        baseline["harness"]["measurement_contract"]["rubric_version"] = "rubric-v1"
        candidate = deepcopy(baseline)
        candidate["harness"]["measurement_contract"]["rubric_version"] = "rubric-v2"
        proc = run_compare(baseline, candidate)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["comparability_status"], "Not Comparable")
        self.assertIn("harness.measurement_contract.rubric_version", out["mismatches"])

    def test_fixture_version_change_is_not_comparable(self):
        baseline = benchmark_payload()
        candidate = deepcopy(baseline)
        candidate["fixture_version"] = "2"
        proc = run_compare(baseline, candidate)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["comparability_status"], "Not Comparable")
        self.assertIn("fixture_version", out["mismatches"])

    def test_missing_comparability_identity_is_unknown_not_comparable(self):
        baseline = benchmark_payload()
        candidate = deepcopy(baseline)
        candidate["harness"]["config_hash"] = None
        proc = run_compare(baseline, candidate)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["comparability_status"], "Unknown")
        self.assertIn("harness.config_hash", out["unknown_fields"])

    def test_model_version_change_is_not_comparable(self):
        baseline = benchmark_payload()
        candidate = deepcopy(baseline)
        candidate["harness"]["model_version"] = "2026-09-20"
        proc = run_compare(baseline, candidate)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["comparability_status"], "Not Comparable")
        self.assertIn("harness.model_version", out["mismatches"])


if __name__ == "__main__":
    unittest.main()

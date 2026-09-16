import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_experiment_plan.py"
SCHEMA = ROOT / "schemas" / "experiment-plan.json"
SKILL = ROOT / "skills" / "experiment-planner" / "SKILL.md"


def verified_holdout_evidence() -> list[dict]:
    return [
        {
            "mechanism": "verified_hard_control",
            "verified": True,
            "evidence": "Synthetic hard exclusion/eligibility boundary verified before launch",
        }
    ]


def base_plan(*, status: str = "Ready") -> dict:
    return {
        "experiment_id": "exp-synthetic-1",
        "decision_question": "Does the treatment improve the primary outcome?",
        "hypothesis": {
            "change": "Synthetic reversible treatment",
            "mechanism": "Changes qualified delivery",
            "expected_outcome": "Improves the primary metric without breaching guardrails",
        },
        "mode": "Suggest",
        "scope": {
            "marketplace": "US",
            "profile_scope": "profile-synthetic-a",
            "ad_type": "Sponsored Products",
            "entity_type": "campaign",
            "entity_ids": ["campaign-synthetic-1"],
            "asin_ids": [],
            "exclusions": [],
        },
        "treatment": {"description": "Synthetic treatment"},
        "comparison": {
            "design_type": "holdout",
            "control_integrity": "Clean",
            "isolation_evidence": verified_holdout_evidence(),
        },
        "primary_metric": {"name": "orders", "success_rule": "Predeclared decision rule"},
        "guardrails": [],
        "windows": {
            "baseline": "matched mature baseline",
            "treatment": "declared treatment window",
            "observation": "attribution-mature observation window",
        },
        "status": status,
    }


class ExperimentPlanSemanticValidatorTests(unittest.TestCase):
    def run_validator(self, payload: dict) -> subprocess.CompletedProcess[str]:
        self.assertTrue(
            VALIDATOR.is_file(),
            "Ready experiment plans need a deterministic semantic validator before external execution review",
        )
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "-"],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_schema_exposes_profile_scope(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        scope_properties = schema["properties"]["scope"]["properties"]
        self.assertIn("profile_scope", scope_properties)

    def test_schema_exposes_holdout_isolation_evidence_without_optimization_signal_mechanism(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        comparison_properties = schema["properties"]["comparison"]["properties"]
        self.assertIn("isolation_evidence", comparison_properties)
        mechanisms = comparison_properties["isolation_evidence"]["items"]["properties"]["mechanism"]["enum"]
        self.assertIn("verified_hard_control", mechanisms)
        self.assertIn("platform_randomization", mechanisms)
        self.assertNotIn("optimization_signal", mechanisms)

    def test_ready_plan_rejects_missing_profile_scope(self):
        payload = base_plan()
        payload["scope"].pop("profile_scope")
        result = self.run_validator(payload)
        self.assertEqual(2, result.returncode)
        self.assertIn("profile_scope", result.stderr)

    def test_ready_plan_rejects_missing_entity_ids(self):
        payload = base_plan()
        payload["scope"]["entity_ids"] = []
        result = self.run_validator(payload)
        self.assertEqual(2, result.returncode)
        self.assertIn("entity_ids", result.stderr)

    def test_ready_holdout_rejects_missing_isolation_evidence(self):
        payload = base_plan()
        payload["comparison"].pop("isolation_evidence")
        result = self.run_validator(payload)
        self.assertEqual(2, result.returncode)
        self.assertIn("isolation_evidence", result.stderr)

    def test_ready_holdout_rejects_unverified_isolation_evidence(self):
        payload = base_plan()
        payload["comparison"]["isolation_evidence"][0]["verified"] = False
        result = self.run_validator(payload)
        self.assertEqual(2, result.returncode)
        self.assertIn("verified", result.stderr)

    def test_ready_holdout_rejects_optimization_signal_as_isolation_mechanism(self):
        payload = base_plan()
        payload["scope"]["audience_control_semantics"] = [
            {
                "control": "audience-signal-a",
                "semantics": "optimization_signal",
                "evidence": "Configured as model input",
                "delivery_verified": False,
            }
        ]
        payload["comparison"]["isolation_evidence"] = [
            {
                "mechanism": "optimization_signal",
                "verified": True,
                "evidence": "Audience signal configured",
            }
        ]
        result = self.run_validator(payload)
        self.assertEqual(2, result.returncode)
        self.assertIn("optimization_signal", result.stderr)

    def test_ready_holdout_rejects_non_clean_control_integrity(self):
        payload = base_plan()
        payload["comparison"]["control_integrity"] = "Unknown"
        result = self.run_validator(payload)
        self.assertEqual(2, result.returncode)
        self.assertIn("control_integrity", result.stderr)

    def test_ready_holdout_accepts_optimization_signal_when_separate_verified_boundary_exists(self):
        payload = base_plan()
        payload["scope"]["audience_control_semantics"] = [
            {
                "control": "audience-signal-a",
                "semantics": "optimization_signal",
                "evidence": "Configured as model input, not as the holdout boundary",
                "delivery_verified": False,
            }
        ]
        result = self.run_validator(payload)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_ready_plan_accepts_complete_collision_safe_scope(self):
        result = self.run_validator(base_plan())
        self.assertEqual(0, result.returncode, result.stderr)

    def test_shadow_only_plan_can_preserve_unresolved_scope(self):
        payload = base_plan(status="Shadow Only")
        payload.pop("scope")
        payload["comparison"] = {"design_type": "holdout"}
        result = self.run_validator(payload)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_skill_uses_only_machine_readable_status_names(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        allowed = schema["properties"]["status"]["enum"]
        skill = SKILL.read_text(encoding="utf-8")
        self.assertNotIn("`Directional only`", skill)
        for status in allowed:
            self.assertIn(f"`{status}`", skill)


if __name__ == "__main__":
    unittest.main()

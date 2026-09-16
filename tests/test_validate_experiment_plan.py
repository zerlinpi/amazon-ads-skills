import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_experiment_plan.py"
SCHEMA = ROOT / "schemas" / "experiment-plan.json"
SKILL = ROOT / "skills" / "experiment-planner" / "SKILL.md"


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
        "comparison": {"design_type": "holdout"},
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

    def test_ready_plan_accepts_complete_collision_safe_scope(self):
        result = self.run_validator(base_plan())
        self.assertEqual(0, result.returncode, result.stderr)

    def test_shadow_only_plan_can_preserve_unresolved_scope(self):
        payload = base_plan(status="Shadow Only")
        payload.pop("scope")
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

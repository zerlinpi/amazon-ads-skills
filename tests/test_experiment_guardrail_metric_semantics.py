import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_experiment_plan.py"
SCHEMA = ROOT / "schemas/experiment-plan.json"
SKILL = ROOT / "skills/experiment-planner/SKILL.md"

spec = importlib.util.spec_from_file_location("validate_experiment_plan", VALIDATOR)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def ready_plan(*, status: str = "Ready") -> dict:
    return {
        "experiment_id": "guardrail-metric-semantics-1",
        "decision_question": "Can the treatment improve qualified traffic without breaching the conversion guardrail?",
        "hypothesis": {
            "change": "change one bounded control",
            "mechanism": "improve qualified traffic",
            "expected_outcome": "improve CTR without breaching ROAS guardrail",
        },
        "mode": "Shadow",
        "scope": {
            "marketplace": "US",
            "profile_scope": "profile-a",
            "entity_type": "campaign",
            "entity_ids": ["campaign-1"],
        },
        "treatment": {"description": "bounded shadow treatment"},
        "comparison": {"design_type": "pre_post"},
        "primary_metric": {"name": "CTR", "success_rule": "increase"},
        "guardrails": [
            {
                "metric": "ROAS",
                "rule": "must remain above the declared business floor",
            }
        ],
        "windows": {
            "baseline": "previous",
            "treatment": "current",
            "observation": "attribution-mature",
        },
        "status": status,
    }


class ExperimentGuardrailMetricSemanticsTests(unittest.TestCase):
    def test_schema_exposes_guardrail_metric_semantics_envelope(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        guardrail_props = schema["properties"]["guardrails"]["items"]["properties"]
        self.assertIn("metric_semantics", guardrail_props)
        semantic_props = guardrail_props["metric_semantics"]["properties"]
        for field in ("metric_family", "attribution_family", "semantic_version", "aggregation_semantics"):
            self.assertIn(field, semantic_props)

    def test_ready_conversion_guardrail_requires_explicit_metric_semantics(self):
        plan = ready_plan()

        errors = module.validate_experiment_plan(plan)

        self.assertTrue(
            any("guardrail" in error.lower() and "metric semantics" in error.lower() for error in errors),
            errors,
        )

    def test_ready_conversion_guardrail_accepts_explicit_metric_semantics(self):
        plan = ready_plan()
        plan["guardrails"][0]["metric_semantics"] = {
            "metric_family": "conversion",
            "attribution_family": "standard",
            "semantic_version": "amazon-store-attribution-2026-01-01",
        }

        self.assertEqual(module.validate_experiment_plan(plan), [])

    def test_ready_combined_readout_requires_guardrail_aggregation_semantics(self):
        plan = ready_plan()
        plan["comparison"]["requires_combined_readout"] = True
        plan["guardrails"][0]["metric_semantics"] = {
            "metric_family": "conversion",
            "attribution_family": "standard",
            "semantic_version": "amazon-store-attribution-2026-01-01",
        }

        errors = module.validate_experiment_plan(plan)

        self.assertTrue(
            any("guardrail" in error.lower() and "aggregation_semantics" in error for error in errors),
            errors,
        )

    def test_ready_combined_readout_accepts_guardrail_aggregation_semantics(self):
        plan = ready_plan()
        plan["comparison"]["requires_combined_readout"] = True
        plan["guardrails"][0]["metric_semantics"] = {
            "metric_family": "conversion",
            "attribution_family": "standard",
            "semantic_version": "amazon-store-attribution-2026-01-01",
            "aggregation_semantics": "ratio_or_derived",
        }
        plan["primary_metric"]["metric_semantics"] = {
            "metric_family": "traffic",
            "attribution_family": "not_applicable",
            "semantic_version": "traffic-v1",
            "aggregation_semantics": "ratio_or_derived",
        }

        self.assertEqual(module.validate_experiment_plan(plan), [])

    def test_non_ready_guardrail_may_preserve_unresolved_semantics(self):
        plan = ready_plan(status="Shadow Only")
        self.assertEqual(module.validate_experiment_plan(plan), [])

    def test_skill_routes_ready_conversion_guardrails_through_metric_semantics(self):
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("metric_semantics", text)
        self.assertIn("guardrail", text)


if __name__ == "__main__":
    unittest.main()

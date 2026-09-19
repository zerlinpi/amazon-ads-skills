import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_experiment_plan.py"

spec = importlib.util.spec_from_file_location("validate_experiment_plan", VALIDATOR)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def ready_plan(primary_metric):
    return {
        "experiment_id": "metric-semantics-1",
        "decision_question": "Did the treatment improve conversion performance?",
        "hypothesis": {
            "change": "change one bounded control",
            "mechanism": "improve eligible traffic efficiency",
            "expected_outcome": "improve the primary conversion metric",
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
        "primary_metric": primary_metric,
        "guardrails": [],
        "windows": {"baseline": "previous", "treatment": "current", "observation": "mature"},
        "status": "Ready",
    }


class ExperimentMetricSemanticsTests(unittest.TestCase):
    def test_ready_conversion_metric_requires_explicit_attribution_family(self):
        plan = ready_plan({"name": "Purchases", "success_rule": "increase"})
        errors = module.validate_experiment_plan(plan)
        self.assertTrue(any("metric semantics" in error.lower() for error in errors), errors)

    def test_ready_conversion_metric_accepts_bounded_standard_attribution_semantics(self):
        plan = ready_plan({
            "name": "Purchases",
            "success_rule": "increase",
            "metric_semantics": {
                "metric_family": "conversion",
                "attribution_family": "standard",
                "semantic_version": "amazon-store-attribution-2026-01-01",
            },
        })
        self.assertEqual(module.validate_experiment_plan(plan), [])

    def test_ready_all_views_metric_accepts_distinct_all_views_family(self):
        plan = ready_plan({
            "name": "Purchases (all views)",
            "success_rule": "increase",
            "metric_semantics": {
                "metric_family": "conversion",
                "attribution_family": "all_views",
                "semantic_version": "amazon-store-attribution-2026-01-01",
            },
        })
        self.assertEqual(module.validate_experiment_plan(plan), [])

    def test_ready_declared_conversion_family_cannot_bypass_gate_via_display_name(self):
        plan = ready_plan({
            "name": "Attributed orders",
            "success_rule": "increase",
            "metric_semantics": {
                "metric_family": "conversion",
                "attribution_family": None,
                "semantic_version": None,
            },
        })
        errors = module.validate_experiment_plan(plan)
        self.assertTrue(
            any("attribution_family" in error or "semantic_version" in error for error in errors),
            errors,
        )

    def test_ready_combined_readout_requires_primary_aggregation_semantics(self):
        plan = ready_plan({
            "name": "Reach",
            "success_rule": "increase",
            "metric_semantics": {
                "metric_family": "reach",
                "attribution_family": "not_applicable",
                "semantic_version": "reach-v1",
            },
        })
        plan["comparison"]["requires_combined_readout"] = True

        errors = module.validate_experiment_plan(plan)

        self.assertTrue(
            any("aggregation_semantics" in error for error in errors),
            errors,
        )

    def test_ready_non_combined_readout_does_not_invent_aggregation_requirement(self):
        plan = ready_plan({
            "name": "Reach",
            "success_rule": "increase",
            "metric_semantics": {
                "metric_family": "reach",
                "attribution_family": "not_applicable",
                "semantic_version": "reach-v1",
            },
        })

        self.assertEqual(module.validate_experiment_plan(plan), [])

    def test_non_ready_plan_may_leave_metric_semantics_unresolved(self):
        plan = ready_plan({"name": "Purchases", "success_rule": "increase"})
        plan["status"] = "Shadow Only"
        self.assertEqual(module.validate_experiment_plan(plan), [])


if __name__ == "__main__":
    unittest.main()

"""RED-first: combined Ready readouts cannot declare known ratio KPIs additive.

All inputs are synthetic; no account reads or Amazon Ads writes.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def combined_metric(name, *, aggregation="additive", guardrail=False, status="Ready"):
    plan = base_plan(status=status)
    plan["comparison"]["requires_combined_readout"] = True
    conversion = name.upper() in {"ROAS", "ACOS", "CVR", "SALES"}
    semantics = {
        "metric_family": "conversion" if conversion else "traffic",
        "attribution_family": "standard" if conversion else "not_applicable",
        "semantic_version": "synthetic-report-v1",
        "aggregation_semantics": aggregation,
    }
    item = {
        "metric" if guardrail else "name": name,
        "rule" if guardrail else "success_rule": "synthetic predeclared rule",
        "metric_semantics": semantics,
    }
    if guardrail:
        plan["primary_metric"] = {
            "name": "Impressions", "success_rule": "increase",
            "metric_semantics": {
                "metric_family": "traffic", "attribution_family": "not_applicable",
                "semantic_version": "synthetic-report-v1",
                "aggregation_semantics": "additive",
            },
        }
        plan["guardrails"] = [item]
    else:
        plan["primary_metric"] = item
    return plan


class ReadyCombinedRatioAggregationTests(unittest.TestCase):
    def assert_ratio_rejected(self, name, *, aggregation="additive", guardrail=False):
        errors = validate_experiment_plan(combined_metric(
            name, aggregation=aggregation, guardrail=guardrail
        ))
        self.assertTrue(any("aggregation_semantics" in error for error in errors), errors)

    def test_roas_primary_cannot_claim_additive(self):
        self.assert_ratio_rejected("ROAS")

    def test_acos_primary_cannot_claim_additive(self):
        self.assert_ratio_rejected("ACOS")

    def test_cvr_primary_cannot_claim_additive(self):
        self.assert_ratio_rejected("CVR")

    def test_ctr_primary_cannot_claim_additive(self):
        self.assert_ratio_rejected("CTR")

    def test_cpc_primary_cannot_claim_additive(self):
        self.assert_ratio_rejected("CPC")

    def test_tacos_primary_cannot_claim_additive(self):
        self.assert_ratio_rejected("TACOS")

    def test_roas_guardrail_cannot_claim_additive(self):
        self.assert_ratio_rejected("ROAS", guardrail=True)

    def test_ctr_guardrail_cannot_claim_nonadditive_deduplicated(self):
        self.assert_ratio_rejected(
            "CTR", aggregation="non_additive_deduplicated", guardrail=True
        )

    def test_roas_ratio_semantics_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(
            combined_metric("ROAS", aggregation="ratio_or_derived")
        ))

    def test_ctr_ratio_semantics_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(
            combined_metric("CTR", aggregation="ratio_or_derived")
        ))

    def test_impressions_additive_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(combined_metric("Impressions")))

    def test_sales_additive_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(combined_metric("Sales")))

    def test_shadow_only_can_preserve_ratio_misclassification(self):
        self.assertEqual([], validate_experiment_plan(
            combined_metric("ROAS", status="Shadow Only")
        ))

    def test_non_combined_ready_keeps_legacy_aggregation_contract(self):
        plan = combined_metric("ROAS")
        plan["comparison"]["requires_combined_readout"] = False
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

"""RED-first: non-ad retail and rank metric labels are not ad-attributed conversions.

All inputs are synthetic. No Amazon Ads access or account mutation.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def retail_metric(name, *, family="retail", guardrail=False, status="Ready"):
    plan = base_plan(status=status)
    item = {
        "metric" if guardrail else "name": name,
        "rule" if guardrail else "success_rule": "synthetic predeclared decision rule",
        "metric_semantics": {
            "metric_family": family,
            "attribution_family": "not_applicable",
            "semantic_version": "synthetic-retail-v1",
        },
    }
    if guardrail:
        plan["guardrails"] = [item]
    else:
        plan["primary_metric"] = item
    return plan


class RetailMetricNameBoundaryTests(unittest.TestCase):
    def assert_ready(self, name, **kwargs):
        errors = validate_experiment_plan(retail_metric(name, **kwargs))
        self.assertEqual([], errors)

    def assert_conversion_gate(self, name, **kwargs):
        errors = validate_experiment_plan(retail_metric(name, **kwargs))
        self.assertTrue(any("metric_family" in e for e in errors), errors)

    def test_total_retail_sales_is_not_ad_attributed_sales(self):
        self.assert_ready("Total Retail Sales")

    def test_retail_sales_is_not_ad_attributed_sales(self):
        self.assert_ready("Retail Sales")

    def test_organic_sales_is_not_ad_attributed_sales(self):
        self.assert_ready("Organic Sales")

    def test_sales_rank_is_not_a_conversion_count(self):
        self.assert_ready("Sales Rank")

    def test_wholesale_traffic_does_not_match_sales_substring(self):
        self.assert_ready("Wholesale Traffic", family="traffic")

    def test_organic_sales_guardrail_is_not_ad_attributed(self):
        self.assert_ready("Organic Sales", guardrail=True)

    def test_bare_sales_remains_ambiguous_and_requires_conversion_identity(self):
        self.assert_conversion_gate("Sales")

    def test_total_sales_remains_ambiguous_and_requires_conversion_identity(self):
        self.assert_conversion_gate("Total Sales")

    def test_attributed_sales_cannot_hide_under_retail_family(self):
        self.assert_conversion_gate("Ad-Attributed Sales")

    def test_attributed_retail_sales_cannot_use_retail_exemption(self):
        self.assert_conversion_gate("Attributed Retail Sales")

    def test_attributed_sales_guardrail_cannot_hide_under_retail_family(self):
        self.assert_conversion_gate("Ad-Attributed Sales", guardrail=True)

    def test_explicit_conversion_family_still_requires_conversion_provenance(self):
        errors = validate_experiment_plan(retail_metric("Retail Sales", family="conversion"))
        self.assertTrue(any("attribution_family" in e for e in errors), errors)

    def test_purchases_still_requires_conversion_identity(self):
        self.assert_conversion_gate("Purchases", family="traffic")

    def test_shadow_only_can_keep_unresolved_retail_label(self):
        self.assert_ready("Retail Sales", status="Shadow Only")


if __name__ == "__main__":
    unittest.main()

"""RED-first: official Amazon benchmark derived rates must never be direct-sum additive.

Synthetic metadata only; no account access, credentials, external writes or raw source claims.
Official benchmark metric definitions (2026-10-06):
https://advertising.amazon.com/help/GXRC3X4EEPXH8NVE
"""
import unittest

from scripts.evaluate_metric_aggregation_gate import evaluate_metric_aggregation_gate
from scripts.validate_experiment_plan import validate_experiment_plan
from test_experiment_combined_ratio_aggregation import combined_metric


def standalone(name, aggregation="additive"):
    return evaluate_metric_aggregation_gate({
        "metric_name": name,
        "metric_semantics": {"aggregation_semantics": aggregation},
        "source_relation": "disjoint",
    })


def ready(name, aggregation="additive", *, guardrail=False, status="Ready"):
    plan = combined_metric(name, aggregation=aggregation, guardrail=guardrail, status=status)
    # The shared fixture defaults to traffic for new labels. Purchase-rate
    # metrics are conversion-derived and need resolved attribution identity.
    metric = plan["guardrails"][0] if guardrail else plan["primary_metric"]
    if "purchase" in name.lower():
        metric["metric_semantics"].update({
            "metric_family": "conversion",
            "attribution_family": "standard",
            "semantic_version": "synthetic-report-v1",
        })
    return plan


class OfficialDerivedRateAggregationTests(unittest.TestCase):
    def assert_blocked(self, name):
        result = standalone(name)
        self.assertEqual("Blocked", result["aggregation_status"], (name, result))
        self.assertFalse(result["direct_sum_allowed"], (name, result))

    def assert_ready_rejected(self, name, *, guardrail=False):
        errors = validate_experiment_plan(ready(name, guardrail=guardrail))
        self.assertTrue(
            any("aggregation_semantics" in error for error in errors),
            (name, errors),
        )

    def test_purchase_rate_standalone(self):
        self.assert_blocked("Purchase rate")

    def test_purchase_rate_variant_standalone(self):
        self.assert_blocked("Purchase rate (combined)")

    def test_add_to_cart_rate_standalone(self):
        self.assert_blocked("Add to cart rate (new to brand, promoted)")

    def test_detail_page_view_rate_standalone(self):
        self.assert_blocked("Detail page view rate")

    def test_branded_search_rate_standalone(self):
        self.assert_blocked("Branded search rate")

    def test_cost_per_purchase_standalone(self):
        self.assert_blocked("Cost per purchase")

    def test_cost_per_detail_page_view_standalone(self):
        self.assert_blocked("Cost per detail page view (promoted)")

    def test_percent_new_to_brand_standalone(self):
        self.assert_blocked("Percent of purchases new to brand")

    def test_purchase_rate_ready_primary(self):
        self.assert_ready_rejected("Purchase rate")

    def test_add_to_cart_rate_ready_primary(self):
        self.assert_ready_rejected("Add to cart rate")

    def test_detail_page_view_rate_ready_primary(self):
        self.assert_ready_rejected("Detail page view rate (promoted)")

    def test_cost_per_purchase_ready_primary(self):
        self.assert_ready_rejected("Cost per purchase")

    def test_purchase_rate_ready_guardrail(self):
        self.assert_ready_rejected("Purchase rate (new to brand)", guardrail=True)

    def test_cost_per_detail_page_view_ready_guardrail(self):
        self.assert_ready_rejected("Cost per detail page view", guardrail=True)

    def test_ratio_semantics_standalone_remains_blocked_from_direct_sum(self):
        result = standalone("Purchase rate", aggregation="ratio_or_derived")
        self.assertEqual("Blocked", result["aggregation_status"])
        self.assertFalse(result["direct_sum_allowed"])

    def test_valid_ratio_ready_remains_compatible(self):
        self.assertEqual([], validate_experiment_plan(
            ready("Purchase rate", aggregation="ratio_or_derived")
        ))

    def test_additive_count_remains_allowed(self):
        self.assertTrue(standalone("Purchases")["direct_sum_allowed"])

    def test_additive_impressions_remains_allowed(self):
        self.assertTrue(standalone("Impressions")["direct_sum_allowed"])

    def test_unrelated_rate_word_in_long_label_is_not_suffix(self):
        self.assertTrue(standalone("Rate limit adjustment count")["direct_sum_allowed"])

    def test_shadow_only_keeps_unresolved_metadata(self):
        self.assertEqual([], validate_experiment_plan(
            ready("Purchase rate", status="Shadow Only")
        ))

    def test_noncombined_ready_keeps_legacy_contract(self):
        plan = ready("Add to cart rate")
        plan["comparison"]["requires_combined_readout"] = False
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

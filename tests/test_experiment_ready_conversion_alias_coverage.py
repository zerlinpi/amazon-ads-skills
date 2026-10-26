"""RED-first: named ad conversion metrics cannot hide behind a traffic family.

All examples are synthetic. No account reads or live Amazon Ads writes.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def ready_metric(name, *, guardrail=False, family="traffic", with_semantics=True):
    plan = base_plan()
    item = {
        "metric" if guardrail else "name": name,
        "rule" if guardrail else "success_rule": "increase",
    }
    if with_semantics:
        item["metric_semantics"] = {
            "metric_family": family,
            "attribution_family": "standard",
            "semantic_version": "ads-reporting-v1",
        }
    if guardrail:
        plan["guardrails"] = [item]
    else:
        plan["primary_metric"] = item
    return plan


class ReadyConversionAliasCoverageTests(unittest.TestCase):
    def assert_family_rejected(self, name, *, guardrail=False):
        errors = validate_experiment_plan(ready_metric(name, guardrail=guardrail))
        self.assertTrue(any("metric_family" in e for e in errors), errors)

    def test_primary_acos_is_conversion_derived(self):
        self.assert_family_rejected("ACOS")

    def test_primary_acos_unknown_family_cannot_bypass(self):
        plan = ready_metric("ACOS", family="Unknown")
        self.assertTrue(any("metric_family" in e for e in validate_experiment_plan(plan)))

    def test_primary_acos_requires_metric_semantics(self):
        plan = ready_metric("ACOS", with_semantics=False)
        self.assertTrue(any("metric semantics" in e for e in validate_experiment_plan(plan)))

    def test_guardrail_acos_is_conversion_derived(self):
        self.assert_family_rejected("ACOS", guardrail=True)

    def test_primary_attributed_orders_is_conversion(self):
        self.assert_family_rejected("Attributed Orders")

    def test_guardrail_attributed_orders_is_conversion(self):
        self.assert_family_rejected("Ad-attributed Orders", guardrail=True)

    def test_primary_units_sold_is_conversion(self):
        self.assert_family_rejected("Units Sold")

    def test_primary_attributed_units_is_conversion(self):
        self.assert_family_rejected("Attributed Units")

    def test_primary_cvr_is_conversion_derived(self):
        self.assert_family_rejected("CVR")

    def test_guardrail_cvr_is_conversion_derived(self):
        self.assert_family_rejected("CVR", guardrail=True)

    def test_valid_acos_identity_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(ready_metric("ACOS", family="conversion")))

    def test_valid_attributed_orders_identity_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(
            ready_metric("Attributed Orders", family="conversion")
        ))

    def test_tacos_not_mistaken_for_acos(self):
        # Total ACOS can use total retail sales, not necessarily attributed sales.
        self.assertEqual([], validate_experiment_plan(ready_metric("TACOS")))

    def test_clicks_remain_nonconversion(self):
        self.assertEqual([], validate_experiment_plan(ready_metric("Clicks")))

    def test_shadow_keeps_unresolved_acos(self):
        plan = ready_metric("ACOS", family="Unknown")
        plan["status"] = "Shadow Only"
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

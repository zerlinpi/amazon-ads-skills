"""RED-first: an observed SP retailer scope must not contradict Amazon Business controls.

Repository-normalized read-side labels, not native Amazon API enums. Synthetic
fixtures only; no live Amazon Ads calls or account writes.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot


STANDARD = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def compare_retailer(before_retailer=None, after_retailer=None, *,
                     business_before=None, business_after=None,
                     site_before="ALL_ELIGIBLE", site_after="ALL_ELIGIBLE",
                     omit_before=False, omit_after=False,
                     budget_treatment=False):
    baseline = snapshot(1.0, dict(STANDARD))
    post = snapshot(1.2, dict(STANDARD))
    for record, retailer, business, site, omit in (
        (baseline, before_retailer, business_before, site_before, omit_before),
        (post, after_retailer, business_after, site_after, omit_after),
    ):
        placement = next(c for c in record["controls"] if c["control_type"] == "placement_adjustment")["state"]
        if business is not None:
            placement["amazon_business"] = business
        routing = next(c for c in record["controls"] if c["control_type"] == "targeting_or_routing")["state"]
        routing["site_restriction"] = site
        if not omit:
            routing["retailer_scope"] = retailer
    treatment = "base_bid"
    if budget_treatment:
        for record, amount in ((baseline, 100), (post, 120)):
            record["coverage"]["requirement_provenance"]["decision_surface"] = "sponsored_products_budget_change"
            next(c for c in record["controls"] if c["control_type"] == "base_bid")["state"] = 1.0
            budget = next(c for c in record["controls"] if c["control_type"] == "budget_or_pacing")["state"]
            budget["base_average_daily_budget"] = amount
            budget["effective_daily_budget"] = amount
        treatment = "budget_or_pacing"
    return compare_control_state(baseline, post, treatment)


class RetailerScopeEvidenceTests(unittest.TestCase):
    def assert_unknown(self, *args, **kwargs):
        result = compare_retailer(*args, **kwargs)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(any("retailer_scope" in reason for reason in result["reasons"]), result)

    def test_across_retailers_cannot_claim_observed_business_zero(self):
        self.assert_unknown("ACROSS_RETAILERS", "ACROSS_RETAILERS", business_before=0, business_after=0)

    def test_across_retailers_cannot_claim_business_modifier(self):
        self.assert_unknown("ACROSS_RETAILERS", "ACROSS_RETAILERS", business_before=25, business_after=25)

    def test_across_retailers_cannot_claim_business_exclusive_site(self):
        self.assert_unknown("ACROSS_RETAILERS", "ACROSS_RETAILERS",
                            site_before="AMAZON_BUSINESS", site_after="AMAZON_BUSINESS")

    def test_across_retailers_conflict_during_budget_treatment(self):
        self.assert_unknown("ACROSS_RETAILERS", "ACROSS_RETAILERS",
                            business_before=0, business_after=0, budget_treatment=True)

    def test_across_retailers_business_exclusive_during_budget_treatment(self):
        self.assert_unknown("ACROSS_RETAILERS", "ACROSS_RETAILERS",
                            site_before="AMAZON_BUSINESS", site_after="AMAZON_BUSINESS",
                            budget_treatment=True)

    def test_unmapped_retailer_scope_is_not_stable(self):
        self.assert_unknown("SOME_NEW_RETAILER_SCOPE", "SOME_NEW_RETAILER_SCOPE")

    def test_mixed_scope_requires_explicit_mapping(self):
        self.assert_unknown("MIXED", "MIXED")

    def test_boolean_false_is_not_retailer_scope(self):
        self.assert_unknown(False, False)

    def test_boolean_true_is_not_retailer_scope(self):
        self.assert_unknown(True, True)

    def test_numeric_zero_is_not_retailer_scope(self):
        self.assert_unknown(0, 0)

    def test_dict_is_not_retailer_scope(self):
        self.assert_unknown({"retailer": "AMAZON_STORE"}, {"retailer": "AMAZON_STORE"})

    def test_whitespace_padded_scope_is_not_normalized_implicitly(self):
        self.assert_unknown(" AMAZON_STORE ", " AMAZON_STORE ")

    def test_one_sided_missing_baseline_is_unknown(self):
        self.assert_unknown("AMAZON_STORE", "AMAZON_STORE", omit_before=True)

    def test_one_sided_missing_post_is_unknown(self):
        self.assert_unknown("AMAZON_STORE", "AMAZON_STORE", omit_after=True)

    def test_one_sided_missing_during_budget_treatment_is_unknown(self):
        self.assert_unknown("AMAZON_STORE", "AMAZON_STORE",
                            omit_before=True, budget_treatment=True)

    def test_amazon_store_with_explicit_business_zero_remains_valid(self):
        result = compare_retailer("AMAZON_STORE", "AMAZON_STORE", business_before=0, business_after=0)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_amazon_store_with_business_modifier_remains_valid(self):
        result = compare_retailer("AMAZON_STORE", "AMAZON_STORE", business_before=25, business_after=25)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_business_exclusive_amazon_store_remains_valid(self):
        result = compare_retailer("AMAZON_STORE", "AMAZON_STORE",
                                  site_before="AMAZON_BUSINESS", site_after="AMAZON_BUSINESS")
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_across_retailers_without_business_controls_is_supported(self):
        result = compare_retailer("ACROSS_RETAILERS", "ACROSS_RETAILERS")
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_real_retailer_scope_change_is_confounded(self):
        result = compare_retailer("AMAZON_STORE", "ACROSS_RETAILERS")
        self.assertEqual(result["classification"], "Confounded", result)
        self.assertIn("targeting_or_routing", result.get("changed_controls", []))

    def test_both_absent_legacy_evidence_stays_compatible(self):
        result = compare_retailer(omit_before=True, omit_after=True)
        self.assertEqual(result["classification"], "Treatment Isolated", result)


if __name__ == "__main__":
    unittest.main()

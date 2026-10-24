"""RED-first: Sponsored Products site routing must be observed, not a repeated placeholder.

These synthetic snapshots use repository-normalized read-side routing labels,
not an Amazon Ads native API request schema. No account writes or retries.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot


PLACEMENTS = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def compare_routes(before_state, after_state=None, *, budget_treatment=False):
    if after_state is None:
        after_state = before_state
    baseline = snapshot(1.0, dict(PLACEMENTS))
    post = snapshot(1.2, dict(PLACEMENTS))
    for record, route in ((baseline, before_state), (post, after_state)):
        next(c for c in record["controls"] if c["control_type"] == "targeting_or_routing")["state"] = route
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


class SponsoredProductsSiteRoutingEvidenceTests(unittest.TestCase):
    def assert_unknown(self, state, *, budget_treatment=False):
        result = compare_routes(state, budget_treatment=budget_treatment)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_missing_site_restriction_is_not_all_eligible(self):
        self.assert_unknown({})

    def test_repeated_unknown_is_not_stable_routing(self):
        self.assert_unknown({"site_restriction": "Unknown"})

    def test_repeated_unsupported_is_not_no_restriction(self):
        self.assert_unknown({"site_restriction": "Unsupported"})

    def test_repeated_partial_is_not_complete_routing(self):
        self.assert_unknown({"site_restriction": "Partial"})

    def test_repeated_missing_label_is_not_complete_routing(self):
        self.assert_unknown({"site_restriction": "Missing"})

    def test_unavailable_is_not_complete_routing(self):
        self.assert_unknown({"site_restriction": "Unavailable"})

    def test_explicit_null_is_not_a_routing_state(self):
        self.assert_unknown({"site_restriction": None})

    def test_boolean_false_is_not_all_eligible(self):
        self.assert_unknown({"site_restriction": False})

    def test_boolean_true_is_not_business_only(self):
        self.assert_unknown({"site_restriction": True})

    def test_numeric_zero_is_not_all_eligible(self):
        self.assert_unknown({"site_restriction": 0})

    def test_blank_site_restriction_is_not_a_routing_state(self):
        self.assert_unknown({"site_restriction": "  "})

    def test_unmapped_label_is_not_silently_accepted(self):
        self.assert_unknown({"site_restriction": "SOME_NEW_SITE"})

    def test_whitespace_padded_label_is_not_normalized_implicitly(self):
        self.assert_unknown({"site_restriction": " AMAZON_BUSINESS "})

    def test_unstructured_state_is_not_accepted(self):
        self.assert_unknown("ALL_ELIGIBLE")

    def test_missing_site_restriction_during_budget_treatment(self):
        self.assert_unknown({}, budget_treatment=True)

    def test_unknown_site_restriction_during_budget_treatment(self):
        self.assert_unknown({"site_restriction": "Unknown"}, budget_treatment=True)

    def test_explicit_all_eligible_remains_compatible(self):
        result = compare_routes({"site_restriction": "ALL_ELIGIBLE"})
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_explicit_business_only_is_distinct_valid_normalized_routing(self):
        result = compare_routes({"site_restriction": "AMAZON_BUSINESS"})
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_site_routing_change_confounds_base_bid_treatment(self):
        result = compare_routes(
            {"site_restriction": "ALL_ELIGIBLE"},
            {"site_restriction": "AMAZON_BUSINESS"},
        )
        self.assertEqual(result["classification"], "Confounded", result)
        self.assertIn("targeting_or_routing", result.get("changed_controls", []))

    def test_site_routing_change_confounds_budget_treatment(self):
        result = compare_routes(
            {"site_restriction": "ALL_ELIGIBLE"},
            {"site_restriction": "AMAZON_BUSINESS"},
            budget_treatment=True,
        )
        self.assertEqual(result["classification"], "Confounded", result)

    def test_one_sided_missing_routing_is_unknown(self):
        result = compare_routes({"site_restriction": "ALL_ELIGIBLE"}, {})
        self.assertEqual(result["classification"], "Unknown", result)

    def test_routing_proof_does_not_override_nested_collection_coverage(self):
        result = compare_routes({"site_restriction": "ALL_ELIGIBLE", "routing_rules": []})
        self.assertEqual(result["classification"], "Unknown", result)


if __name__ == "__main__":
    unittest.main()

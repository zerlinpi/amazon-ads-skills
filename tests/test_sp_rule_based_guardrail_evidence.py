"""RED-first: a rule-based bidding label without ROAS guardrail is incomplete.

Synthetic read-only control snapshots; this is a repository-owned normalized
evidence contract, not an Amazon-native bidding API schema.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot


PLACEMENTS = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def compare_rule(before, after=None, *, budget_treatment=False):
    if after is None:
        after = before
    baseline = snapshot(1.0, dict(PLACEMENTS), bidding_strategy=before)
    post = snapshot(1.2, dict(PLACEMENTS), bidding_strategy=after)
    if budget_treatment:
        for record, amount in ((baseline, 100), (post, 120)):
            record["coverage"]["requirement_provenance"]["decision_surface"] = "sponsored_products_budget_change"
            next(c for c in record["controls"] if c["control_type"] == "base_bid")["state"] = 1.0
            state = next(c for c in record["controls"] if c["control_type"] == "budget_or_pacing")["state"]
            state["base_average_daily_budget"] = amount
            state["effective_daily_budget"] = amount
        treatment = "budget_or_pacing"
    else:
        treatment = "base_bid"
    return compare_control_state(baseline, post, treatment)


def rule(guardrail, strategy="rule_based", **extra):
    return {"strategy": strategy, "roas_guardrail": guardrail, **extra}


class SponsoredProductsRuleBasedGuardrailTests(unittest.TestCase):
    def assert_unknown(self, value, *, budget_treatment=False):
        result = compare_rule(value, budget_treatment=budget_treatment)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_legacy_bare_rule_based_is_not_complete_evidence(self):
        self.assert_unknown("rule_based")

    def test_legacy_hyphen_rule_based_is_not_complete_evidence(self):
        self.assert_unknown("rule-based")

    def test_legacy_bare_rule_based_during_budget_treatment(self):
        self.assert_unknown("rule_based", budget_treatment=True)

    def test_complete_rule_based_numeric_guardrail_is_usable(self):
        self.assertEqual(compare_rule(rule(3.0))["classification"], "Treatment Isolated")

    def test_complete_rule_based_decimal_string_guardrail_is_usable(self):
        self.assertEqual(compare_rule(rule("3.25"))["classification"], "Treatment Isolated")

    def test_complete_hyphen_rule_based_guardrail_is_usable(self):
        self.assertEqual(compare_rule(rule(3, strategy="rule-based"))["classification"], "Treatment Isolated")

    def test_complete_rule_based_during_budget_treatment(self):
        self.assertEqual(compare_rule(rule(3), budget_treatment=True)["classification"], "Treatment Isolated")

    def test_rule_guardrail_change_is_confounded(self):
        self.assertEqual(compare_rule(rule(3), rule(4))["classification"], "Confounded")

    def test_rule_guardrail_change_confounds_budget_treatment(self):
        self.assertEqual(compare_rule(rule(3), rule(4), budget_treatment=True)["classification"], "Confounded")

    def test_missing_guardrail_fails_closed(self):
        self.assert_unknown({"strategy": "rule_based"})

    def test_unknown_guardrail_fails_closed(self):
        self.assert_unknown(rule("Unknown"))

    def test_unsupported_guardrail_fails_closed(self):
        self.assert_unknown(rule("Unsupported"))

    def test_zero_guardrail_fails_closed(self):
        self.assert_unknown(rule(0))

    def test_negative_guardrail_fails_closed(self):
        self.assert_unknown(rule(-1))

    def test_boolean_guardrail_fails_closed(self):
        self.assert_unknown(rule(True))

    def test_nonfinite_guardrail_fails_closed(self):
        self.assert_unknown(rule(float("inf")))

    def test_percent_formatted_guardrail_fails_closed(self):
        self.assert_unknown(rule("300%"))

    def test_structured_guardrail_fails_closed(self):
        self.assert_unknown(rule({"status": "Observed", "value": 3}))

    def test_extra_unverified_rule_fields_fail_closed(self):
        self.assert_unknown(rule(3, status="Unknown"))

    def test_non_rule_strategy_remains_supported(self):
        self.assertEqual(compare_rule("fixed")["classification"], "Treatment Isolated")

    def test_non_rule_object_does_not_bypass_normalized_contract(self):
        self.assert_unknown(rule(3, strategy="fixed"))


if __name__ == "__main__":
    unittest.main()

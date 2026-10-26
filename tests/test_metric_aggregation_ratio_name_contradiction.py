"""RED-first: standalone direct-sum gate must not trust additive ratio KPI labels.

Synthetic metadata only; no Amazon Ads calls, account data, or writes.
"""
import unittest

from scripts.evaluate_metric_aggregation_gate import evaluate_metric_aggregation_gate


def evaluate(name=None, semantics="additive", relation="disjoint"):
    payload = {
        "metric_semantics": {"aggregation_semantics": semantics},
        "source_relation": relation,
    }
    if name is not None:
        payload["metric_name"] = name
    return evaluate_metric_aggregation_gate(payload)


class AggregationRatioNameContradictionTests(unittest.TestCase):
    def assert_blocked(self, name):
        result = evaluate(name)
        self.assertEqual("Blocked", result["aggregation_status"], result)
        self.assertFalse(result["direct_sum_allowed"], result)
        self.assertIn("ratio", result["reason"].lower())

    def test_roas_additive_claim_cannot_authorize_sum(self):
        self.assert_blocked("ROAS")

    def test_acos_additive_claim_cannot_authorize_sum(self):
        self.assert_blocked("ACOS")

    def test_tacos_additive_claim_cannot_authorize_sum(self):
        self.assert_blocked("TACOS")

    def test_ctr_additive_claim_cannot_authorize_sum(self):
        self.assert_blocked("CTR")

    def test_cvr_additive_claim_cannot_authorize_sum(self):
        self.assert_blocked("CVR")

    def test_cpc_additive_claim_cannot_authorize_sum(self):
        self.assert_blocked("CPC")

    def test_bounded_ratio_name_with_label_suffix_is_blocked(self):
        self.assert_blocked("Campaign ROAS (7d)")

    def test_case_insensitive_ratio_label_is_blocked(self):
        self.assert_blocked("acOs")

    def test_non_ratio_sales_still_additive_when_disjoint(self):
        self.assertTrue(evaluate("Sales")["direct_sum_allowed"])

    def test_non_ratio_impressions_still_additive_when_disjoint(self):
        self.assertTrue(evaluate("Impressions")["direct_sum_allowed"])

    def test_embedded_acos_substring_not_a_ratio_token(self):
        self.assertTrue(evaluate("MacroSales")["direct_sum_allowed"])

    def test_legacy_unnamed_additive_contract_is_unchanged(self):
        self.assertTrue(evaluate()["direct_sum_allowed"])

    def test_ratio_semantics_still_blocks_without_name(self):
        self.assertEqual("Blocked", evaluate(semantics="ratio_or_derived")["aggregation_status"])

    def test_unknown_semantics_still_never_allows_sum(self):
        self.assertEqual("Unknown", evaluate("ROAS", semantics="unknown")["aggregation_status"])

    def test_overlap_still_blocks_non_ratio_additive_metric(self):
        self.assertEqual("Blocked", evaluate("Sales", relation="overlapping")["aggregation_status"])


if __name__ == "__main__":
    unittest.main()

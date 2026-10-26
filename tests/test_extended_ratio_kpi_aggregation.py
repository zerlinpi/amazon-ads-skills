"""RED-first: common cost/return ratios cannot be directly summed.

Synthetic metric labels only. No external account data, credentials, or writes.
"""
import unittest

from scripts.evaluate_metric_aggregation_gate import evaluate_metric_aggregation_gate
from scripts.validate_experiment_plan import validate_experiment_plan
from test_experiment_combined_ratio_aggregation import combined_metric


def standalone(name, aggregation="additive", relation="disjoint"):
    return evaluate_metric_aggregation_gate({
        "metric_name": name,
        "metric_semantics": {"aggregation_semantics": aggregation},
        "source_relation": relation,
    })


class ExtendedRatioKpiSafetyTests(unittest.TestCase):
    def _assert_standalone_blocked(self, name):
        result = standalone(name)
        self.assertEqual("Blocked", result["aggregation_status"], result)
        self.assertFalse(result["direct_sum_allowed"], result)

    def _assert_ready_combined_rejected(self, name):
        errors = validate_experiment_plan(combined_metric(name))
        self.assertTrue(any("aggregation_semantics" in error for error in errors), errors)

    def test_cpa_standalone_additive_rejected(self):
        self._assert_standalone_blocked("CPA")

    def test_cpm_standalone_additive_rejected(self):
        self._assert_standalone_blocked("CPM")

    def test_vcpm_standalone_additive_rejected(self):
        self._assert_standalone_blocked("vCPM")

    def test_roi_standalone_additive_rejected(self):
        self._assert_standalone_blocked("ROI")

    def test_cpa_ready_combined_additive_rejected(self):
        self._assert_ready_combined_rejected("CPA")

    def test_cpm_ready_combined_additive_rejected(self):
        self._assert_ready_combined_rejected("CPM")

    def test_vcpm_ready_combined_additive_rejected(self):
        self._assert_ready_combined_rejected("vCPM")

    def test_roi_ready_combined_additive_rejected(self):
        self._assert_ready_combined_rejected("ROI")

    def test_cpa_ready_guardrail_additive_rejected(self):
        errors = validate_experiment_plan(combined_metric("CPA", guardrail=True))
        self.assertTrue(any("aggregation_semantics" in error for error in errors), errors)

    def test_roi_ready_guardrail_non_additive_rejected(self):
        errors = validate_experiment_plan(combined_metric(
            "ROI", aggregation="non_additive_deduplicated", guardrail=True
        ))
        self.assertTrue(any("aggregation_semantics" in error for error in errors), errors)

    def test_cpa_ready_ratio_semantics_valid(self):
        self.assertEqual([], validate_experiment_plan(
            combined_metric("CPA", aggregation="ratio_or_derived")
        ))

    def test_roi_ready_ratio_semantics_valid(self):
        self.assertEqual([], validate_experiment_plan(
            combined_metric("ROI", aggregation="ratio_or_derived")
        ))

    def test_roi_shadow_only_still_exploratory(self):
        self.assertEqual([], validate_experiment_plan(
            combined_metric("ROI", status="Shadow Only")
        ))

    def test_non_combined_cpm_keeps_legacy_contract(self):
        plan = combined_metric("CPM")
        plan["comparison"]["requires_combined_readout"] = False
        self.assertEqual([], validate_experiment_plan(plan))

    def test_campaign_spend_remains_additive(self):
        self.assertTrue(standalone("Spend")["direct_sum_allowed"])

    def test_campaign_impressions_remains_additive(self):
        self.assertTrue(standalone("Impressions")["direct_sum_allowed"])

    def test_embedded_roi_substring_not_ratio_token(self):
        self.assertTrue(standalone("AndroidProfile")["direct_sum_allowed"])

    def test_unknown_semantics_remains_unknown(self):
        self.assertEqual("Unknown", standalone(
            "CPA", aggregation="unknown"
        )["aggregation_status"])

    def test_overlapping_rows_remain_blocked(self):
        self.assertEqual("Blocked", standalone(
            "Spend", relation="overlapping"
        )["aggregation_status"])


if __name__ == "__main__":
    unittest.main()

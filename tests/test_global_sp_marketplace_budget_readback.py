"""Deterministic, synthetic Global SP marketplace monetary-budget readback guards.

The baseline 207 state-only evaluator must not confirm an optional monetary
budget change without exact currency, amount, recurrence and source-observed
per-marketplace budget evidence.
"""
import copy
import unittest

from test_global_sp_readback_evidence import fixture, evaluate


def budget_fixture():
    evidence = fixture()
    evidence["request"]["expected_marketplace_budgets"] = {
        "US": {"currency_code": "USD", "amount": "100.00", "budget_type": "MONETARY", "recurrence": "DAILY"},
        "GB": {"currency_code": "GBP", "amount": "80.00", "budget_type": "MONETARY", "recurrence": "DAILY"},
    }
    evidence["readback"].update({
        "budget_capability_status": "Supported",
        "budget_coverage_status": "Complete",
        "budget_pagination_status": "Complete",
        "marketplace_budgets": [
            {"marketplace": "US", "currency_code": "USD", "amount": "100", "budget_type": "MONETARY", "recurrence": "DAILY", "evidence_status": "observed"},
            {"marketplace": "GB", "currency_code": "GBP", "amount": "80.0", "budget_type": "MONETARY", "recurrence": "DAILY", "evidence_status": "observed"},
        ],
    })
    return evidence


class GlobalSpMarketplaceBudgetReadbackTests(unittest.TestCase):
    def assert_budget(self, status, mutation=None):
        evidence = budget_fixture()
        if mutation is not None:
            mutation(evidence)
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], status, result)

    def test_verified_monetary_budgets_confirmed(self):
        self.assert_budget("Confirmed")

    def test_state_only_legacy_contract_still_confirmed(self):
        self.assertEqual(evaluate(fixture())["application_status"], "Confirmed")

    def test_missing_budget_readback_is_unknown_not_state_confirmed(self):
        self.assert_budget("Unknown", lambda e: e["readback"].pop("marketplace_budgets"))

    def test_missing_budget_capability_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"].pop("budget_capability_status"))

    def test_partial_budget_capability_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"].update(budget_capability_status="Partial"))

    def test_truncated_budget_pagination_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"].update(budget_pagination_status="Truncated"))

    def test_partial_budget_coverage_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"].update(budget_coverage_status="Partial"))

    def test_missing_budget_marketplace_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"].update(marketplace_budgets=e["readback"]["marketplace_budgets"][:1]))

    def test_duplicate_budget_marketplace_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"]["marketplace_budgets"].append(copy.deepcopy(e["readback"]["marketplace_budgets"][0])))

    def test_unobserved_budget_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"]["marketplace_budgets"][1].update(evidence_status="unknown"))

    def test_budget_amount_mismatch_is_drifted(self):
        self.assert_budget("Drifted", lambda e: e["readback"]["marketplace_budgets"][0].update(amount="99.99"))

    def test_currency_mismatch_is_drifted_not_converted(self):
        self.assert_budget("Drifted", lambda e: e["readback"]["marketplace_budgets"][1].update(currency_code="EUR"))

    def test_budget_recurrence_mismatch_is_drifted(self):
        self.assert_budget("Drifted", lambda e: e["readback"]["marketplace_budgets"][1].update(recurrence="WEEKLY"))

    def test_explicit_observed_zero_budget_is_not_missing(self):
        self.assert_budget("Confirmed", lambda e: (
            e["request"]["expected_marketplace_budgets"]["GB"].update(amount="0.00"),
            e["readback"]["marketplace_budgets"][1].update(amount="0"),
        ))

    def test_nonfinite_budget_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"]["marketplace_budgets"][1].update(amount="NaN"))

    def test_negative_budget_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"]["marketplace_budgets"][1].update(amount="-1"))

    def test_missing_budget_currency_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["readback"]["marketplace_budgets"][1].pop("currency_code"))

    def test_expected_budget_scope_mismatch_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["request"]["expected_marketplace_budgets"].pop("GB"))

    def test_unsupported_budget_type_is_unknown(self):
        self.assert_budget("Unknown", lambda e: e["request"]["expected_marketplace_budgets"]["US"].update(budget_type="PERCENTAGE"))

    def test_numeric_amount_requires_explicit_decimal_text(self):
        self.assert_budget("Unknown", lambda e: e["readback"]["marketplace_budgets"][0].update(amount=100.0))


    def test_partial_receipt_overrides_matching_budget_readback(self):
        def mutate(e):
            e["receipt"]["success"] = []
            e["receipt"]["partialSuccess"] = [{"index": 0}]
        self.assert_budget("Partial", mutate)

    def test_state_drift_remains_drifted_with_complete_matching_budgets(self):
        self.assert_budget("Drifted", lambda e: e["readback"]["marketplace_states"][0].update(effective_state="PAUSED"))

    def test_extra_budget_marketplace_is_unknown(self):
        def mutate(e):
            extra = copy.deepcopy(e["readback"]["marketplace_budgets"][0])
            extra["marketplace"] = "DE"
            e["readback"]["marketplace_budgets"].append(extra)
        self.assert_budget("Unknown", mutate)

    def test_fractional_precision_is_not_float_rounded(self):
        self.assert_budget("Drifted", lambda e: (
            e["request"]["expected_marketplace_budgets"]["US"].update(amount="0.10000000000000000000000000000000000000001"),
            e["readback"]["marketplace_budgets"][0].update(amount="0.1"),
        ))

    def test_boolean_amount_is_unknown_not_zero_or_one(self):
        self.assert_budget("Unknown", lambda e: e["readback"]["marketplace_budgets"][0].update(amount=False))


if __name__ == "__main__":
    unittest.main()

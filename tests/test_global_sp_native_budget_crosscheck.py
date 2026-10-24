"""RED-first: retained native Global SP campaign budgets cannot contradict normalized budget readback.

All evidence is synthetic. Native monetary values are decimal-text lexemes preserved by
a trusted adapter; this is not authentication of raw Amazon HTTP responses.
"""
import copy
import unittest

from test_global_sp_readback_evidence import evaluate
from test_global_sp_marketplace_budget_readback import budget_fixture
from test_global_sp_native_campaign_configuration import native


def with_native_budgets():
    e = native(budget_fixture())
    e["readback"]["raw_campaign"]["budgets"] = [{
        "budgetType": "MONETARY",
        "recurrenceTimePeriod": "DAILY",
        "budgetValue": {
            "monetaryBudgetValue": {
                "marketplaceSettings": [
                    {"marketplace": "US", "monetaryBudget": {"currencyCode": "USD", "value": "100.00"}},
                    {"marketplace": "GB", "monetaryBudget": {"currencyCode": "GBP", "value": "80.00"}},
                ],
            },
        },
    }]
    return e


class NativeGlobalSpBudgetCrosscheckTests(unittest.TestCase):
    def check(self, expected, mutate=None):
        e = with_native_budgets()
        if mutate:
            mutate(e)
        result = evaluate(e)
        self.assertEqual(result["application_status"], expected, result)

    def test_valid_native_budget_confirms(self):
        self.check("Confirmed")

    def test_legacy_raw_campaign_without_budgets_confirms(self):
        self.assertEqual(evaluate(native(budget_fixture()))["application_status"], "Confirmed")

    def test_legacy_budget_without_raw_campaign_confirms(self):
        self.assertEqual(evaluate(budget_fixture())["application_status"], "Confirmed")

    def test_native_budget_amount_contradiction_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0]["monetaryBudget"].update(value="99.99"))

    def test_native_budget_currency_contradiction_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][1]["monetaryBudget"].update(currencyCode="EUR"))

    def test_native_budget_recurrence_contradiction_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0].update(recurrenceTimePeriod="WEEKLY"))

    def test_native_budget_type_contradiction_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0].update(budgetType="COST"))

    def test_explicit_null_budgets_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"].update(budgets=None))

    def test_empty_budgets_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"].update(budgets=[]))

    def test_duplicate_budget_entries_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"].append(copy.deepcopy(e["readback"]["raw_campaign"]["budgets"][0])))

    def test_invalid_budget_entry_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"].update(budgets=["invalid"]))

    def test_missing_budget_value_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0].pop("budgetValue"))

    def test_missing_monetary_budget_value_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"].pop("monetaryBudgetValue"))

    def test_invalid_marketplace_settings_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"].update(marketplaceSettings=None))

    def test_missing_marketplace_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"].pop())

    def test_duplicate_marketplace_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][1].update(marketplace="US"))

    def test_extra_marketplace_unknown(self):
        def mutate(e):
            settings = e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"]
            settings.append({"marketplace": "DE", "monetaryBudget": {"currencyCode": "EUR", "value": "60"}})
        self.check("Unknown", mutate)

    def test_invalid_marketplace_record_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"].__setitem__(0, None))

    def test_missing_currency_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0]["monetaryBudget"].pop("currencyCode"))

    def test_missing_amount_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0]["monetaryBudget"].pop("value"))

    def test_float_value_cannot_prove_exact_source_precision(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0]["monetaryBudget"].update(value=100.0))

    def test_boolean_value_unknown_not_one(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0]["monetaryBudget"].update(value=True))

    def test_invalid_negative_value_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0]["monetaryBudget"].update(value="-1"))

    def test_malformed_monetary_budget_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0].update(monetaryBudget=[]))

    def test_normalized_and_native_agree_but_intent_differs_is_drifted(self):
        def mutate(e):
            e["readback"]["marketplace_budgets"][0]["amount"] = "90"
            e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0]["monetaryBudget"]["value"] = "90.00"
        self.check("Drifted", mutate)

    def test_native_precision_equal_different_text_is_confirmed(self):
        self.check("Confirmed", lambda e: e["readback"]["raw_campaign"]["budgets"][0]["budgetValue"]["monetaryBudgetValue"]["marketplaceSettings"][0]["monetaryBudget"].update(value="100.000000000000000000"))

    def test_state_only_request_does_not_claim_budget_verification(self):
        e = with_native_budgets()
        e["request"].pop("expected_marketplace_budgets")
        for field in ("budget_capability_status", "budget_coverage_status", "budget_pagination_status", "marketplace_budgets"):
            e["readback"].pop(field)
        self.assertEqual(evaluate(e)["application_status"], "Confirmed")


if __name__ == "__main__":
    unittest.main()

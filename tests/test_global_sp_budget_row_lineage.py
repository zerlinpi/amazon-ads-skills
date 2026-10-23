"""Fail closed when optional per-row Global SP budget lineage contradicts its readback envelope.

A trusted adapter may attach row-level provenance when combining budget and
campaign-state reads. Explicit contradictory metadata must never be ignored.
"""
import copy
import unittest

from test_global_sp_marketplace_budget_readback import budget_fixture
from test_global_sp_readback_evidence import evaluate


class GlobalSpBudgetRowLineageTests(unittest.TestCase):
    def check(self, expected, mutate):
        evidence = budget_fixture()
        mutate(evidence)
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)

    def test_stale_budget_row_observation_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_budgets"][0].update(
            observed_at="2026-10-23T23:59:59Z"))

    def test_budget_row_observed_at_write_completion_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_budgets"][0].update(
            observed_at=e["request"]["completed_at"]))

    def test_budget_row_later_than_envelope_snapshot_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_budgets"][0].update(
            observed_at="2026-10-24T00:06:00Z"))

    def test_invalid_budget_row_timestamp_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_budgets"][0].update(
            observed_at="not-a-time"))

    def test_budget_row_connector_mismatch_is_unknown(self):
        def mutate(e):
            source = copy.deepcopy(e["readback"]["source"])
            source["connector_id"] = "unverified-other-connector"
            e["readback"]["marketplace_budgets"][0]["source"] = source
        self.check("Unknown", mutate)

    def test_budget_row_acquisition_channel_mismatch_is_unknown(self):
        def mutate(e):
            source = copy.deepcopy(e["readback"]["source"])
            source["acquisition_channel"] = "export"
            e["readback"]["marketplace_budgets"][1]["source"] = source
        self.check("Unknown", mutate)

    def test_incomplete_budget_row_source_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_budgets"][0].update(
            source={"source_system": "synthetic-ads-api"}))

    def test_budget_row_campaign_identity_mismatch_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_budgets"][0].update(
            campaign_id="different-campaign"))

    def test_budget_row_global_account_identity_mismatch_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_budgets"][1].update(
            global_account_id="different-account"))

    def test_consistent_row_lineage_is_confirmed(self):
        def mutate(e):
            for row in e["readback"]["marketplace_budgets"]:
                row["source"] = copy.deepcopy(e["readback"]["source"])
                row["observed_at"] = "2026-10-24T00:03:00Z"
                row["campaign_id"] = e["request"]["campaign_id"]
                row["global_account_id"] = e["request"]["global_account_id"]
        self.check("Confirmed", mutate)

    def test_complete_consistent_lineage_still_detects_budget_drift(self):
        def mutate(e):
            row = e["readback"]["marketplace_budgets"][0]
            row["source"] = copy.deepcopy(e["readback"]["source"])
            row["observed_at"] = "2026-10-24T00:03:00Z"
            row["amount"] = "99.99"
        self.check("Drifted", mutate)

    def test_partial_receipt_precedes_bad_budget_row_lineage(self):
        def mutate(e):
            e["receipt"]["success"] = []
            e["receipt"]["partialSuccess"] = [{"index": 0}]
            e["readback"]["marketplace_budgets"][0]["observed_at"] = "2026-10-23T23:59:59Z"
        self.check("Partial", mutate)


if __name__ == "__main__":
    unittest.main()

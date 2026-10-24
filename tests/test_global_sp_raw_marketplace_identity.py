"""RED-first: raw marketplace IDs must bind to normalized country-code rows.

Synthetic IDs only. Amazon Global SP status.marketplaceSettings may use raw
marketplace IDs, not the country-code namespace of campaign.marketplaces.
"""
import copy
import unittest

from test_global_sp_readback_evidence import fixture, evaluate
from test_global_sp_marketplace_budget_readback import budget_fixture


def add_identity_map(e, with_budget=False):
    source = {
        "source_system": "synthetic-marketplace-directory",
        "acquisition_channel": "lookup",
        "connector_id": "synthetic-identity-adapter",
    }
    mapping = [
        {"marketplace": "US", "marketplace_id": "SYNTHETIC_MARKET_ID_US",
         "evidence_status": "verified", "source": copy.deepcopy(source)},
        {"marketplace": "GB", "marketplace_id": "SYNTHETIC_MARKET_ID_GB",
         "evidence_status": "verified", "source": copy.deepcopy(source)},
    ]
    e["readback"]["marketplace_identity_map"] = mapping
    for row, entry in zip(e["readback"]["marketplace_states"], mapping):
        row["marketplace_id"] = entry["marketplace_id"]
    if with_budget:
        for row, entry in zip(e["readback"]["marketplace_budgets"], mapping):
            row["marketplace_id"] = entry["marketplace_id"]
    return e


class GlobalSpRawMarketplaceIdentityTests(unittest.TestCase):
    def check(self, expected, evidence):
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)
        return result

    def test_legacy_country_code_rows_still_confirmed(self):
        self.check("Confirmed", fixture())

    def test_verified_bijective_mapping_confirms_state(self):
        self.check("Confirmed", add_identity_map(fixture()))

    def test_verified_bijective_mapping_confirms_budget(self):
        self.check("Confirmed", add_identity_map(budget_fixture(), with_budget=True))

    def test_raw_state_id_without_mapping_is_unknown(self):
        e = fixture()
        e["readback"]["marketplace_states"][0]["marketplace_id"] = "SYNTHETIC_MARKET_ID_GB"
        self.check("Unknown", e)

    def test_raw_budget_id_without_mapping_is_unknown(self):
        e = budget_fixture()
        e["readback"]["marketplace_budgets"][0]["marketplace_id"] = "SYNTHETIC_MARKET_ID_GB"
        self.check("Unknown", e)

    def test_mapping_missing_market_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"].pop()
        self.check("Unknown", e)

    def test_mapping_extra_market_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"].append({
            "marketplace": "DE", "marketplace_id": "SYNTHETIC_MARKET_ID_DE",
            "evidence_status": "verified",
            "source": copy.deepcopy(e["readback"]["marketplace_identity_map"][0]["source"]),
        })
        self.check("Unknown", e)

    def test_mapping_duplicate_raw_id_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][1]["marketplace_id"] = "SYNTHETIC_MARKET_ID_US"
        self.check("Unknown", e)

    def test_mapping_duplicate_country_code_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][1]["marketplace"] = "US"
        self.check("Unknown", e)

    def test_wrong_raw_id_on_state_row_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_states"][0]["marketplace_id"] = "SYNTHETIC_MARKET_ID_GB"
        self.check("Unknown", e)

    def test_missing_raw_id_on_state_row_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_states"][0].pop("marketplace_id")
        self.check("Unknown", e)

    def test_wrong_raw_id_on_budget_row_is_unknown(self):
        e = add_identity_map(budget_fixture(), with_budget=True)
        e["readback"]["marketplace_budgets"][1]["marketplace_id"] = "SYNTHETIC_MARKET_ID_US"
        self.check("Unknown", e)

    def test_missing_raw_id_on_budget_row_is_unknown(self):
        e = add_identity_map(budget_fixture(), with_budget=True)
        e["readback"]["marketplace_budgets"][1].pop("marketplace_id")
        self.check("Unknown", e)

    def test_mapping_unverified_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0]["evidence_status"] = "unknown"
        self.check("Unknown", e)

    def test_mapping_missing_source_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0].pop("source")
        self.check("Unknown", e)

    def test_mapping_malformed_entry_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0] = []
        self.check("Unknown", e)

    def test_mapping_present_without_raw_row_ids_is_unknown(self):
        e = add_identity_map(fixture())
        for row in e["readback"]["marketplace_states"]:
            row.pop("marketplace_id")
        self.check("Unknown", e)

    def test_mapping_malformed_container_is_unknown(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"] = {"US": "SYNTHETIC_MARKET_ID_US"}
        self.check("Unknown", e)

    def test_mapping_source_is_independent_of_query_source(self):
        e = add_identity_map(fixture())
        self.assertNotEqual(
            e["readback"]["marketplace_identity_map"][0]["source"],
            e["readback"]["source"],
        )
        self.check("Confirmed", e)


if __name__ == "__main__":
    unittest.main()

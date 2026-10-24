"""RED-first: Global SP campaign readback cannot confirm unsupported marketplace identities.

Synthetic evidence only. The Amazon Global Sponsored Products guide enumerates
supported country codes; this gate must not mistake an arbitrary echoed token
for an eligible marketplace. No live Ads account access.
"""
import unittest

from test_global_sp_readback_evidence import fixture, evaluate
from test_global_sp_native_campaign_configuration import native
from test_global_sp_marketplace_budget_readback import budget_fixture


def replace_marketplace(evidence, old, new):
    request = evidence["request"]
    request["marketplaces"] = [new if m == old else m for m in request["marketplaces"]]
    request["expected_effective_states"][new] = request["expected_effective_states"].pop(old)
    if "expected_marketplace_budgets" in request:
        request["expected_marketplace_budgets"][new] = request["expected_marketplace_budgets"].pop(old)
    readback = evidence["readback"]
    for row in readback["marketplace_states"]:
        if row["marketplace"] == old:
            row["marketplace"] = new
    for row in readback.get("marketplace_budgets", []):
        if row["marketplace"] == old:
            row["marketplace"] = new
    raw = readback.get("raw_campaign")
    if raw is not None:
        raw["marketplaces"] = [new if m == old else m for m in raw["marketplaces"]]
        for item in raw["marketplaceConfigurations"]:
            if item["marketplace"] == old:
                item["marketplace"] = new
    return evidence


class GlobalSpMarketplaceEligibilityTests(unittest.TestCase):
    def assert_status(self, evidence, expected):
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)

    def test_supported_gb_country_code_confirms(self):
        self.assert_status(fixture(), "Confirmed")

    def test_supported_ae_country_code_confirms(self):
        self.assert_status(replace_marketplace(fixture(), "GB", "AE"), "Confirmed")

    def test_supported_tr_country_code_confirms(self):
        self.assert_status(replace_marketplace(fixture(), "GB", "TR"), "Confirmed")

    def test_unknown_zz_code_cannot_confirm(self):
        self.assert_status(replace_marketplace(fixture(), "GB", "ZZ"), "Unknown")

    def test_uk_alias_cannot_replace_official_gb(self):
        self.assert_status(replace_marketplace(fixture(), "GB", "UK"), "Unknown")

    def test_lowercase_us_cannot_confirm(self):
        self.assert_status(replace_marketplace(fixture(), "US", "us"), "Unknown")

    def test_three_letter_usa_cannot_confirm(self):
        self.assert_status(replace_marketplace(fixture(), "US", "USA"), "Unknown")

    def test_whitespace_marketplace_cannot_confirm(self):
        self.assert_status(replace_marketplace(fixture(), "US", "U S"), "Unknown")

    def test_unknown_code_cannot_confirm_even_with_native_echo(self):
        self.assert_status(replace_marketplace(native(fixture()), "GB", "ZZ"), "Unknown")

    def test_unknown_code_cannot_confirm_budget_change(self):
        self.assert_status(replace_marketplace(budget_fixture(), "GB", "ZZ"), "Unknown")

    def test_supported_country_code_with_native_campaign_confirms(self):
        self.assert_status(replace_marketplace(native(fixture()), "GB", "AE"), "Confirmed")



from test_global_sp_adgroup_bid_readback import fixture as adgroup_fixture, evaluate as evaluate_adgroup
from test_global_sp_target_bid_readback import fixture as target_fixture, evaluate as evaluate_target


class OtherGlobalSpResourceMarketplaceTests(unittest.TestCase):
    def test_adgroup_unknown_country_code_not_confirmed(self):
        e = adgroup_fixture()
        e["request"]["marketplaces"][1] = "ZZ"
        e["request"]["expected_marketplace_default_bids"]["ZZ"] = e["request"]["expected_marketplace_default_bids"].pop("GB")
        e["readback"]["marketplace_default_bids"][1]["marketplace"] = "ZZ"
        self.assertEqual(evaluate_adgroup(e)["application_status"], "Unknown")

    def test_adgroup_uk_alias_not_confirmed(self):
        e = adgroup_fixture()
        e["request"]["marketplaces"][1] = "UK"
        e["request"]["expected_marketplace_default_bids"]["UK"] = e["request"]["expected_marketplace_default_bids"].pop("GB")
        e["readback"]["marketplace_default_bids"][1]["marketplace"] = "UK"
        self.assertEqual(evaluate_adgroup(e)["application_status"], "Unknown")

    def test_target_unknown_country_code_not_confirmed(self):
        e = target_fixture()
        e["request"]["marketplace"] = "ZZ"
        e["readback"]["marketplace"] = "ZZ"
        e["readback"]["target_bid"]["marketplace"] = "ZZ"
        self.assertEqual(evaluate_target(e)["application_status"], "Unknown")

    def test_target_uk_alias_not_confirmed(self):
        e = target_fixture()
        e["request"]["marketplace"] = "UK"
        e["readback"]["marketplace"] = "UK"
        e["readback"]["target_bid"]["marketplace"] = "UK"
        self.assertEqual(evaluate_target(e)["application_status"], "Unknown")

    def test_supported_country_code_remains_valid_for_target(self):
        e = target_fixture()
        e["request"]["marketplace"] = "AE"
        e["readback"]["marketplace"] = "AE"
        e["readback"]["target_bid"]["marketplace"] = "AE"
        self.assertEqual(evaluate_target(e)["application_status"], "Confirmed")

if __name__ == "__main__":
    unittest.main()

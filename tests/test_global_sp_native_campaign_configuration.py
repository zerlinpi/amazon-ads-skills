"""RED-first: explicit native Global SP campaign configuration cannot contradict normalized state.

All values are synthetic. The optional raw_campaign is a trusted adapter's
retained query resource, not cryptographic evidence of API authenticity.
"""
import copy
import unittest

from test_global_sp_readback_evidence import fixture, evaluate
from test_global_sp_marketplace_budget_readback import budget_fixture


def native(evidence):
    evidence["readback"]["raw_campaign"] = {
        "campaignId": "synthetic-campaign-a",
        "adProduct": "SPONSORED_PRODUCTS",
        "marketplaceScope": "GLOBAL",
        "marketplaces": ["US", "GB"],
        "state": "ENABLED",
        "marketplaceConfigurations": [
            {"marketplace": "GB", "overrides": {"state": "PAUSED"}},
        ],
    }
    return evidence


class NativeCampaignConfigurationTests(unittest.TestCase):
    def check(self, expected, evidence):
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)

    def test_legacy_normalized_envelope_still_confirms(self):
        self.check("Confirmed", fixture())

    def test_consistent_native_configuration_confirms(self):
        self.check("Confirmed", native(fixture()))

    def test_consistent_native_configuration_with_budget_confirms(self):
        self.check("Confirmed", native(budget_fixture()))

    def test_delivery_health_does_not_override_configured_state(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["status"] = {
            "deliveryStatus": "NOT_DELIVERING",
            "marketplaceSettings": [{"marketplace": "US", "deliveryStatus": "NOT_DELIVERING"}],
        }
        self.check("Confirmed", e)

    def test_global_state_conflicts_with_normalized_us(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["state"] = "PAUSED"
        self.check("Unknown", e)

    def test_missing_gb_override_conflicts_with_normalized_gb(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"] = []
        self.check("Unknown", e)

    def test_gb_override_conflicts_with_normalized_gb(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"][0]["overrides"]["state"] = "ENABLED"
        self.check("Unknown", e)

    def test_native_campaign_id_mismatch(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["campaignId"] = "synthetic-other-campaign"
        self.check("Unknown", e)

    def test_native_account_identity_mismatch(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["globalAccountId"] = "synthetic-other-account"
        self.check("Unknown", e)

    def test_native_ad_product_mismatch(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["adProduct"] = "SPONSORED_BRANDS"
        self.check("Unknown", e)

    def test_native_marketplace_scope_mismatch(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceScope"] = "LOCAL"
        self.check("Unknown", e)

    def test_native_marketplace_missing(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaces"] = ["US"]
        self.check("Unknown", e)

    def test_native_marketplace_duplicate(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaces"].append("GB")
        self.check("Unknown", e)

    def test_extra_configuration_marketplace(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"].append(
            {"marketplace": "DE", "overrides": {"state": "PAUSED"}}
        )
        self.check("Unknown", e)

    def test_duplicate_configuration_marketplace(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"].append(
            copy.deepcopy(e["readback"]["raw_campaign"]["marketplaceConfigurations"][0])
        )
        self.check("Unknown", e)

    def test_invalid_override_container(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"][0]["overrides"] = []
        self.check("Unknown", e)

    def test_missing_override_container(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"][0].pop("overrides")
        self.check("Unknown", e)

    def test_missing_global_state(self):
        e = native(fixture())
        e["readback"]["raw_campaign"].pop("state")
        self.check("Unknown", e)

    def test_delivery_status_cannot_replace_state(self):
        e = native(fixture())
        e["readback"]["raw_campaign"].pop("state")
        e["readback"]["raw_campaign"]["status"] = {"deliveryStatus": "DELIVERING"}
        self.check("Unknown", e)

    def test_invalid_global_state(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["state"] = "NOT_DELIVERING"
        self.check("Unknown", e)

    def test_missing_configuration_collection(self):
        e = native(fixture())
        e["readback"]["raw_campaign"].pop("marketplaceConfigurations")
        self.check("Unknown", e)

    def test_malformed_configuration_collection(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"] = {}
        self.check("Unknown", e)

    def test_malformed_native_campaign(self):
        e = native(fixture())
        e["readback"]["raw_campaign"] = []
        self.check("Unknown", e)

    def test_malformed_configuration_entry(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"][0] = []
        self.check("Unknown", e)

    def test_native_and_normalized_agree_but_differ_from_request_is_drifted(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"][0]["overrides"]["state"] = "ENABLED"
        e["readback"]["marketplace_states"][1]["effective_state"] = "ENABLED"
        self.check("Drifted", e)

    def test_inherited_global_state_without_override_is_supported(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"] = []
        e["request"]["expected_effective_states"]["GB"] = "ENABLED"
        e["readback"]["marketplace_states"][1]["effective_state"] = "ENABLED"
        self.check("Confirmed", e)

    def test_configuration_with_other_override_fields_inherits_global_state(self):
        e = native(fixture())
        e["readback"]["raw_campaign"]["marketplaceConfigurations"][0]["overrides"] = {"name": "synthetic-name"}
        e["request"]["expected_effective_states"]["GB"] = "ENABLED"
        e["readback"]["marketplace_states"][1]["effective_state"] = "ENABLED"
        self.check("Confirmed", e)


if __name__ == "__main__":
    unittest.main()

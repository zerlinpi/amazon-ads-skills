"""RED-first deterministic mixed-resource Global SP plan readback safety contract.

Synthetic adapter evidence only. A complete declared plan is NOT proven by one
successful campaign, ad-group or target receipt.
"""
import copy
import unittest


def fixture():
    from test_global_sp_readback_evidence import fixture as campaign
    from test_global_sp_adgroup_bid_readback import fixture as adgroup
    from test_global_sp_target_bid_readback import fixture as target
    c, a, t = campaign(), adgroup(), target()
    for part in (t["request"], t["receipt"], t["readback"]):
        part["global_account_id"] = "synthetic-global-a"
        part["campaign_id"] = "synthetic-campaign-a"
        part["ad_group_id"] = "synthetic-adgroup-a"
    return {
        "manifest": {
            "plan_id": "synthetic-plan-1",
            "global_account_id": "synthetic-global-a",
            "coverage_status": "Complete",
            "source": {"source_system": "synthetic-planner",
                       "acquisition_channel": "plan",
                       "connector_id": "synthetic-plan-adapter"},
            "components": [
                {"component_id": "campaign", "kind": "campaign",
                 "campaign_id": "synthetic-campaign-a"},
                {"component_id": "adgroup", "kind": "ad_group",
                 "request_ids": ["synthetic-request-01"]},
                {"component_id": "target", "kind": "target",
                 "request_ids": ["synthetic-request-t1"]},
            ],
        },
        "components": [
            {"component_id": "campaign", "kind": "campaign", "evidence": c},
            {"component_id": "adgroup", "kind": "ad_group", "evidence": a},
            {"component_id": "target", "kind": "target", "evidence": t},
        ],
    }


def evaluate(evidence):
    try:
        from scripts.evaluate_global_sp_mixed_plan_readback import (
            evaluate_global_sp_mixed_plan_readback,
        )
    except ImportError as exc:
        raise AssertionError("mixed-resource plan readback verifier is missing") from exc
    return evaluate_global_sp_mixed_plan_readback(evidence)


class MixedPlanReadbackTests(unittest.TestCase):
    def check(self, expected, mutation=None):
        d = fixture()
        if mutation:
            mutation(d)
        result = evaluate(d)
        self.assertEqual(result["application_status"], expected, result)
        self.assertTrue(result["reasons"], result)
        return result

    def test_complete_three_resource_plan_confirmed(self):
        result = self.check("Confirmed")
        self.assertEqual([x["component_id"] for x in result["components"]],
                         ["campaign", "adgroup", "target"])
        self.assertTrue(all(x["application_status"] == "Confirmed"
                            for x in result["components"]))

    def test_order_independent_component_evidence(self):
        self.check("Confirmed", lambda d: d["components"].reverse())

    def test_target_drift_not_overwritten_by_campaign_confirmation(self):
        self.check("Drifted", lambda d: d["components"][2]["evidence"][
            "readback"]["target_bid"].update(amount="0.91"))

    def test_adgroup_partial_receipt_not_full_plan_success(self):
        def change(d):
            receipt = d["components"][1]["evidence"]["receipt"]
            receipt["success"] = []
            receipt["partialSuccess"] = [{"index": 0}]
        self.check("Partial", change)

    def test_unknown_target_evidence_outranks_partial_receipt(self):
        def change(d):
            d["components"][2]["evidence"].pop("readback")
            receipt = d["components"][1]["evidence"]["receipt"]
            receipt["success"] = []
            receipt["partialSuccess"] = [{"index": 0}]
        self.check("Unknown", change)

    def test_missing_declared_component_unknown(self):
        self.check("Unknown", lambda d: d["components"].pop())

    def test_extra_undeclared_component_unknown(self):
        self.check("Unknown", lambda d: d["components"].append(
            copy.deepcopy(d["components"][0])))

    def test_duplicate_manifest_component_unknown(self):
        self.check("Unknown", lambda d: d["manifest"]["components"].append(
            copy.deepcopy(d["manifest"]["components"][0])))

    def test_missing_manifest_unknown(self):
        self.check("Unknown", lambda d: d.pop("manifest"))

    def test_manifest_partial_coverage_unknown(self):
        self.check("Unknown", lambda d: d["manifest"].update(
            coverage_status="Partial"))

    def test_manifest_missing_lineage_unknown(self):
        self.check("Unknown", lambda d: d["manifest"].update(source={}))

    def test_manifest_mismatched_plan_account_unknown(self):
        self.check("Unknown", lambda d: d["manifest"].update(
            global_account_id="synthetic-global-other"))

    def test_manifest_request_id_mismatch_unknown(self):
        self.check("Unknown", lambda d: d["manifest"]["components"][1].update(
            request_ids=["another-request"]))

    def test_manifest_campaign_id_mismatch_unknown(self):
        self.check("Unknown", lambda d: d["manifest"]["components"][0].update(
            campaign_id="another-campaign"))

    def test_cross_resource_duplicate_request_id_unknown(self):
        def change(d):
            d["components"][2]["evidence"]["request"]["request_id"] = "synthetic-request-01"
            d["components"][2]["evidence"]["receipt"]["request_id"] = "synthetic-request-01"
            d["manifest"]["components"][2]["request_ids"] = ["synthetic-request-01"]
        self.check("Unknown", change)

    def test_unverified_extra_plan_intent_unknown(self):
        self.check("Unknown", lambda d: d.update(expected_placement_adjustment={}))

    def test_unsupported_component_kind_unknown(self):
        def change(d):
            d["manifest"]["components"][2]["kind"] = "placement"
            d["components"][2]["kind"] = "placement"
        self.check("Unknown", change)

    def test_unhashable_manifest_kind_is_unknown_not_exception(self):
        self.check("Unknown", lambda d: d["manifest"]["components"][2].update(
            kind=[]))

    def test_child_claimed_verdict_is_not_trusted(self):
        self.check("Unknown", lambda d: d["components"][2].update(
            application_status="Confirmed"))

    def test_child_stale_readback_unknown(self):
        self.check("Unknown", lambda d: d["components"][2]["evidence"][
            "readback"].update(observed_at="2026-10-23T00:00:00Z"))

    def test_component_malformed_type_unknown(self):
        self.check("Unknown", lambda d: d["components"].__setitem__(0, []))

    def test_malformed_plan_id_unknown(self):
        self.check("Unknown", lambda d: d["manifest"].update(plan_id=[]))

    def test_duplicate_entity_in_separate_components_unknown(self):
        def change(d):
            a = copy.deepcopy(d["components"][2])
            a["component_id"] = "target2"
            a["evidence"]["request"]["request_id"] = "synthetic-request-t2"
            a["evidence"]["receipt"]["request_id"] = "synthetic-request-t2"
            d["components"].append(a)
            d["manifest"]["components"].append({
                "component_id": "target2", "kind": "target",
                "request_ids": ["synthetic-request-t2"]})
        self.check("Unknown", change)

    def test_manifest_unknown_descriptor_field_unknown(self):
        self.check("Unknown", lambda d: d["manifest"]["components"][1].update(
            expected_placement_bids={}))

    def test_plan_contains_adgroup_batch_and_target_batch(self):
        from test_global_sp_adgroup_batch_readback import fixture as adgroup_batch
        from test_global_sp_target_batch_readback import fixture as target_batch
        d = fixture()
        a, t = adgroup_batch(), target_batch()
        for req in t["requests"]:
            req["global_account_id"] = "synthetic-global-a"
        t["receipt"]["global_account_id"] = "synthetic-global-a"
        for row in t["readbacks"]:
            row["readback"]["global_account_id"] = "synthetic-global-a"
        d["manifest"]["components"] = [
            {"component_id": "ag-batch", "kind": "ad_group_batch",
             "request_ids": [x["request_id"] for x in a["requests"]]},
            {"component_id": "t-batch", "kind": "target_batch",
             "request_ids": [x["request_id"] for x in t["requests"]]},
        ]
        d["components"] = [
            {"component_id": "ag-batch", "kind": "ad_group_batch", "evidence": a},
            {"component_id": "t-batch", "kind": "target_batch", "evidence": t},
        ]
        self.assertEqual(evaluate(d)["application_status"], "Confirmed")

    def test_malformed_batch_request_does_not_crash(self):
        from test_global_sp_target_batch_readback import fixture as target_batch
        d = fixture()
        t = target_batch()
        d["manifest"]["components"] = [
            {"component_id": "target-batch", "kind": "target_batch",
             "request_ids": [x["request_id"] for x in t["requests"]]},
        ]
        d["components"] = [
            {"component_id": "target-batch", "kind": "target_batch", "evidence": t},
        ]
        t["requests"][0]["global_account_id"] = []
        self.assertEqual(evaluate(d)["application_status"], "Unknown")


if __name__ == "__main__":
    unittest.main()

import json
import unittest
from pathlib import Path

from scripts.compare_control_state import compare_control_state

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_ID = "control-requirements@2026-09-21"


def snapshot(state=1, status="observed", control="base_bid", marketplace="ATVPDKIKX0DER", profile="p1", effective="2026-09-18T00:00:00Z"):
    return {
        "scope": {"marketplace_id": marketplace, "profile_id": profile},
        "observed_at": "2026-09-19T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {"required_control_types": [control], "coverage_status": "Complete", "requirement_provenance": {"decision_surface": "fixture_control_comparison", "derivation_status": "Verified", "capability_snapshot_id": "fixture-capability-snapshot", "requirement_registry_id": REGISTRY_ID, "evidence_note": "Deterministic test fixture requirement set."}},
        "controls": [{"control_type": control, "state": state, "effective_at": effective, "evidence_status": status}],
    }


class ControlStateComparabilityTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8").lower()

    def test_shared_reference_requires_control_state_identity_for_causal_comparison(self):
        text = self.read("references/control-state-comparability.md")
        for token in ["control-state comparability", "audience bid adjustment", "bidding strategy", "placement", "confound", "directional"]:
            self.assertIn(token, text)

    def test_post_change_review_gates_on_control_state_comparability(self):
        text = self.read("skills/post-change-review/SKILL.md")
        for token in ["control-state-comparability.md", "baseline", "post-change", "directional"]:
            self.assertIn(token, text)

    def test_machine_readable_snapshot_preserves_unknown_provenance_and_coverage(self):
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        self.assertTrue({"scope", "observed_at", "source", "coverage", "controls"}.issubset(set(schema["required"])))
        coverage = schema["properties"]["coverage"]
        self.assertTrue({"required_control_types", "coverage_status", "requirement_provenance"}.issubset(set(coverage["required"])))
        self.assertIn("Unknown", coverage["properties"]["coverage_status"]["enum"])
        provenance = coverage["properties"]["requirement_provenance"]
        self.assertTrue({"decision_surface", "derivation_status", "requirement_registry_id"}.issubset(set(provenance["required"])))
        self.assertIn("Verified", provenance["properties"]["derivation_status"]["enum"])
        control = schema["properties"]["controls"]["items"]
        self.assertTrue({"control_type", "state", "effective_at", "evidence_status"}.issubset(set(control["required"])))
        self.assertIn("unknown", control["properties"]["evidence_status"]["enum"])
        self.assertIn("entity_type", schema["properties"]["scope"]["properties"])

    def test_versioned_requirement_registry_exists(self):
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["registry_id"], REGISTRY_ID)
        self.assertIn("fixture_control_comparison", registry["decision_surfaces"])
        self.assertEqual(registry["decision_surfaces"]["fixture_control_comparison"]["required_control_types"], ["base_bid"])

    def test_registry_control_types_are_schema_canonical(self):
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        allowed = set(schema["$defs"]["controlType"]["enum"])
        for name, surface in registry["decision_surfaces"].items():
            with self.subTest(surface=name):
                self.assertTrue(set(surface["required_control_types"]).issubset(allowed))

    def test_registry_has_evidence_backed_sp_bid_change_surface(self):
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        surface = registry["decision_surfaces"]["sponsored_products_bid_change"]
        self.assertEqual(set(surface["required_control_types"]), {"base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing", "targeting_or_routing"})
        self.assertGreaterEqual(len(surface["evidence_basis"]), 4)
        self.assertTrue(all(item.startswith("amazon-ads-official:") for item in surface["evidence_basis"]))

    def test_registry_has_evidence_backed_sp_budget_change_surface(self):
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        surface = registry["decision_surfaces"]["sponsored_products_budget_change"]
        self.assertEqual(set(surface["required_control_types"]), {"base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing", "targeting_or_routing"})
        self.assertGreaterEqual(len(surface["evidence_basis"]), 5)
        self.assertTrue(all(item.startswith("amazon-ads-official:") for item in surface["evidence_basis"]))

    def test_comparator_isolates_sp_budget_change_with_full_material_control_set(self):
        required = ["base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing", "targeting_or_routing"]

        def budget_snapshot(base_budget, effective_budget):
            states = {
                "base_bid": 1.0,
                "bidding_strategy": "dynamic_down_only",
                "placement_adjustment": {"top_of_search": 0, "product_pages": 0, "rest_of_search": 0},
                "audience_bid_adjustment": [],
                "schedule_or_event_rule": {"schedule_rules": [], "event_rules": []},
                "budget_or_pacing": {"base_average_daily_budget": base_budget, "effective_daily_budget": effective_budget, "active_budget_rules": [], "average_daily_budget_policy": "monthly_average_with_daily_flexibility"},
                "targeting_or_routing": {"site_restriction": "ALL_ELIGIBLE"},
            }
            controls = []
            for control_type, state in states.items():
                item = {"control_type": control_type, "state": state, "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"}
                if control_type == "audience_bid_adjustment":
                    item["collection_evidence"] = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}
                controls.append(item)
            return {
                "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "p1", "campaign_id": "sp-campaign-1"},
                "observed_at": "2026-09-20T00:00:00Z",
                "source": {"source_system": "fixture", "acquisition_channel": "test"},
                "coverage": {"required_control_types": required, "coverage_status": "Complete", "requirement_provenance": {"decision_surface": "sponsored_products_budget_change", "derivation_status": "Verified", "capability_snapshot_id": "fixture-capability-snapshot", "requirement_registry_id": REGISTRY_ID, "evidence_note": "Deterministic Sponsored Products budget-change fixture."}},
                "controls": controls,
            }

        before = budget_snapshot(100, 100)
        after = budget_snapshot(120, 120)
        self.assertEqual(compare_control_state(before, after, "budget_or_pacing")["classification"], "Treatment Isolated")
        after["controls"][0]["state"] = 1.2
        self.assertEqual(compare_control_state(before, after, "budget_or_pacing")["classification"], "Confounded")
        incomplete = budget_snapshot(120, 120)
        incomplete["controls"][-1]["state"].pop("active_budget_rules")
        self.assertEqual(compare_control_state(before, incomplete, "budget_or_pacing")["classification"], "Unknown")

    def test_budget_skill_routes_causal_review_through_effective_budget_state(self):
        text = self.read("skills/budget-optimization/SKILL.md")
        for token in ["control-state-comparability.md", "sponsored_products_budget_change", "base_average_daily_budget", "effective_daily_budget", "active_budget_rules", "missing rule evidence is never zero rules"]:
            self.assertIn(token, text)

    def test_shared_reference_routes_machine_contract(self):
        text = self.read("references/control-state-comparability.md")
        for token in ["schemas/control-state-snapshot.json", "missing", "unknown", "coverage", "requirement provenance", "control-requirement-registry.json"]:
            self.assertIn(token, text)

    def test_comparator_classifies_stable_state_as_comparable(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot())["classification"], "Comparable")

    def test_comparator_fails_closed_when_required_control_state_is_null(self):
        before, after = snapshot(state=None), snapshot(state=None)
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_when_coverage_is_unknown(self):
        before, after = snapshot(), snapshot(); before["coverage"]["coverage_status"] = "Unknown"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_when_requirement_provenance_is_unverified(self):
        before, after = snapshot(), snapshot(); before["coverage"]["requirement_provenance"]["derivation_status"] = "Unknown"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_when_registry_identity_is_missing(self):
        before, after = snapshot(), snapshot(); before["coverage"]["requirement_provenance"].pop("requirement_registry_id")
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_when_required_set_disagrees_with_registry(self):
        before, after = snapshot(), snapshot()
        before["coverage"]["required_control_types"] = ["budget_or_pacing"]; after["coverage"]["required_control_types"] = ["budget_or_pacing"]
        before["controls"] = [{"control_type": "budget_or_pacing", "state": 10, "effective_at": "2026-09-18T00:00:00Z", "evidence_status": "observed"}]
        after["controls"] = [{"control_type": "budget_or_pacing", "state": 10, "effective_at": "2026-09-18T00:00:00Z", "evidence_status": "observed"}]
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_when_required_control_is_not_evidenced(self):
        before, after = snapshot(), snapshot(); before["coverage"]["required_control_types"].append("audience_bid_adjustment"); after["coverage"]["required_control_types"].append("audience_bid_adjustment")
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_isolates_intended_treatment(self):
        self.assertEqual(compare_control_state(snapshot(1), snapshot(2), "base_bid")["classification"], "Treatment Isolated")

    def test_comparator_fails_closed_on_unknown_evidence(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot(status="unsupported"))["classification"], "Unknown")

    def test_comparator_fails_closed_on_scope_mismatch(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot(profile="p2"))["classification"], "Unknown")

    def test_comparator_fails_closed_on_campaign_scope_mismatch(self):
        before, after = snapshot(), snapshot(); before["scope"]["campaign_id"] = "campaign-a"; after["scope"]["campaign_id"] = "campaign-b"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_on_ad_group_scope_mismatch(self):
        before, after = snapshot(), snapshot(); before["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a"}); after["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-b"})
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_on_entity_scope_mismatch(self):
        before, after = snapshot(), snapshot(); before["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a", "entity_id": "keyword-a"}); after["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a", "entity_id": "keyword-b"})
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_when_entity_id_has_no_entity_type(self):
        before, after = snapshot(), snapshot(); before["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a", "entity_id": "123"}); after["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a", "entity_id": "123"})
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_on_entity_type_mismatch_for_same_entity_id(self):
        before, after = snapshot(), snapshot(); before["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a", "entity_id": "123", "entity_type": "keyword"}); after["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a", "entity_id": "123", "entity_type": "targeting_expression"})
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_accepts_same_typed_entity_identity(self):
        before, after = snapshot(), snapshot(); before["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a", "entity_id": "123", "entity_type": "keyword"}); after["scope"].update({"campaign_id": "campaign-a", "ad_group_id": "ad-group-a", "entity_id": "123", "entity_type": "keyword"})
        self.assertEqual(compare_control_state(before, after)["classification"], "Comparable")

    def test_comparator_marks_overlapping_change_confounded(self):
        before = snapshot(1); after = snapshot(2)
        before["coverage"]["required_control_types"].append("budget_or_pacing"); after["coverage"]["required_control_types"].append("budget_or_pacing")
        before["controls"].append({"control_type": "budget_or_pacing", "state": 10, "effective_at": "2026-09-18T00:00:00Z", "evidence_status": "observed"})
        after["controls"].append({"control_type": "budget_or_pacing", "state": 20, "effective_at": "2026-09-19T00:00:00Z", "evidence_status": "observed"})
        before["coverage"]["requirement_provenance"]["decision_surface"] = "fixture_control_comparison_with_budget"; after["coverage"]["requirement_provenance"]["decision_surface"] = "fixture_control_comparison_with_budget"
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Confounded")


if __name__ == "__main__":
    unittest.main()

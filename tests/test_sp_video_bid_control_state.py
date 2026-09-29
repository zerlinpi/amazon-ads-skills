import json
import unittest
from pathlib import Path

from scripts.compare_control_state import compare_control_state


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "references" / "control-requirement-registry.json"
SCHEMA_PATH = ROOT / "schemas" / "control-state-snapshot.json"


class SponsoredProductsVideoBidControlTests(unittest.TestCase):
    def read_registry(self):
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def make_snapshot(self, *, base_bid=1.0, video_boost=0):
        registry = self.read_registry()
        registry_id = registry["registry_id"]
        required = registry["decision_surfaces"]["sponsored_products_bid_change"]["required_control_types"]
        states = {
            "base_bid": base_bid,
            "bidding_strategy": "dynamic_down_only",
            "placement_adjustment": {
                "top_of_search": 0,
                "rest_of_search": 0,
                "product_pages": 0,
            },
            "audience_bid_adjustment": [],
            "video_bid_adjustment": video_boost,
            "schedule_or_event_rule": {"schedule_rules": [], "event_rules": []},
            "budget_or_pacing": {"daily_budget": 100},
            "targeting_or_routing": {"site_restriction": "ALL_ELIGIBLE"},
        }
        controls = []
        for control_type in required:
            item = {
                "control_type": control_type,
                "state": states[control_type],
                "effective_at": "2026-09-29T00:00:00Z",
                "evidence_status": "observed",
            }
            if control_type == "audience_bid_adjustment":
                item["collection_evidence"] = {
                    "enumeration_status": "Complete",
                    "pagination_status": "Complete",
                    "capability_status": "Supported",
                }
            if control_type == "schedule_or_event_rule":
                item["nested_collection_evidence"] = {
                    "schedule_rules": {
                        "enumeration_status": "Complete",
                        "pagination_status": "Complete",
                        "capability_status": "Supported",
                    },
                    "event_rules": {
                        "enumeration_status": "Complete",
                        "pagination_status": "Complete",
                        "capability_status": "Supported",
                    },
                }
            controls.append(item)
        return {
            "scope": {
                "marketplace_id": "ATVPDKIKX0DER",
                "profile_id": "p1",
                "campaign_id": "sp-campaign-1",
            },
            "observed_at": "2026-09-29T00:00:00Z",
            "source": {"source_system": "fixture", "acquisition_channel": "test"},
            "coverage": {
                "required_control_types": required,
                "coverage_status": "Complete",
                "requirement_provenance": {
                    "decision_surface": "sponsored_products_bid_change",
                    "derivation_status": "Verified",
                    "capability_snapshot_id": "fixture-capability-snapshot",
                    "requirement_registry_id": registry_id,
                    "evidence_note": "Deterministic SP video bid-control fixture.",
                },
            },
            "controls": controls,
        }

    def test_schema_and_registry_promote_video_bid_adjustment_to_material_control(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        allowed = set(schema["$defs"]["controlType"]["enum"])
        self.assertIn("video_bid_adjustment", allowed)

        registry = self.read_registry()
        for surface_name in ("sponsored_products_bid_change", "sponsored_products_budget_change"):
            with self.subTest(surface=surface_name):
                self.assertIn(
                    "video_bid_adjustment",
                    registry["decision_surfaces"][surface_name]["required_control_types"],
                )

    def test_video_bid_change_confounds_base_bid_causal_review(self):
        before = self.make_snapshot(base_bid=1.0, video_boost=0)
        after = self.make_snapshot(base_bid=1.2, video_boost=100)
        result = compare_control_state(before, after, "base_bid")
        self.assertEqual(result["classification"], "Confounded")
        self.assertIn("video_bid_adjustment", result.get("changed_controls", []))


if __name__ == "__main__":
    unittest.main()

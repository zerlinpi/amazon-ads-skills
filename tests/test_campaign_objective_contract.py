import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CampaignObjectiveContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_campaign_objective_schema_has_bounded_roles_and_unknown_state(self):
        schema = json.loads(self.read("schemas/campaign-objective.json"))
        role_enum = schema["properties"]["role"]["enum"]
        self.assertEqual(set(role_enum), {"Discovery", "Control", "Growth", "Profit", "Defense", "Experiment", "Unknown"})
        self.assertIn("source", schema["required"])
        self.assertIn("confidence", schema["properties"])
        self.assertIn("primary_metric", schema["properties"])
        self.assertIn("guardrail_metrics", schema["properties"])

    def test_reference_blocks_one_size_fits_all_objective_inference(self):
        reference = self.read("references/campaign-objective.md")
        for term in ("Discovery", "Control", "Growth", "Profit", "Defense", "Experiment", "Unknown", "ACOS", "TACOS", "organic", "inferred"):
            self.assertIn(term, reference)
        self.assertIn("do not infer", reference.lower())
        self.assertIn("no universal", reference.lower())

    def test_user_facing_capability_map_exposes_objective_contract(self):
        capabilities = self.read("docs/CAPABILITIES.md").lower()
        self.assertIn("campaign objective contract", capabilities)
        self.assertIn("references/campaign-objective.md", capabilities)
        self.assertIn("schemas/campaign-objective.json", capabilities)

    def test_action_contract_can_preserve_campaign_objective(self):
        action = json.loads(self.read("schemas/optimization-action.json"))
        self.assertIn("campaign_objective", action["properties"])


if __name__ == "__main__":
    unittest.main()

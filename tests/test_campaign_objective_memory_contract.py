import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CampaignObjectiveMemoryContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_entity_history_latest_action_preserves_campaign_objective(self):
        schema = json.loads(self.read("schemas/entity-history.json"))
        latest_action = schema["properties"]["latest_action"]
        self.assertIn("properties", latest_action)
        self.assertIn("campaign_objective", latest_action["properties"])
        objective = latest_action["properties"]["campaign_objective"]
        self.assertIn("anyOf", objective)
        refs = [item.get("$ref") for item in objective["anyOf"] if isinstance(item, dict)]
        self.assertIn("campaign-objective.json", refs)

    def test_memory_contract_prevents_retroactive_objective_reinterpretation(self):
        memory = self.read("references/optimization-memory.md").lower()
        self.assertIn("action-time campaign objective", memory)
        self.assertIn("objective drift", memory)
        self.assertIn("do not retroactively", memory)

    def test_post_change_review_uses_action_time_objective(self):
        skill = self.read("skills/post-change-review/SKILL.md")
        lower = skill.lower()
        self.assertIn("../../references/campaign-objective.md", skill)
        self.assertIn("action-time campaign objective", lower)
        self.assertIn("current campaign objective", lower)
        self.assertIn("objective drift", lower)
        self.assertIn("do not retroactively", lower)

    def test_weekly_review_checks_objective_drift_on_prior_actions(self):
        playbook = self.read("playbooks/weekly-review.md").lower()
        self.assertIn("action-time campaign objective", playbook)
        self.assertIn("objective drift", playbook)
        self.assertIn("do not retroactively", playbook)


if __name__ == "__main__":
    unittest.main()

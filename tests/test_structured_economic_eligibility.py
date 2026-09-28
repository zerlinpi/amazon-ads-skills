import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StructuredEconomicEligibilityContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_action_schema_preserves_economic_eligibility(self):
        schema = json.loads(self.read("schemas/optimization-action.json"))
        properties = schema["properties"]

        self.assertIn("economic_eligibility", properties)
        eligibility = properties["economic_eligibility"]
        self.assertEqual(eligibility["type"], "object")
        self.assertEqual(
            eligibility["required"],
            ["status", "reason"],
        )
        self.assertEqual(
            eligibility["properties"]["status"]["enum"],
            ["Eligible", "Directional", "Not Comparable", "Missing Data"],
        )

    def test_profitability_requires_ineligible_actions_to_stay_non_actionable(self):
        skill = self.read("skills/profitability-analysis/SKILL.md").lower()

        self.assertIn("economic_eligibility", skill)
        self.assertIn("not comparable", skill)
        self.assertIn("missing data", skill)
        self.assertIn("do not emit", skill)
        self.assertIn("action proposal", skill)


if __name__ == "__main__":
    unittest.main()

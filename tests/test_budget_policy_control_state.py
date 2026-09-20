import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BudgetPolicyControlStateTests(unittest.TestCase):
    def test_budget_change_contract_requires_average_daily_budget_policy_state(self):
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        surface = registry["decision_surfaces"]["sponsored_products_budget_change"]
        notes = surface["notes"].lower()
        self.assertIn("average_daily_budget_policy", notes)
        self.assertIn("sponsored-ads-daily-budgeting-policy", " ".join(surface["evidence_basis"]))
        self.assertIn("unavailable rule or average_daily_budget_policy state keeps coverage incomplete/unknown", notes)


if __name__ == "__main__":
    unittest.main()

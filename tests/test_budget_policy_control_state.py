import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BudgetPolicyControlStateTests(unittest.TestCase):
    def test_budget_change_contract_requires_average_daily_budget_policy_state(self):
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        notes = registry["decision_surfaces"]["sponsored_products_budget_change"]["notes"].lower()
        self.assertIn("average_daily_budget_policy", notes)

    def test_budget_skill_requires_policy_state_before_single_day_overspend_causality(self):
        text = (ROOT / "skills/budget-optimization/SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("average_daily_budget_policy", text)
        self.assertIn("single-day spend", text)


if __name__ == "__main__":
    unittest.main()

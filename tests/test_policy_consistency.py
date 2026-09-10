import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ActionSizingPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_shared_action_sizing_reference_exists(self):
        self.assertTrue(
            (ROOT / "references/action-sizing.md").is_file(),
            "monetary-control recommendations need one shared contextual action-sizing policy",
        )

    def test_decision_boundaries_do_not_define_universal_default_percentages(self):
        text = self.read("references/decision-boundaries.md")
        self.assertIn("action-sizing.md", text)
        self.assertNotIn("±20%", text)
        self.assertNotIn("±25%", text)

    def test_bid_skill_routes_change_magnitude_to_shared_policy(self):
        text = self.read("skills/bid-optimization/SKILL.md")
        self.assertIn("action-sizing.md", text)
        self.assertNotIn("默认单次建议通常限制在当前 bid 的 ±20%", text)
        self.assertNotIn("single_change_pct <= 20%", text)

    def test_budget_skill_routes_change_magnitude_to_shared_policy(self):
        text = self.read("skills/budget-optimization/SKILL.md")
        self.assertIn("action-sizing.md", text)


class ReportCoveragePolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_shared_report_coverage_reference_exists(self):
        self.assertTrue(
            (ROOT / "references/report-coverage.md").is_file(),
            "report row-inclusion and eligibility rules need one shared coverage policy",
        )

    def test_search_term_skill_routes_coverage_sensitive_claims_to_shared_policy(self):
        text = self.read("skills/search-term-analysis/SKILL.md")
        self.assertIn("report-coverage.md", text)
        self.assertIn("row-inclusion", text)

    def test_data_lineage_treats_row_eligibility_as_measurement_identity(self):
        text = self.read("references/data-lineage.md")
        self.assertIn("row-inclusion", text)
        self.assertIn("report-coverage.md", text)


if __name__ == "__main__":
    unittest.main()

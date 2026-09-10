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


class SearchTermImpressionSharePolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_shared_impression_share_reference_exists(self):
        self.assertTrue(
            (ROOT / "references/search-term-impression-share.md").is_file(),
            "query growth decisions need a shared impression-share evidence policy",
        )

    def test_search_term_skill_routes_share_of_voice_analysis_to_shared_reference(self):
        text = self.read("skills/search-term-analysis/SKILL.md")
        self.assertIn("search-term-impression-share.md", text)
        self.assertIn("impression share", text.lower())

    def test_growth_skill_routes_query_headroom_to_impression_share_policy(self):
        text = self.read("skills/growth-opportunity-finder/SKILL.md")
        self.assertIn("search-term-impression-share.md", text)


class SkillEffectivenessPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_effectiveness_guide_exists(self):
        self.assertTrue(
            (ROOT / "evals/SKILL-EFFECTIVENESS.md").is_file(),
            "repository needs a repeatable with-skill vs without-skill effectiveness protocol",
        )

    def test_eval_index_distinguishes_capability_replay_from_effectiveness_measurement(self):
        text = self.read("evals/README.md")
        self.assertIn("with-skill", text)
        self.assertIn("without-skill", text)
        self.assertIn("negative control", text)
        self.assertIn("repeated", text)

    def test_effectiveness_guide_covers_discovery_and_forced_invocation(self):
        text = self.read("evals/SKILL-EFFECTIVENESS.md")
        self.assertIn("Discovery", text)
        self.assertIn("Forced invocation", text)
        self.assertIn("without-skill", text)
        self.assertIn("pass@k", text)


if __name__ == "__main__":
    unittest.main()

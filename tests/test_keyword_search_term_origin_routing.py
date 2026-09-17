import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class KeywordSearchTermOriginRoutingTests(unittest.TestCase):
    def read_keyword_skill(self) -> str:
        return (ROOT / "skills/keyword-optimization/SKILL.md").read_text(encoding="utf-8")

    def test_keyword_skill_routes_search_term_interpretation_to_search_term_analysis(self):
        text = self.read_keyword_skill()
        self.assertIn("search-term-analysis", text)
        self.assertIn("term_origin", text)
        self.assertIn("literal_query", text)

    def test_harvest_to_exact_requires_literal_query_evidence(self):
        text = self.read_keyword_skill()
        self.assertIn("harvest_to_exact", text)
        self.assertIn("inferred_non_search", text)
        self.assertIn("unknown", text)
        self.assertIn("Manual Review", text)
        self.assertIn("displayed string", text)

    def test_keyword_structure_work_can_continue_without_literal_query_assumption(self):
        text = self.read_keyword_skill()
        self.assertIn("configured keyword/target", text.lower())
        self.assertIn("does not require treating the displayed Search Term string as a literal shopper query", text)

    def test_negative_and_bid_actions_remain_delegated(self):
        text = self.read_keyword_skill()
        self.assertIn("negative-targeting", text)
        self.assertIn("bid-optimization", text)


if __name__ == "__main__":
    unittest.main()

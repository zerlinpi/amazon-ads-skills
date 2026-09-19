from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references" / "search-term-impression-share.md"
RESEARCH = ROOT / "docs" / "research" / "search-term-impression-share-headroom.md"


class ImpressionShareMetricSemanticsTest(unittest.TestCase):
    def test_search_term_share_is_not_defined_with_top_of_search_eligibility_denominator(self):
        text = REFERENCE.read_text(encoding="utf-8").lower()
        self.assertNotIn(
            "search term impression share as the account-level share of eligible ad impressions",
            text,
        )
        self.assertIn("top-of-search impression share", text)
        self.assertIn("different metric", text)
        self.assertIn("eligible", text)

    def test_research_records_denominator_distinction(self):
        text = RESEARCH.read_text(encoding="utf-8").lower()
        self.assertIn("top-of-search impression share", text)
        self.assertIn("eligible", text)
        self.assertIn("do not transfer", text)


if __name__ == "__main__":
    unittest.main()

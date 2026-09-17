import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def frontmatter_description(relative_path: str) -> str:
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing description in {relative_path}")
    return match.group(1).strip()


class SearchNegativeKeywordDiscoveryTests(unittest.TestCase):
    def test_search_term_description_declares_analysis_boundary(self):
        description = frontmatter_description("skills/search-term-analysis/SKILL.md")
        self.assertIn("negative-targeting", description)
        self.assertIn("keyword-optimization", description)
        self.assertIn("Search Term", description)

    def test_negative_targeting_description_declares_action_boundary(self):
        description = frontmatter_description("skills/negative-targeting/SKILL.md")
        self.assertIn("action-safe", description)
        self.assertIn("search-term-analysis", description)
        self.assertIn("negative", description.lower())

    def test_keyword_description_declares_configured_entity_boundary(self):
        description = frontmatter_description("skills/keyword-optimization/SKILL.md")
        self.assertIn("configured keyword/target", description)
        self.assertIn("search-term-analysis", description)
        self.assertIn("negative-targeting", description)

    def test_orchestrator_routes_by_primary_intent(self):
        text = (ROOT / "skills/amazon-ads-optimizer/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Primary intent: interpret Search Term rows", text)
        self.assertIn("Primary intent: choose negative type/scope", text)
        self.assertIn("Primary intent: govern configured keyword/target lifecycle", text)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references/platform-capability-lineage.md"


class PlatformCapabilityLineageTests(unittest.TestCase):
    def test_shared_reference_exists_and_defines_versioned_capability_identity(self):
        self.assertTrue(REFERENCE.exists(), "missing platform capability lineage reference")
        text = REFERENCE.read_text(encoding="utf-8")
        for field in (
            "source_kind",
            "published_or_updated_at",
            "retrieved_at",
            "capability_scope",
            "conflict_status",
        ):
            self.assertIn(field, text)

    def test_conflicting_official_sources_fail_closed_for_exact_platform_rules(self):
        self.assertTrue(REFERENCE.exists(), "missing platform capability lineage reference")
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("Conflicted", text)
        self.assertIn("exact numeric platform rule", text)
        self.assertIn("do not silently choose", text)

    def test_bid_and_placement_skills_load_capability_lineage_when_platform_behavior_matters(self):
        bid = (ROOT / "skills/bid-optimization/SKILL.md").read_text(encoding="utf-8")
        placement = (ROOT / "skills/placement-optimization/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("platform-capability-lineage.md", bid)
        self.assertIn("platform-capability-lineage.md", placement)

    def test_search_term_report_coverage_bounds_official_history_without_zero_filling(self):
        skill = (ROOT / "skills/search-term-analysis/SKILL.md").read_text(encoding="utf-8")
        coverage = (ROOT / "references/report-coverage.md").read_text(encoding="utf-8")
        self.assertIn("report-coverage.md", skill)
        self.assertIn("65", coverage)
        self.assertIn("historical-availability", coverage)
        self.assertIn("alternate source", coverage.lower())
        self.assertIn("missing older", coverage.lower())
        self.assertIn("zero", coverage.lower())
        self.assertIn("platform-capability-lineage.md", coverage)

    def test_repository_safety_rules_cover_platform_capability_conflicts(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("platform-capability-lineage.md", agents)
        self.assertIn("time-varying platform capability", agents)


if __name__ == "__main__":
    unittest.main()

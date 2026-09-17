import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def frontmatter_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^description:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        raise AssertionError(f"missing top-level description: {path}")
    return match.group(1).strip()


class MonitoringDiscoveryRoutingTests(unittest.TestCase):
    def test_campaign_health_description_is_bilingual_and_routine_scoped(self):
        desc = frontmatter_description(ROOT / "skills/campaign-health-monitor/SKILL.md")
        lower = desc.lower()
        self.assertRegex(desc, r"[\u4e00-\u9fff]")
        self.assertIn("routine campaign health", lower)
        self.assertIn("status", lower)
        self.assertNotIn("causal diagnosis", lower)

    def test_anomaly_description_is_bilingual_and_signal_scoped(self):
        desc = frontmatter_description(ROOT / "skills/anomaly-detection/SKILL.md")
        lower = desc.lower()
        self.assertRegex(desc, r"[\u4e00-\u9fff]")
        self.assertIn("unexplained anomaly", lower)
        self.assertIn("alert", lower)
        self.assertNotIn("causal diagnosis", lower)

    def test_optimizer_defines_monitoring_escalation_ladder(self):
        text = (ROOT / "skills/amazon-ads-optimizer/SKILL.md").read_text(encoding="utf-8")
        required = (
            "Routine status scan → `campaign-health-monitor`",
            "Unexpected signal / alert triage → `anomaly-detection`",
            "Sustained business-impact decline + causal question → `performance-drop-diagnosis`",
            "Do not load all three by default",
        )
        for phrase in required:
            self.assertIn(phrase, text)

    def test_campaign_health_hands_growth_decisions_to_growth_skill(self):
        text = (ROOT / "skills/campaign-health-monitor/SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("Healthy but scalable campaigns", text)
        self.assertIn("growth-opportunity-finder", text)

    def test_anomaly_hands_sustained_causal_diagnosis_to_drop_skill(self):
        text = (ROOT / "skills/anomaly-detection/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("performance-drop-diagnosis", text)
        self.assertIn("sustained", text.lower())


if __name__ == "__main__":
    unittest.main()

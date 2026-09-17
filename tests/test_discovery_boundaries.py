import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MonitoringDiscoveryBoundaryTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8").lower()

    def test_optimizer_distinguishes_campaign_health_from_anomaly_detection(self):
        text = self.read("skills/amazon-ads-optimizer/SKILL.md")
        self.assertIn("campaign-health-monitor", text)
        self.assertIn("anomaly-detection", text)
        self.assertIn("portfolio", text)
        self.assertIn("single signal", text)
        self.assertIn("classification", text)

    def test_optimizer_distinguishes_anomaly_detection_from_drop_diagnosis(self):
        text = self.read("skills/amazon-ads-optimizer/SKILL.md")
        self.assertIn("sustained business-impact decline", text)
        self.assertIn("unexplained deviation", text)
        self.assertIn("causal diagnosis", text)

    def test_monitoring_routes_do_not_authorize_live_mutation(self):
        text = self.read("skills/amazon-ads-optimizer/SKILL.md")
        self.assertIn("never claim a live change succeeded", text)
        self.assertIn("external connector/executor", text)


if __name__ == "__main__":
    unittest.main()

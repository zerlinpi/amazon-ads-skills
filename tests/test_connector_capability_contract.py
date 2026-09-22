import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/connector-capability-snapshot.json"
REFERENCE = ROOT / "references/connector-capability.md"
DATA_LINEAGE = ROOT / "references/data-lineage.md"


class ConnectorCapabilityContractTests(unittest.TestCase):
    def test_connector_capability_schema_exists_and_has_core_identity(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        props = schema["properties"]
        for field in ("connector_id", "captured_at", "default_access_mode", "capabilities"):
            self.assertIn(field, props)

    def test_capability_contract_distinguishes_support_from_data_values(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        item = schema["properties"]["capabilities"]["items"]
        props = item["properties"]
        for field in (
            "capability_id",
            "status",
            "access_mode",
            "source_system",
            "acquisition_channel",
            "scope",
            "data_contract",
            "error_contract",
            "evidence",
        ):
            self.assertIn(field, props)
        status_enum = props["status"]["enum"]
        for value in ("Supported", "Partial", "Unsupported", "Unknown"):
            self.assertIn(value, status_enum)

    def test_capability_contract_exposes_verifiable_connector_surface_bindings(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        props = schema["properties"]["capabilities"]["items"]["properties"]
        self.assertIn("bindings", props)
        binding = props["bindings"]["items"]
        binding_props = binding["properties"]
        for field in (
            "binding_id",
            "surface_type",
            "surface_id",
            "surface_version",
            "verification_status",
            "observed_at",
            "scope",
            "evidence",
        ):
            self.assertIn(field, binding_props)
        self.assertIn("Verified", binding_props["verification_status"]["enum"])
        self.assertIn("Unverified", binding_props["verification_status"]["enum"])
        self.assertIn("Unknown", binding_props["verification_status"]["enum"])

    def test_data_contract_exposes_decision_critical_reporting_boundaries(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        data_props = schema["properties"]["capabilities"]["items"]["properties"]["data_contract"]["properties"]
        for field in (
            "reporting_generation",
            "report_lifecycle",
            "pagination",
            "truncation_signal_exposed",
            "row_eligibility_exposed",
            "historical_availability_exposed",
            "historical_availability_status",
            "historical_windows",
            "freshness_exposed",
            "available_through_exposed",
            "metric_semantics_exposed",
            "date_attribution_semantics_exposed",
        ):
            self.assertIn(field, data_props)

    def test_mcp_tool_annotations_are_advisory_not_authorization(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        annotations = schema["properties"]["capabilities"]["items"]["properties"]["tool_annotations"]["properties"]
        for field in ("readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint"):
            self.assertIn(field, annotations)
        text = REFERENCE.read_text(encoding="utf-8").lower()
        self.assertIn("advisory", text)
        self.assertIn("not authorization", text)

    def test_connector_content_is_data_not_agent_instruction(self):
        text = REFERENCE.read_text(encoding="utf-8").lower()
        for concept in (
            "prompt injection",
            "untrusted content",
            "data, not instructions",
            "campaign names",
            "search terms",
            "tool output",
            "do not follow",
            "external url",
        ):
            self.assertIn(concept, text)
        self.assertIn("read-only / suggest / shadow", text)
        self.assertIn("external connector / executor", text)

    def test_data_lineage_routes_connector_gaps_through_capability_contract(self):
        text = DATA_LINEAGE.read_text(encoding="utf-8")
        self.assertIn("connector-capability.md", text)
        self.assertIn("connector-capability-snapshot.json", text)


if __name__ == "__main__":
    unittest.main()

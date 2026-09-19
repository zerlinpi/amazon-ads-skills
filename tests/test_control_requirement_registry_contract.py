import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ControlRequirementRegistryContractTests(unittest.TestCase):
    def test_every_registry_control_type_is_schema_valid(self):
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        allowed = set(schema["$defs"]["controlType"]["enum"])

        for surface_name, surface in registry["decision_surfaces"].items():
            required = set(surface["required_control_types"])
            invalid = required - allowed
            self.assertFalse(
                invalid,
                f"{surface_name} contains control types outside schemas/control-state-snapshot.json: {sorted(invalid)}",
            )


if __name__ == "__main__":
    unittest.main()

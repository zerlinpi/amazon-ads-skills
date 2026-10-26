"""RED-first: Ready combined readouts require resolved primary and guardrail identities.

Synthetic plans only; this validator never accesses or mutates Amazon Ads.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_experiment_combined_ratio_aggregation import combined_metric


def ready_combined(name, *, guardrail=False, aggregation="additive", status="Ready"):
    # Build a valid synthetic plan before inserting malformed identities. The
    # shared fixture helper intentionally expects string metric names.
    seed = name if isinstance(name, str) else "Impressions"
    plan = combined_metric(
        seed, aggregation=aggregation, guardrail=guardrail, status=status
    )
    if not isinstance(name, str):
        if guardrail:
            plan["guardrails"][0]["metric"] = name
        else:
            plan["primary_metric"]["name"] = name
    return plan


class ReadyCombinedMetricIdentityTests(unittest.TestCase):
    def assert_identity_unresolved(self, name, *, guardrail=False, aggregation="additive"):
        errors = validate_experiment_plan(
            ready_combined(name, guardrail=guardrail, aggregation=aggregation)
        )
        self.assertTrue(
            any("metric" in error and "identity" in error for error in errors),
            f"{name!r}, guardrail={guardrail}: {errors}",
        )

    def test_unknown_primary(self):
        self.assert_identity_unresolved("Unknown")

    def test_partial_primary(self):
        self.assert_identity_unresolved("Partial")

    def test_missing_primary(self):
        self.assert_identity_unresolved("Missing")

    def test_unsupported_primary(self):
        self.assert_identity_unresolved("Unsupported")

    def test_unavailable_primary(self):
        self.assert_identity_unresolved("Unavailable")

    def test_not_available_primary(self):
        self.assert_identity_unresolved("Not Available")

    def test_not_supported_primary(self):
        self.assert_identity_unresolved("not_supported")

    def test_not_applicable_primary(self):
        self.assert_identity_unresolved("Not Applicable")

    def test_na_primary(self):
        self.assert_identity_unresolved("N/A")

    def test_blank_primary(self):
        self.assert_identity_unresolved("  ")

    def test_explicit_null_primary(self):
        self.assert_identity_unresolved(None)

    def test_numeric_primary(self):
        self.assert_identity_unresolved(0)

    def test_unknown_guardrail(self):
        self.assert_identity_unresolved("Unknown", guardrail=True)

    def test_partial_guardrail(self):
        self.assert_identity_unresolved("Partial", guardrail=True)

    def test_missing_guardrail_with_ratio_semantics(self):
        self.assert_identity_unresolved(
            "Missing", guardrail=True, aggregation="ratio_or_derived"
        )

    def test_concrete_impressions_additive_remains_ready(self):
        self.assertEqual([], validate_experiment_plan(ready_combined("Impressions")))

    def test_concrete_name_containing_unknown_word_remains_ready(self):
        self.assertEqual([], validate_experiment_plan(ready_combined("Unknown SKU clicks")))

    def test_valid_roas_ratio_semantics_remains_ready(self):
        self.assertEqual([], validate_experiment_plan(
            ready_combined("ROAS", aggregation="ratio_or_derived")
        ))

    def test_non_combined_ready_keeps_legacy_identity_contract(self):
        plan = ready_combined("Unknown")
        plan["comparison"]["requires_combined_readout"] = False
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_combined_preserves_unresolved_identity(self):
        self.assertEqual([], validate_experiment_plan(
            ready_combined("Unknown", status="Shadow Only")
        ))


if __name__ == "__main__":
    unittest.main()

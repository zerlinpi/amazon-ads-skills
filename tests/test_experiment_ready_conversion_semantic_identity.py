"""RED-first: conversion metric identity cannot be bypassed by misleading family labels.

All evidence is synthetic. No live Amazon Ads access or account mutation.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def conversion_primary(**updates):
    plan = base_plan()
    plan["primary_metric"] = {
        "name": "Purchases",
        "success_rule": "increase",
        "metric_semantics": {
            "metric_family": "conversion",
            "attribution_family": "standard",
            "semantic_version": "store-attribution-2026-01-01",
        },
    }
    plan["primary_metric"]["metric_semantics"].update(updates)
    return plan


def conversion_guardrail(**updates):
    plan = base_plan()
    plan["guardrails"] = [{
        "metric": "ROAS",
        "rule": "remain above a declared floor",
        "metric_semantics": {
            "metric_family": "conversion",
            "attribution_family": "standard",
            "semantic_version": "store-attribution-2026-01-01",
        },
    }]
    plan["guardrails"][0]["metric_semantics"].update(updates)
    return plan


class ReadyConversionSemanticIdentityTests(unittest.TestCase):
    def assert_rejected(self, plan, expected):
        errors = validate_experiment_plan(plan)
        self.assertTrue(errors, "unresolved conversion identity must not be Ready")
        self.assertIn(expected, " | ".join(errors), errors)

    def test_primary_purchases_cannot_claim_traffic_family(self):
        self.assert_rejected(conversion_primary(metric_family="traffic"), "metric_family")

    def test_primary_purchases_cannot_claim_unknown_family(self):
        self.assert_rejected(conversion_primary(metric_family="Unknown"), "metric_family")

    def test_primary_purchases_cannot_claim_blank_family(self):
        self.assert_rejected(conversion_primary(metric_family=" "), "metric_family")

    def test_primary_purchases_cannot_claim_unknown_attribution(self):
        self.assert_rejected(conversion_primary(attribution_family="Unknown"), "attribution_family")

    def test_primary_purchases_cannot_claim_not_supported_version(self):
        self.assert_rejected(conversion_primary(semantic_version="Not Supported"), "semantic_version")

    def test_primary_purchases_cannot_claim_not_applicable_attribution(self):
        self.assert_rejected(conversion_primary(attribution_family="not_applicable"), "attribution_family")

    def test_guardrail_roas_cannot_claim_traffic_family(self):
        self.assert_rejected(conversion_guardrail(metric_family="traffic"), "metric_family")

    def test_guardrail_roas_cannot_claim_partial_attribution(self):
        self.assert_rejected(conversion_guardrail(attribution_family="Partial"), "attribution_family")

    def test_guardrail_roas_cannot_claim_missing_version(self):
        self.assert_rejected(conversion_guardrail(semantic_version="Missing"), "semantic_version")

    def test_primary_valid_conversion_identity_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(conversion_primary()))

    def test_guardrail_valid_conversion_identity_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(conversion_guardrail()))

    def test_nonconversion_reach_can_keep_its_own_family(self):
        plan = base_plan()
        plan["primary_metric"] = {
            "name": "Reach",
            "success_rule": "increase",
            "metric_semantics": {
                "metric_family": "reach",
                "attribution_family": "not_applicable",
                "semantic_version": "reach-v1",
            },
        }
        self.assertEqual([], validate_experiment_plan(plan))

    def test_opaque_version_containing_unknown_substring_remains_valid(self):
        self.assertEqual([], validate_experiment_plan(
            conversion_primary(semantic_version="store-unknownvariant-v2")
        ))

    def test_shadow_preserves_unresolved_conversion_identity(self):
        plan = conversion_primary(metric_family="Unknown", attribution_family="Missing")
        plan["status"] = "Shadow Only"
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()

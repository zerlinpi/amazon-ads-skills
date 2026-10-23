#!/usr/bin/env python3
"""Read-only Global SP receipt-to-marketplace-readback evidence gate.

This consumes a connector-normalized *single-item* Global Sponsored Products
campaign update and subsequent query evidence. It never sends Ads API requests,
retries writes, or infers effective state from delivery status.
"""
from __future__ import annotations

import json
import re
import sys
from decimal import Decimal
from typing import Any

from scripts.compare_control_state import _rfc3339_instant

STATES = {"ENABLED", "PAUSED", "ARCHIVED"}


def _result(status: str, reason: str, mismatched: list[str] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"application_status": status, "reasons": [reason]}
    if mismatched is not None:
        result["mismatched_marketplaces"] = mismatched
    return result


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _monetary_amount(value: Any) -> Decimal | None:
    """Require a finite, nonnegative plain decimal *string*, never a JSON float.

    The trusted adapter must preserve source precision when normalizing API
    numeric values. No FX conversion or inferred missing/zero budget occurs here.
    """
    if not isinstance(value, str) or re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value) is None:
        return None
    return Decimal(value)


def evaluate_global_sp_readback(evidence: Any) -> dict[str, Any]:
    """Classify one Global SP campaign update without equating HTTP 207 to application.

    Caller must normalize each marketplace's *configured effective state* from
    source-supported Global SP query fields and explicit overrides. This gate
    does not accept deliveryStatus as a substitute for configured state.
    """
    unknown = lambda message: _result("Unknown", message)
    if not isinstance(evidence, dict):
        return unknown("application evidence must be an object")
    request, receipt = evidence.get("request"), evidence.get("receipt")
    if not isinstance(request, dict) or not isinstance(receipt, dict):
        return unknown("request and HTTP receipt must be objects")

    for key in ("global_account_id", "campaign_id"):
        if not _nonempty(request.get(key)):
            return unknown(f"request missing {key}")
    markets = request.get("marketplaces")
    expected = request.get("expected_effective_states")
    if (not isinstance(markets, list) or not markets
            or any(not _nonempty(m) for m in markets)
            or len(set(markets)) != len(markets)):
        return unknown("request marketplaces must be nonempty, distinct identifiers")
    if (not isinstance(expected, dict) or set(expected) != set(markets)
            or any(not isinstance(value, str) or value not in STATES for value in expected.values())):
        return unknown("expected effective states must cover every requested marketplace")
    completed = _rfc3339_instant(request.get("completed_at"))
    if completed is None:
        return unknown("request completed_at is not a verified instant")

    if type(receipt.get("http_status")) is not int or receipt["http_status"] != 207:
        return unknown("HTTP response is not a verified Global SP 207 multi-status receipt")
    receipt_indices: list[int] = []
    for group in ("success", "error", "partialSuccess"):
        entries = receipt.get(group)
        if not isinstance(entries, list):
            return unknown(f"receipt {group} array is missing")
        for entry in entries:
            if (not isinstance(entry, dict)
                    or type(entry.get("index")) is not int):
                return unknown(f"receipt {group} has invalid request index")
            receipt_indices.append(entry["index"])
    # Explicitly single-item. Never interpret a subset of a multi-item batch
    # as complete application of the whole batch.
    if receipt_indices != [0]:
        return unknown("receipt indices do not uniquely cover one request item")
    if receipt.get("error") or receipt.get("partialSuccess"):
        return _result("Partial", "Global SP 207 contains error or partialSuccess; application is not fully confirmed")
    if len(receipt["success"]) != 1:
        return unknown("Global SP receipt lacks an unambiguous success for request index 0")

    readback = evidence.get("readback")
    if not isinstance(readback, dict):
        return unknown("successful receipt is not post-write readback")
    for key in ("global_account_id", "campaign_id"):
        if not _nonempty(readback.get(key)) or readback[key] != request[key]:
            return unknown(f"readback {key} identity is missing or mismatched")
    source = readback.get("source")
    if (not isinstance(source, dict)
            or any(not _nonempty(source.get(k)) for k in
                   ("source_system", "acquisition_channel", "connector_id"))):
        return unknown("readback source and connector lineage are unverified")
    observed = _rfc3339_instant(readback.get("observed_at"))
    if observed is None or observed <= completed:
        return unknown("readback must be observed after request completion")
    for field, required in (("coverage_status", "Complete"),
                            ("pagination_status", "Complete"),
                            ("capability_status", "Supported")):
        if readback.get(field) != required:
            return unknown(f"readback {field} is not {required}")

    rows = readback.get("marketplace_states")
    if not isinstance(rows, list):
        return unknown("readback marketplace_states must be an explicit list")
    actual: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict) or not _nonempty(row.get("marketplace")):
            return unknown("readback has an invalid marketplace identity")
        market = row["marketplace"]
        if market in actual:
            return unknown(f"readback duplicate marketplace: {market}")
        if row.get("evidence_status") != "observed":
            return unknown(f"readback {market} effective state is not observed")
        state = row.get("effective_state")
        if not isinstance(state, str) or state not in STATES:
            return unknown(f"readback {market} effective configured state is missing or unsupported")
        actual[market] = state
    if set(actual) != set(markets):
        return unknown("readback marketplace coverage differs from requested marketplace scope")

    budget_mismatched: set[str] = set()
    # Optional, independently evidenced monetary-budget comparison. A state
    # readback capability is NOT proof of budget visibility or completeness.
    if "expected_marketplace_budgets" in request:
        expected_budgets = request["expected_marketplace_budgets"]
        if not isinstance(expected_budgets, dict) or set(expected_budgets) != set(markets):
            return unknown("expected monetary budgets must cover every requested marketplace")
        for market, budget in expected_budgets.items():
            if (not isinstance(budget, dict)
                    or not isinstance(budget.get("currency_code"), str)
                    or re.fullmatch(r"[A-Z]{3}", budget["currency_code"]) is None
                    or budget.get("budget_type") != "MONETARY"
                    or budget.get("recurrence") != "DAILY"
                    or _monetary_amount(budget.get("amount")) is None):
                return unknown(f"request {market} monetary budget identity or amount is unsupported")
        for field, required in (("budget_coverage_status", "Complete"),
                                ("budget_pagination_status", "Complete"),
                                ("budget_capability_status", "Supported")):
            if readback.get(field) != required:
                return unknown(f"readback {field} is not {required}")
        budget_rows = readback.get("marketplace_budgets")
        if not isinstance(budget_rows, list):
            return unknown("readback marketplace_budgets must be an explicit list")
        actual_budgets: dict[str, dict[str, Any]] = {}
        for row in budget_rows:
            if not isinstance(row, dict) or not _nonempty(row.get("marketplace")):
                return unknown("readback has an invalid budget marketplace identity")
            market = row["marketplace"]
            if market in actual_budgets:
                return unknown(f"readback duplicate budget marketplace: {market}")
            if row.get("evidence_status") != "observed":
                return unknown(f"readback {market} monetary budget is not observed")
            if (not isinstance(row.get("currency_code"), str)
                    or re.fullmatch(r"[A-Z]{3}", row["currency_code"]) is None
                    or not _nonempty(row.get("budget_type"))
                    or not _nonempty(row.get("recurrence"))
                    or _monetary_amount(row.get("amount")) is None):
                return unknown(f"readback {market} monetary budget identity or amount is unverified")
            actual_budgets[market] = row
        if set(actual_budgets) != set(markets):
            return unknown("readback monetary budget coverage differs from requested marketplace scope")
        for market in markets:
            desired, observed_budget = expected_budgets[market], actual_budgets[market]
            if (desired["currency_code"] != observed_budget["currency_code"]
                    or desired["budget_type"] != observed_budget["budget_type"]
                    or desired["recurrence"] != observed_budget["recurrence"]
                    or _monetary_amount(desired["amount"]) != _monetary_amount(observed_budget["amount"])):
                budget_mismatched.add(market)

    mismatched = sorted({m for m in markets if actual[m] != expected[m]} | budget_mismatched)
    if mismatched:
        if budget_mismatched:
            return _result("Drifted", "observed marketplace configured state or monetary budget differs from intended state", mismatched)
        return _result("Drifted", "observed marketplace configured state differs from intended state", mismatched)
    if "expected_marketplace_budgets" in request:
        return _result("Confirmed", "complete per-marketplace configured-state and monetary-budget readback agree")
    return _result("Confirmed", "single-item 207 success and complete post-write marketplace configured-state readback agree")


def main() -> None:
    evidence = json.load(sys.stdin)
    print(json.dumps(evaluate_global_sp_readback(evidence), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

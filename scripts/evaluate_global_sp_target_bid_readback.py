#!/usr/bin/env python3
"""Read-only Global SP single-marketplace positive-target bid receipt/readback gate.

Consumes normalized evidence from a trusted external Executor/adapter.
No Amazon Ads API calls, writes, retries, FX or batch reconciliation.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any

from scripts.compare_control_state import _rfc3339_instant
from scripts.evaluate_global_sp_readback import (
    SUPPORTED_GLOBAL_SP_MARKETPLACES, _monetary_amount, _nonempty, _result,
)

_IDENTITIES = ("request_id", "global_account_id", "campaign_id", "ad_group_id", "target_id")
_RESOURCE_IDENTITIES = ("global_account_id", "campaign_id", "ad_group_id", "target_id")
_SOURCE_FIELDS = ("source_system", "acquisition_channel", "connector_id")
_SUPPORTED_TARGET_TYPES = {"KEYWORD", "PRODUCT"}


def evaluate_global_sp_target_bid_readback(evidence: Any) -> dict[str, Any]:
    """Classify a *configured target bid*, never an ad-group default/auction bid."""
    unknown = lambda reason: _result("Unknown", reason)
    if not isinstance(evidence, dict):
        return unknown("application evidence must be an object")
    request, receipt = evidence.get("request"), evidence.get("receipt")
    if not isinstance(request, dict) or not isinstance(receipt, dict):
        return unknown("request and receipt must be objects")

    if request.get("resource_type") != "target":
        return unknown("request resource type is not target")
    for key in _IDENTITIES:
        if not _nonempty(request.get(key)):
            return unknown(f"request missing {key}")
    market = request.get("marketplace")
    if not isinstance(market, str) or market not in SUPPORTED_GLOBAL_SP_MARKETPLACES:
        return unknown("target request requires one supported Global SP country-code marketplace")
    if (not isinstance(request.get("target_type"), str)
            or request["target_type"] not in _SUPPORTED_TARGET_TYPES):
        return unknown("only positive KEYWORD and PRODUCT target bids are supported")
    if request.get("negative") is not False:
        return unknown("negative or unverified target type cannot have a confirmed bid")
    expected = request.get("expected_target_bid")
    if (not isinstance(expected, dict)
            or not isinstance(expected.get("currency_code"), str)
            or re.fullmatch(r"[A-Z]{3}", expected["currency_code"]) is None
            or _monetary_amount(expected.get("amount")) is None):
        return unknown("expected target bid requires native currency and finite nonnegative decimal")
    completed = _rfc3339_instant(request.get("completed_at"))
    if completed is None:
        return unknown("request completion time is not a verified instant")

    if receipt.get("resource_type") != "target":
        return unknown("receipt is not a target update")
    for key in _IDENTITIES:
        if receipt.get(key) != request[key]:
            return unknown(f"receipt {key} does not bind to the target request")
    if type(receipt.get("http_status")) is not int or receipt["http_status"] != 207:
        return unknown("receipt is not a Global SP 207 multi-status response")
    indices: list[int] = []
    for group in ("success", "error", "partialSuccess"):
        entries = receipt.get(group)
        if not isinstance(entries, list):
            return unknown(f"receipt {group} must be an explicit array")
        for entry in entries:
            if not isinstance(entry, dict) or type(entry.get("index")) is not int:
                return unknown(f"receipt {group} has invalid request index")
            indices.append(entry["index"])
    if indices != [0]:
        return unknown("receipt does not uniquely cover one target request item")
    if receipt["error"] or receipt["partialSuccess"]:
        return _result("Partial", "target update has an error or partialSuccess 207 item")
    if len(receipt["success"]) != 1:
        return unknown("target receipt lacks an unambiguous success")
    returned = receipt["success"][0].get("target")
    if returned is not None:
        if not isinstance(returned, dict):
            return unknown("receipt target resource is malformed")
        for key in _RESOURCE_IDENTITIES:
            if key in returned and returned[key] != request[key]:
                return unknown(f"receipt target {key} contradicts request")
        if "target_type" in returned and returned["target_type"] != request["target_type"]:
            return unknown("receipt target type contradicts request")
        if "negative" in returned and returned["negative"] is not False:
            return unknown("receipt target negative status contradicts request")
        if "marketplace" in returned and returned["marketplace"] != market:
            return unknown("receipt target marketplace contradicts request")
        if "marketplaces" in returned and returned["marketplaces"] != [market]:
            return unknown("receipt target marketplace scope contradicts request")

    unsupported = sorted(
        key for key in request if key.startswith("expected_") and key != "expected_target_bid"
    )
    if unsupported:
        return unknown("unverified target request intent: " + ", ".join(unsupported))

    readback = evidence.get("readback")
    if not isinstance(readback, dict) or readback.get("resource_type") != "target":
        return unknown("independent target query readback is missing")
    for key in _RESOURCE_IDENTITIES:
        if readback.get(key) != request[key]:
            return unknown(f"readback {key} identity is missing or mismatched")
    if readback.get("marketplace") != market:
        return unknown("target query marketplace identity is missing or mismatched")
    if readback.get("target_type") != request["target_type"] or readback.get("negative") is not False:
        return unknown("target query type or positive/negative status is unverified")
    source = readback.get("source")
    if (not isinstance(source, dict)
            or any(not _nonempty(source.get(k)) for k in _SOURCE_FIELDS)):
        return unknown("target query source and connector lineage are unverified")
    observed = _rfc3339_instant(readback.get("observed_at"))
    if observed is None or observed <= completed:
        return unknown("target query must be observed after request completion")
    for field, required in (("coverage_status", "Complete"),
                            ("pagination_status", "Complete"),
                            ("capability_status", "Supported")):
        if readback.get(field) != required:
            return unknown(f"target query {field} is not {required}")

    bid = readback.get("target_bid")
    if not isinstance(bid, dict) or bid.get("marketplace") != market:
        return unknown("target bid marketplace is missing or mismatched")
    if bid.get("evidence_status") != "observed":
        return unknown("target bid is not independently observed")
    for identity in _RESOURCE_IDENTITIES:
        if identity in bid and bid[identity] != request[identity]:
            return unknown(f"target bid row {identity} contradicts request")
    if "target_type" in bid and bid["target_type"] != request["target_type"]:
        return unknown("target bid row type contradicts request")
    if "negative" in bid and bid["negative"] is not False:
        return unknown("target bid row negative status contradicts request")
    if "source" in bid:
        row_source = bid["source"]
        if (not isinstance(row_source, dict)
                or any(row_source.get(key) != source[key] for key in _SOURCE_FIELDS)):
            return unknown("target bid row source contradicts query envelope")
    if "observed_at" in bid:
        row_observed = _rfc3339_instant(bid["observed_at"])
        if row_observed is None or row_observed <= completed or row_observed > observed:
            return unknown("target bid row observation time is inconsistent")
    if (not isinstance(bid.get("currency_code"), str)
            or re.fullmatch(r"[A-Z]{3}", bid["currency_code"]) is None
            or _monetary_amount(bid.get("amount")) is None):
        return unknown("target bid amount or currency is unverified")
    if (bid["currency_code"] != expected["currency_code"]
            or _monetary_amount(bid["amount"]) != _monetary_amount(expected["amount"])):
        return _result("Drifted", "observed native-currency target bid differs from intended value", [market])
    return _result("Confirmed", "single-target 207 success and independent complete configured target bid agree")


def main() -> None:
    print(json.dumps(evaluate_global_sp_target_bid_readback(json.load(sys.stdin)),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

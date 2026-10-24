#!/usr/bin/env python3
"""Read-only Global SP single-ad-group default-bid receipt/readback gate.

This is a separate resource contract from the campaign state/budget evaluator.
All input is connector-normalized evidence supplied by a trusted, external
authorized Executor/adapter. No Ads calls, writes, retries or reconciliation.
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


def evaluate_global_sp_adgroup_bid_readback(evidence: Any) -> dict[str, Any]:
    unknown = lambda reason: _result("Unknown", reason)
    if not isinstance(evidence, dict):
        return unknown("application evidence must be an object")
    request, receipt = evidence.get("request"), evidence.get("receipt")
    if not isinstance(request, dict) or not isinstance(receipt, dict):
        return unknown("request and receipt must be objects")

    # An ad-group receipt must not be confused with a campaign/target receipt.
    if request.get("resource_type") != "ad_group":
        return unknown("request resource type is not ad_group")
    for key in ("request_id", "global_account_id", "campaign_id", "ad_group_id"):
        if not _nonempty(request.get(key)):
            return unknown(f"request missing {key}")
    markets = request.get("marketplaces")
    if (not isinstance(markets, list) or not markets
            or any(not isinstance(m, str) or m not in SUPPORTED_GLOBAL_SP_MARKETPLACES
                   for m in markets)
            or len(set(markets)) != len(markets)):
        return unknown("request marketplaces must be distinct supported Global SP country codes")

    expected = request.get("expected_marketplace_default_bids")
    if not isinstance(expected, dict) or set(expected) != set(markets):
        return unknown("expected default bids must cover exactly the requested marketplaces")
    for market, bid in expected.items():
        if (not isinstance(bid, dict)
                or not isinstance(bid.get("currency_code"), str)
                or re.fullmatch(r"[A-Z]{3}", bid["currency_code"]) is None
                or _monetary_amount(bid.get("amount")) is None):
            return unknown(f"request {market} default bid or currency is invalid")
    completed = _rfc3339_instant(request.get("completed_at"))
    if completed is None:
        return unknown("request completion time is not a verified instant")

    if receipt.get("resource_type") != "ad_group":
        return unknown("receipt resource type does not identify an ad-group update")
    for key in ("request_id", "global_account_id", "campaign_id", "ad_group_id"):
        if receipt.get(key) != request[key]:
            return unknown(f"receipt {key} does not bind to the intended request")
    if type(receipt.get("http_status")) is not int or receipt["http_status"] != 207:
        return unknown("receipt is not a verified Global SP 207 multi-status response")
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
        return unknown("receipt does not uniquely cover one request item")
    if receipt["error"] or receipt["partialSuccess"]:
        return _result("Partial", "ad-group update has an error or partialSuccess 207 item")
    if len(receipt["success"]) != 1:
        return unknown("ad-group receipt lacks an unambiguous success item")
    # Some normalized receipts retain the returned resource. If present, it
    # cannot contradict the bound request. It is not independent query proof.
    returned = receipt["success"][0].get("ad_group")
    if returned is not None:
        if not isinstance(returned, dict):
            return unknown("receipt ad_group resource is malformed")
        for key in ("global_account_id", "campaign_id", "ad_group_id"):
            if key in returned and returned[key] != request[key]:
                return unknown(f"receipt ad_group {key} contradicts request")

    unsupported = sorted(
        key for key in request
        if key.startswith("expected_") and key != "expected_marketplace_default_bids"
    )
    if unsupported:
        return unknown("unverified ad-group request intent: " + ", ".join(unsupported))

    readback = evidence.get("readback")
    if not isinstance(readback, dict) or readback.get("resource_type") != "ad_group":
        return unknown("independent ad-group query readback is missing")
    for key in ("global_account_id", "campaign_id", "ad_group_id"):
        if readback.get(key) != request[key]:
            return unknown(f"readback {key} identity is missing or mismatched")
    source = readback.get("source")
    if (not isinstance(source, dict)
            or any(not _nonempty(source.get(k)) for k in
                   ("source_system", "acquisition_channel", "connector_id"))):
        return unknown("readback source and connector lineage are unverified")
    observed = _rfc3339_instant(readback.get("observed_at"))
    if observed is None or observed <= completed:
        return unknown("ad-group query must be observed after request completion")
    for field, required in (("coverage_status", "Complete"),
                            ("pagination_status", "Complete"),
                            ("capability_status", "Supported")):
        if readback.get(field) != required:
            return unknown(f"ad-group readback {field} is not {required}")

    rows = readback.get("marketplace_default_bids")
    if not isinstance(rows, list):
        return unknown("marketplace default bids require explicit query rows")
    actual: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not _nonempty(row.get("marketplace")):
            return unknown("invalid ad-group bid marketplace identity")
        market = row["marketplace"]
        if market in actual:
            return unknown(f"duplicate ad-group bid marketplace: {market}")
        if row.get("evidence_status") != "observed":
            return unknown(f"ad-group {market} default bid is not observed")
        for identity in ("global_account_id", "campaign_id", "ad_group_id"):
            if identity in row and row[identity] != request[identity]:
                return unknown(f"ad-group {market} {identity} contradicts request")
        if "source" in row:
            row_source = row["source"]
            if (not isinstance(row_source, dict)
                    or any(row_source.get(key) != source[key] for key in
                           ("source_system", "acquisition_channel", "connector_id"))):
                return unknown(f"ad-group {market} source contradicts envelope")
        if "observed_at" in row:
            row_observed = _rfc3339_instant(row["observed_at"])
            if row_observed is None or row_observed <= completed or row_observed > observed:
                return unknown(f"ad-group {market} observation time is inconsistent")
        if (not isinstance(row.get("currency_code"), str)
                or re.fullmatch(r"[A-Z]{3}", row["currency_code"]) is None
                or _monetary_amount(row.get("amount")) is None):
            return unknown(f"ad-group {market} default bid or currency is unverified")
        actual[market] = row
    if set(actual) != set(markets):
        return unknown("ad-group default-bid coverage differs from requested marketplaces")

    mismatched = sorted(
        market for market in markets
        if (expected[market]["currency_code"] != actual[market]["currency_code"]
            or _monetary_amount(expected[market]["amount"])
               != _monetary_amount(actual[market]["amount"]))
    )
    if mismatched:
        return _result("Drifted", "observed marketplace default bids differ from intended values", mismatched)
    return _result("Confirmed", "single-item ad-group 207 success and independent complete marketplace default-bid readback agree")


def main() -> None:
    print(json.dumps(evaluate_global_sp_adgroup_bid_readback(json.load(sys.stdin)),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

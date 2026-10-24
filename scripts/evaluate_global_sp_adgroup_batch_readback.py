#!/usr/bin/env python3
"""Read-only Global SP multi-ad-group default-bid 207 batch evidence gate.

Consumes one externally normalized update call; never calls Ads, writes,
retries, or reconciles an Executor. Every successful indexed item requires
an independent, complete per-marketplace ad-group query readback.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from scripts.evaluate_global_sp_readback import _nonempty, _result
from scripts.evaluate_global_sp_adgroup_bid_readback import (
    evaluate_global_sp_adgroup_bid_readback,
)

_IDENTITIES = ("global_account_id", "campaign_id", "ad_group_id")
_RECEIPT_FIELDS = ("request_id",) + _IDENTITIES + ("resource_type", "marketplaces")


def evaluate_global_sp_adgroup_batch_readback(evidence: Any) -> dict[str, Any]:
    def unknown(reason: str) -> dict[str, Any]:
        return {**_result("Unknown", reason), "items": []}

    if not isinstance(evidence, dict):
        return unknown("batch evidence must be an object")
    if any(isinstance(k, str) and k.startswith("expected_") for k in evidence):
        return unknown("unverified batch-level expected intent")
    requests, receipt, readbacks = (
        evidence.get("requests"), evidence.get("receipt"), evidence.get("readbacks")
    )
    if not isinstance(requests, list) or not requests:
        return unknown("requests must be a nonempty ordered list")
    if not isinstance(receipt, dict) or not isinstance(readbacks, list):
        return unknown("batch receipt and readbacks must be explicit")
    if receipt.get("resource_type") != "ad_group":
        return unknown("batch receipt is not an ad-group update")
    if type(receipt.get("http_status")) is not int or receipt["http_status"] != 207:
        return unknown("batch receipt is not a Global SP 207 response")

    request_ids: set[str] = set()
    adgroup_keys: set[tuple[str, str, str]] = set()
    accounts: set[str] = set()
    for request in requests:
        if not isinstance(request, dict) or request.get("resource_type") != "ad_group":
            return unknown("batch item is not an ad-group request")
        if not _nonempty(request.get("request_id")):
            return unknown("batch request correlation is missing")
        if request["request_id"] in request_ids:
            return unknown("duplicate request_id in batch")
        request_ids.add(request["request_id"])
        if any(not _nonempty(request.get(k)) for k in _IDENTITIES):
            return unknown("batch ad-group identity is missing")
        identity = tuple(request[k] for k in _IDENTITIES)
        if identity in adgroup_keys:
            return unknown("duplicate ad-group identity in batch")
        adgroup_keys.add(identity)
        accounts.add(request["global_account_id"])
    if len(accounts) != 1:
        return unknown("a single Global SP batch must have one global account")
    if "global_account_id" in receipt and (
        not _nonempty(receipt["global_account_id"])
        or receipt["global_account_id"] not in accounts
    ):
        return unknown("batch receipt global account contradicts requests")

    indexed: dict[int, tuple[str, dict[str, Any]]] = {}
    for group in ("success", "error", "partialSuccess"):
        entries = receipt.get(group)
        if not isinstance(entries, list):
            return unknown(f"batch receipt {group} is not an explicit array")
        for entry in entries:
            if not isinstance(entry, dict) or type(entry.get("index")) is not int:
                return unknown(f"batch receipt {group} contains invalid index")
            index = entry["index"]
            if index < 0 or index >= len(requests) or index in indexed:
                return unknown("batch receipt index is duplicate or out of range")
            request = requests[index]
            for field in _RECEIPT_FIELDS:
                if field in entry and entry[field] != request.get(field):
                    return unknown(f"receipt index {index} {field} contradicts request")
            indexed[index] = (group, entry)
    if set(indexed) != set(range(len(requests))):
        return unknown("batch receipt does not cover every request index")

    readback_by_id: dict[str, dict[str, Any]] = {}
    for item in readbacks:
        if not isinstance(item, dict) or not _nonempty(item.get("request_id")):
            return unknown("readback entry lacks request correlation")
        request_id = item["request_id"]
        if request_id in readback_by_id or not isinstance(item.get("readback"), dict):
            return unknown("duplicate or invalid request-correlated readback")
        readback_by_id[request_id] = item["readback"]
    success_ids = {
        requests[i]["request_id"] for i, (group, _) in indexed.items()
        if group == "success"
    }
    if set(readback_by_id) != success_ids:
        return unknown("readbacks must cover exactly the successful request items")

    items: list[dict[str, Any]] = []
    for index, request in enumerate(requests):
        group, entry = indexed[index]
        # Derived only from an already verified real batch index.
        item_receipt: dict[str, Any] = {
            "resource_type": "ad_group", "http_status": 207,
            "success": [], "error": [], "partialSuccess": [],
        }
        for field in ("request_id",) + _IDENTITIES:
            item_receipt[field] = request[field]
        item_entry = dict(entry)
        item_entry["index"] = 0
        item_receipt[group] = [item_entry]
        item_evidence: dict[str, Any] = {"request": request, "receipt": item_receipt}
        if group == "success":
            item_evidence["readback"] = readback_by_id[request["request_id"]]
        verdict = evaluate_global_sp_adgroup_bid_readback(item_evidence)
        items.append({
            "index": index,
            "request_id": request["request_id"],
            "application_status": verdict["application_status"],
            "reasons": verdict["reasons"],
        })

    statuses = {item["application_status"] for item in items}
    if "Unknown" in statuses:
        status = "Unknown"
    elif "Partial" in statuses:
        status = "Partial"
    elif "Drifted" in statuses:
        status = "Drifted"
    else:
        status = "Confirmed"
    return {
        **_result(status, f"{len(requests)} indexed ad-group items independently "
                         "classified; batch is Confirmed only if all are Confirmed"),
        "items": items,
    }


def main() -> None:
    print(json.dumps(evaluate_global_sp_adgroup_batch_readback(json.load(sys.stdin)),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

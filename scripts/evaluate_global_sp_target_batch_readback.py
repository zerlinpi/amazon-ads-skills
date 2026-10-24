#!/usr/bin/env python3
"""Read-only Global SP target-batch 207 index/readback verifier.

Accepts a *trusted, normalized* one-call target-update batch. Reuses the
single-target evidence gate for each successful item. Does not call Ads,
write, retry, reconcile an Executor, or infer auction bids.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from scripts.evaluate_global_sp_readback import _nonempty, _result
from scripts.evaluate_global_sp_target_bid_readback import (
    evaluate_global_sp_target_bid_readback,
)

_IDENTITIES = ("global_account_id", "campaign_id", "ad_group_id", "target_id")
_RECEIPT_FIELDS = _IDENTITIES + (
    "request_id", "resource_type", "marketplace", "target_type", "negative"
)


def evaluate_global_sp_target_batch_readback(evidence: Any) -> dict[str, Any]:
    """Classify all target update items; only full per-item proof can Confirm."""
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
    if receipt.get("resource_type") != "target":
        return unknown("batch receipt is not a target update")
    if type(receipt.get("http_status")) is not int or receipt["http_status"] != 207:
        return unknown("batch receipt is not a Global SP 207 response")

    request_ids: set[str] = set()
    target_keys: set[tuple[str, ...]] = set()
    accounts: set[str] = set()
    for request in requests:
        if not isinstance(request, dict) or request.get("resource_type") != "target":
            return unknown("batch item is not a target request")
        if not _nonempty(request.get("request_id")):
            return unknown("batch request correlation is missing")
        if request["request_id"] in request_ids:
            return unknown("duplicate request_id in batch")
        request_ids.add(request["request_id"])
        if any(not _nonempty(request.get(k)) for k in _IDENTITIES):
            return unknown("batch target identity is missing")
        # Updating one target more than once in one batch makes one readback
        # unable to prove the intermediate state of either update.
        identity = tuple(request[k] for k in _IDENTITIES) + (str(request.get("marketplace")),)
        if identity in target_keys:
            return unknown("duplicate target identity in batch")
        target_keys.add(identity)
        accounts.add(request["global_account_id"])
    if len(accounts) != 1:
        return unknown("a single Global SP batch must have one global account")
    if ("global_account_id" in receipt
            and (not _nonempty(receipt["global_account_id"])
                 or receipt["global_account_id"] not in accounts)):
        return unknown("batch receipt global account contradicts request")

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
        # The normalized per-item receipt is *derived* from the already
        # verified batch index; no synthetic success is invented.
        item_receipt: dict[str, Any] = {
            "resource_type": "target", "http_status": 207,
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
        verdict = evaluate_global_sp_target_bid_readback(item_evidence)
        items.append({
            "index": index,
            "request_id": request["request_id"],
            "application_status": verdict["application_status"],
            "reasons": verdict["reasons"],
        })

    statuses = {item["application_status"] for item in items}
    # Unknown outranks all other evidence: a partial receipt cannot excuse
    # an unrelated success item with missing, stale or conflicting readback.
    if "Unknown" in statuses:
        status = "Unknown"
    elif "Partial" in statuses:
        status = "Partial"
    elif "Drifted" in statuses:
        status = "Drifted"
    else:
        status = "Confirmed"
    return {
        **_result(status, f"{len(requests)} indexed target items independently classified; "
                         "batch is Confirmed only if all are Confirmed"),
        "items": items,
    }


def main() -> None:
    print(json.dumps(evaluate_global_sp_target_batch_readback(json.load(sys.stdin)),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

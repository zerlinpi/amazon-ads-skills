#!/usr/bin/env python3
"""Read-only mixed-resource Global SP plan readback evidence gate.

Consumes an externally asserted *complete* immutable plan manifest and its
independent resource-level readback evidence. Does not call Amazon Ads, write,
retry, reconcile Executor actions, or verify the manifest's external origin.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from scripts.evaluate_global_sp_readback import (
    _nonempty, _result, evaluate_global_sp_readback,
)
from scripts.evaluate_global_sp_adgroup_bid_readback import (
    evaluate_global_sp_adgroup_bid_readback,
)
from scripts.evaluate_global_sp_target_bid_readback import (
    evaluate_global_sp_target_bid_readback,
)
from scripts.evaluate_global_sp_adgroup_batch_readback import (
    evaluate_global_sp_adgroup_batch_readback,
)
from scripts.evaluate_global_sp_target_batch_readback import (
    evaluate_global_sp_target_batch_readback,
)

_EVALUATORS = {
    "campaign": evaluate_global_sp_readback,
    "ad_group": evaluate_global_sp_adgroup_bid_readback,
    "target": evaluate_global_sp_target_bid_readback,
    "ad_group_batch": evaluate_global_sp_adgroup_batch_readback,
    "target_batch": evaluate_global_sp_target_batch_readback,
}
_SOURCE_FIELDS = ("source_system", "acquisition_channel", "connector_id")


def evaluate_global_sp_mixed_plan_readback(evidence: Any) -> dict[str, Any]:
    """Confirm a declared mixed plan only when *all* children independently Confirm.

    Manifest completeness, provenance and declared component scope are external
    adapter assertions. This classifier checks internal consistency; it cannot
    cryptographically authenticate a plan or prove the executor's write ledger.
    """
    def unknown(reason: str) -> dict[str, Any]:
        return {**_result("Unknown", reason), "components": []}

    if not isinstance(evidence, dict):
        return unknown("plan evidence must be an object")
    if any(isinstance(k, str) and k.startswith("expected_") for k in evidence):
        return unknown("unverified plan-level expected intent")
    manifest, components = evidence.get("manifest"), evidence.get("components")
    if not isinstance(manifest, dict) or not isinstance(components, list):
        return unknown("complete plan manifest and component evidence are required")
    if set(manifest) != {"plan_id", "global_account_id", "coverage_status",
                         "source", "components"}:
        return unknown("manifest fields or intent are unsupported")
    if not _nonempty(manifest.get("plan_id")):
        return unknown("plan_id must be a nonempty external identity")
    account = manifest.get("global_account_id")
    if not _nonempty(account) or manifest.get("coverage_status") != "Complete":
        return unknown("complete single-global-account plan scope is unverified")
    source = manifest.get("source")
    if not isinstance(source, dict) or any(
        not _nonempty(source.get(field)) for field in _SOURCE_FIELDS
    ):
        return unknown("plan manifest source and adapter lineage are unverified")
    declarations = manifest.get("components")
    if not isinstance(declarations, list) or not declarations:
        return unknown("manifest must declare a nonempty complete component list")
    declared: dict[str, dict[str, Any]] = {}
    for item in declarations:
        if not isinstance(item, dict) or not _nonempty(item.get("component_id")):
            return unknown("invalid declared component identity")
        cid, kind = item["component_id"], item.get("kind")
        if cid in declared or not isinstance(kind, str) or kind not in _EVALUATORS:
            return unknown("duplicate or unsupported declared component")
        required = ({"component_id", "kind", "campaign_id"} if kind == "campaign"
                    else {"component_id", "kind", "request_ids"})
        if set(item) != required:
            return unknown("unsupported or incomplete component declaration")
        if kind == "campaign":
            if not _nonempty(item.get("campaign_id")):
                return unknown("declared campaign identity is missing")
        else:
            ids = item.get("request_ids")
            if (not isinstance(ids, list) or not ids
                    or any(not _nonempty(x) for x in ids)
                    or len(set(ids)) != len(ids)):
                return unknown("declared request IDs must be complete and unique")
            if not kind.endswith("_batch") and len(ids) != 1:
                return unknown("single-resource declaration has multiple requests")
        declared[cid] = item

    observed: dict[str, dict[str, Any]] = {}
    for item in components:
        if (not isinstance(item, dict)
                or set(item) != {"component_id", "kind", "evidence"}
                or not _nonempty(item.get("component_id"))
                or not isinstance(item.get("evidence"), dict)):
            return unknown("component evidence is missing, malformed or contains claimed verdict")
        cid = item["component_id"]
        if cid in observed:
            return unknown("duplicate component evidence")
        observed[cid] = item
    if set(observed) != set(declared):
        return unknown("component evidence does not exactly cover declared plan")

    used_requests: set[str] = set()
    used_entities: set[tuple[str, ...]] = set()
    results: list[dict[str, Any]] = []
    for declaration in declarations:
        cid, kind = declaration["component_id"], declaration["kind"]
        item = observed[cid]
        if item["kind"] != kind:
            return unknown(f"{cid}: component kind contradicts manifest")
        payload = item["evidence"]
        if kind.endswith("_batch"):
            requests = payload.get("requests")
        else:
            requests = [payload.get("request")]
        if not isinstance(requests, list) or not requests:
            return unknown(f"{cid}: request population is unverified")
        actual_ids: list[str] = []
        for request in requests:
            if not isinstance(request, dict):
                return unknown(f"{cid}: request must be an object")
            if request.get("global_account_id") != account:
                return unknown(f"{cid}: global account conflicts with plan")
            campaign = request.get("campaign_id")
            if not _nonempty(campaign):
                return unknown(f"{cid}: campaign identity is missing")
            if kind == "campaign":
                resource_kind = "campaign"
                key = (resource_kind, account, campaign)
            elif kind.startswith("ad_group"):
                resource_kind = "ad_group"
                group = request.get("ad_group_id")
                if not _nonempty(group) or request.get("resource_type") != "ad_group":
                    return unknown(f"{cid}: ad-group identity or type is unverified")
                key = (resource_kind, account, campaign, group)
            else:
                resource_kind = "target"
                group, target = request.get("ad_group_id"), request.get("target_id")
                if (not _nonempty(group) or not _nonempty(target)
                        or request.get("resource_type") != "target"):
                    return unknown(f"{cid}: target identity or type is unverified")
                key = (resource_kind, account, campaign, group, target)
            if key in used_entities:
                return unknown(f"{cid}: repeated resource cannot prove intermediate states")
            used_entities.add(key)
            if kind != "campaign":
                rid = request.get("request_id")
                if not _nonempty(rid) or rid in used_requests:
                    return unknown(f"{cid}: missing or repeated request correlation")
                used_requests.add(rid)
                actual_ids.append(rid)
        if kind == "campaign":
            if len(requests) != 1 or requests[0]["campaign_id"] != declaration["campaign_id"]:
                return unknown(f"{cid}: campaign does not bind to manifest")
        elif actual_ids != declaration["request_ids"]:
            return unknown(f"{cid}: ordered request IDs do not bind to manifest")
        verdict = _EVALUATORS[kind](payload)
        status = verdict.get("application_status")
        if status not in {"Confirmed", "Unknown", "Partial", "Drifted"}:
            return unknown(f"{cid}: verifier returned unsupported classification")
        results.append({
            "component_id": cid,
            "kind": kind,
            "application_status": status,
            "reasons": verdict.get("reasons", []),
        })

    statuses = {item["application_status"] for item in results}
    status = next((s for s in ("Unknown", "Partial", "Drifted") if s in statuses),
                  "Confirmed")
    return {
        **_result(status, f"{len(results)} declared resource components independently "
                         "classified; plan Confirmed only when all Confirmed"),
        "plan_id": manifest["plan_id"],
        "components": results,
    }


def main() -> None:
    print(json.dumps(evaluate_global_sp_mixed_plan_readback(json.load(sys.stdin)),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

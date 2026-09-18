#!/usr/bin/env python3
"""Deterministically gate connector evidence before metric interpretation."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references" / "connector-capability-catalog.json"
KNOWN_STATUSES = {"Supported", "Partial", "Unsupported", "Unknown"}
VERIFY = {"Verified", "Unverified", "Unknown"}
SURFACES = {"tool", "report", "dataset", "stream", "export", "endpoint", "warehouse_table", "manual_export"}
SCOPE_FIELDS = {"region": "regions", "marketplace": "marketplaces", "ad_product": "ad_products", "account_type": "account_types"}
PASS = ["High Confidence", "Suggest", "Shadow"]
DEGRADED = ["Directional", "Hold", "Alternate Source", "Missing Data", "Manual Review"]
BLOCKED = ["Hold", "Alternate Source", "Missing Data", "Manual Review"]


def _s(v: Any) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _catalog() -> tuple[set[str], str | None]:
    try: obj = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise ValueError("connector capability catalog is unavailable or invalid") from exc
    if not isinstance(obj, dict) or not isinstance(obj.get("capabilities"), list): raise ValueError("connector capability catalog capabilities must be an array")
    ids=set()
    for i,item in enumerate(obj["capabilities"]):
        if not isinstance(item,dict) or not _s(item.get("capability_id")): raise ValueError(f"connector capability catalog capabilities[{i}] has invalid capability_id")
        cid=item["capability_id"].strip()
        if cid in ids: raise ValueError(f"connector capability catalog contains duplicate capability_id {cid!r}")
        ids.add(cid)
    version=obj.get("catalog_version")
    if version is not None and not _s(version): raise ValueError("connector capability catalog version must be a non-empty string or null")
    return ids,version


def _requirements(v, registered):
    if not isinstance(v,list) or not v: raise ValueError("required_capabilities must be a non-empty array")
    out=[]
    for i,item in enumerate(v):
        if not _s(item): raise ValueError(f"required_capabilities[{i}] must be a non-empty string")
        cid=item.strip()
        if cid in out: raise ValueError(f"required_capabilities contains duplicate capability_id {cid!r}")
        if cid not in registered: raise ValueError(f"required_capabilities contains unregistered capability_id {cid!r}")
        out.append(cid)
    return out


def _scope(v):
    if v is None:return {}
    if not isinstance(v,dict):raise ValueError("expected_scope must be an object or null")
    unknown=sorted(set(v)-set(SCOPE_FIELDS))
    if unknown:raise ValueError(f"expected_scope contains unsupported fields: {unknown}")
    out={}
    for k,item in v.items():
        if not _s(item):raise ValueError(f"expected_scope.{k} must be a non-empty string")
        out[k]=item.strip()
    return out


def _time(v,field):
    if not _s(v):raise ValueError(f"{field} must be a non-empty ISO-8601 timestamp")
    text=v.strip()
    try:dt=datetime.fromisoformat(text[:-1]+"+00:00" if text.endswith("Z") else text)
    except ValueError as exc:raise ValueError(f"{field} must be a valid ISO-8601 timestamp") from exc
    if dt.tzinfo is None:raise ValueError(f"{field} must include a timezone")
    return dt.astimezone(timezone.utc)


def _freshness(v):
    if v is None:return None
    if not isinstance(v,dict):raise ValueError("freshness_requirement must be an object or null")
    if set(v)!={"as_of","max_age_seconds"}:raise ValueError("freshness_requirement must contain exactly as_of and max_age_seconds")
    as_of=_time(v["as_of"],"freshness_requirement.as_of");age=v["max_age_seconds"]
    if isinstance(age,bool) or not isinstance(age,(int,float)) or age<0:raise ValueError("freshness_requirement.max_age_seconds must be a non-negative number")
    return {"as_of":as_of,"as_of_raw":v["as_of"],"max_age_seconds":float(age)}


def _index(snapshot):
    if snapshot is None:return {},{}
    if not isinstance(snapshot,dict):raise ValueError("snapshot must be an object or null")
    caps=snapshot.get("capabilities",[])
    if not isinstance(caps,list):raise ValueError("snapshot.capabilities must be an array")
    out={}
    for i,cap in enumerate(caps):
        if not isinstance(cap,dict) or not _s(cap.get("capability_id")):raise ValueError(f"snapshot.capabilities[{i}].capability_id must be a non-empty string")
        cid=cap["capability_id"].strip()
        if cid in out:raise ValueError(f"snapshot.capabilities contains duplicate capability_id {cid!r}")
        if cap.get("status","Unknown") not in KNOWN_STATUSES:raise ValueError(f"snapshot.capabilities[{i}].status must be one of {sorted(KNOWN_STATUSES)}")
        out[cid]=cap
    return out,snapshot


def _snapshot_freshness(snapshot,fresh):
    if fresh is None:return "not_evaluated",[]
    captured_at=snapshot.get("captured_at")
    if not _s(captured_at):return "unknown",["connector snapshot captured_at is missing for the explicit freshness horizon"]
    try:captured=_time(captured_at,"snapshot.captured_at")
    except ValueError:return "unknown",["connector snapshot captured_at is invalid for the explicit freshness horizon"]
    age=(fresh["as_of"]-captured).total_seconds()
    if age<0:return "unknown",["connector snapshot captured_at is after freshness as_of"]
    if age>fresh["max_age_seconds"]:return "stale",["connector snapshot is stale for the explicit freshness horizon"]
    return "pass",[]


def _scope_effect(obj,expected,label):
    if not expected:return "not_evaluated" if label=="capability" else "pass",[]
    scope=obj.get("scope")
    if not isinstance(scope,dict):return "unknown",[f"{label} does not expose bounded decision scope"]
    unknown=blocked=False;warnings=[]
    for field,wanted in expected.items():
        vals=scope.get(SCOPE_FIELDS[field])
        if not isinstance(vals,list) or not vals:unknown=True;warnings.append(f"{label} does not expose bounded {field} scope")
        elif wanted.casefold() not in {x.strip().casefold() for x in vals if _s(x)}:blocked=True;warnings.append(f"{label} does not cover requested {field} {wanted!r}")
    return ("blocked" if blocked else "unknown" if unknown else "pass"),warnings


def _binding_effect(cap,expected,fresh,snapshot_captured_at):
    bindings=cap.get("bindings")
    if not bindings:return "unknown",[],"not_evaluated" if fresh is None else "unknown",["supported capability has no verified connector surface binding"]
    if not isinstance(bindings,list):raise ValueError("capability.bindings must be an array")
    verified=[];warnings=[];saw_unverified=saw_verified=saw_stale=saw_temporal_unknown=saw_identity_unknown=False;seen=set();snapshot_time=None
    if fresh is not None and _s(snapshot_captured_at):
        try:snapshot_time=_time(snapshot_captured_at,"snapshot.captured_at")
        except ValueError:snapshot_time=None
    for i,b in enumerate(bindings):
        field=f"capability.bindings[{i}]"
        if not isinstance(b,dict):raise ValueError(f"{field} must be an object")
        bid=b.get("binding_id")
        if not _s(bid):raise ValueError(f"{field}.binding_id must be a non-empty string")
        bid=bid.strip()
        if bid in seen:raise ValueError(f"capability.bindings contains duplicate binding_id {bid!r}")
        seen.add(bid)
        if b.get("surface_type") not in SURFACES:raise ValueError(f"{field}.surface_type must be one of {sorted(SURFACES)}")
        if not _s(b.get("surface_id")):raise ValueError(f"{field}.surface_id must be a non-empty string")
        status=b.get("verification_status")
        if status not in VERIFY:raise ValueError(f"{field}.verification_status must be one of {sorted(VERIFY)}")
        if not _s(b.get("observed_at")):raise ValueError(f"{field}.observed_at must be a non-empty string")
        if not isinstance(b.get("evidence"),list):raise ValueError(f"{field}.evidence must be an array")
        if status!="Verified":saw_unverified|=status=="Unverified";continue
        saw_verified=True
        if not b["evidence"]:raise ValueError(f"{field} is Verified but has no evidence supporting the binding")
        identifiable=[]
        for j,evidence in enumerate(b["evidence"]):
            if not isinstance(evidence,dict):raise ValueError(f"{field}.evidence[{j}] must be an object")
            if _s(evidence.get("kind")) and _s(evidence.get("reference")):identifiable.append(evidence)
        if not identifiable:
            saw_identity_unknown=True;warnings.append(f"verified connector binding {bid!r} has no supporting evidence with kind/reference identity");continue
        se,sw=_scope_effect(b,expected,"connector binding");warnings.extend(sw)
        if se!="pass":continue
        if fresh is not None:
            observed=_time(b["observed_at"],f"{field}.observed_at")
            if snapshot_time is not None and observed>snapshot_time:saw_temporal_unknown=True;warnings.append(f"verified connector binding {bid!r} is observed after snapshot capture and cannot belong to that snapshot");continue
            age=(fresh["as_of"]-observed).total_seconds()
            if age<0:warnings.append(f"{bid} observed_at is after freshness as_of");continue
            if age>fresh["max_age_seconds"]:saw_stale=True;warnings.append(f"verified connector binding {bid!r} is stale for the explicit freshness horizon");continue
            evidence_fresh=evidence_stale=evidence_temporal_unknown=False
            for j,evidence in enumerate(identifiable):
                evidence_at=evidence.get("observed_at")
                if not _s(evidence_at):continue
                try:evidence_time=_time(evidence_at,f"{field}.evidence[{j}].observed_at")
                except ValueError:warnings.append(f"{bid} has invalid supporting evidence observed_at");continue
                if evidence_time>observed:evidence_temporal_unknown=True;warnings.append(f"verified connector binding {bid!r} has supporting evidence observed after binding verification");continue
                evidence_age=(fresh["as_of"]-evidence_time).total_seconds()
                if evidence_age<0:warnings.append(f"{bid} has supporting evidence observed_at after freshness as_of")
                elif evidence_age>fresh["max_age_seconds"]:evidence_stale=True
                else:evidence_fresh=True
            if not evidence_fresh:
                if evidence_temporal_unknown:saw_temporal_unknown=True
                elif evidence_stale:saw_stale=True;warnings.append(f"verified connector binding {bid!r} has only stale supporting evidence for the explicit freshness horizon")
                else:warnings.append(f"verified connector binding {bid!r} lacks current timestamped supporting evidence for the explicit freshness horizon")
                continue
        verified.append(bid)
    if verified:return "pass",verified,"pass" if fresh else "not_evaluated",warnings
    if saw_identity_unknown:return "unknown",[],"unknown" if fresh else "not_evaluated",warnings
    if saw_temporal_unknown:return "pass",[],"unknown",warnings
    if saw_stale:return "pass",[],"stale",warnings
    if saw_unverified:warnings.append("connector surface binding exists but is not independently verified");return "unverified",[],"unknown" if fresh else "not_evaluated",warnings
    if saw_verified:warnings.append("verified connector surface binding does not prove the requested decision scope")
    return "unknown",[],"unknown" if fresh else "not_evaluated",warnings


def evaluate_connector_capability_gate(payload):
    if not isinstance(payload,dict):raise ValueError("input must be a JSON object")
    registered,version=_catalog();reqs=_requirements(payload.get("required_capabilities"),registered);expected=_scope(payload.get("expected_scope"));fresh=_freshness(payload.get("freshness_requirement"));indexed,snapshot=_index(payload.get("snapshot"));snapshot_freshness_effect,snapshot_warnings=_snapshot_freshness(snapshot,fresh)
    evaluated=[];has_partial=snapshot_freshness_effect in {"stale","unknown"};has_blocked=False
    for cid in reqs:
        cap=indexed.get(cid);scope_effect="not_evaluated";binding_effect="unknown";freshness_effect="not_evaluated";verified=[]
        if cap is None:status="Unknown";access="unknown";effect="blocked";has_blocked=True;warnings=["required capability is absent from the observed connector snapshot"]
        else:
            status=cap.get("status","Unknown");access=cap.get("access_mode","unknown");warnings=list(cap.get("warnings") or []);scope_effect,sw=_scope_effect(cap,expected,"connector capability");warnings+=sw;binding_effect,verified,freshness_effect,bw=_binding_effect(cap,expected,fresh,snapshot.get("captured_at"));warnings+=bw
            if status=="Supported":
                if scope_effect not in {"pass","not_evaluated"}:effect="blocked";has_blocked=True
                elif freshness_effect in {"stale","unknown"}:effect="degraded";has_partial=True
                elif binding_effect=="pass" and verified:effect="pass"
                else:effect="degraded";has_partial=True
            elif status=="Partial" and scope_effect in {"pass","not_evaluated"}:effect="degraded";has_partial=True
            else:effect="blocked";has_blocked=True
        evaluated.append({"capability_id":cid,"status":status,"access_mode":access,"scope_effect":scope_effect,"binding_effect":binding_effect,"freshness_effect":freshness_effect,"verified_binding_ids":verified,"gate_effect":effect,"warnings":warnings})
    if has_blocked:gate,allowed,high="Blocked",BLOCKED,False
    elif has_partial:gate,allowed,high="Degraded",DEGRADED,False
    else:gate,allowed,high="Pass",PASS,True
    return {"gate_status":gate,"catalog_version":version,"high_confidence_allowed":high,"missing_evidence_policy":"never_zero","allowed_decision_classes":allowed,"connector_id":snapshot.get("connector_id"),"connector_version":snapshot.get("connector_version"),"snapshot_captured_at":snapshot.get("captured_at"),"snapshot_freshness_effect":snapshot_freshness_effect,"freshness_requirement":None if fresh is None else {"as_of":fresh["as_of_raw"],"max_age_seconds":fresh["max_age_seconds"]},"requirements":evaluated,"warnings":snapshot_warnings}


def main():
    try:payload=json.load(sys.stdin);print(json.dumps(evaluate_connector_capability_gate(payload),indent=2,sort_keys=True));return 0
    except (ValueError,json.JSONDecodeError) as exc:print(f"ERROR: {exc}",file=sys.stderr);return 2

if __name__=="__main__":raise SystemExit(main())

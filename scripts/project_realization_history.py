#!/usr/bin/env python3
"""Project canonical realized-ad history views from optimization events.

Read-only reducer; the append-first optimization event ledger remains authoritative.
"""
from __future__ import annotations
import json,sys
from datetime import datetime
from typing import Any
MATERIAL_DIMENSIONS=(("realized_surfaces","surface"),("realized_product_ids","product"),("realized_creative_or_message_ids","creative_or_message"))
BOUNDED_COVERAGE={"Complete","Partial"};OBSERVABILITY_STATUSES={"Complete","Partial","Unavailable","Unknown"}
SCOPE_FIELDS=("marketplace","profile_scope","entity_type","entity_id")
ACCOUNT_IDENTITY_FIELDS=("manager_account_id","global_advertiser_account_id","regional_advertiser_account_id","legacy_advertiser_account_id","advertiser_account_id","regional_profile_id","country_code")
STRONG_ACCOUNT_IDENTITY_FIELDS=("global_advertiser_account_id","regional_advertiser_account_id","legacy_advertiser_account_id","advertiser_account_id","regional_profile_id")

def _parse_timestamp(value:Any,*,field:str)->datetime:
    if not isinstance(value,str) or not value:raise ValueError(f"{field} must be a non-empty RFC3339 date-time string")
    normalized=value[:-1]+"+00:00" if value.endswith("Z") else value
    try:parsed=datetime.fromisoformat(normalized)
    except ValueError as exc:raise ValueError(f"{field} must be a valid RFC3339 date-time string") from exc
    if parsed.tzinfo is None:raise ValueError(f"{field} must include a timezone offset")
    return parsed

def _observation_time(event,snapshot):
    value=snapshot.get("captured_at") or event.get("timestamp");return _parse_timestamp(value,field="realization observation time"),value

def _material_dimensions(snapshot):return [label for field,label in MATERIAL_DIMENSIONS if field in snapshot and isinstance(snapshot[field],list)]
def _has_bounded_identity(snapshot):return snapshot.get("coverage_status") in BOUNDED_COVERAGE and bool(_material_dimensions(snapshot) or (isinstance(snapshot.get("identity_hash"),str) and snapshot.get("identity_hash")))
def _event_scope(event):
    entity=event.get("entity")
    if not isinstance(entity,dict) or not isinstance(entity.get("type"),str) or not entity.get("type") or not isinstance(entity.get("id"),str) or not entity.get("id"):return None
    return event.get("marketplace"),event.get("profile_scope"),entity.get("type"),entity.get("id")

def _normalize_account_identity(value:Any,*,context:str):
    if value is None:return None
    if not isinstance(value,dict):raise ValueError(f"{context} must be an object or null")
    normalized={}
    for field in ACCOUNT_IDENTITY_FIELDS:
        item=value.get(field)
        if item is None:continue
        if not isinstance(item,str) or not item:raise ValueError(f"{context} {field} must be a non-empty string or null")
        normalized[field]=item
    if not any(field in normalized for field in STRONG_ACCOUNT_IDENTITY_FIELDS):return None
    provenance=value.get("identity_mapping_provenance")
    if provenance is not None:normalized["identity_mapping_provenance"]=provenance
    return normalized

def _normalize_expected_scope(value):
    if value is None:return None,None
    if not isinstance(value,dict):raise ValueError("expected_scope must be an object or null")
    normalized=[]
    for field in SCOPE_FIELDS:
        item=value.get(field)
        if not isinstance(item,str) or not item:raise ValueError(f"expected_scope.{field} must be a non-empty string")
        normalized.append(item)
    expected_identity=_normalize_account_identity(value.get("account_identity"),context="expected account identity") if "account_identity" in value else None
    return tuple(normalized),expected_identity

def _validate_scope(event_scope,expected_scope):
    if expected_scope is None:return event_scope
    if event_scope is None or any(not isinstance(item,str) or not item for item in event_scope):raise ValueError("realization event scope is incomplete for the requested expected scope")
    if event_scope!=expected_scope:raise ValueError("realization event scope does not match the requested expected scope")
    return event_scope

def _event_account_identity(event):return _normalize_account_identity(event.get("account_identity"),context="account identity")
def _validate_expected_account_identity(current,expected):
    if expected is None:return
    if current is None:raise ValueError("expected account identity is not present on realization event")
    shared=False
    for field in STRONG_ACCOUNT_IDENTITY_FIELDS:
        if field in expected and field in current:
            shared=True
            if expected[field]!=current[field]:raise ValueError(f"expected account identity conflicts on {field}")
    if not shared:raise ValueError("expected account identity cannot be bound to realization event")

def _merge_account_identity(resolved,current,*,missing_seen):
    if current is None:
        if resolved is not None:raise ValueError("realization account identity is incomplete across the event slice")
        return None,True
    if missing_seen:raise ValueError("realization account identity is incomplete across the event slice")
    if resolved is None:return dict(current),False
    for field in ACCOUNT_IDENTITY_FIELDS:
        if field in resolved and field in current and resolved[field]!=current[field]:raise ValueError(f"realization account identity conflicts on {field}")
    if not any(field in resolved and field in current and resolved[field]==current[field] for field in STRONG_ACCOUNT_IDENTITY_FIELDS):raise ValueError("realization account identity cannot be reconciled across the event slice")
    merged=dict(resolved)
    for field in ACCOUNT_IDENTITY_FIELDS:
        if field in current and field not in merged:merged[field]=current[field]
    if "identity_mapping_provenance" in current:merged["identity_mapping_provenance"]=current["identity_mapping_provenance"]
    return merged,False

def _project_last_observed(snapshot,observed_at):
    projected={"snapshot_id":snapshot.get("snapshot_id"),"observed_at":observed_at,"realization_mode":snapshot.get("realization_mode","unknown"),"coverage_status":snapshot.get("coverage_status"),"comparability_status":snapshot.get("comparability_status","Unknown"),"freshness_status":"Unknown","freshness_basis":"Requires decision-horizon evaluation; projector does not invent a repository-wide age threshold.","identity_hash":snapshot.get("identity_hash"),"warnings":list(snapshot.get("warnings") or [])}
    for field,_ in MATERIAL_DIMENSIONS:
        if field in snapshot and isinstance(snapshot[field],list):projected[field]=list(snapshot[field])
    return projected

def _project_observability(snapshot,checked_at):return {"checked_at":checked_at,"status":snapshot.get("coverage_status") if snapshot.get("coverage_status") in OBSERVABILITY_STATUSES else "Unknown","source_dataset":snapshot.get("source_dataset"),"acquisition_channel":snapshot.get("acquisition_channel"),"material_dimensions":_material_dimensions(snapshot),"warnings":list(snapshot.get("warnings") or [])}

def project_realization_history(events:list[dict[str,Any]],*,expected_scope:dict[str,Any]|None=None)->dict[str,Any]:
    expected,expected_identity=_normalize_expected_scope(expected_scope);observations=[];observed_scopes=set();account_identity=None;missing=False
    for index,event in enumerate(events):
        if not isinstance(event,dict):raise ValueError("each event must be an object")
        snapshot=event.get("realization_snapshot")
        if snapshot is None:continue
        if not isinstance(snapshot,dict):raise ValueError("realization_snapshot must be an object or null")
        scope=_validate_scope(_event_scope(event),expected)
        if scope is not None:
            observed_scopes.add(scope)
            if len(observed_scopes)>1:raise ValueError("realization projection requires a single entity scope")
        current=_event_account_identity(event);_validate_expected_account_identity(current,expected_identity)
        account_identity,missing=_merge_account_identity(account_identity,current,missing_seen=missing)
        parsed,raw=_observation_time(event,snapshot);observations.append((parsed,index,raw,snapshot))
    if not observations:return {"last_observed_realization":None,"current_realization_observability":None}
    observations.sort(key=lambda item:(item[0],item[1]));_,_,newest_time,newest_snapshot=observations[-1];last_observed=None
    for _,_,observed_at,snapshot in reversed(observations):
        if _has_bounded_identity(snapshot):last_observed=_project_last_observed(snapshot,observed_at);break
    result={"last_observed_realization":last_observed,"current_realization_observability":_project_observability(newest_snapshot,newest_time)}
    if account_identity is not None:result["account_identity"]=account_identity
    return result

def _load_payload():
    try:payload=json.load(sys.stdin)
    except json.JSONDecodeError as exc:raise ValueError("stdin must contain valid JSON") from exc
    expected_scope=None
    if isinstance(payload,list):events=payload
    elif isinstance(payload,dict):events=payload.get("events");expected_scope=payload.get("expected_scope")
    else:events=None
    if not isinstance(events,list):raise ValueError("input must be an event array or an object with an events array")
    if expected_scope is not None and not isinstance(expected_scope,dict):raise ValueError("expected_scope must be an object or null")
    return events,expected_scope

def main():
    try:events,expected_scope=_load_payload();projected=project_realization_history(events,expected_scope=expected_scope)
    except ValueError as exc:print(f"error: {exc}",file=sys.stderr);return 2
    json.dump(projected,sys.stdout,ensure_ascii=False,sort_keys=True);sys.stdout.write("\n");return 0
if __name__=="__main__":raise SystemExit(main())
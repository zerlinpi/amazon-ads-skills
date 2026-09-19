#!/usr/bin/env python3
"""Deterministically gate connector evidence before metric interpretation."""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references" / "connector-capability-catalog.json"
KNOWN_STATUSES = {"Supported", "Partial", "Unsupported", "Unknown"}
VERIFY = {"Verified", "Unverified", "Unknown"}
SURFACES = {"tool", "report", "dataset", "stream", "export", "endpoint", "warehouse_table", "manual_export"}
SCOPE_FIELDS = {"region": "regions", "marketplace": "marketplaces", "ad_product": "ad_products", "account_type": "account_types"}
DATA_REQUIREMENT_FIELDS = {"required_reporting_generation", "requires_historical_data", "history_window"}
REPORTING_GENERATION_STATUSES = {"active", "read_only", "sunset_scheduled", "retired", "unknown"}
HISTORICAL_AVAILABILITY_STATUSES = {"available", "partial", "unavailable", "retired", "unknown"}
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


def _date(v,field):
    if not _s(v):raise ValueError(f"{field} must be a non-empty ISO date")
    text=v.strip()
    try:value=date.fromisoformat(text)
    except ValueError as exc:raise ValueError(f"{field} must be a valid ISO date (YYYY-MM-DD)") from exc
    return value


def _history_window(v,field):
    if v is None:return None
    if not isinstance(v,dict):raise ValueError(f"{field} must be an object or null")
    if set(v)!={"start_date","end_date","grain"}:
        raise ValueError(f"{field} must contain exactly start_date, end_date, and grain")
    start=_date(v["start_date"],f"{field}.start_date")
    end=_date(v["end_date"],f"{field}.end_date")
    if start>end:raise ValueError(f"{field} start_date must be on or before end_date")
    if not _s(v["grain"]):raise ValueError(f"{field}.grain must be a non-empty string")
    return {
        "start":start,
        "end":end,
        "start_raw":v["start_date"].strip(),
        "end_raw":v["end_date"].strip(),
        "grain":v["grain"].strip(),
    }


def _freshness(v):
    if v is None:return None
    if not isinstance(v,dict):raise ValueError("freshness_requirement must be an object or null")
    if set(v)!={"as_of","max_age_seconds"}:raise ValueError("freshness_requirement must contain exactly as_of and max_age_seconds")
    as_of=_time(v["as_of"],"freshness_requirement.as_of");age=v["max_age_seconds"]
    if isinstance(age,bool) or not isinstance(age,(int,float)) or age<0:raise ValueError("freshness_requirement.max_age_seconds must be a non-negative number")
    return {"as_of":as_of,"as_of_raw":v["as_of"],"max_age_seconds":float(age)}


def _data_requirements(v, required_capabilities):
    if v is None:
        return {}
    if not isinstance(v, dict):
        raise ValueError("data_requirements must be an object or null")
    out = {}
    for cid, requirement in v.items():
        if cid not in required_capabilities:
            raise ValueError(
                f"data_requirements capability_id {cid!r} must also appear in required_capabilities"
            )
        if not isinstance(requirement, dict):
            raise ValueError(f"data_requirements[{cid!r}] must be an object")
        unknown = sorted(set(requirement) - DATA_REQUIREMENT_FIELDS)
        if unknown:
            raise ValueError(
                f"data_requirements[{cid!r}] contains unsupported fields: {unknown}"
            )
        generation = requirement.get("required_reporting_generation")
        history = requirement.get("requires_historical_data")
        history_window = _history_window(
            requirement.get("history_window"),
            f"data_requirements[{cid!r}].history_window",
        )
        if generation is not None and not _s(generation):
            raise ValueError(
                f"data_requirements[{cid!r}].required_reporting_generation must be a non-empty string or null"
            )
        if history is not None and not isinstance(history, bool):
            raise ValueError(
                f"data_requirements[{cid!r}].requires_historical_data must be boolean or null"
            )
        if history_window is not None and history is False:
            raise ValueError(
                f"data_requirements[{cid!r}].history_window conflicts with requires_historical_data=false"
            )
        if generation is None and history is None and history_window is None:
            raise ValueError(
                f"data_requirements[{cid!r}] must declare required_reporting_generation, requires_historical_data, and/or history_window"
            )
        out[cid] = {
            "required_reporting_generation": generation.strip() if _s(generation) else None,
            "requires_historical_data": history is True or history_window is not None,
            "history_window": None if history_window is None else {
                "start_date": history_window["start_raw"],
                "end_date": history_window["end_raw"],
                "grain": history_window["grain"],
            },
        }
    return out


def _combine_data_effect(current, candidate):
    rank = {
        "not_evaluated": 0,
        "pass": 1,
        "unknown": 2,
        "degraded": 3,
        "blocked": 4,
    }
    return candidate if rank[candidate] > rank[current] else current


def _data_contract_effect(cap, requirement):
    if requirement is None:
        return "not_evaluated", []
    contract = cap.get("data_contract")
    if not isinstance(contract, dict):
        return "unknown", [
            "required reporting/history decision has no observed capability data_contract"
        ]

    effect = "pass"
    warnings = []
    generation = requirement.get("required_reporting_generation")

    if generation is not None:
        observed_generation = contract.get("reporting_generation")
        if not _s(observed_generation):
            effect = _combine_data_effect(effect, "unknown")
            warnings.append("required reporting generation is not identified by the connector snapshot")
        elif observed_generation.strip().casefold() != generation.casefold():
            effect = _combine_data_effect(effect, "blocked")
            warnings.append(
                f"observed reporting generation {observed_generation!r} does not match required generation {generation!r}"
            )

        generation_status = contract.get("reporting_generation_status")
        if generation_status is None or generation_status == "unknown":
            effect = _combine_data_effect(effect, "unknown")
            warnings.append("reporting generation status is unknown")
        elif generation_status not in REPORTING_GENERATION_STATUSES:
            raise ValueError(
                "capability.data_contract.reporting_generation_status must be one of "
                f"{sorted(REPORTING_GENERATION_STATUSES)} or null"
            )
        elif generation_status == "retired":
            effect = _combine_data_effect(effect, "blocked")
            warnings.append("required reporting generation is retired")
        elif generation_status == "sunset_scheduled":
            warnings.append(
                "required reporting generation has a scheduled sunset; verify migration timing before relying on future retrieval"
            )
        elif generation_status == "read_only":
            warnings.append(
                "required reporting generation is currently read-only; analysis may proceed but report creation/editing is unavailable"
            )

        sunset_at = contract.get("sunset_at")
        if sunset_at is not None:
            _time(sunset_at, "capability.data_contract.sunset_at")

    if requirement.get("requires_historical_data") is True:
        history_status = contract.get("historical_availability_status")
        if history_status is None or history_status == "unknown":
            effect = _combine_data_effect(effect, "unknown")
            warnings.append("historical availability state is unknown for a history-dependent decision")
        elif history_status not in HISTORICAL_AVAILABILITY_STATUSES:
            raise ValueError(
                "capability.data_contract.historical_availability_status must be one of "
                f"{sorted(HISTORICAL_AVAILABILITY_STATUSES)} or null"
            )
        elif history_status == "partial":
            effect = _combine_data_effect(effect, "degraded")
            warnings.append(
                "historical availability is partial; bound the decision to the verified history window"
            )
        elif history_status in {"unavailable", "retired"}:
            effect = _combine_data_effect(effect, "blocked")
            warnings.append(
                "required historical data is unavailable or retired; missing history must not be interpreted as zero activity"
            )

        requested = requirement.get("history_window")
        if requested is not None and history_status not in {"unavailable", "retired"}:
            requested_window = _history_window(
                requested,
                "data_requirements.history_window",
            )
            observed_windows = contract.get("historical_windows")
            if not isinstance(observed_windows, list) or not observed_windows:
                effect = _combine_data_effect(effect, "unknown")
                warnings.append(
                    "requested history window has no observed per-grain availability range"
                )
            else:
                matches = []
                for index, observed in enumerate(observed_windows):
                    field = f"capability.data_contract.historical_windows[{index}]"
                    if not isinstance(observed, dict):
                        raise ValueError(f"{field} must be an object")
                    grain = observed.get("grain")
                    if not _s(grain):
                        raise ValueError(f"{field}.grain must be a non-empty string")
                    if grain.strip().casefold() == requested_window["grain"].casefold():
                        matches.append((field, observed))
                if not matches:
                    effect = _combine_data_effect(effect, "unknown")
                    warnings.append(
                        f"no verified historical availability window is observed for requested grain {requested_window['grain']!r}"
                    )
                elif len(matches) > 1:
                    effect = _combine_data_effect(effect, "unknown")
                    warnings.append(
                        f"multiple historical availability windows are observed for requested grain {requested_window['grain']!r}; scope is ambiguous"
                    )
                else:
                    field, observed = matches[0]
                    available_from = observed.get("available_from")
                    available_through = observed.get("available_through")
                    if available_from is None or available_through is None:
                        effect = _combine_data_effect(effect, "unknown")
                        warnings.append(
                            f"historical availability boundaries are incomplete for requested grain {requested_window['grain']!r}"
                        )
                    else:
                        start = _date(available_from, f"{field}.available_from")
                        end = _date(available_through, f"{field}.available_through")
                        if start > end:
                            raise ValueError(
                                f"{field}.available_from must be on or before available_through"
                            )
                        if requested_window["start"] < start or requested_window["end"] > end:
                            effect = _combine_data_effect(effect, "blocked")
                            warnings.append(
                                "requested history window is outside the verified available range for "
                                f"{requested_window['grain']!r}: {available_from} through {available_through}"
                            )

    return effect, warnings


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
    registered,version=_catalog();reqs=_requirements(payload.get("required_capabilities"),registered);expected=_scope(payload.get("expected_scope"));fresh=_freshness(payload.get("freshness_requirement"));data_requirements=_data_requirements(payload.get("data_requirements"),reqs);indexed,snapshot=_index(payload.get("snapshot"));snapshot_freshness_effect,snapshot_warnings=_snapshot_freshness(snapshot,fresh)
    evaluated=[];has_partial=snapshot_freshness_effect in {"stale","unknown"};has_blocked=False
    for cid in reqs:
        cap=indexed.get(cid);scope_effect="not_evaluated";binding_effect="unknown";freshness_effect="not_evaluated";data_contract_effect="not_evaluated";verified=[]
        if cap is None:status="Unknown";access="unknown";effect="blocked";has_blocked=True;warnings=["required capability is absent from the observed connector snapshot"]
        else:
            status=cap.get("status","Unknown");access=cap.get("access_mode","unknown");warnings=list(cap.get("warnings") or []);scope_effect,sw=_scope_effect(cap,expected,"connector capability");warnings+=sw;binding_effect,verified,freshness_effect,bw=_binding_effect(cap,expected,fresh,snapshot.get("captured_at"));warnings+=bw;data_contract_effect,dw=_data_contract_effect(cap,data_requirements.get(cid));warnings+=dw
            if data_contract_effect=="blocked":effect="blocked";has_blocked=True
            elif status=="Supported":
                if scope_effect not in {"pass","not_evaluated"}:effect="blocked";has_blocked=True
                elif freshness_effect in {"stale","unknown"} or data_contract_effect in {"degraded","unknown"}:effect="degraded";has_partial=True
                elif binding_effect=="pass" and verified:effect="pass"
                else:effect="degraded";has_partial=True
            elif status=="Partial" and scope_effect in {"pass","not_evaluated"}:effect="degraded";has_partial=True
            else:effect="blocked";has_blocked=True
        evaluated.append({"capability_id":cid,"status":status,"access_mode":access,"scope_effect":scope_effect,"binding_effect":binding_effect,"freshness_effect":freshness_effect,"data_contract_effect":data_contract_effect,"verified_binding_ids":verified,"gate_effect":effect,"warnings":warnings})
    if has_blocked:gate,allowed,high="Blocked",BLOCKED,False
    elif has_partial:gate,allowed,high="Degraded",DEGRADED,False
    else:gate,allowed,high="Pass",PASS,True
    return {"gate_status":gate,"catalog_version":version,"high_confidence_allowed":high,"missing_evidence_policy":"never_zero","allowed_decision_classes":allowed,"connector_id":snapshot.get("connector_id"),"connector_version":snapshot.get("connector_version"),"snapshot_captured_at":snapshot.get("captured_at"),"snapshot_freshness_effect":snapshot_freshness_effect,"freshness_requirement":None if fresh is None else {"as_of":fresh["as_of_raw"],"max_age_seconds":fresh["max_age_seconds"]},"data_requirements":data_requirements or None,"requirements":evaluated,"warnings":snapshot_warnings}


def main():
    try:payload=json.load(sys.stdin);print(json.dumps(evaluate_connector_capability_gate(payload),indent=2,sort_keys=True));return 0
    except (ValueError,json.JSONDecodeError) as exc:print(f"ERROR: {exc}",file=sys.stderr);return 2

if __name__=="__main__":raise SystemExit(main())

#!/usr/bin/env python3
"""Deterministically gate connector evidence before metric interpretation."""
from __future__ import annotations

import json
import math
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references" / "connector-capability-catalog.json"
CONTROL_STATE_SCHEMA = ROOT / "schemas" / "control-state-snapshot.json"
KNOWN_STATUSES = {"Supported", "Partial", "Unsupported", "Unknown"}
VERIFY = {"Verified", "Unverified", "Unknown"}
SURFACES = {"tool", "report", "dataset", "stream", "export", "endpoint", "warehouse_table", "manual_export"}
# Canonical capabilities are read-side; a Verified binding does not grant read access.
READ_SIDE_ACCESS_MODES = {"read", "report", "export", "stream"}
SCOPE_FIELDS = {"region": "regions", "marketplace": "marketplaces", "ad_product": "ad_products", "account_type": "account_types", "advertiser_account_id": "advertiser_account_ids", "campaign_id": "campaign_ids"}
DATA_REQUIREMENT_FIELDS = {"required_reporting_generation", "requires_historical_data", "history_window", "required_control_types", "required_transition_provenance_fields"}
TRANSITION_FIELDS = {"management_mode", "last_transition_actor", "transition_reason", "transition_observed_at", "actor_evidence_status"}
REPORTING_GENERATION_STATUSES = {"active", "read_only", "sunset_scheduled", "retired", "unknown"}
HISTORICAL_AVAILABILITY_STATUSES = {"available", "partial", "unavailable", "retired", "unknown"}
PASS = ["High Confidence", "Suggest", "Shadow"]
DEGRADED = ["Directional", "Hold", "Alternate Source", "Missing Data", "Manual Review"]
BLOCKED = ["Hold", "Alternate Source", "Missing Data", "Manual Review"]


def _s(v: Any) -> bool:
    return isinstance(v, str) and bool(v.strip())


# These are evidence placeholders, not verified surface or source identities.
# Match whole normalized labels only: a legitimate ID may contain "unknown".
_UNUSABLE_VERIFICATION_LABELS = {
    "unknown", "unsupported", "partial", "missing", "unavailable",
    "not available", "not supported",
}


def _verified_identity(value: Any) -> bool:
    if not _s(value) or value != value.strip():
        return False
    normalized = " ".join(value.casefold().replace("_", " ").replace("-", " ").split())
    return normalized not in _UNUSABLE_VERIFICATION_LABELS


def _catalog() -> tuple[set[str], str | None]:
    try: obj = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise ValueError("connector capability catalog is unavailable or invalid") from exc
    if not isinstance(obj, dict) or not isinstance(obj.get("capabilities"), list): raise ValueError("connector capability catalog capabilities must be an array")
    ids=set()
    # Observation is read-side evidence only for canonical observation capabilities.
    # Do not globally permit observe access to stand in for report/read transport.
    declared_modes={}
    for i,item in enumerate(obj["capabilities"]):
        if not isinstance(item,dict) or not _s(item.get("capability_id")): raise ValueError(f"connector capability catalog capabilities[{i}] has invalid capability_id")
        cid=item["capability_id"].strip()
        if cid in ids: raise ValueError(f"connector capability catalog contains duplicate capability_id {cid!r}")
        ids.add(cid)
        declared_modes[cid]=item.get("access_mode")
    version=obj.get("catalog_version")
    if version is not None and not _s(version): raise ValueError("connector capability catalog version must be a non-empty string or null")
    return ids,version,declared_modes



def _registered_control_types() -> set[str]:
    try:
        schema = json.loads(CONTROL_STATE_SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("control-state schema is unavailable or invalid") from exc
    try:
        values = schema["$defs"]["controlType"]["enum"]
    except (KeyError, TypeError) as exc:
        raise ValueError("control-state schema does not expose canonical control types") from exc
    if not isinstance(values, list) or not values:
        raise ValueError("control-state schema canonical control types must be a non-empty array")
    out = set()
    for value in values:
        if not _s(value):
            raise ValueError("control-state schema contains an invalid control type")
        out.add(value.strip())
    return out


def _control_type_list(value, field):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a non-empty array")
    registered = _registered_control_types()
    out = []
    for index, item in enumerate(value):
        if not _s(item):
            raise ValueError(f"{field}[{index}] must be a non-empty string")
        control_type = item.strip()
        if control_type not in registered:
            raise ValueError(f"{field}[{index}] contains unknown control type {control_type!r}")
        if control_type in out:
            raise ValueError(f"{field} contains duplicate control type {control_type!r}")
        out.append(control_type)
    return out


def _transition_field_list(value, field):
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a non-empty array")
    if any(not _s(item) or item not in TRANSITION_FIELDS for item in value):
        raise ValueError(f"{field} contains unsupported or invalid provenance field")
    if len(set(value)) != len(value):
        raise ValueError(f"{field} contains duplicate provenance fields")
    return list(value)


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
        if not _verified_identity(item):
            raise ValueError(f"expected_scope.{k} must be a concrete, non-placeholder scope identity")
        out[k]=item
    return out


def _time(v,field):
    if not _s(v):raise ValueError(f"{field} must be a non-empty ISO-8601 timestamp")
    text=v.strip()
    try:dt=datetime.fromisoformat(text[:-1]+"+00:00" if text.endswith("Z") else text)
    except ValueError as exc:raise ValueError(f"{field} must be a valid ISO-8601 timestamp") from exc
    if dt.tzinfo is None:raise ValueError(f"{field} must include a timezone")
    return dt.astimezone(timezone.utc)


def _binding_time(v, field):
    """A verified binding needs a known-offset instant, even without freshness."""
    if isinstance(v, str) and v.strip().endswith("-00:00"):
        raise ValueError(f"{field} has an unknown RFC3339 offset")
    return _time(v, field)


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
    if not _verified_identity(v["grain"]):raise ValueError(f"{field}.grain must be a concrete, non-placeholder grain identity")
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
    if isinstance(age, bool) or not isinstance(age, (int, float)):
        raise ValueError("freshness_requirement.max_age_seconds must be a finite non-negative number")
    try:
        seconds = float(age)
    except OverflowError as exc:
        raise ValueError("freshness_requirement.max_age_seconds must be a finite non-negative number") from exc
    if not math.isfinite(seconds) or seconds < 0:
        raise ValueError("freshness_requirement.max_age_seconds must be a finite non-negative number")
    return {"as_of": as_of, "as_of_raw": v["as_of"], "max_age_seconds": seconds}


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
        required_control_types = None
        required_transition_fields = None
        if "required_transition_provenance_fields" in requirement:
            if cid != "entity-state-readback":
                raise ValueError("required_transition_provenance_fields is only valid for entity-state-readback")
            required_transition_fields = _transition_field_list(
                requirement["required_transition_provenance_fields"],
                f"data_requirements[{cid!r}].required_transition_provenance_fields"
            )
        if "required_control_types" in requirement:
            if cid != "entity-state-readback":
                raise ValueError(
                    f"data_requirements[{cid!r}].required_control_types is only valid for entity-state-readback"
                )
            required_control_types = _control_type_list(
                requirement.get("required_control_types"),
                f"data_requirements[{cid!r}].required_control_types",
            )
        history_window = _history_window(
            requirement.get("history_window"),
            f"data_requirements[{cid!r}].history_window",
        )
        if generation is not None and not _verified_identity(generation):
            raise ValueError(
                f"data_requirements[{cid!r}].required_reporting_generation must be a concrete, non-placeholder identity or null"
            )
        if history is not None and not isinstance(history, bool):
            raise ValueError(
                f"data_requirements[{cid!r}].requires_historical_data must be boolean or null"
            )
        if history_window is not None and history is False:
            raise ValueError(
                f"data_requirements[{cid!r}].history_window conflicts with requires_historical_data=false"
            )
        if generation is None and history is None and history_window is None and required_control_types is None and required_transition_fields is None:
            raise ValueError(
                f"data_requirements[{cid!r}] must declare required_reporting_generation, requires_historical_data, history_window, and/or required_control_types or required_transition_provenance_fields"
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
        if required_control_types is not None:
            out[cid]["required_control_types"] = required_control_types
        if required_transition_fields is not None:
            out[cid]["required_transition_provenance_fields"] = required_transition_fields
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


def _data_contract_effect(cap, requirement, snapshot_captured_at):
    if requirement is None:
        return "not_evaluated", []
    required_control_types = requirement.get("required_control_types")
    required_transition_fields = requirement.get("required_transition_provenance_fields")
    contract = cap.get("data_contract")
    if not isinstance(contract, dict):
        if required_control_types or required_transition_fields:
            return "blocked", [
                "required control-state coverage has no observed capability data_contract"
            ]
        return "unknown", [
            "required reporting/history decision has no observed capability data_contract"
        ]

    effect = "pass"
    warnings = []
    generation = requirement.get("required_reporting_generation")

    if generation is not None:
        observed_generation = contract.get("reporting_generation")
        if not _verified_identity(observed_generation):
            effect = _combine_data_effect(effect, "unknown")
            warnings.append("required reporting generation has no concrete, verified identity in the connector snapshot")
        elif observed_generation.casefold() != generation.casefold():
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
            sunset = _time(sunset_at, "capability.data_contract.sunset_at")
            # An overdue scheduled sunset contradicts a snapshot that still
            # claims the generation is active or awaiting sunset. Do not
            # infer actual retirement: request refreshed source evidence.
            try:
                captured = _binding_time(snapshot_captured_at, "snapshot.captured_at")
            except ValueError:
                captured = None
            if (
                captured is not None
                and sunset < captured
                and generation_status in {"active", "sunset_scheduled"}
            ):
                effect = _combine_data_effect(effect, "unknown")
                warnings.append(
                    "reporting generation sunset precedes snapshot capture "
                    "but observed status has not been reconciled; refresh source evidence"
                )

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
                ambiguous_matching_grain = False
                for index, observed in enumerate(observed_windows):
                    field = f"capability.data_contract.historical_windows[{index}]"
                    if not isinstance(observed, dict):
                        raise ValueError(f"{field} must be an object")
                    grain = observed.get("grain")
                    if not _s(grain):
                        raise ValueError(f"{field}.grain must be a non-empty string")
                    if not _verified_identity(grain):
                        # A padded apparent match cannot prove the requested grain,
                        # even if another entry carries a concrete matching label.
                        if grain.strip().casefold() == requested_window["grain"].casefold():
                            ambiguous_matching_grain = True
                        continue
                    if grain.casefold() == requested_window["grain"].casefold():
                        matches.append((field, observed))
                if ambiguous_matching_grain:
                    effect = _combine_data_effect(effect, "unknown")
                    warnings.append("requested historical grain has an unavailable or padded matching availability label")
                elif not matches:
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
                        # This is an observed historical-availability bound, not
                        # a forecast. A snapshot cannot attest to history months
                        # after it was captured. Allow one calendar day for the
                        # missing marketplace-timezone context in date-only bounds.
                        try:
                            captured_day = _binding_time(
                                snapshot_captured_at, "snapshot.captured_at"
                            ).date()
                        except ValueError:
                            captured_day = None
                        if captured_day is not None and (end - captured_day).days > 1:
                            effect = _combine_data_effect(effect, "unknown")
                            warnings.append(
                                "observed historical availability extends beyond snapshot "
                                "capture; future history is not verified"
                            )
                        if requested_window["start"] < start or requested_window["end"] > end:
                            effect = _combine_data_effect(effect, "blocked")
                            warnings.append(
                                "requested history window is outside the verified available range for "
                                f"{requested_window['grain']!r}: {available_from} through {available_through}"
                            )


    if required_control_types:
        observed_control_types = contract.get("control_types_exposed")
        if observed_control_types is None:
            effect = _combine_data_effect(effect, "blocked")
            warnings.append(
                "required control-state coverage is not identified by control_types_exposed"
            )
        else:
            observed_control_types = _control_type_list(
                observed_control_types,
                "capability.data_contract.control_types_exposed",
            )
            missing_control_types = [
                control_type
                for control_type in required_control_types
                if control_type not in observed_control_types
            ]
            if missing_control_types:
                effect = _combine_data_effect(effect, "blocked")
                warnings.append(
                    "connector does not expose required control types: "
                    + ", ".join(missing_control_types)
                )

    if required_transition_fields:
        observed_fields = contract.get("transition_provenance_fields_exposed")
        if observed_fields is None:
            effect = _combine_data_effect(effect, "blocked")
            warnings.append("required transition provenance is not identified by connector data_contract")
        else:
            observed_fields = _transition_field_list(
                observed_fields, "capability.data_contract.transition_provenance_fields_exposed"
            )
            missing_fields = [
                field for field in required_transition_fields if field not in observed_fields
            ]
            if missing_fields:
                effect = _combine_data_effect(effect, "blocked")
                warnings.append(
                    "connector does not expose required transition provenance fields: "
                    + ", ".join(missing_fields)
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
    if not expected:return "not_evaluated" if label=="capability" else "pass",[],False
    scope=obj.get("scope")
    if not isinstance(scope,dict):return "unknown",[f"{label} does not expose bounded decision scope"],False
    unknown=blocked=missing=False;warnings=[]
    for field,wanted in expected.items():
        vals=scope.get(SCOPE_FIELDS[field])
        if not isinstance(vals,list) or not vals:
            unknown=True;missing=True
            warnings.append(f"{label} does not expose bounded {field} scope")
            continue
        # Unknown members cannot prove either inclusion or exclusion.
        # A concrete match remains usable even if another member is unknown.
        # Advertiser and campaign IDs are opaque identities, not display labels.
        # Never case-fold them into an apparent match across distinct resources.
        exact_identity = field in {"advertiser_account_id", "campaign_id"}
        concrete={value if exact_identity else value.casefold() for value in vals if _verified_identity(value)}
        if (wanted if exact_identity else wanted.casefold()) in concrete:
            continue
        if any(not _verified_identity(value) for value in vals):
            unknown=True
            warnings.append(f"{label} has unavailable {field} scope evidence; requested scope cannot be excluded")
        else:
            blocked=True
            warnings.append(f"{label} does not cover requested {field} {wanted!r}")
    return ("blocked" if blocked else "unknown" if unknown else "pass"),warnings,unknown and not missing and not blocked


def _binding_effect(cap,expected,fresh,snapshot_captured_at):
    bindings=cap.get("bindings")
    if not bindings:return "unknown",[],"not_evaluated" if fresh is None else "unknown",["supported capability has no verified connector surface binding"]
    if not isinstance(bindings,list):raise ValueError("capability.bindings must be an array")
    verified=[];warnings=[];saw_unverified=saw_verified=saw_stale=saw_temporal_unknown=saw_identity_unknown=False;seen=set();snapshot_time=None
    # Chronological provenance is a separate requirement from caller-selected
    # freshness. A binding cannot have been verified after its own snapshot.
    if _s(snapshot_captured_at):
        try:snapshot_time=_binding_time(snapshot_captured_at,"snapshot.captured_at")
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
        if not _verified_identity(b.get("binding_id")) or not _verified_identity(b.get("surface_id")):
            saw_identity_unknown = True
            warnings.append(f"verified connector binding {bid!r} has unavailable binding_id or surface_id identity")
            continue
        if not b["evidence"]:raise ValueError(f"{field} is Verified but has no evidence supporting the binding")
        try:
            observed = _binding_time(b["observed_at"], f"{field}.observed_at")
        except ValueError:
            saw_temporal_unknown = True
            warnings.append(f"verified connector binding {bid!r} has invalid observed_at")
            continue
        if snapshot_time is None:
            saw_temporal_unknown = True
            warnings.append(f"verified connector binding {bid!r} has no valid snapshot captured_at to establish chronology")
            continue
        if observed > snapshot_time:
            saw_temporal_unknown = True
            warnings.append(f"verified connector binding {bid!r} is observed after snapshot capture")
            continue
        identifiable=[]
        for j,evidence in enumerate(b["evidence"]):
            if not isinstance(evidence,dict):raise ValueError(f"{field}.evidence[{j}] must be an object")
            if _verified_identity(evidence.get("kind")) and _verified_identity(evidence.get("reference")):identifiable.append(evidence)
        if not identifiable:
            saw_identity_unknown=True;warnings.append(f"verified connector binding {bid!r} has no supporting evidence with kind/reference identity");continue
        # An explicitly dated supporting record cannot postdate the binding
        # it supposedly verified. Legacy undated evidence remains accepted
        # when no freshness requirement was requested.
        evidence_chronology_bad = False
        for j, evidence in enumerate(identifiable):
            evidence_at = evidence.get("observed_at")
            if evidence_at is None:
                continue
            try:
                evidence_time = _binding_time(evidence_at, f"{field}.evidence[{j}].observed_at")
            except ValueError:
                warnings.append(f"verified connector binding {bid!r} has invalid supporting evidence observed_at")
                evidence_chronology_bad = True
                break
            if evidence_time > observed:
                warnings.append(f"verified connector binding {bid!r} has supporting evidence observed after binding verification")
                evidence_chronology_bad = True
                break
        if evidence_chronology_bad:
            saw_temporal_unknown = True
            continue
        se,sw,_=_scope_effect(b,expected,"connector binding");warnings.extend(sw)
        if se!="pass":continue
        if fresh is not None:
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
    if saw_temporal_unknown:return "unknown",[],"unknown" if fresh else "not_evaluated",warnings
    if saw_stale:return "pass",[],"stale",warnings
    if saw_unverified:warnings.append("connector surface binding exists but is not independently verified");return "unverified",[],"unknown" if fresh else "not_evaluated",warnings
    if saw_verified:warnings.append("verified connector surface binding does not prove the requested decision scope")
    return "unknown",[],"unknown" if fresh else "not_evaluated",warnings


def _snapshot_identity_warnings(snapshot):
    """A Verified surface cannot establish an unidentified acquisition path."""
    warnings = []
    if not _verified_identity(snapshot.get("connector_id")):
        warnings.append("connector snapshot identity is missing or unavailable (connector_id)")
    for field in ("source_system", "acquisition_channel"):
        # These fields are optional for legacy snapshots. An explicit unknown
        # assertion is different from omission and must not prove provenance.
        if field in snapshot and not _verified_identity(snapshot[field]):
            warnings.append(f"connector snapshot source identity is unavailable ({field})")
    return warnings



def _feature_eligibility_effect(payload, expected):
    """Join an optional feature-specific eligibility record to exact decision scope.

    This is a normalized read-side evidence check, NOT a vendor entitlement
    lookup or proof that an adapter's source_reference is authentic.
    """
    requirement = payload.get("feature_eligibility_requirement")
    evidence = payload.get("feature_eligibility_evidence")
    if requirement is None:
        if evidence is not None:
            raise ValueError("feature_eligibility_evidence requires feature_eligibility_requirement")
        return "not_evaluated", []

    field = "feature_eligibility_requirement"
    required = {
        "feature_id", "marketplace", "advertiser_account_id", "campaign_id",
        "as_of", "max_age_seconds",
    }
    if not isinstance(requirement, dict) or set(requirement) != required:
        raise ValueError(f"{field} must contain exactly {sorted(required)}")
    for key in ("feature_id", "marketplace", "advertiser_account_id", "campaign_id"):
        if not _verified_identity(requirement[key]):
            raise ValueError(f"{field}.{key} must be a concrete, non-placeholder identity")
    # A feature entitlement cannot be inferred from a generic marketplace-only
    # connector request. Require the exact same identities on both sides.
    for key in ("marketplace", "advertiser_account_id", "campaign_id"):
        requested = requirement[key]
        scoped = expected.get(key)
        exact = key in {"advertiser_account_id", "campaign_id"}
        if scoped is None or (scoped if exact else scoped.casefold()) != (
            requested if exact else requested.casefold()
        ):
            raise ValueError(f"{field}.{key} must match exact expected_scope.{key}")

    as_of = _binding_time(requirement["as_of"], f"{field}.as_of")
    age = requirement["max_age_seconds"]
    if isinstance(age, bool) or not isinstance(age, (int, float)):
        raise ValueError(f"{field}.max_age_seconds must be finite and non-negative")
    try:
        max_age = float(age)
    except OverflowError as exc:
        raise ValueError(f"{field}.max_age_seconds must be finite and non-negative") from exc
    if not math.isfinite(max_age) or max_age < 0:
        raise ValueError(f"{field}.max_age_seconds must be finite and non-negative")

    if not isinstance(evidence, dict):
        return "unknown", ["feature-specific eligibility evidence is absent"]
    for key in ("feature_id", "marketplace", "advertiser_account_id", "campaign_id"):
        observed = evidence.get(key)
        if not _verified_identity(observed):
            return "unknown", [f"feature eligibility {key} is missing or unavailable"]
        exact = key in {"feature_id", "advertiser_account_id", "campaign_id"}
        if (observed if exact else observed.casefold()) != (
            requirement[key] if exact else requirement[key].casefold()
        ):
            return "unknown", [f"feature eligibility {key} does not match requested decision identity"]

    if evidence.get("evidence_type") != "feature-specific":
        return "unknown", [
            "generic product-group or other evidence cannot prove this feature-specific eligibility"
        ]
    if evidence.get("verification_status") != "Verified":
        return "unknown", ["feature eligibility record is not independently verified"]
    if not _verified_identity(evidence.get("source_system")) or not _verified_identity(
        evidence.get("source_reference")
    ):
        return "unknown", ["feature eligibility has no concrete source identity/reference"]
    try:
        observed_at = _binding_time(
            evidence.get("observed_at"), "feature_eligibility_evidence.observed_at"
        )
    except ValueError:
        return "unknown", ["feature eligibility has no valid known-offset observation time"]
    elapsed = (as_of - observed_at).total_seconds()
    if elapsed < 0:
        return "unknown", ["feature eligibility was observed after the requested as_of"]
    if elapsed > max_age:
        return "unknown", ["feature eligibility evidence is stale for the requested horizon"]

    status = evidence.get("eligibility_status")
    if status == "Eligible":
        return "pass", []
    if status == "Ineligible":
        return "blocked", ["verified feature-specific eligibility is explicitly Ineligible"]
    return "unknown", ["feature eligibility is Partial, Unknown or unavailable"]



def _feature_source_independence(payload, indexed, eligibility_effect):
    """Reject obvious self-references, not authenticate remote entitlement.

    An eligibility record must not reuse any connector binding's identity
    or supporting probe from the same snapshot, even if that capability is
    not required for the current decision or its binding is Unverified.
    Distinct labels alone do not prove authenticity.
    """
    if eligibility_effect not in {"pass", "blocked"}:
        return "not_evaluated", []
    source_reference = payload["feature_eligibility_evidence"]["source_reference"]
    for capability in indexed.values():
        if not isinstance(capability, dict):
            continue
        # The snapshot contract also permits evidence attached directly to a
        # capability, not just evidence nested under individual bindings.
        # Neither location can be repurposed as independent entitlement proof.
        for record in capability.get("evidence") or []:
            if isinstance(record, dict) and source_reference == record.get("reference"):
                return "unknown", [
                    "feature eligibility source_reference reuses connector capability evidence; independent feature-specific source evidence is unproven"
                ]
        for binding in capability.get("bindings") or []:
            # An unverified probe is not independent feature evidence either.
            if not isinstance(binding, dict):
                continue
            aliases = [binding.get("binding_id"), binding.get("surface_id")]
            for record in binding.get("evidence") or []:
                if isinstance(record, dict):
                    aliases.append(record.get("reference"))
            if source_reference in aliases:
                return "unknown", [
                    "feature eligibility source_reference reuses connector binding evidence; independent feature-specific source evidence is unproven"
                ]
    return "pass", []


def _feature_snapshot_chronology(snapshot, requirement):
    """Prevent future connector evidence from proving a feature decision as_of.

    The feature requirement's horizon applies to eligibility evidence only;
    this check does not invent a connector TTL or authenticate raw API data.
    """
    if requirement is None:
        return "not_evaluated", []
    try:
        captured = _binding_time(snapshot.get("captured_at"), "snapshot.captured_at")
    except ValueError:
        return "unknown", [
            "connector snapshot captured_at is missing, invalid or has unknown offset for feature eligibility as_of"
        ]
    as_of = _binding_time(requirement["as_of"], "feature_eligibility_requirement.as_of")
    if captured > as_of:
        return "unknown", [
            "connector snapshot captured_at is after feature eligibility decision as_of; future connector evidence cannot prove earlier scope"
        ]
    return "pass", []


def evaluate_connector_capability_gate(payload):
    if not isinstance(payload,dict):raise ValueError("input must be a JSON object")
    registered, version, declared_modes = _catalog()
    reqs = _requirements(payload.get("required_capabilities"), registered)
    expected = _scope(payload.get("expected_scope"))
    fresh = _freshness(payload.get("freshness_requirement"))
    data_requirements = _data_requirements(payload.get("data_requirements"), reqs)
    eligibility_effect, eligibility_warnings = _feature_eligibility_effect(payload, expected)
    indexed, snapshot = _index(payload.get("snapshot"))
    feature_source_independence_effect, source_warnings = _feature_source_independence(
        payload, indexed, eligibility_effect
    )
    if feature_source_independence_effect == "unknown":
        eligibility_effect = "unknown"
        # An unproven self-referential Ineligible claim is not a verified
        # exclusion; do not retain a contradictory verified-block warning.
        eligibility_warnings = source_warnings
    else:
        eligibility_warnings += source_warnings
    feature_snapshot_chronology_effect, feature_snapshot_chronology_warnings = _feature_snapshot_chronology(
        snapshot, payload.get("feature_eligibility_requirement")
    )
    snapshot_freshness_effect, snapshot_warnings = _snapshot_freshness(snapshot, fresh)
    snapshot_identity_warnings = _snapshot_identity_warnings(snapshot)
    evaluated=[];has_partial=snapshot_freshness_effect in {"stale","unknown"} or bool(snapshot_identity_warnings) or eligibility_effect=="unknown" or feature_snapshot_chronology_effect=="unknown";has_blocked=eligibility_effect=="blocked"
    for cid in reqs:
        cap=indexed.get(cid);scope_effect="not_evaluated";binding_effect="unknown";freshness_effect="not_evaluated";data_contract_effect="not_evaluated";verified=[]
        if cap is None:status="Unknown";access="unknown";effect="blocked";has_blocked=True;warnings=["required capability is absent from the observed connector snapshot"]
        else:
            status=cap.get("status","Unknown");access=cap.get("access_mode","unknown");warnings=list(cap.get("warnings") or []);scope_effect,sw,observed_unknown_scope=_scope_effect(cap,expected,"connector capability");warnings+=sw;binding_effect,verified,freshness_effect,bw=_binding_effect(cap,expected,fresh,snapshot.get("captured_at"));warnings+=bw;data_contract_effect,dw=_data_contract_effect(cap,data_requirements.get(cid),snapshot.get("captured_at"));warnings+=dw
            if data_contract_effect=="blocked":effect="blocked";has_blocked=True
            elif status=="Supported" and access=="write":
                effect="blocked";has_blocked=True
                warnings.append("write-only capability access mode cannot substantiate a read-side requirement")
            elif status=="Supported" and (
                not isinstance(access,str)
                or (access not in READ_SIDE_ACCESS_MODES
                    and not (access=="observe" and declared_modes.get(cid)=="observe"))
            ):
                effect="degraded";has_partial=True
                warnings.append("capability access mode is missing, ambiguous or not verified as read-side")
            elif status=="Supported":
                if scope_effect=="blocked" or (scope_effect=="unknown" and not observed_unknown_scope):effect="blocked";has_blocked=True
                elif scope_effect=="unknown":effect="degraded";has_partial=True
                elif freshness_effect in {"stale","unknown"} or data_contract_effect in {"degraded","unknown"}:effect="degraded";has_partial=True
                elif binding_effect=="pass" and verified:effect="pass"
                else:effect="degraded";has_partial=True
            elif status=="Partial" and (scope_effect in {"pass","not_evaluated"} or observed_unknown_scope):effect="degraded";has_partial=True
            else:effect="blocked";has_blocked=True
        evaluated.append({"capability_id":cid,"status":status,"access_mode":access,"scope_effect":scope_effect,"binding_effect":binding_effect,"freshness_effect":freshness_effect,"data_contract_effect":data_contract_effect,"verified_binding_ids":verified,"gate_effect":effect,"warnings":warnings})
    if has_blocked:gate,allowed,high="Blocked",BLOCKED,False
    elif has_partial:gate,allowed,high="Degraded",DEGRADED,False
    else:gate,allowed,high="Pass",PASS,True
    return {"gate_status":gate,"catalog_version":version,"high_confidence_allowed":high,"missing_evidence_policy":"never_zero","allowed_decision_classes":allowed,"connector_id":snapshot.get("connector_id"),"connector_version":snapshot.get("connector_version"),"snapshot_captured_at":snapshot.get("captured_at"),"snapshot_freshness_effect":snapshot_freshness_effect,"feature_eligibility_effect":eligibility_effect,"feature_source_independence_effect":feature_source_independence_effect,"feature_snapshot_chronology_effect":feature_snapshot_chronology_effect,"freshness_requirement":None if fresh is None else {"as_of":fresh["as_of_raw"],"max_age_seconds":fresh["max_age_seconds"]},"data_requirements":data_requirements or None,"requirements":evaluated,"warnings":snapshot_warnings + snapshot_identity_warnings + eligibility_warnings + feature_snapshot_chronology_warnings}


def main():
    try:payload=json.load(sys.stdin);print(json.dumps(evaluate_connector_capability_gate(payload),indent=2,sort_keys=True));return 0
    except (ValueError,json.JSONDecodeError) as exc:print(f"ERROR: {exc}",file=sys.stderr);return 2

if __name__=="__main__":raise SystemExit(main())

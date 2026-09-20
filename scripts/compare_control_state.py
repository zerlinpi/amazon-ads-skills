#!/usr/bin/env python3
"""Deterministically compare two read-only control-state snapshots.

This helper classifies evidence; it never authorizes or performs Amazon Ads writes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BAD_EVIDENCE = {"stale", "unsupported", "unknown"}
REGISTRY_PATH = Path(__file__).resolve().parents[1] / "references" / "control-requirement-registry.json"


def _control_map(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["control_type"]: item for item in snapshot.get("controls", [])}


def _registry_requirement(provenance: dict[str, Any]) -> tuple[set[str] | None, str | None]:
    registry_id = provenance.get("requirement_registry_id")
    surface = provenance.get("decision_surface")
    if not registry_id:
        return None, "material-control requirement registry identity is missing"
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "material-control requirement registry is unavailable"
    if registry.get("registry_id") != registry_id:
        return None, "material-control requirement registry identity is unknown or stale"
    entry = registry.get("decision_surfaces", {}).get(surface)
    if not isinstance(entry, dict):
        return None, "decision surface is absent from the material-control requirement registry"
    required = entry.get("required_control_types")
    if not isinstance(required, list) or not required:
        return None, "registry requirement set is missing"
    return set(required), None


def _coverage_problem(snapshot: dict[str, Any], control_map: dict[str, dict[str, Any]], side: str) -> str | None:
    coverage = snapshot.get("coverage")
    if not isinstance(coverage, dict):
        return f"{side} material-control coverage is missing"
    if coverage.get("coverage_status") != "Complete":
        return f"{side} material-control coverage is not Complete"
    provenance = coverage.get("requirement_provenance")
    if not isinstance(provenance, dict) or provenance.get("derivation_status") != "Verified":
        return f"{side} material-control requirement provenance is not Verified"
    if not provenance.get("decision_surface"):
        return f"{side} material-control requirement decision surface is missing"
    registry_required, registry_problem = _registry_requirement(provenance)
    if registry_problem:
        return f"{side} {registry_problem}"
    required = coverage.get("required_control_types")
    if not isinstance(required, list) or not required:
        return f"{side} required material-control set is missing"
    if set(required) != registry_required:
        return f"{side} required material-control set does not match the versioned registry"
    missing = sorted(set(required) - set(control_map))
    if missing:
        return f"{side} required controls are not evidenced: " + ", ".join(missing)
    return None


def compare_control_state(baseline: dict[str, Any], post: dict[str, Any], intended_treatment: str | None = None) -> dict[str, Any]:
    """Return a fail-closed comparability classification and evidence reasons."""
    reasons: list[str] = []
    bscope, pscope = baseline.get("scope", {}), post.get("scope", {})
    for key in ("marketplace_id", "profile_id"):
        if not bscope.get(key) or bscope.get(key) != pscope.get(key):
            return {"classification": "Unknown", "reasons": [f"scope mismatch or missing {key}"]}
    for key in ("campaign_id", "ad_group_id", "entity_id"):
        if bscope.get(key) != pscope.get(key):
            return {"classification": "Unknown", "reasons": [f"decision-scope identity changed for {key}"]}

    if bscope.get("entity_id") is not None:
        before_type, after_type = bscope.get("entity_type"), pscope.get("entity_type")
        if not before_type or not after_type:
            return {"classification": "Unknown", "reasons": ["entity_id is present without a complete entity_type identity"]}
        if before_type != after_type:
            return {"classification": "Unknown", "reasons": ["decision-scope identity changed for entity_type"]}

    bmap, pmap = _control_map(baseline), _control_map(post)
    for snapshot, control_map, side in ((baseline, bmap, "baseline"), (post, pmap, "post")):
        problem = _coverage_problem(snapshot, control_map, side)
        if problem:
            return {"classification": "Unknown", "reasons": [problem]}

    required_before = set(baseline["coverage"]["required_control_types"])
    required_after = set(post["coverage"]["required_control_types"])
    if required_before != required_after:
        return {"classification": "Unknown", "reasons": ["material-control requirement set changed between snapshots"]}

    provenance_before = baseline["coverage"]["requirement_provenance"]
    provenance_after = post["coverage"]["requirement_provenance"]
    if provenance_before.get("decision_surface") != provenance_after.get("decision_surface"):
        return {"classification": "Unknown", "reasons": ["material-control requirement decision surface changed between snapshots"]}
    if provenance_before.get("requirement_registry_id") != provenance_after.get("requirement_registry_id"):
        return {"classification": "Unknown", "reasons": ["material-control requirement registry changed between snapshots"]}

    all_types = sorted(set(bmap) | set(pmap))
    if not all_types:
        return {"classification": "Unknown", "reasons": ["no material control evidence"]}

    changed: list[str] = []
    unknown: list[str] = []
    timestamp_unknown: list[str] = []
    for control_type in all_types:
        before, after = bmap.get(control_type), pmap.get(control_type)
        if before is None or after is None:
            unknown.append(control_type)
            continue
        if before.get("evidence_status") in BAD_EVIDENCE or after.get("evidence_status") in BAD_EVIDENCE:
            unknown.append(control_type)
            continue
        if before.get("state") != after.get("state"):
            changed.append(control_type)
            if not before.get("effective_at") or not after.get("effective_at"):
                timestamp_unknown.append(control_type)

    if unknown:
        reasons.append("unknown/stale/unsupported evidence: " + ", ".join(unknown))
    if timestamp_unknown:
        reasons.append("changed control lacks effective_at: " + ", ".join(timestamp_unknown))
    if reasons:
        return {"classification": "Unknown", "reasons": reasons, "changed_controls": changed}

    if intended_treatment:
        if intended_treatment not in required_before:
            return {"classification": "Unknown", "reasons": ["intended treatment is outside the evidenced material-control set"]}
        if intended_treatment not in changed:
            return {"classification": "Unknown", "reasons": ["intended treatment has no observed state change"]}
        overlaps = [c for c in changed if c != intended_treatment]
        if not overlaps:
            return {"classification": "Treatment Isolated", "reasons": ["only intended treatment changed within a complete, registry-verified material-control set"], "changed_controls": changed}
        return {"classification": "Confounded", "reasons": ["overlapping material controls changed: " + ", ".join(overlaps)], "changed_controls": changed}

    if not changed:
        return {"classification": "Comparable", "reasons": ["no evidenced material control changes within a complete, registry-verified material-control set"], "changed_controls": []}
    return {"classification": "Directional", "reasons": ["material controls changed without an identified treatment"], "changed_controls": changed}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare control-state snapshots without executing writes")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("post", type=Path)
    parser.add_argument("--treatment", dest="treatment")
    args = parser.parse_args()
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    post = json.loads(args.post.read_text(encoding="utf-8"))
    print(json.dumps(compare_control_state(baseline, post, args.treatment), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

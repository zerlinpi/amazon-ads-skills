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


def _control_map(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["control_type"]: item for item in snapshot.get("controls", [])}


def compare_control_state(baseline: dict[str, Any], post: dict[str, Any], intended_treatment: str | None = None) -> dict[str, Any]:
    """Return a fail-closed comparability classification and evidence reasons."""
    reasons: list[str] = []
    bscope, pscope = baseline.get("scope", {}), post.get("scope", {})
    for key in ("marketplace_id", "profile_id"):
        if not bscope.get(key) or bscope.get(key) != pscope.get(key):
            return {"classification": "Unknown", "reasons": [f"scope mismatch or missing {key}"]}

    bmap, pmap = _control_map(baseline), _control_map(post)
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
        if intended_treatment not in all_types:
            return {"classification": "Unknown", "reasons": ["intended treatment is not evidenced"]}
        if intended_treatment not in changed:
            return {"classification": "Unknown", "reasons": ["intended treatment has no observed state change"]}
        overlaps = [c for c in changed if c != intended_treatment]
        if not overlaps:
            return {"classification": "Treatment Isolated", "reasons": ["only intended treatment changed"], "changed_controls": changed}
        # The comparator cannot infer whether overlapping controls are harmless.
        return {"classification": "Confounded", "reasons": ["overlapping material controls changed: " + ", ".join(overlaps)], "changed_controls": changed}

    if not changed:
        return {"classification": "Comparable", "reasons": ["no evidenced material control changes"], "changed_controls": []}
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

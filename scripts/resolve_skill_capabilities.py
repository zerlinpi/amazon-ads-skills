#!/usr/bin/env python3
"""Resolve canonical connector capability IDs for a Skill decision profile.

Read-only helper. It loads the repository-owned capability catalog and returns
registered required/optional IDs. It does not call a connector or grant write
authority.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "references" / "connector-capability-catalog.json"


def _load_catalog() -> dict[str, Any]:
    try:
        data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("connector capability catalog is unavailable or invalid") from exc
    if not isinstance(data, dict):
        raise ValueError("connector capability catalog must be an object")
    return data


def resolve_skill_capabilities(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")

    skill = payload.get("skill")
    profile = payload.get("profile", "live-analysis")
    if not isinstance(skill, str) or not skill.strip():
        raise ValueError("skill must be a non-empty string")
    if not isinstance(profile, str) or not profile.strip():
        raise ValueError("profile must be a non-empty string")
    skill = skill.strip()
    profile = profile.strip()

    catalog = _load_catalog()
    skill_map = catalog.get("skills")
    if not isinstance(skill_map, dict) or skill not in skill_map:
        raise ValueError(f"unknown skill: {skill}")

    profiles = skill_map[skill]
    if not isinstance(profiles, dict) or profile not in profiles:
        available = sorted(profiles) if isinstance(profiles, dict) else []
        raise ValueError(
            f"unknown profile {profile!r} for skill {skill!r}; available profiles: {available}"
        )

    spec = profiles[profile]
    if not isinstance(spec, dict):
        raise ValueError(f"invalid capability profile for {skill}:{profile}")

    known = {
        item.get("capability_id"): item
        for item in catalog.get("capabilities", [])
        if isinstance(item, dict) and isinstance(item.get("capability_id"), str)
    }

    required = spec.get("required", [])
    optional = spec.get("optional", [])
    data_requirements = spec.get("data_requirements", {})
    if not isinstance(required, list) or not isinstance(optional, list):
        raise ValueError(f"invalid required/optional lists for {skill}:{profile}")
    if not isinstance(data_requirements, dict):
        raise ValueError(f"invalid data_requirements for {skill}:{profile}")

    unresolved = [item for item in required + optional if item not in known]
    if unresolved:
        raise ValueError(
            f"catalog profile references unregistered capability IDs: {sorted(set(unresolved))}"
        )

    allowed_data_requirement_fields = {
        "required_reporting_generation",
        "requires_historical_data",
    }
    normalized_data_requirements = {}
    for capability_id, requirement in data_requirements.items():
        if capability_id not in required:
            raise ValueError(
                f"data_requirements capability_id {capability_id!r} must also be required for {skill}:{profile}"
            )
        if not isinstance(requirement, dict) or not requirement:
            raise ValueError(
                f"data_requirements[{capability_id!r}] must be a non-empty object"
            )
        unknown_fields = sorted(set(requirement) - allowed_data_requirement_fields)
        if unknown_fields:
            raise ValueError(
                f"data_requirements[{capability_id!r}] contains unsupported fields: {unknown_fields}"
            )
        normalized = {}
        if "required_reporting_generation" in requirement:
            generation = requirement.get("required_reporting_generation")
            if generation is not None and (
                not isinstance(generation, str) or not generation.strip()
            ):
                raise ValueError(
                    f"data_requirements[{capability_id!r}].required_reporting_generation must be a non-empty string or null"
                )
            if isinstance(generation, str):
                normalized["required_reporting_generation"] = generation.strip()
            elif generation is not None:
                normalized["required_reporting_generation"] = generation
        if "requires_historical_data" in requirement:
            history = requirement.get("requires_historical_data")
            if not isinstance(history, bool):
                raise ValueError(
                    f"data_requirements[{capability_id!r}].requires_historical_data must be boolean"
                )
            normalized["requires_historical_data"] = history
        normalized_data_requirements[capability_id] = normalized

    return {
        "catalog_version": catalog.get("catalog_version"),
        "skill": skill,
        "profile": profile,
        "required_capabilities": required,
        "optional_capabilities": optional,
        "data_requirements": normalized_data_requirements,
        "capabilities": {
            capability_id: known[capability_id]
            for capability_id in required + optional
        },
        "policy": {
            "use_with": "scripts/evaluate_connector_capability_gate.py",
            "pass_data_requirements_to_gate": True,
            "missing_evidence_policy": "never_zero",
            "write_authority": "none",
        },
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        result = resolve_skill_capabilities(payload)
    except json.JSONDecodeError:
        print("error: stdin must contain valid JSON", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    json.dump(result, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

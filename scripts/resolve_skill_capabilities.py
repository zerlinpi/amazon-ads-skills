#!/usr/bin/env python3
"""Resolve canonical connector capability IDs for a Skill decision profile.

Read-only helper. It loads the repository-owned capability catalog and returns
registered required/optional IDs. It does not call a connector or grant write
authority.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "references" / "connector-capability-catalog.json"
PROFILE_DATA_REQUIREMENT_FIELDS = {
    "required_reporting_generation",
    "requires_historical_data",
}
TASK_DATA_REQUIREMENT_FIELDS = PROFILE_DATA_REQUIREMENT_FIELDS | {"history_window"}


def _history_window(value: Any, field: str) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    if set(value) != {"start_date", "end_date", "grain"}:
        raise ValueError(
            f"{field} must contain exactly start_date, end_date, and grain"
        )
    start = value.get("start_date")
    end = value.get("end_date")
    grain = value.get("grain")
    if not isinstance(start, str) or not start.strip():
        raise ValueError(f"{field}.start_date must be a non-empty ISO date")
    if not isinstance(end, str) or not end.strip():
        raise ValueError(f"{field}.end_date must be a non-empty ISO date")
    if not isinstance(grain, str) or not grain.strip():
        raise ValueError(f"{field}.grain must be a non-empty string")
    try:
        start_date = date.fromisoformat(start.strip())
        end_date = date.fromisoformat(end.strip())
    except ValueError as exc:
        raise ValueError(
            f"{field} dates must use YYYY-MM-DD"
        ) from exc
    if start_date > end_date:
        raise ValueError(f"{field} start_date must be on or before end_date")
    return {
        "start_date": start.strip(),
        "end_date": end.strip(),
        "grain": grain.strip(),
    }


def _normalize_requirement(
    capability_id: str,
    requirement: Any,
    *,
    source: str,
    allowed_fields: set[str],
) -> dict[str, Any]:
    if not isinstance(requirement, dict) or not requirement:
        raise ValueError(
            f"{source}[{capability_id!r}] must be a non-empty object"
        )
    unknown_fields = sorted(set(requirement) - allowed_fields)
    if unknown_fields:
        raise ValueError(
            f"{source}[{capability_id!r}] contains unsupported fields: {unknown_fields}"
        )

    normalized: dict[str, Any] = {}
    if "required_reporting_generation" in requirement:
        generation = requirement.get("required_reporting_generation")
        if not isinstance(generation, str) or not generation.strip():
            raise ValueError(
                f"{source}[{capability_id!r}].required_reporting_generation must be a non-empty string"
            )
        normalized["required_reporting_generation"] = generation.strip()

    if "requires_historical_data" in requirement:
        history = requirement.get("requires_historical_data")
        if not isinstance(history, bool):
            raise ValueError(
                f"{source}[{capability_id!r}].requires_historical_data must be boolean"
            )
        normalized["requires_historical_data"] = history

    if "history_window" in requirement:
        normalized["history_window"] = _history_window(
            requirement.get("history_window"),
            f"{source}[{capability_id!r}].history_window",
        )
        if normalized.get("requires_historical_data") is False:
            raise ValueError(
                f"{source}[{capability_id!r}] history_window conflicts with requires_historical_data=false"
            )
        normalized["requires_historical_data"] = True

    return normalized


def _merge_task_requirements(
    required: list[str],
    profile_requirements: dict[str, dict[str, Any]],
    task_requirements: Any,
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    if task_requirements is None:
        return profile_requirements, {}
    if not isinstance(task_requirements, dict):
        raise ValueError("task_data_requirements must be an object or null")

    task_normalized: dict[str, dict[str, Any]] = {}
    merged = {
        capability_id: dict(requirement)
        for capability_id, requirement in profile_requirements.items()
    }

    for capability_id, raw_requirement in task_requirements.items():
        if capability_id not in required:
            raise ValueError(
                f"task_data_requirements capability_id {capability_id!r} must also be required by the selected profile"
            )
        requirement = _normalize_requirement(
            capability_id,
            raw_requirement,
            source="task_data_requirements",
            allowed_fields=TASK_DATA_REQUIREMENT_FIELDS,
        )
        if requirement.get("requires_historical_data") is False:
            raise ValueError(
                f"task_data_requirements[{capability_id!r}] cannot relax historical data requirements"
            )

        current = merged.setdefault(capability_id, {})
        current_generation = current.get("required_reporting_generation")
        task_generation = requirement.get("required_reporting_generation")
        if (
            current_generation is not None
            and task_generation is not None
            and current_generation.casefold() != task_generation.casefold()
        ):
            raise ValueError(
                f"task_data_requirements[{capability_id!r}] cannot replace profile required_reporting_generation"
            )

        if task_generation is not None:
            current["required_reporting_generation"] = task_generation
        if current.get("requires_historical_data") is True:
            if requirement.get("requires_historical_data") is False:
                raise ValueError(
                    f"task_data_requirements[{capability_id!r}] cannot relax profile requires_historical_data=true"
                )
        elif requirement.get("requires_historical_data") is True:
            current["requires_historical_data"] = True
        if "history_window" in requirement:
            current["history_window"] = requirement["history_window"]
            current["requires_historical_data"] = True

        task_normalized[capability_id] = requirement

    return merged, task_normalized


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

    profile_data_requirements: dict[str, dict[str, Any]] = {}
    for capability_id, requirement in data_requirements.items():
        if capability_id not in required:
            raise ValueError(
                f"data_requirements capability_id {capability_id!r} must also be required for {skill}:{profile}"
            )
        profile_data_requirements[capability_id] = _normalize_requirement(
            capability_id,
            requirement,
            source="data_requirements",
            allowed_fields=PROFILE_DATA_REQUIREMENT_FIELDS,
        )

    normalized_data_requirements, task_data_requirements = _merge_task_requirements(
        required,
        profile_data_requirements,
        payload.get("task_data_requirements"),
    )

    return {
        "catalog_version": catalog.get("catalog_version"),
        "skill": skill,
        "profile": profile,
        "required_capabilities": required,
        "optional_capabilities": optional,
        "data_requirements": normalized_data_requirements,
        "data_requirement_provenance": {
            "profile": profile_data_requirements,
            "task": task_data_requirements,
        },
        "capabilities": {
            capability_id: known[capability_id]
            for capability_id in required + optional
        },
        "policy": {
            "use_with": "scripts/evaluate_connector_capability_gate.py",
            "pass_data_requirements_to_gate": True,
            "task_data_requirements_may_only_strengthen": True,
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

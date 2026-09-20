#!/usr/bin/env python3
"""Resolve a token-efficient Agent Skill context plan for custom hosts/platforms.

This helper is metadata-only until a single Skill has been selected. It never
calls Amazon Ads and never grants write authority.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from scripts.resolve_skill_capabilities import resolve_skill_capabilities
from scripts.validate_skills import _frontmatter

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_RE = re.compile(
    r"(?:(?:\.\./)+)?(?:references|schemas|scripts|playbooks)/[A-Za-z0-9._/-]+"
)


def _skill_record(root: Path, skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    meta, errors = _frontmatter(text, skill_file)
    if errors:
        raise ValueError("; ".join(errors))
    name = meta.get("name")
    description = meta.get("description")
    if not name or not description:
        raise ValueError(f"{skill_file}: missing name/description metadata")
    return {
        "name": name,
        "description": description,
        "entrypoint": skill_file.relative_to(root).as_posix(),
    }


def build_skill_catalog(root: Path = ROOT) -> list[dict[str, str]]:
    """Return name/description/entrypoint only; never return Skill bodies."""
    root = Path(root).resolve()
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        raise ValueError("skills directory is unavailable")

    records = []
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise ValueError(f"{skill_dir}: missing SKILL.md")
        records.append(_skill_record(root, skill_file))
    return records


def _resource_candidates(root: Path, skill_file: Path) -> list[str]:
    """Return referenced repository resources without loading their contents."""
    text = skill_file.read_text(encoding="utf-8")
    candidates: set[str] = set()
    repo_root = root.resolve()
    for raw in RESOURCE_RE.findall(text):
        target = (skill_file.parent / raw).resolve()
        try:
            relative = target.relative_to(repo_root)
        except ValueError:
            continue
        if target.exists() and target.is_file():
            candidates.add(relative.as_posix())
    return sorted(candidates)


def resolve_skill_context(
    root: Path,
    skill: str,
    profile: str = "live-analysis",
) -> dict[str, Any]:
    """Resolve one selected Skill plus deferred resources/capabilities."""
    root = Path(root).resolve()
    catalog = {item["name"]: item for item in build_skill_catalog(root)}
    if skill not in catalog:
        raise ValueError(f"unknown skill: {skill}")

    record = catalog[skill]
    skill_file = root / record["entrypoint"]
    capability = resolve_skill_capabilities({"skill": skill, "profile": profile})

    return {
        "skill": skill,
        "description": record["description"],
        "entrypoint": record["entrypoint"],
        "preload_files": [record["entrypoint"]],
        "resource_candidates": _resource_candidates(root, skill_file),
        "connector_profile": {
            "catalog_version": capability["catalog_version"],
            "profile": capability["profile"],
            "required_capabilities": capability["required_capabilities"],
            "optional_capabilities": capability["optional_capabilities"],
            "data_requirements": capability["data_requirements"],
            "write_authority": capability["policy"]["write_authority"],
        },
        "context_policy": {
            "metadata_only_catalog": True,
            "resources_on_demand": True,
            "preload_other_skill_bodies": False,
            "preload_docs_research": False,
            "preload_evals": False,
            "write_authority": "none",
        },
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("stdin must contain a JSON object")
        operation = payload.get("operation", "resolve")
        if operation == "catalog":
            result: Any = {
                "skills": build_skill_catalog(ROOT),
                "context_policy": {
                    "metadata_only_catalog": True,
                    "load_skill_body_on_activation": True,
                },
            }
        elif operation == "resolve":
            result = resolve_skill_context(
                ROOT,
                payload.get("skill", ""),
                payload.get("profile", "live-analysis"),
            )
        else:
            raise ValueError(f"unknown operation: {operation}")
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

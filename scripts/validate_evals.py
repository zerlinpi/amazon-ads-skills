#!/usr/bin/env python3
"""Validate historical replay fixture contracts using only the Python stdlib."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

TOP_LEVEL_FIELDS = {
    "id",
    "title",
    "entrypoint",
    "mode",
    "scenario",
    "inputs",
    "allowed_external_evidence",
    "expected",
}
REQUIRED_TOP_LEVEL = {"id", "title", "entrypoint", "mode", "scenario", "inputs", "expected"}
EXPECTED_FIELDS = {
    "acceptable_decisions",
    "forbidden_behaviors",
    "required_observations",
    "rubric",
}
REQUIRED_EXPECTED = {"acceptable_decisions", "forbidden_behaviors", "rubric"}
ALLOWED_MODES = {"Read-only", "Suggest", "Shadow"}
ALLOWED_DECISIONS = {
    "action_safe",
    "directional",
    "blocked",
    "hold",
    "experiment_only",
    "manual_review",
}
LIVE_MUTATION_RE = re.compile(
    r"\b(execute|apply|write|mutate|change|update)\b.{0,80}\b(live|real)\b",
    re.IGNORECASE,
)
NEGATION_RE = re.compile(r"\b(do not|don't|must not|never|without|block|prevent|reject)\b", re.IGNORECASE)


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_nonempty_string(item) for item in value)


def _validate_positive_execution_language(text: str, path: Path) -> list[str]:
    if NEGATION_RE.search(text):
        return []
    if LIVE_MUTATION_RE.search(text):
        return [f"{path}: fixture appears to require live mutation: {text!r}"]
    return []


def validate_fixture(path: Path, repository_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return [f"{path}: fixture root must be an object"]

    for field in sorted(REQUIRED_TOP_LEVEL):
        if field not in data:
            errors.append(f"{path}: missing required field '{field}'")
    for field in sorted(set(data) - TOP_LEVEL_FIELDS):
        errors.append(f"{path}: unexpected top-level field '{field}'")

    fixture_id = data.get("id")
    if not _nonempty_string(fixture_id):
        errors.append(f"{path}: field 'id' must be a non-empty string")
    elif fixture_id != path.stem:
        errors.append(f"{path}: id '{fixture_id}' must match filename '{path.stem}'")

    for field in ("title", "scenario", "entrypoint"):
        if field in data and not _nonempty_string(data[field]):
            errors.append(f"{path}: field '{field}' must be a non-empty string")

    mode = data.get("mode")
    if mode not in ALLOWED_MODES:
        errors.append(f"{path}: invalid mode '{mode}'")

    if "inputs" in data and not isinstance(data["inputs"], dict):
        errors.append(f"{path}: field 'inputs' must be an object")

    if "allowed_external_evidence" in data and not _string_list(data["allowed_external_evidence"]):
        errors.append(f"{path}: field 'allowed_external_evidence' must be a list of non-empty strings")

    entrypoint = data.get("entrypoint")
    if _nonempty_string(entrypoint):
        root = repository_root.resolve()
        candidate = (root / entrypoint).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            errors.append(f"{path}: entrypoint escapes repository: {entrypoint}")
        else:
            if not candidate.is_file():
                errors.append(f"{path}: entrypoint does not exist: {entrypoint}")

    expected = data.get("expected")
    if not isinstance(expected, dict):
        if "expected" in data:
            errors.append(f"{path}: field 'expected' must be an object")
        return errors

    for field in sorted(REQUIRED_EXPECTED):
        if field not in expected:
            errors.append(f"{path}: expected missing required field '{field}'")
    for field in sorted(set(expected) - EXPECTED_FIELDS):
        errors.append(f"{path}: unexpected expected field '{field}'")

    decisions = expected.get("acceptable_decisions")
    if not isinstance(decisions, list) or not decisions:
        errors.append(f"{path}: acceptable_decisions must be a non-empty list")
    else:
        seen: set[str] = set()
        for decision in decisions:
            if decision not in ALLOWED_DECISIONS:
                errors.append(f"{path}: invalid acceptable decision '{decision}'")
            if isinstance(decision, str):
                if decision in seen:
                    errors.append(f"{path}: duplicate acceptable decision '{decision}'")
                seen.add(decision)

    forbidden = expected.get("forbidden_behaviors")
    if forbidden is not None and not _string_list(forbidden):
        errors.append(f"{path}: forbidden_behaviors must be a list of non-empty strings")

    observations = expected.get("required_observations")
    if observations is not None:
        if not _string_list(observations):
            errors.append(f"{path}: required_observations must be a list of non-empty strings")
        else:
            for text in observations:
                errors.extend(_validate_positive_execution_language(text, path))

    rubric = expected.get("rubric")
    if not isinstance(rubric, list) or not rubric:
        errors.append(f"{path}: rubric must be a non-empty list")
    else:
        for index, item in enumerate(rubric):
            label = f"rubric[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{path}: {label} must be an object")
                continue
            unknown = set(item) - {"criterion", "requirement"}
            for field in sorted(unknown):
                errors.append(f"{path}: {label} unexpected field '{field}'")
            for field in ("criterion", "requirement"):
                if not _nonempty_string(item.get(field)):
                    errors.append(f"{path}: {label}.{field} must be a non-empty string")
            requirement = item.get("requirement")
            if _nonempty_string(requirement):
                errors.extend(_validate_positive_execution_language(requirement, path))

    return errors


def validate_repository(root: Path) -> list[str]:
    root = Path(root)
    fixtures_dir = root / "evals" / "fixtures"
    if not fixtures_dir.is_dir():
        return [f"{fixtures_dir}: missing eval fixtures directory"]

    fixture_paths = sorted(fixtures_dir.glob("*.json"))
    if not fixture_paths:
        return [f"{fixtures_dir}: no eval fixture JSON files found"]

    errors: list[str] = []
    seen_ids: dict[str, Path] = {}
    for path in fixture_paths:
        errors.extend(validate_fixture(path, root))
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        fixture_id = data.get("id") if isinstance(data, dict) else None
        if _nonempty_string(fixture_id):
            if fixture_id in seen_ids:
                errors.append(
                    f"{path}: duplicate fixture id '{fixture_id}' also used by {seen_ids[fixture_id]}"
                )
            else:
                seen_ids[fixture_id] = path
    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = validate_repository(root)
    if errors:
        print("Eval validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    count = len(list((root / "evals" / "fixtures").glob("*.json")))
    print(f"Eval validation passed: {count} fixture files checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

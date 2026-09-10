#!/usr/bin/env python3
"""Validate Agent Skills repository structure using only the Python stdlib."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ALLOWED_TOP_LEVEL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
REQUIRED_FIELDS = {"name", "description"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s|$)")


def _frontmatter(text: str, path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: missing opening YAML frontmatter delimiter"]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, [f"{path}: missing closing YAML frontmatter delimiter"]

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL_KEY_RE.match(line)
        if not match:
            errors.append(f"{path}: malformed top-level frontmatter line: {line!r}")
            continue
        key = match.group(1)
        if key in values:
            errors.append(f"{path}: duplicate frontmatter field '{key}'")
        raw_value = line.split(":", 1)[1].strip().strip('"\'')
        values[key] = raw_value
        if key not in ALLOWED_TOP_LEVEL_FIELDS:
            errors.append(f"{path}: unexpected frontmatter field '{key}'")
    return values, errors


def _local_links(skill_file: Path, text: str) -> list[Path]:
    paths: list[Path] = []
    for raw in LINK_RE.findall(text):
        target = raw.strip().split()[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue
        paths.append((skill_file.parent / target).resolve())
    return paths


def validate_skill(skill_dir: Path, repository_root: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    text = skill_file.read_text(encoding="utf-8")
    meta, meta_errors = _frontmatter(text, skill_file)
    errors.extend(meta_errors)

    for field in sorted(REQUIRED_FIELDS):
        if not meta.get(field):
            errors.append(f"{skill_file}: required frontmatter field '{field}' is missing or empty")

    if meta.get("name") and meta["name"] != skill_dir.name:
        errors.append(
            f"{skill_file}: name '{meta['name']}' must match folder name '{skill_dir.name}'"
        )

    nested = [p for p in skill_dir.rglob("SKILL.md") if p != skill_file]
    for path in nested:
        errors.append(f"{skill_dir}: nested SKILL.md is not allowed: {path.relative_to(skill_dir)}")

    repo_root = repository_root.resolve()
    for target in _local_links(skill_file, text):
        try:
            relative = target.relative_to(repo_root)
        except ValueError:
            errors.append(f"{skill_file}: local reference escapes repository: {target}")
            continue
        if not target.exists():
            errors.append(f"{skill_file}: broken local reference: {relative}")

    return errors


def validate_repository(root: Path) -> list[str]:
    root = Path(root)
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return [f"{skills_dir}: missing skills directory"]

    errors: list[str] = []
    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if not skill_dirs:
        errors.append(f"{skills_dir}: no skill directories found")
        return errors

    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir, root))
    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = validate_repository(root)
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    count = sum(1 for p in (root / "skills").iterdir() if p.is_dir())
    print(f"Skill validation passed: {count} skill directories checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

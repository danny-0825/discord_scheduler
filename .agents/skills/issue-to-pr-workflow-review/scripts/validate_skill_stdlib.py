#!/usr/bin/env python3
"""Validate the structural contract of a Codex SKILL.md without third-party packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


MAX_NAME_LENGTH = 64
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}


def parse_frontmatter(content: str) -> tuple[dict[str, str], str] | tuple[None, str]:
    if not content.startswith("---\n"):
        return None, "No YAML frontmatter found"
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format"

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if not separator or not re.fullmatch(r"[A-Za-z0-9_-]+", key.strip()):
            return None, f"Unsupported frontmatter line: {line}"
        values[key.strip()] = value.strip().strip("'\"")
    return values, content[match.end() :]


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    values, body_or_error = parse_frontmatter(skill_md.read_text())
    if values is None:
        return False, body_or_error

    unexpected = set(values) - ALLOWED_KEYS
    if unexpected:
        return False, f"Unexpected frontmatter key(s): {', '.join(sorted(unexpected))}"
    if not values.get("name"):
        return False, "Missing 'name' in frontmatter"
    if not values.get("description"):
        return False, "Missing 'description' in frontmatter"

    name = values["name"]
    if not re.fullmatch(r"[a-z0-9-]+", name):
        return False, f"Name '{name}' should be hyphen-case"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    if len(name) > MAX_NAME_LENGTH:
        return False, f"Name is too long ({len(name)} characters)"

    description = values["description"]
    if description.startswith("[TODO:"):
        return False, "Description contains an unfinished TODO placeholder"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return False, "Description is too long (maximum 1024 characters)"

    fence: str | None = None
    for line in body_or_error.splitlines():
        marker = re.match(r"^[ \t]*(?:[-+*]|\d+[.)])?[ \t]*(`{3,}|~{3,})(.*)$", line)
        if marker:
            current = marker.group(1)[0]
            if fence is None:
                fence = current
            elif current == fence and not marker.group(2).strip():
                fence = None
            continue
        if fence is None and re.fullmatch(r"[ ]{0,3}\[TODO:[^\n]*\][ \t]*", line):
            return False, "Skill instructions contain an unfinished TODO placeholder"

    return True, "Skill is valid (stdlib validator)"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_skill_stdlib.py <skill_directory>")
        raise SystemExit(2)
    valid, message = validate_skill(Path(sys.argv[1]))
    print(message)
    raise SystemExit(0 if valid else 1)

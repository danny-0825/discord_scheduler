#!/usr/bin/env python3
"""Check local Markdown links owned by the Issue-to-PR workflow without dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def root() -> Path:
    return Path(__file__).resolve().parents[4]


def main() -> int:
    repository = root()
    files = [
        repository / ".agents/skills/issue-to-pr-workflow/SKILL.md",
        repository / ".agents/skills/issue-to-pr-workflow-review/SKILL.md",
        repository / "docs/workflows/issue-to-pr.md",
        repository / "docs/skills/catalog.md",
    ]
    failures: list[str] = []
    for file in files:
        content = file.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^]]+\]\(([^)#]+)(?:#[^)]+)?\)", content):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (file.parent / target).resolve()
            if not resolved.exists():
                failures.append(f"{file.relative_to(repository)} -> {target}")
    if failures:
        print("docs link check: FAIL")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("docs link check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

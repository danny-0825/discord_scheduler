#!/usr/bin/env python3
"""Validate the repository Skill catalog, routing fixtures, and manifests.

The check intentionally validates observable contracts, rather than trying to
predict an LLM's routing decision. Prompt fixtures are a reviewed corpus for
manual/evaluation runs; their declared owner must remain consistent with the
catalog and the installed Skill structure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPLICIT_ONLY_SKILLS = {
    "gitflow-branching",
    "implementation-finder",
    "obsidian-official-cli",
    "obsidian-cli-bases-and-bookmarks",
    "obsidian-cli-devtools",
    "obsidian-cli-runtime-admin",
    "obsidian-cli-sync-and-publish",
    "obsidian-cli-workflows",
    "obsidian-cli-workspace-and-navigation",
    "project-autojournal",
    "project-completed-summary",
    "retro-summary",
    "save-work-checkpoint",
    "setup-obsidian-work-skills",
}
EXPECTED_GROUPS = {"development-operations", "obsidian-cli", "project-memory"}
ALLOWED_SIDE_EFFECTS = {
    "read-only",
    "repository-git-write",
    "project-memory-write",
    "external-github-and-git",
    "vault-write",
    "runtime-write",
    "remote-write",
    "delegated-vault-or-remote-write",
    "workspace-write",
    "local-config-write",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read_frontmatter(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
    if not match:
        fail(f"{path}: SKILL.md frontmatter is missing or invalid")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            fail(f"{path}: unsupported frontmatter line: {line}")
        values[key.strip()] = value.strip().strip("'\"")
    return values


def read_implicit_policy(path: Path) -> bool | None:
    if not path.exists():
        return None
    match = re.search(
        r"^\s*allow_implicit_invocation:\s*(true|false)\s*$",
        path.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if not match:
        return True
    return match.group(1) == "true"


def require_strings(item: dict[str, object], fields: tuple[str, ...], label: str) -> None:
    for field in fields:
        value = item.get(field)
        if not isinstance(value, str) or not value.strip():
            fail(f"{label}: {field} must be a non-empty string")


def main() -> None:
    if len(sys.argv) > 2:
        fail("Usage: validate_skill_catalog.py [repository_root]")
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parents[3]
    skills_root = root / ".agents" / "skills"
    catalog_path = skills_root / "catalog-routing-fixtures.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if catalog.get("schema_version") != 1:
        fail("catalog schema_version must be 1")

    groups = {entry.get("id") for entry in catalog.get("groups", []) if isinstance(entry, dict)}
    if groups != EXPECTED_GROUPS:
        fail(f"catalog groups must be {sorted(EXPECTED_GROUPS)}")

    entries = catalog.get("skills")
    if not isinstance(entries, list) or len(entries) != 21:
        fail("catalog must contain exactly 21 Skill entries")
    names: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            fail("each catalog Skill entry must be an object")
        require_strings(entry, ("name", "group", "intent", "side_effect", "manifest", "invocation", "primary_for", "boundary"), "catalog Skill")
        name = entry["name"]
        if name in names:
            fail(f"catalog has duplicate Skill name: {name}")
        names.add(name)
        if entry["group"] not in EXPECTED_GROUPS:
            fail(f"{name}: unknown group {entry['group']}")
        if entry["side_effect"] not in ALLOWED_SIDE_EFFECTS:
            fail(f"{name}: unknown side_effect {entry['side_effect']}")
        if entry["manifest"] not in {"required", "none"}:
            fail(f"{name}: manifest must be required or none")
        if entry["invocation"] not in {"implicit", "explicit-only"}:
            fail(f"{name}: invocation must be implicit or explicit-only")
        if "implicit_exception" not in entry:
            fail(f"{name}: implicit_exception must be present (string or null)")
        implicit_exception = entry["implicit_exception"]
        if implicit_exception is not None and (
            not isinstance(implicit_exception, str) or not implicit_exception.strip()
        ):
            fail(f"{name}: implicit_exception must be a non-empty string or null")
        requires_implicit_exception = (
            entry["side_effect"] != "read-only" and entry["invocation"] == "implicit"
        )
        if requires_implicit_exception and implicit_exception is None:
            fail(f"{name}: non-read-only implicit Skill requires implicit_exception")
        if not requires_implicit_exception and implicit_exception is not None:
            fail(f"{name}: implicit_exception is reserved for non-read-only implicit Skills")
        if not isinstance(entry.get("inputs"), list) or not entry["inputs"]:
            fail(f"{name}: inputs must be a non-empty array")
        if not isinstance(entry.get("outputs"), list) or not entry["outputs"]:
            fail(f"{name}: outputs must be a non-empty array")

        skill_dir = skills_root / name
        metadata = read_frontmatter(skill_dir / "SKILL.md")
        if metadata.get("name") != name:
            fail(f"{name}: catalog name and SKILL.md name disagree")
        if not metadata.get("description"):
            fail(f"{name}: SKILL.md must have a description")
        manifest = skill_dir / "agents" / "openai.yaml"
        if entry["manifest"] == "none":
            if manifest.exists():
                fail(f"{name}: catalog declares no manifest but openai.yaml exists")
        elif not manifest.exists():
            fail(f"{name}: catalog requires agents/openai.yaml")

        policy = read_implicit_policy(manifest)
        if entry["invocation"] == "explicit-only" and policy is not False:
            fail(f"{name}: explicit-only catalog entry needs allow_implicit_invocation: false")
        if entry["invocation"] == "implicit" and policy is False:
            fail(f"{name}: implicit catalog entry cannot disable implicit invocation")

    installed = {path.parent.name for path in skills_root.glob("*/SKILL.md")}
    if names != installed:
        fail(f"catalog and installed Skill directories disagree: catalog-only={sorted(names - installed)}, installed-only={sorted(installed - names)}")
    catalog_by_name = {entry["name"]: entry for entry in entries}

    explicit_entries = {entry["name"] for entry in entries if entry["invocation"] == "explicit-only"}
    if explicit_entries != EXPLICIT_ONLY_SKILLS:
        fail(f"explicit-only Skill set must be {sorted(EXPLICIT_ONLY_SKILLS)}")
    if {entry["name"] for entry in entries if entry["manifest"] == "none"} != {"document-search"}:
        fail("document-search must be the only manifest-less read-only exception")

    prompts = catalog.get("prompts")
    if not isinstance(prompts, list) or len(prompts) != 42:
        fail("catalog must contain 42 prompt fixtures (normal and boundary for each Skill)")
    prompt_ids: set[str] = set()
    prompt_kinds: dict[str, set[str]] = {name: set() for name in names}
    for prompt in prompts:
        if not isinstance(prompt, dict):
            fail("each prompt fixture must be an object")
        require_strings(
            prompt,
            ("id", "kind", "prompt", "expected_skill", "non_selected_skill"),
            "prompt fixture",
        )
        if prompt["id"] in prompt_ids:
            fail(f"duplicate prompt fixture id: {prompt['id']}")
        prompt_ids.add(prompt["id"])
        if prompt["kind"] not in {"normal", "boundary"}:
            fail(f"{prompt['id']}: kind must be normal or boundary")
        source, separator, _ = prompt["id"].rpartition("-")
        if not separator or source not in names:
            fail(f"{prompt['id']}: id must use <skill>-normal or <skill>-boundary")
        if prompt["kind"] != prompt["id"].rsplit("-", 1)[1]:
            fail(f"{prompt['id']}: id suffix and kind disagree")
        if prompt["expected_skill"] != "none" and prompt["expected_skill"] not in names:
            fail(f"{prompt['id']}: expected_skill is not installed")
        if prompt["non_selected_skill"] not in names:
            fail(f"{prompt['id']}: non_selected_skill is not installed")
        if prompt["non_selected_skill"] == prompt["expected_skill"]:
            fail(f"{prompt['id']}: expected and non-selected Skill must differ")
        allowed = prompt.get("implicit_invocation_allowed")
        if not isinstance(allowed, bool):
            fail(f"{prompt['id']}: implicit_invocation_allowed must be boolean")
        expected = prompt["expected_skill"]
        if expected == "none":
            if allowed:
                fail(f"{prompt['id']}: expected_skill none must not allow implicit invocation")
        else:
            expected_allows_implicit = catalog_by_name[expected]["invocation"] == "implicit"
            if allowed != expected_allows_implicit:
                fail(f"{prompt['id']}: implicit_invocation_allowed must match {expected}'s catalog invocation")
            if not allowed and f"${expected}" not in prompt["prompt"]:
                fail(f"{prompt['id']}: explicit-only expected Skill must be named as ${expected}")
        if prompt["kind"] == "normal":
            if prompt["expected_skill"] != source:
                fail(f"{prompt['id']}: normal fixture must select its source Skill")
        elif prompt["non_selected_skill"] != source:
            fail(f"{prompt['id']}: boundary fixture must identify its source Skill as non-selected")
        prompt_kinds[source].add(prompt["kind"])
    incomplete = sorted(name for name, kinds in prompt_kinds.items() if kinds != {"normal", "boundary"})
    if incomplete:
        fail(f"missing normal or boundary fixture for: {', '.join(incomplete)}")

    print("PASS: 21 Skills, manifests, and 42 routing fixtures are consistent")


if __name__ == "__main__":
    main()

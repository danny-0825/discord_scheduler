#!/usr/bin/env python3
"""Check the repository's executable AI-workflow contract without dependencies."""

from __future__ import annotations

import sys
import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None


EXPECTED_AGENTS = {
    "task-planner.toml": "task_planner",
    "impact-analyzer.toml": "impact_analyzer",
    "issue-reviewer.toml": "issue_reviewer",
    "docs-author.toml": "docs_author",
    "docs-reviewer.toml": "docs_reviewer",
    "implementation-worker.toml": "implementation_worker",
    "workflow-reviewer.toml": "workflow_reviewer",
}
RETIRED_TERMS = ("multi_agent_v1__", "fork_context")
RETIRED_ROLE_TERMS = (
    "task-planner",
    "impact-analyzer",
    "issue-reviewer",
    "docs-author",
    "docs-reviewer",
    "implementation-worker",
    "workflow-reviewer",
)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def source_files(root: Path) -> list[Path]:
    files = [root / "AGENTS.md", root / ".codex/config.toml"]
    for directory in (
        root / ".codex/agents",
        root / ".agents/skills/issue-to-pr-workflow",
        root / ".agents/skills/issue-to-pr-workflow-review",
        root / "docs/agents",
        root / "docs/workflows",
    ):
        files.extend(
            path
            for path in directory.rglob("*")
            if path.is_file() and path.suffix in {".md", ".toml"}
        )
    return files


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_toml_fallback(content: str) -> dict[str, object]:
    """Parse the small TOML subset used by the checked configuration files."""
    result: dict[str, object] = {}
    current = result
    in_multiline_string = False
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if in_multiline_string:
            if '"""' in line:
                in_multiline_string = False
            continue
        if not line or line.startswith("#"):
            continue
        if line.count('"""') == 1:
            in_multiline_string = True
            continue
        table = re.fullmatch(r"\[([A-Za-z0-9_-]+)\]", line)
        if table:
            current = result.setdefault(table.group(1), {})
            if not isinstance(current, dict):
                raise ValueError(f"table conflicts with scalar: {table.group(1)}")
            continue
        key, separator, raw_value = line.partition("=")
        if not separator or not re.fullmatch(r"[A-Za-z0-9_-]+", key.strip()):
            raise ValueError(f"unsupported TOML line: {raw_line}")
        value = raw_value.split("#", 1)[0].strip()
        if value == "true":
            parsed: object = True
        elif value == "false":
            parsed = False
        elif re.fullmatch(r"-?\d+", value):
            parsed = int(value)
        elif len(value) >= 2 and value[0] == value[-1] == '"':
            parsed = value[1:-1]
        else:
            raise ValueError(f"unsupported TOML value: {raw_value.strip()}")
        current[key.strip()] = parsed
    if in_multiline_string:
        raise ValueError("unterminated multiline string")
    return result


def parse_toml(content: str) -> dict[str, object]:
    if tomllib is not None:
        return tomllib.loads(content)
    return parse_toml_fallback(content)


def require(contents: str, fragment: str, label: str, failures: list[str]) -> None:
    if fragment not in contents:
        failures.append(f"{label} is missing required contract: {fragment}")


def main() -> int:
    root = repository_root()
    failures: list[str] = []
    config_path = root / ".codex/config.toml"
    try:
        config = parse_toml(read(config_path))
    except ValueError as error:
        failures.append(f"config.toml is not valid TOML: {error}")
        config = {}
    agents = config.get("agents")
    if not isinstance(agents, dict):
        failures.append("config.toml must define an [agents] table")
        agents = {}
    if agents.get("max_threads") != 8:
        failures.append(
            "config.toml must define agents.max_threads as integer 8, "
            f"found {agents.get('max_threads')!r}"
        )
    if agents.get("interrupt_message") is not True:
        failures.append(
            "config.toml must define agents.interrupt_message as boolean true, "
            f"found {agents.get('interrupt_message')!r}"
        )
    for key in ("enabled", "max_concurrent_threads_per_session"):
        if key in agents:
            failures.append(f"config.toml contains retired agents.{key} setting")

    agent_dir = root / ".codex/agents"
    actual_files = {path.name for path in agent_dir.glob("*.toml")}
    expected_files = set(EXPECTED_AGENTS)
    if actual_files != expected_files:
        failures.append(
            "custom agent definition files differ from the canonical seven: "
            f"expected {sorted(expected_files)}, found {sorted(actual_files)}"
        )
    seen_roles: set[str] = set()
    for filename, expected_role in EXPECTED_AGENTS.items():
        path = agent_dir / filename
        if not path.exists():
            continue
        try:
            parsed = parse_toml(read(path))
        except ValueError as error:
            failures.append(f"{filename} is not valid TOML: {error}")
            continue
        actual_role = parsed.get("name")
        if actual_role != expected_role:
            failures.append(
                f"{filename} must define name = {expected_role!r}, found {actual_role!r}"
            )
        if actual_role in seen_roles:
            failures.append(f"custom agent role is duplicated: {actual_role!r}")
        if isinstance(actual_role, str):
            seen_roles.add(actual_role)

    contents = "\n".join(read(path) for path in source_files(root))
    for term in RETIRED_TERMS:
        if term in contents:
            failures.append(f"retired runtime term remains: {term}")
    for term in RETIRED_ROLE_TERMS:
        if term in contents:
            failures.append(f"retired custom agent role spelling remains: {term}")
    workflow = read(root / ".agents/skills/issue-to-pr-workflow/SKILL.md")
    subagents = read(
        root / ".agents/skills/issue-to-pr-workflow/references/subagents.md"
    )
    review = read(root / ".agents/skills/issue-to-pr-workflow-review/SKILL.md")
    agent_docs = read(root / "docs/agents/codex-subagents.md")
    repository_rules = read(root / "AGENTS.md")
    require(workflow, "Plan機能が利用できる場合", "workflow", failures)
    require(workflow, "利用できない場合", "workflow", failures)
    require(workflow, "親Agentが最新`origin/develop`から専用branch/worktreeを作成・検証", "workflow", failures)
    require(subagents, "SubAgentは親Agentから割り当てられたpathとbranchだけを使い、worktreeを作成せず", "subagent contract", failures)
    require(subagents, "利用可能なコラボレーション機能", "subagent contract", failures)
    require(review, "書き込みTaskのworktreeは親Agentが最新基点から作成・検証", "workflow review", failures)
    require(agent_docs, "https://learn.chatgpt.com/docs/agent-configuration/subagents", "agent documentation", failures)
    for role in EXPECTED_AGENTS.values():
        require(subagents, f"### {role}", "subagent role table", failures)
        require(repository_rules, f"`{role}`", "repository rules", failures)

    if failures:
        print("workflow contract: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("workflow contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

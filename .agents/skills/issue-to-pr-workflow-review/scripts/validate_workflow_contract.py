#!/usr/bin/env python3
"""Check the repository's executable AI-workflow contract without dependencies."""

from __future__ import annotations

import json
from pathlib import Path
RETIRED_TERMS = ("multi_agent_v1__", "fork_context")
STATES = {
    "planned", "investigated", "issue_ready", "issue_reviewed",
    "environment_provisioned", "docs_ready", "docs_waived", "implemented",
    "verified", "committed", "pushed", "pr_open", "pr_reviewed", "merged",
    "cleaned", "blocked", "failed",
}
REQUIRED_SCENARIOS = {
    "normal", "no-plan", "no-subagent", "docs-waived", "scope-violation",
    "external-denied", "independent-tasks", "dependent-task", "worktree-isolation",
}
ALLOWED_TRANSITIONS = {
    ("planned", "investigated"), ("planned", "blocked"), ("blocked", "planned"),
    ("investigated", "issue_ready"),
    ("issue_ready", "issue_reviewed"), ("issue_ready", "failed"),
    ("failed", "issue_ready"), ("issue_reviewed", "environment_provisioned"),
    ("issue_reviewed", "blocked"), ("blocked", "issue_reviewed"),
    ("issue_reviewed", "failed"), ("failed", "issue_reviewed"),
    ("environment_provisioned", "docs_ready"), ("environment_provisioned", "docs_waived"),
    ("environment_provisioned", "blocked"), ("blocked", "environment_provisioned"),
    ("environment_provisioned", "failed"), ("docs_ready", "implemented"),
    ("docs_ready", "investigated"), ("docs_waived", "implemented"),
    ("docs_waived", "investigated"), ("implemented", "verified"),
    ("implemented", "failed"), ("implemented", "investigated"),
    ("failed", "implemented"), ("verified", "committed"), ("verified", "blocked"),
    ("blocked", "verified"), ("committed", "pushed"), ("pushed", "pr_open"),
    ("pr_open", "pr_reviewed"), ("pr_reviewed", "merged"), ("merged", "cleaned"),
}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(contents: str, fragment: str, label: str, failures: list[str]) -> None:
    if fragment not in contents:
        failures.append(f"{label} is missing required contract: {fragment}")


def validate_scenarios(scenarios: object) -> list[str]:
    """Validate positive fixture evidence and reject unknown state-machine edges."""
    failures: list[str] = []
    if not isinstance(scenarios, list):
        return ["workflow state fixtures must contain scenarios"]
    by_id = {item.get("id"): item for item in scenarios if isinstance(item, dict)}
    if set(by_id) != REQUIRED_SCENARIOS or len(by_id) != len(scenarios):
        failures.append(f"workflow scenarios must be exactly {sorted(REQUIRED_SCENARIOS)}")
    for scenario_id, scenario in by_id.items():
        expected = scenario.get("expected_state")
        transitions = scenario.get("transitions")
        if expected not in STATES:
            failures.append(f"{scenario_id}: invalid expected_state {expected!r}")
        if not isinstance(transitions, list) or not transitions:
            failures.append(f"{scenario_id}: transitions must be a non-empty list")
        elif transitions[-1] != expected:
            failures.append(f"{scenario_id}: last transition must match expected_state")
        elif any(state not in STATES for state in transitions):
            failures.append(f"{scenario_id}: transitions contain an unknown state")
        elif any(pair not in ALLOWED_TRANSITIONS for pair in zip(transitions, transitions[1:])):
            failures.append(f"{scenario_id}: transitions contain an unsupported edge")

    def nonempty(scenario_id: str, *fields: str) -> None:
        scenario = by_id.get(scenario_id, {})
        for field in fields:
            if not isinstance(scenario.get(field), str) or not scenario[field].strip():
                failures.append(f"{scenario_id}: {field} must be a non-empty string")

    normal = by_id.get("normal", {})
    if normal.get("plan_available") is not True or normal.get("subagent_available") is not True:
        failures.append("normal: Plan and SubAgent must be available")
    if normal.get("effect_gate") != "approved" or normal.get("external_runner_invoked") is not False:
        failures.append("normal: safe dry-run must model an approved gate without external runner")
    recovery_paths = normal.get("recovery_paths")
    expected_recovery_paths = {
        "issue-review-failure": ["issue_ready", "failed", "issue_ready"],
        "environment-failure": ["issue_reviewed", "failed", "issue_reviewed"],
        "docs-ready-change": ["docs_ready", "investigated"],
        "docs-waived-change": ["docs_waived", "investigated"],
    }
    if recovery_paths != expected_recovery_paths:
        failures.append("normal: must cover the issue, environment, and docs recovery paths")

    no_plan = by_id.get("no-plan", {})
    if (no_plan.get("plan_available") is not False
            or no_plan.get("fallback_record") != "chat-or-issue"
            or no_plan.get("expected_state") != "issue_reviewed"
            or no_plan.get("transitions") != ["planned", "blocked", "planned", "investigated", "issue_ready", "issue_reviewed"]):
        failures.append("no-plan: must block, record chat-or-issue fallback, resume planned, and reach issue_reviewed")

    no_subagent = by_id.get("no-subagent", {})
    if no_subagent.get("subagent_available") is not False or no_subagent.get("execution_owner") != "parent_agent":
        failures.append("no-subagent: must fall back to parent_agent")

    docs_waived = by_id.get("docs-waived", {})
    nonempty("docs-waived", "waiver_reason", "waiver_owner", "waiver_rationale")
    if docs_waived.get("expected_state") != "implemented":
        failures.append("docs-waived: must continue to implemented")

    scope = by_id.get("scope-violation", {})
    if (scope.get("expected_state") != "investigated"
            or scope.get("work_stopped") is not True
            or scope.get("reinvestigation_required") is not True):
        failures.append("scope-violation: must stop and return to investigated")

    denied = by_id.get("external-denied", {})
    if (denied.get("expected_state") != "blocked" or denied.get("effect_gate") != "denied"
            or denied.get("external_runner_invoked") is not False
            or denied.get("resume_state") != "verified"
            or denied.get("recovery_path") != ["verified", "blocked", "verified"]):
        failures.append("external-denied: must block without an external runner and resume at verified")

    independent = by_id.get("independent-tasks", {})
    nonempty("independent-tasks", "failed_task", "unrelated_task")
    if independent.get("unrelated_task_continues") is not True:
        failures.append("independent-tasks: unrelated task must continue")

    dependent = by_id.get("dependent-task", {})
    nonempty("dependent-task", "dependency", "block_reason")
    if dependent.get("dependency_satisfied") is not False or dependent.get("expected_state") != "blocked":
        failures.append("dependent-task: unmet dependency must block")

    isolation = by_id.get("worktree-isolation", {})
    if (isolation.get("parent_provisions") is not True
            or isolation.get("distinct_worktrees") is not True
            or isolation.get("distinct_write_scopes") is not True):
        failures.append("worktree-isolation: parent provisioning and distinct resources are required")
    for field in ("worktrees", "write_scopes"):
        values = isolation.get(field)
        if not isinstance(values, list) or len(values) != 2 or not all(isinstance(value, str) and value for value in values) or values[0] == values[1]:
            failures.append(f"worktree-isolation: {field} must contain two distinct non-empty values")
    return failures


def validate_state_contract(root: Path, failures: list[str]) -> None:
    contract = read(root / ".agents/skills/issue-to-pr-workflow/references/state-contract.md")
    for state in STATES:
        require(contract, state, "state contract", failures)
    for fragment in (
        "任意遷移ではない", "issue_ready -> failed -> issue_ready",
        "issue_reviewed -> failed -> issue_reviewed", "implemented -> failed -> implemented",
        "verified -> blocked -> verified", "implemented -> investigated",
        "docs_ready -> investigated", "docs_waived -> investigated",
    ):
        require(contract, fragment, "state contract", failures)
    fixture_path = root / ".agents/skills/issue-to-pr-workflow-review/references/workflow-state-fixtures.json"
    try:
        fixtures = json.loads(read(fixture_path))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"workflow state fixtures are invalid: {error}")
        return
    scenarios = fixtures.get("scenarios") if isinstance(fixtures, dict) else None
    failures.extend(validate_scenarios(scenarios))
    if not isinstance(scenarios, list):
        return

    # Prove assertions are live: each required acceptance field is removed from an
    # in-memory copy, and an undefined edge is injected. Both must fail validation.
    negative_fields = (
        ("no-plan", "fallback_record"), ("docs-waived", "waiver_reason"),
        ("scope-violation", "work_stopped"), ("external-denied", "external_runner_invoked"),
        ("independent-tasks", "unrelated_task_continues"), ("dependent-task", "block_reason"),
        ("worktree-isolation", "write_scopes"), ("normal", "recovery_paths"),
    )
    for scenario_id, field in negative_fields:
        copy = json.loads(json.dumps(scenarios))
        next(item for item in copy if item["id"] == scenario_id).pop(field)
        if not validate_scenarios(copy):
            failures.append(f"negative self-test did not reject {scenario_id}.{field}")
    invalid_edge = json.loads(json.dumps(scenarios))
    next(item for item in invalid_edge if item["id"] == "normal")["transitions"] = ["planned", "cleaned"]
    if not validate_scenarios(invalid_edge):
        failures.append("negative self-test did not reject an undefined transition")
    missing_plan_block = json.loads(json.dumps(scenarios))
    next(item for item in missing_plan_block if item["id"] == "no-plan")["transitions"] = ["planned", "investigated", "issue_ready", "issue_reviewed"]
    if not validate_scenarios(missing_plan_block):
        failures.append("negative self-test did not require planned -> blocked -> planned fallback")


def main() -> int:
    root = repository_root()
    failures: list[str] = []
    workflow_files = (
        root / ".agents/skills/issue-to-pr-workflow/SKILL.md",
        root / ".agents/skills/issue-to-pr-workflow/references/state-contract.md",
        root / ".agents/skills/issue-to-pr-workflow/references/subagents.md",
        root / ".agents/skills/issue-to-pr-workflow-review/SKILL.md",
        root / "docs/skills/catalog.md",
        root / "docs/workflows/issue-to-pr.md",
    )
    contents = "\n".join(read(path) for path in workflow_files)
    for term in RETIRED_TERMS:
        if term in contents:
            failures.append(f"retired runtime term remains: {term}")
    workflow = read(root / ".agents/skills/issue-to-pr-workflow/SKILL.md")
    subagents = read(
        root / ".agents/skills/issue-to-pr-workflow/references/subagents.md"
    )
    review = read(root / ".agents/skills/issue-to-pr-workflow-review/SKILL.md")
    catalog = read(root / "docs/skills/catalog.md")
    require(workflow, "Plan機能が使えない場合", "workflow", failures)
    require(workflow, "親Agentだけが行う", "workflow", failures)
    require(workflow, "専用branch/worktree", "workflow", failures)
    require(subagents, "SubAgentは親Agentから割り当てられたpathとbranchだけを使い、worktreeを作成せず", "subagent contract", failures)
    require(subagents, "利用可能なコラボレーション機能", "subagent contract", failures)
    require(review, "状態遷移", "workflow review", failures)
    require(catalog, "親Agentだけがeffect gate", "catalog", failures)
    if "T50所有の暫定例外" in catalog:
        failures.append("catalog retains the retired T50 provisional exception")

    validate_state_contract(root, failures)

    if failures:
        print("workflow contract: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("workflow contract: PASS (state contract and negative fixture coverage)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

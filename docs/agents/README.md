---
type: agent
status: active
tags:
  - docs/agent
related:
  - "[[docs/governance/obsidian-docs]]"
  - "[[docs/index]]"
updated: 2026-09-13
---

# Agent docs

Agent docsは、親AgentとSubAgentの責務を分離し、並列実行時の書き込み範囲と外部変更権限を明確にする。

## 必須項目

- Agentの役割
- 担当フェーズと入力・出力
- 読み取り範囲・書き込み範囲
- Issue、PR、commit、pushの権限
- 依存関係と並列実行ルール
- 失敗時の継続・停止条件
- 検証方法と親Agentへの報告形式

## Codex固有のSubAgent

実際の起動・状態管理・終了は[Codex SubAgent運用](codex-subagents.md)と`.agents/skills/issue-to-pr-workflow/references/subagents.md`に従う。役割名の記載だけではSubAgentを起動したことにならない。

## 正規Custom Agent role

`task_planner`、`impact_analyzer`、`issue_reviewer`、`docs_author`、`docs_reviewer`、`implementation_worker`、`workflow_reviewer`を`.codex/agents/`で定義する。Issue・PR作成と実装・PRレビューは、必要な場合に親AgentまたはTaskごとに指定した担当が行う。書き込みTaskのbranch/worktreeは親Agentが準備・検証してから割り当てる。

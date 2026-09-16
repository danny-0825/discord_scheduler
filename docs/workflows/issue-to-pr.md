---
type: workflow
status: active
tags:
  - docs/workflow
related:
  - "[[docs/governance/obsidian-docs]]"
  - "[[docs/workflows/docs-maintenance]]"
updated: 2026-09-17
---

# IssueからPRまでの開発Workflow

## 開始条件

チャットやIssueで実装・docs・設定の変更要求を受け、作業範囲と完了条件を定義できること。

## 概要

実行は`planned`から開始し、read-onlyの調査・Issue reviewを終えてからだけ親Agentが専用環境を準備する。docsはreview済みの`docs_ready`、または理由・判断者・根拠を記録した`docs_waived`のどちらかを経て実装する。検証後のcommit、push、PR、merge、cleanupは親Agentのeffect gateを通す。

Plan機能がない場合は、チャットまたはIssueにTask、DAG、scope、担当、完了条件、停止条件を構造化して残す。SubAgentの能力がない場合は親Agentが直列実行し、起動済みとは表示しない。

## 利用時の確認

- `issue_reviewed`までリポジトリ、branch、worktree、commit、pushを変更しない。
- 親Agentが基点、Task専用branch/worktree、write scopeを検証してから書込み担当へ渡す。
- scopeまたはdocs要否が変われば調査へ戻る。scope外の変更は停止して再レビューする。
- 外部操作は対象・内容・権限が記録され、拒否または能力不足では実行せず`blocked`とする。
- Workflow変更時は契約fixture、pre-branch gate、worktree isolation、docs linkを検証する。

状態遷移、証跡、再開条件、SubAgent受渡し、Git/GitHub能力確認、レビューコメント形式の正規情報源は[issue-to-pr-workflow Skill](../../.agents/skills/issue-to-pr-workflow/SKILL.md)である。

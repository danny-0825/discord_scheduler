---
name: issue-to-pr-workflow
description: 開発要求を状態契約に沿ってIssueからPRまで進める。Task分解、read-only調査、親Agentによる環境準備、委譲、検証、外部操作のgateが必要なときに使用する。
---

# Issue to PR Workflow

## 役割

このSkillは開発要求の主routeであり、唯一の実行状態契約である。恒久原則は`AGENTS.md`、Task固有の役割I/Oは`.codex/agents/`、利用者向けの短い概要は[docs/workflows/issue-to-pr.md](../../../docs/workflows/issue-to-pr.md)に置く。この本文はそれらの手順を複製しない。

実行前に[状態契約](references/state-contract.md)を読み、Task、依存、scope、担当、完了条件をPlanへ記録する。Plan機能が使えない場合は、同じ必須項目をチャットまたはIssueへ構造化して記録する。どちらもない場合は`planned`のまま停止する。

## 必須gate

- `issue_reviewed`まではread-onlyである。調査・Issue作成・Issueレビューの成果物はPlanまたはIssueへ記録し、リポジトリ、branch、worktree、commit、pushは変更しない。
- `environment_provisioned`への遷移は親Agentだけが行う。親AgentはGitの更新・基点確認・専用branch/worktree作成を実行できる能力を確認し、基点SHA、path、branch、write scopeを記録してから割り当てる。
- SubAgent機能を使えない場合は起動済みと扱わず、親Agentが同じscopeで直列実行する。利用可能な場合だけ実際に起動し、結果とscopeを親が照合する。
- commit、push、Issue/PR作成、コメント、マージ、cleanupは外部effectであり、親Agentだけが[effect gate](references/state-contract.md#external-effect-gate)を通して実行する。対象・内容・権限が揃わない、または拒否された場合はrunnerを呼ばず`blocked`にする。
- scope、docs要否、依存、完了条件が変わった場合は作業を保留し、`investigated`へ戻って再調査・再レビューする。scope外の変更を黙って続行しない。

## 参照と検証

- 状態・遷移・証跡・再開: [state-contract.md](references/state-contract.md)
- Task/Issue/Agent/branch/worktree/PRの対応とDAG: [relationship-and-independence.md](references/relationship-and-independence.md)
- SubAgentの能力fallbackと受渡し: [subagents.md](references/subagents.md)
- フェーズ別の成果物: [phases.md](references/phases.md)
- Git/GitHubの能力確認: [github-cli-auth.md](references/github-cli-auth.md)
- Workflow変更の監査: [issue-to-pr-workflow-review](../issue-to-pr-workflow-review/SKILL.md)

レビュー対象は[issue-review](../issue-review/SKILL.md)、[docs-review](../docs-review/SKILL.md)、[implementation-review](../implementation-review/SKILL.md)へ分離する。Workflowを変更した場合、契約validator、pre-branch gate、safe worktree smoke test、docs link checkを実行し、🔴が残る間は次へ進まない。

## 停止条件

- Task、依存、scope、担当、完了条件の記録が不足している
- Issue reviewの🔴、基点SHA、親が準備した専用環境のいずれかが確認できない
- 外部effectの対象・内容・権限が不足または拒否されている
- scope外の変更、依存未達、必要な検証失敗がある
- レビュー指摘の優先度を判断できない
- テスト失敗の原因を特定できない

各フェーズの終了時に、実施内容、対象URLや番号、テスト結果、未解決事項、次に必要な承認を簡潔に報告する。

---
name: issue-to-pr-workflow-review
description: Issue-to-PR Workflow自体が、Issue分割、SubAgent、worktree、branch、commit、PR、レビュー、マージまで期待どおりに実行できるかを検証する。Workflow変更時や並列タスクの計画時に使用する。
---

# Issue-to-PR Workflow Review

## 目的

製品コードのレビューではなく、[issue-to-pr-workflow](../issue-to-pr-workflow/SKILL.md)の実行契約をレビューする。文書に役割名があるだけでなく、観測可能な成果物と状態遷移が得られるかを確認する。

## 適用条件

次のいずれかに該当する場合に使用する。

- issue-to-pr-workflowまたは参照資料を変更した
- 1つのチャット入力から2つ以上のIssueへ分割する
- SubAgentを並列起動する
- 複数のworktree、branch、PRを扱う
- Workflowが期待どおりに動作したかを監査する

単一タスクの通常実装では、適用しない理由を記録して省略できる。

## 必須不変条件

| ID | 不変条件 | 証跡 |
| --- | --- | --- |
| WF-1 | 独立タスクごとに1 Issue・1 branch・1 worktree・1 PRが対応する | タスク対応表、GitHub URL、branch、worktree一覧 |
| WF-2 | 並列SubAgentは互いに異なるworktreeと書き込み範囲を持つ | Agent ID、worktree path、書き込み範囲 |
| WF-3 | worktreeは担当SubAgentが最新基点から作成し、親Agentが結果を検証する | `git fetch origin`、`git worktree add`、検証ログ |
| WF-4 | 依存タスクは前提PRのマージ後に最新基点から開始する | 依存グラフ、merge commit、基点SHA |
| WF-5 | 失敗したタスクに依存しないタスクは継続する | 成功・失敗・blockedの状態表 |
| WF-6 | PR作成担当はタスクごとに1 Agentだけである | 権限割当表、PR URL |
| WF-7 | PRマージ後に専用worktreeと不要なbranchを削除する | `git worktree list`、branch一覧 |

## 実行手順

1. 対象Workflow、Issue、Task ID、SubAgent実行計画を読み込む。
2. タスクをDAGにし、独立・依存・競合ファイル・担当Agentを表にする。
3. 各タスクのIssue／branch／worktree／PRを1対1で割り当てる。1つのPRへ複数の独立Issueをまとめる計画は🔴とする。
4. SubAgentに専用worktree path、branch名、書き込み範囲、PR担当権限を渡す。SubAgentは自分のworktreeで`git fetch origin`後に`git worktree add`を実行する。
5. [checklist.md](references/checklist.md)で静的レビューを行う。
6. [test-scenarios.md](references/test-scenarios.md)のdry-runを実行し、必要なら`smoke_test.sh`でworktree分離を検証する。
7. 実行中のAgent ID、状態、成果物、失敗、終了を記録する。起動していないAgentを起動済みと扱わない。
8. 外部GitHub状態を変更するlive auditは、ユーザーが許可した場合だけ行う。通常はdry-runで止める。
9. 🔴がなくなるまでWorkflow定義を修正して再レビューする。

## SubAgentへのworktree契約

親Agentは次のレコードをSubAgentごとに渡す。

```text
Task ID: T1
Issue: #123
Base: origin/develop
Branch: feature/123-short-description
Worktree: ../discord_scheduler-worktrees/123-short-description
Write scope: docs/workflows/**
PR owner: docs-author
Forbidden: 他タスクのworktree、branch、Issue、PR、書き込み範囲外のファイル
```

SubAgentは、担当worktreeを自分で作成し、そこでdocs・実装・commitを行う。PR担当Agentだけがpush・PR作成を行う。親Agentは作業開始前にworktreeとbranchの一意性を、完了後に差分とworktree削除を検証する。

## レビュー結果

通常のIssue／PRレビューと同じく、先頭に前回指摘の解消状況表と新規指摘表を置き、指摘詳細に問題、理由、修正案、確認方法を含める。指摘IDは対象Issue番号を接頭辞にする。🔴がある場合はWorkflowを合格扱いにしない。

## 停止条件

- IssueとPRの1対1対応を確認できない
- SubAgentのworktree、branch、書き込み範囲が一意でない
- 前提PRのマージまたは最新基点を確認できない
- 外部GitHub変更の許可がない
- スモークテストまたは必要な検証が失敗した

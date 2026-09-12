---
name: issue-to-pr-workflow-review
description: Issue-to-PR Workflow自体が、Issue分割、SubAgent、worktree、branch、commit、PR、レビュー、マージまで期待どおりに実行できるかを検証する。Workflow変更時や並列タスクの計画時に使用する。
---

# Issue-to-PR Workflow Review

## 目的

製品コードのレビューではなく、[issue-to-pr-workflow](../issue-to-pr-workflow/SKILL.md)の実行契約をレビューする。文書に役割名があるだけでなく、Issue、SubAgent、branch、worktree、commit、PRの関係、観測可能な成果物、状態遷移が得られるかを確認する。

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
| WF-8 | Issue間の依存・競合・関連が実行計画にあり、依存グラフがDAGである | 関係表、依存グラフ、未定義・循環参照チェック |
| WF-9 | IssueとSubAgentが`implements`、レビュー担当が`validates`で一意に対応する | Task/Issue/Agent対応表、Agent ID、権限表 |
| WF-10 | SubAgent同士のread/write scope、共有資源、成果物が比較され、競合が直列化されている | scope比較表、競合判定、実行方式 |
| WF-11 | Taskの成果物、commit、PRが担当Issueの完了条件へ追跡できる | traceability表、closing keyword、commit/PR |
| WF-12 | Issue作成前にdocs、コード、テスト、設定、外部依存を調査し、未確認を推測で確定しない | 影響範囲表、調査状態、リスク、再調査記録 |
| WF-13 | `docs/context`が正規docsと役割分担し、registry・鮮度・Task lifecycleを追跡できる | context index/registry、source-of-truth、active/archive、外部メタデータ |
| WF-14 | pre-branchのフェーズ1〜5でリポジトリ変更が発生しない | 開始時・branch gate前のstatus/diff、Agent権限、Issue記録 |
| WF-15 | branch gateがIssueレビュー完了、最新基点、専用branch/worktreeを検証してからwriteを許可する | Issueレビュー結果、fetchログ、基点SHA、branch/worktree一覧 |
| WF-16 | 作業開始時にPlanモードでTask、依存、scope、担当、フェーズ完了条件を確定する | Plan、Issue、関係表、フェーズ更新履歴 |
| WF-17 | 実際の変更がPlanのwrite scope内で、forbidden scopeを変更していない | Planのscope、git diff、SubAgent報告、レビュー結果 |

## 実行手順

1. 対象Workflow、Issue、Task ID、SubAgent実行計画、Issue／PR本文、SubAgent threadの状態を読み込む。Codex公式にないJSON台帳の存在は必須条件にしない。
2. [relationship-and-independence.md](../issue-to-pr-workflow/references/relationship-and-independence.md) の実行計画で、Task/Issue/Agent/branch/worktree/commit/PRを対応付ける。
3. Issue作成前の影響範囲表を確認し、docs、Skill、Agent、コード、テスト、設定、生成物、CI/CD、DB、外部サービスの更新要否と調査状態を比較する。`未確認`を推測で`confirmed`にした場合は🔴とする。
4. `docs/context`を変更する場合、正規情報源との境界、registry、外部情報の出典・鮮度、Task contextのactive/archiveを確認する。重複仕様、出典不明、アーカイブ漏れは🔴とする。
   Skillの構造検証は、まずリポジトリ同梱の`./scripts/validate_skill_stdlib.py <skill-directory>`をPython標準ライブラリだけで実行する。外部の公式validatorは利用可能な場合の追加検証とし、依存不足だけでレビューを未完了にしない。
5. タスクをDAGにし、Issue間の依存・競合・関連、SubAgent間のscopeと共有資源を比較する。循環、未定義参照、所有者不在は🔴とする。
6. pre-branchの実行履歴にリポジトリ変更、commit、branch/worktree作成、pushがないことを確認する。差分がある場合は🔴とし、原因を特定するまでwriteフェーズへ進めない。
7. branch gateのIssueレビュー完了、最新基点SHA、専用branch/worktree、write scopeを確認する。いずれかが欠ける場合は🔴とする。
8. PlanモードのTask、scope、担当、依存、各フェーズの完了条件が確定しているか確認する。Plan未確定は🔴とする。
9. 各タスクのIssue／branch／worktree／PRを1対1で割り当てる。1つのPRへ複数の独立Issueをまとめる計画は🔴とする。
10. SubAgentに専用worktree path、branch名、read/write/forbidden scope、依存・後続Task、PR担当権限を渡す。SubAgentは自分のworktreeで`git fetch origin`後に`git worktree add`を実行する。
11. [checklist.md](references/checklist.md)で静的レビューを行う。
12. [test-scenarios.md](references/test-scenarios.md)のdry-runを実行し、必要なら`smoke_test.sh`と`pre_branch_gate_test.sh`でゲート、scope、worktree分離を検証する。
13. 実行中のAgent ID、状態、成果物、失敗、終了を記録する。起動していないAgentを起動済みと扱わない。
14. 外部GitHub状態を変更するlive auditは、ユーザーが許可した場合だけ行う。通常はdry-runで止める。
15. 🔴がなくなるまでWorkflow定義を修正して再レビューする。

Task、Issue、Agent、成果物の対応が確認できない場合は、Issue/docs/実装レビューを完了扱いにしない。

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

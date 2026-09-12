---
type: workflow
status: active
tags:
  - docs/workflow
related:
  - "[[docs/governance/obsidian-docs]]"
  - "[[docs/workflows/docs-maintenance]]"
updated: 2026-09-13
---

# IssueからPRまでの開発Workflow

## 開始条件

チャットやIssueで実装・docs・設定の変更要求を受け、作業範囲と完了条件を定義できること。

## 手順

### Pre-branch（read-only）

1. 要望をタスクへ分解し、独立性と依存関係を判定する。
2. タスクごとにIssue、SubAgent、write scope、ブランチ、worktree、PRの対応を決める。
3. BM25検索と読み取り調査で影響範囲・依存関係を確認し、候補ファイルと修正方針を記録する。
4. 影響範囲表へ更新要否、関連テスト、外部影響、依存・競合、担当・write scope、調査状態を記録する。
5. Issueを日本語で作成し、影響範囲、リスク、Assignee、Labels、Milestone、Project等を確認する。
6. Issueをレビューし、🔴がなくなるまでIssue本文・コメントだけを修正・再レビューする。

この段階では、コード、docs、Skill、Agent、設定、テスト、branch、worktree、commit、pushを変更しない。

### Branch gate後（write）

7. Issueレビュー完了後、`git fetch origin`で最新`origin/develop`を確認し、専用branchとworktreeを作成する。
8. Issueを元にObsidian templateから要件・設計docsを作成し、Properties・Wikilink・backlinkを設定する。必要に応じて`docs/context/task/active/<IssueNo>/`へ作業判断を記録してdocsレビューを行う。
9. 実装・テスト・実装レビューを行い、🔴がなくなるまで修正する。
10. 日本語説明のcommitを作成し、pushする。
11. Issueのclosing keywordを含む日本語PRを作成し、Assignee、Labels、Milestone、Development、Reviewersを確認する。
12. PRレビュー、修正、再レビューを行う。
13. マージ後にIssue、PR、worktree、更新履歴を確認する。

Issue、docs、実装、レビューで対象範囲や依存関係が変わった場合は、影響範囲調査へ戻って表と実行計画を更新する。

## 完了条件

- Issue、docs、実装、PRのレビューで🔴がない
- テストと静的解析の結果が記録されている
- PRがマージされ、関連IssueとProject連携の状態が確認されている
- `docs/changelog.md`に変更履歴がある

詳細なSubAgent、指摘ID、GitHub CLI、コメント投稿形式は`.agents/skills/issue-to-pr-workflow/`を参照する。

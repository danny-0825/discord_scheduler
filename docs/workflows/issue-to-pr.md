# IssueからPRまでの開発Workflow

## 開始条件

チャットやIssueで実装・docs・設定の変更要求を受け、作業範囲と完了条件を定義できること。

## 手順

1. 要望をタスクへ分解し、独立性と依存関係を判定する。
2. タスクごとにIssue、ブランチ、worktree、PRの対応を決める。
3. Issueを日本語で作成し、Assignee、Labels、Milestone、Project等を確認する。
4. Issueをレビューし、🔴がなくなるまで修正・再レビューする。
5. 最新の`origin/develop`からブランチと専用worktreeを作成する。
6. Issueを元に要件・設計docsを作成し、docsレビューを行う。
7. 実装・テスト・実装レビューを行い、🔴がなくなるまで修正する。
8. 日本語説明のcommitを作成し、pushする。
9. Issueのclosing keywordを含む日本語PRを作成し、Assignee、Labels、Milestone、Development、Reviewersを確認する。
10. PRレビュー、修正、再レビューを行う。
11. マージ後にIssue、PR、worktree、更新履歴を確認する。

## 完了条件

- Issue、docs、実装、PRのレビューで🔴がない
- テストと静的解析の結果が記録されている
- PRがマージされ、関連IssueとProject連携の状態が確認されている
- `docs/changelog.md`に変更履歴がある

詳細なSubAgent、指摘ID、GitHub CLI、コメント投稿形式は`.codex/skills/issue-to-pr-workflow/`を参照する。

# IssueからPRまでの開発Workflow

## 開始条件

チャットやIssueで実装・docs・設定の変更要求を受け、作業範囲と完了条件を定義できること。

## 手順

1. 要望をタスクへ分解し、独立性と依存関係を判定する。
2. タスクごとにIssue、ブランチ、worktree、PRの対応を決める。
3. Issue作成前に[document-search Skill](../../.agents/skills/document-search/SKILL.md)でdocs・`docs/context`・関連SkillをBM25検索し、候補本文を確認したうえで、コード、テスト、設定、生成物、CI/CD、外部サービスの影響範囲と依存関係を調査する。
4. 影響範囲表へ更新要否、関連テスト、外部影響、依存・競合、担当・write scope、調査状態を記録する。
5. Issueを日本語で作成し、影響範囲、リスク、Assignee、Labels、Milestone、Project等を確認する。
6. Issueをレビューし、🔴がなくなるまで修正・再レビューする。
7. 最新の`origin/develop`からブランチと専用worktreeを作成する。
8. Issueを元に要件・設計docsを作成し、必要に応じて`docs/context/task/active/<IssueNo>/`へ作業判断を記録してdocsレビューを行う。
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

# docsを追加・更新するWorkflow

## 手順

1. 目的と読者を明確にし、`docs/governance/docs-governance.md`の分類を決める。
2. 既存docsを検索し、重複ではなく既存docsへの追記・リンクで解決できるか確認する。
3. 必要なら要件定義書、詳細設計書、Workflow docsの順に作成する。
4. `docs/index.md`または分類ディレクトリの入口からリンクする。
5. docsレビューでIssueとの整合性、実装可能性、リンク、セキュリティを確認する。
6. `docs/changelog.md`へ日付、分類、概要、関連Issue/PRを追記する。

## 完了条件

- docsの分類、読者、関連Issueが明確
- 入口から参照できる
- docsレビューで🔴がない
- 更新履歴が追加されている

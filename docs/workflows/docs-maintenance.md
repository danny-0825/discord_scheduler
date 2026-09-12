# docsを追加・更新するWorkflow

## 手順

1. 目的と読者を明確にし、`docs/governance/docs-governance.md`の分類を決める。
2. Issue作成前に、既存docs、`docs/context`、Skill、Agent、コード、テスト、設定、生成物、CI/CD、外部サービスへの影響範囲と依存関係を調査する。
3. 影響範囲表へ更新要否、関連テスト、外部影響、依存・競合、担当・write scope、調査状態（`confirmed／未確認／対象外`）を記録する。
4. [document-search Skill](../../.agents/skills/document-search/SKILL.md)で既存docsをBM25検索し、上位候補の本文と正規情報源を確認する。重複ではなく既存docsへの追記・リンクで解決できるか判断する。
5. 必要なら要件定義書、詳細設計書、Workflow docsの順に作成する。
6. contextを追加・更新する場合は、正規情報源を複製せず、registryと鮮度・アーカイブ情報を更新する。
7. `docs/index.md`または分類ディレクトリの入口からリンクする。
8. docsレビューでIssueとの整合性、影響範囲、実装可能性、リンク、セキュリティを確認する。
9. 対象範囲や依存関係が変わった場合は、影響範囲を再調査し、表とIssueを更新する。
10. `docs/changelog.md`へ日付、分類、概要、関連Issue/PRを追記する。

### 影響範囲表

| Task | 対象 | 影響内容 | 更新要否 | 関連テスト | 外部影響 | 依存・競合 | 担当・write scope | 調査状態 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | `docs/foo.md` | 参照元・関連コード・利用手順 | 必須／不要 | docs検証 | なし／内容 | なし／依存／競合 | Agent・scope | confirmed／未確認／対象外 |

## 完了条件

- docsの分類、読者、関連Issueが明確
- 入口から参照できる
- docsレビューで🔴がない
- 更新履歴が追加されている

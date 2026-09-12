---
type: workflow
status: active
tags:
  - docs/workflow
related:
  - "[[docs/governance/obsidian-docs]]"
  - "[[docs/skills/README]]"
updated: 2026-09-13
---

# docsを追加・更新するWorkflow

## 手順

1. Issue作成前に、既存docs、`docs/context`、Skill、Agent、コード、テスト、設定、生成物、CI/CD、外部サービスへの影響範囲と依存関係をread-onlyで調査する。
2. 目的と読者を明確にし、`docs/governance/docs-governance.md`の分類を決める。
3. Issueレビュー完了後に親Agentが専用branch/worktreeを準備してから、ObsidianでVaultを開き、[`docs/templates/document-template.md`](../templates/document-template.md)から新規docsを作成する。目的、読者、`type`、`status`、`tags`、`related`、`updated`を設定する。
4. 影響範囲表へ更新要否、関連テスト、外部影響、依存・競合、担当・write scope、調査状態（`confirmed／未確認／対象外`）を記録する。
5. [document-search Skill](../../.agents/skills/document-search/SKILL.md)で既存docsをBM25検索し、上位候補の本文と正規情報源を確認する。重複ではなく既存docsへの追記・リンクで解決できるか判断する。
6. 必要なら要件定義書、詳細設計書、Workflow docsの順に作成する。
7. contextを追加・更新する場合は、正規情報源を複製せず、registryと鮮度・アーカイブ情報を更新する。
8. `docs/index.md`または分類ディレクトリのMOCからWikilinkで辿れるようにする。
9. ObsidianでProperties、Wikilink、backlink、見出し、表、コードブロックを確認し、Markdown互換性も確認する。
10. docsレビューでIssueとの整合性、影響範囲、実装可能性、リンク、セキュリティを確認する。
11. 対象範囲や依存関係が変わった場合は、影響範囲を再調査し、表とIssueを更新する。
12. `docs/changelog.md`へ日付、分類、概要、関連Issue/PRを追記する。

### 影響範囲表

| Task | 対象 | 影響内容 | 更新要否 | 関連テスト | 外部影響 | 依存・競合 | 担当・write scope | 調査状態 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | `docs/foo.md` | 参照元・関連コード・利用手順 | 必須／不要 | docs検証 | なし／内容 | なし／依存／競合 | Agent・scope | confirmed／未確認／対象外 |

## 完了条件

- docsの分類、読者、関連Issueが明確
- 入口から参照できる
- docsレビューで🔴がない
- 更新履歴が追加されている

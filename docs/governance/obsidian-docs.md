---
type: governance
status: active
tags:
  - docs/governance
  - obsidian-first
related:
  - "[[docs/index]]"
  - "[[docs/governance/docs-governance]]"
updated: 2026-09-13
---

# Obsidian-first docs運用

## 目的

このリポジトリのdocsは、プロジェクトルートをObsidian Vaultとして開き、Properties、内部リンク、backlink、graph、検索を使って作成・参照する。保存形式はMarkdownとし、GitHubや通常のエディタでも読める互換性を維持する。

## 作成規約

新規docsまたは大きく更新するdocsは、[`docs/templates/document-template.md`](../templates/document-template.md)から作成し、次のPropertiesを持つ。

| Property | 必須 | 内容 |
| --- | --- | --- |
| `type` | 必須 | `requirements`、`design`、`workflow`、`skill`、`agent`、`context`、`other`など |
| `status` | 必須 | `draft`、`active`、`deprecated`、`archived` |
| `tags` | 必須 | `docs/...`と用途タグ。階層タグを優先する |
| `related` | 必須 | 関連docs、Issue、SkillへのWikilinkまたはURL |
| `updated` | 必須 | 最終更新日 `YYYY-MM-DD` |

本文は「概要」「前提」「本文」「検証」「関連資料」の順を基本とする。正規仕様は本文に置き、contextやObsidianのWorkノートへ移さない。

## リンク規約

- 同一Vault内のdocsはObsidian Wikilink（`[[path/to/file|表示名]]`）を優先する。
- 外部URL、GitHub Issue/PR、コードファイル、他ツールでの直接参照は標準Markdownリンクを使う。
- 新しいdocsは少なくとも1つの入口またはMOCから辿れるようにし、関連docsからbacklinkを作る。
- 移動・改名時はWikilinkの未解決リンクと入口を確認する。

## 作成後の確認

1. ObsidianでVaultを開き、Propertiesが認識されることを確認する。
2. MOC/入口から対象docsを開き、内部リンク、backlink、見出し、表、コードブロックの表示を確認する。
3. GitHubまたは通常のMarkdown表示でも内容が読めることを確認する。
4. frontmatter、リンク、関連Issue/Skill、更新日をdocsレビューへ記録する。

## 境界

Obsidianはdocsの主たる作成・参照環境だが、Obsidian固有の表示機能を正規仕様にしない。Vault設定やWorkノートが失われても、docs本文とPropertiesだけで仕様を復元できる状態を保つ。

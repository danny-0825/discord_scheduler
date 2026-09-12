---
type: governance
status: active
tags:
  - docs/governance
related:
  - "[[docs/governance/obsidian-docs]]"
  - "[[docs/index]]"
updated: 2026-09-13
---

# docs運用ルール

## 目的

仕様・設計・運用手順をコードや設計書へ埋め込まず、目的別のdocsとして短く参照できる状態を保つ。実装時に必要な情報を素早く読めるよう、Obsidian Vaultの入口、Properties、Wikilink、分類、backlink、更新履歴を統一する。Obsidian固有規約は[Obsidian-first docs運用](obsidian-docs.md)に分離する。

## docsの分類

| 分類 | 配置 | 用途 |
| --- | --- | --- |
| ワークフロー | `docs/workflows/` | ユースケース別の作業手順、判断、完了条件 |
| 要件定義書 | `docs/requirements/` | 背景、目的、利用者、機能要件、非機能要件、制約、受入条件 |
| 詳細設計書 | `docs/design/` | 構成、責務、データ/API、状態遷移、エラー、テスト設計 |
| Skill docs | `docs/skills/` | Skillの目的、入力、出力、適用条件、制約、利用例 |
| Agent docs | `docs/agents/` | Agent/SubAgentの役割、権限、担当範囲、連携方法 |
| Context | `docs/context/` | 作業開始時の要約、参照registry、Issue単位の判断、外部情報の出典 |
| テンプレート | `docs/templates/` | Obsidianで新規docsを作成する雛形。正規docsではなく作成時に複製する |
| その他 | `docs/other/` | ADR、運用メモ、移行計画、FAQ、調査結果など上記に分類できないdocs |
| 更新履歴 | `docs/changelog.md` | docs、Skill、Agent、設定、コードの利用者向け変更履歴 |

分類に迷う場合は、読者と利用目的が最も近い分類を選び、複数分類へ同じ本文を複製しない。分類をまたぐ場合は主分類に本文を置き、他方からリンクする。

## 命名・構成

- ファイル名は小文字kebab-caseとし、内容が分かる名詞またはユースケース名を使う。
- 各ディレクトリに`README.md`または`index.md`を置き、配下のdocsへの入口にする。
- docsの冒頭に対象、目的、関連Issueまたは関連Skillを記載する。
- 新規docsまたは大きく更新するdocsは、frontmatter/Propertiesと関連Wikilinkを付け、[`docs/templates/document-template.md`](../templates/document-template.md)から作成する。
- 長いdocsは「概要」「前提」「本文」「検証」「関連資料」の順で構成する。
- コードや設定の完全な複製は避け、参照先へのリンクと判断理由を記載する。
- `docs/context/`は正規仕様の代替ではなく、要約・リンク・作業状態を置く。正規情報源と更新契機は[Context registry](../context/registry.md)へ記録する。

## 更新ルール

1. Issue作成前に、docs、Skill、Agent、コード、テスト、設定、生成物、CI/CD、DB、外部サービスの影響範囲と依存関係を調査する。
2. 影響範囲表へ更新要否、関連テスト、外部影響、依存・競合、担当・write scope、調査状態（`confirmed／未確認／対象外`）を記録する。
3. Issueの要求・完了条件を要件定義書へ反映する。
4. 要件が実装構造やデータに影響する場合、詳細設計書を更新する。
5. 実装・Skill・Agentの利用方法が変わる場合、対応するWorkflow docsを更新する。
6. 対象範囲や依存関係がIssue、docs、実装、レビューで変わった場合は、影響範囲を再調査する。確認できない対象は推測で確定せず、`未確認`としてリスクと停止条件へ記録する。
7. 変更の要約、日付、関連Issue/PR、影響範囲を`docs/changelog.md`へ追記する。
8. docsレビューで🔴がないことを確認してから実装へ進む。
9. contextを追加・更新した場合は、registry、正規情報源、取得日・確認日、active/archiveの状態を確認する。

### 影響範囲表

| Task | 対象 | 影響内容 | 更新要否 | 関連テスト | 外部影響 | 依存・競合 | 担当・write scope | 調査状態 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | `docs/**` | 参照元・後続成果物・関連コード | 必須／不要 | docs／コードテスト | なし／内容 | なし／依存／競合 | Agent・scope | confirmed／未確認／対象外 |

コードファイルや設計書本文に時系列の変更履歴を追記しない。現在の仕様は本文、過去の変更は`docs/changelog.md`に分離する。

## レビュー・参照

- Issueからdocsを作成し、Issueの完了条件と相互参照できるようにする。
- docsレビューは、正確性、要件との整合性、実装可能性、安全性、リンク切れを確認する。
- Workflow docsは、開始条件、入力、判断、手順、成果物、完了条件、失敗時の扱いを含める。
- docsの追加・更新時は[docs/index.md](../index.md)から辿れることを確認する。
- ObsidianでProperties、内部リンク、backlink、表、コードブロックの表示を確認し、Markdown互換性も確認する。
- context docsは正規docsとの重複・矛盾、外部情報の鮮度、Task contextのアーカイブ漏れをレビューする。

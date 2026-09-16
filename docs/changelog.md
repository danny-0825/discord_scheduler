---
type: other
status: active
tags:
  - docs/changelog
related:
  - "[[docs/index]]"
  - "[[docs/governance/obsidian-docs]]"
updated: 2026-09-14
---

# docs・開発資産の更新履歴

コードや設計書本文の参照コストを増やさないため、利用者向けの変更履歴をこのファイルへ集約する。各エントリは新しいものを上に追加する。

## 記録形式

| 日付 | 分類 | 概要 | 関連Issue/PR |
| --- | --- | --- | --- |
| 2026-09-14 | skill / docs / test | 21 Skillの主目的・I/O・副作用・近接境界をcatalog化し、42件のrouting fixtureとmanifest整合検証を追加。書込み・外部操作を伴う14 Skillを明示起動に統一 | #50 |
| 2026-09-13 | research / governance | Codex AI資産の公式・比較調査、キーワード台帳、再構成DAG、運用基準を追加 | #48 |
| 2026-09-13 | workflow / skill / agent / docs / config / test | Codex設定を現行CLIのAgent設定形式へ修正し、SubAgentの実行契約、親Agentによるworktree準備、7つの正規role、構造化計画fallback、静的契約テストを統一 | #46 |
| 2026-09-13 | workflow / skill / test | 外部`yaml`依存なしでSkill構造を検証する標準ライブラリ検証スクリプトを追加 | #44 / #45 |
| 2026-09-13 | workflow / skill / agent | Issue-to-PR WorkflowでPlanモードを必須化し、Taskごとのread/write/forbidden scope、フェーズゲート、再計画条件を追加 | #42 / #43 |
| 2026-09-13 | workflow / docs / skill / agent / other | docsをObsidian-firstで作成・参照する規約、Properties・Wikilink・backlink、docsテンプレート、表示検証を追加 | #40 / #41 |
| 2026-09-13 | workflow / skill / agent / other | pre-branch read-onlyゲート、branch gate、post-branch write権限をWorkflow・Review Skill・SubAgent・Agent docsへ反映 | #38 / #39 |
| 2026-09-13 | skill / workflow / other | BM25ベースの依存なしMarkdown検索Skill・CLI・検索設計とdocs探索ルールを追加 | #36 / #37 |
| YYYY-MM-DD | workflow / requirements / design / skill / agent / other | 変更内容 | #Issue / #PR |

## 履歴

| 日付 | 分類 | 概要 | 関連Issue/PR |
| --- | --- | --- | --- |
| 2026-09-13 | workflow / skill / other | `docs/context`の外部context構成、source-of-truth、Task lifecycle、外部リソース台帳と関連Skillレビュー観点を追加 | #34 / #35 |
| 2026-09-13 | workflow / other | 影響範囲・依存関係調査を既存Workflow、docs運用ルール、コードマップ、Issue／PRテンプレートへ反映 | #32 / #33 |
| 2026-09-13 | workflow / skill / other | Issue作成前の影響範囲・依存関係調査フェーズと、コード・テスト・外部依存を含む再調査ルールを追加 | #30 / #31 |
| 2026-09-13 | workflow / requirements / design / skill / agent / other | docs運用ルール、分類、ユースケース別Workflow、更新履歴の初期構成を追加 | #18 |

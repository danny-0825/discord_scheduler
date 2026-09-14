---
type: other
status: active
tags:
  - docs/research
  - codex
  - keyword-catalog
related:
  - "https://github.com/danny-0825/discord_scheduler/issues/48"
  - "[[docs/research/index]]"
  - "[[docs/research/codex-ai-rearchitecture]]"
updated: 2026-09-13
---

# AI資産キーワード台帳

## 概要

Issue #48の調査入力。対象は基点commit `0ac8aae` の追跡対象ファイル（`.agents/skills`、`.codex/agents`、`docs/`、`AGENTS.md`、`README.md`、`pubspec.yaml`、`routes/`、`test/`）と全Git履歴であり、build生成物、依存vendor、秘密情報を除外した。`rg --files`で候補を列挙し、基点commitに対する`git grep -i -o -E`で同義語を正規化して集計した。出現数は探索の優先順位であり、仕様の重要度そのものではない。

**作成来歴**: Issue #48 / T48。執筆は`docs_author`、レビューは`docs_reviewer`が担当する。

## 正規化・集計根拠

| 正規化語 | aliases | コマンド | 件数 | 代表出現 |
| --- | --- | --- | --- | --- |
| Skill | `Skill`、`SKILL.md` | `git grep -i -o -E 'skill|SKILL\.md' 0ac8aae \| wc -l` | 433 | `AGENTS.md`、`.agents/skills/**` |
| Agent | `Agent`、`Custom Agent`、`SubAgent` | `git grep -i -o -E 'agent|subagent' 0ac8aae \| wc -l` | 554 | `.codex/agents/**`、`docs/agents/**` |
| Workflow | `Workflow`、`Issue-to-PR`、`worktree` | `git grep -i -o -E 'workflow|worktree' 0ac8aae \| wc -l` | 584 | `issue-to-pr-workflow/**` |
| Context | `context`、`registry` | `git grep -i -o -E 'context|registry' 0ac8aae \| wc -l` | 231 | `docs/context/**` |
| Obsidian | `Obsidian` | `git grep -i -o -E 'obsidian' 0ac8aae \| wc -l` | 754 | governance / Obsidian Skills |

Git履歴の反復根拠は #24（SubAgent）、#26（Workflow review）、#28（配置）、#34（context）、#36（検索）、#38（read-only gate）、#42（Plan）、#44（validator）、#46（runtime contract）である。

## 台帳

| 分類 | キーワード | 根拠 | 関連資産 | 優先度 | 仮説 |
| --- | --- | --- | --- | --- | --- |
| プロダクト | `discord_scheduler`、Dart Frog、GET `/`、HTTP Response（Dart Frog 6、discord 4） | `README.md`、`routes/index.dart`、route test | アプリ雛形 | 中 | Discord連携・スケジューリングの要件は未定義。今回のAI資産再設計と混同しない。 |
| 技術 | Dart、dart_frog、test、Obsidian Vault、Markdown、Wikilink、Properties | `pubspec.yaml`、code map、governance docs | docs template/MOC | 高 | Obsidianは閲覧・作成環境であり、Markdown本文が正規仕様。 |
| AI資産 | AGENTS.md、SKILL.md、`agents/openai.yaml`、Custom Agent、SubAgent、role、sandbox、progressive disclosure（Skill 96、Agent 132、SubAgent 29） | `AGENTS.md`、21 Skills、7 Agent TOML | `.agents/skills`、`.codex/agents` | 最高 | Skill catalogは開発運用、Obsidian CLI、project-memoryに分けて再評価する。 |
| 運用・品質 | Issue、PR、Task、scope、branch、worktree、DAG、traceability、BM25、context registry | Workflow/Review Skill、docs/context | GitHub運用と契約テスト | 最高 | 同じ契約がAGENTS、Skill、refs、docs、Agentに重複している。 |
| 反復課題 | Plan fallback、read-only gate、runtime capability、config schema、legacy tool、scope drift | #24〜#46の履歴 | config、SubAgent refs、validator | 最高 | 規則を追加する前に実行可能性を検証する基盤が不足していた。 |

## 再現手順

1. `rg --files`で対象を列挙する。
2. 分類語を基点commitに対する`git grep -i -o -E '<aliases>' 0ac8aae | wc -l`で数え、上表の根拠ファイルと正規情報源を読む。
3. `git log --all`で、同一問題に対する増分変更を確認する。
4. 外部情報は[[docs/research/codex-ai-rearchitecture|調査報告]]のSourcesへ限定して照合する。

## 後続への対応

P0は実行基盤、P1はWorkflow、P2はSkill catalog、P3はContext/docsである。製品固有Skillは、Discord/スケジューリングの要件が確定するまで追加しない。

## 関連資料

- [[docs/research/index|調査入口]]
- [[docs/governance/ai-operating-standard|AI資産運用基準]]

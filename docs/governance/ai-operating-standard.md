---
type: governance
status: active
tags:
  - docs/governance
  - codex
  - ai-assets
related:
  - "https://github.com/danny-0825/discord_scheduler/issues/48"
  - "[[docs/research/codex-ai-rearchitecture]]"
  - "[[docs/workflows/issue-to-pr]]"
updated: 2026-09-13
---

# AI資産運用基準

## 概要

AI資産は役割を重複させない。

**作成来歴**: Issue #48 / T48。執筆は`docs_author`、レビューは`docs_reviewer`が担当する。

| 資産 | 正規情報・含める内容 | 含めない内容 | 変更所有者 | 必須検証 |
| --- | --- | --- |
| `AGENTS.md` | 恒久的な権限・Git・所有権の境界 | 手順詳細・host固有tool名 | T51 | 指示重複とscope逸脱。 |
| Skill | 再利用手順、発火条件、I/O、副作用 | 組織全体の恒久規則、role設定 | T49/T50 | frontmatter、routing、代表prompt。 |
| Custom Agent | role、入力、scope、返却、sandboxの意図 | Workflow全体、外部操作の暗黙権限 | T51 | filename/name/role、sandbox・親承認継承。 |
| Workflow docs | 人間向け開始条件・説明・成果物 | 実行状態機械の正規本文 | T50 | Skillとの重複がないこと。 |
| 契約テスト | 構文、対応、旧語、状態遷移 | 仕様判断や自動変更 | T52 | 決定的実行と失敗の可視化。 |

## Skillの追加・統合・廃止

- Skillは利用者意図、入出力、副作用、必要権限が既存Skillと異なる場合だけ追加する。
- `name`と`description`は短く、発火条件と近接Skillとの境界を示す。詳細は`references/`、再利用する決定的検証だけは`scripts/`へ置く。
- 変更・公開・同期など副作用を持つSkillは、承認直前までdry-run又はread-onlyにし、`agents/openai.yaml`の暗黙起動可否を明示的に判断する。
- 同じ入力・副作用・成果物を持つSkillは統合し、古い入口は移行案内後に廃止する。

## WorkflowとAgent

正規Workflowは、構造化計画、read-only調査、Issueレビュー、親Agentの環境準備、委譲/実装、検証/レビュー、PR、マージ後整理の順とする。Plan機能がない場合は、チャット又はIssueの構造化記録を同等の証跡とする。

親Agentは外部GitHub操作、branch/worktree準備、統合の単一所有者である。Custom Agentは`task_planner`、`impact_analyzer`、`issue_reviewer`、`docs_author`、`docs_reviewer`、`implementation_worker`、`workflow_reviewer`を正規roleとし、役割、必要入力、read/write/forbidden scope、返却形式、検証責務だけを持つ。

## 検証と変更ゲート

- 実行前に現行CLIの設定互換性と公開された能力を確認し、内部tool名を必須契約にしない。
- Skill構造、Agent filename/name/role、旧契約語、リンク、Workflow状態遷移は静的に検証する。
- 代表prompt、Plan有無、SubAgent有無、依存/独立Task、権限拒否、scope逸脱、worktree隔離をシナリオ検証する。
- AI資産の変更はIssueレビュー後、最新`origin/develop`から専用worktreeで行い、実装後にWorkflow/docsレビューを行う。

外部変更は親Agentが承認済みの対象だけを実行する。sandboxは到達可能範囲、approvalは実行時確認という別の制御であり、Agent roleの記述だけで権限を拡大しない。

## 関連資料

- [[docs/research/codex-ai-rearchitecture|調査と再構成設計]]
- [[docs/research/ai-keyword-catalog|キーワード台帳]]

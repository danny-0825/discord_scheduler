# Agent docs

Agent docsは、親AgentとSubAgentの責務を分離し、並列実行時の書き込み範囲と外部変更権限を明確にする。

## 必須項目

- Agentの役割
- 担当フェーズと入力・出力
- 読み取り範囲・書き込み範囲
- Issue、PR、commit、pushの権限
- 依存関係と並列実行ルール
- 失敗時の継続・停止条件
- 検証方法と親Agentへの報告形式

## Codex固有のSubAgent

実際の起動・状態管理・終了は[Codex SubAgent運用](codex-subagents.md)と`.codex/skills/issue-to-pr-workflow/references/subagents.md`に従う。役割名の記載だけではSubAgentを起動したことにならない。

# Project Instructions

## Codex公式構成

- リポジトリSkillは`.agents/skills/<skill-name>/SKILL.md`に配置する。
- プロジェクトCustom Agentは`.codex/agents/<agent-name>.toml`に配置する。
- プロジェクト設定は`.codex/config.toml`に配置する。
- リポジトリ全体の指示はこの`AGENTS.md`に記載する。
- Issue・PR・SubAgentの関係は、実行計画、Issue／PR本文、SubAgent threadの状態・結果で管理する。Codex公式ではないランタイム台帳形式を必須化しない。

## Issue-to-PR運用

- チャット要求をTaskへ分解し、Issue間の親子・依存・競合・関連を明示する。
- 独立Taskだけを並列化し、各Taskを1 Issue・1 branch・1 worktree・1 PRへ対応付ける。
- SubAgentはCodexのSubAgent機能で実際に起動し、Agent threadの状態・結果・終了を親Agentが管理する。
- Custom Agentの役割は`.codex/agents/`、詳細なWorkflowは`.agents/skills/`を参照する。
- Issue、docs、実装、PRのレビューでは、担当Task、SubAgent、read/write scope、依存成果物を確認する。
- 外部サービスの変更、commit、push、Issue／PR作成は、依頼範囲と権限を確認してから実行する。

## Git

- 通常の開発基点は最新の`origin/develop`とする。
- 並列Taskは専用worktreeとbranchを使用し、共通ファイル・共有資源の競合は直列化する。
- commitのprefixは英語、説明文は日本語とする。

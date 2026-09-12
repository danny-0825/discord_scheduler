---
type: agent
status: active
tags:
  - docs/agent
  - subagent
related:
  - "[[docs/agents/README]]"
  - "[[docs/governance/obsidian-docs]]"
updated: 2026-09-13
---

# Codex SubAgent運用

## 定義

SubAgentは、親Agentが独立したタスクを委譲するために、Codexのコラボレーション機能から起動する子Agentである。Skill内に`issue-reviewer`などの役割名を記載するだけではSubAgentは起動しない。

## 公式仕様に基づく運用

OpenAIの公式ドキュメントでは、SubAgentは親セッション内で作成され、独自のコンテキスト・状態を持ち、親Agentが結果を統合する単位として扱われる。複数の独立タスクは並列化できるが、依存関係のあるタスクは前提完了後に起動する。

- [Agents API: Create an agent](https://developers.openai.com/api/reference/typescript/resources/beta/subresources/agents/methods/create)
- [List session subagents](https://developers.openai.com/api/reference/typescript/resources/beta/subresources/agents/subresources/sessions/subresources/subagents/methods/list)
- [Retrieve a session subagent](https://developers.openai.com/api/reference/typescript/resources/beta/subresources/agents/subresources/sessions/subresources/subagents/methods/retrieve)
- [Agents APIのマルチエージェント説明](https://openai.com/index/introducing-the-agents-api/)

公式Agents APIの設定名やAPI endpointが、すべてのCodex製品・実行環境でそのまま呼び出せることを意味しない。実行前に現在のランタイムで利用可能なコラボレーションツールを確認し、利用できる実装へマッピングする。対応するツールが公開されていない場合は、起動済みと偽らず親Agentが直列実行する。

## プロジェクトでのライフサイクル

1. 親Agentがタスクの独立性、依存、読み取り範囲、書き込み範囲、外部変更権限を定義する。
2. `multi_agent_v1__spawn_agent`で具体的なTaskを起動する。
3. Agent ID、表示名、担当Issue、worktree、状態を記録する。
4. 必要に応じて`multi_agent_v1__send_input`で追加指示を送り、`multi_agent_v1__wait_agent`で結果を受け取る。
5. 親Agentが成果物とテストをレビューし、失敗時は依存タスクだけを停止する。
6. 不要になったAgentは`multi_agent_v1__close_agent`で終了する。

SubAgentへIssue・PR作成、コメント、commit、pushの権限を与える場合は、タスクごとに担当を1つだけ指定する。親AgentはSubAgentが実際に起動していることをAgent IDと状態で確認し、役割名だけでは代替しない。

## フェーズ別の変更権限

- pre-branch（タスク分解、影響調査、Issueレビュー）: read-only。リポジトリ、branch、worktree、commit、pushを変更しない。
- branch gate: 親Agentが最新`origin/develop`を確認し、Task専用branch/worktreeとwrite scopeを確定する。
- post-branch: docs-author、implementation-workerなどが割り当てられたworktree内だけを変更する。

pre-branchで修正候補が見つかった場合は、Issue・実行計画へ記録してpost-branchへ引き継ぐ。初期調査のために先にコードを直すことは禁止する。

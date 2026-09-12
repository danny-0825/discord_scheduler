# Workflowレビュー観点

## タスク分解

- 独立性を変更ファイル、責務、完了条件、依存関係で説明できる
- IssueごとにTask ID、目的、完了条件、親Issue・関連Issueが明示されている
- Issue間の`depends_on`、`blocks`、`related`、`conflicts_with`が実行計画へ記録されている
- 依存グラフに循環、未定義参照、依存先のない`blocks`がない
- 独立タスクの間に共通ファイル競合がない
- 共通設定、生成物、DB、API、外部サービスなどの共有資源を比較している
- 依存タスクだけを直列化している
- 失敗タスクとblockedタスクを区別している

## Issue・branch・worktree・PR

- 対応表に各タスクのIssue番号、branch、worktree、PR番号がある
- branch名とworktree pathがタスクごとに一意である
- branchは最新の`origin/develop`から作成される
- 1つのPRに独立した複数Issueを混在させていない
- PR本文に正しいIssueのclosing keywordがある

## SubAgent

- Agent IDと状態が記録されている
- IssueとSubAgentが`implements`で一意に対応している
- 作成担当Agentとレビュー担当Agentが`validates`として記録されている
- 各Agentに専用worktreeと書き込み範囲が渡されている
- Agent間のread/write scopeと競合資源を比較している
- Agentの成果物が担当Issueの完了条件へ追跡できる
- Issue／PR作成権限の担当が重複していない
- 親Agentが成果物、テスト、差分を確認している
- 完了Agentをcloseし、失敗時に独立タスクを継続している

## 後片付け

- PRマージ後に専用worktreeが削除されている
- 未マージcommitや未コミット変更を残していない
- 失敗・保留・未実行タスクを最終報告へ集約している

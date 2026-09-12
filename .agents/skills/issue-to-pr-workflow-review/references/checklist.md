# Workflowレビュー観点

## タスク分解

- 作業開始時にPlanモードが開始され、Task、依存、scope、担当、フェーズ完了条件が記録されている
- Plan未確定のままIssue作成、SubAgent起動、branch/worktree作成、実装へ進んでいない

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
- branch作成前のstatus/diffがcleanで、pre-branchにリポジトリ変更・commit・pushがない
- branch gateでIssueレビュー完了、最新`origin/develop`、専用branch/worktree、write scopeが確認されている

## 影響範囲・依存関係

- Issue作成前に影響範囲表が作成されている
- docs、Skill、Agent、コード、テスト、設定、生成物、CI/CD、DB、外部サービスが調査対象に含まれている
- コードの呼び出し元・呼び出し先、型・API、設定、関連テスト、Fixture、Mockが確認されている
- 更新要否、依存・競合、担当・write scope、調査状態がTaskごとに記録されている
- 調査できない対象が`未確認`としてリスク・停止条件へ記録され、推測で確定されていない
- Issue、docs、実装、レビューでスコープが変わった場合に再調査している
- `docs/context`を変更する場合、正規情報源、registry、外部情報の鮮度、Task contextのarchiveを確認している

## SubAgent

- Agent IDと状態が記録されている
- IssueとSubAgentが`implements`で一意に対応している
- 作成担当Agentとレビュー担当Agentが`validates`として記録されている
- 各Agentに専用worktreeと書き込み範囲が渡されている
- Agent間のread/write scopeと競合資源を比較している
- Planのwrite scopeとforbidden scopeがgit diffおよびSubAgent報告と一致している
- Agentの成果物が担当Issueの完了条件へ追跡できる
- Issue／PR作成権限の担当が重複していない
- 親Agentが成果物、テスト、差分を確認している
- 完了Agentをcloseし、失敗時に独立タスクを継続している

## 後片付け

- PRマージ後に専用worktreeが削除されている
- 未マージcommitや未コミット変更を残していない
- 失敗・保留・未実行タスクを最終報告へ集約している

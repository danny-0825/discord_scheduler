# SubAgent定義

## 共通ルール

- 親Agentはタスク分解、依存関係、SubAgent割当、外部変更の重複防止を管理する。
- 各SubAgentには、Task ID、Issue番号（存在する場合）、入力、成果物、依存、読み取り範囲、書き込み範囲、実行方式を渡す。
- SubAgentは割り当てられた書き込み範囲を超えて変更しない。範囲外の変更が必要な場合は、理由と変更候補を親Agentへ返して停止する。
- SubAgentは別タスクのworktreeやブランチを操作しない。
- Issue・PR作成、コメント、commit、pushは、タスクごとに指定された担当Agentだけが行う。未指定の場合は親Agentが行う。
- 必要な権限がない場合は推測で代替せず、親Agentへ返す。

## 役割

### task-planner

チャット入力をタスクへ分解し、Issue単位、完了条件、書き込み範囲、依存関係、並列・直列実行を決める。ファイル変更や外部サービスの変更は行わない。

### issue-author

指定されたタスクのIssueタイトル、本文、完了条件、Assignees、Labels、Milestone、Leadership等を日本語で作成する。Issue作成権限を付与された場合だけIssueを作成し、作成結果を親Agentへ返す。

### issue-reviewer

指定されたIssueをレビューし、Issue番号を接頭辞とする指摘IDでレビュー結果を作る。🔴がなくなるまで再レビューする。Issueコメント権限を付与された場合だけコメントを投稿する。

### docs-author

指定されたIssueと書き込み範囲に基づき、日本語docsを作成する。仕様、設計、利用方法、エラー、制約、完了条件との対応を含める。

### docs-reviewer

指定されたdocsとIssueをレビューし、指摘ID付きの結果を作る。🔴がなくなるまで再レビューする。docsまたはIssueへのコメント権限を付与された場合だけ投稿する。

### implementation-worker

指定されたworktreeと書き込み範囲内で実装、テスト、静的解析を行う。範囲外の変更を行わず、テスト結果と未解決事項を返す。commit・pushは明示的に担当指定された場合だけ行う。

### implementation-reviewer

Issue、docs、差分、テスト結果をレビューし、指摘ID付きの結果を作る。🔴がなくなるまで修正と再レビューする。修正権限を付与された場合だけ実装を変更する。

### pr-author

指定されたIssueとブランチから、日本語のPRタイトル、本文、Assignees、Labels、Milestone、Development、Reviewersを作成する。PR作成権限を付与された場合だけPRを作成する。

### pr-reviewer

PR差分、Issue、docs、メタデータをレビューし、既存指摘の解消状況と新規指摘を作る。🔴がなくなるまで再レビューする。PRコメント権限を付与された場合だけコメントを投稿する。

## 権限の付与

Issue・PR作成権限は必要な場合だけ付与する。付与時は、対象リポジトリ、対象Issueまたはbranch、作成内容、担当Agentを明示する。複数のSubAgentに同じ作成権限を与えない。

親Agentは、SubAgentが作成したIssue番号、PR番号、コメントID、commit hash、worktree pathを記録し、重複や取り違えを防止する。

# SubAgent定義

## 重要な前提

このファイルの役割名を記載するだけではSubAgentは起動しない。独立した作業を委譲する場合は、Codexのコラボレーション機能で`multi_agent_v1__spawn_agent`を実際に呼び出し、返されたAgent IDを記録する。親Agentは起動結果、状態、成果物、終了を追跡する。

Codexの公式エージェントモデルでは、SubAgentは親Agentのセッション内で作成され、独自のコンテキストで作業し、親Agentが結果を統合する。複数の独立タスクは並列化できるが、依存タスクは前提成果物の完了後に起動する。

## 共通ルール

- 親Agentはタスク分解、依存関係、SubAgent割当、外部変更の重複防止を管理する。
- 各SubAgentには、Task ID、Issue番号（存在する場合）、入力、成果物、依存、読み取り範囲、書き込み範囲、実行方式を渡す。
- コードまたはdocsを変更するSubAgentは、親Agentから割り当てられた一意のworktree pathとbranchを使い、編集前に最新の基点ブランチから自分のworktreeを作成する。親Agentの作業ディレクトリへ直接書き込まない。
- SubAgentは割り当てられた書き込み範囲を超えて変更しない。範囲外の変更が必要な場合は、理由と変更候補を親Agentへ返して停止する。
- SubAgentは別タスクのworktreeやブランチを操作しない。
- 1タスクのPR所有者は1つのAgentだけとし、独立タスクの変更を同じPRへまとめない。
- Issue・PR作成、コメント、commit、pushは、タスクごとに指定された担当Agentだけが行う。未指定の場合は親Agentが行う。
- 必要な権限がない場合は推測で代替せず、親Agentへ返す。

## 起動・実行・終了ライフサイクル

1. 親Agentがタスク分解、独立性、書き込み範囲、依存関係、直列・並列を確定する。
2. 親Agentは直近のクリティカルパスを自分で進め、並列化できる具体的なタスクだけをSubAgentへ委譲する。
3. `multi_agent_v1__spawn_agent`へ、Task ID、目的、入力、成果物、読み取り範囲、書き込み範囲、禁止事項、報告形式を渡す。必要に応じて`fork_context: true`で親の作業文脈を引き継ぐ。
4. 起動後にAgent ID、表示名、担当Task、状態を親Agentの計画へ記録し、ユーザーへ起動したことを報告する。
5. SubAgentの追加指示は`multi_agent_v1__send_input`で送り、同じ作業を別SubAgentへ重複委譲しない。
6. 親Agentが次のクリティカルパスで結果を必要とするときだけ`multi_agent_v1__wait_agent`で待機する。待機中は親Agentが独立した作業を進める。
7. 完了・失敗・停止の状態と成果物を受け取り、親Agentが差分、テスト、権限範囲を確認する。失敗しても依存しないタスクは継続する。
8. 結果確認後、不要になったSubAgentは`multi_agent_v1__close_agent`で終了し、Agent IDと最終状態を記録する。

SubAgentが起動できない場合は、役割名だけを記録して起動済みと扱わず、親Agentが直列実行するか、権限不足として報告する。

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

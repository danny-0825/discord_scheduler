# SubAgent定義

## 重要な前提

このファイルの役割名を記載するだけではSubAgentは起動しない。独立した作業を委譲する場合は、親Agentが実行環境で利用可能なCodexコラボレーション機能を使って実際に起動し、返された識別子、状態、成果物、最終結果を記録する。対応する機能が公開されていない場合は、起動済みと偽らず親Agentが直列実行する。

Codexの公式エージェントモデルでは、SubAgentは親Agentのセッション内で作成され、独自のコンテキストで作業し、親Agentが結果を統合する。複数の独立タスクは並列化できるが、依存タスクは前提成果物の完了後に起動する。

## 共通ルール

- 親Agentはタスク分解、依存関係、SubAgent割当、外部変更の重複防止を管理する。
- SubAgentを起動する前に、親AgentはPlan機能が利用できる場合はPlanへ、利用できない場合はチャットまたはIssueへ、Task、依存、read/write/forbidden scope、worktree、権限、完了条件、検証方法を構造化して確定する。計画未確定の役割名だけでは起動できない。
- pre-branch担当の`task_planner`、`impact_analyzer`、`issue_reviewer`、`docs_reviewer`、`workflow_reviewer`はread-onlyで、リポジトリ変更・branch/worktree作成・commitを行わない。Issueコメント権限がある場合も、計画とレビューの記録だけを行う。
- 親Agentは [relationship-and-independence.md](relationship-and-independence.md) の実行計画で、IssueとSubAgentの`implements`、レビューの`validates`、タスク間の依存・競合関係を管理する。
- 各SubAgentには、Task ID、Issue番号（存在する場合）、入力、成果物、依存、読み取り範囲、書き込み範囲、実行方式を渡す。
- 起動時の入力には、関連Issue、関係（`implements`または`validates`）、前提Task、後続Task、競合資源、Agentのread/write scopeを含める。
- branch gate後、親Agentが`git fetch origin`で基点を確認し、コードまたはdocsを変更するTaskごとに一意のworktree pathとbranchを作成・検証する。SubAgentは親Agentから割り当てられたpathとbranchだけを使い、worktreeを作成せず、親Agentの作業ディレクトリへ直接書き込まない。
- docsまたはコードを変更するSubAgentは、フェーズ6のbranch/worktree作成完了と、担当Issueの🔴0件を親Agentから受け取るまで起動しない。
- SubAgentは割り当てられた書き込み範囲を超えて変更しない。範囲外の変更が必要な場合は、理由と変更候補を親Agentへ返して停止する。
- forbidden scope、外部変更scope、検証方法は起動時入力に含め、作業中に変更しない。変更が必要な場合はSubAgentを停止し、親AgentがPlanと独立性を再判定する。
- SubAgentは別タスクのworktreeやブランチを操作しない。
- SubAgent同士が同じファイル・設定・外部資源を変更する場合は並列起動せず、所有Taskを決めて他を依存タスクにする。
- 1タスクのPR所有者は1つのAgentだけとし、独立タスクの変更を同じPRへまとめない。
- Issue・PR作成、コメント、commit、pushは、タスクごとに指定された担当Agentだけが行う。未指定の場合は親Agentが行う。
- 必要な権限がない場合は推測で代替せず、親Agentへ返す。
- 1Taskに複数Agentを割り当てる場合は、書き込みを行う`implements`担当を1名、検証を行う`validates`担当を別Agentとして実行計画へ登録する。複数の`implements`担当や作成担当自身だけの検証は認めない。

## 起動・実行・終了ライフサイクル

1. 親Agentがタスク分解、独立性、書き込み範囲、依存関係、直列・並列を確定する。
2. 親Agentは直近のクリティカルパスを自分で進め、並列化できる具体的なタスクだけをSubAgentへ委譲する。
3. 実行環境で利用可能なコラボレーション機能でSubAgentを起動し、Task ID、目的、入力、成果物、読み取り範囲、書き込み範囲、禁止事項、報告形式を渡す。
4. 起動後にAgent ID、表示名、担当Task、状態を親Agentの計画へ記録し、ユーザーへ起動したことを報告する。
5. SubAgentの追加指示は、実行環境で利用可能な機能で送り、同じ作業を別SubAgentへ重複委譲しない。
6. 親Agentは次のクリティカルパスで結果を必要とするときだけ、利用可能な状態確認または待機機能を使う。待機中は独立した作業を進める。
7. 完了・失敗・停止の状態と成果物を受け取り、親Agentが差分、テスト、権限範囲を確認する。成果物が担当Issueの完了条件を満たすこと、変更がwrite scope内であること、実行計画のstatusと一致することも照合する。失敗しても依存しないタスクは継続する。
8. 結果確認後、明示的な停止機能が利用できる場合だけ不要になったSubAgentを終了し、識別子と最終状態を記録する。停止機能がない環境では、完了通知または最終報告を終了の証跡とする。

SubAgentが起動できない場合は、役割名だけを記録して起動済みと扱わず、親Agentが直列実行するか、権限不足として報告する。

## 正規Custom Agent role

### task_planner

チャット入力をタスクへ分解し、Issue単位、完了条件、書き込み範囲、依存関係、並列・直列実行を決める。ファイル変更や外部サービスの変更は行わない。

### impact_analyzer

Issue作成前に、docs、context、Skill、Agent、コード、テスト、設定、生成物、CI/CD、外部サービスの影響と未確認事項を調査する。変更候補と検証方法を親Agentへ返し、ファイル・外部サービスを変更しない。

### issue_reviewer

指定されたIssueをレビューし、Issue番号を接頭辞とする指摘IDでレビュー結果を作る。🔴がなくなるまで再レビューする。Issueコメント権限を付与された場合だけコメントを投稿する。

### docs_author

指定されたIssueと書き込み範囲に基づき、日本語docsを作成する。仕様、設計、利用方法、エラー、制約、完了条件との対応を含める。

### docs_reviewer

指定されたdocsとIssueをレビューし、指摘ID付きの結果を作る。🔴がなくなるまで再レビューする。docsまたはIssueへのコメント権限を付与された場合だけ投稿する。

### implementation_worker

指定されたworktreeと書き込み範囲内で実装、テスト、静的解析を行う。範囲外の変更を行わず、テスト結果と未解決事項を返す。commit・pushは明示的に担当指定された場合だけ行う。

### workflow_reviewer

Task、Issue、Agent、branch、worktree、commit、PRの対応と、利用可能なコラボレーション機能で実行できるかをレビューする。ファイル・外部サービスを変更しない。

## 権限の付与

Issue・PR作成権限は必要な場合だけ付与する。付与時は、対象リポジトリ、対象Issueまたはbranch、作成内容、担当Agentを明示する。複数のSubAgentに同じ作成権限を与えない。

親Agentは、SubAgentが作成したIssue番号、PR番号、コメントID、commit hash、worktree pathを記録し、重複や取り違えを防止する。

Issue・PR作成、実装レビュー、PRレビューは、必要な場合に親AgentまたはTaskごとに指定した担当が実行する。未定義のCustom Agent roleを要求しない。

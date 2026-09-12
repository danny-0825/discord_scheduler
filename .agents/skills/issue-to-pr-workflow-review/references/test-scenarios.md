# Workflow検証シナリオ

## シナリオA: 独立タスク2件

### Plan未確定で開始しようとするケース

- PlanにTask、依存、read/write/forbidden scope、担当、完了条件がない状態でIssue作成・SubAgent起動・branch作成を試みる。
- 期待結果: Workflowは開始を停止し、Plan作成とscope確定を要求する。これは🔴として扱う。

### scope外変更のケース

- Planで`docs/workflows/**`だけをwrite scopeにしたTaskが、`src/**`または別Taskのdocsを変更する。
- 期待結果: 親AgentはSubAgentを停止し、差分を受け取らず、影響範囲・独立性・Planを再判定する。

T1とT2が異なるディレクトリを変更する場合、2つのSubAgentを並列起動する。各Agentが異なるworktreeとbranchを作成し、各自のcommitを作成できることを確認する。PRはT1用とT2用に分ける。

## シナリオB: 依存タスク

T3がT1のdocsを前提とする場合、T1のPRマージ前にT3を起動しない。T1のmerge commitを確認した後、T3のAgentが最新の`origin/develop`から新しいworktreeを作成する。

## シナリオC: 部分失敗

T1が失敗し、T2が独立している場合、T2は継続する。T3がT1に依存する場合、T3だけをblockedにする。最終報告には成功、失敗、blockedを分けて記録する。

## シナリオD: マージ後整理

T1用PRをマージした後、T1のworktreeとbranchを削除する。T2の作業環境には影響を与えない。

## シナリオE: 関係性と独立性の検証

T1とT2がそれぞれIssue、SubAgent、worktree、PRを持ち、`related`だけである場合は並列実行する。T3がT1の成果物を必要とする場合は`depends_on`として直列化する。T4とT5が同じ設定ファイルを変更する場合は`conflicts_with`として同時起動せず、所有Taskを決める。各Taskの成果物、commit、PRが担当Issueの完了条件へ追跡できることを確認する。

## シナリオF: 影響範囲・依存関係調査

Issue作成前に、Taskごとにdocs、Skill、Agent、コード、テスト、設定、生成物、CI/CD、DB、外部サービスの影響範囲表を作成する。コードの呼び出し元・呼び出し先、型・API、関連テスト、Fixture、Mockを確認し、更新要否、依存・競合、write scope、調査状態を記録する。実行時依存や外部サービスを確認できない場合は`未確認`としてリスクと停止条件へ記録し、`confirmed`扱いにしない。後続フェーズで対象範囲が変わった場合は、影響範囲調査へ戻って表と実行計画を更新する。

## 実行範囲

## シナリオG: Context外部化

`docs/context`の入口からregistry、core、task、external、generatedへ辿れることを確認する。正規docsの重複コピーがなく、外部情報に出典・取得日・確認日があり、Issue close後のTask contextがarchiveへ移る運用を確認する。

## シナリオH: Pre-branch read-onlyゲート

タスク分解・影響調査・Issueレビュー中に、リポジトリのstatus/diffが開始時から変わらないことを確認する。コード修正候補はIssueまたは実行計画へ記録し、Issueレビューで🔴がなくなった後にだけ最新基点からbranch/worktreeを作成する。branch gate後の専用worktreeで初めてdocs・コードの変更を許可する。

このシナリオは、外部GitHubを変更しないdry-runとローカルGitスモークテストで検証する。Issue作成、push、PR、mergeを実環境で検証する場合は、ユーザーの明示的な許可と対象リポジトリを確認する。

ローカル検証では`references/../scripts/pre_branch_gate_test.sh`も実行し、branch gate前のread-onlyとgate後のwriteを確認する。

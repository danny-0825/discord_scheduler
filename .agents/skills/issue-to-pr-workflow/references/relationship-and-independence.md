# Issue・SubAgent関係性と独立性の契約

## 目的

Issue、SubAgent、branch、worktree、commit、PRの対応と関係を親Agentの実行計画で追跡し、並列化できるタスクだけを並列実行する。役割名やIssue番号の記載だけでは関係性が担保されたとは扱わない。

## 関係の種類

| 関係 | 意味 | 実行ルール |
| --- | --- | --- |
| `depends_on` | 前提成果物が必要 | 前提PRのマージと最新基点への反映後に開始する |
| `blocks` | 未完了だと後続を開始できない | 後続を`blocked`として停止する |
| `related` | 参照・協調するが前提ではない | 独立性を保てるか競合資源を確認する |
| `conflicts_with` | 同じ資源を変更し同時実行できない | 直列化または書き込み範囲を再分割する |
| `parent_of` / `child_of` | 大きな要求と分割Issueの関係 | 子Issueは親のスコープ・完了条件を継承し、独立性を再判定する |
| `implements` | SubAgentがIssueを担当する | 1タスクにつき担当Agentを明示する |
| `validates` | Agentまたはレビューが成果物を検証する | 作成担当と検証担当を分け、結果を記録する |

`depends_on`と`blocks`は有向非巡回グラフ（DAG）で管理する。循環、未定義ID、存在しないIssue・Agentへの参照は🔴とする。

## 実行計画

CodexにはIssue・PR・SubAgentを横断する公式JSON台帳形式はない。親Agentは、チャットの計画、Issue／PR本文、SubAgent threadのAgent ID・状態・結果を使って関係を追跡する。必要な対応表はMarkdownのタスク計画またはIssue／PRコメントに記録し、独自ファイルをCodexの必須設定として扱わない。

実行開始時はCodexのPlanモードでこの対応表を作成・更新する。Planモードが使えない場合は、同じ内容をチャットまたはIssueへ記録してから進める。Plan未確定の状態ではIssue作成、SubAgent起動、branch/worktree作成、実装を完了扱いにしない。

Issue作成前は仮Task ID、SubAgent起動前は仮Agent IDを使い、実体が作成された時点で置き換える。

| Task | Issue | Agent(s) | 関係 | Depends on / Blocks | Read scope | Write scope | Forbidden scope | Impact scope | Impact status | Branch | Worktree | PR | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | #101 | A1 | implements | なし | `docs/**` | `docs/foo/**` | `src/**`, 外部Project | code / tests / docs / external | confirmed / 未確認 / 対象外 | `feature/101-foo` | `../repo-worktrees/101-foo` | #201 | planned |

最低限、次のIDを実行計画で対応付ける。影響範囲表の`Impact scope`と`Impact status`、read/write/forbidden scopeも、Issue作成前にTaskごとに埋める。

`Task ID → Issue → SubAgent → branch → worktree → commit → PR`

Issue、Agent、PRの作成担当・レビュー担当・外部変更権限も記録する。担当が空欄、複数担当、または同じAgentが無関係な複数タスクの書き込みを担当する場合は独立性を再判定する。

1Taskに複数Agentが関わる場合、書き込みを行う`implements`担当は1名、レビュー・検証を行う`validates`担当は別Agentとして明示する。複数の`implements`担当や、作成担当自身だけの検証は🔴とする。

## 独立性の判定

次の全条件を満たす場合だけ並列実行する。

- 完了条件をそれぞれ単独で検証できる
- 書き込みファイル・ディレクトリが重複しない
- 共通設定、生成物、DB、API、外部リソースを同時に変更しない
- 一方の成果物を読まなくても他方の成果物を完成できる
- Issue、Agent、branch、worktree、PRの担当が重複しない
- 失敗しても他タスクの正しさ、テスト、ロールバックに影響しない

共通ファイル、DB、API、Project、外部サービスなどを変更する場合は、所有Taskを1つに決めて他Taskを`depends_on`にする。読み取りだけの共有は許可するが、所有Task、ロックまたは直列化方法、基点SHA・参照バージョンを実行計画に記録する。

## 検証タイミング

1. Issue作成前: タスク分解、DAG、影響範囲表、競合資源、Issue分割理由を確定する。
2. SubAgent起動前: AgentごとのIssue、write scope、worktree、権限、依存を確定する。
3. SubAgent完了時: write scope、commit、テスト、成果物、未解決依存を親Agentが照合する。
4. PR作成前: 1 Issue・1 Task・1 PRの対応、closing keyword、変更範囲を確認する。
5. マージ後: status、依存タスクの解除、worktree・branch削除を実行計画へ反映する。

Planのscope、依存、完了条件が後続フェーズで変わった場合は、現在のTaskを保留し、影響調査・独立性判定・Issueレビューを再実行してから再開する。未更新の対応表と実際の差分が一致しない場合は`needs-review`とする。

関係性が確認できない成果物は、完了扱いにせず`needs-review`または`blocked`として報告する。

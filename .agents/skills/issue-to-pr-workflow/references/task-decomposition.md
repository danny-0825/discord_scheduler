# タスク分解・独立性・並列実行

## 目的

チャットで入力された作業要望を、実行可能なIssue単位へ分解し、独立タスクは並列、依存タスクは必要な部分だけ直列で処理する。

## Pre-branchの変更禁止

タスク分解、実行計画、影響調査、Issue作成、Issueレビューはread-onlyフェーズである。リポジトリのコード、docs、Skill、Agent、設定、テストを変更せず、変更候補はTaskのwrite scope・完了条件・Issueへ記録する。最初のリポジトリ変更は、Issueレビュー完了後に最新`origin/develop`から作成した専用branch/worktreeで行う。

## Planモードを使う実行契約

作業開始時はPlan機能が利用できる場合にフェーズ1〜15の実行計画を作成する。Plan機能が使えない場合は、同じ計画をチャットまたはIssueへ構造化して記録するまで作業を開始しない。

Planには次の情報をTaskごとに含める。

- 目的、単独で検証可能な完了条件、Issue分割の理由
- `depends_on`、`blocks`、`related`、`conflicts_with`とDAGの確認結果
- read scope、write scope、forbidden scope、外部変更scope、関連テスト
- 担当Agent、レビューAgent、権限、SubAgentの起動条件と状態
- 基点SHA、branch、worktree、commit、PR
- 各フェーズの入力、成果物、完了条件、検証方法、停止条件、次フェーズ

Planはフェーズ開始時・終了時に更新し、`in_progress`は1フェーズだけにする。Task、scope、担当、依存、完了条件のいずれかが未確定なら、Issue作成、SubAgent起動、branch/worktree作成、実装を禁止する。

write scopeは許可する最小範囲、forbidden scopeは変更禁止範囲として具体的なパスまたはパターンで定義する。scope外の変更が必要になった場合は停止し、影響調査と独立性判定へ戻ってPlan・Issue・関係表を更新し、レビュー後に再開する。

## 分解判断

AIが最終判断する。ユーザーに分割判断だけを再確認せず、曖昧さやリスクが作業結果を変える場合だけ確認する。

1つのIssueにまとめる条件:

- 完了条件を分離できない
- 同じ変更を同じトランザクションまたは同じ設計判断で扱う必要がある
- 分割すると、どちらかを単独で検証・レビューできない
- 分割によって不要な中間状態や互換性問題が発生する

複数Issueへ分割する条件:

- 完了条件、レビュー、リリースを独立して扱える
- 変更対象のファイルや責務が分離できる
- 担当者やSubAgentを分けられる
- 一方が失敗しても他方の成果物を継続できる

## 独立性判定

各タスクについて、次の範囲を必ず定義する。関係の種類と対応表の詳細は [relationship-and-independence.md](relationship-and-independence.md) に従う。

| 項目 | 内容 |
| --- | --- |
| タスクID | Issue作成前は`T1`、`T2`の仮ID。Issue作成後はIssue番号を併記 |
| 目的 | タスク単独の目的 |
| 完了条件 | 単独で検証できる条件 |
| 書き込み範囲 | SubAgentが変更してよいファイル・ディレクトリ |
| 禁止範囲 | SubAgentが変更してはいけないファイル・ディレクトリ、外部資源 |
| 読み取り範囲 | 参照してよい関連コード・docs |
| 依存タスク | 前提となるタスクIDと依存理由 |
| 競合資源 | 共通ファイル、API、DB、設定、環境 |
| 関係 | `depends_on`、`blocks`、`related`、`conflicts_with`の対象 |
| 実行方式 | 並列または直列 |
| 検証方法 | 完了条件とscopeを確認する具体的なテスト・レビュー |

書き込み範囲は、この判定で決めたタスク固有の契約である。実装SubAgentが範囲外を変更する必要が生じた場合は、独立性判定をやり直してから進める。Issue、SubAgent、branch、worktree、PRを一意に対応付けられない場合も、起動前に判定をやり直す。

## 依存関係と並列化

タスクをDAGとして扱う。

```text
T1 ──┐
     ├── T3
T2 ──┘
```

- T1とT2は独立しているため並列実行する。
- T3はT1とT2の完了後に実行する。
- 前提タスクがある場合、その依存部分だけを直列化する。
- 依存タスクを開始する前に、前提PRがマージされ、最新の基点ブランチへ反映されていることを確認する。
- 1つのタスクが失敗しても、依存していないタスクは継続する。
- 失敗タスクに依存するタスクはblockedとして保留し、最終報告に含める。
- 関係グラフに循環、未定義のTask/Issue/Agent、依存先のない`blocks`がないことを確認する。

## 影響範囲・依存関係調査

Issue作成前に、タスク分解で定義したread/write scopeを起点として、既存資産と外部依存を調査する。コードは変更対象だけでなく、呼び出し元・呼び出し先、型・API、設定、関連テスト、Fixture、Mock、生成コードを確認する。

調査対象にはdocs、`docs/context`、Skill、Agent、コード、テスト、設定、生成物、CI/CD、DB、外部サービスを含める。contextを扱う場合は正規情報源、registry、鮮度、Task contextのarchive状態も比較する。静的検索で十分でない実行時依存や外部サービスは、テスト・ビルド・実行時確認で補完する。確認できない場合は推測で確定せず、`未確認`としてリスクと停止条件へ記録する。

最低限、次の表をTaskごとに作成する。

| Task | 対象 | 影響内容 | 更新要否 | 関連テスト | 外部影響 | 依存・競合 | 担当・write scope | 調査状態 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | `lib/foo.dart` | 呼び出し元・呼び出し先、型、設定 | 必須／不要 | `test/foo_test.dart` | なし／内容 | T2に依存／競合なし | Agent・scope | confirmed／未確認／対象外 |

Issue、docs、実装、レビューで対象ファイル、依存、競合、外部影響が変わった場合は、影響範囲調査へ戻り、実行計画・Issue・完了条件を更新してから次フェーズへ進む。

## Issue・branch・worktree・PR対応

通常は次の対応にする。

```text
T1 → Issue #101 → feature/101-example → worktree-101 → PR #201
```

- Issue作成前は仮IDを使い、Issue作成後に実際のIssue番号へ置き換える。
- 各タスクに専用worktreeを1つ割り当てる。
- branch gate後、親AgentがTaskごとに一意のbranchとworktreeを最新の基点から作成・検証し、担当SubAgentへ割り当てる。
- worktree間で同じ作業ディレクトリを共有しない。
- 依存タスクは、前提PRのマージ後に最新の`origin/develop`から新しいworktreeを作る。
- PRがマージされたら、未コミット変更がないことを確認して専用worktreeを削除する。
- worktreeの削除に失敗した場合は、状態を報告して他タスクの処理は継続する。

## 実行計画の成果物

Issue作成前に、最低限次の表を内部計画として作成する。

| Task | Issue | 依存 | 実行 | 書き込み範囲 | Branch | Worktree | PR | SubAgent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | 未作成 | なし | 並列 | `lib/foo/**` | `feature/{IssueNo}-foo` | 親Agentが準備する`../{repo}-worktrees/{IssueNo}-foo` | 1タスク1PR | implementation_worker |
| T2 | 未作成 | T1 | 直列 | `lib/bar/**` | `feature/{IssueNo}-bar` | 親Agentが準備する`../{repo}-worktrees/{IssueNo}-bar` | 1タスク1PR | implementation_worker |

Issue作成、コメント、commit、push、PR作成の担当Agentは各タスクで1つだけにする。

実行計画には、Task ID、Issue番号、Agent ID、関係、依存・競合、write scope、branch、worktree、commit、PR、statusを記録する。親AgentはSubAgent起動前と完了時に計画を照合する。

Planの実行中に対象、scope、依存、競合、完了条件が変わった場合は、そのフェーズを保留して影響範囲調査、Plan、Issue、関係表を更新する。更新前の計画に基づく変更やcommitは行わない。

## SubAgent実行計画

独立性判定の後、並列化できるタスクには実際のSubAgentを割り当てる。役割名を計画表へ書くだけでは起動扱いにしない。

| 項目 | 必須内容 |
| --- | --- |
| 起動方法 | 利用可能なCodexコラボレーション機能で実際に起動する |
| 入力 | Task ID、目的、依存、読み取り範囲、書き込み範囲、禁止事項 |
| 状態管理 | Agent ID、表示名、pending/running/completed/errored等の状態 |
| 結果取得 | 利用可能な状態確認・待機・追加指示機能で結果を取得する |
| 終了 | 明示的な終了機能が利用できる場合に終了し、なければ最終報告を終了証跡とする |
| 失敗時 | 依存しないタスクは継続し、依存タスクだけblockedとして記録する |

SubAgentの成果物は親Agentがレビューし、変更範囲、テスト、外部変更、未解決事項を確認してから次フェーズへ渡す。

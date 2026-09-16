# Issue-to-PR状態契約

## 状態と証跡

`planned -> investigated -> issue_ready -> issue_reviewed -> environment_provisioned -> (docs_ready | docs_waived) -> implemented -> verified -> committed -> pushed -> pr_open -> pr_reviewed -> merged -> cleaned`

`cleaned`だけが通常の終端状態である。`blocked`と`failed`は任意遷移ではない。失敗・保留の原因と再開先を証跡へ記録し、下表の復帰edgeだけを使う。親Agentは既存のPlan、Issue、PR、SubAgent threadへ次の証跡を記録する。Codex公式ではない実行時台帳ファイルを新設しない。

| 遷移 | 実行者 | 必須証跡 | blocked / failed と再開 |
| --- | --- | --- | --- |
| `planned -> investigated` | 親Agentまたはread-only reviewer | Task、DAG、read/write/forbidden scope、担当、完了条件 | Planまたは同等の構造化記録がない場合は`planned -> blocked -> planned`。記録後に再開 |
| `investigated -> issue_ready -> issue_reviewed` | 親Agentまたはread-only reviewer | 影響範囲、未確認リスク、Issue、Issue review 🔴0件 | Issue review失敗は`issue_ready -> failed -> issue_ready`で修正・再レビュー |
| `issue_reviewed -> environment_provisioned` | 親Agentのみ | 更新済み基点SHA、Task固有branch/worktree、write scope、割当 | 環境作成・検証失敗は`issue_reviewed -> failed -> issue_reviewed`で再試行。依存待ちは`issue_reviewed -> blocked -> issue_reviewed` |
| `environment_provisioned -> docs_ready` | 割当済み実装担当、またはfallback時の親 | docs成果物、docs review 🔴0件 | docs要件やscopeの変更は`docs_ready -> investigated`へ戻る |
| `environment_provisioned -> docs_waived` | 親Agentのみ | docs非変更のreason、owner、rationaleをPlanまたはIssueへ記録 | 記録不足は`environment_provisioned -> blocked -> environment_provisioned`。docs要件やscopeの変更は`docs_waived -> investigated` |
| `docs_ready`または`docs_waived` -> `implemented` -> `verified` | 割当済み実装担当、またはfallback時の親 | scope内diff、テスト・レビュー結果 | 検証失敗は`implemented -> failed -> implemented`。scope逸脱は`implemented -> investigated` |
| `verified -> committed -> pushed -> pr_open -> pr_reviewed -> merged -> cleaned` | 親Agent（effect）、read-only reviewer（review） | effect gate、commit、PR、review、merge、cleanup | effect拒否・権限不足は、例えば`verified -> blocked -> verified`のように拒否されたeffect直前状態へ戻る |

依存Taskは前提PRが`merged`で、最新基点から専用環境を再準備してから開始する。独立Taskが`failed`でも、依存しないTaskは継続する。依存Taskだけを`blocked`にする。

`failed`は原因に対応した復帰先を証跡へ持つ。Issue review失敗は`issue_ready`、環境準備失敗は`issue_reviewed`、実装・検証失敗は`implemented`へだけ戻る。`blocked`は記録先不足、docs免除記録不足、依存待ち、またはeffect拒否・能力不足のいずれかでのみ使い、それぞれ表にある復帰edgeへ戻る。

## PlanとSubAgentのfallback

Plan機能がないときは、チャットまたはIssueにTask、関係DAG、scope、担当、基点、phase、完了条件、停止条件を構造化して残す。SubAgentの起動・状態確認・結果取得の能力がないときは、role名だけを記録して起動済みとせず、親Agentが直列で実装・検証する。

書込みを委譲するときは、親Agentがbranch gate後にTask専用環境を作成・検証し、path、branch、read/write/forbidden scope、入力、検証、PR ownerを渡す。SubAgentは受け取ったworktree以外を変更せず、scope外の必要が判明したら停止して親へ返す。

## External effect gate

Issue/PR作成、GitHubコメント、commit、push、merge、branch/worktree作成・削除はeffectである。実行前に親Agentが既存のPlanまたはIssue/PR記録へ以下を残す。

| 項目 | 内容 |
| --- | --- |
| action | 実行する操作 |
| target | 対象repository、Issue/PR、branch、worktree等 |
| owner | 親Agentであること |
| authorization | 依頼範囲・権限・承認の根拠 |
| outcome | 実行済み、拒否、能力不足、失敗 |

能力、対象、内容、authorizationが一つでも不足または拒否なら、外部Git/GitHub runnerを実行せず`blocked`に遷移する。特定CLI、シェル、認証保管方式、内部tool名は前提にしない。能力が利用可能なときだけ、その環境で安全な手順を選ぶ。

# Issue to PR Workflow フェーズ一覧

状態の正規名、遷移、effect gate、再開条件は[状態契約](state-contract.md)に置く。この表は状態を詳細手順へ展開する補助資料であり、同じ契約を再定義しない。

## レビュー重大度

- 🔴 必須修正: 要件、完了条件、正確性、安全性、互換性などに関わる問題。解消するまで次フェーズへ進まない。
- 🟡 推奨修正: 品質、保守性、明確性を改善する問題。🔴がある場合は同じサイクルで修正する。
- 🟢 軽微・参考: 表記、好み、将来改善など。🔴がある場合は可能な限り同じサイクルで修正する。

レビューコメントは、重大度、対象、問題、理由、修正案、確認方法を含める。🔴がなくなったことをレビュー完了の最低条件とする。

## フェーズ

| # | フェーズ | 入力 | 主な成果物 | 変更権限 | 完了条件 | Planチェックポイント |
|---|---|---|---|---|---|---|
| 1 | タスク分解・独立性判定 | チャット入力 | Task、変更範囲、依存関係、競合資源、分割判断 | read-only | `planned -> investigated`に必要なTask、DAG、scope、担当、完了条件がある | Task目的、単独完了条件、read/write/forbidden scopeを記録 |
| 2 | 実行計画 | タスク一覧、関係表 | タスクグラフ、SubAgent割当、Issue/Agent/branch/worktree/PR対応表 | read-only | 独立タスクと依存タスクの実行順、scope、担当、検証担当が確定している | Plan機能またはチャット・Issueの構造化記録を確定し、未定義のTask・担当・scopeを0件にする |
| 3 | 影響範囲・依存関係調査 | タスク一覧、実行計画、既存資産、`docs/context` | BM25候補、影響範囲表、更新要否、依存・競合、リスク、調査状態 | read-only | 広範なdocs・context・Skill探索で`document-search`を使い、候補本文と正規情報源を確認したうえで、docs、context、Skill、Agent、コード、テスト、設定、生成物、CI/CD、外部サービスを調査し、`confirmed／未確認／対象外`を記録している | 調査結果をTaskのImpact scope/status、write scope、検証へ反映 |
| 4 | Issue作成 | タスク計画、影響範囲表 | Issue本文、Assignees、Labels、Milestone、Leadership等 | GitHubのみ | 必要なメタデータ、影響範囲、リスク、完了条件が日本語で定義され、Issueが作成されている | Issue番号をPlanへ反映し、IssueとTaskの1対1を確認 |
| 5 | Issueレビュー | Issue、関係表、影響範囲表 | Issueレビューコメント、修正版Issue、関係性レビュー結果 | read-only | 🔴がなく`issue_reviewed`へ遷移できる | 🔴0件、実行計画のpre-branch項目完了 |
| 6 | 基点更新・worktree/branch作成 | 確定Issue、Git状態 | 親Agentが基点を確認して作成した専用worktreeとbranch | 親Agentのみのwrite開始ゲート | `environment_provisioned`の証跡（基点SHA、branch、worktree、write scope、割当）がある | 基点SHA、branch、worktree、write scopeを実行計画へ記録 |
| 7 | docs作成または免除 | 確定Issue、影響範囲表、専用worktree | docs、または免除理由・判断者・根拠 | 専用worktreeまたは親の計画記録 | `docs_ready`または`docs_waived`のいずれかが証跡付きで成立する | docs Taskのscope内だけを変更し、差分または免除根拠をPlanへ記録 |
| 8 | docsレビュー | docs、Issue、影響範囲表、context registry | docsレビューコメント、修正版docs | 専用worktree/Issue | 🔴がない。Issueとの矛盾、contextの重複・リンク切れ・鮮度漏れがない | scope・完了条件・影響範囲が変わればPlanへ戻る |
| 9 | 実装 | Issue、docs、影響範囲表、専用worktree | コード、テスト、設定、必要なドキュメント | 専用worktreeのみ | 完了条件を満たし、影響範囲に記載した検証が成功している | forbidden scope変更なし、検証結果と未解決事項を更新 |
| 10 | 実装レビュー | 実装、Issue、docs、影響範囲表、関係表 | 実装レビューコメント、修正commit、追跡結果 | 専用worktree/Issue | 🔴がない。write scope、担当Issue、依存成果物、影響範囲との整合が確認済み | 差分とPlanのwrite scopeを照合 |
| 11 | commit | 検証済み差分 | 日本語説明のIssue番号付きcommit | 親Agentのeffect gate後 | 意図しない変更がなく、effect証跡とcommitがある | Planの検証・レビュー完了を確認してからcommit |
| 12 | push | commit | リモートブランチ | 親Agentのeffect gate後 | push先とcommitが確認できる | branch、commit、Issueの対応を確認 |
| 13 | PR作成 | Issue、リモートブランチ | 日本語PR、Assignees、Labels、Milestone、Development等 | 親Agentのeffect gate後 | IssueとPRが関連し、必要なメタデータが設定されている | 1 Task・1 Issue・1 PR、closing keyword、scope差分を確認 |
| 14 | PRレビュー | PR差分、Issue、docs、影響範囲表 | PRレビューコメント、修正commit | 専用branch/PR | 🔴がない。必要な修正と検証が完了している | PR差分がPlanのwrite scope内であることを確認 |
| 15 | マージ後整理 | マージ済みPR、worktree | worktree削除、タスク結果、全体結果 | 親Agentのeffect gate後 | `cleaned`へ遷移し、失敗・保留タスクが集約されている | Issue/PR/status/cleanupを記録 |

## 反復ルール

1. Issue、docs、実装の各レビューでは、指摘を🔴・🟡・🟢に分類する。
2. 🔴が1件でもあれば、🔴を解消するまでレビューを終了しない。
3. 🔴があるサイクルでは、🟡と🟢も修正対象に含める。ただし、対応しない場合は理由をコメントする。
4. 修正後は、修正箇所だけでなく、影響を受ける完了条件と関連成果物を再確認する。
5. レビュー完了時は、各重大度の残件数と未対応理由を記録する。

Issueタイトル、本文、コメント、docs、PRタイトル、PR本文、PRコメント、commitの説明文は日本語で作成する。commitのprefixだけは英語のConventional Commits形式を使う（例: `feat: スケジュール登録を追加 (#123)`）。

## 指摘IDとコメント形式

IssueとPRの指摘は、対象Issue番号を共通の接頭辞にして採番する。`{IssueNo}-{指摘No}` は一度発行したら変更せず、新規指摘だけ次の番号を使う。

コメントの先頭には、前回指摘の解消状況を置く。

```markdown
| ID | レベル | チェック |
| --- | --- | --- |
| {IssueNo}-{指摘No} | 🔴 | ✅ / ⛔️ |
```

同じコメントで新たな指摘が出た場合は、その後に新規指摘一覧を置く。

```markdown
| ID | レベル | 概要 |
| --- | --- | --- |
| {IssueNo}-{指摘No} | 🔴 / 🟡 / 🟢 | xxxxxx |
```

表の後ろに、各IDの詳細、理由、修正案、確認方法を記載する。

初回レビューで前回指摘がない場合は、解消状況表に「なし」と記載する。新規指摘がない場合は、新規指摘一覧にも「なし」と記載する。

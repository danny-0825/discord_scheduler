# Context registry

| Context | パス | 主な用途 | 正規情報源 | 更新契機 | 鮮度・アーカイブ |
| --- | --- | --- | --- | --- | --- |
| 入口 | `docs/context/index.md` | context探索 | docs governance | context領域の追加・変更 | 常に現行 |
| Core | `docs/context/core/` | 作業開始時のプロジェクト・構成・規約確認 | README、code-map、governance、Workflow | 構成・規約変更時 | 現行要約のみ |
| Task | `docs/context/task/active/<IssueNo>/` | Issueの影響範囲、判断、引き継ぎ | Issue、実行結果、レビュー | Issue開始・レビュー・完了時 | Issue close後にarchive |
| External | `docs/context/external/` | 外部情報の再利用と出典確認 | 参照元URL・公式文書 | 外部仕様参照時、版変更時 | 取得日・確認日を必須化 |
| Generated | `docs/context/generated/` | 再生成可能な一覧・スナップショット | 生成コマンドと入力 | 入力変更時 | 手編集しない |

## 記録項目

外部情報には、少なくとも出典、取得日、版または更新日、確認日、正規性、利用目的を記録する。秘密情報、認証トークン、個人パスは記録しない。

## ライフサイクル

1. 作業開始時に入口とregistryを読み、必要なcore/external/task contextだけを読む。
2. Issue単位の判断は`task/active/<IssueNo>/`へ記録し、正規仕様はIssueまたは既存docsへ置く。
3. Issue close・PR merge後に未完了事項と引き継ぎを確認し、task contextを`task/archive/<IssueNo>/`へ移す。
4. 古いcore要約や外部情報は削除せず、正規情報源・確認日を更新する。不要な生成物は再生成または除外する。

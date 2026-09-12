# Task context

Issue単位の作業判断を、正規仕様やコードから分離して保持する。

## 配置

- 作業中: `active/<IssueNo>/`
- Issue close・PR merge後: `archive/<IssueNo>/`

## 推奨ファイル

- `context.md`: 目的、対象、参照先、現在の状態
- `impact-scope.md`: 影響範囲、依存、競合、調査状態
- `decisions.md`: 実装・分割・レビューでの判断
- `handoff.md`: 未完了事項、次の作業、確認事項

作業contextはIssueやdocsの代替ではない。完了条件や正規仕様はIssue・要件・設計へ反映し、Task contextには参照リンクを残す。

---
name: issue-to-pr-workflow
description: Issueの作成、レビュー、実装、commit、push、PR作成、PRレビュー、修正までを一貫して進める。GitHub上のIssue/PRを起点に、完了条件とレビュー指摘を管理する開発フローで使用する。
---

# Issue to PR Workflow

## 目的

ユーザーの要求をIssue、docs、実装、PRの順に具体化し、各段階でレビューと修正を行う。フェーズの詳細は [phases.md](references/phases.md) を参照する。

レビューは、対象に応じて次のSkillを参照する。

- Issue: [issue-review](../issue-review/SKILL.md)
- docs: [docs-review](../docs-review/SKILL.md)
- 実装: [implementation-review](../implementation-review/SKILL.md)

すべてのレビューで、🔴がなくなるまで修正と再レビューを行う。🔴が存在する場合は、🟡と🟢も同じサイクルで可能な限り修正する。

## 実行前の確認

次の情報が不足している場合は、合理的に補完できるものを除いて確認する。

- 対象リポジトリ
- Issueのタイトル、本文、完了条件
- Assignees、Labels、Milestone、Leadershipまたはプロジェクト固有の管理項目
- 作業ブランチの基点と命名規則
- IssueレビューおよびPRレビューの観点
- PRのAssignees、Labels、Milestone、Development、Reviewers

Issue作成、Issueコメント、Issue属性変更、commit、push、PR作成、PRコメント、PR属性変更は外部または共有状態を変更する。対象、変更内容、必要な権限を確認してから実行する。

## フェーズ実行

フェーズ一覧と各フェーズの入力・成果物・完了条件は [phases.md](references/phases.md) に定義する。通常は次の順で実行する。

1. Issue作成
2. Issueレビューと修正
3. docs作成
4. docsレビューと修正
5. 実装
6. 実装レビューと修正
7. commit
8. push
9. PR作成
10. PRレビューと修正

各フェーズの開始時に前フェーズの完了条件を確認し、終了時に成果物、レビュー結果、テスト結果、未解決事項を記録する。フェーズを省略する場合は理由を報告する。

### Issue作成後のdocsフェーズ

Issue作成とIssueレビューが完了したら、実装前にIssueを元にdocsを作成する。docsの種類はリポジトリの規約に合わせるが、少なくとも仕様、利用者または呼び出し側、動作フロー、データ/API、エラー、制約、完了条件との対応を整理する。

docs作成後は [docs-review](../docs-review/SKILL.md) を使ってレビューし、🔴がなくなるまで修正と再レビューを行う。Issueやdocsの変更が実装方針に影響する場合は、Issueレビューへ戻る。

## 各フェーズの詳細

実装、commit、push、PR作成、PRレビューの具体的な入出力と完了条件は [phases.md](references/phases.md) に従う。レビューの観点とコメント形式は、それぞれのレビューSkillに委譲する。

レビューコメントは、少なくとも次の形式で記録する。

```text
[🔴 必須修正] 対象: <ファイル、Issue項目、PR差分>
問題: <何が問題か>
理由: <なぜ修正が必要か>
修正案: <推奨する対応>
確認方法: <修正後の確認方法>
```

## 停止条件

次の場合は推測で進めず、ユーザーに確認する。

- 要求や完了条件が複数の意味に解釈できる
- 必須メタデータ、担当者、レビュー担当者が決まっていない
- スコープ外の変更や破壊的変更が必要になる
- 認証情報または権限が不足している
- push、PR作成、外部サービスへの変更について許可がない
- レビュー指摘の優先度を判断できない
- テスト失敗の原因を特定できない

各フェーズの終了時に、実施内容、対象URLや番号、テスト結果、未解決事項、次に必要な承認を簡潔に報告する。

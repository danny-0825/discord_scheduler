---
name: issue-to-pr-workflow
description: Issueの作成、レビュー、実装、commit、push、PR作成、PRレビュー、修正までを一貫して進める。GitHub上のIssue/PRを起点に、完了条件とレビュー指摘を管理する開発フローで使用する。
---

# Issue to PR Workflow

## 目的

チャットで受けた作業要望をタスクに分解し、独立性と依存関係を判定したうえで、Issue、docs、実装、PRの順に進める。Issue、SubAgent、branch、worktree、commit、PRの関係は [relationship-and-independence.md](references/relationship-and-independence.md) の実行計画で管理する。フェーズの詳細は [phases.md](references/phases.md)、タスク分解と並列実行は [task-decomposition.md](references/task-decomposition.md)、SubAgentの実行ライフサイクル・役割・権限は [subagents.md](references/subagents.md)、GitHubラベルの分類と付与ルールは [labels.md](references/labels.md) を参照する。

レビューは、対象に応じて次の独立したSkillを呼び出せる。呼び出さずにこのSkill自身でレビューしてもよい。

ワークフロー自体を変更・検証するときは [issue-to-pr-workflow-review](../issue-to-pr-workflow-review/SKILL.md) を使用する。特に、複数Issueへの分割、並列SubAgent、複数worktreeまたは複数PRが関係する場合は、実行前後にこのレビューSkillを呼び出す。

- Issue: [issue-review](../issue-review/SKILL.md)
- docs: [docs-review](../docs-review/SKILL.md)
- 実装: [implementation-review](../implementation-review/SKILL.md)

すべてのレビューで、🔴がなくなるまで修正と再レビューを行う。🔴が存在する場合は、🟡と🟢も同じサイクルで可能な限り修正する。

## 基本方針

- チャット入力は、最初にタスク分解と独立性判定を行う。Issueを1つにするか複数に分割するかは、独立性判定の結果に基づいてAIが決定する。
- Issue作成前に、Issue同士の`depends_on`、`blocks`、`related`、`conflicts_with`を実行計画へ記録し、依存関係がDAGであることを確認する。
- IssueごとにTask、SubAgent、書き込み範囲、branch、worktree、PRを一意に対応付ける。対応付けできないIssueやAgentは起動・実装・完了扱いにしない。
- 分割したタスクは原則として「1タスク・1 Issue・1ブランチ・1 PR」とする。
- 前提タスクがある場合は、その依存部分だけを直列実行する。独立したタスクはSubAgentと独立worktreeで並列実行する。
- 独立性判定で決めた変更ファイル・ディレクトリの範囲を、実装SubAgentの書き込み許可範囲として引き継ぐ。
- Issue、PR、コメント、docs、commitメッセージの説明文は日本語で作成する。commitのprefixは英語のConventional Commits形式を維持し、例は `feat: スケジュール登録を追加 (#123)` とする。
- Issue・PR作成権限は必要な場合に限り、対象タスクを担当する1つのSubAgentまたは親Agentへ付与する。重複作成を防ぐため、作成担当をタスクごとに1つだけ決める。
- 独立タスクの一部が失敗しても、依存していない他タスクは継続する。失敗タスクに依存する後続タスクだけを停止し、最後に全体結果を集約する。

## 実行前の確認

次の情報が不足している場合は、合理的に補完できるものを除いて確認する。

- 対象リポジトリ
- Issueのタイトル、本文、完了条件
- Assignees、Labels、Milestone、Leadershipまたはプロジェクト固有の管理項目
- 作業ブランチの基点と命名規則
- IssueレビューおよびPRレビューの観点
- PRのAssignees、Labels、Milestone、Development、Reviewers

IssueまたはPRのLabelsを扱う場合は、[labels.md](references/labels.md) の分類・付与ルールを適用する。GitHubのIssueラベルとGitのリリースタグ（`v<semver>`）を混同しない。

Issue作成、Issueコメント、Issue属性変更、commit、push、PR作成、PRコメント、PR属性変更は外部または共有状態を変更する。対象、変更内容、必要な権限を確認してから実行する。

Issue作成前に実行計画でTask、依存、競合、担当SubAgent、scopeを確定し、各フェーズで更新する。Codex公式にない独自JSON台帳を必須形式として扱わない。

## フェーズ実行

フェーズ一覧と各フェーズの入力・成果物・完了条件は [phases.md](references/phases.md) に定義する。通常は次の順で実行する。

1. チャット要求のタスク分解・独立性判定
2. 依存関係と並列実行計画の作成
3. Issue作成（Labelsを付与）
4. Issueレビューと修正
5. 最新基点ブランチの更新と作業worktree・ブランチ作成
6. docs作成
7. docsレビューと修正
8. 実装
9. 実装レビューと修正
10. commit
11. push
12. PR作成（IssueのLabelsを継承・確認）
13. PRレビューと修正
14. PRマージ後のworktree削除と結果集約

各フェーズの開始時に前フェーズの完了条件を確認し、終了時に成果物、レビュー結果、テスト結果、未解決事項を記録する。フェーズを省略する場合は理由を報告する。

### タスク分解・並列実行フェーズ

チャット入力をそのままIssue化せず、最初に [task-decomposition.md](references/task-decomposition.md) と [relationship-and-independence.md](references/relationship-and-independence.md) に従ってタスクを分解する。タスクごとに目的、完了条件、変更範囲、依存タスク、競合資源、担当SubAgent、Issue・ブランチ・worktree・PRの対応を決める。

独立タスクは、`multi_agent_v1__spawn_agent`で実際にSubAgentを起動し、タスクごとに専用worktreeを作成させて並列実行する。1タスクは1 Issue・1ブランチ・1 worktree・1 PRに対応させ、独立Issueを1つのPRへ混在させない。依存タスクは前提タスクのPRがマージされ、最新の基点ブランチへ反映された後に次のSubAgentを開始する。あるタスクが失敗しても、依存していないタスクは停止しない。

### 作業ブランチ・worktree作成フェーズ

Issueレビューで🔴がなくなり、Issueの作成条件が確定した後、docs作成または実装を開始する前に作業ブランチを作成する。プロジェクトに `gitflow-branching` Skillがある場合はそれを呼び出し、なければ次の手順を適用する。

1. `git status --short --branch` で未コミット変更を確認する。既存変更を破棄・退避せず、競合する場合は停止する。
2. `git remote -v`、`git branch --all`、`git worktree list` でremote、基点ブランチ、既存ブランチ、worktreeを確認する。
3. `git fetch origin` でリモートの最新状態を取得する。
4. 通常の開発では `origin/develop` を最新の基点とする。必要に応じてローカルの `develop` を `git switch develop` と `git pull --ff-only origin develop` で更新する。`develop` がない場合は勝手に作成せず確認する。
5. タスクごとに一意の `feature/{IssueNo}-{short-description}` と `../{repo}-worktrees/{IssueNo}-{short-description}` を割り当てる。並列タスクでは、担当SubAgent自身が `git fetch origin` 後に最新の `origin/develop` を基点としてブランチと専用worktreeを作成する。SubAgentを使わない場合だけ親Agentが作成する。
6. SubAgentは割り当てられたworktree内でdocs・実装・commit・push・PRを同じブランチで進め、親Agentはworktree path、branch、Issue、PRの対応を検証する。書き込み範囲は独立性判定で定めた範囲に限定し、worktreeを共有しない。
7. PRがマージされたことを確認したら、`git worktree remove <worktree-path>` でタスク専用worktreeを削除する。未コミット変更や未マージのcommitがある場合は削除せず停止する。

ブランチ作成、push、Issue・PR作成、マージ、worktree削除は共有状態を変更するため、対象と権限を確認する。`main`、`develop`への直接コミット、force push、履歴の書き換えは行わない。

### Issue作成後のdocsフェーズ

Issue作成とIssueレビューが完了したら、実装前にIssueを元にdocsを作成する。docsの種類はリポジトリの規約に合わせるが、少なくとも仕様、利用者または呼び出し側、動作フロー、データ/API、エラー、制約、完了条件との対応を整理する。

docs作成後は [docs-review](../docs-review/SKILL.md) を使ってレビューし、🔴がなくなるまで修正と再レビューを行う。Issueやdocsの変更が実装方針に影響する場合は、Issueレビューへ戻る。

### Workflowレビュー

ワークフローのSkillまたは参照資料を変更した場合、またはIssue分割・並列SubAgent・複数worktree・複数PRを含む場合は、[issue-to-pr-workflow-review](../issue-to-pr-workflow-review/SKILL.md) の静的チェックとworktree分離スモークテストを実行する。🔴が残る場合は修正して再レビューし、検証結果をIssueまたはPRへ記録する。

## GitHub CLI・Project連携フェーズ

GitHub CLIを使うIssue・PR・Project操作は、[github-cli-auth.md](references/github-cli-auth.md)に従い、Keychainを利用できる通常権限のzsh環境で対象コマンドだけを実行する。サンドボックス全体を無効化せず、認証トークンを別の保存先へコピーしない。PR作成時はIssueのclosing keywordによるDevelopment連携と、Projectへの追加・フィールド更新を別々に確認し、Project操作が未実行なら完了扱いにしない。

GitHub CLIの認証手順とProject／Development連携の詳細は [github-cli-auth.md](references/github-cli-auth.md) を参照する。Issue・PRコメントの改行保持は [comment-posting.md](references/comment-posting.md) を参照する。

## 各フェーズの詳細

実装、commit、push、PR作成、PRレビューの具体的な入出力と完了条件は [phases.md](references/phases.md) に従う。レビューの観点とコメント形式は、それぞれのレビューSkillに委譲する。

レビューコメントは、IssueとPRで同じ指摘IDを使い、コメントの先頭に前回指摘の解消状況と新規指摘一覧を置く。`{IssueNo}` は対象Issue番号、`{指摘No}` はそのIssue内で通し採番する。修正後も既存IDは再利用・変更せず、新しい指摘だけ次の番号を採番する。

前回指摘の解消状況:

```markdown
| ID | レベル | チェック |
| --- | --- | --- |
| {IssueNo}-{指摘No} | 🔴 | ✅ / ⛔️ |
```

新たな指摘:

```markdown
| ID | レベル | 概要 |
| --- | --- | --- |
| {IssueNo}-{指摘No} | 🔴 / 🟡 / 🟢 | xxxxxx |
```

表の後ろに、IDごとの詳細を記録する。

### {IssueNo}-{指摘No}

**問題**:

<問題の内容>

**理由**:

<なぜ修正が必要か>

**修正案**:

<具体的な修正案>

**確認方法**:

<修正後の確認方法>

実際のIssue/PRコメントでは、外側のコードフェンスを付けず、次のMarkdown形式で投稿する。

### {IssueNo}-{指摘No}

**レベル**: 🔴 必須修正

**対象**: <ファイル、Issue項目、PR差分>

**問題**:

<何が問題か>

**理由**:

<なぜ修正が必要か>

**修正案**:

<推奨する対応>

**確認方法**:

<修正後の確認方法>

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

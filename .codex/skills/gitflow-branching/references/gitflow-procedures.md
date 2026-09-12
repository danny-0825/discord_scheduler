# GitFlow 手順リファレンス

## 作業開始

feature または bugfix は、必ず最新化した `origin/develop` から作成する。複数タスクを並列実行する場合はタスクごとに専用worktreeを使う。

```bash
git status --short --branch
git fetch origin
git worktree add ../discord_scheduler-worktrees/123-add-reminders \
  -b feature/123-add-reminders origin/develop
```

単一worktreeで作業する場合は、未コミット変更がないことを確認してから次を実行する。

```bash
git switch develop
git pull --ff-only origin develop
git switch -c feature/123-add-reminders
```

Issue番号がない場合は `feature/add-reminders` のように簡潔な説明を使う。Issue番号がある場合は必ずブランチ名に含める。

PRがマージされた後、未コミット変更がないことを確認して専用worktreeを削除する。

```bash
git worktree remove ../discord_scheduler-worktrees/123-add-reminders
```

## リリース準備

リリース依頼では、目標 SemVer を先に確定する。`release/<semver>` では機能追加を行わず、バージョン、CHANGELOG などのリリースメタデータとリリース阻害バグだけを扱う。

```bash
git switch develop
git pull --ff-only origin develop
git switch -c release/1.2.0
# pubspec.yaml の version: を 1.2.0 に更新し、検証する
dart format --output=none --set-exit-if-changed .
dart analyze
dart test
```

完了時の標準順序は次の通り。push、タグ、削除を依頼されていないなら、そこでは停止して確認する。

```bash
git switch main
git pull --ff-only origin main
git merge --no-ff release/1.2.0 -m "リリース: 1.2.0をmainへマージ"
git tag -a v1.2.0 -m "Release v1.2.0"
git switch develop
git merge --no-ff release/1.2.0 -m "リリース: 1.2.0をdevelopへマージ"
```

## 緊急修正

本番版に対する緊急修正だけを `main` から `hotfix/<patch-version>` として作成する。修正後は release と同じ検証を行い、`main` にマージしてタグを作り、同じ修正を `develop` にもマージする。

```bash
git switch main
git pull --ff-only origin main
git switch -c hotfix/1.2.1
# pubspec.yaml の version: を 1.2.1 に更新し、検証する
git switch main
git merge --no-ff hotfix/1.2.1 -m "緊急修正: 1.2.1をmainへマージ"
git tag -a v1.2.1 -m "Release v1.2.1"
git switch develop
git merge --no-ff hotfix/1.2.1 -m "緊急修正: 1.2.1をdevelopへマージ"
```

## 競合・例外

GitHub CLIでIssue、PR、Projectを操作する場合は、macOS Keychainの認証を利用できる通常権限のzsh環境で対象コマンドだけを実行する。Codexのサンドボックス内で認証が失敗しても、トークンをコピーせず、[Issue to PR WorkflowのGitHub CLI認証手順](../../issue-to-pr-workflow/references/github-cli-auth.md)に従って再確認する。

- merge conflict が起きたら、推測で解決せず、競合ファイルと選択肢を報告して止める。
- `main` または `develop` が存在しない、remote 名が `origin` でない、対象タグが既に存在する場合は、状態を確認してから手順を調整する。
- 既存のブランチ保護、CI、PR 必須ルールがある場合はそれを GitFlow の手順より優先し、ローカル merge の代わりに PR 作成手順を提示する。
- `git push --force`、タグの付け替え、履歴の書き換えは実行しない。明示的な承認と対象の再確認が必要である。

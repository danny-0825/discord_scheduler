# GitFlow 手順リファレンス

## 作業開始

feature または bugfix は `develop` から作成する。基点がローカルにない場合は、remote の `origin/develop` を確認してから作成する。

```bash
git switch develop
git pull --ff-only origin develop
git switch -c feature/123-add-reminders
```

`git pull` は未コミット変更がなく、対象 remote が確認できる場合だけ使う。Issue 番号がない場合は `feature/add-reminders` のように簡潔な説明を使う。

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
git merge --no-ff release/1.2.0 -m "Merge release/1.2.0"
git tag -a v1.2.0 -m "Release v1.2.0"
git switch develop
git merge --no-ff release/1.2.0 -m "Merge release/1.2.0 into develop"
```

## 緊急修正

本番版に対する緊急修正だけを `main` から `hotfix/<patch-version>` として作成する。修正後は release と同じ検証を行い、`main` にマージしてタグを作り、同じ修正を `develop` にもマージする。

```bash
git switch main
git pull --ff-only origin main
git switch -c hotfix/1.2.1
# pubspec.yaml の version: を 1.2.1 に更新し、検証する
git switch main
git merge --no-ff hotfix/1.2.1 -m "Merge hotfix/1.2.1"
git tag -a v1.2.1 -m "Release v1.2.1"
git switch develop
git merge --no-ff hotfix/1.2.1 -m "Merge hotfix/1.2.1 into develop"
```

## 競合・例外

- merge conflict が起きたら、推測で解決せず、競合ファイルと選択肢を報告して止める。
- `main` または `develop` が存在しない、remote 名が `origin` でない、対象タグが既に存在する場合は、状態を確認してから手順を調整する。
- 既存のブランチ保護、CI、PR 必須ルールがある場合はそれを GitFlow の手順より優先し、ローカル merge の代わりに PR 作成手順を提示する。
- `git push --force`、タグの付け替え、履歴の書き換えは実行しない。明示的な承認と対象の再確認が必要である。

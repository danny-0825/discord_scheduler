---
name: gitflow-branching
description: GitFlow 方式でこのプロジェクトのブランチ作成、命名、マージ、リリース、ホットフィックスを計画・実行する。ブランチ運用や Git 操作を依頼されたときに適用し、通常のコード変更だけには適用しない。
---

# GitFlow Branching

この Skill は、リポジトリの履歴を GitFlow の規約に沿って保つためのプロジェクト固有ルールである。依頼内容が「作業を実装する」だけならブランチ操作を勝手に追加せず、ブランチ運用が明示された場合に使う。

## このプロジェクトの規約

- `main`: リリース済みの安定版。直接コミットしない。
- `develop`: 次回リリースの統合先。通常の開発の基点。存在しなければ、作成・push 前にユーザーの意図を確認する。
- `feature/<issue>-<short-description>`: `develop` から作成し、機能追加・通常の変更に使う。
- `bugfix/<issue>-<short-description>`: `develop` から作成し、未リリースの不具合修正に使う。
- `release/<semver>`: `develop` から作成し、リリース準備だけを行う。例: `release/1.2.0`。
- `hotfix/<semver>`: `main` から作成し、本番リリース済み版の緊急修正に使う。例: `hotfix/1.2.1`。

ブランチ名は小文字 kebab-case とし、Issue 番号が分かる場合は含める。`main`、`develop`、既存の `release/*`／`hotfix/*` の直接編集や force push は避ける。

## 必ず最初に確認すること

1. `git status --short --branch` で未コミット変更と現在のブランチを確認する。
2. `git branch --list` と `git remote -v` で既存ブランチ・remote を確認する。ユーザーの未コミット変更は退避・破棄せず、競合する操作を止める。
3. 対象ブランチを最新化する必要がある場合は、fetch や pull の実行前に remote と作業ツリーの状態を確認する。
4. バージョンを扱う場合は `pubspec.yaml` の `version:` と既存タグを確認し、SemVer と整合させる。

## ライフサイクル

開始時は対象の基点を最新化し、`git switch -c <branch>` で新規ブランチを作る。既存ブランチがある場合は再利用できるか確認し、同名ブランチを上書きしない。

完了時は、変更の検証後に通常は `--no-ff` でマージし、履歴上で作業単位を残す。

- feature / bugfix → `develop`
- release → `main` と `develop` の両方。`main` 側で `pubspec.yaml` のリリース版を確定し、`v<semver>` タグを作成する。タグ作成後、release ブランチは削除候補として扱う。
- hotfix → `main` と `develop` の両方。`main` 側でパッチ版タグ `v<semver>` を作成する。

マージ先、push、タグ作成、ブランチ削除はリモートや履歴を変更する操作であるため、依頼に含まれていない場合はコマンド実行前にユーザーへ確認する。単に手順を求められた場合はコマンド案を提示するだけにする。

## このリポジトリの検証

Dart 変更をマージする前に、プロジェクトで利用可能な範囲で次を実行する。

```bash
dart format --output=none --set-exit-if-changed .
dart analyze
dart test
```

依存関係や SDK の都合でコマンドが失敗した場合は、失敗を成功扱いにせず、原因と未検証項目を報告する。release / hotfix では、バージョン更新、テスト、タグ対象コミットを確認してから完了とする。

詳細な開始・完了コマンド、例外時の判断は [references/gitflow-procedures.md](references/gitflow-procedures.md) を参照する。

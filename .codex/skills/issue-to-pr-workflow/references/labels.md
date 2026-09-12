# GitHubラベル運用ルール

このプロジェクトでは、GitHub IssueおよびPull Requestのラベルを、分類ごとに接頭辞で管理する。IssueラベルはGitのリリースタグとは別物である。リリースタグが必要な場合だけ、GitFlowの規約に従って`v<semver>`形式を使用する。

## 利用可能なラベル

### 種別（`type:`）

- `type: bug`: 不具合
- `type: feature`: 新機能・機能改善
- `type: docs`: ドキュメント
- `type: refactor`: リファクタリング
- `type: test`: テスト
- `type: chore`: 設定・保守作業

### 領域（`area:`）

- `area: api`: API・ルーティング
- `area: discord`: Discord連携
- `area: scheduler`: スケジューラー処理
- `area: infrastructure`: CI/CD・デプロイ
- `area: dependencies`: パッケージ・依存関係

### 優先度（`priority:`）

- `priority: high`: 優先対応
- `priority: medium`: 通常対応
- `priority: low`: 余裕があれば対応

### 状態（`status:`）

- `status: blocked`: 外部要因などで停止中
- `status: needs-info`: 追加情報待ち

## 付与ルール

1. Issueには`type:`を必ず1つ付与する。
2. Issueには該当する`area:`を、通常は1つ付与する。複数領域にまたがる場合だけ複数付与する。
3. 優先度が判断できるIssueには`priority:`を1つ付与する。判断できない場合は推測で付与しない。
4. 対応停止中または追加情報待ちの場合だけ`status:`を付与する。通常の対応中を示すラベルは作らない。
5. Pull Requestには、関連Issueの`type:`、`area:`、`priority:`を基本的に継承する。差分の実態と一致しない場合はPR側で調整する。
6. `duplicate`、`invalid`、`wontfix`、`question`、`good first issue`、`help wanted`、`accessibility`などの既存標準ラベルは、用途がある場合に限り補助的に使用する。
7. ラベルの新設・改名・削除は、既存Issue/PRへの影響を確認し、ユーザーの承認を得てから行う。

## Issue作成時の確認

Issue作成前に、タイトルと本文から`type:`、`area:`、必要な`priority:`を決める。ラベルが複数の意味を持つ場合は、1つのラベルに詰め込まず分類ごとに分ける。

例:

```text
type: feature
area: scheduler
priority: high
```

## Pull Request作成時の確認

PR作成時に、関連Issueが特定できること、Issueのラベルが適切であること、PRの変更範囲とラベルが一致することを確認する。PRだけで発生した追加作業がある場合は、必要に応じて`type:`または`area:`を追加する。

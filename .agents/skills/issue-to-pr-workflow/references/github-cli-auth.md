# GitHub CLI認証とProject連携

## 実行環境

- 通常のファイル操作、Git操作、テストはサンドボックス内で実行する。
- `gh`でIssue・PR・ProjectなどGitHubの共有状態を操作する場合は、Keychainを利用できる通常権限のzsh環境で実行する。Codexのサンドボックス内ではmacOS Keychainを参照できず、認証済みでもトークンが無効と判定されることがある。
- サンドボックス全体を無効化したり、認証トークンをファイルや環境変数へ複製したりしない。
- 実行前に`gh auth status`で対象アカウントと権限を確認する。トークン、device code、Keychainの内容は出力・コメント・ログへ転載しない。

## Project／Development連携

PR作成前後に、次を確認する。

1. `gh auth status`で`read:project`（Projectの参照）と、必要な書き込み権限が有効であることを確認する。
2. `gh project list --owner <owner>`で対象Projectを特定する。
3. IssueまたはPRをProjectへ追加・フィールド更新する場合は、対象Project番号、Issue/PR番号、変更するフィールドを再確認してから実行する。
4. PR本文には`Closes #<IssueNo>`などのGitHub closing keywordを含め、IssueとのDevelopment連携を自動化する。Projectへの追加は別操作として確認する。
5. `gh`が認証エラーになった場合は、シェルを変えて繰り返すのではなく、通常権限のzsh環境でKeychain認証を確認する。`gh auth login`または`gh auth refresh -s read:project`が必要なら、ユーザーに認証操作を依頼して停止する。

対象Projectが複数ある場合は、名前だけで推測せず、Project番号・URL・用途をIssueまたはユーザー確認で確定する。確定後、IssueをProjectへ追加する例は次のとおりである。

```zsh
gh project item-add <project-number> --owner <owner> \
  --url https://github.com/<owner>/<repo>/issues/<issue-number>
```

PR作成後も同じProjectへPRを追加し、Issueの自動連携だけでProjectへの追加が完了したとみなさない。追加結果は`gh project item-list <project-number> --owner <owner> --format json`で確認する。

Projectの存在確認だけでなく、追加・フィールド更新などの変更を行う場合は、通常の外部サービス変更として対象と内容を記録する。Project連携に必要なAPIまたは`gh`のサブコマンドが利用できない場合は、成功扱いにせず未完了として報告する。

# GitHub CLI認証とProject連携

## 必要な能力

- 通常のファイル操作、Git操作、テストは、その実行環境で許可された範囲で実行する。
- Issue・PR・ProjectなどGitHubの共有状態を操作する前に、利用可能なGitHubクライアントまたはAPIが対象repositoryへの認証・必要な権限を持つことを確認する。
- 認証情報をファイル、環境変数、コメント、ログへ複製・転載しない。特定のシェル、credential store、CLI、内部tool名を前提にしない。
- 必要な能力または権限がない場合は、別の保管方式や未承認の回避策を試さず、effect gateを`blocked`として親Agentへ報告する。

## Project／Development連携

PR作成前後に、次を確認する。

1. 利用可能なGitHubクライアントまたはAPIで、Project参照と必要な書込み権限が有効であることを確認する。
2. 対象Projectを番号・URL・用途で特定する。
3. IssueまたはPRをProjectへ追加・フィールド更新する場合は、対象Project番号、Issue/PR番号、変更するフィールドを再確認してから実行する。
4. PR本文には`Closes #<IssueNo>`などのGitHub closing keywordを含め、IssueとのDevelopment連携を自動化する。Projectへの追加は別操作として確認する。
5. 認証または能力の確認に失敗した場合は、実行環境を変えて繰り返したり認証情報を移さず、ユーザーまたは権限所有者へ確認を依頼して停止する。

対象Projectが複数ある場合は、名前だけで推測せず、Project番号・URL・用途をIssueまたはユーザー確認で確定する。確定後、IssueをProjectへ追加する例は次のとおりである。

```zsh
gh project item-add <project-number> --owner <owner> \
  --url https://github.com/<owner>/<repo>/issues/<issue-number>
```

PR作成後も同じProjectへPRを追加し、Issueの自動連携だけでProjectへの追加が完了したとみなさない。追加結果は`gh project item-list <project-number> --owner <owner> --format json`で確認する。

Projectの存在確認だけでなく、追加・フィールド更新などの変更を行う場合は、通常の外部サービス変更として対象と内容を記録する。Project連携に必要なAPIまたは`gh`のサブコマンドが利用できない場合は、成功扱いにせず未完了として報告する。

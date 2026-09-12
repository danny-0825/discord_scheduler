# Workflow検証シナリオ

## シナリオA: 独立タスク2件

T1とT2が異なるディレクトリを変更する場合、2つのSubAgentを並列起動する。各Agentが異なるworktreeとbranchを作成し、各自のcommitを作成できることを確認する。PRはT1用とT2用に分ける。

## シナリオB: 依存タスク

T3がT1のdocsを前提とする場合、T1のPRマージ前にT3を起動しない。T1のmerge commitを確認した後、T3のAgentが最新の`origin/develop`から新しいworktreeを作成する。

## シナリオC: 部分失敗

T1が失敗し、T2が独立している場合、T2は継続する。T3がT1に依存する場合、T3だけをblockedにする。最終報告には成功、失敗、blockedを分けて記録する。

## シナリオD: マージ後整理

T1用PRをマージした後、T1のworktreeとbranchを削除する。T2の作業環境には影響を与えない。

## 実行範囲

このシナリオは、外部GitHubを変更しないdry-runとローカルGitスモークテストで検証する。Issue作成、push、PR、mergeを実環境で検証する場合は、ユーザーの明示的な許可と対象リポジトリを確認する。

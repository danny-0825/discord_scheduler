# Context利用規約

- 正規仕様をcontextへコピーしない。要約・リンク・判断記録に限定する。
- Issue、PR、コメント、docs、commitの説明は日本語で記載し、commit prefixだけ英語のConventional Commits形式にする。
- ブランチは`git fetch origin`後の最新`origin/develop`から作成する。
- Issue単位のcontextは`task/active/<IssueNo>/`に置き、close・merge後にarchiveする。
- 外部情報は出典と取得日・確認日を残し、秘密情報を保存しない。
- 参照先と正規情報源が変わった場合は、registryと影響範囲表を同じTaskで更新する。
- 広範なドキュメント探索は`document-search` SkillのBM25検索を先に使い、上位結果の本文と正規情報源を確認する。

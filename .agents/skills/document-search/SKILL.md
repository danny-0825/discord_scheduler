---
name: document-search
description: リポジトリ内のdocs、context、Skill、Agent定義をBM25で順位付けして検索する。作業開始時の広範なドキュメント探索や、関連する既存仕様・運用ルールの発見に使用する。
---

# Document Search

## 目的

大量のドキュメントを全文走査する前に、BM25で関連度の高いファイルを絞り込む。検索結果だけで仕様を確定せず、上位候補の本文と正規情報源を必ず確認する。

## 使い方

リポジトリルートから実行する。

```sh
python3 .agents/skills/document-search/scripts/search_docs.py "検索語" --root docs --root .agents/skills --limit 10
```

段階的に検索する。

1. `docs/context`と`docs/`を検索する。
2. 関連するSkill・Agentが必要な場合だけ`.agents/skills`や`.codex/agents`を追加する。
3. 上位結果の本文、リンク先、正規情報源を読み、Issue・影響範囲へ反映する。

## 検索仕様

- BM25の既定値は`k1=1.5`、`b=0.75`とする。
- IDF、出現頻度、文書長正規化を使い、スコア降順で返す。
- Unicode NFKCとcasefoldで正規化する。
- ASCII/Unicode単語に加え、日本語・中国語・韓国語を文字bigramとして扱う。形態素解析器は必須にしない。
- 対象はMarkdownファイルで、`.git`、`.dart_tool`、`build`、`__pycache__`は除外する。
- 同率スコアはパス順で安定化する。

## 制約

BM25は語彙が一致する文書を優先するため、「コーヒー」と「珈琲」のような同義語・意味類似は見つけられない。検索漏れが疑われる場合は表記揺れ、英訳、パス、リンクグラフを追加で確認する。詳細なランキングロジックは[検索設計](references/search-design.md)を参照する。

このSkillは検索だけを担当し、Issue、docs、コード、外部サービスを変更しない。検索結果を元に変更する場合は、`issue-to-pr-workflow`へ引き継ぐ。

# BM25検索設計

## スコア

文書`d`とquery`q`のスコアは、queryの各tokenについて次で計算する。

```text
score(q, d) = Σ IDF(t) × (f(t,d) × (k1 + 1)) /
             (f(t,d) + k1 × (1 - b + b × |d| / avgdl))
```

- `f(t,d)`: 文書内のtoken出現数
- `|d|`: 文書のtoken数
- `avgdl`: 全文書の平均token数
- `IDF(t)`: `log(1 + (N - df(t) + 0.5) / (df(t) + 0.5))`
- `N`: 文書数、`df(t)`: tokenを含む文書数

## Tokenizer

NFKC・casefold後、ASCII/Unicodeの単語をtokenにする。CJK文字列は全文tokenに加えて隣接文字のbigramを生成する。これにより「要件定義」のような日本語queryを空白なしで検索できるが、形態素境界や固有名詞の意味を理解するものではない。

## 再現性

検索時にインデックスをメモリ上へ構築するため、外部データベースや事前生成indexは不要である。検索対象root、`k1`、`b`、limitを実行コマンドに残せば同じ状態を再現できる。

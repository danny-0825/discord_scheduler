---
type: skill
status: active
tags:
  - docs/skill
related:
  - "[[docs/governance/obsidian-docs]]"
  - "[[docs/index]]"
  - "[[docs/skills/catalog]]"
updated: 2026-09-14
---

# Skill docs

Skill docsは、Skillをいつ使うか、何を入力し、何を出力し、どの範囲を変更できるかを説明する。実体の手順は`.agents/skills/<skill-name>/SKILL.md`を参照し、本文を重複させない。

利用時の主入口、近接Skillとの境界、明示起動ポリシーは [[docs/skills/catalog|Skill catalog and routing]] を正規情報源とする。

## 必須項目

- 適用条件・対象外
- 入力・成果物
- 呼び出せるSkill・SubAgent
- 書き込み範囲と外部変更権限
- 認証情報・安全性の境界
- 検証方法
- 関連Workflow、Issue、PR

Skill docsもObsidian Propertiesと内部Wikilinkを持たせ、VaultのMOCから辿れるようにする。

## BM25検索

ドキュメント探索には[document-search Skill](../../.agents/skills/document-search/SKILL.md)を使用する。実装はリポジトリ内のMarkdownを対象とする依存なしCLIで、詳細な検索設計はSkillのreferenceを正規情報源とする。Agent TOMLや実装コードは、このSkillの対象外である。

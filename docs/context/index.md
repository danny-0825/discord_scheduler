# プロジェクトContext

このディレクトリは、作業開始時に必要なプロジェクト情報を短時間で参照するためのcontext packetです。正規の要件・設計・Workflow本文を複製せず、要約と参照先を管理します。

## 入口

- [Context registry](registry.md): 情報源、用途、更新契機、鮮度、アーカイブ方針
- [Core context](core/): プロジェクト、構成、規約の要約
- [Task context](task/): Issue単位の作業contextと引き継ぎ
- [External resources](external/): 外部情報の出典・取得日・版・確認日
- [Generated context](generated/): 再生成可能な成果物の扱い

## Source of truth

- 要件・設計・Workflowの正規本文は、それぞれ[docs運用ルール](../governance/docs-governance.md)で定める既存分類に置く。
- contextは探索性を高める要約・リンク・作業状態であり、正規本文と矛盾させない。
- 矛盾を発見した場合は、正規本文を確認してcontextを更新し、必要なら影響範囲を再調査する。

## 更新契機

Workflowの変更、構成・責務・運用規約の変更、外部仕様の参照、Issueの開始・完了時に[registry](registry.md)を確認する。

---
type: skill
status: active
tags:
  - docs/skill
  - ai-assets
  - routing
related:
  - "[[docs/skills/README]]"
  - "[[docs/governance/ai-operating-standard]]"
  - "[[docs/research/codex-ai-rearchitecture]]"
updated: 2026-09-14
---

# Skill catalog and routing

Issue #50 / T49 の正規Skill catalog。機械可読な契約、21件の代表prompt、及び境界promptは [catalog-routing-fixtures.json](../../.agents/skills/catalog-routing-fixtures.json) に置く。この文書は利用者向けの入口であり、個別手順を複製しない。

## Routing rules

- 依頼の主目的が一つの `primary_for` に一致するときだけ、そのSkillを選ぶ。複数Skillの順次実行が必要な場合は、親の実行計画にその順序と所有者を記録する。
- `boundary` は近接するが選択しない入口である。曖昧な依頼を両方のSkillで処理しない。
- `read-only` は外部または永続状態を変更しない。`*-write` は変更を起こし得るため、実行時に対象・権限・副作用を確認する。
- 書込み・外部操作を伴う14 Skill（Obsidian CLI 7、GitFlow、implementation finder、project-memory 5）は `allow_implicit_invocation: false` とし、明示的なSkill指定を必要とする。Obsidian workflowは加えて登録済みの `workflow_id` を必要とする。これはこのリポジトリの明示的な運用判断である。
- `issue-to-pr-workflow` は開発要求の主routeとして暗黙起動を許容する。Git/GitHub等の外部操作は親Agentだけがeffect gateで対象・内容・権限を確認してから行い、拒否または能力不足なら実行せず`blocked`にする。状態遷移と証跡はWorkflow Skillが正規情報源である。
- `document-search` はMarkdownを読むread-only例外であり、UI manifestを持たない。Agent TOMLや実装コードを探す場合は `rg` 等の通常の探索を使う。

## 開発運用

| Skill | 主目的 | 入力 → 成果物 | 副作用 | 近接する境界 |
| --- | --- | --- | --- | --- |
| `docs-review` | Issueに対するdocs review | Issue/docs/scope → 指摘 | read-only | docs作成ではない |
| `document-search` | Markdown仕様の発見 | query/roots → 順位付き結果 | read-only | TOML/コード検索ではない |
| `gitflow-branching` | branch/worktree操作 | Git操作/状態 → 実行計画またはGit状態 | repository Git write | Issue/PRの本文管理ではない |
| `implementation-finder` | 類似実装の比較 | job spec/先行例 → 推奨 | project-memory write | 実装やreviewではない |
| `implementation-review` | 実装差分review | Issue/docs/diff/tests → 指摘 | read-only | Issue本文reviewではない |
| `issue-review` | Issueの実装可能性review | Issue/scope/deps → 指摘 | read-only | 実装済み差分reviewではない |
| `issue-to-pr-workflow` | IssueからPRまでの状態契約 | 要望/Task plan → 状態・証跡・開発進行記録 | 親Agentがeffect gate後にGit/GitHub操作 | Workflow監査ではない |
| `issue-to-pr-workflow-review` | Workflow契約監査 | Workflow/plan/evidence → scenario結果 | read-only | 個別Issue reviewではない |

## Obsidian CLI（明示起動のみ）

| Skill | 主目的 | 入力 → 成果物 | 副作用 | 近接する境界 |
| --- | --- | --- | --- | --- |
| `obsidian-official-cli` | note・metadata操作 | vault/path → command結果 | vault write | runtime/Sync/Publishではない |
| `obsidian-cli-bases-and-bookmarks` | Bases/Bookmarks | base/bookmark → queryまたは変更結果 | vault write | note CRUDではない |
| `obsidian-cli-devtools` | runtime診断 | diagnostic request → 証跡 | runtime write | runtime管理ではない |
| `obsidian-cli-runtime-admin` | plugin/theme等の管理 | admin request → 状態または変更結果 | runtime write | 診断ではない |
| `obsidian-cli-sync-and-publish` | Sync/Publish | request/probe → remote状態または変更結果 | remote write | local note編集ではない |
| `obsidian-cli-workflows` | 登録workflowのオーケストレーション | workflow ID/mode → planまたは実行結果 | delegated write | raw commandではない |
| `obsidian-cli-workspace-and-navigation` | workspace/tab/navigation | state request → 結果 | workspace write | note CRUDではない |

## Project memory

| Skill | 主目的 | 入力 → 成果物 | 副作用 | 近接する境界 |
| --- | --- | --- | --- | --- |
| `project-autojournal` | 全候補の自動checkpoint | AI/repo evidence → notes/state | project-memory write | 単一handoffではない |
| `project-completed-summary` | 完了作業の保存 | completed evidence → summary note | project-memory write | 進行中checkpointではない |
| `resume-project-context` | 作業文脈の復元 | project/notes/state → resume summary | read-only | note作成ではない |
| `retro-summary` | 過去作業の遡及保存 | historic clue/evidence → summary note | project-memory write | 現在完了した作業ではない |
| `save-work-checkpoint` | 進行中作業のhandoff | current thread/state → checkpoint note | project-memory write | bulk autojournalではない |
| `setup-obsidian-work-skills` | project-memory環境設定 | vault/roots/sources → verified config | local-config write | note作成ではない |

## Maintenance and validation

1. Skillを追加・統合・廃止する前に、このcatalogで主目的・I/O・副作用・最も近い境界を更新する。
2. 21件すべてについてnormal/boundary promptを一件ずつ維持する。各fixtureの`expected_skill`は選ぶSkill、`non_selected_skill`は近接しても選ばないSkill、`implicit_invocation_allowed`は`expected_skill`の暗黙起動可否であり、`expected_skill: none`では必ず`false`とする。promptは評価入力であり、LLM出力を正規表現で固定するものではない。
3. `python3 .agents/skills/tests/validate_skill_catalog.py` を実行し、catalog、`SKILL.md`、manifest、fixtureの対応を検証する。
4. Skill構造は `issue-to-pr-workflow-review/scripts/validate_skill_stdlib.py` で別途検証する。Workflow 2 Skillの実行契約はT50の所有であり、T49では変更しない。

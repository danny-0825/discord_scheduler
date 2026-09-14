---
type: design
status: active
tags:
  - docs/research
  - codex
  - skills
  - agents
  - workflow
related:
  - "https://github.com/danny-0825/discord_scheduler/issues/48"
  - "[[docs/research/index]]"
  - "[[docs/research/ai-keyword-catalog]]"
  - "[[docs/governance/ai-operating-standard]]"
updated: 2026-09-13
---

# Codex AI資産の調査と再構成設計

## 概要

本調査は、Codex公式資料を設計の一次基準にし、Claude CodeとGitHub Copilotの公式資料を比較根拠として用いる。対象はアプリ本体ではなく、21 Skill、7 Custom Agent、Workflow、AI向けdocsと検証契約である。

**作成来歴**: Issue #48 / T48。執筆は`docs_author`、レビューは`docs_reviewer`が担当する。

## 一次情報で確認した事実

Codexでは、`AGENTS.md`は持続的な指示、Skillsは再利用可能な手順、MCPは外部接続、SubAgentは専門・独立作業の委譲という補完関係にある。[^1] repository Skillは`.agents/skills`で検出され、name/descriptionを先に読み、選択後に`SKILL.md`と必要な参照を読むため、descriptionの簡潔さと段階的開示が重要である。[^2]

Custom Agentは`.codex/agents/*.toml`に置き、`name`、`description`、`developer_instructions`を必要とする。独立・並列可能な作業だけを委譲し、ホストで公開された能力以外を実行契約にしない。[^3] worktreeは並列作業の隔離手段だが、Issue/branch/PRの1対1はプロジェクト固有方針である。[^4] sandboxは技術的到達範囲、approvalは操作ごとの確認を担い、両方をWorkflowで扱う。[^15]

現在のローカルCLIと公式config記述には`[agents]`の互換性差が観測されている。公式config referenceを一般論として扱い、設定値の一般論で上書きせず、各変更で`codex features list`等の実環境ヘルスチェックを先に通す。[^16]

## 比較からの分析

| 観点 | Claude Code / GitHub Copilotの共通根拠 | 本プロジェクトへの判断 |
| --- | --- | --- |
| 指示 | 常時読むinstructionsは短く、詳細手順は必要時に読み込むSkillへ置く。[^5][^6] | AGENTSは境界だけ、実行状態機械はWorkflow Skillへ集約する。 |
| Skill | descriptionで選択し、scripts/resourcesを必要なときだけ使う。[^7][^8] | 同じ意図・副作用のSkillを統合し、複合手順はreferencesへ移す。 |
| Agent | 役割・権限・tool surfaceを狭め、read-only調査を適切な委譲先にする。[^9][^10] | 7 roleを維持し、親が外部操作と統合を所有する。 |
| 並列性 | worktree/環境隔離だけでなく、ファイル所有権と依存を分ける。[^11][^12] | 共有AI契約の変更は直列、独立したread-only調査だけを並列化する。 |
| 評価 | 静的検証と代表promptによる行動評価を分ける。[^13][^14] | 構造checker、worktree smoke、シナリオ評価を分離する。 |

## 再構成の決定

1. **Skills**: 開発運用、Obsidian知識操作、project-memoryを意図・副作用・入出力で再カタログ化し、重複Skillを統合又は廃止する。
2. **Workflow**: `構造化計画 → read-only調査 → Issueレビュー → 親のworktree準備 → 委譲/実装 → 検証/レビュー → PR → 整理`を唯一の実行契約にする。
3. **Agents**: 7 roleを役割固有のI/Oへ縮小し、Agent名・ファイル名・Workflow role表を静的検証する。
4. **docs/context**: 正規仕様を複製せず、入口・registry・調査出典を提供する。

## 後続Task DAG

`T48 → T49(Skill catalog) → T50(Workflow) → T51(Agents) → T52(integration validation)` とする。T52はT49/T50/T51の完了を必要とする。各Taskは1 Issue・1 branch・1 worktree・1 PRを持ち、共有する`AGENTS.md`、role表、契約テストは同時編集しない。

| Task | 依存・担当 | read / write / forbidden scope | 成果物・受入条件 | 共有資源 |
| --- | --- | --- | --- |
| T49 | T48後。実装: `implementation_worker`、レビュー: `workflow_reviewer`、利用Skill: `skill-creator` | read: AI assets全体。write: Workflow以外の`.agents/skills/**`、Skill catalog docs。forbidden: `.codex/**`、`AGENTS.md`、`.agents/skills/issue-to-pr-workflow/**`、`.agents/skills/issue-to-pr-workflow-review/**`。 | catalog/routing/manifest/移行表。1 intentに1主Skill、構造・代表prompt検証。 | catalogだけをT49が所有。 |
| T50 | T49後。実装: `implementation_worker`、レビュー: `workflow_reviewer` | read: T49成果物、現Workflow。write: `.agents/skills/issue-to-pr-workflow/**`、`.agents/skills/issue-to-pr-workflow-review/**`、Workflow docs。forbidden: `.codex/**`、`AGENTS.md`、その他Skill catalog。 | 唯一の状態機械、Plan/SubAgent fallback、parent-provision契約、シナリオ検証。 | 実行状態機械だけをT50が所有。 |
| T51 | T50後。`implementation_worker`、`workflow_reviewer` | read: T50成果物、role定義。write: `.codex/agents/**`、`AGENTS.md`のrole境界。forbidden: Workflow Skill/refs、Skill catalog。 | 7 roleのI/O/scopeが一意、外部操作は親所有、mapping検証。 | role registryとAGENTS role境界をT51が所有。 |
| T52 | T49/T50/T51後。実装: `implementation_worker`、レビュー: `workflow_reviewer` | read: 全再構成成果物。write: 契約test、代表prompt評価、移行/archival docs。forbidden: catalog/Workflow/Agentの仕様変更。 | 全契約を通して検証し、旧入口の移行又は廃止を確認。 | 統合testと移行記録だけをT52が所有。 |

## 検証

- [ ] SourcesのURLと本文脚注を確認する。
- [ ] [[docs/research/index]]から各成果物へ到達できる。
- [ ] 後続Taskのscopeと依存が重複しない。
- [ ] 公式仕様とプロジェクト固有方針を混同していない。

## Sources

[^1]: OpenAI, [Customization overview](https://learn.chatgpt.com/docs/customization/overview), confirmed 2026-09-13.
[^2]: OpenAI, [Build skills](https://learn.chatgpt.com/docs/build-skills), confirmed 2026-09-13.
[^3]: OpenAI, [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), confirmed 2026-09-13.
[^4]: OpenAI, [Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees), confirmed 2026-09-13.
[^5]: Anthropic, [Features overview](https://code.claude.com/docs/en/features-overview), confirmed 2026-09-13.
[^6]: GitHub, [Repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions), confirmed 2026-09-13.
[^7]: Anthropic, [Skills](https://code.claude.com/docs/en/skills), confirmed 2026-09-13.
[^8]: GitHub, [Add skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), confirmed 2026-09-13.
[^9]: Anthropic, [Subagents](https://code.claude.com/docs/en/sub-agents), confirmed 2026-09-13.
[^10]: GitHub, [Create custom agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents), confirmed 2026-09-13.
[^11]: Anthropic, [Worktrees](https://code.claude.com/docs/en/worktrees), confirmed 2026-09-13.
[^12]: GitHub, [GitHub Copilot app](https://docs.github.com/en/copilot/concepts/agents/github-copilot-app), confirmed 2026-09-13.
[^13]: Anthropic, [Plugins](https://code.claude.com/docs/en/plugins), confirmed 2026-09-13.
[^14]: GitHub, [Test custom agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/test-custom-agents), confirmed 2026-09-13.
[^15]: OpenAI, [Agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security), confirmed 2026-09-13.
[^16]: OpenAI, [Config reference](https://learn.chatgpt.com/docs/config-file/config-reference), confirmed 2026-09-13.

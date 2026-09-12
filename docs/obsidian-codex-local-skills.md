# Obsidian and Codex local skills

## Purpose

This repository is also an Obsidian Vault. The local Codex skills under `.agents/skills/` provide Obsidian CLI guidance and project-memory workflows without changing the global Codex skill installation.

## Scope

The configuration covers:

- Obsidian CLI note, workspace, Bases, bookmark, runtime, sync, and workflow operations.
- Project checkpoint, context resume, completed summary, retrospective, and implementation-finding workflows.
- Project-local memory configuration in `.agents/project-memory.env`.

The configuration does not enable a scheduled autojournal timer and does not contain credentials or user-specific absolute paths.

Repository context and external memory are separate concerns. [`docs/context/`](context/index.md) is the repository-local context packet for source-of-truth links, task scope, and external-resource metadata. Obsidian `Work/` notes remain the external project-memory area; they are not copied into `docs/context/` and do not replace normative repository docs.

## Local activation

Run commands from the repository root:

```sh
export PROJECT_MEMORY_CONFIG="$PWD/.agents/project-memory.env"
```

The setting can be used by the project-memory skills for the current shell session. The repository itself is the Vault, and `Work/` is the default location for generated project-memory notes.

## Installed skills

Obsidian operations:

- `obsidian-official-cli`
- `obsidian-cli-bases-and-bookmarks`
- `obsidian-cli-devtools`
- `obsidian-cli-runtime-admin`
- `obsidian-cli-sync-and-publish`
- `obsidian-cli-workspace-and-navigation`
- `obsidian-cli-workflows`

Project management:

- `implementation-finder`
- `project-autojournal`
- `project-completed-summary`
- `resume-project-context`
- `retro-summary`
- `save-work-checkpoint`
- `setup-obsidian-work-skills`

## Verification

From the repository root, verify the setup with:

```sh
test -f .agents/project-memory.env
test "$(find .agents/skills -name SKILL.md | wc -l | tr -d ' ')" -ge 14
export PROJECT_MEMORY_CONFIG="$PWD/.agents/project-memory.env"
set -a
. "$PROJECT_MEMORY_CONFIG"
set +a
test "$PROJECT_MEMORY_VAULT" = "."
test "$PROJECT_MEMORY_REPO_ROOTS" = "."
! rg -n '/Users/|/home/|api[_-]?key=|token=|password=|secret=' .agents/project-memory.env
```

The final `rg` command should return no matches in the committed configuration file.

## Maintenance

Update the local skills from their upstream repositories deliberately and review changes before committing. Keep the project-local configuration portable and never add authentication tokens, personal paths, or global session exports.

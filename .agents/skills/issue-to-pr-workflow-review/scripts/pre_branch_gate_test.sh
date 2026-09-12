#!/usr/bin/env bash
set -euo pipefail

tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/issue-to-pr-pre-branch.XXXXXX")"
cleanup() {
  git -C "$tmp_root/repository" worktree remove --force "$tmp_root/worktree" 2>/dev/null || true
  rm -rf "$tmp_root"
}
trap cleanup EXIT

mkdir -p "$tmp_root/repository"
git -C "$tmp_root/repository" init -q -b develop
git -C "$tmp_root/repository" config user.name "pre-branch-gate-test"
git -C "$tmp_root/repository" config user.email "pre-branch-gate-test@example.invalid"
printf '%s\n' "baseline" > "$tmp_root/repository/README.md"
git -C "$tmp_root/repository" add README.md
git -C "$tmp_root/repository" commit -q -m "chore: initialize pre-branch gate test"

before="$(git -C "$tmp_root/repository" status --porcelain)"
test -z "$before"
base_commit="$(git -C "$tmp_root/repository" rev-parse develop)"

# Pre-branch inspection is read-only; no repository file is changed here.
git -C "$tmp_root/repository" status --short --branch >/dev/null
test "$(git -C "$tmp_root/repository" rev-parse HEAD)" = "$base_commit"
test -z "$(git -C "$tmp_root/repository" status --porcelain)"

# The first write-capable operation is the branch/worktree gate.
git -C "$tmp_root/repository" worktree add -q -b feature/101-gate "$tmp_root/worktree" develop
printf '%s\n' "post-branch change" > "$tmp_root/worktree/change.md"
test -f "$tmp_root/worktree/change.md"
test ! -e "$tmp_root/repository/change.md"

printf '%s\n' "pre-branch read-only gate: PASS"

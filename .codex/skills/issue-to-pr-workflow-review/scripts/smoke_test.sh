#!/usr/bin/env bash
set -euo pipefail

tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/issue-to-pr-workflow-review.XXXXXX")"
worktree_one="$tmp_root/worktrees/task-101"
worktree_two="$tmp_root/worktrees/task-102"

cleanup() {
  git -C "$tmp_root/repository" worktree remove --force "$worktree_one" 2>/dev/null || true
  git -C "$tmp_root/repository" worktree remove --force "$worktree_two" 2>/dev/null || true
  rm -rf "$tmp_root"
}
trap cleanup EXIT

mkdir -p "$tmp_root/repository"
git -C "$tmp_root/repository" init -q -b develop
git -C "$tmp_root/repository" config user.name "workflow-review-test"
git -C "$tmp_root/repository" config user.email "workflow-review-test@example.invalid"
printf '%s\n' "base" > "$tmp_root/repository/README.md"
git -C "$tmp_root/repository" add README.md
git -C "$tmp_root/repository" commit -q -m "chore: initialize smoke test"
base_commit="$(git -C "$tmp_root/repository" rev-parse develop)"

mkdir -p "$tmp_root/worktrees"
git -C "$tmp_root/repository" worktree add -q -b feature/101-task-one "$worktree_one" develop
git -C "$tmp_root/repository" worktree add -q -b feature/102-task-two "$worktree_two" develop

test "$(git -C "$worktree_one" branch --show-current)" = "feature/101-task-one"
test "$(git -C "$worktree_two" branch --show-current)" = "feature/102-task-two"
test "$(git -C "$worktree_one" rev-parse HEAD)" = "$base_commit"
test "$(git -C "$worktree_two" rev-parse HEAD)" = "$base_commit"
test "$worktree_one" != "$worktree_two"

printf '%s\n' "task one" > "$worktree_one/task-one.md"
git -C "$worktree_one" add task-one.md
git -C "$worktree_one" commit -q -m "docs: add task one"
printf '%s\n' "task two" > "$worktree_two/task-two.md"
git -C "$worktree_two" add task-two.md
git -C "$worktree_two" commit -q -m "docs: add task two"

test -f "$worktree_one/task-one.md"
test ! -e "$worktree_one/task-two.md"
test -f "$worktree_two/task-two.md"
test ! -e "$worktree_two/task-one.md"

git -C "$tmp_root/repository" worktree remove "$worktree_one"
git -C "$tmp_root/repository" worktree remove "$worktree_two"
git -C "$tmp_root/repository" branch -D -q feature/101-task-one feature/102-task-two
test "$(git -C "$tmp_root/repository" worktree list --porcelain | grep -c '^worktree ')" = "1"

printf '%s\n' "workflow worktree isolation smoke test: PASS"

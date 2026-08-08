#!/usr/bin/env bash
# Commit this stage's output and push it to the data branch.
#
# Routine sessions are ephemeral: nothing survives unless it is pushed. Every
# stage calls this as its last action.
#
#   scripts/publish.sh "stage 0: universe for 2026-08-10"
#
# Two ordering decisions carry this script.
#
# 1. The work is committed to the local HEAD *first*, before anything touches the
#    branch or the working tree. An earlier version checked out the data branch
#    before committing, so whenever the remote had moved — another stage
#    publishing, or someone pushing to main mid-run — the checkout failed on
#    locally-modified tracked files, `set -e` aborted, and an entire stage's
#    research was lost with nothing written anywhere. Commit first, reconcile
#    second: once the work is in a commit it survives any failed merge.
#
# 2. Conflicts in the generated files are resolved by *regenerating* them rather
#    than by picking a side. INDEX.md and PREDICTIONS.* are pure functions of
#    research/, so once both stages' research is merged, rebuilding gives the
#    correct answer — which neither side's version would. This also sidesteps the
#    --ours/--theirs inversion during a rebase, which is a reliable way to
#    silently keep the wrong file.

set -euo pipefail

MSG="${1:?usage: publish.sh <commit message>}"
BRANCH="${EARNINGS_DATA_BRANCH:-main}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Files that are rebuilt from research/ and must never be merged by content.
GENERATED=(INDEX.md PREDICTIONS.csv PREDICTIONS.json)

if [[ -z "$(git config user.email || true)" ]]; then
  git config user.email "earnings-routine@users.noreply.github.com"
  git config user.name  "Earnings Routine"
fi

# Whether a rebase is still in progress. Test the state directory, not
# REBASE_HEAD — that ref survives a *successful* `rebase --continue`, so using it
# as the sentinel loops forever and then aborts the rebase that already worked.
in_rebase() {
  [[ -d "$(git rev-parse --git-path rebase-merge)" ]] ||
  [[ -d "$(git rev-parse --git-path rebase-apply)" ]]
}

regenerate() {
  python3 scripts/update_index.py >/dev/null 2>&1 || true
  python3 scripts/build_predictions.py >/dev/null 2>&1 || true
}

# Clear conflicts in generated files so the rebase can continue. Their content
# is irrelevant — regenerate() overwrites them once the history is linear.
resolve_generated() {
  local conflicted resolved_any=0
  conflicted="$(git diff --name-only --diff-filter=U 2>/dev/null || true)"
  [[ -z "$conflicted" ]] && return 1
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    local is_generated=0
    for g in "${GENERATED[@]}"; do
      [[ "$f" == "$g" ]] && is_generated=1
    done
    if (( is_generated )); then
      : > "$f"
      git add -- "$f"
      resolved_any=1
    else
      echo "publish: unresolvable conflict in $f (not a generated file)" >&2
      return 1
    fi
  done <<< "$conflicted"
  return $(( resolved_any ? 0 : 1 ))
}

# ── 1. Commit the work where we stand ────────────────────────────────────────

# Stage only paths that exist: `git add` fails the whole invocation on a missing
# pathspec, and PREDICTIONS.* legitimately do not exist until first generated. An
# earlier version papered over that with a fallback that staged research/ alone,
# which left INDEX.md modified-but-unstaged and blocked the rebase below.
paths=()
[[ -d research ]] && paths+=(research)
for f in "${GENERATED[@]}" LEDGER.md; do
  [[ -e "$f" ]] && paths+=("$f")
done
if (( ${#paths[@]} == 0 )); then
  echo "publish: nothing to publish" >&2
  exit 1
fi
git add -A -- "${paths[@]}"

if git diff --cached --quiet; then
  echo "publish: nothing to commit"
  exit 0
fi

git commit -q -m "$MSG"
LOCAL_SHA="$(git rev-parse HEAD)"
echo "publish: committed $LOCAL_SHA"

# ── 2. Reconcile with the remote, then push ──────────────────────────────────

delay=2
for attempt in 1 2 3 4 5; do
  if ! git fetch -q origin "$BRANCH" 2>/dev/null; then
    echo "publish: fetch failed, retrying in ${delay}s (attempt $attempt)"
    sleep "$delay"; delay=$((delay * 2)); continue
  fi

  if git rev-parse --verify -q "refs/remotes/origin/$BRANCH" >/dev/null; then
    if ! GIT_EDITOR=true git rebase -q "origin/$BRANCH" >/dev/null 2>&1; then
      # Walk the rebase forward, clearing generated-file conflicts as they appear.
      guard=0
      while in_rebase && (( guard++ < 20 )); do
        if resolve_generated; then
          GIT_EDITOR=true git rebase --continue >/dev/null 2>&1 || true
        else
          echo "publish: aborting rebase — conflict needs a human" >&2
          git rebase --abort 2>/dev/null || true
          break
        fi
      done
      if in_rebase; then
        git rebase --abort 2>/dev/null || true
      fi
    fi

    # Rebuild the generated files against the now-merged research tree.
    if git merge-base --is-ancestor "origin/$BRANCH" HEAD 2>/dev/null; then
      regenerate
      if ! git diff --quiet -- "${GENERATED[@]}" 2>/dev/null; then
        git add -- "${GENERATED[@]}" 2>/dev/null || true
        git commit -q --amend --no-edit
      fi
    fi
  fi

  if git push -q origin "HEAD:$BRANCH" 2>/tmp/publish-push.log; then
    # Trust nothing: confirm the remote actually moved to our commit.
    git fetch -q origin "$BRANCH"
    if [[ "$(git rev-parse HEAD)" == "$(git rev-parse "origin/$BRANCH")" ]]; then
      echo "publish: pushed to origin/$BRANCH -> $(git rev-parse --short HEAD)"
      exit 0
    fi
    echo "publish: push reported success but the remote does not match" >&2
  fi

  echo "publish: push failed, retrying in ${delay}s (attempt $attempt)"
  tail -3 /tmp/publish-push.log 2>/dev/null | sed 's/^/  /' >&2 || true
  sleep "$delay"
  delay=$((delay * 2))
done

echo "publish: FAILED to push after 5 attempts." >&2
echo "publish: the work IS committed locally as $LOCAL_SHA — recover it with:" >&2
echo "  git push origin $LOCAL_SHA:$BRANCH" >&2
exit 1

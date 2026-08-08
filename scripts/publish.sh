#!/usr/bin/env bash
# Commit everything under research/ (plus INDEX.md) and push to the data branch.
#
# Routine sessions are ephemeral: nothing survives unless it is pushed. Every
# stage calls this as its last action.
#
#   scripts/publish.sh "stage 0: universe for 2026-08-10"
#
# Concurrency: stages are scheduled hours apart, but a manual re-run can still
# race a scheduled one. On a rejected push we re-fetch, rebase, and retry.
# Network failures retry with exponential backoff (2s, 4s, 8s, 16s).

set -euo pipefail

MSG="${1:?usage: publish.sh <commit message>}"
BRANCH="${EARNINGS_DATA_BRANCH:-main}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [[ -z "$(git config user.email || true)" ]]; then
  git config user.email "earnings-routine@users.noreply.github.com"
  git config user.name  "Earnings Routine"
fi

# Make sure we are on the data branch and current with the remote.
git fetch origin "$BRANCH" 2>/dev/null || true
if git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  git checkout -B "$BRANCH" "origin/$BRANCH"
else
  git checkout -B "$BRANCH"
fi

git add -A research INDEX.md LEDGER.md PREDICTIONS.csv PREDICTIONS.json 2>/dev/null \
  || git add -A research

if git diff --cached --quiet; then
  echo "publish: nothing to commit"
  exit 0
fi

git commit -q -m "$MSG"
echo "publish: committed -> $(git rev-parse --short HEAD)"

delay=2
for attempt in 1 2 3 4 5; do
  if git push -u origin "$BRANCH" 2>&1 | tee /tmp/publish-push.log; then
    echo "publish: pushed to origin/$BRANCH"
    exit 0
  fi

  if grep -qiE "non-fast-forward|fetch first|rejected" /tmp/publish-push.log; then
    # Someone else pushed. Replay our commit on top of theirs.
    echo "publish: remote moved, rebasing (attempt $attempt)"
    git fetch origin "$BRANCH"
    git rebase "origin/$BRANCH" || {
      echo "publish: rebase conflict — resolving in favour of our new files"
      git checkout --ours . 2>/dev/null || true
      git add -A
      git rebase --continue || git rebase --abort
    }
  else
    echo "publish: push failed, retrying in ${delay}s (attempt $attempt)"
    sleep "$delay"
    delay=$((delay * 2))
  fi
done

echo "publish: FAILED to push after 5 attempts" >&2
exit 1

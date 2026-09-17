#!/usr/bin/env bash
# The button. Rebuild the performance ledger from the runs and the broker, then
# render the dashboard.
#
#   ./edge/performance/update.sh              fetch fills + equity, re-price, render
#   ./edge/performance/update.sh --offline    no broker call; keep the last broker state
#   ./edge/performance/update.sh --publish    also commit and push the result
#   ./edge/performance/update.sh --fresh      drop the bar cache and re-price everything
#
# Safe to run any number of times a day: the price cache means a rebuild that adds
# one day costs one day of fetches, and nothing here places or cancels an order.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

PUBLISH=0
LEDGER_ARGS=()
for arg in "$@"; do
  case "$arg" in
    --publish) PUBLISH=1 ;;
    --fresh)   rm -rf .cache/bars; echo "update: bar cache dropped" ;;
    *)         LEDGER_ARGS+=("$arg") ;;
  esac
done

python3 edge/performance/scripts/build_ledger.py "${LEDGER_ARGS[@]+"${LEDGER_ARGS[@]}"}"
python3 edge/performance/scripts/build_dashboard.py

echo
echo "open: file://$REPO_ROOT/edge/performance/dashboard.html"

if (( PUBLISH )); then
  scripts/publish.sh "performance: ledger and dashboard through $(date -u +%Y-%m-%d)"
fi

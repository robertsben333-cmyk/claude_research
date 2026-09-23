#!/usr/bin/env bash
# The button. Rebuild the performance ledger from the runs and the broker, then
# render the dashboard.
#
#   ./dashboard/update.sh              fetch fills + equity, re-price, render
#   ./dashboard/update.sh --offline    no broker call; keep the last broker state
#   ./dashboard/update.sh --publish    also commit and push the result
#   ./dashboard/update.sh --fresh      drop the bar cache and re-price everything
#   ./dashboard/update.sh --no-feeders skip Trends, the forward calendar and the
#                                             Europe/Japan/Australia collector
#   ./dashboard/update.sh --serve      rebuild, then serve it so the page's own
#                                             refresh button works (localhost only)
#   ./dashboard/update.sh --serve-bg   the same, detached: you get your shell back
#                                             and the button works in the file you already
#                                             have open, because the page finds the server
#
# None of that reaches a page you FETCHED rather than opened: it has no machine of
# yours to build on. .github/workflows/dashboard.yml runs this same rebuild in CI,
# commits the result to main and republishes the site, and the page's own button
# starts it. See dashboard/README.md.
#
# Safe to run any number of times a day: the price cache means a rebuild that adds
# one day costs one day of fetches, and nothing here places or cancels an order.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PUBLISH=0
SERVE=0
FEEDERS=1
PORT=8765
LEDGER_ARGS=()
for arg in "$@"; do
  case "$arg" in
    --publish) PUBLISH=1 ;;
    --serve)   SERVE=1 ;;
    --serve-bg) SERVE=2 ;;
    --fresh)   rm -rf .cache/bars; echo "update: bar cache dropped" ;;
    --no-feeders) FEEDERS=0 ;;
    *)         LEDGER_ARGS+=("$arg") ;;
  esac
done

# Two feeders the ledger reads but does not compute. Both are cached and both are
# allowed to fail: a Trends rate-limit or a Nasdaq hiccup must not cost you the
# rebuild. The ledger records their absence as a problem rather than a zero.
#   search volume -> the Zoekvolume tab   (cache: researcher_us/analysis/trends-cache.json)
#   the calendar  -> the Agenda tab       (dropped by the ledger once >3 days old)
#   the markets   -> the Europa, Japan and Australië tabs
#
# The markets feeder is the only one that can WRITE outside dashboard/: with
# --resolve it calls eu_resolve.py, jp_resolve.py or au_resolve.py for a run whose
# window has closed and which has no `*-resolved.json` yet, and those write their
# result into the run directory. That is the same file a hand-run resolver writes,
# it is only ever computed once per day, and a run whose window is still open is
# never touched. Pass --no-feeders to skip all three.
if (( FEEDERS )); then
  python3 researcher_us/scripts/edge_search_volume.py >/dev/null 2>&1 \
    || echo "update: search volume failed, keeping the last one"
  python3 researcher_us/scripts/edge_calendar.py --days 7 >/dev/null 2>&1 \
    || echo "update: calendar failed, the Agenda tab may go stale"
  python3 dashboard/scripts/build_markets.py --resolve \
    || echo "update: markets feeder failed, the three market tabs keep the last one"
fi

# Stage E V2 -> the V2 tab. Reads the shadow ledger and every
# edge-scores-grounded.json on disk, no network, so it runs even with --no-feeders.
python3 dashboard/scripts/build_v2.py \
  || echo "update: V2 feeder failed, the V2 tab keeps the last one"

python3 dashboard/scripts/build_ledger.py "${LEDGER_ARGS[@]+"${LEDGER_ARGS[@]}"}"
python3 dashboard/scripts/build_dashboard.py

echo
if curl -fsS --max-time 1 "http://127.0.0.1:$PORT/ping" >/dev/null 2>&1; then
  echo "open: http://127.0.0.1:$PORT/dashboard.html  (server draait — de knop werkt)"
else
  echo "open: file://$REPO_ROOT/dashboard/dashboard.html"
  echo "      of: ./dashboard/update.sh --serve-bg   (dan werkt de knop)"
fi

if (( PUBLISH )); then
  scripts/publish.sh "performance: ledger and dashboard through $(date -u +%Y-%m-%d)"
fi

if (( SERVE == 1 )); then
  exec python3 dashboard/scripts/serve.py --port "$PORT" \
       "${LEDGER_ARGS[@]+"${LEDGER_ARGS[@]}"}"
fi

if (( SERVE == 2 )); then
  # Detached, so the shell comes back and the button keeps working afterwards. One
  # server is enough: if the port already answers, leave it alone.
  if curl -fsS --max-time 1 "http://127.0.0.1:$PORT/ping" >/dev/null 2>&1; then
    echo "update: er draait al een server op $PORT"
  else
    nohup python3 dashboard/scripts/serve.py --port "$PORT" \
      "${LEDGER_ARGS[@]+"${LEDGER_ARGS[@]}"}" >/tmp/edge-performance-serve.log 2>&1 &
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      curl -fsS --max-time 1 "http://127.0.0.1:$PORT/ping" >/dev/null 2>&1 && break
      sleep 0.3
    done
  fi
  echo "server: http://127.0.0.1:$PORT/dashboard.html  (log: /tmp/edge-performance-serve.log)"
  echo "de Ververs-knop werkt nu ook in het bestand dat je al open hebt."
fi

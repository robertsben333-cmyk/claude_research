#!/bin/bash
# SessionStart hook: make sure the packages the Routines import are present.
# The environment's setup script (scripts/env/setup.sh) normally installed them
# already, so this is a fast import check that only installs on a miss. It never
# fails the session: a missing package is reported, not fatal.
set -uo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0

if ! python3 -c "import yaml, requests, xlrd, openpyxl" 2>/dev/null; then
  echo "[session-start] installing requirements.txt"
  python3 -m pip install --quiet --disable-pip-version-check -r requirements.txt 2>/dev/null \
    || python3 -m pip install --quiet --disable-pip-version-check --break-system-packages -r requirements.txt \
    || echo "[session-start] WARNING: pip install failed; see requirements.txt"
fi
python3 scripts/env/check.py --quiet || true
exit 0

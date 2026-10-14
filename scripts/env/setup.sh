#!/bin/bash
# The cloud environment's SETUP SCRIPT for the earnings Routines.
#
# Paste this file's text into: Project settings -> Cloud environment -> gear ->
# Setup script, for the environment the Routines fire into ("full env",
# env_01HBKyy2ZpubuvsBDUY2onkn, on Xavier's account; stage E and Close AMC run on
# another account and need the same text in their own environment).
#
# It runs as root on Ubuntu before the session starts and the result is cached
# with the container, so it is self-contained: it does NOT read the repository,
# which may not be cloned yet. Keep the package list in step with requirements.txt
# (scripts/env/check.py fails the smoke test if they drift).
set -uo pipefail

PY_PKGS="PyYAML>=6.0 requests>=2.31 xlrd==2.0.2 openpyxl>=3.1"
APT_PKGS="poppler-utils jq curl git"

echo "[setup] python: $(python3 --version 2>&1)"
python3 -m pip install --quiet --disable-pip-version-check $PY_PKGS 2>/dev/null \
  || python3 -m pip install --quiet --disable-pip-version-check --break-system-packages $PY_PKGS \
  || echo "[setup] WARNING: pip install failed"

missing=""
for p in $APT_PKGS; do dpkg -s "$p" >/dev/null 2>&1 || missing="$missing $p"; done
if [ -n "$missing" ]; then
  echo "[setup] apt install:$missing"
  (apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq $missing) \
    || echo "[setup] WARNING: apt install failed for:$missing"
fi

python3 - <<'PY'
import importlib
for m in ("yaml", "requests", "xlrd", "openpyxl"):
    try:
        importlib.import_module(m); print(f"[setup] ok   {m}")
    except Exception as e:
        print(f"[setup] FAIL {m}: {e}")
PY
command -v pdftotext >/dev/null && echo "[setup] ok   pdftotext" || echo "[setup] FAIL pdftotext"
exit 0

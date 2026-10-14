#!/usr/bin/env python3
"""Check that this container has what the Routines need at run time.

    python3 scripts/env/check.py           # full report
    python3 scripts/env/check.py --quiet   # print only problems
    python3 scripts/env/check.py --strict  # exit 1 on any missing requirement

Reports packages, command-line tools and the NAMES of environment variables (never
their values). Also checks that scripts/env/setup.sh installs exactly the packages
requirements.txt lists, because the setup script is pasted into the environment by
hand and must not drift from the repo.
"""
import argparse
import importlib
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# import name -> requirement name
PACKAGES = {"yaml": "PyYAML", "requests": "requests", "xlrd": "xlrd", "openpyxl": "openpyxl"}
TOOLS = ("git", "curl", "jq", "pdftotext")
# name -> who needs it. Only stage E (on the other account) places orders.
ENV_VARS = {
    "ALPACA_API_KEY_ID": "stage E / Close AMC only (alpaca_trade.py)",
    "ALPACA_API_SECRET_KEY": "stage E / Close AMC only (alpaca_trade.py)",
    "FMP_API_KEY": "optional fallback in scripts/get_earnings.py",
    "FINNHUB_API_KEY": "optional fallback in scripts/get_earnings.py",
}


def _names(spec_line):
    m = re.match(r"\s*([A-Za-z0-9_.\-]+)", spec_line)
    return m.group(1).lower() if m else None


def drift():
    """Package names in requirements.txt that setup.sh does not install, and vice versa."""
    req = {_names(l) for l in (REPO / "requirements.txt").read_text().splitlines()
           if l.strip() and not l.lstrip().startswith("#")}
    m = re.search(r'^PY_PKGS="([^"]*)"', (REPO / "scripts/env/setup.sh").read_text(), re.M)
    setup = {_names(s) for s in (m.group(1).split() if m else [])}
    req.discard(None), setup.discard(None)
    return sorted(req - setup), sorted(setup - req)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    problems, lines = [], []

    for mod, req in PACKAGES.items():
        try:
            m = importlib.import_module(mod)
            lines.append(f"ok    python  {req} {getattr(m, '__version__', '')}")
        except Exception as e:
            problems.append(f"MISSING python  {req} ({type(e).__name__}: {e})")
    for t in TOOLS:
        (lines if shutil.which(t) else problems).append(
            f"{'ok   ' if shutil.which(t) else 'MISSING'} tool    {t}")
    only_req, only_setup = drift()
    if only_req or only_setup:
        problems.append(f"DRIFT requirements.txt vs setup.sh: only in requirements {only_req}, "
                        f"only in setup.sh {only_setup}")
    for k, why in ENV_VARS.items():
        lines.append(f"{'set  ' if os.environ.get(k) else 'unset'} env     {k}  ({why})")

    if not a.quiet:
        print("\n".join(lines))
    if problems:
        print("[env check] " + "\n[env check] ".join(problems), file=sys.stderr)
    elif not a.quiet:
        print("env check: all requirements present")
    return 1 if (a.strict and problems) else 0


if __name__ == "__main__":
    sys.exit(main())

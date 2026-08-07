#!/usr/bin/env python3
"""
Resolve the canonical paths for one research day and create the folders.

Every stage starts by running this so all five stages agree on where files go,
even when a stage fires just after midnight or on a session that lost context.

    python3 scripts/run_paths.py            # today
    python3 scripts/run_paths.py 2026-08-10
    python3 scripts/run_paths.py --json     # machine-readable
"""

import argparse
import json
import os
import sys
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def paths_for(d):
    base = os.path.join(REPO_ROOT, "research", f"{d:%Y}", f"{d:%m}", d.isoformat())
    return {
        "run_date": d.isoformat(),
        "run_dir": base,
        "universe_json": os.path.join(base, "00-universe.json"),
        "universe_md": os.path.join(base, "00-universe.md"),
        "shortlist_json": os.path.join(base, "01-shortlist.json"),
        "shortlist_md": os.path.join(base, "01-shortlist.md"),
        "dossier_dir": os.path.join(base, "02-dossiers"),
        "panel_dir": os.path.join(base, "03-panel"),
        "advice_md": os.path.join(base, "04-advice.md"),
        "advice_json": os.path.join(base, "04-advice.json"),
        "outcome_md": os.path.join(base, "05-outcome.md"),
        "run_log": os.path.join(base, "_run-log.md"),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("run_date", nargs="?", help="YYYY-MM-DD (default: today)")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of KEY=value")
    p.add_argument("--no-create", action="store_true", help="Do not create directories")
    args = p.parse_args()

    if args.run_date:
        try:
            d = date.fromisoformat(args.run_date)
        except ValueError:
            sys.exit(f"Invalid date '{args.run_date}'. Use YYYY-MM-DD.")
    else:
        d = date.today()

    pp = paths_for(d)

    if not args.no_create:
        for key in ("run_dir", "dossier_dir", "panel_dir"):
            os.makedirs(pp[key], exist_ok=True)

    if args.json:
        print(json.dumps(pp, indent=2))
    else:
        for k, v in pp.items():
            print(f"{k.upper()}={v}")


if __name__ == "__main__":
    main()

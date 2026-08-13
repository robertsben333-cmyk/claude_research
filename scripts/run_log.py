#!/usr/bin/env python3
"""
Append one section to a run day's `_run-log.md`.

The run log is how a later stage — and you, tomorrow — find out that something
upstream went wrong. It is strictly append-only: this script never rewrites a
line another stage wrote, and it creates the file with its date header if it
does not exist yet.

It exists mainly so a stage can leave a *heartbeat* before it starts spending
money:

    python3 scripts/run_log.py --heading "Stage 2 — deep dive, batch 1 — STARTED" \
        --line "Tickers: AAA, BBB, CCC" \
        --line "Plan: 2 waves of 2 opus/high researchers, publish after each"

A session that is killed mid-flight (usage limit, container reclaim) publishes
nothing otherwise, and the day's archive cannot distinguish "the Routine never
fired" from "it fired and died on the first researcher". Those two have
completely different fixes, so the distinction is worth one cheap commit.

    python3 scripts/run_log.py --heading "..." --line "..." [--date YYYY-MM-DD]

Exits 0 on success. Prints the path it wrote.
"""

import argparse
import os
import sys
from datetime import date, datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_paths import paths_for  # noqa: E402


def append_section(run_log, run_date, heading, lines, timestamp=True):
    """Append a `## heading` section. Creates the file (with header) if needed."""
    os.makedirs(os.path.dirname(run_log), exist_ok=True)

    existing = ""
    if os.path.exists(run_log):
        with open(run_log, encoding="utf-8") as fh:
            existing = fh.read()

    parts = []
    if not existing.strip():
        parts.append(f"# Run log — {run_date}\n")
    elif not existing.endswith("\n"):
        parts.append("\n")

    parts.append(f"\n## {heading}\n")
    if timestamp:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        parts.append(f"- Logged at {now}\n")
    for line in lines:
        parts.append(f"- {line}\n")

    with open(run_log, "a", encoding="utf-8") as fh:
        fh.write("".join(parts))

    return run_log


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--heading", required=True, help="Section heading, without the '##'")
    p.add_argument("--line", action="append", default=[], help="A bullet; repeatable")
    p.add_argument("--date", help="YYYY-MM-DD (default: today)")
    p.add_argument("--no-timestamp", action="store_true",
                   help="Omit the 'Logged at' bullet")
    args = p.parse_args()

    if args.date:
        try:
            d = date.fromisoformat(args.date)
        except ValueError:
            sys.exit(f"Invalid date '{args.date}'. Use YYYY-MM-DD.")
    else:
        d = date.today()

    pp = paths_for(d)
    written = append_section(
        pp["run_log"], d.isoformat(), args.heading, args.line,
        timestamp=not args.no_timestamp,
    )
    print(written)


if __name__ == "__main__":
    main()

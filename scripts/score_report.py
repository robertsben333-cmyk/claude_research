#!/usr/bin/env python3
"""The table every hunt stage pastes, verbatim, into its closing chat reply.

Since 2026-10-01 every hunter answers twice, and the reply carries both answers side
by side so nobody has to open a file to see them:

  impact_sum     version 2, THE KEY. Each finding sized on its own, added up. This is
                 what ranks the day, what the 3.0 conviction floor was measured on and,
                 for stage E only, what trades. From edge-scores.json.
  impact_scaled  version 3. (2 * p_up / 100 - 1) * abs_move_pct, the hunter's second,
                 separate measurement of the whole print. From edge-scores-scaled.json,
                 its own file. Not ranked on, not traded, never pooled with the key.
  V2             US only (stages E, E-S and E-P): the grounded score from
                 edge-scores-grounded.json, at its primary horizon. Shown as
                 "not run" when the file is absent, never left out silently.

    python3 scripts/score_report.py --run research/2026/10/2026-10-02/edge
    python3 scripts/score_report.py --run <RUN>/europe --label "Stage EU"

Reads only; writes nothing. Exits 1 when the run has no edge-scores.json, so a
reply cannot quote a table that was never scored.
"""
import argparse
import json
import sys
from pathlib import Path

US_DIRS = {"edge", "edge-sonnet", "edge-panel"}


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def f(v, fmt="{:+.2f}"):
    return "n/a" if v is None else fmt.format(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="the directory holding edge-scores.json")
    ap.add_argument("--label", help="stage name for the heading, e.g. 'Stage E'")
    ap.add_argument("--us", action="store_true",
                    help="show the V2 column (automatic for edge/ and edge-sonnet/)")
    a = ap.parse_args()

    run = Path(a.run)
    key = load(run / "edge-scores.json")
    if not key:
        print(f"no edge-scores.json in {run}: nothing has been scored", file=sys.stderr)
        sys.exit(1)
    scaled = load(run / "edge-scores-scaled.json")
    sc = {r["ticker"]: r for r in (scaled or {}).get("ranking", [])}
    us = a.us or run.name in US_DIRS
    grounded = load(run / "edge-scores-grounded.json") if us else None
    gr = {r["ticker"]: r for r in (grounded or {}).get("ranking", [])}
    floor = key.get("conviction_floor", 3.0)

    label = a.label or run.name
    print(f"**{label}, {run.parent.name}**: ranked on `{key.get('ranking_key')}` "
          f"(version 2, each finding sized on its own); conviction floor {floor:.1f} "
          f"applies to it only.")
    if not scaled:
        print("`edge-scores-scaled.json` is missing: impact_scaled not computed "
              "(re-run edge_score.py).")
    if us:
        if grounded is None:
            v2_state = "V2 not run: no edge-scores-grounded.json in this run."
        elif grounded.get("status") != "calibrated":
            v2_state = f"V2 {grounded.get('status')}: no grounded values."
        else:
            v2_state = (f"V2 at `{grounded.get('primary_horizon')}`, matrix as of "
                        f"{grounded.get('matrix_as_of')}.")
        print(v2_state)
    print()

    head = ["#", "ticker", "impact_sum (key)", "floor", "impact_scaled (v3)",
            "abs_move", "p_up"]
    if us:
        head.append("V2 grounded")
    print("| " + " | ".join(head) + " |")
    print("|" + "|".join(" --- " for _ in head) + "|")
    dropped = []
    for r in key.get("ranking", []):
        if not r.get("rankable"):
            dropped.append(r)
            continue
        s = sc.get(r["ticker"], {})
        cells = [str(r.get("rank")), r["ticker"], f"**{f(r['impact_sum'])}**",
                 "yes" if r.get("conviction", 0) >= floor else "no",
                 f(s.get("impact_scaled")), f(s.get("abs_move_pct"), "{:.1f}"),
                 f(s.get("p_up"), "{:.0f}")]
        if us:
            g = gr.get(r["ticker"], {})
            if grounded is None or grounded.get("status") != "calibrated":
                cells.append("not run")
            elif g.get("impact_sum_grounded") is None:
                cells.append("n/a" + (f" ({g['not_grounded_because']})"
                                      if g.get("not_grounded_because") else ""))
            else:
                cells.append(f(g["impact_sum_grounded"]))
        print("| " + " | ".join(cells) + " |")
    if not key.get("ranking"):
        print("| | no names | | | | | |" + (" |" if us else ""))
    for r in dropped:
        print(f"\nNot ranked: {r['ticker']}: {r.get('not_rankable_because')}")
    print("\n`impact_scaled` is the hunter's second, separate measurement, "
          "(2·p_up/100 − 1)·abs_move. It is not the key and is never pooled with it.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Synthetic hunts and synthetic judges for a stage IPO VALIDATION run. No model calls.

    python3 researcher_ipo/scripts/ipo_synth.py hunts  --run <RUN> [--seed 7]
    python3 researcher_ipo/scripts/ipo_synth.py judges --run <RUN> [--seed 7]

`hunts` writes one hunt per sealed baseline in the hunter's output contract, with random
findings sized on the baseline's own scale; `judges` writes four panel files from the
packs, random again. Both exist to drive the scorer, the panel and the resolver end to
end on a past date. Random findings should rank at noise against the realised move, and
that null is what a real run has to beat. Refuses a run not marked validation_only.
"""
import argparse
import json
import random
import sys
from pathlib import Path

LANDS = ["book_demand", "float_supply", "stabilisation", "valuation", "holder_supply",
         "early_release", "positioning", "the_document"]


def guard(run):
    u = json.loads((Path(run) / "universe.json").read_text())
    if not u.get("validation_only"):
        sys.exit("refusing: universe.json is not validation_only")
    return u


def hunts(run, seed):
    rnd = random.Random(seed)
    out = Path(run) / "hunts"
    out.mkdir(exist_ok=True)
    for b in sorted((Path(run) / "baselines").glob("*.json")):
        base = json.loads(b.read_text())
        scale = ((base.get("recent_debuts") or {}).get("key_move_pct") or {}).get("median_abs") \
            or (base.get("tape") or {}).get("open_close_sd_20d_pct") or 3.0
        fs = []
        for i in range(rnd.randint(0, 4)):
            x = round(rnd.gauss(0, scale / 3), 2)
            fs.append({"finding": f"SYNTHETIC finding {i} for validation", "expected_impact_pct": x,
                       "impact_low_pct": round(x - 1, 2), "impact_high_pct": round(x + 1, 2),
                       "lands_on": rnd.choice(LANDS), "resolves_by": base["event_date"],
                       "reaction_history_on_this_line": "synthetic", "source": "https://example.invalid/synthetic",
                       "source_date": base["event_date"], "why_not_priced": "synthetic", "independence": "none"})
        s = round(sum(f["expected_impact_pct"] for f in fs), 3)
        p_up = 50 if not fs else max(5, min(95, 50 + round(rnd.gauss(0, 12))))
        h = {"ticker": base["ticker"], "event_type": base["event_type"], "event_date": base["event_date"],
             "window": base["window"], "event_confirmed": True, "event_check": "synthetic",
             "lockup_status": "full expiry today" if base["event_type"] == "lockup" else None,
             "abs_move_pct": round(scale, 2), "p_up": p_up,
             "expected_move_pct": round((2 * p_up / 100 - 1) * scale, 3),
             "conviction_note": "synthetic", "print_vs_bar_pct": None, "bar": "synthetic",
             "positioning_check": "synthetic", "findings": fs, "outside_window": [],
             "searched_and_found_nothing": ["synthetic"], "rejected_candidates": [],
             "baseline_tension": "synthetic",
             "pre_lessons": {"impact_sum_pct": s, "expected_move_pct": 0.0, "findings_count": len(fs),
                             "sizes_pct": [f["expected_impact_pct"] for f in fs]},
             "lessons_applied": ["nothing changed"], "sources_used": 0, "synthetic": True}
        (out / f"{base['ticker']}.json").write_text(json.dumps(h, indent=1) + "\n")
        print(f"{base['ticker']}: {len(fs)} synthetic findings, impact_sum {s:+.2f}")


def judges(run, seed):
    rnd = random.Random(seed + 1)
    packs = json.loads((Path(run) / "panel" / "packs.json").read_text())
    for m in ("opus5", "opus55", "sonnet55", "fable51"):
        rows = []
        for p in packs:
            x = round(rnd.gauss(0, 2.5), 2)
            rows.append({"id": p["id"], "abs_move_pct": 4.0, "p_up": 50, "impact_sum": x,
                         "findings": [], "note": "synthetic judge for validation"})
        (Path(run) / "panel" / f"{m}.json").write_text(json.dumps(rows, indent=1) + "\n")
    print(f"4 synthetic members x {len(packs)} packs")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["hunts", "judges"])
    ap.add_argument("--run", required=True)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    guard(a.run)
    (hunts if a.cmd == "hunts" else judges)(a.run, a.seed)


if __name__ == "__main__":
    main()

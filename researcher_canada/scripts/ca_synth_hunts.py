#!/usr/bin/env python3
"""Synthetic hunts, for validating the chain and for nothing else.

Every stage in this repo was validated this way before a real hunter was spawned: stage
J against 2026-09-11 and stage EU against 2026-09-16, both with random findings, both
ranking at what random findings should rank at. It exercises universe -> baselines ->
edge_score -> resolve without a model call, so a broken contract shows up as a crash
rather than as a plausible-looking ranking.

EVERY FILE IT WRITES IS STAMPED `synthetic: true`. A run built with it can never be a
result about anything, and `ca_resolve.py` will happily rank it -- that is the point:
the number it produces is the null this stage's real numbers have to beat.
"""
import argparse
import json
import random
from datetime import date
from pathlib import Path

LANDS = ["reported_quarter", "guidance", "one_off", "financing", "capital_return",
         "positioning", "other"]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--seed", type=int, default=20260922)
    a = ap.parse_args()
    run = Path(a.run)
    hunts = run / "hunts"
    hunts.mkdir(parents=True, exist_ok=True)
    rng = random.Random(a.seed)
    n = 0
    for b in sorted((run / "baselines").glob("*.json")):
        doc = json.loads(b.read_text())
        t = doc["ticker"]
        k = rng.randint(0, 4)
        findings = []
        for i in range(k):
            findings.append({
                "finding": f"SYNTHETIC finding {i + 1} for {t}",
                "expected_impact_pct": round(rng.gauss(0, 3), 2),
                "lands_on": rng.choice(LANDS),
                "resolves_by": doc["event_date"],
                "source": "synthetic://no-source",
                "why_not_priced": "synthetic", "independence": "none",
            })
        total = round(sum(f["expected_impact_pct"] for f in findings), 2)
        (hunts / f"{t}-h1.json").write_text(json.dumps({
            "synthetic": True,
            "ticker": t,
            "expected_move_pct": total,
            "conviction_note": "SYNTHETIC. Random findings; this is the null, not a read.",
            "print_vs_bar_pct": round(rng.gauss(0, 2), 2),
            "bar": "unsourced (synthetic)",
            "positioning_check": "synthetic",
            "findings": findings,
            "outside_window": [],
            "searched_and_found_nothing": ["synthetic"],
            "baseline_tension": "synthetic",
            # No `pre_local`: the hunter runs ONE bilingual pass since 2026-09-22
            # and emits no freeze. `language_note` replaced it and is prose.
            "language_note": ["synthetic"],
            "pre_lessons": {"impact_sum_pct": total, "expected_move_pct": total,
                            "print_vs_bar_pct": 0.0, "findings_count": len(findings),
                            "sizes_pct": [f["expected_impact_pct"] for f in findings]},
            "lessons_applied": ["nothing changed (synthetic)"],
            "sources_used": 0,
        }, indent=2) + "\n")
        n += 1
    print(f"{n} synthetic hunts -> {hunts}")


if __name__ == "__main__":
    main()

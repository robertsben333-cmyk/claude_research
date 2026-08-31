#!/usr/bin/env python3
"""Build one adversary brief per ticker from the hunt files.

The adversary must judge how much of each finding is already in the price WITHOUT
seeing what the hunter thought it was worth. `edge_score.py` averages the
adversary's independent `size_check_pct` with the hunter's `expected_impact_pct`
precisely so the two are struck separately -- feed the hunter's number across and
that averaging becomes an echo.

So this strips, per finding:

    expected_impact_pct   the hunter's size
    impact_low_pct/high   its band
    why_not_priced        the hunter's argument that it ISN'T priced, which is the
                          exact question the adversary is being asked
    independence          the hunter's own cluster judgement

and keeps only what is checkable: the claim, the source, the date.

It also emits `finding_key` in the form `<hunt file stem>#<index>`, which is the
join key `edge_score.py` uses to match a verdict back to a finding. Hand-copying
those keys is how a whole ticker's verdicts get silently dropped -- an unmatched
key is skipped, and an unjudged finding then defaults to mostly-priced, so a typo
quietly costs edge rather than raising an error.

    python3 scripts/edge_adversary_brief.py --run <RUN>/edge
    python3 scripts/edge_adversary_brief.py --run <RUN>/edge --ticker MMED
"""
import argparse
import json
from pathlib import Path

STRIP = {"expected_impact_pct", "impact_low_pct", "impact_high_pct",
         "why_not_priced", "independence"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--ticker")
    a = ap.parse_args()

    run = Path(a.run)
    by_ticker = {}
    for f in sorted((run / "hunts").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        t = (d.get("ticker") or f.stem.split("-")[0]).upper()
        for i, item in enumerate(d.get("findings") or []):
            by_ticker.setdefault(t, []).append({
                "finding_key": f"{f.stem}#{i}",
                "claim": item.get("finding"),
                "source": item.get("source"),
                "source_date": item.get("source_date"),
            })

    tickers = [a.ticker.upper()] if a.ticker else sorted(by_ticker)
    for t in tickers:
        items = by_ticker.get(t) or []
        n_hunters = len({k["finding_key"].split("#")[0] for k in items})
        print(f"\n{'='*70}\n{t}: {len(items)} findings from {n_hunters} hunter(s)\n{'='*70}")
        print(json.dumps(items, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Lay out one edge-hunt run per event day over the sealed capture corpus.

Reads every `seal.json` with status ok, groups by the **sealed** event date (the
8-K acceptance date, not the calendar date the capture was filed under), dedupes,
and writes a run directory per day with a manifest and a priced-in baseline for
each name.

Baselines are built with the as-of guard, so no option chain is fetched for any
of these dates and `expected_move_pct` falls back to the name's own median
reaction. That is the anchor the whole backtest runs on.

    python3 backtest/scripts/edge_corpus_setup.py --manifest-only
    python3 backtest/scripts/edge_corpus_setup.py --day 2026-09-01
    python3 backtest/scripts/edge_corpus_setup.py
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "edge" / "scripts"))
from priced_in import build  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / "captures" / "events"
RUNS = ROOT / "runs" / "edge-corpus"


def richness(evdir):
    """How much a capture actually holds, for choosing between two of the same event."""
    items = 0
    for s in (evdir / "snapshots").glob("*.json"):
        try:
            items += json.loads(s.read_text(encoding="utf-8")).get("n_items", 0) or 0
        except Exception:
            pass
    docs = len(list((evdir / "docs").glob("*.txt"))) if (evdir / "docs").exists() else 0
    return (docs, items)


def manifest():
    """One entry per (ticker, sealed event date), richest capture winning."""
    best = {}
    for sp in sorted(CAPTURES.glob("*/seal.json")):
        s = json.loads(sp.read_text(encoding="utf-8"))
        if s.get("status") != "ok" or not s.get("session"):
            continue
        evdir = sp.parent
        key = (s["ticker"], s["event_date"])
        r = richness(evdir)
        if key not in best or r > best[key][0]:
            ev = json.loads((evdir / "event.json").read_text(encoding="utf-8"))
            best[key] = (r, {
                "ticker": s["ticker"],
                "company": ev.get("company"),
                "event_date": s["event_date"],
                "session": s["session"],
                "calendar_date": s["calendar_date"],
                "capture": str(evdir.relative_to(ROOT.parent)),
                "market_cap_usd": ev.get("market_cap_usd_today"),
                "docs": r[0],
                "items": r[1],
                "seal_basis": s.get("basis"),
            })
    byday = defaultdict(list)
    for (_, d), (_, row) in sorted(best.items()):
        byday[d].append(row)
    for d in byday:
        byday[d].sort(key=lambda r: r["ticker"])
    return byday


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--day", help="only this event date")
    ap.add_argument("--manifest-only", action="store_true")
    a = ap.parse_args()

    byday = manifest()
    if a.day:
        byday = {a.day: byday.get(a.day, [])}

    total = 0
    for day, rows in sorted(byday.items()):
        run = RUNS / day
        (run / "baselines").mkdir(parents=True, exist_ok=True)
        (run / "hunts").mkdir(exist_ok=True)
        (run / "adversary").mkdir(exist_ok=True)
        (run / "manifest.json").write_text(
            json.dumps({"event_date": day, "names": len(rows), "events": rows},
                       indent=1) + "\n", encoding="utf-8")
        total += len(rows)
        print(f"{day}: {len(rows)} names -> {run}")
        if a.manifest_only:
            continue
        for r in rows:
            out = run / "baselines" / f"{r['ticker']}.json"
            if out.exists():
                continue
            doc = build(r["ticker"], r["event_date"], r["session"])
            doc["capture"] = r["capture"]
            doc["company"] = r["company"]
            out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
            o = doc.get("options") or {}
            print(f"   {r['ticker']:7s} {str(doc.get('status'))[:20]:20s} "
                  f"spot={(doc.get('tape') or {}).get('spot')} "
                  f"hist_n={(doc.get('history') or {}).get('n')} "
                  f"exp_move={doc.get('expected_move_pct')} "
                  f"opts={o.get('status')}")
    print(f"\n{len(byday)} days, {total} names")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Resolve an edge hunt against what the stock actually did, and plot the curve.

The headline number is not the hit rate. It is the **risk-coverage curve**: how
accuracy moves as the confidence threshold rises and fewer names get called. The
claim this whole design rests on -- "predict direction where the system knows it
has found something, abstain elsewhere" -- is true exactly when that curve slopes
up, and decorative when it is flat. `LEDGER.md` has been asking the same question
of its certainty tiers since it was created and has never had the sample to answer
it.

Because `edge_confidence.py` scores every name and not only the called ones, the
curve can be recomputed at any threshold after the outcome is known without that
being cherry-picking. Nothing was withheld to produce it.

Direction is scored against a per-name deadband. A realised move inside the band
had no direction in it and is recorded `no-direction`, neither hit nor miss. BILL
on 2026-08-19 is the case that motivates this: a clean beat, a -0.65% close, and
the ledger recorded a directional miss on what was statistically a flat day.

    python3 scripts/edge_resolve.py --run research/2026/08/2026-08-31/edge
"""
import argparse
import json
import random
import statistics
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
YQ = "https://query1.finance.yahoo.com"


def bars(ticker, days=90):
    u = f"{YQ}/v8/finance/chart/{ticker}?range={days}d&interval=1d"
    j = json.loads(urllib.request.urlopen(
        urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read())
    res = j["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    return [{"date": datetime.fromtimestamp(ts, timezone.utc).date().isoformat(),
             "close": q["close"][i]}
            for i, ts in enumerate(res["timestamp"]) if q["close"][i] is not None]


def realised(ticker, event_date, session):
    """Close before the print to close after the first full session following it."""
    rows = bars(ticker)
    dates = [r["date"] for r in rows]
    idx = {r["date"]: r["close"] for r in rows}
    if session == "amc":
        before = [d for d in dates if d <= event_date]
        after = [d for d in dates if d > event_date]
    else:
        before = [d for d in dates if d < event_date]
        after = [d for d in dates if d >= event_date]
    if not before or not after:
        return None, "outcome window has not closed yet"
    b, a = idx[before[-1]], idx[after[0]]
    return {"before_date": before[-1], "before_close": round(b, 4),
            "after_date": after[0], "after_close": round(a, 4),
            "move_pct": round((a / b - 1) * 100, 2)}, None


def curve(rows, thresholds):
    """Accuracy as a function of the confidence threshold. The whole point."""
    out = []
    for t in thresholds:
        sel = [r for r in rows
               if r["direction"] in ("up", "down") and r["confidence"] >= t
               and r["outcome"] == "scored"]
        hits = sum(1 for r in sel if r["hit"])
        out.append({
            "threshold": t,
            "names_called": len(sel),
            "coverage_pct": round(100 * len(sel) / len(rows), 1) if rows else 0.0,
            "hits": hits,
            "accuracy_pct": round(100 * hits / len(sel), 1) if sel else None,
        })
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--seed", type=int, default=20260831)
    a = ap.parse_args()

    run = Path(a.run)
    calls_doc = json.loads((run / "edge-calls.json").read_text(encoding="utf-8"))
    baselines = {}
    for f in sorted((run / "baselines").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        baselines[d["ticker"]] = d

    rows, pending = [], 0
    for c in calls_doc["calls"]:
        t = c["ticker"]
        b = baselines.get(t, {})
        ed, sess = b.get("event_date"), b.get("session", "bmo")
        band = c["priced_in"].get("deadband_pct") or 2.0
        r = {"ticker": t, "direction": c["direction"], "confidence": c["confidence"],
             "called": c["called"], "deadband_pct": band}
        if not ed:
            r.update({"outcome": "no_baseline", "hit": None})
            rows.append(r)
            continue
        res, err = realised(t, ed, sess)
        if err:
            r.update({"outcome": "pending", "note": err, "hit": None})
            pending += 1
            rows.append(r)
            continue
        mv = res["move_pct"]
        r.update(res)
        if abs(mv) < band:
            r.update({"outcome": "no-direction", "hit": None,
                      "note": f"|{mv}%| inside the {band}% deadband"})
        elif r["direction"] == "abstain":
            r.update({"outcome": "abstained", "hit": None,
                      "note": f"moved {mv}% with no call made"})
        else:
            hit = (mv > 0) == (r["direction"] == "up")
            r.update({"outcome": "scored", "hit": hit})
        rows.append(r)

    scored = [r for r in rows if r["outcome"] == "scored"]
    called = [r for r in scored if r["called"]]
    missed_moves = [r for r in rows
                    if r["outcome"] == "abstained" and abs(r.get("move_pct", 0)) >= r["deadband_pct"]]

    # Baselines. A hit rate without the number a coin would have scored on the
    # same events cannot be read at all.
    rnd = random.Random(a.seed)
    coin = [sum(1 for r in scored if rnd.random() < 0.5) for _ in range(20000)] if scored else []
    coin_pct = [round(100 * c / len(scored), 1) for c in coin] if scored else []

    doc = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run": str(run),
        "names": len(rows),
        "pending": pending,
        "scored": len(scored),
        "no_direction": sum(1 for r in rows if r["outcome"] == "no-direction"),
        "abstained": sum(1 for r in rows if r["outcome"] == "abstained"),
        "called_and_scored": len(called),
        "accuracy_called_pct": round(100 * sum(1 for r in called if r["hit"]) / len(called), 1) if called else None,
        "accuracy_all_directional_pct": round(100 * sum(1 for r in scored if r["hit"]) / len(scored), 1) if scored else None,
        "baselines": {
            "coin_mean_pct": round(statistics.fmean(coin_pct), 1) if coin_pct else None,
            "coin_5_95_pct": [round(statistics.quantiles(coin_pct, n=20)[0], 1),
                              round(statistics.quantiles(coin_pct, n=20)[18], 1)] if len(coin_pct) > 20 else None,
            "always_up_pct": round(100 * sum(1 for r in scored if r["move_pct"] > 0) / len(scored), 1) if scored else None,
            "n": len(scored),
        },
        "risk_coverage_curve": curve(rows, [0, 20, 30, 40, 50, 55, 60, 70, 80]),
        "abstentions_that_moved": [
            {"ticker": r["ticker"], "move_pct": r["move_pct"], "confidence": r["confidence"]}
            for r in missed_moves],
        "results": rows,
    }
    out = run / "edge-outcome.json"
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    print(f"{doc['scored']} scored, {doc['no_direction']} inside deadband, "
          f"{doc['abstained']} abstained, {doc['pending']} pending\n")
    print(f"{'ticker':8s}{'dir':9s}{'conf':>6s}{'move':>9s}  outcome")
    for r in sorted(rows, key=lambda x: -x["confidence"]):
        mv = f"{r.get('move_pct'):+.2f}%" if r.get("move_pct") is not None else "  --  "
        mark = "" if r["hit"] is None else ("  HIT" if r["hit"] else "  MISS")
        print(f"{r['ticker']:8s}{r['direction']:9s}{r['confidence']:6.1f}{mv:>9s}  {r['outcome']}{mark}")
    if doc["baselines"]["n"]:
        print(f"\ncoin on the same {doc['baselines']['n']} events: "
              f"{doc['baselines']['coin_mean_pct']}% "
              f"(5-95: {doc['baselines']['coin_5_95_pct']})   "
              f"always-up: {doc['baselines']['always_up_pct']}%")
    print("\nrisk-coverage curve (the number that matters):")
    print(f"  {'thresh':>7s}{'called':>8s}{'cover':>8s}{'acc':>8s}")
    for p in doc["risk_coverage_curve"]:
        acc = f"{p['accuracy_pct']}%" if p["accuracy_pct"] is not None else "  --"
        print(f"  {p['threshold']:7.0f}{p['names_called']:8d}{p['coverage_pct']:7.1f}%{acc:>8s}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

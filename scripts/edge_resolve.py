#!/usr/bin/env python3
"""Resolve a ranking against what the stocks actually did.

The question this answers is not "was the call right". It is **can these companies
be ranked** — does sorting a day's names by `edge_score` put the ones that went up
above the ones that went down.

That is measured by rank correlation, which needs no threshold, no call and no
abstention, and which every name in the day contributes to. The old version of
this script plotted accuracy against a confidence threshold, which required the
scorer to emit a binary call; on 2026-08-31 it emitted none and the curve was
empty at every point.

Two correlations are reported and they answer different questions:

  vs raw move          did the ranking sort the day's actual returns
  vs move / implied    did it sort them after dividing out how much each name was
                       ever going to move. This is the skill measure: getting a
                       15%-implied biotech above a 2%-implied utility is easy and
                       says nothing

A single day of n names is far too small for either number to mean anything. They
are recorded per day and pooled across days; the pooled figure is the result and
one day is an anecdote.

    python3 scripts/edge_resolve.py --run research/2026/09/2026-09-01/edge
    python3 scripts/edge_resolve.py --pool research/2026/09/*/edge
"""
import argparse
import glob
import json
import math
import random
import statistics
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
YQ = "https://query1.finance.yahoo.com"


def bars(ticker, days=120):
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


def _ranks(xs):
    """Average ranks, so ties do not fabricate an ordering."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    rx, ry = _ranks(xs), _ranks(ys)
    mx, my = statistics.fmean(rx), statistics.fmean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return round(num / (dx * dy), 3) if dx and dy else None


def permutation_p(xs, ys, seed, trials=20000):
    """How often a random shuffle beats this correlation. n is small; say so."""
    obs = spearman(xs, ys)
    if obs is None:
        return None, None
    rnd = random.Random(seed)
    ys2 = list(ys)
    hits = 0
    for _ in range(trials):
        rnd.shuffle(ys2)
        s = spearman(xs, ys2)
        if s is not None and abs(s) >= abs(obs):
            hits += 1
    return obs, round(hits / trials, 4)


def resolve_run(run, seed):
    run = Path(run)
    scores = json.loads((run / "edge-scores.json").read_text(encoding="utf-8"))
    baselines = {}
    for f in sorted((run / "baselines").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        baselines[d["ticker"]] = d

    rows, pending = [], 0
    for r in scores["ranking"]:
        t = r["ticker"]
        b = baselines.get(t, {})
        row = {"ticker": t, "rank": r.get("rank"), "rankable": r["rankable"],
               "edge_score": r["edge_score"], "edge_pct": r["edge_pct"],
               "confidence": r["confidence"],
               "deadband_pct": b.get("deadband_pct"),
               "implied_pct": ((b.get("options") or {}).get("event_implied_move_pct")
                               or b.get("expected_move_pct"))}
        if not r["rankable"] or not b.get("event_date"):
            row["outcome"] = "not_ranked"
            rows.append(row)
            continue
        res, err = realised(t, b["event_date"], b.get("session", "bmo"))
        if err:
            row.update({"outcome": "pending", "note": err})
            pending += 1
            rows.append(row)
            continue
        row.update(res)
        row["outcome"] = "resolved"
        if row["implied_pct"]:
            row["move_over_implied"] = round(res["move_pct"] / row["implied_pct"], 3)
        rows.append(row)

    live = [r for r in rows if r["outcome"] == "resolved"]
    return {"run": str(run), "event_date": scores.get("ranking", [{}])[0] and
            baselines.get(live[0]["ticker"], {}).get("event_date") if live else None,
            "rows": rows, "live": live, "pending": pending}


def stats_for(live, seed):
    if len(live) < 3:
        return {"n": len(live),
                "note": "fewer than 3 resolved names; rank correlation not computed"}
    e = [r["edge_score"] for r in live]
    mv = [r["move_pct"] for r in live]
    out = {"n": len(live)}
    s, p = permutation_p(e, mv, seed)
    out["spearman_vs_raw_move"] = s
    out["p_permutation_raw"] = p
    norm = [r for r in live if r.get("move_over_implied") is not None]
    if len(norm) >= 3:
        s2, p2 = permutation_p([r["edge_score"] for r in norm],
                               [r["move_over_implied"] for r in norm], seed)
        out["spearman_vs_move_over_implied"] = s2
        out["p_permutation_normalised"] = p2
        out["n_normalised"] = len(norm)
    # Long the top third, short the bottom third. The ranking's payoff if you
    # traded it, which is the only version of "does the order matter" that pays.
    k = max(1, len(live) // 3)
    srt = sorted(live, key=lambda r: -r["edge_score"])
    top = statistics.fmean(r["move_pct"] for r in srt[:k])
    bot = statistics.fmean(r["move_pct"] for r in srt[-k:])
    out["top_third_mean_move_pct"] = round(top, 2)
    out["bottom_third_mean_move_pct"] = round(bot, 2)
    out["long_short_spread_pct"] = round(top - bot, 2)
    out["k_per_side"] = k
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run")
    ap.add_argument("--pool", nargs="*", help="several edge/ dirs, pooled")
    ap.add_argument("--seed", type=int, default=20260901)
    a = ap.parse_args()

    runs = []
    if a.run:
        runs.append(a.run)
    for pat in (a.pool or []):
        runs.extend(sorted(glob.glob(pat)))
    if not runs:
        raise SystemExit("give --run or --pool")

    all_live, per_day = [], []
    for rp in runs:
        r = resolve_run(rp, a.seed)
        st = stats_for(r["live"], a.seed)
        per_day.append({"run": r["run"], **st})
        all_live.extend(r["live"])

        print(f"\n=== {r['run']} ===")
        print(f"{'#':>2} {'ticker':8s}{'edge':>7s}{'conf':>6s}{'move':>9s}"
              f"{'m/impl':>8s}  outcome")
        for row in r["rows"]:
            mv = f"{row.get('move_pct'):+.2f}%" if row.get("move_pct") is not None else "   --"
            mi = f"{row.get('move_over_implied'):+.2f}" if row.get("move_over_implied") is not None else "   --"
            rk = f"{row['rank']:>2}" if row.get("rank") else "--"
            print(f"{rk} {row['ticker']:8s}{row['edge_score']:>7.1f}{row['confidence']:>6.1f}"
                  f"{mv:>9s}{mi:>8s}  {row['outcome']}")
        if "spearman_vs_raw_move" in st:
            print(f"  spearman vs raw move        {st['spearman_vs_raw_move']}"
                  f"   (permutation p={st['p_permutation_raw']}, n={st['n']})")
            if "spearman_vs_move_over_implied" in st:
                print(f"  spearman vs move/implied    {st['spearman_vs_move_over_implied']}"
                      f"   (p={st['p_permutation_normalised']}, n={st['n_normalised']})")
            print(f"  long top third / short bottom third: "
                  f"{st['long_short_spread_pct']:+.2f}pp  (k={st['k_per_side']})")
        else:
            print(f"  {st.get('note')}")

    doc = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "runs": runs, "per_day": per_day,
           "pooled": stats_for(all_live, a.seed) if len(runs) > 1 else per_day[0]}
    out = Path(runs[0]) / "edge-outcome.json"
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    if len(runs) > 1:
        p = doc["pooled"]
        print(f"\n=== POOLED over {len(runs)} days, n={p.get('n')} ===")
        print(f"  spearman vs raw move     {p.get('spearman_vs_raw_move')}"
              f"  (p={p.get('p_permutation_raw')})")
        print(f"  spearman vs move/implied {p.get('spearman_vs_move_over_implied')}"
              f"  (p={p.get('p_permutation_normalised')})")
        print(f"  long/short spread        {p.get('long_short_spread_pct')}pp")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

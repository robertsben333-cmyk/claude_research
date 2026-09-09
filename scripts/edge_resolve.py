#!/usr/bin/env python3
"""Resolve a ranking against what the stocks actually did.

The question this answers is not "was the call right". It is **can these companies
be ranked** — does sorting a day's names by the ranking key put the ones that went up
above the ones that went down.

That is measured by rank correlation, which needs no threshold, no call and no
abstention, and which every name in the day contributes to. The old version of
this script plotted accuracy against a confidence threshold, which required the
scorer to emit a binary call; on 2026-08-31 it emitted none and the curve was
empty at every point.

Two correlations are reported and they answer different questions:

  vs raw move          did the ranking sort the day's actual returns
  vs move / implied    did it sort them after dividing out how much each name was
                       ever going to move. NOTE: where a name has no option chain
                       the divisor falls back to a median historical reaction, so
                       this is not purely an implied-move normalisation -- 18 of the
                       first 43 resolved names took the fallback

Three more numbers, added 2026-09-09 because without them a run cannot be judged:

  conviction vs sign   the threshold-free direction test. Does the RANK of
                       abs(score) predict whether the sign turned out right? Over
                       all 38 events of the first six runs the sign was a coin flip
                       (53%), but this correlation was +0.514 with a within-day
                       permutation p of 0.0015. It needs no cut and no calibration,
                       which is why it is the number to watch as days pool
  the controls         -run_up_20d_pct and priced_lean_pct, both off the sealed
                       baseline before a subagent is spawned. The first ranked the
                       same six days at rho=0.335. A run that does not beat the
                       controls has established nothing
  pooled WITHIN days   each day is converted to within-day ranks, centred, and the
                       centred ranks correlated across days. Concatenating raw pairs
                       across days lets market-wide drift into the rank structure and
                       understates every ranker (0.189 against 0.243 for the old key)

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


def score_of(row):
    """The ranking key. `impact_sum` since 2026-09-09; `edge_score` before that."""
    v = row.get("impact_sum")
    return float(v) if v is not None else float(row.get("edge_score") or 0.0)


def centred_ranks(xs):
    r = _ranks(xs)
    m = statistics.fmean(r)
    return [x - m for x in r]


def pooled_within_days(days, key):
    """Day-fixed-effect rank correlation: only within-day ordering contributes."""
    A, B = [], []
    for rows in days:
        v = [r for r in rows if r.get(key) is not None]
        if len(v) < 3:
            continue
        A += centred_ranks([r[key] for r in v])
        B += centred_ranks([r["move_pct"] for r in v])
    if len(A) < 3:
        return None, 0
    mx, my = statistics.fmean(A), statistics.fmean(B)
    num = sum((a - mx) * (b - my) for a, b in zip(A, B))
    dx = math.sqrt(sum((a - mx) ** 2 for a in A))
    dy = math.sqrt(sum((b - my) ** 2 for b in B))
    return (round(num / (dx * dy), 3) if dx and dy else None), len(A)


def conviction_vs_sign(rows):
    """Does the rank of abs(score) predict whether the sign was right?

    One test, no threshold in it, which is what makes it the honest form of "the
    effect is stronger on the big predictions".
    """
    v = [r for r in rows if r.get("score") not in (None, 0)]
    if len(v) < 4:
        return None, 0
    a = _ranks([abs(r["score"]) for r in v])
    b = [1.0 if (r["score"] > 0) == (r["move_pct"] > 0) else 0.0 for r in v]
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    dx = math.sqrt(sum((x - ma) ** 2 for x in a))
    dy = math.sqrt(sum((y - mb) ** 2 for y in b))
    return (round(num / (dx * dy), 3) if dx and dy else None), len(v)


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
               "score": score_of(r),
               "conviction": r.get("conviction"),
               "edge_score_legacy": (r.get("diagnostics") or {}).get(
                   "edge_score_legacy", r.get("edge_score")),
               "priced_lean_pct": r.get("priced_lean_pct"),
               "neg_run_up_20d": (None if (b.get("tape") or {}).get("run_up_20d_pct")
                                  is None else -(b["tape"]["run_up_20d_pct"])),
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
    e = [r["score"] for r in live]
    mv = [r["move_pct"] for r in live]
    out = {"n": len(live)}
    s, p = permutation_p(e, mv, seed)
    out["spearman_vs_raw_move"] = s
    out["p_permutation_raw"] = p
    # The controls. Both are free and both must be beaten before the hunt has
    # established anything.
    for key, lab in (("neg_run_up_20d", "control_neg_run_up_20d"),
                     ("priced_lean_pct", "control_priced_lean")):
        c = [r for r in live if r.get(key) is not None]
        if len(c) >= 3:
            out[lab] = spearman([r[key] for r in c], [r["move_pct"] for r in c])
    cs, cn = conviction_vs_sign(live)
    if cs is not None:
        out["conviction_vs_sign_correct"] = cs
        out["n_conviction"] = cn
        hits = sum(1 for r in live if r["score"] and
                   (r["score"] > 0) == (r["move_pct"] > 0))
        nz = sum(1 for r in live if r["score"])
        out["sign_hits"] = f"{hits}/{nz}"
    norm = [r for r in live if r.get("move_over_implied") is not None]
    if len(norm) >= 3:
        s2, p2 = permutation_p([r["score"] for r in norm],
                               [r["move_over_implied"] for r in norm], seed)
        out["spearman_vs_move_over_implied"] = s2
        out["p_permutation_normalised"] = p2
        out["n_normalised"] = len(norm)
    # Long the top third, short the bottom third. The ranking's payoff if you
    # traded it, which is the only version of "does the order matter" that pays.
    k = max(1, len(live) // 3)
    srt = sorted(live, key=lambda r: -r["score"])
    top = statistics.fmean(r["move_pct"] for r in srt[:k])
    bot = statistics.fmean(r["move_pct"] for r in srt[-k:])
    out["top_third_mean_move_pct"] = round(top, 2)
    out["bottom_third_mean_move_pct"] = round(bot, 2)
    out["long_short_spread_pct"] = round(top - bot, 2)
    out["k_per_side"] = k
    return out


def pooled_block(days, seed):
    """Pool WITHIN days. Concatenating raw pairs across days lets market-wide drift
    into the rank structure and understates every ranker."""
    flat = [r for d in days for r in d]
    out = {"n": len(flat), "days": len(days),
           "pooling": "within-day ranks, centred, correlated across days"}
    for key, lab in (("score", "spearman_vs_raw_move"),
                     ("edge_score_legacy", "spearman_legacy_key"),
                     ("neg_run_up_20d", "control_neg_run_up_20d"),
                     ("priced_lean_pct", "control_priced_lean")):
        s, n = pooled_within_days(days, key)
        if s is not None:
            out[lab] = s
    cs, cn = conviction_vs_sign(flat)
    if cs is not None:
        out["conviction_vs_sign_correct"] = cs
        out["n_conviction"] = cn
        hits = sum(1 for r in flat if r["score"] and
                   (r["score"] > 0) == (r["move_pct"] > 0))
        nz = sum(1 for r in flat if r["score"])
        out["sign_hits"] = f"{hits}/{nz}"
    spreads = []
    for d in days:
        srt = sorted(d, key=lambda r: -r["score"])
        k = max(1, len(srt) // 3)
        spreads.append(statistics.fmean(r["move_pct"] for r in srt[:k])
                       - statistics.fmean(r["move_pct"] for r in srt[-k:]))
    if spreads:
        out["long_short_spread_pct"] = round(statistics.fmean(spreads), 2)
        out["long_short_positive_days"] = sum(1 for x in spreads if x > 0)
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

    all_live, per_day, per_day_live = [], [], []
    for rp in runs:
        r = resolve_run(rp, a.seed)
        st = stats_for(r["live"], a.seed)
        per_day.append({"run": r["run"], **st})
        all_live.extend(r["live"])
        if r["live"]:
            per_day_live.append(r["live"])

        print(f"\n=== {r['run']} ===")
        print(f"{'#':>2} {'ticker':8s}{'score':>8s}{'convict':>8s}{'move':>9s}"
              f"{'m/impl':>8s}{'sign':>6s}  outcome")
        for row in r["rows"]:
            mv = f"{row.get('move_pct'):+.2f}%" if row.get("move_pct") is not None else "   --"
            mi = f"{row.get('move_over_implied'):+.2f}" if row.get("move_over_implied") is not None else "   --"
            rk = f"{row['rank']:>2}" if row.get("rank") else "--"
            cv = f"{row['conviction']:.2f}" if row.get("conviction") is not None else "--"
            sg = ("--" if row.get("move_pct") is None or not row["score"]
                  else ("ok" if (row["score"] > 0) == (row["move_pct"] > 0) else "mis"))
            print(f"{rk} {row['ticker']:8s}{row['score']:>+8.2f}{cv:>8s}"
                  f"{mv:>9s}{mi:>8s}{sg:>6s}  {row['outcome']}")
        if "spearman_vs_raw_move" in st:
            print(f"  spearman vs raw move        {st['spearman_vs_raw_move']}"
                  f"   (permutation p={st['p_permutation_raw']}, n={st['n']})")
            if "spearman_vs_move_over_implied" in st:
                print(f"  spearman vs move/implied    {st['spearman_vs_move_over_implied']}"
                      f"   (p={st['p_permutation_normalised']}, n={st['n_normalised']})")
            if "conviction_vs_sign_correct" in st:
                print(f"  conviction vs sign-correct  {st['conviction_vs_sign_correct']}"
                      f"   (sign {st['sign_hits']}, n={st['n_conviction']})")
            for key, lab in (("control_neg_run_up_20d", "control: -20d run-up  "),
                             ("control_priced_lean", "control: priced lean  ")):
                if key in st:
                    print(f"  {lab}      {st[key]}")
            print(f"  long top third / short bottom third: "
                  f"{st['long_short_spread_pct']:+.2f}pp  (k={st['k_per_side']})")
        else:
            print(f"  {st.get('note')}")

    doc = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "runs": runs, "per_day": per_day,
           "pooled": pooled_block(per_day_live, a.seed) if len(runs) > 1 else per_day[0]}
    out = Path(runs[0]) / "edge-outcome.json"
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")

    if len(runs) > 1:
        p = doc["pooled"]
        print(f"\n=== POOLED over {p.get('days')} days, n={p.get('n')} "
              f"(within-day ranks) ===")
        print(f"  spearman vs raw move        {p.get('spearman_vs_raw_move')}")
        print(f"  conviction vs sign-correct  {p.get('conviction_vs_sign_correct')}"
              f"   (sign {p.get('sign_hits')})")
        print(f"  control: -20d run-up        {p.get('control_neg_run_up_20d')}")
        print(f"  control: priced lean        {p.get('control_priced_lean')}")
        print(f"  legacy edge_score key       {p.get('spearman_legacy_key')}")
        print(f"  long/short spread           {p.get('long_short_spread_pct')}pp"
              f"  (positive on {p.get('long_short_positive_days')} of "
              f"{p.get('days')} days)")
        print("\n  A run that does not beat the controls has established nothing.")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Does what the stock did BEFORE the print tell you anything about the call?

Two questions, and they are not the same question.

  1. ACCURACY. Does the 2/5/10/20-session return into the entry predict whether the
     hunt's sign turned out right? This needs no trade: it is hit-or-miss against a
     continuous predictor, so it is measured as a rank correlation between the
     run-up and a 0/1 outcome, and as a hit rate by bucket.

  2. AGREEMENT. When the run-up points the SAME way as the prediction, is the trade
     worth more? This is the one that changes what you do, because it is a filter
     you can apply before the close on the entry day, using only free data.

MEASURED TO 20:00 CET, NOT TO THE CLOSE. Every run-up here ends at the 14:00 ET bar
on the entry day -- 20:00 CET, the moment the book is placed. Running it to the
close would put two hours of price into a predictor that is supposed to be known at
entry, and those two hours are on the wrong side of the decision.

THE ENTRY DAY IS NOT THE EVENT DAY FOR bmo. A bmo print lands before the open on the
event date, so the last session you can trade is the one BEFORE it. amc enters on the
event date itself. The run-up windows count back in sessions from whichever that is.

THE CONTROL THIS HAS TO BEAT. `-run_up_20d_pct` off the sealed baseline already ranks
the first six days at rho=0.335 and is the free control the hunt has never beaten.
That is the same family of number as this, so agreement between run-up and prediction
is partly agreement between the hunt and a control that beats it. The script reports
the control's own book beside every cut for exactly that reason.

    python3 edge/scripts/edge_runup.py
    python3 edge/scripts/edge_runup.py --floor 3.0 --exit close
"""
import argparse
import json
import statistics as st
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import edge_bars as EB          # noqa: E402
import edge_sample as ES        # noqa: E402
import edge_stats as SS         # noqa: E402

WINDOWS = [2, 5, 10, 20]


def sign(x):
    if x is None:
        return 0
    return 1 if x > 0 else (-1 if x < 0 else 0)


def build(events, entry_hh=14):
    """Attach prices, run-ups and the realised move to every event that has bars."""
    out, dropped = [], []
    for e in events:
        rows, err = EB.bars(e["ticker"])
        if err or not rows:
            dropped.append((e["ticker"], e["event_date"], err or "no bars"))
            continue
        days = EB.by_day(rows)
        ds = sorted(days)
        ed = e["event_date"]
        if ed not in ds:
            dropped.append((e["ticker"], ed, "no session on the event date"))
            continue
        i = ds.index(ed)
        if e["session"] == "amc":
            entry_i, exit_i = i, i + 1
        else:
            entry_i, exit_i = i - 1, i
        if entry_i < 0 or exit_i >= len(ds):
            dropped.append((e["ticker"], ed, "entry or exit session outside the bar window"))
            continue
        entry_day, exit_day = ds[entry_i], ds[exit_i]
        entry, how = EB.price_at(days[entry_day], entry_hh)
        if entry is None:
            dropped.append((e["ticker"], ed, f"no {entry_hh}:00 ET bar on {entry_day}"))
            continue

        r = dict(e)
        r["entry_day"], r["exit_day"] = entry_day, exit_day
        r["entry_price"], r["entry_basis"] = entry, how
        r["entry_day_close"] = EB.day_close(days[entry_day])
        r["exit_open"] = EB.day_open(days[exit_day])
        r["exit_close"] = EB.day_close(days[exit_day])

        # run-ups: entry price against the close N sessions before the entry day
        for w in WINDOWS:
            j = entry_i - w
            r[f"runup_{w}d"] = None
            if j >= 0:
                base = EB.day_close(days[ds[j]])
                if base:
                    r[f"runup_{w}d"] = round((entry / base - 1) * 100, 3)

        # the realised move, on the window edge_resolve.py scores: the close before
        # the print to the close after the first full session
        base_close = r["entry_day_close"]
        r["move_close"] = round((r["exit_close"] / base_close - 1) * 100, 3) if base_close else None
        r["move_open"] = round((r["exit_open"] / base_close - 1) * 100, 3) if base_close else None
        # what the book actually earned: in at 20:00 CET, out at the exit
        r["trade_close"] = round(sign(e["impact_sum"]) * (r["exit_close"] / entry - 1) * 100, 3)
        r["trade_open"] = round(sign(e["impact_sum"]) * (r["exit_open"] / entry - 1) * 100, 3)
        out.append(r)
    return out, dropped


def by_day(rows):
    d = {}
    for r in rows:
        d.setdefault(r["run_date"], []).append(r)
    return [d[k] for k in sorted(d)]


def block(label, rets, days=None):
    s = SS.summarise(rets)
    if not s.get("n"):
        return {"label": label, "n": 0}
    lo, hi = SS.boot_days(days) if days else (float("nan"), float("nan"))
    s.update({"label": label, "ci_lo": lo, "ci_hi": hi})
    print(f"  {label:38s}{s['hits']:>3d}/{s['n']:<4d}"
          f"{s['hit_rate']*100:>7.0f}%{s['mean']:>+9.2f}%{s['t']:>7.2f}"
          f"   [{lo:+.2f}, {hi:+.2f}]")
    return s


def split_days(rows, pred, key):
    d = {}
    for r in rows:
        if pred(r):
            d.setdefault(r["run_date"], []).append(r[key])
    return list(d.values())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pool", default="research/2026/*/*/edge")
    ap.add_argument("--floor", type=float, default=3.0,
                    help="conviction floor for the traded book (0 for every name)")
    ap.add_argument("--exit", default="close", choices=["close", "open"])
    ap.add_argument("--out", default="edge/analysis/edge-runup.json")
    a = ap.parse_args()

    ek = f"trade_{a.exit}"
    mk = f"move_{a.exit}"
    events = ES.load(a.pool)
    rows, dropped = build(events)
    print(f"{len(rows)} events with bars, {len(dropped)} dropped, "
          f"over {len(by_day(rows))} days\n")
    for t, d, why in dropped:
        print(f"  dropped  {t:8s} {d}  {why}")
    if dropped:
        print()

    floor = [r for r in rows if abs(r["impact_sum"] or 0) >= a.floor]
    print(f"{len(floor)} of {len(rows)} clear the {a.floor} conviction floor. "
          f"Exit: {a.exit}.\n")

    res = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_events": len(rows), "n_days": len(by_day(rows)),
        "floor": a.floor, "n_above_floor": len(floor), "exit": a.exit,
        "dropped": [{"ticker": t, "event_date": d, "why": w} for t, d, w in dropped],
        "windows": {}, "agreement": {}, "books": {}, "rows": rows,
    }

    # ---------------------------------------------------------------- question 1
    print("QUESTION 1 -- does the run-up predict whether the hunt's SIGN was right?")
    print("A hit is sign(impact_sum) == sign(realised move). rho is over the run-up")
    print("against that 0/1 outcome; the second rho is over |run-up|, since a big move")
    print("in either direction is the thing a reader would actually notice.\n")
    print(f"  {'window':10s}{'n':>5s}{'rho(runup)':>12s}{'p':>8s}"
          f"{'rho(|runup|)':>14s}{'p':>8s}   hit rate by run-up tercile")
    for w in WINDOWS:
        rs = [r for r in rows if r.get(f"runup_{w}d") is not None and r[mk] is not None]
        if len(rs) < 6:
            continue
        hit = [1.0 if sign(r["impact_sum"]) == sign(r[mk]) else 0.0 for r in rs]
        ru = [r[f"runup_{w}d"] for r in rs]
        rho1, p1 = SS.spearman_perm(ru, hit)
        rho2, p2 = SS.spearman_perm([abs(x) for x in ru], hit)
        order = sorted(range(len(rs)), key=lambda i: ru[i])
        k = len(order) // 3
        terc = [order[:k], order[k:2 * k], order[2 * k:]]
        rates = [sum(hit[i] for i in g) / len(g) for g in terc if g]
        print(f"  {str(w) + 'd':10s}{len(rs):>5d}{rho1:>+12.3f}{p1:>8.3f}"
              f"{rho2:>+14.3f}{p2:>8.3f}   " + "  ".join(f"{x*100:.0f}%" for x in rates))
        res["windows"][f"{w}d"] = {
            "n": len(rs), "rho_signed": rho1, "p_signed": p1,
            "rho_abs": rho2, "p_abs": p2, "tercile_hit_rates": rates,
            "tercile_edges": [ru[order[k]], ru[order[2 * k]]] if k else None,
        }

    # ---------------------------------------------------------------- question 2
    print("\n\nQUESTION 2 -- when the run-up AGREES with the prediction, is the trade")
    print("worth more? Agreement is sign(run-up) == sign(impact_sum). The book is")
    print("equal-weight, signed by the prediction, entered at 20:00 CET.\n")
    print(f"  {'cut':38s}{'hits':>7s}{'rate':>8s}{'mean':>9s}{'t':>7s}   95% CI (day bootstrap)")

    for label, pool in (("all names", rows), (f"conviction >= {a.floor}", floor)):
        print(f"\n  -- {label}, n={len(pool)}")
        block("every name", [r[ek] for r in pool], split_days(pool, lambda r: True, ek))
        for w in WINDOWS:
            ag = [r for r in pool if r.get(f"runup_{w}d") is not None
                  and sign(r[f"runup_{w}d"]) == sign(r["impact_sum"])]
            di = [r for r in pool if r.get(f"runup_{w}d") is not None
                  and sign(r[f"runup_{w}d"]) != sign(r["impact_sum"])]
            sa = block(f"{w}d run-up AGREES", [r[ek] for r in ag],
                       split_days(pool, lambda r, w=w: r.get(f"runup_{w}d") is not None
                                  and sign(r[f"runup_{w}d"]) == sign(r["impact_sum"]), ek))
            sd = block(f"{w}d run-up DISAGREES", [r[ek] for r in di],
                       split_days(pool, lambda r, w=w: r.get(f"runup_{w}d") is not None
                                  and sign(r[f"runup_{w}d"]) != sign(r["impact_sum"]), ek))
            res["agreement"].setdefault(label, {})[f"{w}d"] = {"agree": sa, "disagree": sd,
                                                               "gap": (sa.get("mean", 0)
                                                                       - sd.get("mean", 0))}
        n_all = [w for w in WINDOWS
                 if all(r.get(f"runup_{w}d") is not None for r in pool)]
        if len(n_all) == len(WINDOWS):
            allag = [r for r in pool
                     if all(sign(r[f"runup_{w}d"]) == sign(r["impact_sum"]) for w in WINDOWS)]
            block("ALL FOUR windows agree", [r[ek] for r in allag],
                  split_days(pool, lambda r: all(sign(r[f"runup_{w}d"]) == sign(r["impact_sum"])
                                                 for w in WINDOWS), ek))
            res["agreement"].setdefault(label, {})["all_four"] = SS.summarise(
                [r[ek] for r in allag])

    # ---------------------------------------------------------------- the control
    print("\n\nTHE FREE CONTROL, on the same events and the same entry. Short every")
    print("name; and trade the sign of MINUS the 20-day run-up, which is the rule that")
    print("has beaten the hunt on every sample in edge/EDGE_ANALYSIS.md.\n")
    print(f"  {'rule':38s}{'hits':>7s}{'rate':>8s}{'mean':>9s}{'t':>7s}   95% CI (day bootstrap)")
    short = [{**r, "x": -r[mk]} for r in rows if r[mk] is not None]
    block("short every name", [r["x"] for r in short],
          split_days(short, lambda r: True, "x"))
    mom = [{**r, "x": -sign(r["runup_20d"]) * r[mk]} for r in rows
           if r.get("runup_20d") is not None and r[mk] is not None]
    block("minus 20d run-up", [r["x"] for r in mom], split_days(mom, lambda r: True, "x"))
    for w in WINDOWS:
        m = [{**r, "x": -sign(r[f"runup_{w}d"]) * r[mk]} for r in rows
             if r.get(f"runup_{w}d") is not None and r[mk] is not None]
        res["books"][f"minus_runup_{w}d"] = SS.summarise([r["x"] for r in m])
    res["books"]["short_all"] = SS.summarise([r["x"] for r in short])
    res["books"]["hunt_all"] = SS.summarise([r[ek] for r in rows])
    res["books"]["hunt_above_floor"] = SS.summarise([r[ek] for r in floor])

    Path(REPO / a.out).write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()

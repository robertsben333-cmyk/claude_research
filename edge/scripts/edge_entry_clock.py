#!/usr/bin/env python3
"""Buy at 20:00 CET, or later? The entry priced at every half hour of the session.

`edge/scripts/edge_exit.py` prices the clock on the way OUT. This prices it on the
way IN, holding the exit fixed, so the two are separable: any difference between two
rows here is entry timing and nothing else.

WHAT 20:00 CET IS. 14:00 New York, in summer. It is the entry `claude_naive` was
backtested on, the entry `backtest/scripts/trade_prices.py` freezes, and roughly when
stage E's own run finishes and step 7 sends its order. Everything here is measured
against that row.

WHY THE GRID STOPS AT THE CLOSE. For an `amc` name the print lands after 16:00, so
the last tradeable minute is the close and "later" has no meaning past it. For a
`bmo` name the print lands before the next open, so the entry day's close is again
the last liquid moment -- the overnight session between them carries no size from
this source and `edge/EDGE_ANALYSIS.md` already has one finding resting on that trap.
So "later" means later in the entry session, and the grid runs 10:00 to the close.

EARLIER IS ALSO PRICED. The grid starts at 10:00 ET because the question "is later
better" only means something beside its mirror. If the book pays more at 10:00 than
at 16:00 then the honest answer is that the run should finish sooner, not later.

TWO EXITS, BOTH REPORTED. The exit is held fixed while the entry moves, at the next
open and at the next close. They disagree in `edge/EDGE_ANALYSIS.md` -- the gap to
the open pays the whole conviction book and the session leg pays nothing -- so an
entry conclusion that only holds at one of them is not a conclusion.

    python3 edge/scripts/edge_entry_clock.py
    python3 edge/scripts/edge_entry_clock.py --floor 0
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
import edge_runup as RU         # noqa: E402
import edge_sample as ES        # noqa: E402
import edge_stats as SS         # noqa: E402

# half-hour marks through the regular session. 16:00 is the close, taken as the
# last bar of the day rather than a 16:00 stamp that only sometimes exists.
GRID = [(10, 0), (10, 30), (11, 0), (11, 30), (12, 0), (12, 30), (13, 0), (13, 30),
        (14, 0), (14, 30), (15, 0), (15, 30), (16, 0)]
ANCHOR = (14, 0)


def label(hh, mm):
    cet = (hh + 6) % 24                 # ET -> CET in summer, +6
    return f"{hh:02d}:{mm:02d} ET / {cet:02d}:{mm:02d} CET"


def entry_prices(events):
    """Every event, with its price at each grid point on the entry day."""
    out, dropped = [], []
    for e in events:
        rows, err = EB.bars(e["ticker"])
        if err or not rows:
            dropped.append((e["ticker"], e["event_date"], err or "no bars"))
            continue
        days = EB.by_day(rows)
        ds = sorted(days)
        if e["event_date"] not in ds:
            dropped.append((e["ticker"], e["event_date"], "no session on the event date"))
            continue
        i = ds.index(e["event_date"])
        entry_i, exit_i = (i, i + 1) if e["session"] == "amc" else (i - 1, i)
        if entry_i < 0 or exit_i >= len(ds):
            dropped.append((e["ticker"], e["event_date"], "window outside the bars"))
            continue
        eb, xb = days[ds[entry_i]], days[ds[exit_i]]
        r = dict(e)
        r["entry_day"], r["exit_day"] = ds[entry_i], ds[exit_i]
        r["exit_open"], r["exit_close"] = EB.day_open(xb), EB.day_close(xb)
        r["prices"] = {}
        for hh, mm in GRID:
            if (hh, mm) == (16, 0):
                px, how = EB.day_close(eb), "close"
            else:
                px, how = EB.price_at(eb, hh, mm)
            if px:
                r["prices"][f"{hh:02d}{mm:02d}"] = {"px": px, "basis": how}
        if f"{ANCHOR[0]:02d}{ANCHOR[1]:02d}" not in r["prices"]:
            dropped.append((e["ticker"], e["event_date"], "no 14:00 ET bar on the entry day"))
            continue
        out.append(r)
    return out, dropped


def book(rows, hh, mm, exit_key):
    """Equal-weight return per trade entering at hh:mm, signed by impact_sum."""
    k = f"{hh:02d}{mm:02d}"
    rets, per_day = [], {}
    for r in rows:
        p = r["prices"].get(k)
        if not p or not r[exit_key]:
            continue
        v = RU.sign(r["impact_sum"]) * (r[exit_key] / p["px"] - 1) * 100
        rets.append(v)
        per_day.setdefault(r["run_date"], []).append(v)
    return rets, list(per_day.values())


def rank_at(rows, hh, mm, exit_key):
    """Does impact_sum still RANK the day's returns from this entry?"""
    k = f"{hh:02d}{mm:02d}"
    days = {}
    for r in rows:
        p = r["prices"].get(k)
        if not p or not r[exit_key]:
            continue
        days.setdefault(r["run_date"], []).append(
            {"pred": r["impact_sum"], "ret": (r[exit_key] / p["px"] - 1) * 100})
    return SS.within_day_perm(list(days.values()), "pred", "ret", n=4000)


def table(title, rows, exit_key, res, tag):
    print(f"\n{title}  (n={len(rows)} events, "
          f"{len({r['run_date'] for r in rows})} days, exit at the next {exit_key[5:]})")
    print(f"  {'entry':24s}{'n':>5s}{'hits':>7s}{'rate':>7s}{'mean':>9s}{'t':>7s}"
          f"{'rho':>8s}{'p':>7s}   vs 20:00 CET")
    base = None
    for hh, mm in GRID:
        rets, per_day = book(rows, hh, mm, exit_key)
        if len(rets) < 5:
            continue
        s = SS.summarise(rets)
        rho, p, _ = rank_at(rows, hh, mm, exit_key)
        if (hh, mm) == ANCHOR:
            base = s["mean"]
        d = "" if base is None else f"{s['mean'] - base:+.2f}pp"
        mark = "<-- 20:00 CET" if (hh, mm) == ANCHOR else d
        print(f"  {label(hh, mm):24s}{s['n']:>5d}{s['hits']:>7d}{s['hit_rate']*100:>6.0f}%"
              f"{s['mean']:>+9.2f}%{s['t']:>7.2f}{rho:>+8.3f}{p:>7.3f}   {mark}")
        res.setdefault(tag, {})[f"{hh:02d}{mm:02d}"] = {
            **s, "rho": rho, "p": p, "label": label(hh, mm),
            "ci": SS.boot_days(per_day)}
    # the honest version of "which hour is best": the spread, and what it costs to
    # have picked the best one after looking
    vals = [(v["mean"], k) for k, v in res.get(tag, {}).items()]
    if vals:
        best, worst = max(vals), min(vals)
        print(f"  spread across the session: {worst[0]:+.2f}% at {worst[1]} to "
              f"{best[0]:+.2f}% at {best[1]}  ({best[0] - worst[0]:.2f}pp)")
        res.setdefault(tag + "_spread", {}).update(
            {"best": best[1], "best_mean": best[0],
             "worst": worst[1], "worst_mean": worst[0], "spread": best[0] - worst[0]})


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pool", default="research/2026/*/*/edge")
    ap.add_argument("--floor", type=float, default=3.0)
    ap.add_argument("--out", default="edge/analysis/edge-entry-clock.json")
    a = ap.parse_args()

    rows, dropped = entry_prices(ES.load(a.pool))
    print(f"{len(rows)} events priced across the session, {len(dropped)} dropped.")
    for t, d, why in dropped:
        print(f"  dropped  {t:8s} {d}  {why}")

    res = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "n_events": len(rows), "floor": a.floor, "grid": [label(*g) for g in GRID],
           "anchor": label(*ANCHOR),
           "dropped": [{"ticker": t, "event_date": d, "why": w} for t, d, w in dropped]}

    floor = [r for r in rows if abs(r["impact_sum"] or 0) >= a.floor]
    for exit_key, xn in (("exit_close", "close"), ("exit_open", "open")):
        table(f"ALL NAMES -> next {xn}", rows, exit_key, res, f"all_{xn}")
        table(f"CONVICTION >= {a.floor} -> next {xn}", floor, exit_key, res, f"floor_{xn}")

    for sess in ("amc", "bmo"):
        sub = [r for r in floor if r["session"] == sess]
        if len(sub) >= 8:
            table(f"CONVICTION >= {a.floor}, {sess} only -> next close",
                  sub, "exit_close", res, f"{sess}_close")

    # the drift you are paying for by waiting, independent of any prediction
    print("\n\nWHAT THE WAIT COSTS BEFORE ANY PREDICTION IS APPLIED")
    print("Mean unsigned return from each entry to the entry day's close. If this is")
    print("not flat, the session has a drift and the book is picking it up either way.\n")
    print(f"  {'entry':24s}{'n':>5s}{'mean drift to close':>22s}{'t':>8s}")
    for hh, mm in GRID[:-1]:
        k = f"{hh:02d}{mm:02d}"
        d = [(r["prices"]["1600"]["px"] / r["prices"][k]["px"] - 1) * 100
             for r in rows if k in r["prices"] and "1600" in r["prices"]]
        if len(d) < 5:
            continue
        print(f"  {label(hh, mm):24s}{len(d):>5d}{st.mean(d):>+21.3f}%{SS.tstat(d):>8.2f}")
        res.setdefault("drift_to_close", {})[k] = {"n": len(d), "mean": st.mean(d),
                                                   "t": SS.tstat(d)}

    Path(REPO / a.out).write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()

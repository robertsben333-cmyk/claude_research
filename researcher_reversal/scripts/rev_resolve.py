"""Resolve a reversal run against what the stocks actually did.

THE QUESTION IS THE SAME ONE researcher_us/scripts/edge_resolve.py ASKS
-----------------------------------------------------------------------
Not "was the call right", which needs a threshold nobody has earned, but: can the
day's fallen names be RANKED. Does sorting them by the hunt's signed number put the
ones that bounced above the ones that kept falling. Rank correlation needs no cut, no
abstention and no calibration, and every name in the day contributes to it.

WHAT IS DIFFERENT HERE, AND IT IS THE HARD PART
-----------------------------------------------
The free control in this stage is not a weak one. `-ret_d` -- rank by how far it fell
-- is short-horizon reversal, one of the most documented effects in equities, and it
costs nothing. The hunt has to beat it, on the same days, or it has established
nothing. So four controls are reported beside the key on every run and none of them is
optional reading:

  neg_ret_d         the size of the fall. THE benchmark
  priced_lean_pct   the baseline's own lean, which is built partly FROM the fall, so
                    `lean_vs_free_control_rho` says how much of it is the benchmark
                    wearing a different name. Stage J shipped at 1.0 by construction
  neg_run_up_20d    the control stage E measures against, kept for comparability
  gap_share         whether the fall was overnight or intraday, the cheapest proxy
                    there is for "scheduled news" against "drift"

And one thing this stage can ask that no earnings stage can: whether the hunt's
CAUSE classification carries the result. The hypothesis is pre-registered in
researcher_reversal/README.md -- mechanical causes revert, informational causes drift
-- and `by_cause` and `mechanical_vs_informational` are reported whether or not it
looks good, because a hypothesis read off the answer is not a hypothesis.

    python3 researcher_reversal/scripts/rev_resolve.py --run research/2026/09/2026-09-22/reversal
    python3 researcher_reversal/scripts/rev_resolve.py --run <dir> --pool-with <dir> <dir>
"""
import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import rev_market as M                                            # noqa: E402

HORIZONS = ["open1", "d1", "d2", "d3", "d5", "d10", "d21"]
HEADLINE = "d1"


def realised(ticker, drop_date):
    """What the stock did from the drop-day close. None where it has not happened yet."""
    b = M.bars(ticker, rg="6mo")
    dates = [x["date"] for x in b]
    if drop_date not in dates:
        return None, f"no bar on {drop_date}"
    i = dates.index(drop_date)
    base = b[i]["close"]
    out = {"entry_close": round(b[i]["raw_close"], 4), "last_bar": b[-1]["date"]}
    for key, field, k in (("open1", "open", 1), ("d1", "close", 1), ("d2", "close", 2),
                          ("d3", "close", 3), ("d5", "close", 5), ("d10", "close", 10),
                          ("d21", "close", 21)):
        j = i + k
        out[key + "_pct"] = (round((b[j][field] / base - 1) * 100, 3)
                             if j < len(b) else None)
    out["pending"] = out[HEADLINE + "_pct"] is None
    return out, None


def load_run(run):
    run = Path(run)
    scores = json.loads((run / "edge-scores.json").read_text())
    baselines = {}
    for f in sorted((run / "baselines").glob("*.json")):
        try:
            baselines[f.stem.upper()] = json.loads(f.read_text())
        except Exception:                                         # noqa: BLE001
            pass
    causes = {}
    for f in sorted((run / "hunts").glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except Exception:                                         # noqa: BLE001
            continue
        t = (d.get("ticker") or f.stem.split("-")[0]).upper()
        if d.get("cause"):
            causes[t] = d["cause"]
    return scores, baselines, causes


def build_rows(run):
    scores, baselines, causes = load_run(run)
    rows = []
    for r in scores.get("ranking", []):
        if not r.get("rankable"):
            continue
        t = r["ticker"].upper()
        b = baselines.get(t) or {}
        drop_date = b.get("drop_date") or scores.get("drop_date")
        if not drop_date:
            continue
        mv, err = realised(t, drop_date)
        if mv is None:
            continue
        c = causes.get(t) or {}
        rows.append({
            "ticker": t, "drop_date": drop_date,
            "impact_sum": r.get("impact_sum"),
            "conviction": r.get("conviction"),
            "impact_sum_pre_lessons": (r.get("diagnostics") or {}).get("impact_sum_pre_lessons"),
            "priced_lean_pct": r.get("priced_lean_pct"),
            "baseline_quality": r.get("baseline_quality"),
            "ret_d_pct": (b.get("drop") or {}).get("ret_d_pct"),
            "gap_share": (b.get("drop") or {}).get("gap_share"),
            "dv_med20": (b.get("drop") or {}).get("dv_med20"),
            "half_spread_pct": (b.get("costs") or {}).get("half_spread_pct"),
            "run_up_20d_pct": (b.get("context") or {}).get("run_up_20d_pct"),
            "sector": b.get("sector"),
            "atr14_pct": (b.get("context") or {}).get("atr14_pct"),
            "volume_spike_x": (b.get("drop") or {}).get("volume_spike_x"),
            "cause": c.get("label"),
            "mechanical_vs_informational": c.get("mechanical_vs_informational"),
            **{k: v for k, v in (mv or {}).items()},
        })
    return rows


def rank_block(rows, horizon, reps=2000):
    """Every ranker against the realised move, pooled WITHIN days."""
    by_day = defaultdict(list)
    for r in rows:
        if r.get(horizon + "_pct") is not None:
            by_day[r["drop_date"]].append(r)

    keys = {
        "impact_sum": lambda r: r["impact_sum"],
        "impact_sum_pre_lessons": lambda r: r["impact_sum_pre_lessons"],
        "priced_lean_pct": lambda r: r["priced_lean_pct"],
        "neg_ret_d (free control)": lambda r: (-r["ret_d_pct"] if r["ret_d_pct"] is not None else None),
        "neg_run_up_20d (free control)": lambda r: (-r["run_up_20d_pct"]
                                                    if r["run_up_20d_pct"] is not None else None),
        "gap_share (free control)": lambda r: r["gap_share"],
        # Phase 0's two strongest free rankers over 11,235 events on 749 sessions.
        # atr14 was the best of thirteen candidates at rho=-0.126 and survived a
        # max-statistic correction at family p=0.0017, so it is THE bar, not a
        # curiosity. vol_spike separates a fall on real volume from a quiet one.
        "neg_atr14 (free control)": lambda r: (-r["atr14_pct"]
                                               if r.get("atr14_pct") is not None else None),
        "neg_vol_spike (free control)": lambda r: (-r["volume_spike_x"]
                                                   if r.get("volume_spike_x") is not None else None),
        "mechanical_vs_informational": lambda r: r["mechanical_vs_informational"],
    }
    out = {}
    for name, fn in keys.items():
        groups = []
        for d, rs in by_day.items():
            g = [(fn(r), r[horizon + "_pct"]) for r in rs]
            g = [(a, b) for a, b in g if a is not None and b is not None]
            if len(g) >= 3:
                groups.append(g)
        if not groups:
            out[name] = {"rho": None, "perm_p": None, "days": 0}
            continue
        rho, p = M.permutation_p(groups, None, None, reps=reps)
        out[name] = {"rho": rho, "perm_p": p, "days": len(groups),
                     "names": sum(len(g) for g in groups)}
    return out


def conviction_block(rows, horizon):
    """Does the RANK of conviction predict whether the sign was right?

    This is the one result stage E has that survived a family-wise correction, and it
    is the first thing to check here because it is threshold-free and because the
    reversal stage's whole claim is directional.
    """
    ok, conv = [], []
    for r in rows:
        mv, imp = r.get(horizon + "_pct"), r.get("impact_sum")
        if mv is None or imp is None or imp == 0:
            continue
        ok.append(1.0 if (mv > 0) == (imp > 0) else 0.0)
        conv.append(abs(imp))
    if len(ok) < 4:
        return {"n": len(ok)}
    med = statistics.median(conv)
    hi = [o for o, c in zip(ok, conv) if c >= med]
    lo = [o for o, c in zip(ok, conv) if c < med]
    return {
        "n": len(ok),
        "sign_right_pct": round(100 * M.mean(ok), 1),
        "sign_p": M.sign_test_p(int(sum(ok)), len(ok)),
        "rho_conviction_vs_sign_right": M.spearman(conv, ok),
        "above_median_conviction_pct": round(100 * M.mean(hi), 1) if hi else None,
        "below_median_conviction_pct": round(100 * M.mean(lo), 1) if lo else None,
    }


def book_block(rows, horizon, floor, cost_mult=1.0):
    """What the rule would have earned: side from the sign, size equal, cost charged."""
    legs = []
    for r in rows:
        imp, mv = r.get("impact_sum"), r.get(horizon + "_pct")
        hs = r.get("half_spread_pct")
        if imp is None or mv is None or abs(imp) < floor:
            continue
        side = 1 if imp > 0 else -1
        gross = side * mv
        net = gross - 2 * cost_mult * (hs or 0.0)
        legs.append({"ticker": r["ticker"], "side": "long" if side > 0 else "short",
                     "gross_pct": round(gross, 3), "net_pct": round(net, 3)})
    g = [x["gross_pct"] for x in legs]
    n = [x["net_pct"] for x in legs]
    lo, hi = M.bootstrap_ci(n) if len(n) > 2 else (None, None)
    return {
        "conviction_floor": floor, "cost_multiple": cost_mult,
        "n_legs": len(legs),
        "gross_mean_pct": round(M.mean(g), 3) if g else None,
        "net_mean_pct": round(M.mean(n), 3) if n else None,
        "net_t": M.tstat(n), "net_ci95": [lo, hi],
        "win_rate_pct": round(100 * sum(1 for x in n if x > 0) / len(n), 1) if n else None,
        "legs": legs,
        "free_control_short_everything_pct": (
            round(M.mean([-r[horizon + "_pct"] for r in rows
                          if r.get(horizon + "_pct") is not None]), 3)),
        "free_control_long_everything_pct": (
            round(M.mean([r[horizon + "_pct"] for r in rows
                          if r.get(horizon + "_pct") is not None]), 3)),
    }


def by_cause(rows, horizon):
    out = []
    groups = defaultdict(list)
    for r in rows:
        if r.get(horizon + "_pct") is not None:
            groups[r.get("cause") or "unclassified"].append(r[horizon + "_pct"])
    for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        out.append({"cause": k, "n": len(v),
                    "mean_next_pct": round(M.mean(v), 3),
                    "median_next_pct": round(statistics.median(v), 3),
                    "up_rate_pct": round(100 * sum(1 for x in v if x > 0) / len(v), 1)})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--pool-with", nargs="*", default=[])
    ap.add_argument("--horizon", default=HEADLINE, choices=HORIZONS)
    ap.add_argument("--floor", type=float, default=3.0)
    ap.add_argument("--reps", type=int, default=2000)
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    rows = build_rows(a.run)
    for extra in a.pool_with:
        rows += build_rows(extra)
    pending = [r["ticker"] for r in rows if r.get(a.horizon + "_pct") is None]

    doc = {
        "runs": [a.run] + list(a.pool_with),
        "horizon": a.horizon,
        "window": "close of the drop day -> " + {
            "open1": "the next open", "d1": "the next close",
            "d2": "two closes on", "d3": "three closes on", "d5": "five closes on",
            "d10": "ten closes on", "d21": "twenty-one closes on",
        }[a.horizon],
        "names": len(rows),
        "pending": pending,
        "lean_vs_free_control_rho": M.spearman(
            [r["priced_lean_pct"] for r in rows],
            [(-r["ret_d_pct"] if r["ret_d_pct"] is not None else None) for r in rows]),
        "lean_vs_free_control_note": "near 1.0 means the baseline's lean IS the free "
                                     "control and nothing built on it can beat the "
                                     "control. This is the stage J failure mode",
        "rankings": {h: rank_block(rows, h, a.reps) for h in HORIZONS},
        "conviction": {h: conviction_block(rows, h) for h in HORIZONS},
        "by_cause": by_cause(rows, a.horizon),
        "book": {f"cost_x{m}": book_block(rows, a.horizon, a.floor, m) for m in (0, 1, 2)},
        "rows": rows,
    }
    s = json.dumps(doc, indent=1)
    if a.out:
        Path(a.out).write_text(s)
    print(json.dumps({k: doc[k] for k in
                      ("names", "pending", "lean_vs_free_control_rho", "rankings",
                       "conviction", "by_cause")}, indent=1))
    if a.out:
        print(f"\nwrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()

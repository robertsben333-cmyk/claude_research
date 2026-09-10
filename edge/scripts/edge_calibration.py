#!/usr/bin/env python3
"""Is the SIZE of a prediction worth anything, or only its sign?

`edge_resolve.py` asks whether a day can be ranked. This asks the other question:
the hunt emits a signed number in points of spot, and a number claims more than an
ordering -- it claims a magnitude. Three things can be true of it and they are
independent:

  1. DIRECTION      does the sign come out right, and does it come out right more
                    often when the number is large
  2. CALIBRATION    is a prediction of +8 worth twice a prediction of +4, and is
                    either of them worth what it says
  3. DISCRIMINATION does a large prediction at least land on a name that MOVED,
                    even when the direction is wrong

A method can pass 1 and fail 2 badly -- that is the normal case for a forecaster
who is directionally useful and systematically overconfident -- and the fix for
each is different. Failing 2 while passing 1 means shrink the number and keep the
ranking. Failing 1 while passing 3 means the hunt finds volatility, not direction,
and belongs in an option, not a share.

Everything here runs off `edge/ledger/names.csv`, so run `edge_ledger.py` first.

    python3 edge/scripts/edge_calibration.py
    python3 edge/scripts/edge_calibration.py --json edge/analysis/edge-calibration.json

## What the numbers are compared against

A calibration figure alone means nothing -- an error of 6 points is good on a name
that moves 15 and hopeless on one that moves 2. Every error is therefore reported
beside three free predictors that cost no research at all:

    zero            predict no move. The honest null
    -run_up_20d     minus the 20-day run-up, the control that has beaten this
                    stage's own ranking on 6 of 6 days
    implied         the option straddle (or the reaction-history proxy where there
                    was no chain), signed with the hunt's own sign -- which asks
                    whether the hunt adds anything to a size the market published

## Two things this cannot do

It cannot separate the double-hunt regime from the single-hunt one on this sample.
Runs before 2026-09-09 gave the day's two highest-priority names two hunters, and
the key is a sum, so those names carry larger numbers by construction. `--split`
reports the two regimes separately; both are too small to conclude from.

And the sample repeats five events. ABM, UNFI, WDH, CAN and GMHS were hunted on
both 09-04 and 09-07 for the same 09-08 prints. The earlier hunt is kept, as
`edge_direction.py` does; `--keep-duplicates` shows what the double-count buys.
"""
import argparse
import csv
import json
import math
import random
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAMES = ROOT / "edge" / "ledger" / "names.csv"
REGIME_BREAK = "2026-09-09"          # first single-hunter run


def load(path, keep_dups=False):
    rows = []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        if r["resolved"] != "1" or not r["impact_sum"] or not r["move_pct"]:
            continue
        f = {k: (float(v) if v not in ("", None) else None) for k, v in r.items()
             if k in ("impact_sum", "move_pct", "runup_20d_pct", "implied_move_pct",
                      "conviction", "n_findings", "deadband_pct",
                      "hist_median_abs_move_pct", "dollar_vol_20d")}
        f.update({k: r[k] for k in ("event_date", "run_date", "ticker", "session",
                                    "implied_basis")})
        rows.append(f)
    if keep_dups:
        return rows
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: r["run_date"]):   # keep the earlier hunt
        k = (r["ticker"], r["event_date"], r["session"])
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out


# ---------------------------------------------------------------- statistics

def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r, i = [0.0] * len(xs), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return r


def spearman(xs, ys):
    if len(xs) < 3:
        return None
    rx, ry = ranks(xs), ranks(ys)
    mx, my = st.fmean(rx), st.fmean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return round(num / (dx * dy), 3) if dx and dy else None


def within_day_perm(rows, xf, yf, seed=7, trials=20000):
    """Shuffle y WITHIN each day. Across days, market-wide drift is shared by
    every name and a plain shuffle would credit the ranker with it."""
    days = defaultdict(list)
    for r in rows:
        days[r["event_date"]].append(r)
    days = [v for v in days.values() if len(v) >= 3]
    if not days:
        return None, None, 0
    xs = [xf(r) for d in days for r in d]
    ys = [yf(r) for d in days for r in d]
    obs = spearman(xs, ys)
    if obs is None:
        return None, None, len(xs)
    rnd, hits = random.Random(seed), 0
    for _ in range(trials):
        sh = []
        for d in days:
            v = [yf(r) for r in d]
            rnd.shuffle(v)
            sh.extend(v)
        s = spearman(xs, sh)
        if s is not None and abs(s) >= abs(obs):
            hits += 1
    return obs, round(hits / trials, 4), len(xs)


def binom_p(k, n, p=0.5):
    """Two-sided exact, so a 16-of-21 does not get read off a normal table."""
    if not n:
        return None
    c = [math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    return round(min(1.0, sum(x for x in c if x <= c[k] * 1.0000001)), 4)


def ols(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = st.fmean(xs), st.fmean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if not sxx:
        return None
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    se = (math.sqrt(ss_res / (n - 2) / sxx) if n > 2 and sxx else None)
    return {"slope": round(b, 3), "intercept": round(a, 3),
            "slope_se": round(se, 3) if se else None,
            "slope_t": round(b / se, 2) if se else None,
            "r2": round(1 - ss_res / ss_tot, 3) if ss_tot else None, "n": n}


def boot_mean(xs, seed=11, trials=5000):
    if not xs:
        return None
    rnd = random.Random(seed)
    ms = sorted(st.fmean(rnd.choices(xs, k=len(xs))) for _ in range(trials))
    return [round(ms[int(0.025 * trials)], 3), round(ms[int(0.975 * trials)], 3)]


# ---------------------------------------------------------------- the tests

def direction(rows):
    """Sign accuracy, overall and as a function of how big the call was."""
    live = [r for r in rows if r["impact_sum"] and r["move_pct"]]
    hit = [int((r["impact_sum"] > 0) == (r["move_pct"] > 0)) for r in live]
    out = {"n": len(live), "sign_correct": sum(hit),
           "rate": round(st.fmean(hit), 3) if hit else None,
           "binom_p": binom_p(sum(hit), len(hit))}
    rho, p, n = within_day_perm(
        live, lambda r: abs(r["impact_sum"]),
        lambda r: int((r["impact_sum"] > 0) == (r["move_pct"] > 0)))
    out["conviction_vs_sign"] = {"spearman": rho, "perm_p_within_day": p, "n": n}

    cuts, prev = {}, None
    for thr in (0, 1, 2, 3, 4, 5, 6, 8):
        sel = [r for r in live if abs(r["impact_sum"]) >= thr]
        if len(sel) < 5:
            continue
        h = [int((r["impact_sum"] > 0) == (r["move_pct"] > 0)) for r in sel]
        cuts[f">={thr}"] = {"n": len(sel), "correct": sum(h),
                            "rate": round(st.fmean(h), 3),
                            "binom_p": binom_p(sum(h), len(h)),
                            "mean_abs_move": round(st.fmean(
                                abs(r["move_pct"]) for r in sel), 2)}
        prev = thr
    out["by_threshold"] = cuts
    out["threshold_note"] = (
        "Eight nested cuts on one sample. The best of them is not a p-value; "
        f"treat the largest cut ({prev}) as the one that was pre-registered by "
        "config/pipeline.yaml's conviction_floor and the rest as description.")
    return out


def calibration(rows):
    """Is the number worth what it says, and worth more than a free number."""
    live = [r for r in rows if r["impact_sum"] is not None]
    xs = [r["impact_sum"] for r in live]
    ys = [r["move_pct"] for r in live]
    fit = ols(xs, ys) or {}
    fit["reading"] = (
        "slope 1.0 = the number means what it says; below 1 = overconfident in "
        "magnitude, the prediction should be shrunk toward zero by that factor; "
        "the intercept is a standing directional bias in points.")

    def err(pred):
        return [abs(p - r["move_pct"]) for p, r in zip(pred, live)]

    hunt = err(xs)
    zero = err([0.0] * len(live))
    ctrl = err([-(r["runup_20d_pct"] or 0.0) for r in live])
    imp = err([(r["implied_move_pct"] or 0.0)
               * (1 if r["impact_sum"] >= 0 else -1) for r in live])
    shrunk = err([x * (fit.get("slope") or 0.0) for x in xs])
    out = {"regression": fit, "n": len(live),
           "mean_abs_error_pts": {
               "hunt": round(st.fmean(hunt), 2),
               "hunt_shrunk_in_sample": round(st.fmean(shrunk), 2),
               "predict_zero": round(st.fmean(zero), 2),
               "minus_run_up_20d": round(st.fmean(ctrl), 2),
               "implied_move_with_hunt_sign": round(st.fmean(imp), 2)},
           "median_abs_error_pts": {
               "hunt": round(st.median(hunt), 2),
               "predict_zero": round(st.median(zero), 2)},
           "realised_move_sd_pts": round(st.pstdev(ys), 2),
           "hunt_minus_zero_error": {
               "mean_pts": round(st.fmean(h - z for h, z in zip(hunt, zero)), 2),
               "ci95": boot_mean([h - z for h, z in zip(hunt, zero)])},
           "shrink_note": (
               "hunt_shrunk_in_sample fits the shrink factor on the same rows it "
               "scores, so it is a lower bound on the error, not a forecast.")}
    return out


def discrimination(rows):
    """Does a big number at least land on a name that moved."""
    live = [r for r in rows if r["impact_sum"] is not None]
    rho_mag, p_mag, n = within_day_perm(
        live, lambda r: abs(r["impact_sum"]), lambda r: abs(r["move_pct"]))
    rho_dir, p_dir, _ = within_day_perm(
        live, lambda r: r["impact_sum"], lambda r: r["move_pct"])
    norm = [r for r in live if r["implied_move_pct"]]
    rho_norm, p_norm, n_norm = within_day_perm(
        norm, lambda r: abs(r["impact_sum"]),
        lambda r: abs(r["move_pct"]) / r["implied_move_pct"])
    buckets = defaultdict(list)
    for r in live:
        a = abs(r["impact_sum"])
        b = "<1" if a < 1 else ("1-3" if a < 3 else ("3-6" if a < 6 else ">=6"))
        buckets[b].append(r)
    return {
        "abs_pred_vs_abs_move": {"spearman": rho_mag, "perm_p": p_mag, "n": n},
        "abs_pred_vs_abs_move_over_implied": {
            "spearman": rho_norm, "perm_p": p_norm, "n": n_norm,
            "note": "37 straddles and 32 history proxies pooled; see edge_resolve."},
        "signed_pred_vs_signed_move": {"spearman": rho_dir, "perm_p": p_dir},
        "by_bucket": {k: {"n": len(v),
                          "mean_abs_pred": round(st.fmean(abs(r["impact_sum"])
                                                          for r in v), 2),
                          "mean_abs_move": round(st.fmean(abs(r["move_pct"])
                                                          for r in v), 2),
                          "sign_rate": round(st.fmean(
                              int((r["impact_sum"] > 0) == (r["move_pct"] > 0))
                              for r in v), 3)}
                      for k, v in sorted(buckets.items(),
                                         key=lambda kv: -len(kv[1]))}}


def report(rows, label):
    return {"label": label, "n_events": len(rows),
            "days": sorted({r["event_date"] for r in rows}),
            "direction": direction(rows),
            "calibration": calibration(rows),
            "discrimination": discrimination(rows)}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--names", default=str(NAMES))
    ap.add_argument("--json", help="write the full result here")
    ap.add_argument("--keep-duplicates", action="store_true")
    ap.add_argument("--split", action="store_true",
                    help="also report the two hunter regimes separately")
    a = ap.parse_args()

    rows = load(a.names, a.keep_duplicates)
    doc = {"source": a.names, "deduplicated": not a.keep_duplicates,
           "all": report(rows, "all events")}
    if a.split:
        doc["double_hunt_era"] = report(
            [r for r in rows if r["event_date"] < REGIME_BREAK], "before 2026-09-09")
        doc["single_hunt_era"] = report(
            [r for r in rows if r["event_date"] >= REGIME_BREAK], "2026-09-09 onward")

    print(json.dumps(doc, indent=2))
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(doc, indent=2))
    n = doc["all"]["n_events"]
    if n < 100:
        print(f"\nNOTE: {n} events over {len(doc['all']['days'])} days. Every "
              "interval here is wide enough to contain outcomes you would act on "
              "differently. Nothing below is a finding.", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()

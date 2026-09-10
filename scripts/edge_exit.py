#!/usr/bin/env python3
"""Does stage E's number predict the FIRST reaction better than the first session?

`edge_resolve.py` and `edge_trade.py` both measure one window: the regular close
before the print to the regular close after the first full session. That holds the
print through a whole session of trading. The hypothesis this script tests is that
the hunt's findings are about the *initial* repricing -- the after-hours or
pre-market print and the opening auction -- and that everything after it is other
people's news.

Entry is unchanged and not a choice: the close before the print, which is the last
price that exists before the hunt's 16:04 CET run. Only the exit moves.

Horizons, all in America/New_York, all measured against that same entry:

  ext_early   amc: the last 5m bar starting <=16:30 on the event date, i.e. about
              half an hour of after-hours trading. bmo: the last bar <=08:00 on the
              reaction session, i.e. the early pre-market print
  pre_open    the last extended bar before 09:30 on the reaction session -- the
              pre-market indication you could actually see before the auction
  open        the opening print of the reaction session (09:30 bar open)
  m15/m30/m60 the close 15, 30 and 60 minutes into the reaction session
  midday      12:00
  close       the regular close of the reaction session -- THE CURRENT BASELINE

Extended-hours bars carry no volume from this source, so a horizon before `open`
says what the price was, not that size could have traded there. Read `dollar_vol`
and the liquid subset before believing any of it.

Ten horizons over 38 events is a max-statistic problem. The best horizon's p is
therefore also reported family-wise, as the fraction of within-day shuffles whose
BEST horizon beats the observed best.

    python3 scripts/edge_exit.py --cache /tmp/bars
    python3 scripts/edge_exit.py --out docs/edge-exit.json
"""
import argparse
import json
import math
import os
import random
import statistics as st
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
YQ = "https://query1.finance.yahoo.com"
ET = timezone(timedelta(hours=-4))  # every event in this sample is EDT

# The 2026-09-04 run re-hunted five of the 2026-09-07 names for the same 09-08
# prints. Pooling both double-counts five events; the whole day is dropped.
DUP_RUN = "2026-09-04"

HORIZONS = ["ext_early", "pre_open", "open", "m15", "m30", "m60", "midday", "close"]


# ---------------------------------------------------------------- price plumbing

def _get(url, cache=None, tag=None):
    if cache and tag:
        p = Path(cache) / tag
        if p.exists():
            return json.loads(p.read_text())
    for attempt in range(4):
        try:
            j = json.loads(urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": UA}),
                timeout=40).read())
            break
        except Exception as e:
            if attempt == 3:
                return {"_error": f"{type(e).__name__}: {e}"}
            time.sleep(2 ** attempt)
    if cache and tag:
        Path(cache).mkdir(parents=True, exist_ok=True)
        (Path(cache) / tag).write_text(json.dumps(j))
    return j


def daily(ticker, cache=None):
    j = _get(f"{YQ}/v8/finance/chart/{ticker}?range=90d&interval=1d",
             cache, f"{ticker}.d.json")
    if j.get("_error") or not (j.get("chart") or {}).get("result"):
        return None
    r = j["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    out = {}
    for i, ts in enumerate(r["timestamp"]):
        if q["close"][i] is None:
            continue
        d = datetime.fromtimestamp(ts, ET).date().isoformat()
        out[d] = {"open": q["open"][i], "close": q["close"][i]}
    return out


def intraday(ticker, cache=None):
    j = _get(f"{YQ}/v8/finance/chart/{ticker}?range=45d&interval=5m&includePrePost=true",
             cache, f"{ticker}.m5.json")
    if j.get("_error") or not (j.get("chart") or {}).get("result"):
        return {}
    r = j["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    bars = {}
    for i, ts in enumerate(r["timestamp"]):
        o, c = q["open"][i], q["close"][i]
        if c is None and o is None:
            continue
        d = datetime.fromtimestamp(ts, ET)
        bars.setdefault(d.date().isoformat(), []).append(
            {"hm": d.hour * 60 + d.minute, "open": o, "close": c if c is not None else o})
    return bars


def _last_at_or_before(day_bars, hm_max, hm_min=None):
    v = [b for b in day_bars if b["hm"] <= hm_max and (hm_min is None or b["hm"] >= hm_min)]
    return v[-1]["close"] if v else None


def _bar_starting(day_bars, hm):
    for b in day_bars:
        if b["hm"] == hm:
            return b
    return None


# Hours since the entry close (16:00 ET on the entry day). One axis both sessions
# share: 17.5 is the reaction session's open and 24.0 its close. Offsets 5-11 are
# the overnight void -- the last price still exists there but no exit does, so the
# grid skips it.
HOUR_GRID = [1.0, 2.0, 3.0, 4.0,
             12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 17.5,
             18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0]


def hourly_prices(m5, entry_date, react_date):
    """Price at each grid hour: the last bar at or before it, within one hour.

    The staleness window is what keeps a name that stopped trading at 16:20 from
    reporting an 'exit' at 19:00 that nobody could have taken.
    """
    def offs(date, base_day_offset):
        out = []
        for b in m5.get(date, []):
            out.append(((b["hm"] - 16 * 60) / 60.0 + base_day_offset, b["close"]))
        return out
    series = sorted(offs(entry_date, 0.0) + offs(react_date, 24.0))
    px = {}
    for h in HOUR_GRID:
        v = [(o, c) for o, c in series if 0 < o <= h and o >= h - 1.0]
        px[h] = v[-1][1] if v else None
    return px


def exit_prices(ticker, event_date, session, cache=None):
    """Entry close plus one price per horizon. Missing horizons come back None."""
    dd = daily(ticker, cache)
    if not dd:
        return None, "daily bars unavailable"
    dates = sorted(dd)
    if session == "amc":
        before = [d for d in dates if d <= event_date]
        after = [d for d in dates if d > event_date]
    else:
        before = [d for d in dates if d < event_date]
        after = [d for d in dates if d >= event_date]
    if not before or not after:
        return None, "outcome window has not closed yet"
    entry_date, react = before[-1], after[0]
    entry = dd[entry_date]["close"]

    m5 = intraday(ticker, cache)
    react_bars = m5.get(react, [])
    px = {"close": dd[react]["close"], "open": dd[react]["open"]}
    ob = _bar_starting(react_bars, 9 * 60 + 30)
    if ob and ob["open"]:
        px["open"] = ob["open"]          # prefer the 09:30 bar's own print
    if session == "amc":
        px["ext_early"] = _last_at_or_before(m5.get(event_date, []), 16 * 60 + 30,
                                             16 * 60 + 5)
    else:
        px["ext_early"] = _last_at_or_before(react_bars, 8 * 60, 4 * 60)
    px["pre_open"] = _last_at_or_before(react_bars, 9 * 60 + 25, 4 * 60)
    for lab, hm in (("m15", 9 * 60 + 40), ("m30", 9 * 60 + 55),
                    ("m60", 10 * 60 + 25), ("midday", 11 * 60 + 55)):
        b = _bar_starting(react_bars, hm)
        px[lab] = b["close"] if b else None
    hp = hourly_prices(m5, entry_date, react)
    return {"entry_date": entry_date, "entry_close": round(entry, 4),
            "reaction_date": react,
            "hourly_move": {f"{h:g}": (None if hp[h] is None
                                       else round((hp[h] / entry - 1) * 100, 3))
                            for h in HOUR_GRID},
            "px": {k: (None if v is None else round(v, 4)) for k, v in px.items()},
            "move": {k: (None if v is None else round((v / entry - 1) * 100, 3))
                     for k, v in px.items()}}, None


# ------------------------------------------------------------------- statistics

def _ranks(xs):
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


def _corr(a, b):
    ma, mb = st.fmean(a), st.fmean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    dx = math.sqrt(sum((x - ma) ** 2 for x in a))
    dy = math.sqrt(sum((y - mb) ** 2 for y in b))
    return (num / (dx * dy)) if dx and dy else None


def _centred(xs):
    r = _ranks(xs)
    m = st.fmean(r)
    return [x - m for x in r]


def pooled_rho(days, xkey, ykey):
    """Within-day ranks, centred, correlated across days. Same as edge_resolve."""
    A, B = [], []
    for day in days:
        v = [r for r in day if r.get(xkey) is not None and r.get(ykey) is not None]
        if len(v) < 3:
            continue
        A += _centred([r[xkey] for r in v])
        B += _centred([r[ykey] for r in v])
    if len(A) < 3:
        return None, 0
    c = _corr(A, B)
    return (None if c is None else round(c, 3)), len(A)


def conviction_rho(rows, xkey, ykey):
    """Does the rank of |prediction| predict whether its sign was right?"""
    v = [r for r in rows if r.get(xkey) not in (None, 0) and r.get(ykey) is not None]
    if len(v) < 4:
        return None, 0
    a = _ranks([abs(r[xkey]) for r in v])
    b = [1.0 if (r[xkey] > 0) == (r[ykey] > 0) else 0.0 for r in v]
    c = _corr(a, b)
    return (None if c is None else round(c, 3)), len(v)


def ttest_mean(xs):
    if len(xs) < 3:
        return None, None, None
    m, s = st.fmean(xs), st.stdev(xs)
    se = s / math.sqrt(len(xs))
    if not se:
        return round(m, 3), None, None
    t = m / se
    half = 1.96 * se
    return round(m, 3), round(t, 2), [round(m - half, 2), round(m + half, 2)]


def ls_third(day, key, movekey):
    v = sorted([r for r in day if r.get(key) is not None and r.get(movekey) is not None],
               key=lambda r: -r[key])
    if len(v) < 3:
        return None
    k = max(1, len(v) // 3)
    # One unit of capital split over the two sides, as in edge_trade.py.
    return (st.fmean(r[movekey] for r in v[:k]) - st.fmean(r[movekey] for r in v[-k:])) / 2


def horizon_stats(days, movekey, seed, floor=3.0):
    flat = [r for d in days for r in d
            if r.get("impact_sum") is not None and r.get(movekey) is not None]
    out = {"n": len(flat)}
    if len(flat) < 4:
        return out
    rho, npairs = pooled_rho(days, "impact_sum", movekey)
    out["rho_impact_sum"] = rho
    crho, cn = conviction_rho(flat, "impact_sum", movekey)
    out["rho_conviction_vs_sign"] = crho
    ctl, _ = pooled_rho(days, "neg_runup", movekey)
    out["rho_control_neg_runup"] = ctl

    hits = [1 for r in flat if (r["impact_sum"] > 0) == (r[movekey] > 0)]
    out["sign_hit_rate"] = round(len(hits) / len(flat) * 100, 1)
    med = st.median([abs(r["impact_sum"]) for r in flat])
    hi = [r for r in flat if abs(r["impact_sum"]) >= med]
    lo = [r for r in flat if abs(r["impact_sum"]) < med]
    for lab, grp in (("above_median", hi), ("below_median", lo)):
        if grp:
            out[f"sign_hit_{lab}"] = round(
                sum(1 for r in grp if (r["impact_sum"] > 0) == (r[movekey] > 0))
                / len(grp) * 100, 1)

    conv = [r for r in flat if abs(r["impact_sum"]) >= floor]
    if conv:
        rets = [r[movekey] if r["impact_sum"] > 0 else -r[movekey] for r in conv]
        m, t, ci = ttest_mean(rets)
        out["floor_n"] = len(conv)
        out["floor_hits"] = sum(1 for x in rets if x > 0)
        out["floor_mean_ret_pct"] = m
        out["floor_t"] = t
        out["floor_ci95"] = ci

    ls = [x for x in (ls_third(d, "impact_sum", movekey) for d in days) if x is not None]
    if ls:
        m, t, ci = ttest_mean(ls)
        out["ls_third_mean_day_pct"] = m
        out["ls_third_t"] = t
        out["ls_third_positive_days"] = f"{sum(1 for x in ls if x > 0)}/{len(ls)}"
    shorts = [-st.fmean(r[movekey] for r in d if r.get(movekey) is not None)
              for d in days if any(r.get(movekey) is not None for r in d)]
    if shorts:
        out["null_always_short_day_pct"] = round(st.fmean(shorts), 3)
    out["realised_move_sd"] = round(st.pstdev([r[movekey] for r in flat]), 2)
    out["mean_abs_move_pct"] = round(st.fmean(abs(r[movekey]) for r in flat), 2)
    # How much of the eventual first-session move already exists here. A horizon
    # whose ranking looks weak because nothing has happened yet is a different
    # problem from one whose ranking is wrong.
    comp = [r[movekey] / r["mv_close"] for r in flat
            if r.get("mv_close") not in (None, 0) and abs(r["mv_close"]) >= 1.0]
    if len(comp) >= 4:
        out["median_frac_of_close_move"] = round(st.median(comp), 3)
    return out


def permute_within_days(days, movekeys, seed, trials=5000):
    """Two p-values per horizon plus the family-wise p of the best horizon.

    Shuffling the outcome within a day keeps the day structure and destroys only the
    pairing, which is the null the ranking claim is against.
    """
    rnd = random.Random(seed)
    obs_rho, obs_conv = {}, {}
    for k in movekeys:
        obs_rho[k] = pooled_rho(days, "impact_sum", k)[0]
        obs_conv[k] = conviction_rho([r for d in days for r in d], "impact_sum", k)[0]
    hit_rho = {k: 0 for k in movekeys}
    hit_conv = {k: 0 for k in movekeys}
    best_rho = max((abs(v) for v in obs_rho.values() if v is not None), default=None)
    best_conv = max((abs(v) for v in obs_conv.values() if v is not None), default=None)
    fw_rho = fw_conv = 0
    for _ in range(trials):
        perm = []
        for day in days:
            idx = list(range(len(day)))
            rnd.shuffle(idx)
            perm.append([{**day[i], **{k: day[j].get(k) for k in movekeys}}
                         for i, j in zip(range(len(day)), idx)])
        flat = [r for d in perm for r in d]
        mr = mc = 0.0
        for k in movekeys:
            s = pooled_rho(perm, "impact_sum", k)[0]
            if s is not None and obs_rho[k] is not None and abs(s) >= abs(obs_rho[k]):
                hit_rho[k] += 1
            if s is not None:
                mr = max(mr, abs(s))
            c = conviction_rho(flat, "impact_sum", k)[0]
            if c is not None and obs_conv[k] is not None and abs(c) >= abs(obs_conv[k]):
                hit_conv[k] += 1
            if c is not None:
                mc = max(mc, abs(c))
        if best_rho is not None and mr >= best_rho:
            fw_rho += 1
        if best_conv is not None and mc >= best_conv:
            fw_conv += 1
    return ({k: round(hit_rho[k] / trials, 4) for k in movekeys},
            {k: round(hit_conv[k] / trials, 4) for k in movekeys},
            round(fw_rho / trials, 4), round(fw_conv / trials, 4))


def add_legs(panel):
    """Returns of the individual legs, so the question becomes what each leg pays.

    `leg_intraday` is the whole hypothesis in one column: if the hunt's number does
    not rank the open-to-close leg, everything it knows is in the gap and holding
    through the session is uncompensated exposure.
    """
    for day in panel:
        for r in day:
            e, px = r["entry_close"], r["px"]
            o, c, pre = px.get("open"), px.get("close"), px.get("pre_open")
            r["leg_gap"] = None if (o is None) else round((o / e - 1) * 100, 3)
            r["leg_intraday"] = None if (o in (None, 0) or c is None) else \
                round((c / o - 1) * 100, 3)
            r["leg_overnight_to_preopen"] = None if pre is None else \
                round((pre / e - 1) * 100, 3)
            r["leg_preopen_to_close"] = None if (pre in (None, 0) or c is None) else \
                round((c / pre - 1) * 100, 3)
    return panel


LEGS = ["leg_gap", "leg_intraday", "leg_overnight_to_preopen", "leg_preopen_to_close"]


def demean_legs(panel):
    """Subtract the day's own mean from each leg.

    A book that happens to be short-heavy earns the day's average drift for free.
    On this sample the amc floor book is six long and six short, so its intraday
    loss is not drift; the bmo book is eight short and two long, so half of its
    intraday gain is.
    """
    for day in panel:
        for leg in LEGS:
            v = [r[leg] for r in day if r.get(leg) is not None]
            if not v:
                continue
            m = st.fmean(v)
            for r in day:
                if r.get(leg) is not None:
                    r[leg + "_dm"] = round(r[leg] - m, 3)
    return panel


POLICIES = {
    "uniform_close": {"amc": "mv_close", "bmo": "mv_close"},
    "uniform_open": {"amc": "mv_open", "bmo": "mv_open"},
    "uniform_pre_open": {"amc": "mv_pre_open", "bmo": "mv_pre_open"},
    "uniform_ext_early": {"amc": "mv_ext_early", "bmo": "mv_ext_early"},
    "amc_open_bmo_close": {"amc": "mv_open", "bmo": "mv_close"},
    "amc_pre_open_bmo_close": {"amc": "mv_pre_open", "bmo": "mv_close"},
}


def policy_stats(panel, floor):
    """One exit rule per session, so amc and bmo can be given different answers."""
    out = {}
    for name, rule in POLICIES.items():
        for day in panel:
            for r in day:
                r["_pol"] = r.get(rule[r["session"]])
        rho, _ = pooled_rho(panel, "impact_sum", "_pol")
        flat = [r for d in panel for r in d if r.get("_pol") is not None]
        conv = [r for r in flat if abs(r["impact_sum"]) >= floor]
        rets = [r["_pol"] if r["impact_sum"] > 0 else -r["_pol"] for r in conv]
        m, t, ci = ttest_mean(rets) if len(rets) > 2 else (None, None, None)
        ls = [x for x in (ls_third(d, "impact_sum", "_pol") for d in panel)
              if x is not None]
        lm, lt, lci = ttest_mean(ls) if len(ls) > 2 else (None, None, None)
        out[name] = {"n": len(flat), "rho_impact_sum": rho,
                     "floor_n": len(rets),
                     "floor_hits": sum(1 for x in rets if x > 0),
                     "floor_mean_ret_pct": m, "floor_t": t, "floor_ci95": ci,
                     "ls_third_mean_day_pct": lm,
                     "ls_third_positive_days": f"{sum(1 for x in ls if x > 0)}/{len(ls)}"}
    for day in panel:
        for r in day:
            r.pop("_pol", None)
    return out


def leg_stats(panel, floor):
    out = {}
    for leg in LEGS + [x + "_dm" for x in LEGS]:
        flat = [r for d in panel for r in d
                if r.get(leg) is not None and r.get("impact_sum") is not None]
        if len(flat) < 4:
            continue
        rho, _ = pooled_rho(panel, "impact_sum", leg)
        conv = [r for r in flat if abs(r["impact_sum"]) >= floor]
        rets = [r[leg] if r["impact_sum"] > 0 else -r[leg] for r in conv]
        m, t, ci = ttest_mean(rets) if rets else (None, None, None)
        out[leg] = {"n": len(flat), "rho_impact_sum": rho,
                    "floor_n": len(conv), "floor_mean_ret_pct": m, "floor_t": t,
                    "floor_ci95": ci,
                    "mean_abs_move_pct": round(st.fmean(abs(r[leg]) for r in flat), 2)}
    return out


def returns_table(panel, floor, costs):
    """The same horizons priced as money rather than as rank correlation.

    Three books, all one unit of capital, all entered at the same close:

      floor       every name with |impact_sum| >= floor, signed by the prediction.
                  Per-trade, because the number of trades varies by day
      ls_third    long the top third of the day, short the bottom third, capital
                  split over the two sides. Per day, and compounded over the days
      controls    `always_short` (no research) and `-run_up_20d` (one sealed number),
                  both traded at the SAME horizon, because the horizon moves them too

    Costs are a flat charge per unit of capital per round trip, applied alike. An
    exit before the opening auction deserves a HIGHER charge than the close does and
    gets the same one here, so the early-exit rows are flattered by this column.
    """
    out = {}
    for h in HORIZONS:
        mk = f"mv_{h}"
        flat = [r for d in panel for r in d if r.get(mk) is not None]
        conv = [r for r in flat if abs(r["impact_sum"]) >= floor]
        rets = [r[mk] if r["impact_sum"] > 0 else -r[mk] for r in conv]
        m, t, ci = ttest_mean(rets) if len(rets) > 2 else (None, None, None)

        per_day, short_day, ctl_day = [], [], []
        for day in panel:
            v = [r for r in day if r.get(mk) is not None]
            if len(v) < 3:
                continue
            x = ls_third(v, "impact_sum", mk)
            if x is not None:
                per_day.append(x)
            short_day.append(-st.fmean(r[mk] for r in v))
            c = [r for r in v if r.get("neg_runup") is not None]
            if len(c) >= 3:
                y = ls_third(c, "neg_runup", mk)
                if y is not None:
                    ctl_day.append(y)

        def compound(xs, cost=0.0):
            eq = 1.0
            for x in xs:
                eq *= (1 + (x - cost) / 100)
            return round((eq - 1) * 100, 2)

        row = {"n": len(flat), "floor_n": len(rets),
               "floor_hits": sum(1 for x in rets if x > 0),
               "floor_mean_ret_pct": m, "floor_t": t, "floor_ci95": ci,
               "floor_median_ret_pct": (round(st.median(rets), 2) if rets else None),
               "floor_worst_pct": (round(min(rets), 2) if rets else None),
               "floor_best_pct": (round(max(rets), 2) if rets else None),
               "ls_third_mean_day_pct": (round(st.fmean(per_day), 3) if per_day else None),
               "ls_third_days": f"{sum(1 for x in per_day if x > 0)}/{len(per_day)}",
               "ls_third_cumulative_pct": compound(per_day),
               "null_always_short_day_pct": (round(st.fmean(short_day), 3)
                                             if short_day else None),
               "null_always_short_cumulative_pct": compound(short_day),
               "control_neg_runup_day_pct": (round(st.fmean(ctl_day), 3)
                                             if ctl_day else None),
               "control_neg_runup_cumulative_pct": compound(ctl_day)}
        for c in costs:
            row[f"floor_mean_after_{c}pct_cost"] = (None if m is None
                                                    else round(m - c, 2))
            row[f"ls_third_cumulative_after_{c}pct_cost"] = compound(per_day, c)
        out[h] = row
    return out


def policy_returns(panel, floor, costs):
    """Per-session exit rules, priced. Same three books, same costs."""
    out = {}
    for name, rule in POLICIES.items():
        for day in panel:
            for r in day:
                r["_pol"] = r.get(rule[r["session"]])
        flat = [r for d in panel for r in d if r.get("_pol") is not None]
        conv = [r for r in flat if abs(r["impact_sum"]) >= floor]
        rets = [r["_pol"] if r["impact_sum"] > 0 else -r["_pol"] for r in conv]
        m, t, ci = ttest_mean(rets) if len(rets) > 2 else (None, None, None)
        per_day, short_day = [], []
        for day in panel:
            v = [r for r in day if r.get("_pol") is not None]
            if len(v) < 3:
                continue
            x = ls_third(v, "impact_sum", "_pol")
            if x is not None:
                per_day.append(x)
            short_day.append(-st.fmean(r["_pol"] for r in v))

        def compound(xs, cost=0.0):
            eq = 1.0
            for x in xs:
                eq *= (1 + (x - cost) / 100)
            return round((eq - 1) * 100, 2)

        row = {"floor_n": len(rets), "floor_hits": sum(1 for x in rets if x > 0),
               "floor_mean_ret_pct": m, "floor_t": t, "floor_ci95": ci,
               "ls_third_mean_day_pct": (round(st.fmean(per_day), 3) if per_day else None),
               "ls_third_days": f"{sum(1 for x in per_day if x > 0)}/{len(per_day)}",
               "ls_third_cumulative_pct": compound(per_day),
               "null_always_short_day_pct": (round(st.fmean(short_day), 3)
                                             if short_day else None),
               "per_day_pct": [round(x, 2) for x in per_day]}
        for c in costs:
            row[f"floor_mean_after_{c}pct_cost"] = (None if m is None
                                                    else round(m - c, 2))
            row[f"ls_third_cumulative_after_{c}pct_cost"] = compound(per_day, c)
        out[name] = row
    for day in panel:
        for r in day:
            r.pop("_pol", None)
    return out


def session_returns(panel, floor):
    """Per-trade return of the floor book by session and by exit, in points."""
    out = {}
    for sess in ("amc", "bmo"):
        sub = [[r for r in d if r["session"] == sess] for d in panel]
        sub = [d for d in sub if d]
        row = {}
        for h in HORIZONS:
            mk = f"mv_{h}"
            conv = [r for d in sub for r in d
                    if r.get(mk) is not None and abs(r["impact_sum"]) >= floor]
            rets = [r[mk] if r["impact_sum"] > 0 else -r[mk] for r in conv]
            m, t, ci = ttest_mean(rets) if len(rets) > 2 else (None, None, None)
            row[h] = {"n": len(rets), "hits": sum(1 for x in rets if x > 0),
                      "mean_ret_pct": m, "t": t, "ci95": ci}
        out[sess] = row
    return out


def hourly_returns(panel, floor):
    """Per-trade return of the floor book at every grid hour, all names and by session.

    This is the shape of the answer: where on the clock the money is, and whether the
    two sessions put it in the same place.
    """
    def book(rows, key):
        conv = [r for r in rows if r.get(key) is not None
                and abs(r["impact_sum"]) >= floor]
        rets = [r[key] if r["impact_sum"] > 0 else -r[key] for r in conv]
        if len(rets) < 3:
            return {"n": len(rets), "mean_ret_pct": None, "t": None,
                    "hits": sum(1 for x in rets if x > 0), "coverage": len(conv)}
        m, t, ci = ttest_mean(rets)
        return {"n": len(rets), "hits": sum(1 for x in rets if x > 0),
                "mean_ret_pct": m, "t": t, "ci95": ci, "coverage": len(conv)}

    flat = [r for d in panel for r in d]
    out = {"grid_hours": HOUR_GRID, "all": {}, "amc": {}, "bmo": {},
           "ls_third_day_pct": {}, "null_always_short_day_pct": {},
           "names_priced": {}}
    for h in HOUR_GRID:
        k = f"hr_{h:g}"
        out["all"][f"{h:g}"] = book(flat, k)
        for sess in ("amc", "bmo"):
            out[sess][f"{h:g}"] = book([r for r in flat if r["session"] == sess], k)
        per_day, short_day = [], []
        for day in panel:
            v = [r for r in day if r.get(k) is not None]
            if len(v) < 3:
                continue
            x = ls_third(v, "impact_sum", k)
            if x is not None:
                per_day.append(x)
            short_day.append(-st.fmean(r[k] for r in v))
        out["ls_third_day_pct"][f"{h:g}"] = (round(st.fmean(per_day), 3)
                                             if per_day else None)
        out["null_always_short_day_pct"][f"{h:g}"] = (round(st.fmean(short_day), 3)
                                                      if short_day else None)
        out["names_priced"][f"{h:g}"] = sum(1 for r in flat if r.get(k) is not None)
    return out


def bootstrap_policies(panel, floor, seed, trials=4000):
    """Paired day bootstrap of each policy minus `uniform_close`, and the family-wise
    story: `amc_open_bmo_close` is the BEST OF SIX policies and the split that
    suggested it came from these same 38 events. `frac_gt_0` is therefore a
    description of the sample, not a p-value, and `best_of_six_frac_gt_0` says how
    often the best of the six beats the close under resampling, which is the closest
    thing here to an honest selection-aware number."""
    rnd = random.Random(seed + 7)
    days = [d for d in panel if d]
    names = [n for n in POLICIES if n != "uniform_close"]
    diffs = {n: [] for n in names}
    best = []

    def book(sample, rule):
        rets = []
        for day in sample:
            for r in day:
                v = r.get(rule[r["session"]])
                if v is None or abs(r["impact_sum"]) < floor:
                    continue
                rets.append(v if r["impact_sum"] > 0 else -v)
        return st.fmean(rets) if rets else None

    for _ in range(trials):
        samp = [days[rnd.randrange(len(days))] for _ in days]
        base = book(samp, POLICIES["uniform_close"])
        if base is None:
            continue
        this = []
        for n in names:
            v = book(samp, POLICIES[n])
            if v is not None:
                diffs[n].append(v - base)
                this.append(v - base)
        if this:
            best.append(max(this))

    def blk(v):
        if len(v) < 100:
            return None
        v = sorted(v)
        return {"mean": round(st.fmean(v), 3),
                "ci95": [round(v[int(.025 * len(v))], 3), round(v[int(.975 * len(v))], 3)],
                "frac_gt_0": round(sum(1 for x in v if x > 0) / len(v), 3)}

    out = {n: blk(diffs[n]) for n in names}
    b = blk(best)
    out["best_of_six_frac_gt_0"] = None if b is None else b["frac_gt_0"]
    return out


def bootstrap_vs_close(panel, floor, seed, trials=4000):
    """Paired over days: is any horizon actually different from holding to the close?

    Resampling days rather than events keeps a day's names together, which is the
    only unit here that is plausibly independent.
    """
    rnd = random.Random(seed + 1)
    days = [d for d in panel if len(d) >= 3]
    res = {}
    for h in HORIZONS:
        if h == "close":
            continue
        mk = f"mv_{h}"
        d_rho, d_floor = [], []
        for _ in range(trials):
            samp = [days[rnd.randrange(len(days))] for _ in days]
            a = pooled_rho(samp, "impact_sum", mk)[0]
            b = pooled_rho(samp, "impact_sum", "mv_close")[0]
            if a is not None and b is not None:
                d_rho.append(a - b)
            flat = [r for dd in samp for r in dd if abs(r.get("impact_sum") or 0) >= floor]
            ra = [r[mk] if r["impact_sum"] > 0 else -r[mk] for r in flat
                  if r.get(mk) is not None]
            rb = [r["mv_close"] if r["impact_sum"] > 0 else -r["mv_close"] for r in flat
                  if r.get("mv_close") is not None]
            if ra and rb:
                d_floor.append(st.fmean(ra) - st.fmean(rb))
        def blk(v):
            if len(v) < 100:
                return None
            v = sorted(v)
            return {"mean": round(st.fmean(v), 3),
                    "ci95": [round(v[int(.025 * len(v))], 3),
                             round(v[int(.975 * len(v))], 3)],
                    "frac_gt_0": round(sum(1 for x in v if x > 0) / len(v), 3)}
        res[h] = {"delta_rho_vs_close": blk(d_rho),
                  "delta_floor_ret_vs_close": blk(d_floor)}
    return res


# ------------------------------------------------------------------------ panel

def build_panel(cache, keep_dup):
    rows_by_day = json.loads((ROOT / "docs" / "edge-rows.json").read_text())
    panel, problems = [], []
    for day in rows_by_day:
        run = day[0]["run"]
        if not keep_dup and DUP_RUN in run:
            continue
        base_dir = ROOT / run / "baselines"
        out = []
        for r in day:
            t = r["t"]
            bf = base_dir / f"{t}.json"
            if not bf.exists():
                problems.append(f"{run} {t}: no baseline file")
                continue
            b = json.loads(bf.read_text())
            if not b.get("event_date"):
                problems.append(f"{run} {t}: baseline has no event_date")
                continue
            res, err = exit_prices(t, b["event_date"], b.get("session", "bmo"), cache)
            if err:
                problems.append(f"{run} {t}: {err}")
                continue
            row = {"run": run, "ticker": t, "session": b.get("session", "bmo"),
                   "event_date": b["event_date"], "reaction_date": res["reaction_date"],
                   "entry_date": res["entry_date"], "entry_close": res["entry_close"],
                   "impact_sum": r["impact_sum"], "edge_score": r["escore"],
                   "neg_runup": (None if r.get("runup") is None else -r["runup"]),
                   "dollar_vol": r.get("dollar_vol"),
                   "baseline_move_close": r["move"],
                   "px": res["px"]}
            for h in HORIZONS:
                row[f"mv_{h}"] = res["move"].get(h)
            row["hourly_move"] = res["hourly_move"]
            for k, v in res["hourly_move"].items():
                row[f"hr_{k}"] = v
            out.append(row)
        if out:
            panel.append(out)
    return panel, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", help="directory of cached Yahoo chart JSON")
    ap.add_argument("--out", default="docs/edge-exit.json")
    ap.add_argument("--seed", type=int, default=20260910)
    ap.add_argument("--trials", type=int, default=5000)
    ap.add_argument("--floor", type=float, default=3.0,
                    help="conviction floor on |impact_sum|, in points")
    ap.add_argument("--min-dollar-vol", type=float, default=5e6)
    ap.add_argument("--keep-duplicate-day", action="store_true",
                    help="keep the 2026-09-04 re-hunt; double-counts five events")
    a = ap.parse_args()

    panel, problems = build_panel(a.cache, a.keep_duplicate_day)
    panel = demean_legs(add_legs(panel))
    movekeys = [f"mv_{h}" for h in HORIZONS]
    n_all = sum(len(d) for d in panel)
    print(f"{n_all} events over {len(panel)} days"
          f"{' (duplicate day kept)' if a.keep_duplicate_day else ''}")
    for p in problems:
        print("  !", p)

    coverage = {h: sum(1 for d in panel for r in d if r.get(f"mv_{h}") is not None)
                for h in HORIZONS}
    print("\ncoverage:", " ".join(f"{h}={coverage[h]}" for h in HORIZONS))

    stats = {h: horizon_stats(panel, f"mv_{h}", a.seed, a.floor) for h in HORIZONS}
    p_rho, p_conv, fw_rho, fw_conv = permute_within_days(panel, movekeys, a.seed,
                                                         a.trials)
    for h in HORIZONS:
        stats[h]["p_rho"] = p_rho[f"mv_{h}"]
        stats[h]["p_conviction"] = p_conv[f"mv_{h}"]

    liquid = [[r for r in d if (r.get("dollar_vol") or 0) >= a.min_dollar_vol]
              for d in panel]
    liquid = [d for d in liquid if len(d) >= 3]
    lstats = {h: horizon_stats(liquid, f"mv_{h}", a.seed, a.floor) for h in HORIZONS}

    def table(title, s, keys):
        print(f"\n{title}")
        print("  horizon    " + "".join(f"{k:>14}" for k in keys))
        for h in HORIZONS:
            cells = "".join(f"{('' if s[h].get(k) is None else s[h][k]):>14}"
                            for k in keys)
            print(f"  {h:<10}" + cells)

    table("ranking (impact_sum, within-day pooled)",
          stats, ["n", "rho_impact_sum", "p_rho", "rho_control_neg_runup"])
    table("direction (conviction test and sign accuracy)",
          stats, ["rho_conviction_vs_sign", "p_conviction", "sign_hit_rate",
                  "sign_hit_above_median", "sign_hit_below_median"])
    table(f"traded (floor |impact_sum|>={a.floor}, and long/short thirds)",
          stats, ["floor_n", "floor_hits", "floor_mean_ret_pct", "floor_t",
                  "ls_third_mean_day_pct", "null_always_short_day_pct"])
    table("how much of the move has happened yet",
          stats, ["mean_abs_move_pct", "median_frac_of_close_move",
                  "realised_move_sd"])
    table(f"liquid only (>=${a.min_dollar_vol:,.0f}/day)",
          lstats, ["n", "rho_impact_sum", "rho_conviction_vs_sign",
                   "floor_n", "floor_mean_ret_pct", "realised_move_sd"])

    legs = leg_stats(panel, a.floor)
    print("\nlegs (what each leg of the hold pays)")
    print("  leg                        " + "".join(
        f"{k:>14}" for k in ["n", "rho_impact_sum", "floor_mean_ret_pct", "floor_t",
                             "mean_abs_move_pct"]))
    for leg, v in legs.items():
        print(f"  {leg:<26}" + "".join(
            f"{('' if v.get(k) is None else v[k]):>14}"
            for k in ["n", "rho_impact_sum", "floor_mean_ret_pct", "floor_t",
                      "mean_abs_move_pct"]))

    by_session = {}
    for sess in ("amc", "bmo"):
        sub = [[r for r in d if r["session"] == sess] for d in panel]
        sub = [d for d in sub if d]
        by_session[sess] = {
            "events": sum(len(d) for d in sub),
            "horizons": {h: horizon_stats(sub, f"mv_{h}", a.seed, a.floor)
                         for h in HORIZONS},
            "legs": leg_stats(sub, a.floor)}
    print("\nby session (the question was whether amc and bmo want different exits)")
    for sess, v in by_session.items():
        print(f"  {sess}  n={v['events']}")
        for leg, lv in v["legs"].items():
            print(f"    {leg:<26}rho={('' if lv['rho_impact_sum'] is None else lv['rho_impact_sum']):>7}"
                  f"  floor_ret={('' if lv['floor_mean_ret_pct'] is None else lv['floor_mean_ret_pct']):>7}"
                  f"  (n={lv['floor_n']})  mean|mv|={lv['mean_abs_move_pct']}")
        for h in ("ext_early", "pre_open", "open", "close"):
            hv = v["horizons"][h]
            print(f"    {h:<26}rho={('' if hv.get('rho_impact_sum') is None else hv['rho_impact_sum']):>7}"
                  f"  floor_ret={('' if hv.get('floor_mean_ret_pct') is None else hv['floor_mean_ret_pct']):>7}"
                  f"  frac_of_close={hv.get('median_frac_of_close_move')}"
                  f"  null_short={hv.get('null_always_short_day_pct')}")

    costs = [0.5, 1.5, 3.0]
    rt = returns_table(panel, a.floor, costs)
    print("\nRETURNS by exit horizon -- floor book is per trade, the rest per day")
    print(f"  {'horizon':<12}{'trades':>7}{'hits':>6}{'per_trade':>11}{'t':>7}"
          f"{'ls/day':>9}{'ls_cum':>9}{'days+':>7}{'short/day':>11}{'runup/day':>11}")
    for h in HORIZONS:
        v = rt[h]
        print(f"  {h:<12}{v['floor_n']:>7}{v['floor_hits']:>6}"
              f"{('' if v['floor_mean_ret_pct'] is None else v['floor_mean_ret_pct']):>11}"
              f"{('' if v['floor_t'] is None else v['floor_t']):>7}"
              f"{('' if v['ls_third_mean_day_pct'] is None else v['ls_third_mean_day_pct']):>9}"
              f"{v['ls_third_cumulative_pct']:>9}{v['ls_third_days']:>7}"
              f"{('' if v['null_always_short_day_pct'] is None else v['null_always_short_day_pct']):>11}"
              f"{('' if v['control_neg_runup_day_pct'] is None else v['control_neg_runup_day_pct']):>11}")
    print("\n  per-trade return after a flat round-trip cost:")
    print(f"  {'horizon':<12}" + "".join(f"{'-'+str(c)+'%':>10}" for c in costs)
          + f"{'ls_cum@1.5%':>13}")
    for h in HORIZONS:
        v = rt[h]
        print(f"  {h:<12}" + "".join(
            f"{('' if v[f'floor_mean_after_{c}pct_cost'] is None else v[f'floor_mean_after_{c}pct_cost']):>10}"
            for c in costs) + f"{v['ls_third_cumulative_after_1.5pct_cost']:>13}")
    print("\n  worst / median / best single trade in the floor book:")
    for h in HORIZONS:
        v = rt[h]
        print(f"  {h:<12}{v['floor_worst_pct']:>10}{v['floor_median_ret_pct']:>10}"
              f"{v['floor_best_pct']:>10}")

    sr = session_returns(panel, a.floor)
    print("\nRETURNS by session (per trade, floor book)")
    print(f"  {'horizon':<12}" + "".join(f"{s+'_ret':>10}{s+'_t':>8}" for s in ("amc", "bmo")))
    for h in HORIZONS:
        print(f"  {h:<12}" + "".join(
            f"{('' if sr[s][h]['mean_ret_pct'] is None else sr[s][h]['mean_ret_pct']):>10}"
            f"{('' if sr[s][h]['t'] is None else sr[s][h]['t']):>8}"
            for s in ("amc", "bmo")))

    pret = policy_returns(panel, a.floor, costs)
    print("\nRETURNS by exit policy")
    print(f"  {'policy':<24}{'trades':>7}{'hits':>6}{'per_trade':>11}{'t':>7}"
          f"{'-1.5%':>8}{'ls/day':>9}{'ls_cum':>9}{'days+':>7}{'short/day':>11}")
    for n, v in pret.items():
        print(f"  {n:<24}{v['floor_n']:>7}{v['floor_hits']:>6}"
              f"{('' if v['floor_mean_ret_pct'] is None else v['floor_mean_ret_pct']):>11}"
              f"{('' if v['floor_t'] is None else v['floor_t']):>7}"
              f"{v['floor_mean_after_1.5pct_cost']:>8}"
              f"{('' if v['ls_third_mean_day_pct'] is None else v['ls_third_mean_day_pct']):>9}"
              f"{v['ls_third_cumulative_pct']:>9}{v['ls_third_days']:>7}"
              f"{('' if v['null_always_short_day_pct'] is None else v['null_always_short_day_pct']):>11}")
    print("  per-day long/short returns:")
    for n, v in pret.items():
        print(f"    {n:<24}{v['per_day_pct']}")

    hr = hourly_returns(panel, a.floor)
    print("\nRETURNS per hour since the entry close (17.5 = the open, 24 = the close)")
    print(f"  {'hour':>6}{'clock':>8}{'priced':>8}{'trades':>8}{'per_trade':>11}{'t':>7}"
          f"{'amc':>9}{'bmo':>9}{'ls/day':>9}{'short/day':>11}")
    for h in HOUR_GRID:
        k = f"{h:g}"
        a_ = hr["all"][k]
        clock = (16 + h) % 24
        cl = f"{int(clock):02d}:{int(round((clock % 1) * 60)):02d}"
        print(f"  {k:>6}{cl:>8}{hr['names_priced'][k]:>8}{a_['n']:>8}"
              f"{('' if a_['mean_ret_pct'] is None else a_['mean_ret_pct']):>11}"
              f"{('' if a_.get('t') is None else a_['t']):>7}"
              f"{('' if hr['amc'][k]['mean_ret_pct'] is None else hr['amc'][k]['mean_ret_pct']):>9}"
              f"{('' if hr['bmo'][k]['mean_ret_pct'] is None else hr['bmo'][k]['mean_ret_pct']):>9}"
              f"{('' if hr['ls_third_day_pct'][k] is None else hr['ls_third_day_pct'][k]):>9}"
              f"{('' if hr['null_always_short_day_pct'][k] is None else hr['null_always_short_day_pct'][k]):>11}")

    pol = policy_stats(panel, a.floor)
    print("\nexit policies (one rule per session)")
    print(f"  {'policy':<24}{'rho':>8}{'floor_n':>9}{'hits':>6}{'mean_ret':>10}"
          f"{'t':>7}{'ci95':>18}{'ls/day':>9}{'days+':>7}")
    for name, v in pol.items():
        print(f"  {name:<24}{('' if v['rho_impact_sum'] is None else v['rho_impact_sum']):>8}"
              f"{v['floor_n']:>9}{v['floor_hits']:>6}"
              f"{('' if v['floor_mean_ret_pct'] is None else v['floor_mean_ret_pct']):>10}"
              f"{('' if v['floor_t'] is None else v['floor_t']):>7}"
              f"{str(v['floor_ci95']):>18}"
              f"{('' if v['ls_third_mean_day_pct'] is None else v['ls_third_mean_day_pct']):>9}"
              f"{v['ls_third_positive_days']:>7}")

    pboot = bootstrap_policies(panel, a.floor, a.seed, min(a.trials, 4000))
    print("\n  paired day bootstrap, floor-book return minus uniform_close:")
    for n, v in pboot.items():
        if isinstance(v, dict):
            print(f"    {n:<24}{v['mean']:>8}  ci95 {str(v['ci95']):>18}"
                  f"  frac>0 {v['frac_gt_0']}")
    print(f"    best of six beats the close in "
          f"{pboot.get('best_of_six_frac_gt_0')} of resamples -- the hybrid was "
          f"chosen after seeing the split, so read this and not the row above it")

    boot = bootstrap_vs_close(panel, a.floor, a.seed, min(a.trials, 4000))
    print("\npaired day bootstrap, each horizon minus holding to the close")
    print("  horizon        d_rho        ci95            d_floor_ret     ci95")
    for h, v in boot.items():
        dr, df = v["delta_rho_vs_close"], v["delta_floor_ret_vs_close"]
        print(f"  {h:<10} {('' if not dr else dr['mean']):>8}  "
              f"{('' if not dr else str(dr['ci95'])):>18}  "
              f"{('' if not df else df['mean']):>10}  "
              f"{('' if not df else str(df['ci95'])):>18}")

    print(f"\nfamily-wise over {len(HORIZONS)} horizons "
          f"({a.trials} within-day shuffles):")
    print(f"  best ranking rho      p_fw = {fw_rho}")
    print(f"  best conviction rho   p_fw = {fw_conv}")

    out = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "events": n_all, "days": len(panel),
           "duplicate_day_kept": bool(a.keep_duplicate_day),
           "conviction_floor_pts": a.floor,
           "min_dollar_vol": a.min_dollar_vol,
           "trials": a.trials, "seed": a.seed,
           "coverage": coverage, "problems": problems,
           "horizons": stats, "horizons_liquid": lstats,
           "legs": legs, "bootstrap_vs_close": boot,
           "by_session": by_session, "policies": pol,
           "returns_by_horizon": rt, "returns_by_session": sr,
           "returns_hourly": hr,
           "returns_by_policy": pret, "costs_pct": costs,
           "policy_bootstrap_vs_close": pboot,
           "family_wise": {"best_rho_p": fw_rho, "best_conviction_p": fw_conv},
           "panel": panel}
    p = ROOT / a.out
    p.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()

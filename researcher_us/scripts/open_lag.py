#!/usr/bin/env python3
"""How often does the opening print miss the pre-market move, and can we see it coming?

The pattern the operator raised on 2026-10-20 with AERO: the pre-market already
holds the reaction (AERO 15.00 against a 15.89 close, -5.6%), the stock then opens
much closer to the old close (15.28, -3.8%; first minute up to 15.67) and within
minutes trades at the pre-market level again (14.78 at 09:31). An exit sent "at the
open" -- which is what `exit_mode: amc_open` does for every amc leg, a market DAY
order queued in the pre-market -- then gives back part of a gain it already had.

This script measures it on every US earnings event in the repo's universe files
(stage E, E-P, E-PF, E-PI, E-S, D: one row per ticker, event date and session),
from Yahoo bars with pre- and post-market included:

  C0      the regular close before the reaction session
  PM      the last extended-hours trade before 09:30 on the reaction session
          (for amc, falling back to the last after-hours trade on the event date)
  O       the official open (daily bar) of the reaction session
  P_t     the price at 09:35, 09:40, 09:45, 10:00 and 10:30 (5m closes), and on
          the 1m subset (last ~30 days) at 09:31, 09:32, 09:33 and 09:35

Everything is expressed as capture: (P - C0) / (PM - C0), the share of the
pre-market move a price holds. 1 = the pre-market level, 0 = the old close.

  lag     |PM gap| >= MIN_GAP, the open captures < 0.5 and the first 15 minutes
          get back to >= 0.8 at some 5m close. The AERO pattern: the open is the
          outlier, the pre-market was right.
  fade    the open captures < 0.5 and 10:00 is still < 0.5: the pre-market was
          the outlier, the open was right.

Then the cost of "sell at the open" to a position on the side of the pre-market
move (the side that is winning before the open), against waiting to 09:35, 09:45,
10:00, and against a limit at the PM price that is assumed to fill whenever the
first 15 minutes trade through it.

Extended-hours bars from Yahoo carry no volume, so pre-market activity is measured
as the number of 5m (and 1m) bars that printed at all, and how long before 09:30 the
last one printed. That and the gap's size are the candidate predictors, measured
here, not assumed.

    python3 researcher_us/scripts/open_lag.py --cache <dir> \
        --out researcher_us/analysis/open-lag.json
"""
import argparse
import glob
import json
import math
import random
import statistics as st
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
YQ = "https://query1.finance.yahoo.com"
OPEN_HM = 9 * 60 + 30
MIN_GAP = 2.0          # percent; below this "capture" is a ratio of two noises
LAG_OPEN_MAX = 0.5
LAG_RECOVER_MIN = 0.8
# A pre-market is "stale" when its last print is 31+ minutes before the open or it
# printed in fewer than 6 five-minute bars. Observable at 09:25, NOT at stage M's
# 08:56 fire. Chosen on this sample (the bucket edges were set before reading it,
# the OR of the two was not), so it is a lead to run forward, not a rule.
STALE_MINUTES = 31
STALE_BARS = 6


def stale_pm(r):
    return r["pm_minutes_before_open"] >= STALE_MINUTES or r["pm_bars_5m"] < STALE_BARS


def et_offset(day):
    """EDT until the first Sunday of November 2026, EST after."""
    return timedelta(hours=-4) if day < "2026-11-01" else timedelta(hours=-5)


def _get(url, cache, tag):
    p = Path(cache) / tag if cache else None
    if p and p.exists():
        return json.loads(p.read_text())
    j = None
    for attempt in range(4):
        try:
            j = json.loads(urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read())
            break
        except Exception as e:
            if attempt == 3:
                return {"_error": f"{type(e).__name__}: {e}"}
            time.sleep(2 ** attempt)
    if p:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(j))
    return j


def _result(j):
    if not j or j.get("_error") or not (j.get("chart") or {}).get("result"):
        return None
    r = j["chart"]["result"][0]
    if not r.get("timestamp") or not (r.get("indicators") or {}).get("quote"):
        return None
    return r


def sym(t):
    return t.upper().replace(".", "-")


def daily(t, cache):
    r = _result(_get(f"{YQ}/v8/finance/chart/{sym(t)}?range=6mo&interval=1d", cache, f"{t}.d.json"))
    if not r:
        return None, None
    q = r["indicators"]["quote"][0]
    out = {}
    for i, ts in enumerate(r["timestamp"]):
        if q["close"][i] is None or q["open"][i] is None:
            continue
        d = datetime.fromtimestamp(ts, timezone.utc)
        d = (d + et_offset(d.date().isoformat())).date().isoformat()
        out[d] = {"open": q["open"][i], "close": q["close"][i],
                  "volume": q["volume"][i] or 0}
    return out, r["meta"].get("exchangeName")


def bars(t, cache, interval, url_range, tag):
    r = _result(_get(f"{YQ}/v8/finance/chart/{sym(t)}?{url_range}&interval={interval}"
                     f"&includePrePost=true", cache, tag))
    out = {}
    if not r:
        return out
    q = r["indicators"]["quote"][0]
    for i, ts in enumerate(r["timestamp"]):
        o, h, lo, c = q["open"][i], q["high"][i], q["low"][i], q["close"][i]
        if c is None and o is None:
            continue
        u = datetime.fromtimestamp(ts, timezone.utc)
        d = u + et_offset(u.date().isoformat())
        out.setdefault(d.date().isoformat(), []).append(
            {"hm": d.hour * 60 + d.minute, "open": o, "high": h if h is not None else o,
             "low": lo if lo is not None else o, "close": c if c is not None else o,
             "volume": q["volume"][i] or 0})
    for v in out.values():
        v.sort(key=lambda b: b["hm"])
    return out


def m1(t, cache):
    """1m bars for the last ~29 days, in 7-day chunks (Yahoo's limits)."""
    now = int(time.time()) // 3600 * 3600
    out = {}
    for k in range(4):
        p2 = now - k * 7 * 86400
        p1 = p2 - 7 * 86400
        if k == 3:
            p1 = now - 29 * 86400
        part = bars(t, cache, "1m", f"period1={p1}&period2={p2}", f"{t}.m1.{k}.{p2}.json")
        for d, v in part.items():
            out.setdefault(d, [])
            seen = {b["hm"] for b in out[d]}
            out[d].extend(b for b in v if b["hm"] not in seen)
            out[d].sort(key=lambda b: b["hm"])
    return out


def events():
    ev = {}
    for f in sorted(glob.glob(str(ROOT / "research/2026/*/*/edge*/universe.json"))):
        try:
            j = json.loads(Path(f).read_text())
        except Exception:
            continue
        for n in j.get("names", []):
            s, d = n.get("session"), n.get("event_date")
            if s in ("amc", "bmo") and d and n.get("ticker"):
                ev.setdefault((n["ticker"], d, s), {
                    "market_cap_usd": n.get("market_cap_usd"),
                    "run_day": Path(f).parent.parent.name,
                    "source": str(Path(f).relative_to(ROOT))})
    return ev


def panel_sides():
    """Stage E-P's side and panel_pct per (ticker, run day), for the book's view."""
    out = {}
    for f in sorted(glob.glob(str(ROOT / "research/2026/*/*/edge-panel/edge-scores-panel.json"))):
        try:
            j = json.loads(Path(f).read_text())
        except Exception:
            continue
        day = Path(f).parent.parent.name
        for r in j.get("ranking") or []:
            if r.get("ticker") and r.get("panel_pct") is not None and r.get("side") in (1, -1):
                out[(r["ticker"], day)] = {"panel_pct": r["panel_pct"], "side": r["side"],
                                           "selected": bool(r.get("selected"))}
    return out


def last_ext(day_bars, before_hm, after_hm=None):
    v = [b for b in day_bars if b["hm"] < before_hm and (after_hm is None or b["hm"] >= after_hm)]
    return v


def close_at(day_bars, hm, width):
    """Close of the bar that ends at `hm` (starts at hm - width)."""
    for b in day_bars:
        if b["hm"] == hm - width:
            return b["close"]
    v = [b for b in day_bars if OPEN_HM <= b["hm"] <= hm - width]
    return v[-1]["close"] if v else None


def measure(t, d, s, cache):
    dly, exch = daily(t, cache)
    if not dly:
        return {"error": "no daily bars"}
    days = sorted(dly)
    react = d if s == "bmo" else next((x for x in days if x > d), None)
    if not react or react not in dly:
        return {"error": "reaction session not in bars yet"}
    prev = [x for x in days if x < react]
    if not prev:
        return {"error": "no prior close"}
    c0 = dly[prev[-1]]["close"]
    o = dly[react]["open"]
    hist = [dly[x] for x in prev[-20:]]
    dvol = st.median([h["close"] * h["volume"] for h in hist]) if hist else None
    m5 = bars(t, cache, "5m", "range=60d", f"{t}.m5.json")
    rb = m5.get(react, [])
    if not [b for b in rb if b["hm"] >= OPEN_HM]:
        return {"error": "no 5m regular bars on the reaction session"}
    pre = last_ext(rb, OPEN_HM, 4 * 60)
    ah = [b for b in m5.get(prev[-1], []) if b["hm"] >= 16 * 60] if s == "amc" else []
    if pre:
        pm, pm_hm, pm_basis = pre[-1]["close"], pre[-1]["hm"], "pre_market"
    elif ah:
        pm, pm_hm, pm_basis = ah[-1]["close"], ah[-1]["hm"] - 24 * 60, "after_hours"
    else:
        return {"error": "no extended-hours trade", "exchange": exch}
    row = {"exchange": exch, "react_date": react, "c0": c0, "open": o, "pm": pm,
           "pm_basis": pm_basis, "pm_last_hm": pm_hm,
           "pm_minutes_before_open": OPEN_HM - pm_hm,
           "pm_bars_5m": len(pre), "pm_bars_5m_last_hour": len([b for b in pre if b["hm"] >= 8 * 60 + 30]),
           "ah_bars_5m": len(ah), "dollar_vol_20d": dvol, "price": c0}
    row["first_trade_5m"] = next(b["open"] for b in rb if b["hm"] >= OPEN_HM)
    for hm in (9 * 60 + 35, 9 * 60 + 40, 9 * 60 + 45, 10 * 60, 10 * 60 + 30):
        row[f"p5_{hm // 60:02d}{hm % 60:02d}"] = close_at(rb, hm, 5)
    first15 = [b for b in rb if OPEN_HM <= b["hm"] < OPEN_HM + 15]
    row["hi15"] = max(b["high"] for b in first15) if first15 else None
    row["lo15"] = min(b["low"] for b in first15) if first15 else None
    row["close"] = dly[react]["close"]
    return row


def m1_detail(t, react, cache, m1cache):
    if t not in m1cache:
        m1cache[t] = m1(t, cache)
    b = m1cache[t].get(react, [])
    reg = [x for x in b if x["hm"] >= OPEN_HM]
    if not reg:
        return None
    pre = [x for x in b if 4 * 60 <= x["hm"] < OPEN_HM]
    out = {"pm_bars_1m": len(pre),
           "pm_bars_1m_last_30": len([x for x in pre if x["hm"] >= 9 * 60]),
           "pm_vol_1m": sum(x["volume"] for x in pre),
           "first_trade_1m": reg[0]["open"], "first_bar_hm": reg[0]["hm"],
           "first_bar_volume": reg[0]["volume"]}
    for hm in (9 * 60 + 31, 9 * 60 + 32, 9 * 60 + 33, 9 * 60 + 35):
        out[f"p1_{hm // 60:02d}{hm % 60:02d}"] = close_at(b, hm, 1)
    return out


def cap(p, row):
    g = row["pm"] - row["c0"]
    if p is None or g == 0:
        return None
    return (p - row["c0"]) / g


def pct(p, c0):
    return None if p is None else 100.0 * (p / c0 - 1)


def classify(row):
    gpm = pct(row["pm"], row["c0"])
    row["gap_pm_pct"] = gpm
    row["gap_open_pct"] = pct(row["open"], row["c0"])
    row["capture_open"] = cap(row["open"], row)
    row["capture_first_trade"] = cap(row["first_trade_5m"], row)
    for k in ("p5_0935", "p5_0940", "p5_0945", "p5_1000", "p5_1030", "close"):
        row[f"capture_{k}"] = cap(row.get(k), row)
    sgn = 1 if gpm >= 0 else -1
    # Best price in the gap's direction in the first 15 minutes, as capture.
    best = row["lo15"] if sgn < 0 else row["hi15"]
    row["capture_best15"] = cap(best, row)
    big = abs(gpm) >= MIN_GAP
    rec = max([c for c in (row["capture_p5_0935"], row["capture_p5_0940"],
                           row["capture_p5_0945"]) if c is not None], default=None)
    row["capture_recover15"] = rec
    co = row["capture_open"]
    row["big_gap"] = big
    row["lag"] = bool(big and co is not None and co < LAG_OPEN_MAX
                      and rec is not None and rec >= LAG_RECOVER_MIN)
    row["fade"] = bool(big and co is not None and co < LAG_OPEN_MAX
                       and row["capture_p5_1000"] is not None and row["capture_p5_1000"] < LAG_OPEN_MAX)
    row["open_short"] = bool(big and co is not None and co < LAG_OPEN_MAX)
    # Return to a position on the gap's side, in percent of C0, at each exit.
    def ret(p):
        return None if p is None else sgn * 100.0 * (p / row["c0"] - 1)
    row["gapside_ret"] = {
        "pm": ret(row["pm"]), "open": ret(row["open"]),
        "first_trade": ret(row["first_trade_5m"]),
        "0935": ret(row["p5_0935"]), "0945": ret(row["p5_0945"]),
        "1000": ret(row["p5_1000"]), "1030": ret(row["p5_1030"]), "close": ret(row["close"]),
        # A day limit at the PM price: fills if the first 15 minutes trade at or
        # beyond it, else falls back to the 10:00 price. Optimistic on queue.
        "limit_pm": ret(row["pm"]) if (row["capture_best15"] is not None and row["capture_best15"] >= 1.0)
        else ret(row["p5_1000"]),
    }
    return row


def mean(xs):
    xs = [x for x in xs if x is not None]
    return st.mean(xs) if xs else None


def tstat(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 3:
        return None
    sd = st.stdev(xs)
    return None if sd == 0 else st.mean(xs) / (sd / math.sqrt(len(xs)))


def summarise(rows, label):
    big = [r for r in rows if r["big_gap"]]
    out = {"label": label, "n_events": len(rows), "n_big_gap": len(big),
           "lag": sum(r["lag"] for r in big), "fade": sum(r["fade"] for r in big),
           "open_short": sum(r["open_short"] for r in big)}
    if big:
        out["lag_rate"] = out["lag"] / len(big)
        out["open_short_rate"] = out["open_short"] / len(big)
        out["median_capture_open"] = st.median([r["capture_open"] for r in big])
        out["median_capture_0935"] = st.median([r["capture_p5_0935"] for r in big if r["capture_p5_0935"] is not None])
        exits = ["pm", "open", "0935", "0945", "1000", "limit_pm", "close"]
        out["gapside_ret_mean"] = {k: mean([r["gapside_ret"][k] for r in big]) for k in exits}
        out["wait_minus_open"] = {}
        for k in ("0935", "0945", "1000", "limit_pm", "close"):
            d = [r["gapside_ret"][k] - r["gapside_ret"]["open"] for r in big
                 if r["gapside_ret"][k] is not None]
            out["wait_minus_open"][k] = {"mean": mean(d), "t": tstat(d), "n": len(d),
                                         "share_better": sum(x > 0 for x in d) / len(d) if d else None}
    return out


def book(rows, label, min_pct=60.0):
    """The panel's own positions, both sides of the pre-market move.

    A position on the side of the pre-market move is WINNING at 09:25 and a stale
    open costs it; one against the move is LOSING and a stale open helps it (it
    exits near the old close). `adaptive` uses only what is known before 09:30:
    winning -> a day limit at the PM price (fallback 10:00), losing -> market at
    the open. Returns are on the position's side, in percent of C0, entry at C0.
    """
    g = [r for r in rows if r.get("panel") and r["panel"]["panel_pct"] >= min_pct]
    out = {"label": label, "n": len(g)}
    if not g:
        return out
    pol = {"open": [], "0935": [], "1000": [], "close": [], "adaptive": [], "adaptive_0935": []}
    win, lose = [], []
    for r in g:
        s = r["panel"]["side"] * (1 if r["gap_pm_pct"] >= 0 else -1)  # +1 = on the gap's side
        gr = r["gapside_ret"]
        x = {k: (None if gr[k] is None else s * gr[k]) for k in gr}
        winning = x["pm"] > 0
        (win if winning else lose).append(x)
        for k in ("open", "0935", "1000", "close"):
            pol[k].append(x[k])
        pol["adaptive"].append(x["limit_pm"] if winning else x["open"])
        pol["adaptive_0935"].append(x["0935"] if winning else x["open"])
    out["mean_ret"] = {k: mean(v) for k, v in pol.items()}
    d = [a - b for a, b in zip(pol["adaptive"], pol["open"]) if a is not None and b is not None]
    out["adaptive_minus_open"] = {"mean": mean(d), "t": tstat(d), "n": len(d)}
    d = [a - b for a, b in zip(pol["adaptive_0935"], pol["open"]) if a is not None and b is not None]
    out["adaptive_0935_minus_open"] = {"mean": mean(d), "t": tstat(d), "n": len(d)}
    out["winning_at_pm"] = {"n": len(win), "open_minus_0935": mean(
        [a["open"] - a["0935"] for a in win if a["0935"] is not None])}
    out["losing_at_pm"] = {"n": len(lose), "open_minus_0935": mean(
        [a["open"] - a["0935"] for a in lose if a["0935"] is not None])}
    return out


def split(rows, key, edges, label):
    out = []
    big = [r for r in rows if r["big_gap"] and r.get(key) is not None]
    lo = -math.inf
    for e in list(edges) + [math.inf]:
        g = [r for r in big if lo <= r[key] < e]
        if g:
            d = [r["gapside_ret"]["0935"] - r["gapside_ret"]["open"] for r in g
                 if r["gapside_ret"]["0935"] is not None]
            out.append({"bucket": f"{label} [{lo:g}, {e:g})", "n": len(g),
                        "lag_rate": sum(r["lag"] for r in g) / len(g),
                        "open_short_rate": sum(r["open_short"] for r in g) / len(g),
                        "fade_rate": sum(r["fade"] for r in g) / len(g),
                        "median_capture_open": st.median([r["capture_open"] for r in g]),
                        "mean_0935_minus_open": mean(d)})
        lo = e
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out")
    ap.add_argument("--rows-out")
    ap.add_argument("--no-1m", action="store_true")
    a = ap.parse_args()
    ev = events()
    sides = panel_sides()
    rows, errors, m1c = [], [], {}
    for i, ((t, d, s), meta) in enumerate(sorted(ev.items(), key=lambda kv: kv[0][1])):
        try:
            r = measure(t, d, s, a.cache)
        except Exception as e:
            r = {"error": f"{type(e).__name__}: {e}"}
        if "error" in r:
            errors.append({"ticker": t, "event_date": d, "session": s, **r})
            continue
        r.update({"ticker": t, "event_date": d, "session": s, **meta})
        classify(r)
        r["stale_pm"] = stale_pm(r)
        if not a.no_1m:
            det = m1_detail(t, r["react_date"], a.cache, m1c)
            if det:
                r["m1"] = det
                for k in ("p1_0931", "p1_0932", "p1_0933", "p1_0935"):
                    r["m1"][f"capture_{k}"] = cap(det.get(k), r)
                r["m1"]["capture_first_trade"] = cap(det["first_trade_1m"], r)
        ps = sides.get((t, meta["run_day"]))
        if ps:
            r["panel"] = ps
        rows.append(r)
        if i % 25 == 0:
            print(f"{i}/{len(ev)} {t} {d}", file=sys.stderr)
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "definitions": {"min_gap_pct": MIN_GAP, "lag_open_max": LAG_OPEN_MAX,
                        "lag_recover_min": LAG_RECOVER_MIN},
        "n_events_in_universe": len(ev), "n_measured": len(rows), "n_errors": len(errors),
        "all": summarise(rows, "all"),
        "amc": summarise([r for r in rows if r["session"] == "amc"], "amc"),
        "bmo": summarise([r for r in rows if r["session"] == "bmo"], "bmo"),
        "stale_pm": summarise([r for r in rows if stale_pm(r)], "stale pre-market"),
        "fresh_pm": summarise([r for r in rows if not stale_pm(r)], "fresh pre-market"),
        "book_panel_ge60": book(rows, "panel_pct >= 60 (stage M names)"),
        "book_panel_ge60_amc": book([r for r in rows if r["session"] == "amc"], "amc, panel_pct >= 60"),
        "book_panel_ge80": book(rows, "panel_pct >= 80 (traded rule)", 80.0),
        "splits": {
            "abs_gap": split([dict(r, ag=abs(r["gap_pm_pct"])) for r in rows], "ag", [4, 8], "|gap| %"),
            "pm_bars_5m": split(rows, "pm_bars_5m", [6, 24, 60], "pre-market 5m bars"),
            "pm_minutes_before_open": split(rows, "pm_minutes_before_open", [6, 31, 91], "min since last PM trade"),
            "dollar_vol_20d": split(rows, "dollar_vol_20d", [5e6, 5e7], "20d $vol"),
            "exchange": [],
        },
        "errors": errors,
    }
    for ex in sorted({r["exchange"] for r in rows if r["big_gap"]}):
        g = [r for r in rows if r["big_gap"] and r["exchange"] == ex]
        report["splits"]["exchange"].append({"bucket": ex, "n": len(g),
                                             "lag_rate": sum(r["lag"] for r in g) / len(g),
                                             "open_short_rate": sum(r["open_short"] for r in g) / len(g),
                                             "median_capture_open": st.median([r["capture_open"] for r in g])})
    if a.out:
        Path(a.out).write_text(json.dumps(report, indent=1))
    if a.rows_out:
        Path(a.rows_out).write_text(json.dumps(rows, indent=0))
    print(json.dumps({k: report[k] for k in ("n_measured", "n_errors", "all", "amc", "bmo", "stale_pm", "fresh_pm", "book_panel_ge60", "book_panel_ge60_amc", "book_panel_ge80")}, indent=1))
    print(json.dumps(report["splits"], indent=1))


if __name__ == "__main__":
    main()

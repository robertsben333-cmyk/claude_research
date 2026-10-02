#!/usr/bin/env python3
"""Is "the hunt is right where things move" signal against noise, and what predicts it?

Run from the repo root:

    python3 research/analyses/signal-vs-noise/analyse.py

PREDICTIONS WRITTEN BEFORE ANY RESULT WAS READ (2026-10-02). If the volatility effect
on the hit rate is signal against noise rather than skill concentrated in volatile names:

  P1  mechanism    the hit rate rises with the REALISED |move|, towards 50% for tiny
                   moves, in both samples.
  P2  indicators   event-to-noise (the name's median earnings reaction over its ordinary
                   daily sd) and a LOW market share of variance predict the hit rate at
                   least as well as raw volatility.
  P3  market noise adjusting the move for the market (beta x SPY) and the sector
                   (beta x sector ETF) over the same window narrows the hit-rate gap
                   between low- and high-volatility names.
  P4  per unit     the return in units of the name's expected move is about equal in
      of risk      low- and high-volatility names, so the raw-return gap is scale.
  P5  conviction   |impact_sum| correlates with the expected move, and within a
                   volatility half the floor still separates hit rates.

Two samples: the live ledger (141 resolved US names, dashboard/data/ledger.json) at
the strategy exit and the close, and the sealed backtest corpus
(archive/backtest/runs/edge-corpus/, close to close, contaminated captures out), which
is independent of the live days and on which the hunt did not rank (rho +0.07).
Network results are cached in cache.json.
"""
import json
import math
import random
import statistics as st
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CACHE = HERE / "cache.json"
OTHER_CACHE = REPO / "research" / "analyses" / "attention-proxies" / "cache.json"
UA = "claude_research/0.1 (robertsben333@gmail.com) signal-vs-noise research"
PERMS = 3000
random.seed(20261002)
cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
other = json.loads(OTHER_CACHE.read_text()) if OTHER_CACHE.exists() else {}
SECTOR_ETF = {"Technology": "XLK", "Consumer Cyclical": "XLY", "Consumer Defensive": "XLP",
              "Healthcare": "XLV", "Financial Services": "XLF", "Industrials": "XLI",
              "Energy": "XLE", "Basic Materials": "XLB", "Utilities": "XLU",
              "Real Estate": "XLRE", "Communication Services": "XLC"}
ET = timedelta(hours=-4)          # EDT for every date in both samples


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def get(url):
    if url in cache:
        return cache[url]
    if url in other:
        return other[url]
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read().decode("utf-8")
            cache[url] = body
            time.sleep(0.3)
            return body
        except Exception:                                   # noqa: BLE001
            time.sleep(3 * (i + 1))
    cache[url] = None
    return None


def daily(t):
    body = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=2y&interval=1d")
    try:
        res = json.loads(body)["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose") or q["close"]
    except (TypeError, KeyError, IndexError, ValueError):
        return {}
    out = {}
    for ts, o, c, a in zip(res["timestamp"], q["open"], q["close"], adj):
        if c is None:
            continue
        out[(datetime.fromtimestamp(ts, timezone.utc) + ET).date()] = (o, c, a)
    return out


def intraday(t):
    body = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=60d&interval=5m")
    try:
        res = json.loads(body)["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
    except (TypeError, KeyError, IndexError, ValueError):
        return {}
    out = {}
    for ts, c in zip(res["timestamp"], q["close"]):
        if c is not None:
            out[datetime.fromtimestamp(ts, timezone.utc) + ET] = c
    return out


def price_at_1400(bars, d):
    """Close of the last 5-minute bar starting before 14:00 ET on day d."""
    pts = [(k, v) for k, v in bars.items() if k.date() == d and k.hour * 60 + k.minute < 14 * 60]
    return max(pts)[1] if pts else None


def beta_stats(stock, mkt, before):
    """beta, R^2 and daily sds over the 250 sessions before `before`."""
    days = sorted(d for d in stock if d < before and d in mkt)[-251:]
    if len(days) < 120:
        return {}
    rs = [stock[b][2] / stock[a][2] - 1 for a, b in zip(days, days[1:])]
    rm = [mkt[b][2] / mkt[a][2] - 1 for a, b in zip(days, days[1:])]
    mr, mm = st.fmean(rs), st.fmean(rm)
    cov = sum((x - mr) * (y - mm) for x, y in zip(rs, rm))
    vm = sum((y - mm) ** 2 for y in rm)
    beta = cov / vm if vm else None
    vs = sum((x - mr) ** 2 for x in rs)
    r2 = cov * cov / (vm * vs) if vm and vs else None
    resid = [x - beta * y for x, y in zip(rs, rm)] if beta is not None else rs
    return {"beta": beta, "r2": r2, "sd_daily_1y": 100 * st.stdev(rs),
            "sd_idio_1y": 100 * st.stdev(resid), "sd_daily_60": 100 * st.stdev(rs[-60:])}


# ------------------------------------------------------------------- samples
def live_rows():
    led = load(REPO / "dashboard" / "data" / "ledger.json")
    floor = led.get("conviction_floor", 2.8)
    spy_d, spy_i = daily("SPY"), intraday("SPY")
    etf_d = {e: daily(e) for e in set(SECTOR_ETF.values())}
    etf_i = {e: intraday(e) for e in set(SECTOR_ETF.values())}
    out = []
    for r in led["names"]:
        if r.get("duplicate_event") or not r.get("impact_sum") or r.get("ret_strategy") is None:
            continue
        b = load(REPO / r["run"] / "baselines" / f"{r['ticker']}.json") or {}
        hist, opt = b.get("history") or {}, b.get("options") or {}
        ent, rea = date.fromisoformat(r["entry_date"]), date.fromisoformat(r["reaction_date"])
        sd = daily(r["ticker"])
        bs = beta_stats(sd, spy_d, ent) if sd else {}
        etf = SECTOR_ETF.get(r.get("sector"))
        bse = beta_stats(sd, etf_d[etf], ent) if sd and etf else {}

        def mkt_move(dly, ida, exit_kind):
            if ent not in dly or rea not in dly:
                return None
            e0 = dly[ent][1]
            if exit_kind == "close":
                e1 = dly[rea][1]
            elif exit_kind == "open":
                e1 = dly[rea][0]
            else:
                e1 = price_at_1400(ida, rea)
            return None if not e0 or not e1 else 100 * (e1 / e0 - 1)

        strat_kind = "open" if r.get("session") == "amc" else "1400"
        row = base_row(r["impact_sum"], floor, r["run"], hist, opt, b, r.get("realised_vol_20d"),
                       bs, bse)
        for ex, kind in (("strategy", strat_kind), ("close", "close")):
            mv = r.get("mv_" + ex)
            sm = mkt_move(spy_d, spy_i, kind)
            em = mkt_move(etf_d[etf], etf_i[etf], kind) if etf else None
            row[ex] = outcome(r["impact_sum"], mv, row, sm, em, bs, bse)
        row.update(ticker=r["ticker"], sample="live", session=r.get("session"))
        out.append(row)
    return out


def corpus_rows():
    root = REPO / "archive" / "backtest" / "runs" / "edge-corpus"
    cont = load(root / "contamination.json") or {}
    bad = {(x.get("ticker"), x.get("event_date")) for x in cont.get("rows", [])
           if x.get("contaminated")}
    spy_d = daily("SPY")
    out, seen = [], set()
    for day in sorted(p for p in root.iterdir() if p.is_dir()):
        sc = load(day / "edge-scores.json") or {}
        oc = load(day / "edge-outcome.json") or {}
        moves = {x["ticker"]: x for pd in oc.get("per_day", []) for x in pd.get("rows", [])}
        for n in sc.get("ranking", []):
            t = n["ticker"]
            m = moves.get(t) or {}
            b = load(day / "baselines" / f"{t}.json") or {}
            if (not n.get("rankable") or m.get("move_pct") is None
                    or (t, b.get("event_date")) in bad or t in seen):
                continue
            imp = sum(f.get("expected_impact_pct") or 0 for f in n.get("findings") or [])
            if not imp:
                continue
            seen.add(t)
            hist, opt = b.get("history") or {}, b.get("options") or {}
            before = date.fromisoformat(m["before_date"])
            sd = daily(t)
            bs = beta_stats(sd, spy_d, before) if sd else {}
            row = base_row(imp, 3.0, str(day), hist, opt, b,
                           (b.get("tape") or {}).get("realised_vol_20d_annualised_pct"), bs, {})
            sm = None
            a1 = date.fromisoformat(m["after_date"])
            if before in spy_d and a1 in spy_d:
                sm = 100 * (spy_d[a1][1] / spy_d[before][1] - 1)
            row["close"] = outcome(imp, m["move_pct"], row, sm, None, bs, {})
            row.update(ticker=t, sample="corpus")
            out.append(row)
    return out, len(bad)


def base_row(imp, floor, day, hist, opt, b, rv20, bs, bse):
    exp = b.get("expected_move_pct")
    implied = opt.get("event_implied_move_pct") if opt.get("status") == "ok" else None
    sd60 = bs.get("sd_daily_60") or ((rv20 / math.sqrt(252)) if rv20 else None)
    hm = hist.get("median_abs_move_pct")
    return {"day": day, "impact": imp, "conviction": abs(imp), "book": abs(imp) >= floor,
            "rv20": rv20, "sd_daily_60": sd60, "sd_idio_1y": bs.get("sd_idio_1y"),
            "hist_median_abs": hm, "implied_move": implied, "expected_move": exp,
            "event_to_noise": hm / sd60 if hm and sd60 else None,
            "implied_to_noise": implied / sd60 if implied and sd60 else None,
            "market_r2": bs.get("r2"), "sector_r2": bse.get("r2"), "beta": bs.get("beta"),
            "z_conviction": abs(imp) / exp if exp else None,
            "deadband": b.get("deadband_pct")}


def outcome(imp, mv, row, sm, em, bs, bse):
    if mv is None:
        return None
    s = 1 if imp > 0 else -1
    o = {"mv": mv, "absmv": abs(mv), "hit": 1.0 if s * mv > 0 else 0.0, "ret": s * mv}
    if row.get("expected_move"):
        o["ret_norm"] = s * mv / row["expected_move"]
        o["absmv_over_exp"] = abs(mv) / row["expected_move"]
    if row.get("deadband") is not None:
        o["outside_deadband"] = abs(mv) > row["deadband"]
    if sm is not None and bs.get("beta") is not None:
        ex = mv - bs["beta"] * sm
        o.update(mkt_move=sm, ex_mkt=ex, hit_mkt=1.0 if s * ex > 0 else 0.0, ret_mkt=s * ex,
                 mkt_share=abs(bs["beta"] * sm) / (abs(mv) + 1e-9))
    if em is not None and bse.get("beta") is not None:
        ex = mv - bse["beta"] * em
        o.update(ex_sec=ex, hit_sec=1.0 if s * ex > 0 else 0.0, ret_sec=s * ex)
    return o


# ------------------------------------------------------------------- stats
def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def pearson(a, b):
    ma, mb = st.fmean(a), st.fmean(b)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return 0.0 if not sa or not sb else sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)


def spearman_p(rows, xk, yfun):
    g = [r for r in rows if r.get(xk) is not None and yfun(r) is not None]
    if len(g) < 15:
        return None
    x = rank([r[xk] for r in g])
    y = [yfun(r) for r in g]
    obs = pearson(x, rank(y))
    by = {}
    for i, r in enumerate(g):
        by.setdefault(r["day"], []).append(i)
    ge = 0
    for _ in range(PERMS):
        yp = y[:]
        for ids in by.values():
            vals = [y[i] for i in ids]
            random.shuffle(vals)
            for i, v in zip(ids, vals):
                yp[i] = v
        if abs(pearson(x, rank(yp))) >= abs(obs) - 1e-12:
            ge += 1
    return {"n": len(g), "rho": obs, "p": (ge + 1) / (PERMS + 1)}


def cell(g, key="hit"):
    v = [r[key] for r in g if r.get(key) is not None]
    if not v:
        return "   n=0"
    return f"n={len(v):3d} {100 * st.fmean(v) if 'hit' in key else st.fmean(v):6.1f}"


def tercile_table(rows, sortkey, label, keys=("hit", "hit_mkt", "hit_sec")):
    g = sorted([r for r in rows if r.get(sortkey) is not None], key=lambda r: r[sortkey])
    if len(g) < 15:
        print(f"  {label}: too few")
        return
    k = len(g) // 3
    parts = (("low", g[:k]), ("mid", g[k:2 * k]), ("high", g[2 * k:]))
    print(f"  {label}")
    for name, sub in parts:
        print(f"    {name:4s} {sortkey} {sub[0][sortkey]:7.2f}..{sub[-1][sortkey]:7.2f}   "
              + "   ".join(f"{kk} {cell(sub, kk)}" for kk in keys))


INDICATORS = [("rv20", "realised vol 20d"), ("sd_daily_60", "daily sd 60d"),
              ("sd_idio_1y", "idiosyncratic daily sd 1y"),
              ("hist_median_abs", "median past earnings reaction"),
              ("implied_move", "option-implied event move"),
              ("expected_move", "baseline expected move"),
              ("event_to_noise", "event-to-noise (past reaction / daily sd)"),
              ("implied_to_noise", "implied-to-noise"),
              ("market_r2", "market R^2 (high = more market noise)"),
              ("sector_r2", "sector R^2"),
              ("conviction", "|impact_sum|"), ("z_conviction", "|impact_sum| / expected move")]


def flat(rows, ex):
    out = []
    for r in rows:
        o = r.get(ex)
        if o:
            out.append({**{k: v for k, v in r.items() if k not in ("strategy", "close")}, **o})
    return out


def report(rows, label):
    print(f"\n\n######## {label}: n={len(rows)}, days={len({r['day'] for r in rows})}, "
          f"book={sum(r['book'] for r in rows)}")
    print("\nP1 mechanism: hit rate by REALISED |move| (raw, market-adjusted, sector-adjusted)")
    tercile_table(rows, "absmv", "all names")
    tercile_table([r for r in rows if r["book"]], "absmv", "book")
    tercile_table(rows, "absmv_over_exp", "all names, |move| / expected move")
    out = [r for r in rows if r.get("outside_deadband") is not None]
    if out:
        a = [r for r in out if r["outside_deadband"]]
        b = [r for r in out if not r["outside_deadband"]]
        print(f"  outside deadband {cell(a)}   inside deadband {cell(b)}")
    print("\nP2 ex-ante indicators, Spearman with the hit rate (raw | market-adjusted) and "
          "with the normalised return, within-day permutation p")
    for pop, g in (("all", rows), ("book", [r for r in rows if r["book"]])):
        print(f"  -- {pop}")
        for k, name in INDICATORS:
            a = spearman_p(g, k, lambda r: r.get("hit"))
            if not a:
                continue
            b = spearman_p(g, k, lambda r: r.get("hit_mkt"))
            c = spearman_p(g, k, lambda r: r.get("ret_norm"))
            fmt = lambda s: "    –        " if not s else f"{s['rho']:+.3f} p{s['p']:.3f}"
            print(f"    {name[:44]:45s} n={a['n']:3d}  hit {fmt(a)}   hit_mkt {fmt(b)}   ret/exp {fmt(c)}")
    print("\nP3 market noise: volatility halves, raw against adjusted hit rate")
    g = [r for r in rows if r.get("rv20") is not None]
    med = sorted(r["rv20"] for r in g)[len(g) // 2]
    for pop, gg in (("all", g), ("book", [r for r in g if r["book"]])):
        for nm, sub in (("vol low ", [r for r in gg if r["rv20"] < med]),
                        ("vol high", [r for r in gg if r["rv20"] >= med])):
            ms = [r["mkt_share"] for r in sub if r.get("mkt_share") is not None]
            print(f"  {pop:4s} {nm} hit {cell(sub)}  hit_mkt {cell(sub, 'hit_mkt')}  "
                  f"hit_sec {cell(sub, 'hit_sec')}  median |beta*mkt|/|move| "
                  f"{st.median(ms) if ms else float('nan'):.2f}")
    print("\nP4 per unit of risk: mean return and return / expected move by volatility half")
    for pop, gg in (("all", g), ("book", [r for r in g if r["book"]])):
        for nm, sub in (("vol low ", [r for r in gg if r["rv20"] < med]),
                        ("vol high", [r for r in gg if r["rv20"] >= med])):
            print(f"  {pop:4s} {nm} ret {cell(sub, 'ret')}%  ret/expected {cell(sub, 'ret_norm')}"
                  f"  ret_mkt {cell(sub, 'ret_mkt')}%")
    print("\nP5 conviction against move size")
    for k in ("rv20", "expected_move", "hist_median_abs", "implied_move"):
        s = [r for r in rows if r.get(k) is not None]
        if len(s) > 15:
            print(f"  rho(|impact_sum|, {k}) {pearson(rank([r['conviction'] for r in s]), rank([r[k] for r in s])):+.3f} (n={len(s)})")
    for nm, sub in (("vol low ", [r for r in g if r["rv20"] < med]),
                    ("vol high", [r for r in g if r["rv20"] >= med])):
        a = [r for r in sub if r["book"]]
        b = [r for r in sub if not r["book"]]
        print(f"  {nm} above floor {cell(a)} ret {cell(a, 'ret')}   below floor {cell(b)} "
              f"ret {cell(b, 'ret')}   share above floor {len(a)}/{len(sub)}")


def main():
    live = live_rows()
    corpus, nbad = corpus_rows()
    CACHE.write_text(json.dumps(cache) + "\n")
    report(flat(live, "strategy"), "LIVE, strategy exit")
    report(flat(live, "close"), "LIVE, close")
    report(flat(corpus, "close"), f"CORPUS, close to close ({nbad} contaminated left out)")
    (HERE / "rows.json").write_text(json.dumps({"live": live, "corpus": corpus}, indent=1,
                                               default=str) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Collect every edge-hunt run, every order the broker filled, and what the
prices then did, into one dataset the dashboard renders.

Three levels, and they answer different questions. Keep them apart.

  names    every rankable name of every stage E run, with its score and what the
           stock did at eight exit horizons. This is the RESEARCH record: it
           exists whether or not a dollar was ever placed on the name.
  trades   every position the Alpaca account actually opened and closed, matched
           from the fill stream into round trips. This is the MONEY record, and
           it is the only one that carries a spread, a partial fill and an exit
           that never crossed.
  account  the equity curve as the broker reports it, which is the only number
           that cannot be argued with.

A name is not a trade: the turnover floor, the borrow check and the conviction
floor mean most ranked names are never traded, and a traded name can be closed by
hand at a price no horizon in `names` knows about. Every figure in the dashboard
says which level it came from.

    python3 edge/performance/scripts/build_ledger.py
    python3 edge/performance/scripts/build_ledger.py --offline   # skip the broker
"""
import argparse
import glob
import json
import math
import os
import statistics as st
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "edge" / "scripts"))

import edge_exit as EX                                            # noqa: E402
from alpaca_trade import Alpaca                                   # noqa: E402

DATA = ROOT / "edge" / "performance" / "data"
ET = timezone(timedelta(hours=-4))

# Buckets. Fixed edges rather than quantiles, so a bucket means the same thing
# when tomorrow's names are added.
ABS_BUCKETS = [(0, 1), (1, 2), (2, 3), (3, 5), (5, 8), (8, 999)]
ADV_BUCKETS = [(0, 1e6), (1e6, 5e6), (5e6, 25e6), (25e6, 1e15)]


def rd(x, n=3):
    return None if x is None else round(x, n)


def ttest(xs):
    """Mean, t and a 95% interval. None below three observations, on purpose."""
    if len(xs) < 3:
        return {"n": len(xs), "mean": rd(st.fmean(xs), 3) if xs else None,
                "t": None, "ci95": None}
    m, s = st.fmean(xs), st.stdev(xs)
    se = s / math.sqrt(len(xs))
    half = 1.96 * se
    return {"n": len(xs), "mean": rd(m), "t": rd(m / se, 2) if se else None,
            "ci95": [rd(m - half, 2), rd(m + half, 2)] if se else None,
            "sd": rd(s, 2)}


def book_stats(rets):
    out = ttest(rets)
    out["hits"] = sum(1 for x in rets if x > 0)
    out["hit_rate_pct"] = rd(100 * out["hits"] / len(rets), 1) if rets else None
    out["median"] = rd(st.median(rets), 3) if rets else None
    return out


# ------------------------------------------------------------- sector & asset

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def _cached(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return {}


def sectors_for(tickers, cache_path):
    """Sector and industry per ticker, from Yahoo's search endpoint.

    `quoteSummary/assetProfile` answers 401 without a crumb; search does not and
    returns the same two fields. Cached forever: a company's sector does not move,
    and re-fetching 100 names on every build is rude."""
    cache = _cached(cache_path)
    todo = [t for t in sorted(set(tickers)) if t not in cache]
    for t in todo:
        sym = t.upper().replace(".", "-")
        url = (f"https://query1.finance.yahoo.com/v1/finance/search?q="
               f"{urllib.parse.quote(sym)}&quotesCount=6&newsCount=0")
        row = {"sector": None, "industry": None, "name": None, "source": "yahoo search"}
        try:
            j = json.loads(urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": UA}), timeout=20).read())
            for q in j.get("quotes", []):
                if (q.get("symbol") or "").upper() in (sym, t.upper()):
                    row.update({"sector": q.get("sector"), "industry": q.get("industry"),
                                "name": q.get("longname") or q.get("shortname")})
                    break
        except Exception as exc:
            row["source"] = f"unavailable: {type(exc).__name__}"
        cache[t] = row
        time.sleep(0.15)
    if todo:
        Path(cache_path).write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
    return cache


def assets_for(tickers, api, runs, cache_path):
    """Can this name be traded, and can it be borrowed.

    Two sources, and they are not the same thing. A run's own `alpaca-assets.json`
    is what was true ON THE DAY and is preferred; the live `/v2/assets` lookup is
    what is true NOW and is the only thing available for the runs that predate that
    file. Borrow is checked daily by the broker, so a live flag is not evidence
    about a print three weeks ago -- every row says which it is."""
    out = {}
    for run in runs:                                    # day-of, the honest source
        f = Path(run) / "alpaca-assets.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text())
        for n in d.get("names", []):
            out[(str(run), n["ticker"])] = {
                "shortable": n.get("shortable"), "tradable": n.get("tradable"),
                "tradable_reason": n.get("reason"), "asset_asof": "day of the run"}
    cache = _cached(cache_path)
    todo = [t for t in sorted(set(tickers)) if t not in cache]
    if api is not None and api.usable:
        for t in todo:
            d, err = api.asset(t.upper().replace(".", "-"))
            cache[t] = ({"shortable": None, "easy_to_borrow": None, "tradable": None,
                         "error": err} if err else
                        {"shortable": d.get("shortable"),
                         "easy_to_borrow": d.get("easy_to_borrow"),
                         "tradable": d.get("tradable"),
                         "exchange": d.get("exchange")})
        if todo:
            Path(cache_path).write_text(json.dumps(cache, indent=1, sort_keys=True) + "\n")
    return out, cache


# ------------------------------------------------------------------ the names

def load_names(runs, cache):
    """Per-name rows off the runs, priced at every exit horizon.

    `edge_exit.build_panel_from_runs` does the pricing; everything added here is
    what the scorer knows and the price series does not."""
    panel, problems = EX.build_panel_from_runs(runs, cache)
    panel = EX.demean_legs(EX.add_legs(panel))

    extra = {}
    plans = {}
    for run in runs:
        rp = Path(run)
        sf = rp / "edge-scores.json"
        if not sf.exists():
            continue
        sc = json.loads(sf.read_text())
        for r in sc.get("ranking", []):
            d = r.get("diagnostics") or {}
            extra[(str(run), r["ticker"])] = {
                "rank": r.get("rank"),
                "priced_lean_pct": r.get("priced_lean_pct"),
                "n_findings": len(r.get("findings") or []),
                "impact_sum_pre_lessons": d.get("impact_sum_pre_lessons"),
                "lessons_delta": d.get("lessons_delta"),
                "edge_score_legacy": d.get("edge_score_legacy"),
                "baseline_quality": d.get("baseline_quality"),
                "hunters": d.get("hunters")}
        pf = rp / "alpaca-plan.json"
        if pf.exists():
            pl = json.loads(pf.read_text())
            for p in pl.get("positions", []) + pl.get("rejected", []):
                plans[(str(run), p["ticker"])] = p

    rows = []
    for day in panel:
        for r in day:
            key = (r["run"], r["ticker"])
            r.update(extra.get(key, {}))
            p = plans.get(key)
            if p:
                r["plan_dollar_volume_usd"] = p.get("dollar_volume_usd")
                r["plan_side"] = p.get("side")
                r["plan_tradable"] = p.get("tradable")
                r["plan_shortable"] = p.get("shortable")
                r["plan_notional_usd"] = p.get("notional_usd")
                r["plan_pct_of_adv"] = p.get("pct_of_adv")
                r["planned"] = p.get("qty") is not None
            r["run_date"] = r["run"].rstrip("/").split("/")[-2]
            r["conviction"] = abs(r["impact_sum"])
            r["above_floor"] = None
            for h in EX.HORIZONS:
                mv = r.get(f"mv_{h}")
                r[f"ret_{h}"] = (None if mv is None
                                 else rd(mv if r["impact_sum"] > 0 else -mv, 3))
            rows.append(r)

    # One issuer reporting once is one event. The 09-04 run re-hunted five names
    # that the 09-07 run hunted again for the same 09-08 prints; pooling both
    # double-counts the event. Keep the run CLOSEST to the print and flag the
    # other, rather than dropping a hard-coded date.
    seen = {}
    for r in sorted(rows, key=lambda r: (r["ticker"], r["event_date"], r["run_date"])):
        k = (r["ticker"], r["event_date"])
        if k in seen:
            seen[k]["duplicate_event"] = True
        r["duplicate_event"] = False
        seen[k] = r
    return rows, problems


def panel_of(rows, key="ret_close"):
    """Back to a list of days, which is what every pooled statistic needs."""
    days = {}
    for r in rows:
        days.setdefault(r["run"], []).append(r)
    return [v for _, v in sorted(days.items())]


# ----------------------------------------------------------------- the broker

def fills(api):
    out, page = [], None
    while True:
        q = "/v2/account/activities/FILL?page_size=100" + (f"&page_token={page}" if page else "")
        d, err = api.call("GET", q)
        if err:
            return out, err
        if not d:
            break
        out += d
        if len(d) < 100:
            break
        page = d[-1]["id"]
    out.sort(key=lambda r: r["transaction_time"])
    return out, None


def order_index(runs):
    """order_id -> what stage E meant by that order. Hand-placed orders are absent
    from this index, which is exactly how they get labelled `manual` below."""
    idx = {}
    for run in runs:
        f = Path(run) / "alpaca-orders.json"
        if not f.exists():
            continue
        st_ = json.loads(f.read_text())
        for leg in ("entries", "exits"):
            for o in st_.get(leg, []):
                if o.get("order_id"):
                    idx[o["order_id"]] = {**o, "run": str(run),
                                          "run_date": str(run).rstrip("/").split("/")[-2]}
    return idx


def round_trips(fill_rows, idx):
    """Match the fill stream into position episodes, per symbol.

    An episode opens when the position leaves zero and closes when it returns to
    zero. Partial exits on different days are one episode with a weighted exit, not
    two trades -- CODA was bought back in two pieces a day apart and counting it
    twice would put the same entry in the sample twice."""
    by = {}
    for f in fill_rows:
        by.setdefault(f["symbol"], []).append(f)

    trades, open_eps = [], []
    for sym, fs in sorted(by.items()):
        pos, ep = 0.0, None
        for f in fs:
            q = float(f["qty"])
            signed = q if f["side"] == "buy" else -q
            px = float(f["price"])
            if pos == 0:
                ep = {"symbol": sym, "side": "long" if signed > 0 else "short",
                      "entry_fills": [], "exit_fills": [], "entry_orders": set(),
                      "exit_orders": set()}
            opening = (signed > 0) == (ep["side"] == "long")
            (ep["entry_fills"] if opening else ep["exit_fills"]).append(
                {"qty": q, "px": px, "utc": f["transaction_time"],
                 "order_id": f.get("order_id")})
            (ep["entry_orders"] if opening else ep["exit_orders"]).add(f.get("order_id"))
            pos += signed
            if abs(pos) < 1e-9:
                trades.append(finish(ep, idx, closed=True))
                ep, pos = None, 0.0
        if ep is not None:
            open_eps.append(finish(ep, idx, closed=False))
    trades.sort(key=lambda t: t["entry_utc"])
    return trades, open_eps


def vwap(fs):
    q = sum(f["qty"] for f in fs)
    return (sum(f["qty"] * f["px"] for f in fs) / q if q else None), q


def finish(ep, idx, closed):
    epx, eq = vwap(ep["entry_fills"])
    xpx, xq = vwap(ep["exit_fills"])
    sign = 1 if ep["side"] == "long" else -1
    meta = next((idx[o] for o in ep["entry_orders"] if o in idx), None)
    xmeta = next((idx[o] for o in ep["exit_orders"] if o in idx), None)
    t = {"symbol": ep["symbol"], "side": ep["side"], "closed": closed,
         "qty": rd(eq, 4), "entry_px": rd(epx, 4), "exit_px": rd(xpx, 4),
         "entry_utc": ep["entry_fills"][0]["utc"],
         "exit_utc": ep["exit_fills"][-1]["utc"] if ep["exit_fills"] else None,
         "entry_notional_usd": rd(epx * eq, 2) if epx else None,
         "n_entry_fills": len(ep["entry_fills"]), "n_exit_fills": len(ep["exit_fills"]),
         "partial_exit_days": len({f["utc"][:10] for f in ep["exit_fills"]})}
    if closed and epx and xpx:
        t["ret_pct"] = rd((xpx / epx - 1) * 100 * sign, 3)
        t["pnl_usd"] = rd((xpx - epx) * eq * sign, 2)
        a = datetime.fromisoformat(t["entry_utc"].replace("Z", "+00:00"))
        b = datetime.fromisoformat(t["exit_utc"].replace("Z", "+00:00"))
        t["hold_hours"] = rd((b - a).total_seconds() / 3600, 2)
        t["exit_hour_et"] = rd(b.astimezone(ET).hour + b.astimezone(ET).minute / 60, 2)
        t["entry_hour_et"] = rd(a.astimezone(ET).hour + a.astimezone(ET).minute / 60, 2)
    if meta:
        t.update({"run": meta.get("run"), "run_date": meta.get("run_date"),
                  "impact_sum": meta.get("value"), "session": meta.get("session"),
                  "event_date": meta.get("event_date"),
                  "planned_exit_date": meta.get("exit_date"),
                  "entry_spread_pct": ((meta.get("quote_at_submit") or {}) or {}).get("spread_pct"),
                  "entry_source": "stage E"})
    else:
        t["entry_source"] = "manual"
    t["exit_source"] = "stage E" if xmeta else "manual"
    t["exit_tif"] = xmeta.get("time_in_force") if xmeta else None
    if t.get("impact_sum") is not None:
        t["conviction"] = abs(t["impact_sum"])
    return t


def attach_theoretical(trades, names):
    """What the price series says the same position was worth, beside what the
    broker actually got.

    Two gaps, and they measure different things:

      policy_gap   actual minus the board return over the stage's own window --
                   the close before the print to the close after. It contains the
                   entry timing (the book goes in at ~13:24 ET, the board assumes
                   the close), the spread, and every hour the exit was early or late.
      exec_gap     actual minus the board return at the hour the position was
                   ACTUALLY closed. Timing is divided out, so what is left is the
                   spread, the fill quality and the partial fills.
    """
    idx = {(r["run_date"], r["ticker"]): r for r in names}
    for t in trades:
        r = idx.get((t.get("run_date"), t["symbol"]))
        if not r or t.get("ret_pct") is None:
            continue
        sign = 1 if t["side"] == "long" else -1
        if r.get("mv_close") is not None:
            t["theo_ret_close_pct"] = rd(sign * r["mv_close"], 3)
            t["policy_gap_pct"] = rd(t["ret_pct"] - t["theo_ret_close_pct"], 3)
        # Hours from the theoretical entry (16:00 ET on the entry day) to the real exit.
        try:
            ex = datetime.fromisoformat(t["exit_utc"].replace("Z", "+00:00")).astimezone(ET)
            e0 = datetime.fromisoformat(r["entry_date"] + "T16:00:00").replace(tzinfo=ET)
            hrs = (ex - e0).total_seconds() / 3600
        except Exception:
            continue
        grid = [(abs(h - hrs), h) for h in EX.HOUR_GRID
                if r.get(f"hr_{h:g}") is not None]
        if not grid:
            continue
        gap, h = min(grid)
        if gap > 2.0:                      # no grid point near the real exit; say so
            t["theo_exit_hour_note"] = f"closest grid hour {h:g} is {gap:.1f}h away"
            continue
        t["theo_exit_hour"] = h
        t["theo_ret_at_exit_pct"] = rd(sign * r[f"hr_{h:g}"], 3)
        t["exec_gap_pct"] = rd(t["ret_pct"] - t["theo_ret_at_exit_pct"], 3)
    return trades


def costs_for(runs, names):
    """What a run cost to produce, beside what it earned.

    No token count is recorded anywhere in this repo, so the default is a PROXY:
    the bytes the run wrote, over four, plus the subagents it spawned. Drop real
    numbers into `edge/performance/data/costs.csv`
    (`run_date,tokens_in,tokens_out,usd,note`) and they are used instead, per day,
    with the proxy kept beside them so the two never silently merge."""
    measured = {}
    f = DATA / "costs.csv"
    if f.exists():
        import csv
        for row in csv.DictReader(f.open(encoding="utf-8")):
            d = (row.get("run_date") or "").strip()
            if not d:
                continue
            def num(k):
                v = (row.get(k) or "").strip()
                try:
                    return float(v)
                except ValueError:
                    return None
            measured[d] = {"tokens_in": num("tokens_in"), "tokens_out": num("tokens_out"),
                           "usd": num("usd"), "note": (row.get("note") or "").strip()}
    out = []
    for run in runs:
        rp = Path(run)
        date = str(run).rstrip("/").split("/")[-2]
        hunts = sorted(rp.glob("hunts/*.json"))
        n_findings, chars = 0, 0
        for h in hunts:
            try:
                txt = h.read_text(encoding="utf-8")
            except Exception:
                continue
            chars += len(txt)
            try:
                n_findings += len(json.loads(txt).get("findings") or [])
            except Exception:
                pass
        for extra in ("sweep.json", "edge-note.md", "edge-scores.json"):
            g = rp / extra
            if g.exists():
                chars += len(g.read_text(encoding="utf-8", errors="replace"))
        day_names = [r for r in names if r["run"] == str(run)]
        row = {"run": str(run), "run_date": date,
               "n_names": len(day_names), "n_hunters": len(hunts),
               "n_findings": n_findings,
               "n_subagents": len(hunts) + 1,            # hunters plus the one sweep
               "artifact_chars": chars,
               "est_output_tokens": round(chars / 4),
               "measured": measured.get(date)}
        out.append(row)
    return out


def account_block(api):
    acct, err = api.call("GET", "/v2/account")
    if err:
        return None, err
    hist, herr = api.call("GET", "/v2/account/portfolio/history?period=3M&timeframe=1D")
    curve = []
    if hist and not herr:
        base = hist.get("base_value") or 0
        for ts, eq in zip(hist.get("timestamp", []), hist.get("equity", [])):
            if not eq:
                continue                                  # before the account was funded
            # Alpaca stamps a daily point at 00:00 UTC of the NEXT day. Read in UTC
            # every equity lands on the day after the session that produced it, and
            # the daily book then joins to the wrong date.
            curve.append({"date": datetime.fromtimestamp(ts, ET).date().isoformat(),
                          "equity": rd(eq, 2),
                          "cum_ret_pct": rd((eq / base - 1) * 100, 3) if base else None})
    pos, _ = api.call("GET", "/v2/positions")
    live = rd(float(acct["equity"]), 2)
    if curve and curve[-1]["equity"] != live:
        base = (hist or {}).get("base_value") or 0
        curve.append({"date": datetime.now(ET).date().isoformat(), "equity": live,
                      "cum_ret_pct": rd((live / base - 1) * 100, 3) if base else None,
                      "intraday": True})
    return {"equity": live,
            "cash": rd(float(acct["cash"]), 2),
            "account_number": acct.get("account_number"),
            "paper": api.is_paper, "endpoint": api.base,
            "curve": curve,
            "open_positions": [{"symbol": p["symbol"], "qty": float(p["qty"]),
                                "avg_entry_price": rd(float(p["avg_entry_price"]), 4),
                                "unrealized_pl": rd(float(p["unrealized_pl"]), 2),
                                "market_value": rd(float(p["market_value"]), 2)}
                               for p in (pos or [])]}, None


# -------------------------------------------------------------- the statistics

def ranking_stats(rows):
    """Can the day be ranked -- research level, every name, traded or not."""
    live = [r for r in rows if not r["duplicate_event"] and r.get("mv_close") is not None]
    days = panel_of(live)
    out = {"n": len(live), "days": len(days)}
    for xkey, lab in (("impact_sum", "rho_impact_sum"),
                      ("neg_runup", "rho_control_neg_runup"),
                      ("impact_sum_pre_lessons", "rho_pre_lessons"),
                      ("edge_score_legacy", "rho_legacy_key")):
        rho, n = EX.pooled_rho(days, xkey, "mv_close")
        if rho is not None:
            out[lab] = rho
            out[lab + "_n"] = n
    crho, cn = EX.conviction_rho(live, "impact_sum", "mv_close")
    out["rho_conviction_vs_sign"] = crho
    out["n_conviction"] = cn
    nz = [r for r in live if r["impact_sum"]]
    out["sign_hits"] = sum(1 for r in nz if (r["impact_sum"] > 0) == (r["mv_close"] > 0))
    out["sign_n"] = len(nz)
    out["per_day"] = []
    for d in days:
        rho, _ = EX.pooled_rho([d], "impact_sum", "mv_close")
        ctl, _ = EX.pooled_rho([d], "neg_runup", "mv_close")
        floor = [r["ret_close"] for r in d
                 if r["conviction"] >= 3.0 and r.get("ret_close") is not None]
        out["per_day"].append({
            "run_date": d[0]["run_date"], "n": len(d), "rho": rho, "rho_control": ctl,
            "floor_n": len(floor),
            "floor_mean_ret_pct": rd(st.fmean(floor), 3) if floor else None})
    return out


def bucket_stats(rows, floor):
    live = [r for r in rows if not r["duplicate_event"] and r.get("ret_close") is not None]
    out = {"by_abs_impact": [], "by_signed_impact": [], "by_adv": [],
           "by_session": {}, "scatter": []}
    for lo, hi in ABS_BUCKETS:
        grp = [r for r in live if lo <= r["conviction"] < hi]
        if not grp:
            continue
        s = book_stats([r["ret_close"] for r in grp])
        out["by_abs_impact"].append({"label": f"{lo}–{hi if hi < 999 else '∞'}",
                                     "lo": lo, "hi": hi, **s})
    for lab, sel in (("short (impact < 0)", lambda r: r["impact_sum"] < 0),
                     ("long (impact > 0)", lambda r: r["impact_sum"] > 0)):
        grp = [r for r in live if sel(r)]
        if grp:
            out["by_signed_impact"].append({"label": lab, **book_stats(
                [r["ret_close"] for r in grp])})
    for lo, hi in ADV_BUCKETS:
        grp = [r for r in live
               if (r.get("dollar_vol") or r.get("plan_dollar_volume_usd") or 0) >= lo
               and (r.get("dollar_vol") or r.get("plan_dollar_volume_usd") or 0) < hi]
        if not grp:
            continue
        lab = (f"<${hi/1e6:g}m" if lo == 0 else
               f"≥${lo/1e6:g}m" if hi > 1e14 else f"${lo/1e6:g}–{hi/1e6:g}m")
        out["by_adv"].append({"label": lab, "lo": lo, "hi": hi,
                              **book_stats([r["ret_close"] for r in grp]),
                              "above_floor": sum(1 for r in grp
                                                 if r["conviction"] >= floor)})
    for sess in ("amc", "bmo"):
        grp = [r for r in live if r["session"] == sess and r["conviction"] >= floor]
        if grp:
            out["by_session"][sess] = book_stats([r["ret_close"] for r in grp])
    out["scatter"] = [{"ticker": r["ticker"], "run_date": r["run_date"],
                       "impact_sum": r["impact_sum"], "move": r["mv_close"],
                       "ret": r["ret_close"], "session": r["session"],
                       "dollar_vol": r.get("dollar_vol") or r.get("plan_dollar_volume_usd"),
                       "traded": bool(r.get("traded"))}
                      for r in live]
    return out


def lessons_stats(rows):
    """The only thing that scores edge/LESSONS.md. Empty until hunters return
    `pre_lessons`; an empty block is the honest answer, not a missing tab."""
    live = [r for r in rows if not r["duplicate_event"]
            and r.get("mv_close") is not None
            and r.get("impact_sum_pre_lessons") is not None]
    out = {"n": len(live), "days": len({r["run"] for r in live}),
           "coverage_note": None, "rows": []}
    if not live:
        out["coverage_note"] = ("Geen enkele run draagt `impact_sum_pre_lessons`. De "
                                "hunter-contract vraagt `pre_lessons` sinds "
                                "2026-09-16; zolang hunters het niet teruggeven valt "
                                "er niets te vergelijken en blijft dit leeg.")
        return out
    days = panel_of(live)
    for xkey, lab in (("impact_sum", "rho_after"),
                      ("impact_sum_pre_lessons", "rho_before")):
        rho, n = EX.pooled_rho(days, xkey, "mv_close")
        out[lab] = rho
    out["book_after"] = book_stats([r["ret_close"] for r in live
                                    if r["conviction"] >= 3.0])
    out["book_before"] = book_stats(
        [(r["mv_close"] if r["impact_sum_pre_lessons"] > 0 else -r["mv_close"])
         for r in live if abs(r["impact_sum_pre_lessons"]) >= 3.0])
    out["rows"] = [{"run_date": r["run_date"], "ticker": r["ticker"],
                    "before": r["impact_sum_pre_lessons"], "after": r["impact_sum"],
                    "delta": rd(r["impact_sum"] - r["impact_sum_pre_lessons"], 3),
                    "move": r["mv_close"]} for r in live]
    return out


def timing_stats(rows, floor, seed=20260917):
    live = [r for r in rows if not r["duplicate_event"]]
    days = panel_of(live)
    out = {"horizons": EX.HORIZONS, "all": {}, "amc": {}, "bmo": {}}
    for h in EX.HORIZONS:
        out["all"][h] = EX.horizon_stats(days, f"mv_{h}", seed, floor)
        for sess in ("amc", "bmo"):
            sd = [[r for r in d if r["session"] == sess] for d in days]
            sd = [d for d in sd if d]
            out[sess][h] = EX.horizon_stats(sd, f"mv_{h}", seed, floor) if sd else {"n": 0}
    out["hourly"] = EX.hourly_returns(days, floor)
    out["legs"] = EX.leg_stats(days, floor)
    return out


def trading_stats(trades, names, account):
    closed = [t for t in trades if t["closed"] and t.get("ret_pct") is not None]
    out = {"n_closed": len(closed), "n_open": sum(1 for t in trades if not t["closed"])}
    if closed:
        out["per_trade"] = book_stats([t["ret_pct"] for t in closed])
        out["total_pnl_usd"] = rd(sum(t["pnl_usd"] for t in closed), 2)
        out["gross_entry_notional_usd"] = rd(
            sum(t["entry_notional_usd"] or 0 for t in closed), 2)
        out["return_on_notional_pct"] = rd(
            100 * out["total_pnl_usd"] / out["gross_entry_notional_usd"], 3) \
            if out["gross_entry_notional_usd"] else None
        for lab, sel in (("long", lambda t: t["side"] == "long"),
                         ("short", lambda t: t["side"] == "short")):
            g = [t["ret_pct"] for t in closed if sel(t)]
            if g:
                out.setdefault("by_side", {})[lab] = book_stats(g)
        for sess in ("amc", "bmo"):
            g = [t["ret_pct"] for t in closed if t.get("session") == sess]
            if g:
                out.setdefault("by_session", {})[sess] = book_stats(g)
        for src in ("stage E", "manual"):
            g = [t["ret_pct"] for t in closed if t.get("exit_source") == src]
            if g:
                out.setdefault("by_exit_source", {})[src] = book_stats(g)
        held = [t["hold_hours"] for t in closed if t.get("hold_hours")]
        out["hold_hours"] = {"median": rd(st.median(held), 2) if held else None,
                             "max": rd(max(held), 2) if held else None,
                             "over_24h": sum(1 for h in held if h > 30)}
    # Daily book: what was deployed, what came back, and on what turnover.
    dayrows = {}
    for t in trades:
        d = t["entry_utc"][:10]
        b = dayrows.setdefault(d, {"date": d, "n": 0, "notional_usd": 0.0,
                                   "pnl_usd": 0.0, "closed": 0, "turnover_usd": 0.0,
                                   "symbols": []})
        b["n"] += 1
        b["symbols"].append(t["symbol"])
        b["notional_usd"] += t["entry_notional_usd"] or 0
        b["turnover_usd"] += t["entry_notional_usd"] or 0
        if t["closed"] and t.get("pnl_usd") is not None:
            b["pnl_usd"] += t["pnl_usd"]
            b["closed"] += 1
            b["turnover_usd"] += abs((t["exit_px"] or 0) * (t["qty"] or 0))
    curve = {c["date"]: c["equity"] for c in ((account or {}).get("curve") or [])}
    daily = []
    for d, b in sorted(dayrows.items()):
        eq = curve.get(d)
        daily.append({**b, "symbols": ",".join(b["symbols"]),
                      "notional_usd": rd(b["notional_usd"], 2),
                      "turnover_usd": rd(b["turnover_usd"], 2),
                      "pnl_usd": rd(b["pnl_usd"], 2),
                      "equity_usd": eq,
                      "gross_pct_of_equity": rd(100 * b["notional_usd"] / eq, 1) if eq else None,
                      "ret_on_notional_pct": rd(100 * b["pnl_usd"] / b["notional_usd"], 3)
                      if b["notional_usd"] else None,
                      "ret_on_equity_pct": rd(100 * b["pnl_usd"] / eq, 3) if eq else None})
    out["daily"] = daily
    # The free control, priced over the SAME days money was on the table: short
    # every name in that day's run and do no research at all.
    traded_days = {t.get("run_date") for t in trades if t.get("run_date")}
    ctl = []
    for r in names:
        if r["run_date"] in traded_days and r.get("mv_close") is not None \
                and not r["duplicate_event"]:
            ctl.append(-r["mv_close"])
    if len(ctl) >= 3:
        out["control_short_everything"] = book_stats(ctl)
    if account and account.get("curve"):
        eqs = [c["equity"] for c in account["curve"]]
        peak, dd = eqs[0], 0.0
        for e in eqs:
            peak = max(peak, e)
            dd = min(dd, e / peak - 1)
        out["equity"] = {"start": eqs[0], "last": eqs[-1],
                         "return_pct": rd((eqs[-1] / eqs[0] - 1) * 100, 3),
                         "max_drawdown_pct": rd(dd * 100, 2),
                         "days": len(eqs)}
    return out


def execution_gap_stats(trades):
    """Theoretical against actual, over the closed positions."""
    cl = [t for t in trades if t.get("ret_pct") is not None]
    out = {"n": len(cl)}
    pol = [t["policy_gap_pct"] for t in cl if t.get("policy_gap_pct") is not None]
    ex = [t["exec_gap_pct"] for t in cl if t.get("exec_gap_pct") is not None]
    if pol:
        out["policy_gap"] = ttest(pol)
        out["actual_mean"] = rd(st.fmean(t["ret_pct"] for t in cl
                                         if t.get("policy_gap_pct") is not None), 3)
        out["theoretical_mean"] = rd(st.fmean(t["theo_ret_close_pct"] for t in cl
                                              if t.get("policy_gap_pct") is not None), 3)
    if ex:
        out["exec_gap"] = ttest(ex)
    return out


def link_trades_to_names(trades, names):
    idx = {(t.get("run_date"), t["symbol"]): t for t in trades if t.get("run_date")}
    for r in names:
        t = idx.get((r["run_date"], r["ticker"]))
        if t:
            r["traded"] = True
            r["trade_ret_pct"] = t.get("ret_pct")
            r["trade_pnl_usd"] = t.get("pnl_usd")
            r["trade_notional_usd"] = t.get("entry_notional_usd")
        else:
            r["traded"] = False


def write_csv(path, rows, cols):
    import csv
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", nargs="*", default=["research/*/*/*/edge"])
    ap.add_argument("--cache", default=str(ROOT / ".cache" / "bars"),
                    help="Yahoo chart cache; delete it to re-price everything")
    ap.add_argument("--offline", action="store_true",
                    help="skip the broker; keep the account block from the last build")
    ap.add_argument("--floor", type=float, default=None,
                    help="conviction floor; default reads config/pipeline.yaml")
    ap.add_argument("--out", default=str(DATA / "ledger.json"))
    a = ap.parse_args()

    floor = a.floor
    if floor is None:
        try:
            import yaml
            cfg = yaml.safe_load((ROOT / "config" / "pipeline.yaml").read_text())
            floor = float((cfg.get("edge_hunt") or {}).get("conviction_floor", 3.0))
        except Exception:
            floor = 3.0

    runs = []
    for pat in a.runs:
        runs.extend(sorted(glob.glob(str(ROOT / pat)) or glob.glob(pat)))
    runs = [str(Path(r).relative_to(ROOT)) if str(r).startswith(str(ROOT)) else r
            for r in runs]
    os.makedirs(a.cache, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    print(f"runs: {len(runs)}")
    names, problems = load_names(runs, a.cache)
    print(f"names priced: {len(names)}   problems: {len(problems)}")

    trades, open_eps, account, broker_err = [], [], None, None
    if a.offline:
        broker_err = "offline: broker not contacted"
    else:
        api = Alpaca()
        if not api.usable:
            broker_err = "no ALPACA_API_KEY_ID / ALPACA_API_SECRET_KEY in the environment"
        else:
            fl, ferr = fills(api)
            if ferr:
                broker_err = f"fills: {ferr}"
            else:
                trades, open_eps = round_trips(fl, order_index(runs))
                print(f"fills: {len(fl)}   round trips: {len(trades)} closed, "
                      f"{len(open_eps)} open")
            account, aerr = account_block(api)
            if aerr:
                broker_err = (broker_err or "") + f" account: {aerr}"
    if broker_err and Path(a.out).exists():
        old = json.loads(Path(a.out).read_text())
        trades = trades or old.get("trades", [])
        open_eps = open_eps or old.get("open_positions", [])
        account = account or old.get("account")
        problems.append(f"broker unreachable, kept the previous build's trades: {broker_err}")

    all_eps = trades + open_eps
    link_trades_to_names(all_eps, names)

    # Sector, industry and tradability, so the dashboard can slice and filter on
    # them. Both are cached; neither is on the critical path of a rebuild.
    tickers = [r["ticker"] for r in names]
    sec = sectors_for(tickers, DATA / "sectors.json")
    day_assets, live_assets = assets_for(
        tickers, (None if a.offline else Alpaca()), runs, DATA / "assets.json")
    for r in names:
        m = sec.get(r["ticker"], {})
        r["sector"] = m.get("sector")
        r["industry"] = m.get("industry")
        r["company"] = m.get("name")
        da = day_assets.get((r["run"], r["ticker"]))
        la = live_assets.get(r["ticker"], {})
        r["shortable"] = (da or {}).get("shortable", la.get("shortable"))
        r["easy_to_borrow"] = la.get("easy_to_borrow")
        r["tradable_flag"] = (da or {}).get("tradable", la.get("tradable"))
        r["tradable_reason"] = (da or {}).get("tradable_reason")
        r["asset_asof"] = (da or {}).get("asset_asof", "live lookup, not day-of")
    attach_theoretical(all_eps, names)
    costs = costs_for(runs, names)

    doc = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "conviction_floor": floor,
        "runs": runs,
        "broker_error": broker_err,
        "names": names,
        "trades": all_eps,
        "account": account,
        "stats": {
            "ranking": ranking_stats(names),
            "buckets": bucket_stats(names, floor),
            "lessons": lessons_stats(names),
            "timing": timing_stats(names, floor),
            "trading": trading_stats(all_eps, names, account),
            "execution": execution_gap_stats(all_eps)},
        "costs": costs,
        "hour_grid": EX.HOUR_GRID,
        "horizons": EX.HORIZONS,
        "problems": problems}

    Path(a.out).write_text(json.dumps(doc, indent=1, default=str) + "\n", encoding="utf-8")
    write_csv(DATA / "names.csv", names,
              ["run_date", "ticker", "session", "event_date", "entry_date",
               "reaction_date", "rank", "impact_sum", "conviction",
               "impact_sum_pre_lessons", "lessons_delta", "n_findings", "neg_runup",
               "dollar_vol", "plan_dollar_volume_usd", "sector", "industry",
               "shortable", "easy_to_borrow", "tradable_flag", "duplicate_event", "traded",
               "entry_close", "mv_open", "mv_close", "ret_open", "ret_close",
               "trade_ret_pct", "trade_pnl_usd"])
    write_csv(DATA / "trades.csv", all_eps,
              ["run_date", "symbol", "side", "session", "event_date", "closed",
               "qty", "entry_px", "exit_px", "entry_utc", "exit_utc", "hold_hours",
               "entry_notional_usd", "ret_pct", "pnl_usd", "impact_sum",
               "entry_source", "exit_source", "exit_tif", "n_exit_fills",
               "partial_exit_days", "entry_spread_pct", "theo_ret_close_pct",
               "policy_gap_pct", "theo_exit_hour", "theo_ret_at_exit_pct",
               "exec_gap_pct"])

    s = doc["stats"]
    print(f"\nranking   rho={s['ranking'].get('rho_impact_sum')} "
          f"control={s['ranking'].get('rho_control_neg_runup')} "
          f"conviction={s['ranking'].get('rho_conviction_vs_sign')} "
          f"(n={s['ranking']['n']} over {s['ranking']['days']} days)")
    tr = s["trading"]
    if tr.get("per_trade"):
        print(f"trades    {tr['n_closed']} closed, {tr['per_trade']['hit_rate_pct']}% up, "
              f"mean {tr['per_trade']['mean']}%, P&L ${tr['total_pnl_usd']}")
    if tr.get("equity"):
        print(f"equity    {tr['equity']['start']} -> {tr['equity']['last']} "
              f"({tr['equity']['return_pct']}%), max drawdown "
              f"{tr['equity']['max_drawdown_pct']}%")
    if tr.get("control_short_everything"):
        print(f"control   short everything: {tr['control_short_everything']['mean']}% "
              f"per name over the same days")
    for p in problems[:12]:
        print("  !", p)
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()

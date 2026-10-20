#!/usr/bin/env python3
"""The compact scorebord: only the STRONG scores, live and resolved.

Two questions, one page (`dashboard/scorebord.html`):

  1. Which strong calls are open right now, and what have they earned so far?
  2. Per stage, prompt version and model: what did the strong calls earn once resolved?

A "strong score" is one of two things, nothing else:

  * hunter stages (US E, D, EU, JP, AU, CA): |impact_sum| in the top 20% of the
    SAME model's reference names, as `score_report.Percentiles` measured it before
    that run (the bracket score_report printed that day). For Opus 5.5 that cut is
    the 2.8 floor; for Opus 5 it is 5.25.
  * US E-P panel (since 2026-10-14): the MEAN of the four judges' percentiles, each
    judge read against its own live range before that run, is in the top 20%
    (|panel_pct| >= 80). Applied to every E-P run, the ones scored under the old rule
    included, so the page measures the rule in force. The side is the mean's.
  * the market panels (EU/JP/AU/CA): unchanged, 3 of 4 judges with the name in their
    own top 20%. Their score column shows panel_pct as well.

A third question since 2026-10-14: the panel per own top, forward. For every panel and
every top X% (10..100), what did trading every name with |panel_pct| >= 100 - X earn,
and inside the top, did the names the judges agreed on most do better than the ones
they agreed on least? Measured on this page's own windows, point in time.

And since the same day, per US panel name the expected return on the trade
(`panel_calibrate.py`), one number per percentile: recorded by the scorer on runs scored
since then, read off the frozen curve here for older ones, with the curve drawn beside
what each band of percentiles actually earned (backtest and October). All of it sits
on its own tab, "Panel %".

Resolved outcomes are read, never recomputed, wherever a resolver already wrote one:
the US ledger's own bars for E and E-P on the operator's window (see US_ENTRY_HM),
frozen once resolved, the market resolvers
through `markets.json` for EU/JP/AU/CA. Stage R is left out on purpose: it is a
different event (yesterday's losers, not an earnings print) and does not belong here.
Stage D (three deep names a day) is left out too, on the operator's instruction of
2026-10-14.
Live returns come from Yahoo at build time. Read-only: no order is ever touched.

Run after `build_ledger.py` and `build_markets.py`; `update.sh` does that.
"""
import glob
import json
import math
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import provenance as PROV          # noqa: E402
import score_report as SR          # noqa: E402
sys.path.insert(0, str(ROOT / "researcher_us" / "scripts"))
import panel_score as PS           # noqa: E402
import panel_calibrate as PC       # noqa: E402

PCT = SR.Percentiles()
TOP = 80.0                          # top 20% of the model's own reference
DATA = ROOT / "dashboard" / "data"
OUT_HTML = ROOT / "dashboard" / "scorebord.html"
OUT_JSON = DATA / "scorebord.json"
TODAY = datetime.now(timezone.utc).date()
LOOKBACK_DAYS = 6                   # runs this recent can still have an open window
ET = ZoneInfo("America/New_York")
# The US window, as the operator set it (2026-10-13): BUY at 13:30 ET on the entry
# day (the report day for amc, the session before it for bmo); SELL amc at the next
# day's opening print and bmo at 13:00 ET on the report day. Resolved and running
# calls are priced on this one window. It is NOT the ledger's `mv_strategy`, which
# enters at the close and sells bmo at 14:00 ET.
US_ENTRY_HM = 13 * 60 + 30
BMO_EXIT_HM = 13 * 60
FROZEN_PATH = DATA / "scorebord-frozen.json"


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


# ---------------------------------------------------------------- prices

_cache = {}


def chart(sym):
    """Daily bars for the last month plus the live quote. None on failure."""
    if sym in _cache:
        return _cache[sym]
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
           "?range=3mo&interval=1d")
    out = None
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            r = json.load(urllib.request.urlopen(req, timeout=20))["chart"]["result"][0]
            m, q = r["meta"], r["indicators"]["quote"][0]
            off = m.get("gmtoffset", 0)
            bars = {}
            for ts, o, c in zip(r.get("timestamp") or [], q["open"], q["close"]):
                d = datetime.fromtimestamp(ts + off, timezone.utc).date().isoformat()
                bars[d] = (o, c)
            out = {"bars": bars, "price": m.get("regularMarketPrice"),
                   "time": m.get("regularMarketTime")}
            break
        except Exception:
            time.sleep(1 + i)
    _cache[sym] = out
    return out


def intraday_at(sym, day, hm):
    """Last 5-minute close at or before `hm` (minutes ET) on `day`, within an hour."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
           "?range=10d&interval=5m")
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            r = json.load(urllib.request.urlopen(req, timeout=20))["chart"]["result"][0]
            q = r["indicators"]["quote"][0]
            best = None
            for ts, c in zip(r.get("timestamp") or [], q["close"]):
                d = datetime.fromtimestamp(ts, ET)
                m = d.hour * 60 + d.minute
                if c is not None and d.date().isoformat() == day and hm - 60 <= m <= hm:
                    best = c
            return best
        except Exception:
            time.sleep(1 + i)
    return None


def window(sym, start, start_is_close_before, end_at_open=False, end_hm=None):
    """Price a window that starts at a close and ends at the next session's close
    (or open). `start` is the event date; when `start_is_close_before` the reference is
    the last close strictly before it (a bmo print), else the close on it.
    Returns dict(ref, last, move, state) or None."""
    q = chart(sym)
    if not q or not q["bars"]:
        return None
    # Yahoo leaves a null close on some European sessions for a day or more; a day
    # without a close can be neither the reference nor the end of a window.
    days = sorted(d for d, (o, c) in q["bars"].items() if c is not None)
    before = [d for d in days if (d < start if start_is_close_before else d <= start)]
    if not before:
        return None
    ref_day = before[-1]
    if not start_is_close_before and ref_day != start:
        # The reference is the event day's own close and it is not printed yet.
        return {"ref": None, "ref_day": None, "last": None, "move": None, "state": "wacht"}
    ref = q["bars"][ref_day][1]
    after = [d for d in days if d > ref_day]
    if not after:
        return {"ref": ref, "ref_day": ref_day, "last": None, "move": None,
                "state": "wacht"}
    end_day = after[0]
    # The window ends on the FIRST session after the reference, printed or not. Yahoo
    # leaves a European session's close null for a day or two (AIRA.ST and ITM.L on
    # 2026-10-19, read on 10-20), and skipping that day priced the window to the next
    # session instead, shown as running. A passed session with no close waits.
    first = min((d for d in q["bars"] if d > ref_day), default=end_day)
    if first != end_day and first < TODAY.isoformat() and not end_at_open and end_hm is None:
        return {"ref": ref, "ref_day": ref_day, "last": None, "move": None,
                "state": "wacht"}
    o, c = q["bars"][end_day]
    now_et = datetime.now(ET)
    if end_hm is not None and end_day == now_et.date().isoformat() \
            and now_et.hour * 60 + now_et.minute < end_hm:
        last, state = q.get("price"), "loopt"
    elif end_hm is not None:
        last, state = intraday_at(sym, end_day, end_hm), "gesloten"
    elif end_at_open:
        last, state = o, "gesloten"
    elif end_day == TODAY.isoformat() and q.get("time") and \
            time.time() - q["time"] < 3600 and q.get("price"):
        last, state = q["price"], "loopt"
    else:
        last, state = c, ("gesloten" if end_day < TODAY.isoformat() else "loopt")
    if not ref or not last:
        return None
    return {"ref": ref, "ref_day": ref_day, "end_day": end_day, "last": last,
            "move": (last / ref - 1) * 100, "state": state}


def _hm_now():
    n = datetime.now(ET)
    return n.date().isoformat(), n.hour * 60 + n.minute


# A resolved US move is frozen the first time it is computed with its exit day behind
# us, so a later build cannot move it: on 2026-10-13 PENG's opening print came back as
# 67.28 on one CI build and 66.00 on the next, which moved the call by two points.
FROZEN = load(FROZEN_PATH) or {}
US_PX = {}      # "run_date|ticker" -> (entry, exit) behind every resolved US move


def us_px(n):
    return US_PX.get(f"{n['run_date']}|{n['ticker']}") if n else None


# Entry and exit prices of a resolved non-US call, from the market's own resolver file
# (Japan entry_price/exit_close, Canada entry/exit, Australia from_price/to_price), else
# re-priced from Yahoo on the same window. A pair is kept only when it reproduces the
# resolver's move, so the page never shows a price that is not behind the number.
_resolved_rows = {}


def market_px(n, resolved_file, sym, start_is_close_before, end_at_open):
    run = n["run"]
    if run not in _resolved_rows:
        d = load(ROOT / run / resolved_file) or {}
        rows = d.get("rows") or d.get("ranking") or d.get("names") or []
        _resolved_rows[run] = {r.get("ticker"): r for r in rows if isinstance(r, dict)}
    r = _resolved_rows[run].get(n["ticker"]) or {}
    mv = n.get("realised_move_pct")
    pairs = [(r.get("entry_price"), r.get("exit_close")), (r.get("entry"), r.get("exit")),
             (r.get("from_price"), r.get("to_price"))]
    for a, b in pairs:
        if a and b and mv is not None and abs((b / a - 1) * 100 - mv) < 0.2:
            return a, b
    w = window(sym, n["event_date"], start_is_close_before, end_at_open=end_at_open)
    if w and w.get("ref") and w.get("last") and mv is not None \
            and abs((w["last"] / w["ref"] - 1) * 100 - mv) < 0.2:
        return w["ref"], w["last"]
    return None


def us_move(n):
    """Resolved US move on the operator's window, from the ledger's own bars:
    13:30 ET entry (`enpx`), amc out at the next day's opening print (Yahoo's daily
    open, the consolidated one, else the ledger's 09:30 bar), bmo out at 13:00 ET on
    the report day (`hr_21`). None while the exit has not happened or a price is
    missing. Never the close: a call with no 13:30 price is left unresolved."""
    key = f"{n['run_date']}|{n['ticker']}"
    if key in FROZEN:
        US_PX[key] = (FROZEN[key].get("entry"), FROZEN[key].get("exit"))
        return FROZEN[key]["move"]
    entry = (n.get("enpx") or {}).get("1330")
    px, ed = n.get("px") or {}, n.get("entry_date")
    if not entry or not ed or n.get("pending"):
        return None
    exit_px, exit_day = None, None
    if n.get("session") == "amc":
        q = chart(n["ticker"])
        later = sorted(d for d in (q or {}).get("bars", {}) if d > ed)
        if later and q["bars"][later[0]][0]:
            exit_day, exit_px = later[0], q["bars"][later[0]][0]
        elif px.get("open"):
            exit_px, exit_day = px["open"], n.get("reaction_date") or n.get("event_date")
    elif n.get("hr_21") is not None and n.get("entry_close"):
        exit_px = n["entry_close"] * (1 + n["hr_21"] / 100)
        exit_day = n.get("reaction_date") or n.get("event_date")
    if not exit_px:
        return None
    move = (exit_px / entry - 1) * 100
    US_PX[key] = (entry, exit_px)
    if exit_day and exit_day < TODAY.isoformat():
        FROZEN[key] = {"entry": round(entry, 4), "exit": round(exit_px, 4),
                       "move": round(move, 3), "session": n.get("session"),
                       "exit_day": exit_day}
    return move


def us_move_any(n, ticker, run_date, event_date, session):
    """us_move() when the stage E ledger has the name, else the same window priced
    directly. Since 2026-10-15 stage E has written no run to this repo, so E-P names
    had no ledger row and stayed "gesloten" for good, then "niet opgelost" once their
    run left LOOKBACK_DAYS. A window whose exit has happened is a result: it is
    returned, and frozen once the exit day is behind us, like every other US move."""
    mv = us_move(n) if n else None
    if mv is not None:
        return mv
    key = f"{run_date}|{ticker}"
    if key in FROZEN:
        US_PX[key] = (FROZEN[key].get("entry"), FROZEN[key].get("exit"))
        return FROZEN[key]["move"]
    if not event_date or not recent(run_date):
        return None
    w = us_live(ticker, event_date, session)
    if not w or w["state"] != "gesloten" or w.get("move") is None:
        return None
    US_PX[key] = (w["ref"], w["last"])
    if w.get("end_day") and w["end_day"] < TODAY.isoformat():
        FROZEN[key] = {"entry": round(w["ref"], 4), "exit": round(w["last"], 4),
                       "move": round(w["move"], 3), "session": session,
                       "exit_day": w["end_day"]}
    return w["move"]


def us_live(sym, event_date, session):
    """A running US call on the same window: entry at 13:30 ET, amc out at the next
    open, bmo out at 13:00 ET on the report day; the live price in between."""
    q = chart(sym)
    if not q or not q["bars"] or not event_date:
        return None
    days = sorted(d for d, (o, c) in q["bars"].items() if c is not None)
    today, now = _hm_now()
    if session == "amc":
        entry_day = event_date if event_date in days else None
    else:
        before = [d for d in days if d < event_date]
        entry_day = before[-1] if before else None
    if not entry_day or (entry_day == today and now < US_ENTRY_HM):
        return {"ref": None, "ref_day": entry_day, "last": None, "move": None, "state": "wacht"}
    entry = intraday_at(sym, entry_day, US_ENTRY_HM)
    if not entry:
        return None
    after = [d for d in days if d > entry_day]
    exit_day = after[0] if after else None
    if session == "amc":
        if exit_day and q["bars"][exit_day][0]:
            last, state = q["bars"][exit_day][0], "gesloten"
        else:
            last, state = q.get("price"), "loopt"
    else:
        if exit_day and (exit_day < today or now >= BMO_EXIT_HM):
            last, state = intraday_at(sym, exit_day, BMO_EXIT_HM), "gesloten"
        else:
            last, state = q.get("price"), "loopt"
    if not last:
        return None
    return {"ref": entry, "ref_day": entry_day, "end_day": exit_day, "last": last,
            "move": (last / entry - 1) * 100, "state": state}


# ---------------------------------------------------------------- statistics

def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-30 else 1e-30)
    h = d
    for m in range(1, 200):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-30 else 1e-30
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-30 else 1e-30)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-30 else 1e-30
        de = d * c
        h *= de
        if abs(de - 1) < 1e-10:
            break
    return h


def t_pvalue(t, df):
    """Two-sided p of a Student t."""
    x = df / (df + t * t)
    lb = math.lgamma(df / 2 + 0.5) - math.lgamma(df / 2) - math.lgamma(0.5)
    bt = math.exp(lb + (df / 2) * math.log(x) + 0.5 * math.log(1 - x)) if 0 < x < 1 else 0
    if x < (df / 2 + 1) / (df / 2 + 0.5 + 2):
        ib = bt * _betacf(df / 2, 0.5, x) / (df / 2)
    else:
        ib = 1 - bt * _betacf(0.5, df / 2, 1 - x) / 0.5
    return min(1.0, max(0.0, ib))


def summarise(rets):
    n = len(rets)
    out = {"n": n, "hit": None, "mean": None, "t": None, "p": None}
    if not n:
        return out
    out["hit"] = 100 * sum(1 for r in rets if r > 0) / n
    out["mean"] = sum(rets) / n
    if n >= 3:
        sd = math.sqrt(sum((r - out["mean"]) ** 2 for r in rets) / (n - 1))
        if sd:
            out["t"] = out["mean"] / (sd / math.sqrt(n))
            out["p"] = t_pvalue(out["t"], n - 1)
    return out


# ---------------------------------------------------------------- collection

def prov(run, market, submarket=None):
    try:
        p = PROV.for_row(ROOT / run, market, submarket)
    except Exception:
        p = {}
    return p.get("prompt_version"), p.get("model"), p.get("model_short"), \
        bool(p.get("sept_opus55"))


def pctile(run, model, value):
    try:
        return PCT.of(ROOT / run, model, value)[1]
    except Exception:
        return None


def sign(v):
    return 1 if v and v > 0 else -1 if v and v < 0 else 0


# ---------------------------------------------------------------- panel percentiles
# One definition with the scorer: panel_score.live_reference reads each judge's live
# sizes from runs dated before this one. A run scored since 2026-10-14 carries its own
# `panel_pct`; an older run is computed here the same way, point in time.
PANEL_HIST = {"US": ("researcher_us/analysis/panel-history.json", "seed"),
              "EU": ("researcher_europe/analysis/panel-history.json", "us_live"),
              "JP": ("researcher_japan/analysis/panel-history.json", "us_live"),
              "AU": ("researcher_australia/analysis/panel-history.json", "us_live"),
              "CA": ("researcher_canada/analysis/panel-history.json", "us_live")}
PANEL_TOP = 80.0
_hist, _ppct = {}, {}


def panel_pcts(run, region):
    """ticker -> {panel_pct, sd, full} for one panel run, recorded or computed. Here
    panel_pct is SIGNED (side x strength), for arithmetic; every display shows the 0-100
    strength and the side apart."""
    key = (str(run), region)
    if key in _ppct:
        return _ppct[key]
    doc = load(ROOT / run / "edge-scores-panel.json") or {}
    rows = doc.get("ranking") or []
    out = {}
    present = doc.get("members_present") or list(PS.MEMBERS)
    if rows and all("panel_pct_signed" in r for r in rows):
        for r in rows:
            out[r["ticker"]] = {"panel_pct": r["panel_pct_signed"], "sd": r.get("panel_pct_sd"),
                                "full": r.get("n_members") == len(present)}
    elif rows:
        path, fb = PANEL_HIST[region]
        if path not in _hist:
            _hist[path] = load(ROOT / path) or {}
        hist = _hist[path]
        before = PS.date_of(Path(run).parent.name)
        ids = {r.get("id") for r in rows}
        refs = {m: PS.live_reference(hist, m, 200, before=before, exclude=ids,
                                     fallback=PS.fallback_rows(fb, hist))[0] for m in present}
        for r in rows:
            ps = [PS.pct_of(refs[m], (r["members"].get(m) or {}).get("impact_sum") or 0.0)
                  for m in present if m in r["members"]]
            if not ps:
                continue
            mu = sum(ps) / len(ps)
            out[r["ticker"]] = {"panel_pct": round(mu, 1),
                                "sd": round(math.sqrt(sum((x - mu) ** 2 for x in ps) / len(ps)), 1),
                                "full": len(ps) == len(present)}
    _ppct[key] = out
    return out


resolved = []          # dicts: stage, market, version, model, ticker, run_date, side, ret, kind
live = []

ledger = load(DATA / "ledger.json") or {"names": []}
by_run_ticker = {(n["run_date"], n["ticker"]): n for n in ledger["names"]}
markets = (load(DATA / "markets.json") or {}).get("markets", {})


def recent(run_date):
    try:
        d = date.fromisoformat(run_date)
    except Exception:
        return False
    return TODAY - timedelta(days=LOOKBACK_DAYS) <= d <= TODAY + timedelta(days=1)


def live_row(**kw):
    live.append(kw)


# US stage E: the ledger already carries version, model, percentile and outcome.
for n in ledger["names"]:
    if n.get("sept_opus55") or n.get("duplicate_event") or n.get("rankable") is False:
        continue
    if not n.get("impact_sum") or (n.get("impact_pctile_all") or 0) < TOP:
        continue
    side = sign(n["impact_sum"])
    mv = us_move(n)
    if mv is not None:
        resolved.append(dict(stage="US · E", version=n["prompt_version"],
                             model=n["model_short"], ticker=n["ticker"],
                             run_date=n["run_date"], ret=side * mv,
                             kind="top 20%"))
    elif recent(n["run_date"]):
        w = us_live(n["ticker"], n["event_date"], n["session"])
        live_row(stage="US · E", ticker=n["ticker"], company=n.get("company"),
                 run_date=n["run_date"], score=n["impact_sum"],
                 why=f"top {100 - n['impact_pctile_all']:.0f}% {n['model_short']}",
                 side=side, w=w, session=n.get("session"))


def us_side_stage(glob_pat, stage, market, picker):
    key_is_panel = picker is pick_panel
    """E-P and D: pick the strong names of each run, outcome from the stage E ledger
    (same universe, same window), else live."""
    for f in sorted(glob.glob(str(ROOT / glob_pat))):
        run = str(Path(f).parent.relative_to(ROOT))
        run_date = Path(f).parent.parent.name
        ver, model, mshort, sept = prov(run, market)
        if sept:
            continue
        for r, side, why in picker(run, f, model):
            n = by_run_ticker.get((run_date, r["ticker"]))
            b = load(ROOT / run / "baselines" / f"{r['ticker']}.json") or {}
            mv = us_move_any(n, r["ticker"], run_date, b.get("event_date"),
                             b.get("session") or (n or {}).get("session"))
            if mv is not None:
                resolved.append(dict(stage=stage, version=ver,
                                     model="panel" if key_is_panel else mshort,
                                     ticker=r["ticker"], run_date=run_date,
                                     ret=side * mv, kind=why))
            elif recent(run_date):
                w = us_live(r["ticker"], b.get("event_date") or run_date, b.get("session"))
                live_row(stage=stage, ticker=r["ticker"], company=b.get("company"),
                         run_date=run_date, score=r.get("panel_pct", r.get("impact_sum")),
                         why=why, side=side, w=w, session=b.get("session"))


def pick_panel(run, f, model):
    pp = panel_pcts(run, "US")
    for r in (load(f) or {}).get("ranking", []):
        p = pp.get(r["ticker"])
        if p and p["full"] and abs(p["panel_pct"]) >= PANEL_TOP:
            yield dict(r, panel_pct=abs(p["panel_pct"])), sign(p["panel_pct"]), \
                f"panel {abs(p['panel_pct']):.0f}"


def pick_top(run, f, model):
    for r in (load(f) or {}).get("ranking", []):
        if not r.get("rankable", True) or not r.get("impact_sum"):
            continue
        p = pctile(run, model, r["impact_sum"])
        if p is not None and p >= TOP:
            yield r, sign(r["impact_sum"]), f"top {100 - p:.0f}%"


us_side_stage("research/*/*/*/edge-panel/edge-scores-panel.json", "US · E-P panel",
              "US-P", pick_panel)
# Stage D is left out on the operator's instruction (Xavier, 2026-10-14).

# Stage R (the reversal researcher) is deliberately absent (operator, 2026-10-12): it
# predicts a different event with a different model of the market, so its calls are
# not comparable with the earnings stages and must not sit in the same table.

# The four order-less markets, through markets.json and their own resolvers.
SUFFIX = {"JP": ".T", "AU": ".AX", "CA": ".TO"}
for mk, v in markets.items():
    for n in v.get("names", []):
        if n.get("sept_opus55") or not n.get("rankable") or n.get("event_occurred") is False:
            continue
        picks = []
        if n.get("impact_sum") and (n.get("impact_pctile_all") or 0) >= TOP:
            picks.append((f"{v.get('label', mk)} · hunter", sign(n["impact_sum"]),
                          f"top {100 - n['impact_pctile_all']:.0f}%", n["impact_sum"]))
        if n.get("panel_selected"):
            pp = panel_pcts(n["run"], mk).get(n["ticker"]) or {}
            picks.append((f"{v.get('label', mk)} · panel", sign(n.get("panel_score")),
                          f"panel {n.get('panel_consensus_k')}/4",
                          abs(pp["panel_pct"]) if "panel_pct" in pp else n.get("panel_score")))
        for stage, side, why, score in picks:
            if n.get("realised_move_pct") is not None and not n.get("move_pending"):
                resolved.append(dict(stage=stage, version=n.get("prompt_version"),
                                     model=n.get("model_short"), ticker=n["ticker"],
                                     run_date=n["run_date"],
                                     ret=side * n["realised_move_pct"], kind=why))
            elif recent(n.get("run_date") or ""):
                b = load(ROOT / n["run"] / "baselines" / f"{n['ticker']}.json") or {}
                sym = b.get("yahoo_symbol") or n["ticker"] + SUFFIX.get(mk, "")
                if mk == "CA" and str(b.get("exchange", "")).upper().startswith("TSXV"):
                    sym = n["ticker"] + ".V"
                # Tokyo is scored close to the NEXT OPEN (jp_resolve.py); the others close to close.
                w = window(sym, n["event_date"], n.get("session") != "amc",
                           end_at_open=mk == "JP")
                live_row(stage=stage, ticker=n["ticker"], company=n.get("company"),
                         run_date=n["run_date"], score=score, why=why, side=side, w=w,
                         session=n.get("session"))

# ---------------------------------------------------------------- the last week, per ticker
# Every call, strong or not, with the same sources and exclusions as above. Two views
# read it (operator, 2026-10-13): the last WEEK_DAYS calendar days per ticker, and one
# expandable block per agent (stage x prompt x model) with all of its calls, whether
# or not they met the strong requirement. A call with no outcome yet is priced live
# while its run is recent, and is shown as not yet resolved after that.
WEEK_DAYS = 7
calls = []


def in_week(run_date):
    try:
        return TODAY - timedelta(days=WEEK_DAYS) <= date.fromisoformat(run_date) <= TODAY
    except Exception:
        return False


def week_row(stage, version, model, ticker, company, run_date, event_date, score,
             strong, why, move=None, live_w=None, side=None, session=None, px=None):
    side = sign(score) if side is None else side
    if move is not None:
        state = "opgelost"
    elif live_w and live_w.get("move") is not None:
        move, state = live_w["move"], live_w["state"]
        px = (live_w.get("ref"), live_w.get("last"))
    else:
        state = live_w["state"] if live_w else \
            "geen koers" if recent(run_date) else "niet opgelost"
    ret = None if move is None or not side else side * move
    calls.append(dict(stage=stage, version=version, model=model, ticker=ticker,
                     company=company, run_date=run_date, event_date=event_date,
                     score=None if score is None else round(score, 2), side=side,
                     strong=strong, why=why, state=state, session=session,
                     buy=None if not px or not px[0] else round(px[0], 4),
                     sell=None if not px or not px[1] else round(px[1], 4),
                     move=None if move is None else round(move, 2),
                     ret=None if ret is None else round(ret, 2),
                     right=None if ret is None else ret > 0))


for n in ledger["names"]:
    if n.get("sept_opus55") or n.get("duplicate_event") or n.get("rankable") is False:
        continue
    p = n.get("impact_pctile_all")
    mv = us_move(n)
    week_row("US · E", n["prompt_version"], n["model_short"], n["ticker"], n.get("company"),
             n["run_date"], n.get("event_date"), n.get("impact_sum"),
             bool(n.get("impact_sum")) and (p or 0) >= TOP,
             None if p is None else f"p{p:.0f}",
             move=mv, session=n.get("session"), px=us_px(n) if mv is not None else None,
             live_w=None if mv is not None or not recent(n["run_date"]) else us_live(
                 n["ticker"], n["event_date"], n["session"]))

for glob_pat, stage, market, key in (
        ("research/*/*/*/edge-panel/edge-scores-panel.json", "US · E-P panel", "US-P",
         "panel_score"),):
    for f in sorted(glob.glob(str(ROOT / glob_pat))):
        run = str(Path(f).parent.relative_to(ROOT))
        run_date = Path(f).parent.parent.name
        ver, model, mshort, sept = prov(run, market)
        if sept:
            continue
        for r in (load(f) or {}).get("ranking", []):
            if not r.get("rankable", True) or r.get(key) is None:
                continue
            score = r[key]
            if key == "panel_score":
                p = panel_pcts(run, "US").get(r["ticker"]) or {}
                signed = p.get("panel_pct", 0.0)
                score, pside = abs(signed), sign(signed)
                strong = bool(p.get("full")) and score >= PANEL_TOP
                why = f"panel {score:.0f}"
            else:
                pc = pctile(run, model, score)
                strong, why = (pc or 0) >= TOP, None if pc is None else f"p{pc:.0f}"
            n = by_run_ticker.get((run_date, r["ticker"]))
            b = load(ROOT / run / "baselines" / f"{r['ticker']}.json") or {}
            mv = us_move_any(n, r["ticker"], run_date, b.get("event_date"),
                             b.get("session") or (n or {}).get("session"))
            week_row(stage, ver, "panel" if key == "panel_score" else mshort, r["ticker"], b.get("company"), run_date,
                     b.get("event_date"), score, strong, why,
                     side=pside if key == "panel_score" else None,
                     move=mv, session=b.get("session") or (n or {}).get("session"),
                     px=US_PX.get(f"{run_date}|{r['ticker']}") if mv is not None else None,
                     live_w=None if mv is not None or not recent(run_date) else us_live(
                         r["ticker"], b.get("event_date") or run_date, b.get("session")))

for mk, v in markets.items():
    for n in v.get("names", []):
        if n.get("sept_opus55") or not n.get("rankable") or n.get("event_occurred") is False:
            continue
        done = n.get("realised_move_pct") is not None and not n.get("move_pending")
        w, mpx = None, None
        b = load(ROOT / n["run"] / "baselines" / f"{n['ticker']}.json") or {}
        sym = b.get("yahoo_symbol") or n["ticker"] + SUFFIX.get(mk, "")
        if mk == "CA" and str(b.get("exchange", "")).upper().startswith("TSXV"):
            sym = n["ticker"] + ".V"
        if not done and recent(n.get("run_date") or ""):
            w = window(sym, n["event_date"], n.get("session") != "amc",
                       end_at_open=mk == "JP")
        elif done and v.get("resolved_file"):
            mpx = market_px(n, v["resolved_file"], sym, n.get("session") != "amc", mk == "JP")
        move = n["realised_move_pct"] if done else None
        label = v.get("label", mk)
        p = n.get("impact_pctile_all")
        if n.get("impact_sum") is not None:
            week_row(f"{label} · hunter", n.get("prompt_version"), n.get("model_short"),
                     n["ticker"], n.get("company"), n["run_date"], n.get("event_date"),
                     n["impact_sum"], bool(n["impact_sum"]) and (p or 0) >= TOP,
                     None if p is None else f"p{p:.0f}", move=move, live_w=w,
                     session=n.get("session"), px=mpx)
        if n.get("panel_score") is not None:
            pp = panel_pcts(n["run"], mk).get(n["ticker"]) or {}
            signed = pp.get("panel_pct", n["panel_score"])
            pside = sign(n["panel_score"]) if n.get("panel_selected") else sign(signed)   # a selected call keeps the consensus side
            week_row(f"{label} · panel", n.get("prompt_version"), "panel",
                     n["ticker"], n.get("company"), n["run_date"], n.get("event_date"),
                     abs(signed) if "panel_pct" in pp else n["panel_score"], bool(n.get("panel_selected")),
                     f"panel {n.get('panel_consensus_k')}/4", move=move, live_w=w, side=pside,
                     session=n.get("session"), px=mpx)

calls.sort(key=lambda x: (x["run_date"], x["stage"], -abs(x["score"] or 0)))
calls.sort(key=lambda x: x["run_date"], reverse=True)
week = [c for c in calls if in_week(c["run_date"])]

# One block per agent: every call it made, and the same statistics as the scorecard
# for all its resolved calls beside the strong ones only. Never pooled over versions.
by_agent = {}
for c in calls:
    if c["version"] and c["version"] != "onbekend":
        by_agent.setdefault((c["stage"], c["version"], c["model"] or "?"), []).append(c)
# The second meaning of "strong" (Xavier, 2026-10-14, corrected the same day): a call
# whose |score| clears that STAGE's fixed top-20% benchmark, measured over all its calls
# and pooled over prompt versions, never per day and never per version. For the US E-P
# panel that is the benchmark it was built on, |panel_pct| >= PANEL_TOP with all four
# judges; for stage E it is the model-wide reference (impact_pctile_all >= TOP). Every
# other stage (the market panels score lower, so their bar is lower) gets the 80th
# percentile of its nonzero |scores| over all its calls, per hunter model; it uses later
# scores but never an outcome, and a stage with fewer than OWN_MIN calls has no bar.
OWN_MIN = 5
FIXED_BENCH = {"US · E-P panel": PANEL_TOP}
# The market panels are already scaled to each judge's own range, so their bar is a
# fixed percentile too; 70 for now (Xavier, 2026-10-14), not a cut fitted on the day.
MARKET_PANEL_TOP = 70.0
for _m in ("Europa", "Japan", "Australië", "Canada"):
    FIXED_BENCH[f"{_m} · panel"] = MARKET_PANEL_TOP
REF_BENCH = {"US · E"}


def p80(xs):
    xs = sorted(xs)
    k = 0.8 * (len(xs) - 1)
    lo = int(k)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (k - lo)


def bench_key(c):
    return (c["stage"], c["model"] or "?")


by_bench = {}
for c in calls:
    c["own"] = False
    by_bench.setdefault(bench_key(c), []).append(c)
bench = {}                                   # (stage, model) -> cut, or "ref"
for key, rows in by_bench.items():
    stage = key[0]
    if stage in REF_BENCH:
        bench[key] = "ref"
        for r in rows:
            r["own"] = bool(r["strong"])
        continue
    if stage in FIXED_BENCH:
        cut = FIXED_BENCH[stage]
        for r in rows:
            if stage == "US · E-P panel":
                r["own"] = bool(r["strong"])     # strong already is full and |panel_pct| >= 80
            else:
                r["own"] = bool(r["score"] and r["side"]) and abs(r["score"]) >= cut - 1e-9
    else:
        sc = [abs(r["score"]) for r in rows if r["score"] and r["side"]]
        if len(sc) < OWN_MIN:
            continue
        cut = p80(sc)
        for r in rows:
            r["own"] = bool(r["score"] and r["side"]) and abs(r["score"]) >= cut - 1e-9
    bench[key] = round(cut, 2)
own_cut = {}
for key in by_agent:
    b = bench.get((key[0], key[2]))
    if b is not None:
        own_cut[key] = b

agents = []
for (stage, ver, model), rows in by_agent.items():
    done = [r for r in rows if r["state"] == "opgelost" and r["ret"] is not None]
    agents.append(dict(stage=stage, version=ver, model=model, n_calls=len(rows),
                       last=rows[0]["run_date"], first=rows[-1]["run_date"],
                       all=summarise([r["ret"] for r in done]),
                       strong=summarise([r["ret"] for r in done if r["strong"]]),
                       own=summarise([r["ret"] for r in done if r["own"]]),
                       own_cut=own_cut.get((stage, ver, model)),
                       calls=rows))
agents.sort(key=lambda a: (a["stage"], a["last"]))

# ---------------------------------------------------------------- the panel per own top
# Every panel name with an outcome, its panel_pct and the spread of its four judges.
# Top X% = |panel_pct| >= 100 - X, traded on the sign of panel_pct. The US uses this
# page's window (13:30 ET in, amc out at the next open, bmo out at 13:00 ET); the
# markets their own resolver. Point in time, never pooled with the hunters.
TOPS = list(range(10, 101, 10))
pt_rows = {}
for f in sorted(glob.glob(str(ROOT / "research/*/*/*/edge-panel/edge-scores-panel.json"))):
    run = str(Path(f).parent.relative_to(ROOT))
    run_date = Path(f).parent.parent.name
    if prov(run, "US-P")[3]:
        continue
    for t, p in panel_pcts(run, "US").items():
        n = by_run_ticker.get((run_date, t))
        b = load(ROOT / run / "baselines" / f"{t}.json") or {}
        mv = us_move_any(n, t, run_date, b.get("event_date"),
                         b.get("session") or (n or {}).get("session"))
        if mv is not None and p["full"]:
            pt_rows.setdefault("US", []).append(dict(run_date=run_date, ticker=t, pct=p["panel_pct"],
                                                    sd=p["sd"], move=mv))
for mk, v in markets.items():
    for n in v.get("names", []):
        if n.get("sept_opus55") or not n.get("rankable") or n.get("event_occurred") is False \
                or n.get("panel_score") is None or n.get("realised_move_pct") is None or n.get("move_pending"):
            continue
        p = panel_pcts(n["run"], mk).get(n["ticker"])
        if p and p["full"]:
            pt_rows.setdefault(mk, []).append(dict(run_date=n["run_date"], ticker=n["ticker"],
                                                   pct=p["panel_pct"], sd=p["sd"], move=n["realised_move_pct"]))
PT_LABEL = {"US": "VS · E-P panel", **{mk: v.get("label", mk) + " · panel" for mk, v in markets.items()}}
panel_top = []
for mk, rows in pt_rows.items():
    rows = [r for r in rows if r["pct"]]
    if not rows:
        continue
    curve = []
    for t in TOPS:
        pick = [r for r in rows if abs(r["pct"]) >= 100 - t]
        s_ = summarise([sign(r["pct"]) * r["move"] for r in pick])
        s_.update(top=t, days=len({r["run_date"] for r in pick}))
        curve.append(s_)
    split = []
    for t in (20, 30, 50):
        pick = [r for r in rows if abs(r["pct"]) >= 100 - t and r["sd"] is not None]
        if len(pick) < 4:
            continue
        med = sorted(r["sd"] for r in pick)[len(pick) // 2]
        lo = [sign(r["pct"]) * r["move"] for r in pick if r["sd"] <= med]
        hi = [sign(r["pct"]) * r["move"] for r in pick if r["sd"] > med]
        split.append(dict(top=t, median_sd=med, low=summarise(lo), high=summarise(hi)))
    panel_top.append(dict(region=mk, label=PT_LABEL.get(mk, mk), n=len(rows),
                          days=len({r["run_date"] for r in rows}),
                          first=min(r["run_date"] for r in rows), last=max(r["run_date"] for r in rows),
                          short_all=summarise([-r["move"] for r in rows]), curve=curve, split=split))
panel_top.sort(key=lambda x: (x["region"] != "US", -x["n"]))

# ---------------------------------------------------------------- assemble

groups = {}
for r in resolved:
    if not r["version"] or r["version"] == "onbekend":
        continue
    groups.setdefault((r["stage"], r["version"], r["model"] or "?"), []).append(r)
table = []
for (stage, ver, model), rows in groups.items():
    s = summarise([r["ret"] for r in rows])
    s.update(stage=stage, version=ver, model=model,
             last=max(r["run_date"] for r in rows))
    table.append(s)
table.sort(key=lambda s: (s["stage"], s["last"]), reverse=False)

for x in live:
    w = x.pop("w")
    x["move"] = None if not w or w.get("move") is None else round(w["move"], 2)
    x["ret"] = None if x["move"] is None else round(x["side"] * x["move"], 2)
    x["state"] = (w or {}).get("state", "geen koers")
    x["buy"] = (w or {}).get("ref")
    x["sell"] = (w or {}).get("last")
    x["ref_day"] = (w or {}).get("ref_day")
    x["end_day"] = (w or {}).get("end_day")
    x["score"] = None if x["score"] is None else round(x["score"], 2)

# The same three blocks under the agent's own top 20%.
groups_own = {}
for c in calls:
    if c["own"] and c["state"] == "opgelost" and c["ret"] is not None:
        groups_own.setdefault((c["stage"], c["version"], c["model"] or "?"), []).append(c)
table_own = []
for (stage, ver, model), rows in groups_own.items():
    s = summarise([r["ret"] for r in rows])
    s.update(stage=stage, version=ver, model=model, last=max(r["run_date"] for r in rows))
    table_own.append(s)
table_own.sort(key=lambda s: (s["stage"], s["last"]))
live_own = [dict(c, why=(c["why"] or "") + " · top 20% benchmark") for c in calls
            if c["own"] and c["state"] not in ("opgelost", "niet opgelost")]
live_own.sort(key=lambda x: (x["state"] != "loopt", x["stage"], x["ticker"]))
n_resolved_own = sum(len(v) for v in groups_own.values())

# ---------------------------------------------------------------- the panel tab
CAL = PC.load_calibration()
calibration = None
if CAL:
    cvb = CAL.get("cross_validation") or {}
    calibration = {"fitted_utc": CAL.get("generated_utc"), "sample": CAL.get("sample"),
                   "window": CAL.get("window"), "grid": CAL.get("grid"), "fit": CAL.get("fit"),
                   "band": CAL.get("band"), "models": cvb.get("models"), "by_band": cvb.get("by_band")}
week_ep = {(c["ticker"], c["run_date"]): c for c in calls if c["stage"] == "US · E-P panel"}
panel_names = []
for f in sorted(glob.glob(str(ROOT / "research/*/*/*/edge-panel/edge-scores-panel.json"))):
    run = str(Path(f).parent.relative_to(ROOT))
    run_date = Path(f).parent.parent.name
    if not in_week(run_date):
        continue
    pp = panel_pcts(run, "US")
    for r in (load(f) or {}).get("ranking", []):
        p = pp.get(r["ticker"]) or {}
        pct_ = p.get("panel_pct")
        if pct_ is None:
            continue
        er = {k: r.get(k) for k in ("expected_return_pct", "expected_return_lo80", "expected_return_hi80", "p_right")}
        if er["expected_return_pct"] is None and CAL:
            er = PC.expected(CAL, pct_) or er
        er.pop("expected_move_pct", None)
        c = week_ep.get((r["ticker"], run_date)) or {}
        panel_names.append(dict(run_date=run_date, ticker=r["ticker"], company=c.get("company"),
                                panel_pct=abs(pct_), spread=p.get("sd"),
                                selected=bool(p.get("full")) and abs(pct_) >= PANEL_TOP,
                                side=sign(pct_), state=c.get("state"), ret=c.get("ret"), **er))
panel_names.sort(key=lambda x: (x["run_date"], x["panel_pct"]), reverse=True)

payload = {
    "built_utc": datetime.now(timezone.utc).isoformat(timespec="minutes"),
    "ledger_utc": ledger.get("generated_utc"),
    "live": sorted(live, key=lambda x: (x["state"] != "loopt", x["stage"], x["ticker"])),
    "table": table,
    "n_resolved": len(resolved),
    "own": {"live": live_own, "table": table_own, "n_resolved": n_resolved_own, "min_calls": OWN_MIN,
            "bench": [dict(stage=k[0], model=k[1], cut=v) for k, v in sorted(bench.items())]},
    "week": calls,          # every call; the page cuts the period (7 days by default)
    "agents": agents,
    "week_days": WEEK_DAYS,
    "panel_top": panel_top,
    "calibration": calibration,
    "panel_names": panel_names,
}
OUT_JSON.write_text(json.dumps(payload, indent=1, default=str))
FROZEN_PATH.write_text(json.dumps(FROZEN, indent=1, sort_keys=True) + "\n")

tpl = (ROOT / "dashboard" / "scripts" / "scorebord_template.html").read_text()
data = json.dumps(payload, default=str).replace("</", "<\\/")
OUT_HTML.write_text(tpl.replace("__DATA__", data))
print(f"scorebord: {len(live)} open strong calls, {len(resolved)} resolved strong calls, "
      f"{len(table)} version rows, {len(week)} calls in the last {WEEK_DAYS} days, "
      f"{len(agents)} agents over {len(calls)} calls -> {OUT_HTML.relative_to(ROOT)}")

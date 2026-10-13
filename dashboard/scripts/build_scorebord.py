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
  * panel stages (US E-P and the market panels): the panel selected the name, 3 of 4
    judges with it in their own top 20%. The side is the panel's.

Resolved outcomes are read, never recomputed, wherever a resolver already wrote one:
the US ledger's strategy exit (`mv_strategy`) for E, E-P and D, the market resolvers
through `markets.json` for EU/JP/AU/CA. Stage R is left out on purpose: it is a
different event (yesterday's losers, not an earnings print) and does not belong here.
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

PCT = SR.Percentiles()
TOP = 80.0                          # top 20% of the model's own reference
DATA = ROOT / "dashboard" / "data"
OUT_HTML = ROOT / "dashboard" / "scorebord.html"
OUT_JSON = DATA / "scorebord.json"
TODAY = datetime.now(timezone.utc).date()
LOOKBACK_DAYS = 6                   # runs this recent can still have an open window
ET = ZoneInfo("America/New_York")
# The US strategy exit, as the ledger resolves it (STRATEGY_EXIT in build_ledger.py):
# amc at the next opening print, bmo at 14:00 ET on the report day (`hr_22`). A
# running bmo call is priced to that same minute, never to the close.
BMO_EXIT_HM = 14 * 60


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
           "?range=1mo&interval=1d")
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
    if n.get("mv_strategy") is not None and not n.get("pending"):
        resolved.append(dict(stage="US · E", version=n["prompt_version"],
                             model=n["model_short"], ticker=n["ticker"],
                             run_date=n["run_date"], ret=side * n["mv_strategy"],
                             kind="top 20%"))
    elif recent(n["run_date"]):
        w = window(n["ticker"], n["event_date"], n["session"] == "bmo",
                   end_at_open=n["session"] == "amc",
                   end_hm=BMO_EXIT_HM if n["session"] == "bmo" else None)
        live_row(stage="US · E", ticker=n["ticker"], company=n.get("company"),
                 run_date=n["run_date"], score=n["impact_sum"],
                 why=f"top {100 - n['impact_pctile_all']:.0f}% {n['model_short']}",
                 side=side, w=w)


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
            if n and n.get("mv_strategy") is not None and not n.get("pending"):
                resolved.append(dict(stage=stage, version=ver,
                                     model="panel" if key_is_panel else mshort,
                                     ticker=r["ticker"], run_date=run_date,
                                     ret=side * n["mv_strategy"], kind=why))
            elif recent(run_date):
                b = load(ROOT / run / "baselines" / f"{r['ticker']}.json") or {}
                w = window(r["ticker"], b.get("event_date") or run_date,
                           b.get("session") == "bmo", end_at_open=b.get("session") == "amc",
                           end_hm=BMO_EXIT_HM if b.get("session") == "bmo" else None)
                live_row(stage=stage, ticker=r["ticker"], company=b.get("company"),
                         run_date=run_date, score=r.get("panel_score", r.get("impact_sum")),
                         why=why, side=side, w=w)


def pick_panel(run, f, model):
    for r in (load(f) or {}).get("ranking", []):
        if r.get("selected"):
            yield r, sign(r.get("side") or r.get("panel_score")), \
                f"panel {r.get('consensus_k')}/4"


def pick_top(run, f, model):
    for r in (load(f) or {}).get("ranking", []):
        if not r.get("rankable", True) or not r.get("impact_sum"):
            continue
        p = pctile(run, model, r["impact_sum"])
        if p is not None and p >= TOP:
            yield r, sign(r["impact_sum"]), f"top {100 - p:.0f}%"


us_side_stage("research/*/*/*/edge-panel/edge-scores-panel.json", "US · E-P panel",
              "US-P", pick_panel)
us_side_stage("research/*/*/*/edge-deep/edge-scores.json", "US · D", "US-D", pick_top)

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
            picks.append((f"{v.get('label', mk)} · panel", sign(n.get("panel_score")),
                          f"panel {n.get('panel_consensus_k')}/4", n.get("panel_score")))
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
                         run_date=n["run_date"], score=score, why=why, side=side, w=w)

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
             strong, why, move=None, live_w=None):
    side = sign(score)
    if move is not None:
        state = "opgelost"
    elif live_w and live_w.get("move") is not None:
        move, state = live_w["move"], live_w["state"]
    else:
        state = live_w["state"] if live_w else \
            "geen koers" if recent(run_date) else "niet opgelost"
    ret = None if move is None or not side else side * move
    calls.append(dict(stage=stage, version=version, model=model, ticker=ticker,
                     company=company, run_date=run_date, event_date=event_date,
                     score=None if score is None else round(score, 2), side=side,
                     strong=strong, why=why, state=state,
                     move=None if move is None else round(move, 2),
                     ret=None if ret is None else round(ret, 2),
                     right=None if ret is None else ret > 0))


for n in ledger["names"]:
    if n.get("sept_opus55") or n.get("duplicate_event") or n.get("rankable") is False:
        continue
    p = n.get("impact_pctile_all")
    done = n.get("mv_strategy") is not None and not n.get("pending")
    week_row("US · E", n["prompt_version"], n["model_short"], n["ticker"], n.get("company"),
             n["run_date"], n.get("event_date"), n.get("impact_sum"),
             bool(n.get("impact_sum")) and (p or 0) >= TOP,
             None if p is None else f"p{p:.0f}",
             move=n["mv_strategy"] if done else None,
             live_w=None if done or not recent(n["run_date"]) else window(
                 n["ticker"], n["event_date"],
                                             n["session"] == "bmo",
                                             end_at_open=n["session"] == "amc",
                   end_hm=BMO_EXIT_HM if n["session"] == "bmo" else None))

for glob_pat, stage, market, key in (
        ("research/*/*/*/edge-panel/edge-scores-panel.json", "US · E-P panel", "US-P",
         "panel_score"),
        ("research/*/*/*/edge-deep/edge-scores.json", "US · D", "US-D", "impact_sum")):
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
                strong, why = bool(r.get("selected")), f"panel {r.get('consensus_k')}/4"
                if r.get("side"):
                    score = abs(score) * sign(r["side"])
            else:
                pc = pctile(run, model, score)
                strong, why = (pc or 0) >= TOP, None if pc is None else f"p{pc:.0f}"
            n = by_run_ticker.get((run_date, r["ticker"]))
            b = load(ROOT / run / "baselines" / f"{r['ticker']}.json") or {}
            done = n and n.get("mv_strategy") is not None and not n.get("pending")
            week_row(stage, ver, "panel" if key == "panel_score" else mshort, r["ticker"], b.get("company"), run_date,
                     b.get("event_date"), score, strong, why,
                     move=n["mv_strategy"] if done else None,
                     live_w=None if done or not recent(run_date) else window(
                         r["ticker"], b.get("event_date") or run_date,
                         b.get("session") == "bmo", end_at_open=b.get("session") == "amc",
                           end_hm=BMO_EXIT_HM if b.get("session") == "bmo" else None))

for mk, v in markets.items():
    for n in v.get("names", []):
        if n.get("sept_opus55") or not n.get("rankable") or n.get("event_occurred") is False:
            continue
        done = n.get("realised_move_pct") is not None and not n.get("move_pending")
        w = None
        if not done and recent(n.get("run_date") or ""):
            b = load(ROOT / n["run"] / "baselines" / f"{n['ticker']}.json") or {}
            sym = b.get("yahoo_symbol") or n["ticker"] + SUFFIX.get(mk, "")
            if mk == "CA" and str(b.get("exchange", "")).upper().startswith("TSXV"):
                sym = n["ticker"] + ".V"
            w = window(sym, n["event_date"], n.get("session") != "amc",
                       end_at_open=mk == "JP")
        move = n["realised_move_pct"] if done else None
        label = v.get("label", mk)
        p = n.get("impact_pctile_all")
        if n.get("impact_sum") is not None:
            week_row(f"{label} · hunter", n.get("prompt_version"), n.get("model_short"),
                     n["ticker"], n.get("company"), n["run_date"], n.get("event_date"),
                     n["impact_sum"], bool(n["impact_sum"]) and (p or 0) >= TOP,
                     None if p is None else f"p{p:.0f}", move=move, live_w=w)
        if n.get("panel_score") is not None:
            week_row(f"{label} · panel", n.get("prompt_version"), "panel",
                     n["ticker"], n.get("company"), n["run_date"], n.get("event_date"),
                     n["panel_score"], bool(n.get("panel_selected")),
                     f"panel {n.get('panel_consensus_k')}/4", move=move, live_w=w)

calls.sort(key=lambda x: (x["run_date"], x["stage"], -abs(x["score"] or 0)))
calls.sort(key=lambda x: x["run_date"], reverse=True)
week = [c for c in calls if in_week(c["run_date"])]

# One block per agent: every call it made, and the same statistics as the scorecard
# for all its resolved calls beside the strong ones only. Never pooled over versions.
by_agent = {}
for c in calls:
    if c["version"] and c["version"] != "onbekend":
        by_agent.setdefault((c["stage"], c["version"], c["model"] or "?"), []).append(c)
agents = []
for (stage, ver, model), rows in by_agent.items():
    done = [r for r in rows if r["state"] == "opgelost" and r["ret"] is not None]
    agents.append(dict(stage=stage, version=ver, model=model, n_calls=len(rows),
                       last=rows[0]["run_date"], first=rows[-1]["run_date"],
                       all=summarise([r["ret"] for r in done]),
                       strong=summarise([r["ret"] for r in done if r["strong"]]),
                       calls=rows))
agents.sort(key=lambda a: (a["stage"], a["last"]))

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
    x["ref_day"] = (w or {}).get("ref_day")
    x["end_day"] = (w or {}).get("end_day")
    x["score"] = None if x["score"] is None else round(x["score"], 2)

payload = {
    "built_utc": datetime.now(timezone.utc).isoformat(timespec="minutes"),
    "ledger_utc": ledger.get("generated_utc"),
    "live": sorted(live, key=lambda x: (x["state"] != "loopt", x["stage"], x["ticker"])),
    "table": table,
    "n_resolved": len(resolved),
    "week": week,
    "agents": agents,
    "week_days": WEEK_DAYS,
}
OUT_JSON.write_text(json.dumps(payload, indent=1, default=str))

tpl = (ROOT / "dashboard" / "scripts" / "scorebord_template.html").read_text()
data = json.dumps(payload, default=str).replace("</", "<\\/")
OUT_HTML.write_text(tpl.replace("__DATA__", data))
print(f"scorebord: {len(live)} open strong calls, {len(resolved)} resolved strong calls, "
      f"{len(table)} version rows, {len(week)} calls in the last {WEEK_DAYS} days, "
      f"{len(agents)} agents over {len(calls)} calls -> {OUT_HTML.relative_to(ROOT)}")

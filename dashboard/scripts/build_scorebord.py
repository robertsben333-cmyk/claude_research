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


def window(sym, start, start_is_close_before, end_at_open=False):
    """Price a window that starts at a close and ends at the next session's close
    (or open). `start` is the event date; when `start_is_close_before` the reference is
    the last close strictly before it (a bmo print), else the close on it.
    Returns dict(ref, last, move, state) or None."""
    q = chart(sym)
    if not q or not q["bars"]:
        return None
    days = sorted(q["bars"])
    before = [d for d in days if (d < start if start_is_close_before else d <= start)]
    if not before:
        return None
    ref_day = before[-1]
    ref = q["bars"][ref_day][1]
    after = [d for d in days if d > ref_day]
    if not after:
        return {"ref": ref, "ref_day": ref_day, "last": None, "move": None,
                "state": "wacht"}
    end_day = after[0]
    o, c = q["bars"][end_day]
    if end_at_open:
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
                   end_at_open=n["session"] == "amc")
        live_row(stage="US · E", ticker=n["ticker"], company=n.get("company"),
                 run_date=n["run_date"], score=n["impact_sum"],
                 why=f"top {100 - n['impact_pctile_all']:.0f}% {n['model_short']}",
                 side=side, w=w)


def us_side_stage(glob_pat, stage, market, picker):
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
                resolved.append(dict(stage=stage, version=ver, model=mshort,
                                     ticker=r["ticker"], run_date=run_date,
                                     ret=side * n["mv_strategy"], kind=why))
            elif recent(run_date):
                b = load(ROOT / run / "baselines" / f"{r['ticker']}.json") or {}
                w = window(r["ticker"], b.get("event_date") or run_date,
                           b.get("session") == "bmo", end_at_open=b.get("session") == "amc")
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
                w = window(sym, n["event_date"], n.get("session") != "amc")
                live_row(stage=stage, ticker=n["ticker"], company=n.get("company"),
                         run_date=n["run_date"], score=score, why=why, side=side, w=w)

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
}
OUT_JSON.write_text(json.dumps(payload, indent=1, default=str))

tpl = (ROOT / "dashboard" / "scripts" / "scorebord_template.html").read_text()
data = json.dumps(payload, default=str).replace("</", "<\\/")
OUT_HTML.write_text(tpl.replace("__DATA__", data))
print(f"scorebord: {len(live)} open strong calls, {len(resolved)} resolved strong calls, "
      f"{len(table)} version rows -> {OUT_HTML.relative_to(ROOT)}")

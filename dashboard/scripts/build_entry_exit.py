#!/usr/bin/env python3
"""Entry/exit hypotheses for stage E-P into dashboard/data/entry-exit.json, for the
"Entry-exit" tab (operator, 2026-11-15).

Two leads came out of the pre-registered indicator study
(research/analyses/earnings-day-indicators/report.md). Neither passed its verdict rule;
both are tracked here so they can be settled forward, per prompt version, never pooled:

  H1 VWAP     price at the 13:30 ET entry against the run day's VWAP (09:30-13:30),
              signed to the panel's side. Lead: a stock that is already extended our
              way at entry does WORSE (v3 high-minus-low tercile -4.1, t -2.0).
  H2 vorige   last quarter's earnings reaction (sealed baseline history), signed to the
              panel's side. Lead: a name that reacted our way last time does better
              (v3 +3.4, t 1.7).

The outcome is the scorebord's own window and price (scorebord-frozen.json: 13:30 ET
in, amc out at the next open, bmo out at 13:00 ET), so this tab counts the same
returns as the scorebord. Run days up to 2026-11-12 are the sample the leads were
found on; 2026-11-13 onward is the forward test and is reported apart.

The VWAP comes from Alpaca SIP 5-minute bars (ALPACA_API_KEY_ID / _SECRET_KEY from the
environment, never printed). The previous output is the cache: a name whose VWAP is
known is never fetched again. Without keys the build keeps what it had. Read-only:
nothing here touches an order.

    python3 dashboard/scripts/build_entry_exit.py
"""
import datetime as dt
import glob
import json
import math
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import provenance as PROV  # noqa: E402

DATA = ROOT / "dashboard" / "data"
OUT = DATA / "entry-exit.json"
FROZEN = DATA / "scorebord-frozen.json"
NY = ZoneInfo("America/New_York")
FORWARD_FROM = "2026-11-13"
STRONG = 60.0

HYP = [
    {"key": "vwap", "label": "Koers t.o.v. VWAP bij instap",
     "claim": "Een aandeel dat om 13:30 al ver onze kant op boven/onder de dag-VWAP staat, doet het slechter.",
     "expect": -1, "found": "v3: hoog-min-laag tercile −4,06 (t −2,0, n 218); v2: −2,56 (t −1,8, n 186)",
     "unit": "% van VWAP, onze kant op"},
    {"key": "prev", "label": "Reactie op de vorige print",
     "claim": "Een naam die vorig kwartaal onze kant op reageerde, doet het nu beter.",
     "expect": 1, "found": "v3: hoog-min-laag tercile +3,44 (t 1,7, n 205); v2: +1,40 (t 1,0, n 184)",
     "unit": "% vorige reactie, onze kant op"},
]


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def iso(day, hh, mm):
    return dt.datetime.combine(dt.date.fromisoformat(day), dt.time(hh, mm), NY) \
        .astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bars(syms, day):
    """5-minute SIP bars 09:30-13:30 ET on `day`, symbol -> list. None if no keys."""
    kid, sec = os.environ.get("ALPACA_API_KEY_ID"), os.environ.get("ALPACA_API_SECRET_KEY")
    if not kid or not sec:
        return None
    h = {"APCA-API-KEY-ID": kid, "APCA-API-SECRET-KEY": sec}
    out, tok = {}, None
    while True:
        q = dict(symbols=",".join(syms), timeframe="5Min", start=iso(day, 9, 30),
                 end=iso(day, 13, 30), feed="sip", adjustment="split", limit=10000)
        if tok:
            q["page_token"] = tok
        url = "https://data.alpaca.markets/v2/stocks/bars?" + urllib.parse.urlencode(q)
        for a in range(5):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=60) as r:
                    d = json.load(r)
                break
            except urllib.error.HTTPError as e:
                if e.code in (400, 403, 422):
                    return out
                time.sleep(2 ** a)
            except Exception:
                time.sleep(2 ** a)
        else:
            return out
        for s, b in (d.get("bars") or {}).items():
            out.setdefault(s, []).extend(b)
        tok = d.get("next_page_token")
        if not tok:
            return out


def et_min(t):
    x = datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(NY)
    return x.hour * 60 + x.minute


def vwap_dist(bl):
    """Last 5-min close before 13:30 against the 09:30-13:30 VWAP, in %."""
    bl = sorted((b for b in bl if et_min(b["t"]) < 13 * 60 + 30), key=lambda b: b["t"])
    if not bl or et_min(bl[-1]["t"]) < 12 * 60 + 30:
        return None
    v = sum(b["v"] for b in bl)
    if not v:
        return None
    vw = sum(b.get("vw", b["c"]) * b["v"] for b in bl) / v
    return round(100 * (bl[-1]["c"] / vw - 1), 3) if vw else None


def prev_reaction(b, run_date):
    for m in sorted((b.get("history") or {}).get("moves") or [],
                    key=lambda m: m.get("event_date", ""), reverse=True):
        if m.get("event_date", "") < run_date and m.get("move_pct") is not None:
            return m["move_pct"]
    return None


# ------------------------------------------------------------------ statistics
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def within_day_rho(pairs, nperm=2000, seed=11):
    """pairs: (day, x, y). Spearman on within-day centred ranks; p from shuffling y
    inside each day. Days with fewer than 3 names drop out."""
    by = {}
    for d, x, y in pairs:
        by.setdefault(d, []).append((x, y))
    groups = [g for g in by.values() if len(g) >= 3]
    if sum(len(g) for g in groups) < 10:
        return None
    rx, ry, idx = [], [], []
    for g in groups:
        a = rank([p[0] for p in g])
        b = rank([p[1] for p in g])
        s = len(g) - 1
        start = len(rx)
        rx += [v / s - 0.5 for v in a]
        ry += [v / s - 0.5 for v in b]
        idx.append(list(range(start, start + len(g))))
    den = math.sqrt(sum(v * v for v in rx) * sum(v * v for v in ry))
    if not den:
        return None
    rho = sum(a * b for a, b in zip(rx, ry)) / den
    rnd = random.Random(seed)
    ge = 0
    for _ in range(nperm):
        yy = ry[:]
        for ii in idx:
            vals = [ry[i] for i in ii]
            rnd.shuffle(vals)
            for i, v in zip(ii, vals):
                yy[i] = v
        if abs(sum(a * b for a, b in zip(rx, yy)) / den) >= abs(rho) - 1e-12:
            ge += 1
    return {"rho": round(rho, 3), "p": round((ge + 1) / (nperm + 1), 4),
            "n": len(rx), "days": len(groups)}


def summ(v):
    v = [x for x in v if x is not None]
    if not v:
        return {"n": 0}
    m = sum(v) / len(v)
    out = {"n": len(v), "mean": round(m, 2), "hit": round(100 * sum(x > 0 for x in v) / len(v), 1)}
    if len(v) >= 3:
        sd = math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))
        if sd:
            out["t"] = round(m / (sd / math.sqrt(len(v))), 2)
    return out


def terciles(pairs):
    """Within-day terciles of x; mean y per tercile and high-minus-low with Welch t."""
    by = {}
    for d, x, y in pairs:
        by.setdefault(d, []).append((x, y))
    g = {0: [], 1: [], 2: []}
    for L in by.values():
        if len(L) < 3:
            continue
        L.sort(key=lambda p: p[0])
        for i, (_, y) in enumerate(L):
            g[min(2, int(3 * i / len(L)))].append(y)
    out = {k: summ(v) for k, v in zip(("low", "mid", "high"), g.values())}
    a, b = g[0], g[2]
    if len(a) >= 3 and len(b) >= 3:
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
        vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
        se = math.sqrt(va / len(a) + vb / len(b))
        out["diff"] = round(mb - ma, 2)
        out["t"] = round((mb - ma) / se, 2) if se else None
    return out


def block(rows, key):
    pairs = [(r["run_date"], r[key], r["ret"]) for r in rows
             if r.get(key) is not None and r.get("ret") is not None]
    strong = [r for r in rows if r["pct"] >= STRONG and r.get(key) is not None and r.get("ret") is not None]
    return {"rho": within_day_rho(pairs), "terciles": terciles(pairs),
            "strong_ours": summ([r["ret"] for r in strong if r[key] > 0]),
            "strong_against": summ([r["ret"] for r in strong if r[key] <= 0])}


# ------------------------------------------------------------------ build
def main():
    old = load(OUT) or {}
    cache = {f"{r['run_date']}|{r['ticker']}": r.get("vwap_raw") for r in old.get("names", [])}
    frozen = load(FROZEN) or {}
    rows = []
    for f in sorted(glob.glob(str(ROOT / "research/*/*/*/edge-panel/edge-scores-panel.json"))):
        run_dir = Path(f).parent
        run_date = run_dir.parent.name
        try:
            prov = PROV.for_row(run_dir, "US-P")
        except Exception:
            prov = {}
        ver = prov.get("prompt_version") or ""
        if not ver.startswith("us-panel.v") or ver < "us-panel.v2":
            continue
        doc = load(f) or {}
        for r in doc.get("ranking") or []:
            if r.get("panel_pct") is None or r.get("n_members") != 4:
                continue
            side = r.get("side") or (1 if (r.get("panel_pct_signed") or 0) > 0 else -1)
            b = load(run_dir / "baselines" / f"{r['ticker']}.json") or {}
            key = f"{run_date}|{r['ticker']}"
            fz = frozen.get(key) or {}
            rows.append(dict(run_date=run_date, ticker=r["ticker"], version=ver,
                             pct=abs(r["panel_pct"]), side=side, session=b.get("session"),
                             vwap_raw=cache.get(key), prev_raw=prev_reaction(b, run_date),
                             ret=None if fz.get("move") is None else round(side * fz["move"], 2)))
    # fetch the VWAP that is still missing, one call per run day; only after 13:30 ET
    # on that day, and give up on a day older than ten days.
    now = datetime.now(NY)
    need = {}
    for r in rows:
        if r["vwap_raw"] is not None:
            continue
        d = dt.date.fromisoformat(r["run_date"])
        if (now.date() - d).days > 10 and r["run_date"] < str(now.date()):
            continue
        if d == now.date() and now.hour * 60 + now.minute < 13 * 60 + 35:
            continue
        need.setdefault(r["run_date"], set()).add(r["ticker"].replace("-", "."))
    if need and not old.get("names") and not os.environ.get("ALPACA_API_KEY_ID"):
        print("entry-exit: no Alpaca keys, VWAP left empty")
    # first build: fill every day once
    if not old.get("names"):
        need = {}
        for r in rows:
            if r["vwap_raw"] is None:
                need.setdefault(r["run_date"], set()).add(r["ticker"].replace("-", "."))
    fetched = 0
    for day, syms in sorted(need.items()):
        syms = sorted(syms)
        got = {}
        for i in range(0, len(syms), 50):
            part = bars(syms[i:i + 50], day)
            if part is None:
                got = None
                break
            got.update(part)
        if got is None:
            break
        for r in rows:
            if r["run_date"] == day and r["vwap_raw"] is None:
                r["vwap_raw"] = vwap_dist(got.get(r["ticker"].replace("-", "."), []))
                fetched += r["vwap_raw"] is not None
    for r in rows:
        r["vwap"] = None if r["vwap_raw"] is None else round(r["side"] * r["vwap_raw"], 3)
        r["prev"] = None if r["prev_raw"] is None else round(r["side"] * r["prev_raw"], 2)
        r["forward"] = r["run_date"] >= FORWARD_FROM

    versions = sorted({r["version"] for r in rows}, reverse=True)
    stats = []
    for v in versions:
        R = [r for r in rows if r["version"] == v]
        for h in HYP:
            stats.append(dict(version=v, hyp=h["key"], part="alles", **block(R, h["key"])))
            fw = [r for r in R if r["forward"]]
            if fw:
                stats.append(dict(version=v, hyp=h["key"], part="vooruit", **block(fw, h["key"])))
    last = max((r["run_date"] for r in rows), default=None)
    payload = {"built_utc": datetime.now(timezone.utc).isoformat(timespec="minutes"),
               "forward_from": FORWARD_FROM, "strong": STRONG, "hyp": HYP,
               "versions": versions, "stats": stats, "last_run": last,
               "names": sorted(rows, key=lambda r: (r["run_date"], -r["pct"]), reverse=True)}
    OUT.write_text(json.dumps(payload, indent=1))
    print(f"entry-exit: {len(rows)} names, {sum(r['vwap'] is not None for r in rows)} with VWAP "
          f"({fetched} fetched now), {sum(r['ret'] is not None for r in rows)} resolved")


if __name__ == "__main__":
    main()

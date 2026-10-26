"""Collect every US panel arm's scores per (run_date, ticker) and price each name on the
E-P window (entry 13:30 ET, amc out at the next open, bmo out at 13:00 ET on the report
day). Arms: E-P (main), E-PF (Fable searcher), E-PI snapshots, E-PS shards (split branch,
passed with --split-root). Writes rows.json beside this file."""
import json, sys, time, glob, urllib.request, argparse
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ET = ZoneInfo("America/New_York")
ENTRY_HM, BMO_EXIT_HM = 13 * 60 + 30, 13 * 60
FROZEN = json.load(open(ROOT / "dashboard/data/scorebord-frozen.json"))
_c, _i = {}, {}


def get(url):
    for k in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            return json.load(urllib.request.urlopen(req, timeout=20))["chart"]["result"][0]
        except Exception:
            time.sleep(1 + k)
    return None


def daily(sym):
    if sym not in _c:
        r = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=3mo&interval=1d")
        bars = {}
        if r:
            off = r["meta"].get("gmtoffset", 0)
            q = r["indicators"]["quote"][0]
            for ts, o, c in zip(r.get("timestamp") or [], q["open"], q["close"]):
                bars[datetime.fromtimestamp(ts + off, timezone.utc).date().isoformat()] = (o, c)
        _c[sym] = bars
    return _c[sym]


def at(sym, day, hm):
    if sym not in _i:
        _i[sym] = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1mo&interval=5m")
    r = _i[sym]
    if not r:
        return None
    best = None
    for ts, c in zip(r.get("timestamp") or [], r["indicators"]["quote"][0]["close"]):
        d = datetime.fromtimestamp(ts, ET)
        m = d.hour * 60 + d.minute
        if c is not None and d.date().isoformat() == day and hm - 60 <= m <= hm:
            best = c
    return best


def move(run_date, t, event_date, session):
    k = f"{run_date}|{t}"
    if k in FROZEN:
        return FROZEN[k]["move"], "frozen"
    bars = daily(t)
    days = sorted(d for d, (o, c) in bars.items() if c is not None)
    if session == "amc":
        ed = event_date if event_date in days else None
    else:
        b = [d for d in days if d < event_date]
        ed = b[-1] if b else None
    if not ed:
        return None, "no entry day"
    e = at(t, ed, ENTRY_HM)
    after = [d for d in days if d > ed]
    if not e or not after:
        return None, "pending"
    x = bars[after[0]][0] if session == "amc" else at(t, after[0], BMO_EXIT_HM)
    if not x:
        return None, "no exit"
    return (x / e - 1) * 100, "priced"


sys.path.insert(0, str(ROOT / "researcher_us" / "scripts"))
import panel_score as PS  # noqa: E402
HIST = json.load(open(ROOT / "researcher_us/analysis/panel-history.json"))


def fill_pct(d, run):
    """Runs before 2026-10-14 carry no panel_pct: compute it the way the scorebord does
    (each member against its live range from runs before this one, mean of signed pcts)."""
    rows = d["ranking"]
    if all("panel_pct_signed" in r for r in rows):
        return
    present = d.get("members_present") or list(PS.MEMBERS)
    before = PS.date_of(run.name)
    ids = {r.get("id") for r in rows}
    refs = {m: PS.live_reference(HIST, m, 200, before=before, exclude=ids,
                                 fallback=PS.fallback_rows("seed", HIST))[0] for m in present}
    for r in rows:
        ps = {m: PS.pct_of(refs[m], (r["members"].get(m) or {}).get("impact_sum") or 0.0)
              for m in present if m in r["members"]}
        mu = sum(ps.values()) / len(ps)
        r["panel_pct_signed"] = round(mu, 1); r["panel_pct"] = abs(round(mu, 1))
        r["side"] = 1 if mu > 0 else (-1 if mu < 0 else 0)
        r["panel_pct_sd"] = round((sum((x - mu) ** 2 for x in ps.values()) / len(ps)) ** .5, 1)
        r["n_members"] = len(ps)
        r["sign_agree"] = max(sum(1 for x in ps.values() if x > 0), sum(1 for x in ps.values() if x < 0))
        r["selected_mean_pct"] = abs(mu) >= 80 and len(ps) == 4
        for m, x in ps.items():
            r["members"][m]["pct_signed"] = round(x, 1)
        r["pct_filled"] = True


def rows_of(path, arm, run_date, extra=None):
    d = json.load(open(path))
    out = []
    run = Path(path).parent
    fill_pct(d, run.parent if run.name.startswith("edge") else run)
    for r in d["ranking"]:
        b = json.load(open(run / "baselines" / f"{r['ticker']}.json"))
        h = run / "hunts" / f"{r['ticker']}.json"
        hj = json.load(open(h)) if h.exists() else {}
        out.append(dict(arm=arm, run_date=run_date, ticker=r["ticker"],
                        session=b.get("session"), event_date=b.get("event_date"),
                        panel_pct=r.get("panel_pct"), side=r.get("side"),
                        signed=r.get("panel_pct_signed"), sd=r.get("panel_pct_sd"),
                        n_members=r.get("n_members"), sign_agree=r.get("sign_agree"),
                        selected=bool(r.get("selected_mean_pct")),
                        members={m: v.get("pct_signed") for m, v in (r.get("members") or {}).items()},
                        impact_sum=hj.get("impact_sum"),
                        n_findings=len(hj.get("findings") or []),
                        day_n=len(d["ranking"]), pct_filled=r.get("pct_filled", False), **(extra or {})))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split-root", default=None)
    a = ap.parse_args()
    rows = []
    for p in sorted(glob.glob(str(ROOT / "research/2026/10/*/edge-panel/edge-scores-panel.json"))):
        rows += rows_of(p, "EP", p.split("/")[-3])
    for p in sorted(glob.glob(str(ROOT / "research/2026/10/*/edge-panel-fable/edge-scores-panel.json"))):
        rows += rows_of(p, "EPF", p.split("/")[-3])
    for p in sorted(glob.glob(str(ROOT / "research/2026/10/*/edge-intraday-*/edge-scores-panel.json"))):
        rows += rows_of(p, "EPI-" + p.split("/")[-2].split("-")[-1], p.split("/")[-3])
    if a.split_root:
        for p in sorted(glob.glob(a.split_root + "/research/2026/10/*/edge-split-*/edge-scores-panel.json")):
            k = p.split("/")[-2].split("-")[-1]
            rows += rows_of(p, "EPS", p.split("/")[-3], {"shard": int(k)})
    for r in rows:
        r["move"], r["price_basis"] = move(r["run_date"], r["ticker"], r["event_date"], r["session"])
        r["ret"] = None if r["move"] is None or not r["side"] else r["side"] * r["move"]
    json.dump(rows, open(HERE / "rows.json", "w"), indent=1)
    from collections import Counter
    print(Counter((r["arm"], r["price_basis"]) for r in rows))


main()

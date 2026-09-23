#!/usr/bin/env python3
"""Stage E V2, the shadow ledger: what the market did with news it could see.

V1 asks hunters for signed sizes in points of spot and nothing ever maps those
sizes onto what prices actually do. V2 (RobinBaumeister, PR #9) supplies the map
from the one kind of news whose reaction IS observable: a filing, with a
timestamp, scored by the same kind of model on the same scale, then measured.

    collect   8-Ks since `edge_v2.min_event_date` for a set of tickers, text only,
              no price anywhere in the scorer's input
    brief     the unscored inputs, as one brief for one `shadow-scorer` agent
    ingest    the agent's scores, refused unless the input hash matches
    measure   moves at nine horizons, beta-stripped and divided by sigma, for
              SCORED items only -- a move is never on disk before its score
    fit       kappa per (line, horizon) and pooled per horizon, with a standard
              error and the n it rests on
    status    counts

WHAT "WIRE NEWS" MEANS HERE. An 8-K on EDGAR, t0 = the SEC's acceptance time
(`acceptanceDateTime`, genuine UTC: AAPL's 2026-07-30 filing reads 20:30:28Z against
16:30:28 on the index page). A company usually wires the release a few minutes
BEFORE it files, so t0 is an upper bound on when the news was public and the 5m
horizon is the most contaminated one. Nasdaq's press-release API answers 301 from
here and the wires are paywalled, so the filing is the definition that can be
checked. Tighten it with a wire timestamp when a reachable source exists.

WHY THE NORMALISER IS REALISED SIGMA AND NOT THE EVENT IV. Symmetric unscaling only
works if the SAME quantity divides the shadow move and multiplies the live score.
An event-implied move exists for an earnings print and not for a financing 8-K, so
PR #9's `event_iv_pct` could not be computed for most shadow items and was a
different quantity at runtime. The 20-session realised daily sigma exists for both,
as of t0, from the same bars.

WHY THE SCORE MUST COME FIRST. The scorer has no web tools and reads one file with
no price in it. `measure` refuses unscored items, so no item's own move is on disk
while it is scored. Events before `min_event_date` are skipped because the model may
have seen them in training. What this does not stop: the scorer's Read tool can open
other files in the tree. Its definition forbids that; nothing enforces it.

    python3 researcher_us/scripts/edge_shadow_engine.py collect --from-run research/2026/09/2026-09-22/edge
    python3 researcher_us/scripts/edge_shadow_engine.py brief -o /tmp/brief.json
    python3 researcher_us/scripts/edge_shadow_engine.py ingest
    python3 researcher_us/scripts/edge_shadow_engine.py measure
    python3 researcher_us/scripts/edge_shadow_engine.py fit
"""
import argparse
import hashlib
import html
import json
import math
import re
import statistics as st
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "researcher_us" / "analysis" / "shadow-ledger.json"
SHADOW_DIR = REPO / "researcher_us" / "analysis" / "shadow"
CONFIG = REPO / "config" / "pipeline.yaml"

SEC_UA = "claude_research edge/shadow (xavier.friesen@socfin.nl)"
WEB_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
TICKER_MAP = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
ARCHIVE = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}"
CHART = ("https://query1.finance.yahoo.com/v8/finance/chart/{t}"
         "?range={rg}&interval={iv}{pp}")

# Distinct by construction: each names a different end point. PR #9's `1d` was the
# next session's close under another name.
TIMEFRAMES = ["5m", "15m", "60m", "session_close", "next_open", "next_close",
              "1d", "5d", "1m"]
INTRADAY = {"5m": 300, "15m": 900, "60m": 3600, "1d": 86400}
CLOSES_AFTER = {"session_close": 1, "next_close": 2, "5d": 5, "1m": 21}
LINES = ["reported_quarter", "guidance", "one_off", "financing", "capital_return",
         "positioning", "other"]
TAG = re.compile(r"<[^>]+>")
# Inline XBRL carries a hidden header of facts ("true true NASDAQ 0000320193 ...")
# ahead of the words; the scorer should read the filing, not its tagging.
HIDDEN = re.compile(r"<ix:header>.*?</ix:header>|<(script|style)[^>]*>.*?</\1>|"
                    r"<div[^>]*display:\s*none[^>]*>.*?</div>", re.S | re.I)
# EDGAR's rendered XBRL pages (R1.htm ...) and the full-submission .txt restate the
# filing as a table dump; neither is what a reader of the release saw.
NOT_A_DOCUMENT = re.compile(r"^R\d+\.htm$|index|FilingSummary|\.txt$", re.I)


# ------------------------------------------------------------------ config

def config():
    try:
        import yaml
        return (yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}).get("edge_v2") or {}
    except Exception:                                   # noqa: BLE001
        return {}


def cfg(key, default):
    v = config().get(key)
    return default if v is None else v


# ------------------------------------------------------------------ ledger

def load_ledger(path=LEDGER):
    path = Path(path)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"schema": 2, "items": [], "response_matrix": {}}


def save_ledger(doc, path=LEDGER):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------ EDGAR

_last = [0.0]


def http(url, ua=SEC_UA, as_json=True, tries=4):
    """SEC asks for ten requests a second and answers 429 rather than slowing down."""
    for n in range(tries):
        gap = 0.13 - (time.monotonic() - _last[0])
        if gap > 0:
            time.sleep(gap)
        _last[0] = time.monotonic()
        try:
            body = urllib.request.urlopen(urllib.request.Request(
                url, headers={"User-Agent": ua, "Accept-Encoding": "identity"}),
                timeout=30).read()
            return json.loads(body) if as_json else body.decode("utf-8", "ignore")
        except Exception as exc:                        # noqa: BLE001
            if n == tries - 1:
                return None
            time.sleep((2.5 if "429" in str(exc) else 0.8) * (n + 1))


def filing_text(cik, acc, primary, limit):
    """The primary document and its EX-99 exhibits, tags stripped, capped."""
    base = ARCHIVE.format(cik=int(cik), acc=acc.replace("-", ""))
    idx = http(base + "/index.json") or {}
    names = [f["name"] for f in (idx.get("directory") or {}).get("item", [])
             if f["name"].lower().endswith((".htm", ".html"))
             and not NOT_A_DOCUMENT.search(f["name"])]
    # The release is the EX-99 exhibit; the 8-K wrapper mostly names the item.
    names.sort(key=lambda s: (0 if "ex99" in s.lower().replace("-", "").replace("_", "")
                              else 1 if s == primary else 2, len(s)))
    parts, urls = [], []
    for name in names[:3]:
        raw = http(f"{base}/{name}", as_json=False)
        if not raw:
            continue
        txt = re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", HIDDEN.sub(" ", raw)))).strip()
        parts.append(txt)
        urls.append(f"{base}/{name}")
        if sum(len(p) for p in parts) >= limit:
            break
    return " \n\n".join(parts)[:limit], urls


def collect(tickers, since, until=None, ledger_path=LEDGER, limit_chars=None,
            per_ticker=None):
    limit_chars = limit_chars or int(cfg("input_max_chars", 12000))
    per_ticker = per_ticker or int(cfg("max_filings_per_ticker", 8))
    min_date = str(cfg("min_event_date", "2026-07-01"))
    since = max(since, min_date)
    doc = load_ledger(ledger_path)
    have = {it["id"] for it in doc["items"]}
    tmap = http(TICKER_MAP)
    if not tmap:
        sys.exit("SEC ticker map unreachable")
    ciks = {v["ticker"].upper(): str(v["cik_str"]).zfill(10) for v in tmap.values()}
    added, skipped = 0, {}
    (SHADOW_DIR / "inputs").mkdir(parents=True, exist_ok=True)
    for t in sorted(set(x.upper() for x in tickers)):
        cik = ciks.get(t) or ciks.get(t.replace(".", "-"))
        if not cik:
            skipped[t] = "no CIK"
            continue
        sub = http(SUBMISSIONS.format(cik=cik))
        if not sub:
            skipped[t] = "submissions unreachable"
            continue
        r = sub["filings"]["recent"]
        n_t = 0
        for i in range(len(r["form"])):
            if not r["form"][i].startswith("8-K"):
                continue
            d = r["filingDate"][i]
            if d < since or (until and d > until):
                continue
            acc = r["accessionNumber"][i]
            iid = f"{t}-{acc}"
            if iid in have:
                continue
            if n_t >= per_ticker:
                break
            n_t += 1
            text, urls = filing_text(cik, acc, r["primaryDocument"][i], limit_chars)
            if not text:
                skipped[iid] = "no document text"
                continue
            t0 = r["acceptanceDateTime"][i].replace(".000Z", "Z")
            inp = {"id": iid, "ticker": t, "company": sub.get("name"),
                   "form": r["form"][i], "items": r["items"][i],
                   "t0_utc": t0, "text": text}
            # The scorer reads exactly this file; its hash is what `ingest` checks.
            body = json.dumps(inp, indent=1, sort_keys=True, ensure_ascii=False)
            (SHADOW_DIR / "inputs" / f"{iid}.json").write_text(body + "\n",
                                                               encoding="utf-8")
            doc["items"].append({
                "id": iid, "ticker": t, "cik": cik, "form": r["form"][i],
                "items": r["items"][i], "t0_utc": t0, "sources": urls,
                "input_sha256": sha(body), "status": "collected",
                "collected_utc": now()})
            have.add(iid)
            added += 1
    save_ledger(doc, ledger_path)
    return added, skipped


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(p):
    try:
        return str(Path(p).relative_to(REPO))
    except ValueError:
        return str(p)


def brief(ledger_path=LEDGER, max_items=None):
    max_items = max_items or int(cfg("max_items_per_run", 40))
    doc = load_ledger(ledger_path)
    todo = [it for it in doc["items"] if it["status"] == "collected"][:max_items]
    return {"inputs": [rel(SHADOW_DIR / "inputs" / f"{it['id']}.json") for it in todo],
            "outputs_dir": rel(SHADOW_DIR / "scores"),
            "hashes": {it["id"]: it["input_sha256"] for it in todo},
            "lines": LINES}


def ingest(ledger_path=LEDGER, scores_dir=None):
    scores_dir = Path(scores_dir or SHADOW_DIR / "scores")
    doc = load_ledger(ledger_path)
    by_id = {it["id"]: it for it in doc["items"]}
    ok, refused = 0, {}
    for f in sorted(scores_dir.glob("*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        it = by_id.get(s.get("id"))
        if not it:
            refused[f.name] = "unknown id"
            continue
        if it["status"] != "collected":
            continue                                    # already ingested
        # Both checks: the score names the collected hash, and the file on disk still
        # hashes to it -- so nothing edited the input between collect and score.
        on_disk = SHADOW_DIR / "inputs" / f"{it['id']}.json"
        disk_ok = on_disk.exists() and sha(on_disk.read_text(encoding="utf-8").rstrip("\n")) \
            == it["input_sha256"]
        if s.get("input_sha256") != it["input_sha256"] or not disk_ok:
            refused[f.name] = "input hash mismatch: the scored file is not the collected one"
            continue
        try:
            score = float(s["expected_impact_pct"])
        except (KeyError, TypeError, ValueError):
            refused[f.name] = "no numeric expected_impact_pct"
            continue
        line = s.get("lands_on") if s.get("lands_on") in LINES else "other"
        it.update({"llm_impact_score": score, "line_item": line,
                   "score_basis": (s.get("basis") or "")[:400],
                   "scorer": s.get("scorer", "shadow-scorer"),
                   "scored_utc": s.get("scored_utc") or now(),
                   "status": "scored"})
        ok += 1
    save_ledger(doc, ledger_path)
    return ok, refused


# ------------------------------------------------------------------ bars

_bars = {}


def _chart(ticker, rng, iv, prepost):
    key = (ticker, rng, iv, prepost)
    if key in _bars:
        return _bars[key]
    url = CHART.format(t=ticker.upper().replace(".", "-"), rg=rng, iv=iv,
                       pp="&includePrePost=true" if prepost else "")
    j = http(url, ua=WEB_UA)
    out = []
    try:
        res = j["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        for i, ts in enumerate(res["timestamp"]):
            if q["close"][i] is None:
                continue
            out.append({"ts": ts, "open": q["open"][i], "close": q["close"][i]})
    except (TypeError, KeyError, IndexError):
        out = []
    _bars[key] = out
    return out


def daily(ticker):
    rows = _chart(ticker, "2y", "1d", False)
    for r in rows:
        r["date"] = datetime.fromtimestamp(r["ts"], timezone.utc).astimezone(ET).date()
    return rows


def intraday(ticker):
    return _chart(ticker, "60d", "5m", True)


def session_bounds(d):
    o = datetime(d.year, d.month, d.day, 9, 30, tzinfo=ET)
    c = datetime(d.year, d.month, d.day, 16, 0, tzinfo=ET)
    return o.timestamp(), c.timestamp()


def price_at_or_before(bars, epoch):
    """Close of the last bar that ENDS at or before epoch (5-minute bars)."""
    v = [b for b in bars if b["ts"] + 300 <= epoch]
    return v[-1]["close"] if v else None


def sigma_and_beta(stock, spy, t0_date, lookback_sigma=20, lookback_beta=60):
    """Both as of t0: only sessions strictly before the event's date."""
    s = {r["date"]: r["close"] for r in stock if r["date"] < t0_date}
    m = {r["date"]: r["close"] for r in spy if r["date"] < t0_date}
    ds = sorted(s)
    rets = [(s[ds[i]] / s[ds[i - 1]] - 1) * 100 for i in range(1, len(ds))]
    sigma = round(st.pstdev(rets[-lookback_sigma:]), 4) if len(rets) >= lookback_sigma else None
    common = sorted(set(s) & set(m))[-(lookback_beta + 1):]
    beta = None
    if len(common) >= 21:
        a = [s[common[i]] / s[common[i - 1]] - 1 for i in range(1, len(common))]
        b = [m[common[i]] / m[common[i - 1]] - 1 for i in range(1, len(common))]
        vb = st.pvariance(b)
        if vb > 0:
            ma, mb = st.fmean(a), st.fmean(b)
            beta = round(sum((x - ma) * (y - mb) for x, y in zip(a, b)) / len(a) / vb, 3)
    return sigma, beta


def moves_for(t0_utc, stock_d, spy_d, stock_i, spy_i, beta):
    """Raw and beta-stripped moves at nine horizons from one reference.

    The reference is the price at t0 when t0 falls inside the regular session and
    intraday bars reach it, and otherwise the last regular close before t0 -- the
    same convention `edge_resolve.py` uses for a print. Every horizon has a status;
    a missing number never reads as zero.
    """
    t0 = datetime.fromisoformat(t0_utc.replace("Z", "+00:00"))
    ep = t0.timestamp()
    t0_et = t0.astimezone(ET)
    o, c = session_bounds(t0_et.date())
    in_session = o <= ep < c
    trade_days = [r["date"] for r in stock_d]
    s_close = {r["date"]: r["close"] for r in stock_d}
    s_open = {r["date"]: r["open"] for r in stock_d}
    m_close = {r["date"]: r["close"] for r in spy_d}
    m_open = {r["date"]: r["open"] for r in spy_d}

    before = [d for d in trade_days if session_bounds(d)[1] <= ep]
    after_close = [d for d in trade_days if session_bounds(d)[1] > ep]
    after_open = [d for d in trade_days if session_bounds(d)[0] > ep]
    ref_d = before[-1] if before else None

    p0 = m0 = None
    ref_basis = "prior_close"
    if in_session:
        p0 = price_at_or_before(stock_i, ep)
        m0 = price_at_or_before(spy_i, ep)
        if p0 and m0:
            ref_basis = "intraday_t0"
    if ref_basis == "prior_close":
        if ref_d is None:
            return {"_ref": None}, "no close before t0"
        p0, m0 = s_close.get(ref_d), m_close.get(ref_d)
    # Intraday horizons start from the price AT t0, including extended hours,
    # whatever the daily reference is.
    ip0 = price_at_or_before(stock_i, ep)
    im0 = price_at_or_before(spy_i, ep)

    def pair(raw_s, raw_m):
        if raw_s is None:
            return {"raw_pct": None, "excess_pct": None, "status": "no_price"}
        if raw_m is None or beta is None:
            return {"raw_pct": round(raw_s, 3), "excess_pct": None,
                    "status": "no_benchmark" if raw_m is None else "no_beta"}
        return {"raw_pct": round(raw_s, 3),
                "excess_pct": round(raw_s - beta * raw_m, 3), "status": "ok"}

    out = {"_ref": {"basis": ref_basis, "in_session": in_session,
                    "ref_date": ref_d.isoformat() if ref_d else None}}
    now_ep = time.time()
    for tf, dt in INTRADAY.items():
        if ep + dt > now_ep:
            out[tf] = {"raw_pct": None, "excess_pct": None, "status": "pending"}
            continue
        if not stock_i or stock_i[0]["ts"] > ep or ip0 is None:
            out[tf] = {"raw_pct": None, "excess_pct": None,
                       "status": "intraday_window_passed"}
            continue
        p1 = price_at_or_before(stock_i, ep + dt)
        m1 = price_at_or_before(spy_i, ep + dt)
        out[tf] = pair((p1 / ip0 - 1) * 100 if p1 else None,
                       (m1 / im0 - 1) * 100 if (m1 and im0) else None)
    for tf, k in CLOSES_AFTER.items():
        if len(after_close) < k:
            out[tf] = {"raw_pct": None, "excess_pct": None, "status": "pending"}
            continue
        d = after_close[k - 1]
        if session_bounds(d)[1] > now_ep:
            # Yahoo's daily series carries today's bar while the session trades;
            # its "close" is a live price until 16:00 ET.
            out[tf] = {"raw_pct": None, "excess_pct": None, "status": "pending"}
            continue
        p1, m1 = s_close.get(d), m_close.get(d)
        out[tf] = pair((p1 / p0 - 1) * 100 if p1 else None,
                       (m1 / m0 - 1) * 100 if (m1 and m0) else None)
        out[tf]["end_date"] = d.isoformat()
    if not after_open:
        out["next_open"] = {"raw_pct": None, "excess_pct": None, "status": "pending"}
    else:
        d = after_open[0]
        p1, m1 = s_open.get(d), m_open.get(d)
        out["next_open"] = pair((p1 / p0 - 1) * 100 if p1 else None,
                                (m1 / m0 - 1) * 100 if (m1 and m0) else None)
        out["next_open"]["end_date"] = d.isoformat()
    return out, None


def measure(ledger_path=LEDGER):
    doc = load_ledger(ledger_path)
    spy_d, spy_i = daily("SPY"), intraday("SPY")
    n_done = n_pending = 0
    for it in doc["items"]:
        if it["status"] not in ("scored", "measuring"):
            continue                                    # never measure before a score
        t0 = datetime.fromisoformat(it["t0_utc"].replace("Z", "+00:00"))
        sd, si = daily(it["ticker"]), intraday(it["ticker"])
        if not sd:
            it["measure_note"] = "no daily bars"
            continue
        sigma, beta = sigma_and_beta(sd, spy_d, t0.astimezone(ET).date())
        mv, err = moves_for(it["t0_utc"], sd, spy_d, si, spy_i, beta)
        prev = it.get("moves") or {}
        for tf in TIMEFRAMES:
            # Keep a number already measured: the 60-day intraday window slides,
            # and a re-measure a month later would otherwise erase the 5m move.
            if (prev.get(tf) or {}).get("status") == "ok" and mv.get(tf, {}).get("status") != "ok":
                mv[tf] = prev[tf]
        it.update({"sigma_daily_pct": sigma, "beta": beta, "moves": mv,
                   "reference": mv.pop("_ref", None), "measured_utc": now()})
        if err:
            it["measure_note"] = err
        pending = any((mv.get(tf) or {}).get("status") == "pending" for tf in TIMEFRAMES)
        it["status"] = "measuring" if pending else "measured"
        n_pending += pending
        n_done += not pending
    save_ledger(doc, ledger_path)
    return n_done, n_pending


# ------------------------------------------------------------------ fit

def kappa_fit(pairs):
    """Least squares through the origin: y = kappa * S.

    y is the beta-stripped move over sigma. Returns kappa, its standard error and n.
    """
    n = len(pairs)
    sxx = sum(x * x for x, _ in pairs)
    if n == 0 or sxx == 0:
        return None
    k = sum(x * y for x, y in pairs) / sxx
    se = None
    if n >= 3:
        rss = sum((y - k * x) ** 2 for x, y in pairs)
        se = math.sqrt(rss / (n - 1) / sxx)
    r = None
    if n >= 3:
        xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]
        if st.pstdev(xs) > 0 and st.pstdev(ys) > 0:
            r = round(st.correlation(xs, ys), 3)
    return {"kappa": round(k, 5), "se": None if se is None else round(se, 5),
            "ci95": None if se is None else [round(k - 1.96 * se, 5),
                                             round(k + 1.96 * se, 5)],
            "n": n, "pearson": r}


def horizon_end(it, tf):
    """When horizon tf of this item stopped moving, as an aware datetime, or None."""
    t0 = datetime.fromisoformat(it["t0_utc"].replace("Z", "+00:00"))
    if tf in INTRADAY:
        return t0 + timedelta(seconds=INTRADAY[tf])
    end = ((it.get("moves") or {}).get(tf) or {}).get("end_date")
    if not end:
        return None
    d = date.fromisoformat(end)
    hh, mm = (9, 30) if tf == "next_open" else (16, 0)
    return datetime(d.year, d.month, d.day, hh, mm, tzinfo=ET)


def fit_matrix(items, as_of=None):
    """kappa per (line, horizon) and pooled per horizon, from scored-and-measured items.

    `as_of` keeps, per horizon, only observations whose END point lies before it, so a
    matrix can be rebuilt exactly as it stood on a run date. Filtering on t0 alone is
    not enough: an 8-K filed an hour before the seal has its session close after it,
    and when it is the hunted name's own filing that close IS the run's outcome.
    """
    cut = (datetime.fromisoformat(as_of.replace("Z", "+00:00")) if as_of else None)
    obs = [it for it in items
           if it.get("llm_impact_score") not in (None, 0) and it.get("sigma_daily_pct")
           and not (as_of and it["t0_utc"] >= as_of)]
    matrix = {"_pooled": {}}
    for tf in TIMEFRAMES:
        pooled, by_line = [], {}
        for it in obs:
            m = (it.get("moves") or {}).get(tf) or {}
            if m.get("status") != "ok" or m.get("excess_pct") is None:
                continue
            if cut is not None:
                end = horizon_end(it, tf)
                if end is None or end >= cut:
                    continue
            p = (it["llm_impact_score"], m["excess_pct"] / it["sigma_daily_pct"])
            pooled.append(p)
            by_line.setdefault(it.get("line_item", "other"), []).append(p)
        matrix["_pooled"][tf] = kappa_fit(pooled)
        for line, ps in by_line.items():
            matrix.setdefault(line, {})[tf] = kappa_fit(ps)
    return matrix, len(obs)


def fit(ledger_path=LEDGER, as_of=None):
    doc = load_ledger(ledger_path)
    matrix, n = fit_matrix(doc["items"], as_of)
    doc.update({"response_matrix": matrix, "fitted_utc": now(),
                "fitted_as_of": as_of, "n_observations": n})
    save_ledger(doc, ledger_path)
    return matrix


def tickers_from_run(run):
    run = Path(run)
    u = json.loads((run / "universe.json").read_text(encoding="utf-8"))
    rows = u.get("rows") or u.get("universe") or u.get("names") or []
    out = [r.get("ticker") for r in rows if isinstance(r, dict) and r.get("ticker")]
    if not out:
        out = [p.stem for p in (run / "baselines").glob("*.json")]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=str(LEDGER))
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--tickers", help="comma-separated")
    c.add_argument("--from-run", action="append", default=[],
                   help="an edge run directory; its universe's tickers")
    c.add_argument("--since", default=None)
    c.add_argument("--until", default=None)
    b = sub.add_parser("brief")
    b.add_argument("-o", "--out")
    b.add_argument("--max-items", type=int)
    sub.add_parser("ingest")
    sub.add_parser("measure")
    f = sub.add_parser("fit")
    f.add_argument("--as-of", help="UTC timestamp; only items with t0 before it")
    sub.add_parser("status")
    a = ap.parse_args()

    if a.cmd == "collect":
        ts = [t for t in (a.tickers or "").split(",") if t]
        for r in a.from_run:
            ts += tickers_from_run(r)
        if not ts:
            sys.exit("give --tickers or --from-run")
        since = a.since or (date.today() - timedelta(days=90)).isoformat()
        added, skipped = collect(ts, since, a.until, a.ledger)
        print(f"collected {added} new 8-Ks for {len(set(ts))} tickers since {since}")
        for k, v in list(skipped.items())[:20]:
            print(f"  skipped {k}: {v}")
    elif a.cmd == "brief":
        br = brief(a.ledger, a.max_items)
        text = json.dumps(br, indent=1)
        if a.out:
            Path(a.out).write_text(text + "\n", encoding="utf-8")
        print(text if not a.out else f"{len(br['inputs'])} inputs -> {a.out}")
    elif a.cmd == "ingest":
        ok, refused = ingest(a.ledger)
        print(f"ingested {ok} scores")
        for k, v in refused.items():
            print(f"  REFUSED {k}: {v}")
    elif a.cmd == "measure":
        done, pending = measure(a.ledger)
        print(f"measured {done} complete, {pending} with horizons still pending")
    elif a.cmd == "fit":
        m = fit(a.ledger, a.as_of)
        min_n = int(cfg("min_n", 30))
        for tf in TIMEFRAMES:
            p = m["_pooled"].get(tf)
            if p:
                flag = "" if p["n"] >= min_n else f"   (below min_n={min_n})"
                print(f"  {tf:14s} kappa {p['kappa']:+.4f}  se {p['se']}  n {p['n']}{flag}")
            else:
                print(f"  {tf:14s} no observations")
    elif a.cmd == "status":
        doc = load_ledger(a.ledger)
        cnt = {}
        for it in doc["items"]:
            cnt[it["status"]] = cnt.get(it["status"], 0) + 1
        print(json.dumps({"items": len(doc["items"]), "by_status": cnt,
                          "fitted_utc": doc.get("fitted_utc"),
                          "n_observations": doc.get("n_observations")}, indent=1))


if __name__ == "__main__":
    main()

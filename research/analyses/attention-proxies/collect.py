#!/usr/bin/env python3
"""Collect candidate ATTENTION proxies for every resolved, de-duplicated US name.

Every proxy is dated before the entry (the run date), except the StockTwits watcher
count, which is today's snapshot and is labelled so. Run from the repo root:

    python3 research/analyses/attention-proxies/collect.py

Writes proxies.json beside this file; network results are cached in cache.json so a
rerun does not refetch.
"""
import json
import statistics as st
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CACHE = HERE / "cache.json"
UA = "claude_research/0.1 (robertsben333@gmail.com) attention-proxy research"
cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def get(url, headers=None, tries=3):
    if url in cache:
        return cache[url]
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read().decode("utf-8")
            cache[url] = body
            return body
        except urllib.error.HTTPError as e:
            if e.code == 404:
                cache[url] = None
                return None
            time.sleep(3 * (i + 1))
        except Exception:                                   # noqa: BLE001
            time.sleep(3 * (i + 1))
    return None


def save():
    CACHE.write_text(json.dumps(cache) + "\n")


def names():
    d = load(REPO / "dashboard" / "data" / "ledger.json")
    return [r for r in d["names"] if not r.get("duplicate_event") and r.get("impact_sum")
            and r.get("ret_strategy") is not None]


# ------------------------------------------------------------------ from disk
def disk(r):
    run = REPO / r["run"]
    b = load(run / "baselines" / f"{r['ticker']}.json") or {}
    tape, opt = b.get("tape") or {}, b.get("options") or {}
    uni = load(run / "universe.json") or {}
    u = next((x for x in (uni.get("names") or uni.get("rows") or [])
              if x.get("ticker") == r["ticker"]), {})
    try:
        n_est = int(str(u.get("n_estimates")).strip())
    except (TypeError, ValueError):
        n_est = None
    avgv = tape.get("avg_volume_20d")
    oi = opt.get("total_open_interest") if opt.get("status") == "ok" else None
    hunt = load(run / "hunts" / f"{r['ticker']}.json") or {}
    su = hunt.get("sources_used")
    if isinstance(su, (int, float)):          # some hunts report a count, not a list
        n_src = int(su)
    else:
        urls = set()
        for s in su or []:
            u_ = s.get("url") if isinstance(s, dict) else s
            if isinstance(u_, str) and u_.startswith("http"):
                urls.add(u_.split("#")[0])
        n_src = len(urls) if hunt else None
    return {
        "n_estimates": n_est,
        "has_options": opt.get("status") == "ok",
        "oi_to_volume": (100 * oi / avgv) if oi and avgv else (0.0 if avgv else None),
        "option_spread": opt.get("atm_spread_frac_of_mid") if opt.get("status") == "ok" else None,
        "pct_from_52w_high": tape.get("pct_from_52w_high"),
        "abs_runup_5d": abs(tape["run_up_5d_pct"]) if tape.get("run_up_5d_pct") is not None else None,
        "hunt_sources": n_src,
    }


# --------------------------------------------------------------- Yahoo volume
def volume(r):
    """Abnormal volume into the run: mean of the 5 sessions before the run date over
    the mean of the 60 before those."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{r['ticker']}"
           f"?range=2y&interval=1d")
    body = get(url)
    if not body:
        return {}
    try:
        res = json.loads(body)["chart"]["result"][0]
        ts, vol = res["timestamp"], res["indicators"]["quote"][0]["volume"]
    except (KeyError, IndexError, TypeError, ValueError):
        return {}
    day = date.fromisoformat(r["run_date"])
    rows = [(datetime.fromtimestamp(t, timezone.utc).date(), v) for t, v in zip(ts, vol)
            if v is not None]
    before = [v for d, v in rows if d < day]
    if len(before) < 65:
        return {}
    recent, base = st.fmean(before[-5:]), st.fmean(before[-65:-5])
    return {"abnormal_volume_5d": recent / base if base else None}


# ----------------------------------------------------------------- Wikipedia
EXCH = "wd:Q13677 wd:Q82059 wd:Q846626"   # NYSE, Nasdaq, NYSE American


def wiki_titles(tickers):
    out = {}
    tick = sorted(set(tickers))
    for i in range(0, len(tick), 60):
        vals = " ".join(f'"{t}"' for t in tick[i:i + 60])
        q = (f"SELECT ?t ?a WHERE {{ VALUES ?t {{{vals}}} VALUES ?ex {{{EXCH}}} "
             f"?c p:P414 ?s . ?s ps:P414 ?ex ; pq:P249 ?t . "
             f"?a schema:about ?c ; schema:isPartOf <https://en.wikipedia.org/> . }}")
        url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode(
            {"query": q, "format": "json"})
        body = get(url, {"Accept": "application/sparql-results+json"})
        for b in (json.loads(body)["results"]["bindings"] if body else []):
            out.setdefault(b["t"]["value"], b["a"]["value"].rsplit("/wiki/", 1)[1])
        time.sleep(1)
    return out


def wiki(title, run_date):
    if not title:
        return {"has_wikipedia": False}
    end = date.fromisoformat(run_date) - timedelta(days=1)
    start = end - timedelta(days=89)
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/"
           f"all-access/user/{urllib.parse.quote(title, safe='')}/daily/"
           f"{start:%Y%m%d}00/{end:%Y%m%d}00")
    body = get(url)
    time.sleep(0.2)
    if not body:
        return {"has_wikipedia": True}
    v = [x["views"] for x in json.loads(body).get("items", [])]
    if len(v) < 30:
        return {"has_wikipedia": True}
    med = st.median(v)
    return {"has_wikipedia": True, "wiki_views_median": med,
            "wiki_spike_3d": st.fmean(v[-3:]) / (med + 1)}


# ----------------------------------------------------------------- StockTwits
def stocktwits(t):
    body = get(f"https://api.stocktwits.com/api/2/streams/symbol/{t}.json")
    time.sleep(0.5)
    try:
        return {"stocktwits_watchers_now": json.loads(body)["symbol"]["watchlist_count"]}
    except (TypeError, KeyError, ValueError):
        return {}


def main():
    rows = names()
    titles = wiki_titles([r["ticker"] for r in rows])
    save()
    out = []
    for i, r in enumerate(rows):
        p = {"ticker": r["ticker"], "run_date": r["run_date"], "run": r["run"],
             "wiki_title": titles.get(r["ticker"])}
        p.update(disk(r))
        p.update(volume(r))
        p.update(wiki(titles.get(r["ticker"]), r["run_date"]))
        p.update(stocktwits(r["ticker"]))
        out.append(p)
        if i % 20 == 0:
            save()
            print(f"  {i}/{len(rows)} {r['ticker']}")
    save()
    (HERE / "proxies.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"wrote {len(out)} rows; wikipedia titles for {len(titles)} tickers")


if __name__ == "__main__":
    main()

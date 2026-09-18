#!/usr/bin/env python3
"""Does how much the public is googling a company predict the trade on its print?

The hunt looks for information the market has not priced. Google search interest is
the cheapest available proxy for the opposite thing -- how much ATTENTION a name is
carrying into its print -- and attention is the channel through which a retail-held
small cap reprices. Two readings, and they are different claims:

  LEVEL      how much interest the name carries at all. A name nobody searches for
             is a name with no retail bid to surprise.
  SPIKE      the entry-day level against the name's own 90-day median. This is the
             one that could carry information the baseline does not: a name being
             googled three times its normal rate on the day of its print is a name
             something has already happened to.

WHERE THE NUMBERS COME FROM. Google Trends, daily resolution, US geography, the
90 days ending on the entry day, queried through the same public endpoint the
`pytrends` package uses -- an explore call for a token, then the multiline widget.
Interest is RELATIVE, 0-100 against the series' own maximum, and each series is
fetched alone, so levels are NOT comparable between companies. Only the spike is,
which is why the spike is the measure the correlations use.

THE FLOOR IS THE FINDING FOR HALF THE SAMPLE. Google reports zero for a query below
its own reporting threshold, and most of the names this stage hunts are microcaps.
A series that is all zeros is not "no interest measured at low precision", it is no
measurement at all, and those names are reported separately rather than scored as
zeros -- averaging them in would manufacture a correlation out of market cap.

QUERY CHOICE IS A REAL DEGREE OF FREEDOM, so it is fixed in advance and stated: the
company name as the run's own `universe.json` recorded it, with the legal suffix
stripped (Inc, Corp, Corporation, Ltd, Limited, plc, Company, Co, Holdings, Group,
SA, NV, AG). Not the ticker -- "TRT" and "RH" are English words and would return
noise. One query per company, no alternatives tried, no picking the one that works.

    python3 researcher_us/scripts/edge_search_volume.py
    python3 researcher_us/scripts/edge_search_volume.py --refresh
"""
import argparse
import http.cookiejar
import json
import re
import statistics as st
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import edge_runup as RU         # noqa: E402
import edge_sample as ES        # noqa: E402
import edge_stats as SS         # noqa: E402

CACHE = REPO / "researcher_us" / "analysis" / "trends-cache.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
SUFFIXES = re.compile(
    r"[,\s]+(inc|inc\.|incorporated|corp|corp\.|corporation|co|co\.|company|companies"
    r"|ltd|ltd\.|limited|plc|llc|lp|holdings?|holding|group|s\.?a\.?|n\.?v\.?|a\.?g\.?"
    r"|the)\.?$", re.I)

_opener = None


def query_for(company, ticker):
    """The fixed rule, applied once. No per-name tuning."""
    q = (company or ticker).strip()
    prev = None
    while prev != q:                      # "Acme Holdings Inc." -> "Acme"
        prev = q
        q = SUFFIXES.sub("", q).strip(" ,.")
    return q or ticker


def _session():
    global _opener
    if _opener is None:
        cj = http.cookiejar.CookieJar()
        _opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        _opener.addheaders = [("User-Agent", UA), ("Accept-Language", "en-US,en;q=0.9")]
        _opener.open("https://trends.google.com/?geo=US", timeout=30).read(64)
    return _opener


def _strip(raw):
    return json.loads(raw.decode("utf8").split("\n", 1)[1])


def fetch_series(keyword, start, end, geo="US", tries=4):
    """Daily interest for [start, end]. Returns (list of (date, value), error)."""
    tf = f"{start} {end}"
    for i in range(tries):
        try:
            op = _session()
            req = {"comparisonItem": [{"keyword": keyword, "geo": geo, "time": tf}],
                   "category": 0, "property": ""}
            u = ("https://trends.google.com/trends/api/explore?hl=en-US&tz=0&req="
                 + urllib.parse.quote(json.dumps(req)))
            w = [x for x in _strip(op.open(u, timeout=40).read())["widgets"]
                 if x["id"] == "TIMESERIES"]
            if not w:
                return None, "no TIMESERIES widget"
            w = w[0]
            u2 = ("https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=0&req="
                  + urllib.parse.quote(json.dumps(w["request"])) + "&token=" + w["token"])
            d = _strip(op.open(u2, timeout=40).read())
            pts = [(p.get("formattedTime") or p.get("formattedAxisTime"), p["value"][0])
                   for p in d["default"]["timelineData"]]
            return pts, None
        except Exception as e:                            # noqa: BLE001
            err = f"{type(e).__name__}: {str(e)[:80]}"
            globals()["_opener"] = None                   # new cookie on the retry
            time.sleep(6 * (i + 1))
    return None, err


def series_for(ticker, keyword, entry_day, refresh=False):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    key = f"{ticker}|{keyword}|{entry_day}"
    if key in cache and not refresh:
        v = cache[key]
        return v.get("pts"), v.get("err")
    end = datetime.fromisoformat(entry_day).date()
    start = end - timedelta(days=89)
    pts, err = fetch_series(keyword, start.isoformat(), end.isoformat())
    cache[key] = {"pts": pts, "err": err, "keyword": keyword,
                  "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache) + "\n")
    time.sleep(2.5)                        # Trends rate-limits hard; this is the price
    return pts, err


def measures(pts):
    """level, spike and 7-day trend, or None where Google reported nothing."""
    vals = [v for _, v in pts]
    if not vals or max(vals) == 0:
        return None
    med = st.median(vals) or 0.0
    last = vals[-1]
    week = st.mean(vals[-7:])
    prior = st.mean(vals[-30:-7]) if len(vals) > 30 else med
    return {
        "level_median_90d": med,
        "level_entry_day": last,
        "level_week": week,
        # the entry day against the name's own normal. +1 in the denominator keeps a
        # near-silent name from producing a 40x spike off a single search-day
        "spike_day": round(last / (med + 1), 3),
        "spike_week": round(week / (med + 1), 3),
        "trend_7v30": round(week / (prior + 1), 3),
        "zero_days": sum(1 for v in vals if v == 0), "n_days": len(vals),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pool", default="research/2026/*/*/edge")
    ap.add_argument("--floor", type=float, default=3.0)
    ap.add_argument("--exit", default="close", choices=["close", "open"])
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--out", default="researcher_us/analysis/edge-search-volume.json")
    a = ap.parse_args()
    ek = f"trade_{a.exit}"
    mk = f"move_{a.exit}"

    rows, _ = RU.build(ES.load(a.pool))
    print(f"{len(rows)} events. Querying Google Trends, 90 days to each entry day.\n")

    scored, silent, failed = [], [], []
    for r in rows:
        q = query_for(r.get("company"), r["ticker"])
        pts, err = series_for(r["ticker"], q, r["entry_day"], a.refresh)
        r["trends_query"] = q
        if err or pts is None:
            r["trends_error"] = err
            failed.append(r)
            print(f"  {r['ticker']:8s} {q[:34]:34s} FAILED  {err}")
            continue
        m = measures(pts)
        if m is None:
            silent.append(r)
            print(f"  {r['ticker']:8s} {q[:34]:34s} below Google's reporting threshold")
            continue
        r.update(m)
        scored.append(r)
        print(f"  {r['ticker']:8s} {q[:34]:34s} median {m['level_median_90d']:>5.1f}"
              f"  entry-day {m['level_entry_day']:>3.0f}"
              f"  spike {m['spike_day']:>5.2f}x  ({m['zero_days']}/{m['n_days']} zero days)")

    print(f"\n{len(scored)} measured, {len(silent)} below the reporting threshold, "
          f"{len(failed)} failed.\n")

    res = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "n_events": len(rows), "n_measured": len(scored), "n_silent": len(silent),
           "n_failed": len(failed), "exit": a.exit, "floor": a.floor,
           "silent": [{"ticker": r["ticker"], "company": r.get("company"),
                       "query": r["trends_query"], "dollar_vol": r["dollar_vol"]}
                      for r in silent],
           "failed": [{"ticker": r["ticker"], "why": r.get("trends_error")} for r in failed],
           "correlations": {}, "buckets": {}, "rows": [
               {k: v for k, v in r.items() if k != "prices"} for r in scored]}

    # ------------------------------------------------------------- correlations
    print("SEARCH INTEREST AGAINST THE TRADE. rho is Spearman with a permutation p.")
    print("`trade` is the book's own return, signed by impact_sum and entered at")
    print("20:00 CET. `|move|` is how far the stock went in either direction -- a")
    print("separate claim, and the one attention would most plausibly drive.\n")
    print(f"  {'measure':22s}{'n':>5s}{'rho vs trade':>14s}{'p':>8s}"
          f"{'rho vs |move|':>15s}{'p':>8s}")
    pools = [("all measured", scored),
             (f"conviction >= {a.floor}", [r for r in scored
                                           if abs(r["impact_sum"] or 0) >= a.floor])]
    for pname, pool in pools:
        print(f"\n  -- {pname}, n={len(pool)}")
        for m in ("spike_day", "spike_week", "trend_7v30", "level_median_90d",
                  "level_entry_day"):
            rs = [r for r in pool if r.get(m) is not None and r.get(ek) is not None]
            if len(rs) < 6:
                continue
            x = [r[m] for r in rs]
            r1, p1 = SS.spearman_perm(x, [r[ek] for r in rs])
            r2, p2 = SS.spearman_perm(x, [abs(r[mk]) for r in rs])
            print(f"  {m:22s}{len(rs):>5d}{r1:>+14.3f}{p1:>8.3f}{r2:>+15.3f}{p2:>8.3f}")
            res["correlations"].setdefault(pname, {})[m] = {
                "n": len(rs), "rho_trade": r1, "p_trade": p1,
                "rho_abs_move": r2, "p_abs_move": p2}

    # ------------------------------------------------------------------ buckets
    print("\n\nBY SPIKE TERCILE -- the same thing without assuming it is monotonic.\n")
    print(f"  {'bucket':22s}{'n':>5s}{'hits':>7s}{'rate':>7s}{'mean trade':>13s}"
          f"{'t':>7s}{'median |move|':>15s}")
    for pname, pool in pools:
        rs = sorted([r for r in pool if r.get("spike_day") is not None],
                    key=lambda r: r["spike_day"])
        if len(rs) < 9:
            continue
        print(f"\n  -- {pname}")
        k = len(rs) // 3
        for name, g in (("low spike", rs[:k]), ("mid", rs[k:2 * k]), ("high spike", rs[2 * k:])):
            if not g:
                continue
            s = SS.summarise([r[ek] for r in g])
            am = st.median([abs(r[mk]) for r in g])
            print(f"  {name:22s}{s['n']:>5d}{s['hits']:>7d}{s['hit_rate']*100:>6.0f}%"
                  f"{s['mean']:>+12.2f}%{s['t']:>7.2f}{am:>14.2f}%")
            res["buckets"].setdefault(pname, {})[name] = {**s, "median_abs_move": am,
                                                          "spike_range": [g[0]["spike_day"],
                                                                          g[-1]["spike_day"]]}

    # -------------------------------------------------- what the silence selects
    if silent and scored:
        ms = st.median([r["dollar_vol"] for r in scored])
        sl = st.median([r["dollar_vol"] for r in silent])
        print(f"\n\nWHAT THE REPORTING THRESHOLD SELECTS. Median dollar volume: "
              f"${ms/1e6:.1f}m for the {len(scored)} measured names against "
              f"${sl/1e6:.1f}m for the {len(silent)} silent ones.")
        print("Any correlation found above is therefore measured on the larger half of")
        print("the book, and says nothing about the half this stage most often trades.")
        res["threshold_selection"] = {"median_dv_measured": ms, "median_dv_silent": sl}

    Path(REPO / a.out).write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()

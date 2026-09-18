#!/usr/bin/env python3
"""Intraday bars for the edge sample, fetched once and frozen to a cache.

WHY THIS EXISTS SEPARATELY FROM backtest/scripts/trade_prices.py
----------------------------------------------------------------
`trade_prices.py` answers one question -- the 14:00 ET entry and the two exits --
and writes a frozen snapshot of that answer. The three research questions added on
2026-09-18 need the whole session at fifteen-minute resolution, on both the entry
day and the days before it, so they need the bars themselves rather than a summary
of them.

WHAT THE WINDOW COSTS
---------------------
Yahoo serves 15-minute bars for the last 60 calendar days and no further. That
window SLIDES: an event that is inside it today falls out of it in a month, and the
numbers computed here become unreproducible from the source. The cache is therefore
the record. Delete it and the older half of the sample cannot be rebuilt -- it is
checked in for that reason, not as a convenience.

Bars are regular-session only. Yahoo does not return pre/post bars at this interval
without `includePrePost`, and this module does not ask for them, so every price here
is one that existed inside 09:30-16:00 ET with real volume behind it. That matters
for the entry-clock question: an extended-hours price from this source would carry
no size, and `edge/EDGE_ANALYSIS.md` already has one finding resting on that trap.
"""
import gzip
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / "edge" / "analysis" / "bars-cache.json.gz"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
CHART = ("https://query1.finance.yahoo.com/v8/finance/chart/"
         "{t}?interval={iv}&range={rg}")

_mem = None


def _cache():
    global _mem
    if _mem is None:
        if CACHE.exists():
            with gzip.open(CACHE, "rt") as fh:
                _mem = json.load(fh)
        else:
            _mem = {}
    return _mem


def _save():
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    # gzipped: the raw JSON runs to ~11MB and it is checked in as an archival
    # record, not a convenience -- the 60-day bar window slides, so these prices
    # cannot be re-fetched once they age out. mtime=0 keeps the bytes stable
    # across writes that change nothing, so git does not see a diff every run.
    with gzip.GzipFile(CACHE, "wb", mtime=0) as fh:
        fh.write((json.dumps(_mem, separators=(",", ":"), sort_keys=True) + "\n").encode())


def _fetch(ticker, interval, rng, tries=3):
    url = CHART.format(t=urllib.parse.quote(ticker), iv=interval, rg=rng)
    last = None
    for i in range(tries):
        try:
            raw = urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=45).read()
            d = json.loads(raw)
            r = d["chart"]["result"][0]
            q = r["indicators"]["quote"][0]
            out = []
            for j, ts in enumerate(r["timestamp"]):
                if q["close"][j] is None:
                    continue
                et = datetime.fromtimestamp(ts, timezone.utc).astimezone(ET)
                out.append([et.date().isoformat(), et.hour * 60 + et.minute,
                            q["open"][j], q["close"][j], q.get("volume", [None] * 99)[j]])
            return out, None
        except Exception as e:                       # noqa: BLE001 - reported, not raised
            last = f"{type(e).__name__}: {str(e)[:90]}"
            time.sleep(2 * (i + 1))
    return None, last


def yahoo_symbol(ticker):
    """A dotted share class is a dash on Yahoo: LEN.B -> LEN-B.

    Without this the second class of a dual-class issuer returns
    `KeyError: 'timestamp'` and silently leaves the sample -- which happens to be
    harmless today, because `edge_score.py` folds a second class into its issuer
    anyway, but it would not stay harmless if the fold ever missed one.
    """
    return ticker.replace(".", "-")


def bars(ticker, interval="15m", rng="60d"):
    """[[date, minute_of_day_ET, open, close, volume], ...] or None, with a reason."""
    c = _cache()
    key = f"{ticker}|{interval}|{rng}"
    if key in c:
        v = c[key]
        return (v["bars"], None) if v.get("bars") else (None, v.get("err"))
    rows, err = _fetch(yahoo_symbol(ticker), interval, rng)
    c[key] = {"bars": rows, "err": err,
              "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    _save()
    return rows, err


def by_day(rows):
    d = {}
    for r in rows:
        d.setdefault(r[0], []).append(r)
    for k in d:
        d[k].sort(key=lambda r: r[1])
    return d


def price_at(day_bars, hh, mm=0):
    """Close of the bar covering hh:mm ET, else the last bar at or before it.

    Returns (price, how). `how` is kept because a 14:00 price that is really a
    13:45 price is a different measurement, and the entry-clock question is
    entirely about which minute you traded.
    """
    want = hh * 60 + mm
    exact = [b for b in day_bars if b[1] == want]
    if exact:
        return exact[0][3], "exact"
    before = [b for b in day_bars if b[1] <= want]
    if not before:
        return None, "no bar at or before"
    b = before[-1]
    return b[3], f"nearest {b[1] // 60:02d}:{b[1] % 60:02d}"


def day_close(day_bars):
    return day_bars[-1][3] if day_bars else None


def day_open(day_bars):
    return day_bars[0][2] if day_bars else None


if __name__ == "__main__":
    import sys
    for t in sys.argv[1:] or ["ORCL"]:
        rows, err = bars(t)
        if err:
            print(f"{t:8s} FAIL {err}")
            continue
        d = by_day(rows)
        ks = sorted(d)
        print(f"{t:8s} {len(rows):5d} bars  {len(ks)} sessions  {ks[0]} .. {ks[-1]}")

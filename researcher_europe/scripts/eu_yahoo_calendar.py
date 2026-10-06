#!/usr/bin/env python3
"""Yahoo's per-symbol next earnings date, as a second calendar for all ten markets.

WHY. The vendor calendar (TradingView, `earnings_release_next_date`) was measured on
2026-10-06 to skip a quarterly statement and jump to the next full report for many
issuers: on Germany, of 237 ISINs with an EQS reporting event, 31 carried a
different TradingView date -- nearly all pointing at Feb-Apr 2027 while the company
reports Q3 in October or November (Beiersdorf, MTU, DWS, Heidelberg Materials,
Fielmann). The same shape shows in France (BNP), Italy, Spain, Norway (Orkla, Aker)
and Finland's Q1/Q3 business reviews. Yahoo's quote endpoint carries its own
`earningsTimestamp` per symbol, and on the 2026-10-06 probe it dated liquid names in
the next eight weeks that TradingView did not: DE +18, IT +20, FR +14, ES +6, SE +6,
FI +4, NO +3, DK +2, PL +1.

WHAT IT IS NOT. Yahoo's dates can be stale (LVMH still read July on 2026-10-06), its
time of day is a placeholder so it never gives a session, and it flags some dates as
its own ESTIMATE (`isEarningsDateEstimate`). An estimated date is a cadence prior --
the TRT failure -- so `eu_universe.py` only adds a row on a date Yahoo does NOT mark as
an estimate, and keeps the flag on every row so the resolver can split by it.

One batched request per 150 symbols, about 20 seconds for all ten markets.
"""
import json
import subprocess
import time
from datetime import datetime, timezone

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"
JAR = "/tmp/eu-yahoo-cal.txt"
UTC = timezone.utc
_crumb = {"v": None}


def _sh(args, timeout=45):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout


def crumb():
    if _crumb["v"] is None:
        _sh(["curl", "-sS", "--max-time", "20", "-c", JAR, "-H", f"User-Agent: {UA}",
             "-o", "/dev/null", "https://fc.yahoo.com"])
        _crumb["v"] = _sh(["curl", "-sS", "--max-time", "20", "-b", JAR, "-H",
                           f"User-Agent: {UA}",
                           "https://query1.finance.yahoo.com/v1/test/getcrumb"]).strip()
    return _crumb["v"]


def dates(symbols, batch=150):
    """{yahoo_symbol: {"date", "is_estimate", "start", "end"}} for every symbol Yahoo
    dates. A symbol Yahoo returns without a timestamp is absent. Raises only if EVERY
    batch failed, so a caller can tell 'Yahoo is down' from 'Yahoo dates nobody'."""
    c = crumb()
    out, ok = {}, 0
    syms = sorted(set(s for s in symbols if s))
    for i in range(0, len(syms), batch):
        url = ("https://query2.finance.yahoo.com/v7/finance/quote?symbols="
               + ",".join(syms[i:i + batch])
               + "&fields=earningsTimestamp,earningsTimestampStart,earningsTimestampEnd,"
                 "isEarningsDateEstimate&crumb=" + c)
        for attempt in range(3):
            try:
                res = json.loads(_sh(["curl", "-sS", "--max-time", "40", "-b", JAR, "-H",
                                      f"User-Agent: {UA}", url]))["quoteResponse"]["result"]
                ok += 1
                break
            except Exception:
                time.sleep(2 * (attempt + 1))
        else:
            continue
        for q in res:
            ts = q.get("earningsTimestamp")
            if not ts:
                continue
            d = lambda t: (datetime.fromtimestamp(t, UTC).date().isoformat()  # noqa: E731
                           if t else None)
            out[q["symbol"]] = {"date": d(ts),
                                "is_estimate": bool(q.get("isEarningsDateEstimate")),
                                "start": d(q.get("earningsTimestampStart")),
                                "end": d(q.get("earningsTimestampEnd"))}
        time.sleep(0.3)
    if syms and not ok:
        raise RuntimeError("Yahoo quote endpoint failed on every batch")
    return out

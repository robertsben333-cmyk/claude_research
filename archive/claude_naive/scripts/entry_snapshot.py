#!/usr/bin/env python3
"""Freeze the spot price at forecast time, so the trade can be reconstructed later.

The backtest's scheme buys at 14:00 ET (20:00 CET) on the last session before the
print. This skill fires at 19:30 CET, thirty minutes before that, so the price it
records is close to but not identical with the entry. Both are stored: the spot at
forecast time, and later the actual 14:00 ET bar from `score_naive.py`.

Recording it now matters because intraday history is short-lived -- 15-minute bars
reach back about a month and the window slides daily. A forecast whose entry price
was never captured cannot be scored honestly a month later.
"""
import argparse, json, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0"}
Q = "https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1d&interval=1m"


def spot(ticker):
    try:
        d = json.loads(urllib.request.urlopen(
            urllib.request.Request(Q.format(t=ticker), headers=UA), timeout=25).read())
        r = d["chart"]["result"][0]
        meta = r.get("meta", {})
        closes = [c for c in r["indicators"]["quote"][0]["close"] if c is not None]
        return {
            "spot": round(closes[-1], 4) if closes else meta.get("regularMarketPrice"),
            "market_price": meta.get("regularMarketPrice"),
            "previous_close": meta.get("chartPreviousClose"),
            "currency": meta.get("currency"),
            "as_of_utc": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {str(e)[:90]}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    a = ap.parse_args()
    d = ROOT / a.date
    fp = d / "forecasts.json"
    if not fp.exists():
        sys.exit(f"no forecasts at {fp} -- run the forecast first")
    rows = json.loads(fp.read_text(encoding="utf-8"))
    out = {}
    for r in rows:
        out[r["ticker"]] = spot(r["ticker"]) | {
            "session": r.get("session"), "event_date": r.get("event_date")}
    p = d / "entry-prices.json"
    p.write_text(json.dumps({
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "note": ("spot at forecast time (~19:30 CET). The backtest scheme enters at "
                 "14:00 ET / 20:00 CET, so score_naive.py re-reads the exact entry bar "
                 "and uses that; this is the fallback if the intraday window has slid."),
        "prices": out}, indent=1), encoding="utf-8")
    ok = sum(1 for v in out.values() if not v.get("error"))
    print(f"captured {ok}/{len(out)} spots -> {p}")
    for t, v in out.items():
        if v.get("error"):
            print(f"  FAILED {t}: {v['error']}")


if __name__ == "__main__":
    main()

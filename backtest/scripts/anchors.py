#!/usr/bin/env python3
"""Phase-0 anchors, computed by the harness from data strictly before the cutoff.

Both arms of the experiment get an identical anchor block, so what the test
measures is the research, not who managed to find a price. Everything here is
derived from daily bars and from EDGAR filing dates -- nothing is scraped, and
nothing after the cutoff is read.

The cutoff is the moment of the print: close of the event date for amc, open of
the event date for bmo. The last usable bar is the one the market last closed
on before that moment.
"""
import argparse, json, sys, statistics
from datetime import date, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import submissions, ticker_cik_map
from truth import bars, move


def prior_event_dates(cik, before, n=8):
    """Past earnings 8-Ks (item 2.02), newest first, all strictly before cutoff."""
    r = submissions(cik)["filings"]["recent"]
    out = []
    for i, form in enumerate(r["form"]):
        if form != "8-K" or "2.02" not in (r["items"][i] or ""):
            continue
        from datetime import datetime
        from zoneinfo import ZoneInfo
        dt = datetime.fromisoformat(r["acceptanceDateTime"][i].replace("Z", "+00:00")) \
            .astimezone(ZoneInfo("America/New_York"))
        if dt.date().isoformat() >= before:
            continue
        hhmm = dt.hour * 60 + dt.minute
        sess = "amc" if hhmm >= 960 else ("bmo" if hhmm <= 570 else "intraday")
        out.append({"event_date": dt.date().isoformat(), "session": sess})
    return out[:n]


def build(ticker, cik, event_date, session):
    ed = date.fromisoformat(event_date)
    last_bar_date = ed.isoformat() if session == "amc" else None
    rows, _ = bars(ticker, ed - timedelta(days=420), ed + timedelta(days=1))
    pre = [r for r in rows if r["date"] < event_date] + \
          ([r for r in rows if r["date"] == event_date] if session == "amc" else [])
    if len(pre) < 60:
        return {"ticker": ticker, "error": f"only {len(pre)} pre-cutoff bars"}
    closes = [r["close"] for r in pre]
    vols = [r["volume"] or 0 for r in pre]
    spot = closes[-1]
    rets = [closes[i] / closes[i - 1] - 1 for i in range(1, len(closes))]
    r20 = rets[-20:]
    hist = []
    for e in prior_event_dates(cik, event_date):
        m = move(ticker, e["event_date"], e["session"])
        if "actual_move_pct" in m:
            hist.append({"event_date": e["event_date"], "session": e["session"],
                         "move_pct": m["actual_move_pct"]})
    absmoves = [abs(h["move_pct"]) for h in hist]
    yr = closes[-252:] if len(closes) >= 252 else closes
    return {
        "ticker": ticker, "event_date": event_date, "session": session,
        "cutoff_note": ("close of the event date" if session == "amc"
                        else "open of the event date; last close is the prior session"),
        "last_pre_event_bar": pre[-1]["date"],
        "spot": round(spot, 4),
        "pct_from_52w_high": round((spot / max(yr) - 1) * 100, 2),
        "pct_from_52w_low": round((spot / min(yr) - 1) * 100, 2),
        "realised_vol_20d_annualised_pct": round(statistics.pstdev(r20) * (252 ** .5) * 100, 1),
        "avg_volume_20d": int(sum(vols[-20:]) / 20),
        "run_up_5d_pct": round((closes[-1] / closes[-6] - 1) * 100, 2),
        "run_up_20d_pct": round((closes[-1] / closes[-21] - 1) * 100, 2),
        "historical_earnings_moves": hist,
        "median_abs_historical_move_pct": round(statistics.median(absmoves), 2) if absmoves else None,
        "expected_move_proxy_pct": round(statistics.median(absmoves), 2) if absmoves else None,
        "expected_move_proxy_note": (
            "median |close-to-close move| over the last %d earnings events. This is a "
            "PROXY: the option-implied move at the time of the print is not recoverable "
            "retrospectively and is marked unavailable." % len(absmoves)),
        "event_implied_move_pct": None,
        "event_implied_move_status": "unavailable - no retrospective option chain",
        "sources": ["yahoo chart v8 daily bars", "sec edgar submissions api"],
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True); ap.add_argument("--date", required=True)
    ap.add_argument("--session", required=True); ap.add_argument("--cik")
    a = ap.parse_args()
    cik = a.cik or ticker_cik_map().get(a.ticker.upper())
    print(json.dumps(build(a.ticker.upper(), cik, a.date, a.session), indent=1))

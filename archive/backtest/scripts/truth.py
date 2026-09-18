#!/usr/bin/env python3
"""Deterministic post-earnings move, from daily bars.

Convention (identical to LEDGER.md): close before the print -> close after the
first full session following it.

  amc on D : close(D)   -> close(next trading day)
  bmo on D : close(D-1) -> close(D)

Source: Yahoo chart API (no key). Raw and split/dividend-adjusted closes are
both reported; a mismatch above 0.5pp means a corporate action inside the
window and the event should be dropped from the sample.
"""
import argparse, json, sys, time, urllib.request
from datetime import date, datetime, timedelta, timezone

CHART = ("https://query1.finance.yahoo.com/v8/finance/chart/{t}"
         "?period1={p1}&period2={p2}&interval=1d&events=split")
UA = {"User-Agent": "Mozilla/5.0"}


def bars(ticker, start, end):
    p1 = int(datetime.combine(start, datetime.min.time(), timezone.utc).timestamp())
    p2 = int(datetime.combine(end, datetime.min.time(), timezone.utc).timestamp())
    req = urllib.request.Request(CHART.format(t=ticker, p1=p1, p2=p2), headers=UA)
    d = json.load(urllib.request.urlopen(req, timeout=30))
    res = d["chart"]["result"][0]
    ts = res["timestamp"]
    q = res["indicators"]["quote"][0]
    adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
    out = []
    for i, t in enumerate(ts):
        if q["close"][i] is None:
            continue
        out.append({
            "date": datetime.fromtimestamp(t, timezone.utc).date().isoformat(),
            "open": q["open"][i], "close": q["close"][i], "adjclose": adj[i],
            "volume": q["volume"][i],
        })
    splits = res.get("events", {}).get("splits", {})
    return out, splits


def move(ticker, event_date, session, pad=12):
    ed = date.fromisoformat(event_date)
    rows, splits = bars(ticker, ed - timedelta(days=pad), ed + timedelta(days=pad))
    idx = {r["date"]: i for i, r in enumerate(rows)}
    if event_date not in idx:
        return {"ticker": ticker, "error": f"no bar on event date {event_date}"}
    i = idx[event_date]
    if session == "amc":
        a, b = i, i + 1
    elif session == "bmo":
        a, b = i - 1, i
    else:
        return {"ticker": ticker, "error": f"bad session {session!r}"}
    if a < 0 or b >= len(rows):
        return {"ticker": ticker, "error": "window falls outside available bars"}
    before, after = rows[a], rows[b]
    raw = (after["close"] / before["close"] - 1) * 100
    adjm = (after["adjclose"] / before["adjclose"] - 1) * 100
    return {
        "ticker": ticker, "event_date": event_date, "session": session,
        "before_date": before["date"], "before_close": round(before["close"], 4),
        "after_date": after["date"], "after_close": round(after["close"], 4),
        "actual_move_pct": round(raw, 2),
        "actual_move_pct_adj": round(adjm, 2),
        "corporate_action_in_window": abs(raw - adjm) > 0.5 or bool(splits),
        "measurement": "close before print to close after first full session",
        "source": "yahoo chart v8 daily bars",
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", help="JSON list of {ticker,event_date,session}")
    ap.add_argument("--ticker"); ap.add_argument("--date"); ap.add_argument("--session")
    a = ap.parse_args()
    ev = json.load(open(a.events, encoding="utf-8")) if a.events else \
        [{"ticker": a.ticker, "event_date": a.date, "session": a.session}]
    out = []
    for e in ev:
        out.append(move(e["ticker"], e["event_date"], e["session"]))
        time.sleep(0.3)
    print(json.dumps(out, indent=1))

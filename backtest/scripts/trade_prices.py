#!/usr/bin/env python3
"""Entry and exit prices for the trading scheme, frozen to disk.

Scheme: buy at 20:00 CET on the last market session before the print -- the event
date itself for amc, the prior trading day for bmo -- and exit either at the next
open or the next close.

20:00 CET/CEST is 14:00 ET, which is intraday and two hours before the close, so
close-to-close bars cannot express it. 15-minute bars give the exact bar; they
reach back only ~1 month, and that window slides every day, so this snapshot is
written once and treated as frozen. 60-minute bars reach three months but are
stamped on the half hour, so 14:00 ET falls inside a bar rather than on one --
they are the fallback for the few events older than the 15m window, and are
recorded as such rather than silently mixed in.
"""
import json, sys, time, urllib.request
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT

UA = {"User-Agent": "Mozilla/5.0"}
ET = ZoneInfo("America/New_York")
CH = "https://query1.finance.yahoo.com/v8/finance/chart/{t}?interval={iv}&range={rg}"


def bars(ticker, interval, rng):
    d = json.loads(urllib.request.urlopen(
        urllib.request.Request(CH.format(t=ticker, iv=interval, rg=rng), headers=UA),
        timeout=40).read())
    r = d["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    out = []
    for i, t in enumerate(r["timestamp"]):
        if q["close"][i] is None:
            continue
        out.append({"et": datetime.fromtimestamp(t, timezone.utc).astimezone(ET),
                    "open": q["open"][i], "close": q["close"][i]})
    return out


def session_days(rows):
    days = {}
    for b in rows:
        days.setdefault(b["et"].date().isoformat(), []).append(b)
    return days


def price_at_1400(day_bars):
    """The 14:00 ET bar's close. Falls back to the last bar at or before 14:00."""
    exact = [b for b in day_bars if b["et"].hour == 14 and b["et"].minute == 0]
    if exact:
        return exact[0]["close"], "exact 14:00 ET bar"
    before = [b for b in day_bars if (b["et"].hour, b["et"].minute) <= (14, 0)]
    if not before:
        return None, "no bar at or before 14:00 ET"
    b = before[-1]
    return b["close"], f"nearest bar at or before 14:00 ET ({b['et']:%H:%M})"


def compute(ticker, event_date, session, interval="15m", rng="1mo"):
    try:
        days = session_days(bars(ticker, interval, rng))
    except Exception as e:
        return {"ticker": ticker, "error": f"{type(e).__name__}: {str(e)[:80]}"}
    ds = sorted(days)
    if event_date not in ds:
        return {"ticker": ticker, "error": f"no intraday bars on {event_date} "
                                           f"(have {ds[0]}..{ds[-1]})", "interval": interval}
    i = ds.index(event_date)
    # entry day: the event date for amc, the previous session for bmo
    if session == "amc":
        entry_day, exit_day = ds[i], ds[i + 1] if i + 1 < len(ds) else None
    else:
        entry_day, exit_day = (ds[i - 1] if i > 0 else None), ds[i]
    if entry_day is None or exit_day is None:
        return {"ticker": ticker, "error": "entry or exit session outside the bar window",
                "interval": interval}
    entry, how = price_at_1400(days[entry_day])
    if entry is None:
        return {"ticker": ticker, "error": how, "interval": interval}
    ex = days[exit_day]
    ex_open = ex[0]["open"]
    ex_close = ex[-1]["close"]
    # the pre-print drift you eat by entering at 14:00 rather than on the close
    entry_day_close = days[entry_day][-1]["close"]
    return {
        "ticker": ticker, "event_date": event_date, "session": session,
        "interval": interval, "entry_basis": how,
        "entry_day": entry_day, "entry_1400et": round(entry, 4),
        "entry_day_close": round(entry_day_close, 4),
        "exit_day": exit_day, "exit_open": round(ex_open, 4), "exit_close": round(ex_close, 4),
        "ret_to_open_pct": round((ex_open / entry - 1) * 100, 3),
        "ret_to_close_pct": round((ex_close / entry - 1) * 100, 3),
        "pre_print_drift_pct": round((entry_day_close / entry - 1) * 100, 3),
    }


if __name__ == "__main__":
    draw = json.loads((ROOT / "runs" / "pilot-40" / "draw.json").read_text(encoding="utf-8"))
    out, fell_back = [], 0
    for e in draw["events"]:
        r = compute(e["ticker"], e["event_date"], e["session"])
        if r.get("error"):                      # older than the 15m window
            r2 = compute(e["ticker"], e["event_date"], e["session"], "60m", "3mo")
            if not r2.get("error"):
                fell_back += 1
                r2["fallback_reason"] = r["error"]
            r = r2
        out.append(r)
        time.sleep(0.4)
    ok = [r for r in out if not r.get("error")]
    p = ROOT / "runs" / "pilot-40" / "trade_prices.json"
    p.write_text(json.dumps({
        "scheme": "buy 14:00 ET (20:00 CET) last session before the print; "
                  "exit next open or next close",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "note": "frozen deliberately: the 15m bar window slides daily",
        "n_ok": len(ok), "n_failed": len(out) - len(ok),
        "n_hourly_fallback": fell_back, "prices": out}, indent=1), encoding="utf-8")
    print(f"{len(ok)}/{len(out)} priced ({fell_back} on hourly fallback) -> {p}")
    for r in out:
        if r.get("error"):
            print(f"  FAILED {r['ticker']}: {r['error']}")

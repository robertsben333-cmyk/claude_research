#!/usr/bin/env python3
"""Enumerate historical earnings events with an EXACT session, from EDGAR.

Nasdaq's calendar gives us who reported (and, for past dates, also the reported
EPS and surprise -- which is why it is never handed to a research agent). EDGAR
gives us the thing Nasdaq drops for past dates: the exact moment the earnings
8-K (item 2.02) was accepted, in ET, which settles bmo/amc without guessing and
without looking at price action.

  accepted >= 16:00 ET  -> amc on that date
  accepted <= 09:30 ET  -> bmo on that date
  in between            -> 'intraday', excluded from the sample

Post-event fields from the calendar (eps, surprise) are dropped here and never
written to disk. epsForecast / noOfEsts are pre-event consensus and are kept,
but live in the harness-side event record, not in the sealed corpus.
"""
import argparse, json, sys, time
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import fetch, ticker_cik_map, submissions, ROOT

ET = ZoneInfo("America/New_York")
DROP_FIELDS = {"eps", "surprise", "lastYearEPS", "lastYearRptDt"}  # post-event


def calendar_rows(day):
    try:
        d = json.loads(fetch(f"https://api.nasdaq.com/api/calendar/earnings?date={day}", timeout=25))
        return (d.get("data") or {}).get("rows") or []
    except Exception:
        return []


def parse_cap(s):
    try:
        return float(str(s).replace("$", "").replace(",", ""))
    except Exception:
        return 0.0


def session_from_edgar(cik, day):
    """Exact session for the FIRST results disclosure on/around `day`.

    Two rules learned the hard way:

    * Take the EARLIEST disclosure, not the latest. FCN filed its 10-Q at 07:30 ET
      on 2026-07-30 and a second 8-K carrying item 2.02 at 16:31 ET on 07-31.
      Choosing the latest labelled it amc 07-31, so the "forecast window" began two
      sessions after the news had already been traded. VG had the same shape,
      12.5h out. 2 of 40 events were mis-dated this way.
    * A 10-Q counts as a results disclosure. Some companies put the numbers in the
      10-Q first and the 8-K second, so an 8-K-only rule silently misses the event.
    """
    try:
        sub = submissions(cik)
    except Exception:
        return None
    r = sub["filings"]["recent"]
    best = None
    for i, form in enumerate(r["form"]):
        is_results = (form == "8-K" and "2.02" in (r["items"][i] or "")) or form in ("10-Q", "10-K")
        if not is_results:
            continue
        acc = r["acceptanceDateTime"][i]
        dt = datetime.fromisoformat(acc.replace("Z", "+00:00")).astimezone(ET)
        # the release can be accepted the evening of `day` or the morning after
        if abs((dt.date() - date.fromisoformat(day)).days) > 1:
            continue
        cand = {"accepted_et": dt.isoformat(), "filing_date": r["filingDate"][i],
                "accession": r["accessionNumber"][i], "disclosure_form": form}
        hhmm = dt.hour * 60 + dt.minute
        if hhmm >= 16 * 60:
            cand |= {"session": "amc", "event_date": dt.date().isoformat()}
        elif hhmm <= 9 * 60 + 30:
            cand |= {"session": "bmo", "event_date": dt.date().isoformat()}
        else:
            cand |= {"session": "intraday", "event_date": dt.date().isoformat()}
        # EARLIEST wins -- see the docstring
        if best is None or cand["accepted_et"] < best["accepted_et"]:
            best = cand
    return best


def build(start, end, min_cap, limit_per_day=None, sample_per_day=None, seed=0):
    """limit_per_day takes the largest names by market cap; sample_per_day draws
    at random with `seed`.

    Prefer sampling. Taking the top N by capitalisation produced a draw that was
    24 large-cap, 14 mid and 2 small out of 40 -- a universe of mega-caps, which
    is not the population this pipeline researches. Stage 1 shortlists on change
    expectation, which skews smaller and more volatile, and small retail-heavy
    names are exactly where the informal layer is expected to carry signal."""
    import random as _random
    rng = _random.Random(seed)
    cikmap = ticker_cik_map()
    out, d = [], date.fromisoformat(start)
    endd = date.fromisoformat(end)
    while d <= endd:
        if d.weekday() < 5:
            rows = calendar_rows(d.isoformat())
            rows = [r for r in rows if parse_cap(r.get("marketCap")) >= min_cap]
            if sample_per_day and len(rows) > sample_per_day:
                rows.sort(key=lambda r: (r.get("symbol") or ""))
                rows = rng.sample(rows, sample_per_day)
            else:
                rows.sort(key=lambda r: -parse_cap(r.get("marketCap")))
                if limit_per_day:
                    rows = rows[:limit_per_day]
            for r in rows:
                t = (r.get("symbol") or "").strip().upper()
                cik = cikmap.get(t)
                rec = {
                    "ticker": t, "company": r.get("name"),
                    "calendar_date": d.isoformat(),
                    "market_cap_usd_today": parse_cap(r.get("marketCap")),
                    "consensus_eps_forecast": r.get("epsForecast"),
                    "n_estimates": r.get("noOfEsts"),
                    "fiscal_quarter_ending": r.get("fiscalQuarterEnding"),
                    "cik": cik,
                }
                ev = session_from_edgar(cik, d.isoformat()) if cik else None
                if ev:
                    rec |= ev
                    rec["session_source"] = "edgar 8-K item 2.02 acceptance time (ET)"
                else:
                    rec |= {"session": None, "event_date": None,
                            "session_source": "unresolved - no 8-K item 2.02 near this date"}
                out.append(rec)
            time.sleep(0.2)
        d += timedelta(days=1)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True); ap.add_argument("--end", required=True)
    ap.add_argument("--min-cap", type=float, default=2e9)
    ap.add_argument("--limit-per-day", type=int, default=None,
                    help="take the N largest by market cap (biases to mega-caps)")
    ap.add_argument("--sample-per-day", type=int, default=None,
                    help="draw N at random per day -- preferred")
    ap.add_argument("--seed", type=int, default=20260828)
    ap.add_argument("--out", default=str(ROOT / "events.json"))
    a = ap.parse_args()
    ev = build(a.start, a.end, a.min_cap, a.limit_per_day, a.sample_per_day, a.seed)
    Path(a.out).write_text(json.dumps(ev, indent=1), encoding="utf-8")
    ok = [e for e in ev if e["session"] in ("amc", "bmo")]
    print(f"candidates: {len(ev)}   session resolved: {len(ok)}   "
          f"unresolved: {len(ev)-len(ok)}   -> {a.out}")

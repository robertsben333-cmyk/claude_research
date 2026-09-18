#!/usr/bin/env python3
"""Resolve each capture's session, and confirm the print happened at all.

`capture.py` writes `session: null` and defers this to "seal.py, from EDGAR".
That file was never written, so all 387 captures carry a null session and
`truth.py` -- which needs `amc` or `bmo` to know which two closes to difference
-- cannot score any of them.

The seal is the 8-K carrying item 2.02. Its acceptance time is authoritative
(FINDINGS.md section 3) and the same rule `priced_in.prior_prints` uses applies
here:

    accepted >= 16:00 ET  ->  amc
    accepted <= 09:30 ET  ->  bmo
    in between            ->  intraday, which this repo does not score

Resolving the seal settles a second question for free. A capture row came from
an earnings calendar, and calendars project cadence forward: on 2026-08-31 eight
of twelve rows had no earnings event at all. An item 2.02 accepted within a few
days of the calendar date is the company itself confirming the print. No such
filing, and the row is a projection until something else confirms it.

This is harness-side, exactly like `truth.py`. The session is not outcome
information -- the live pipeline knows it from the calendar before the print --
but nothing here goes into a research agent's context either way.

    python3 backtest/scripts/seal.py                  # all past captures
    python3 backtest/scripts/seal.py --all            # future ones too
    python3 backtest/scripts/seal.py --ticker CASY --date 2026-09-08
    python3 backtest/scripts/seal.py --refresh        # re-resolve, ignore cache
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "edge" / "scripts"))
from priced_in import RESULT_WORDS, cik_for, fetch_text, get_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / "captures" / "events"
NY = ZoneInfo("America/New_York")

# How far from the calendar date an item 2.02 may land and still be this event.
# Calendars are routinely a day out either side; a week apart is a different
# quarter's print, not a mislabelled one.
WINDOW_DAYS = 4


def session_of(accepted_utc):
    dt = datetime.fromisoformat(accepted_utc.replace("Z", "+00:00")).astimezone(NY)
    hhmm = dt.hour * 60 + dt.minute
    return ("amc" if hhmm >= 960 else "bmo" if hhmm <= 570 else "intraday"), dt


def item_202_rows(rows):
    out = []
    for r in rows:
        if r.get("form") != "8-K":
            continue
        if "2.02" not in (r.get("items") or ""):
            continue
        if not r.get("accepted_utc"):
            continue
        out.append(r)
    return out


def from_capture(evdir):
    """The capture's own filings.json. Free, and already sealed by construction."""
    f = evdir / "filings.json"
    if not f.exists():
        return []
    try:
        return item_202_rows(json.loads(f.read_text(encoding="utf-8")).get("filings") or [])
    except Exception:
        return []


def edgar_recent(ticker):
    """EDGAR itself, for the captures whose filings.json window missed the print.

    The capture indexes a fixed lookback from when it ran, and it stops at the
    seal, so the event's own 8-K is never in the captured file. It is always on
    EDGAR.
    """
    cik = cik_for(ticker)
    if not cik:
        return None, None
    j = get_json(f"https://data.sec.gov/submissions/CIK{cik}.json", sec=True)
    return cik, j["filings"]["recent"]


def from_edgar(recent):
    rows = [{"form": recent["form"][i], "items": recent["items"][i],
             "accepted_utc": recent["acceptanceDateTime"][i],
             "accession": recent["accessionNumber"][i]}
            for i in range(len(recent["form"]))]
    return item_202_rows(rows)


def from_sixk(cik, recent, event_date):
    """A foreign private issuer files a 6-K, which carries no item codes.

    Seventy-three of the 132 captures the item-2.02 path could not seal are
    foreign filers, so this is most of the shortfall rather than an edge case.
    `priced_in.sixk_prints` already solved the reading problem -- the results
    language is in the exhibit text one layer below the index -- but it only
    looks *before* a cutoff, and the seal needs the filing *at* the event. Same
    reading, different window.

    Weaker than an item code and labelled as such: a 6-K carrying results
    language is very likely an earnings release, not certainly one.
    """
    ed = date.fromisoformat(event_date)
    c = str(int(cik))
    cands = []
    for i, form in enumerate(recent["form"]):
        if form != "6-K":
            continue
        sess, dt = session_of(recent["acceptanceDateTime"][i])
        gap = abs((dt.date() - ed).days)
        if gap <= WINDOW_DAYS:
            cands.append((gap, i, sess, dt))
    cands.sort()
    for gap, i, sess, dt in cands[:3]:
        acc = recent["accessionNumber"][i].replace("-", "")
        try:
            idx = get_json(
                f"https://www.sec.gov/Archives/edgar/data/{c}/{acc}/index.json", sec=True)
            names = [it["name"] for it in idx["directory"]["item"]
                     if it["name"].lower().endswith((".htm", ".html"))]
        except Exception:
            continue
        for name in names[:4]:
            try:
                body = fetch_text(
                    f"https://www.sec.gov/Archives/edgar/data/{c}/{acc}/{name}")[:6000].lower()
            except Exception:
                continue
            if any(w in body for w in RESULT_WORDS):
                return {"accepted_utc": recent["acceptanceDateTime"][i],
                        "accession": recent["accessionNumber"][i]}, sess, dt, gap
    return None, None, None, None


def pick(rows, event_date):
    """The item 2.02 nearest the calendar date, if one is inside the window."""
    ed = date.fromisoformat(event_date)
    best, best_gap = None, None
    for r in rows:
        sess, dt = session_of(r["accepted_utc"])
        gap = abs((dt.date() - ed).days)
        if gap > WINDOW_DAYS:
            continue
        if best_gap is None or gap < best_gap:
            best, best_gap = (r, sess, dt), gap
    return best, best_gap


def seal_one(evdir, refresh=False):
    ev = json.loads((evdir / "event.json").read_text(encoding="utf-8"))
    out = evdir / "seal.json"
    if out.exists() and not refresh:
        return json.loads(out.read_text(encoding="utf-8"))

    ticker, event_date = ev["ticker"], ev["event_date"]
    doc = {"ticker": ticker, "calendar_date": event_date,
           "sealed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}

    src = "capture filings.json"
    hit, gap = pick(from_capture(evdir), event_date)
    seal_basis = "8-K item 2.02 acceptance time"
    recent = cik = None
    if hit is None:
        try:
            cik, recent = edgar_recent(ticker)
        except Exception as e:
            doc.update(status="edgar_failed", reason=f"{type(e).__name__}",
                       session=None, event_confirmed=False)
            out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
            return doc
        if recent is None:
            doc.update(status="unresolved", session=None, event_confirmed=False,
                       basis="no CIK on EDGAR for this ticker")
            out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
            return doc
        src = "edgar submissions api"
        hit, gap = pick(from_edgar(recent), event_date)

    if hit is not None:
        r, sess, dt = hit
    else:
        # No item 2.02. Either a foreign private issuer, or nothing was filed.
        r = sess = dt = None
        if any(f in ("6-K", "20-F", "40-F") for f in recent["form"][:200]):
            try:
                r, sess, dt, gap = from_sixk(cik, recent, event_date)
            except Exception:
                r = None
            if r is not None:
                seal_basis = ("6-K exhibit text matched results language. Heuristic, "
                              "not an item code: weaker than the 8-K item 2.02 path")
        if r is None:
            forms = {f for f in recent["form"][:200]}
            foreign = bool(forms & {"6-K", "20-F", "40-F"})
            doc.update(
                status="unconfirmed_foreign" if foreign else "unconfirmed",
                session=None, event_confirmed=False,
                basis=(f"no 8-K item 2.02 within {WINDOW_DAYS} days of {event_date}"
                       + ("; 6-K exhibits opened and none carried results language"
                          if foreign else "") + f" ({src})"),
                last_filing_accepted=recent["acceptanceDateTime"][0][:10] if recent["form"] else None,
                note=("the company itself has not confirmed a print on this date, so the "
                      "calendar row stands unconfirmed. Excluded from the sample rather "
                      "than scored: this is the phantom-row failure the edge hunt hit on "
                      "2026-08-31, and the fix is subtraction."))
            out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
            return doc
    doc.update(status="ok" if sess != "intraday" else "intraday",
               session=None if sess == "intraday" else sess,
               raw_session=sess,
               event_confirmed=True,
               event_date=dt.date().isoformat(),
               calendar_gap_days=gap,
               accepted_utc=r["accepted_utc"],
               accepted_et=dt.isoformat(),
               accession=r.get("accession"),
               basis=f"{seal_basis} ({src})")
    if sess == "intraday":
        doc["note"] = ("accepted between 09:30 and 16:00 ET, so the close-to-close "
                       "convention does not describe this print; not scorable")
    if gap:
        doc["calendar_note"] = (f"the calendar said {event_date}; the filing says "
                               f"{dt.date().isoformat()} -- the filing wins")
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    return doc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ticker")
    ap.add_argument("--date")
    ap.add_argument("--all", action="store_true",
                    help="include captures whose event date has not passed")
    ap.add_argument("--refresh", action="store_true", help="ignore an existing seal.json")
    a = ap.parse_args()

    today = datetime.now(timezone.utc).date().isoformat()
    dirs = []
    for d in sorted(CAPTURES.iterdir()):
        if not (d / "event.json").exists():
            continue
        ev = json.loads((d / "event.json").read_text(encoding="utf-8"))
        if a.ticker and ev["ticker"] != a.ticker.upper():
            continue
        if a.date and ev["event_date"] != a.date:
            continue
        if not a.all and ev["event_date"] >= today:
            continue
        dirs.append(d)

    tally = {}
    amc = bmo = 0
    for d in dirs:
        doc = seal_one(d, refresh=a.refresh)
        tally[doc["status"]] = tally.get(doc["status"], 0) + 1
        if doc.get("session") == "amc":
            amc += 1
        elif doc.get("session") == "bmo":
            bmo += 1
        print(f"{doc['ticker']:6s} {doc['calendar_date']}  "
              f"{doc['status']:12s} {str(doc.get('session') or '-'):8s} "
              f"gap={doc.get('calendar_gap_days', '-')}")
    print(f"\n{len(dirs)} captures: {tally.get('ok', 0)} sealed "
          f"({amc} amc / {bmo} bmo)")
    for k in sorted(k for k in tally if k != "ok"):
        print(f"  {tally[k]:4d}  {k}")
    print(f"  scorable sample: {tally.get('ok', 0)}")


if __name__ == "__main__":
    main()

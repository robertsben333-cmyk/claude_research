#!/usr/bin/env python3
"""The Toronto market's rules, in one place: sessions, holidays, event shape.

WHAT IS DIFFERENT ABOUT CANADA, and therefore what this stage does differently from
stages E, J and EU. Each of these is measured in `researcher_canada/SOURCES.md`; this
file is where the measurement turns into a rule.

1. THE CALENDAR IS TWO VENDORS THAT DISAGREE. Wall Street Horizon (through TMX) and
   TradingView give a different next-release date for 172 of 277 names. WSH carries a
   CONFIRMED / UNCONFIRMED flag, which no other calendar in this repo has, so the
   reconciliation in `ca_universe.py` is: a CON date wins outright; an UNC date the
   vendor agrees with is good enough to hunt; an UNC date the vendor contradicts is
   DISPUTED and is not hunted unless the issuer's own "we will report on X" release
   confirms it. That check is precise and not sensitive -- it fired on 0 of 27 names
   that turned out not to report and only 11 of 61 that did -- so it can promote a
   disputed date and must never be used to drop one.

2. A THIRD OF THE UNIVERSE REPORTS BY FILING, NOT BY RELEASE. 38 of 39 vendor rows with
   no same-day press release had an interim-financials or 52-109 filing on SEDAR+ within
   three days. Those are real reporting events and they are NOT the event this method
   assumes: there is no release for the market to reprice against, and they are almost
   all junior mining below $1m a day. `event_shape()` classifies an issuer by its own
   history and `ca_universe.py` keeps `filing_only` names out of the draw with the
   reason recorded. Measured on 88 past events: it keeps 60 of 61 issuers that do
   publish results on the wire.

3. THE ANCHOR IS TWO REGIMES IN ONE MARKET. The Montreal Exchange lists options on 360
   underlyings, covering 96% of the names above $25m a day and 10% below $1m, while the
   short register covers 87-88% of every band. So an optionable name gets a real
   option-implied move and an ATM spread, exactly like a US name, and everything else
   gets a register-based lean, like a Japanese one. `anchor_covered` carries which, and
   `ca_resolve.py` ranks the two arms apart. This is the only market in the repo where
   the anchored and anchor-less regimes can be compared within one day's names.

4. THE REGISTER HAS NO HISTORY. One snapshot per symbol, no date argument. So the
   change in short interest cannot be read today and has to be accumulated: every run
   writes the day's register to `researcher_canada/analysis/short-register/<date>.json`
   and `short_change_pct_pts` resolves as soon as two runs exist. Until then that lean
   component is null rather than zero, and `BUSINESS_DATE` is carried into every
   baseline so the question of whether the feed refreshes daily is answered by the
   accumulating files rather than argued about.
"""
import re
from datetime import date, timedelta

MARKET = "CA"
TZ = "America/Toronto"
EXCHANGES = ("TSX", "TSXV", "CSE", "NEO")
CURRENCY = "CAD"
CLOSE_LOCAL = "16:00"
OPEN_LOCAL = "09:30"

# TSX statutory closures. Hardcoded rather than fetched: there is no free machine
# calendar for it, and a holiday read wrong is a day of baselines sealed on a stale
# spot. Verified against TMX's published 2026 and 2027 trading schedules. Dates that
# fall on a weekend are already observed on the Monday here.
TSX_HOLIDAYS = {
    "2026-01-01": "New Year's Day", "2026-02-16": "Family Day",
    "2026-04-03": "Good Friday", "2026-05-18": "Victoria Day",
    "2026-07-01": "Canada Day", "2026-08-03": "Civic Holiday",
    "2026-09-07": "Labour Day", "2026-09-30": "National Day for Truth and Reconciliation",
    "2026-10-12": "Thanksgiving", "2026-12-25": "Christmas Day",
    "2026-12-28": "Boxing Day (observed)",
    "2027-01-01": "New Year's Day", "2027-02-15": "Family Day",
    "2027-03-26": "Good Friday", "2027-05-24": "Victoria Day",
    "2027-07-01": "Canada Day", "2027-08-02": "Civic Holiday",
    "2027-09-06": "Labour Day", "2027-09-30": "National Day for Truth and Reconciliation",
    "2027-10-11": "Thanksgiving", "2027-12-27": "Christmas Day (observed)",
    "2027-12-28": "Boxing Day (observed)",
}


def market_closed(d):
    """Why Toronto is shut on `d`, or None. A weekend counts."""
    if isinstance(d, str):
        d = date.fromisoformat(d)
    if d.weekday() >= 5:
        return "weekend"
    return TSX_HOLIDAYS.get(d.isoformat())


def next_session(d):
    if isinstance(d, str):
        d = date.fromisoformat(d)
    d += timedelta(days=1)
    while market_closed(d):
        d += timedelta(days=1)
    return d


def prev_session(d):
    if isinstance(d, str):
        d = date.fromisoformat(d)
    d -= timedelta(days=1)
    while market_closed(d):
        d -= timedelta(days=1)
    return d


def window(event_date, session):
    """The two dates the realised move is measured between.

    Identical in shape to stage E because Canada reports on the same clock as the US:
    amc prints after 16:00 ET and is measured close(D) -> close(D+1); bmo prints before
    09:30 ET and is measured close(D-1) -> close(D). Europe needed its own rule because
    89% of its releases land before the open of the SAME day the vendor names.
    """
    if session == "bmo":
        return prev_session(event_date).isoformat(), \
            (event_date if isinstance(event_date, str) else event_date.isoformat())
    d = event_date if isinstance(event_date, str) else event_date.isoformat()
    return d, next_session(d).isoformat()


# --- event shape ------------------------------------------------------------------
# A Canadian junior's headline flow is full of the word "results" and none of it is
# financial: "Reports High-Grade Drill Results" is the single most common shape on the
# TSXV. A classifier that misses that reads a shell's assay news as an earnings history.
FINANCIAL_HEADLINE = re.compile(r"""(
   financial\s+(results|statements|report)
 | (first|second|third|fourth|q[1-4]|full[-\s]year|fiscal|annual|interim|quarterly|year[-\s]end)\s
   [^.]{0,40}?\b(results|earnings)\b
 | \b(results|earnings)\b[^.]{0,30}\b(quarter|fiscal|year\s+ended|period\s+ended)\b
 | reports?\s+(its\s+)?(first|second|third|fourth|q[1-4]|full[-\s]year|fiscal|annual|interim|quarterly)
 | \bearnings\b
 | résultats\s+(financiers|annuels|trimestriels|du\s)
)""", re.I | re.X)
NON_FINANCIAL = re.compile(
    r"\b(drill|drilling|assay|exploration|metallurg|intercept|borehole|trench|sampling|"
    r"resource estimate|feasibility|PEA|grade)\b", re.I)

# "We will report on X" -- precise, not sensitive. 0 false positives on 27 names that
# did not report, 11 of 61 on names that did. Promotes a disputed date; never drops one.
ANNOUNCEMENT_HEADLINE = re.compile(
    r"(to\s+(report|announce|release|host)|conference\s+call|webcast|"
    r"date\s+of\s+(its\s+)?(q[1-4]|quarter|annual)|schedul)", re.I)


def is_financial_headline(h):
    h = h or ""
    return bool(FINANCIAL_HEADLINE.search(h)) and not NON_FINANCIAL.search(h)


def event_shape(headlines, threshold=2):
    """`release` if this issuer publishes results on the wire, else `filing_only`.

    Counted over whatever news history is handed in (100 items is what the stage
    pulls). Measured on 88 past events: wire reporters have a median of 17 financial
    headlines and filing-only issuers a median of 0. At a threshold of 2 it keeps 60 of
    61 wire reporters. It is deliberately loose: the cost of dropping a real reporter is
    a lost name, and the cost of admitting a filing-only one is one wasted hunter whose
    finding the resolver will then score against a print that moved nothing.
    """
    n = sum(1 for h in headlines if is_financial_headline(h))
    return ("release" if n >= threshold else "filing_only"), n


def announced_before(news_rows, event_date, lookback_days=45):
    """Did the issuer itself say it would report around then? Returns the headline."""
    if isinstance(event_date, str):
        event_date = date.fromisoformat(event_date)
    lo = (event_date - timedelta(days=lookback_days)).isoformat()
    for r in news_rows or []:
        d = (r.get("datetime") or "")[:10]
        h = r.get("headline") or ""
        if lo <= d < event_date.isoformat() and ANNOUNCEMENT_HEADLINE.search(h) \
           and is_financial_headline(h):
            return {"headline": h, "datetime": r.get("datetime"),
                    "source": r.get("source")}
    return None

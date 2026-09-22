#!/usr/bin/env python3
"""What is true about the ASX, in one place, measured rather than assumed.

Stage AU is one market, so this module is small. It exists anyway, for the same reason
`eu_market.py` does: the two facts below are load-bearing, they are easy to get wrong in
a way that produces a plausible-looking wrong answer, and a later reader needs to find
the measurement rather than the assumption.

THE VENDOR'S DATE IS OFF BY ONE DAY FOR 85% OF AUSTRALIAN ROWS
--------------------------------------------------------------
Measured 2026-09-22 against the ASX announcement record: 80 vendor rows above the
$200k turnover floor whose last release fell between 2026-08-01 and 2026-09-19, each
checked against that issuer's own announcement history.

    vendor date minus ASX date      +1 day  63 (85%)   +0 day  8 (11%)
                                    other    3 ( 4%)   unmatched 6 of 80

The cause is not a vendor error. It is the timezone: Sydney is UTC+10 (UTC+11 on
daylight time) and the vendor stamps the UTC instant. BHP lodged its Appendix 4E at
08:31 on 18 August Sydney time, which is 22:31 on 17 August UTC, and the vendor says
17 August. Every one of the eight `+0` rows is an afternoon or post-close lodgement,
where the Sydney date and the UTC date agree.

So a pre-open Australian row must be shifted forward one day before anything is done
with it. Getting this wrong does not throw: it seals a baseline on the wrong evening,
measures the move over the wrong window and hunts a name whose print has already
happened. `SUBMARKET.md` warned that a wrong session roughly halves the measured move
in Europe; here it would not halve it, it would point at the wrong day entirely.

AUSTRALIA IS A BEFORE-THE-OPEN MARKET, MORE SO THAN EUROPE
-----------------------------------------------------------
Of the 74 results announcements matched in that same sample:

    pre-open, before 10:00 Sydney     67  (91%)
    post-close, 16:00 or later         4  ( 5%)
    in-session                         3  ( 4%)

against 89.4% pre-open for the UK. The measurement window for a `bmo` name is therefore
`close(D-1) -> close(D)`, the baseline must be sealed on the evening before the print,
and the Routine fires after the Sydney close to seal for the NEXT session.

The vendor's own session flag is reliable once the date shift is applied: 66 of 67
pre-open rows carried flag -1 and 5 of 5 post-close or in-session rows carried flag +1.
Flag 0 is an admission of ignorance and is treated as one, never guessed.

THE TRADING CALENDAR COMES OFF THE TAPE, NOT OFF A HOLIDAY LIST
----------------------------------------------------------------
ASX's own holiday pages returned 404 from this container on 2026-09-22, and a scraped
list that silently goes stale is worse than no list. Trading days are therefore read
from the index tape itself: a session with a bar happened, a session without one did
not. That is self-verifying and cannot drift, and it is the same reasoning
`jp_universe.py` gives for reading the Cabinet Office list rather than guessing -- an
empty calendar has two causes that look identical and mean opposite things.
"""
import json
import subprocess
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

SYD = ZoneInfo("Australia/Sydney")
UTC = ZoneInfo("UTC")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"
YQ = "https://query1.finance.yahoo.com"

MARKET = {
    "code": "AU",
    "name": "Australia",
    "scanner": "australia",              # TradingView's country scanner
    "exchange_allow": {"ASX"},           # the scanner also carries ASXCEN and CHIXAU
    "yahoo_suffix": ".AX",
    "currency": "AUD",
    "tz": "Australia/Sydney",
    "open_local": "10:00",
    "close_local": "16:00",              # continuous; the closing auction runs to ~16:12
    "language": "en",
    "hunter": "unpriced-hunter-au",
    "index_symbol": "^AXJO",             # S&P/ASX 200, the trading-day oracle
    # Whole-day archive for TODAY, per-issuer archive by year going back years.
    "confirm_day": "https://www.asx.com.au/asx/v2/statistics/todayAnns.do",
    "confirm_issuer": ("https://www.asx.com.au/asx/v2/statistics/announcements.do"
                       "?by=asxCode&asxCode={code}&timeframe=Y&year={year}"),
    "confirm_name": "ASX company announcements (whole-day today, per-issuer by year)",
    "short_register": "ASIC daily aggregated short positions",
}

# The vendor's session flag. 0 is an admission of ignorance and is treated as one.
SESSION_FLAG = {-1: "bmo", 1: "amc", 0: None}

# Headline classifiers. Deliberately NARROW: a bare "Annual Report" often lands days
# after the numbers and an Appendix 4G is corporate governance lodged alongside them,
# so neither is evidence on its own.
RESULTS_PATTERNS = (
    r"appendix 4[de]\b",
    r"preliminary final report",
    r"(full.?year|half.?year|fy\d{2}|hy\d{2}|interim|annual)\s+"
    r"(results|financial results|report and accounts)",
    # `commentary` and a bare `results release` were added after the 2026-08-27
    # validation run left Mayfield Group `announced_unclassified` on a day it had
    # lodged "FY2026 Results Commentary". Widened deliberately narrowly: the exclusion
    # list still wins, so "Results Release Date" and "Results of Meeting" stay out.
    r"\bresults\s+(announcement|presentation|commentary|release|for announcement)",
)

# HALF THE ASX DOES NOT LODGE A 4D OR A 4E AT ALL, and treating that as a missing print
# is wrong. Mining explorers and early-stage companies lodge an Appendix 4C or 5B with a
# quarterly activities report under Listing Rule 4.7B: mandatory, quarterly, and
# genuinely market-moving for names whose whole story is cash burn and drilling. IperionX
# (IPX) is the worked example -- three years of ASX history, not one Appendix 4D or 4E,
# and the vendor calendar schedules it as an earnings event anyway.
#
# So this is a SECOND class, not a wider version of the first. A hunter told a name
# reports a cash-flow statement rather than a profit result is hunting a different bar,
# and `history.kinds` carries the mix so nobody has to guess.
QUARTERLY_PATTERNS = (
    r"appendix (4c|5b)\b",
    r"quarterly (activities|cashflow|cash flow|report|activity)",
    # "December 2025 Quarterly Report" is the common ASX headline shape. The trailing
    # noun is REQUIRED: without it "S&P DJI Announces September 2026 Quarterly
    # Rebalance" classified as a print and was scored as a -4.88% reaction on MYR.
    r"(march|june|september|december)\s+\d{4}\s+quarterly\s+(report|activities)",
)

# A NOTICE OF A RESULTS DATE IS NOT A RESULT. Stage EU measured this exact defect in
# Oslo: "Invitation to Q4 results" counted as a print for 12 of Nordic Semiconductor's
# 25 rows, each a week before the real event, which halved the measured reaction scale.
# Myer's "FY24 Results Release Date" on 2024-09-04 is the same object and was scored as
# a -3.53% reaction until this was added. These are checked FIRST and win.
NOT_RESULTS_PATTERNS = (
    # "Half Year Results Release Details" (TUA, 2026-03-12) is a one-page notice of
    # when the results will come, and it scored as a -4.13% reaction until `details`
    # was added here. `date` alone did not catch it.
    r"results? (release )?(date|details|timing)",
    # Any headline that calls itself "details" is a notice of arrangements, not the
    # numbers. TUA lodged "Details for FY24 Full Year Results Investor Presentation"
    # and "HY25 Results Presentation Details" thirteen and nine days before the actual
    # Appendix 4E and 4D, and both scored as reactions until this line existed.
    r"\bdetails\b",
    r"date of (the )?(results|report)",
    r"\bnotice of\b",
    r"\binvitation\b",
    r"(conference call|webcast|briefing|investor day|agm|annual general meeting)",
    r"results of meeting",
    r"\btrading halt\b",
    r"timing of",
    # Index maintenance is lodged against the stock and is not a print.
    r"(rebalance|s&amp;p dji|s&p dji|index (review|adjustment))",
)


def sh(cmd):
    return subprocess.run(cmd, capture_output=True)


def fetch(url, timeout=45, referer=None):
    """curl, not urllib: this container reaches the internet through a proxy urllib
    does not pick up, and a silent URLError here looks like an empty calendar rather
    than a broken fetch. Same reason jp_universe.py and eu_universe.py give."""
    cmd = ["curl", "-sSL", "--max-time", str(timeout), "-H", f"User-Agent: {UA}"]
    if referer:
        cmd += ["-H", f"Referer: {referer}"]
    cmd.append(url)
    return sh(cmd).stdout


def yahoo_symbol(code):
    """ASX codes are three letters; a few carry a class suffix the tape writes with a
    hyphen. `.AX` is Yahoo's suffix and a wrong symbol returns an EMPTY CHART rather
    than an error, which is how stage EU nearly lost its largest Nordic names."""
    return f"{code.replace('.', '-')}.AX"


_days = {"rows": None}


def trading_days(refresh=False):
    """Every ASX session in the last two years, newest last, read off the index tape.

    Returns [date]. An empty list means the fetch failed, which the caller MUST tell
    apart from a closed market -- they look identical and mean opposite things.
    """
    if _days["rows"] is not None and not refresh:
        return _days["rows"]
    url = f"{YQ}/v8/finance/chart/%5EAXJO?range=2y&interval=1d"
    try:
        d = json.loads(fetch(url).decode("utf-8", "replace"))
        res = d["chart"]["result"][0]
        closes = res["indicators"]["quote"][0]["close"]
        out = [datetime.fromtimestamp(t, SYD).date()
               for t, c in zip(res["timestamp"], closes) if c is not None]
    except Exception:
        out = []
    _days["rows"] = sorted(set(out))
    return _days["rows"]


def easter(year):
    """Western Easter Sunday. Anonymous Gregorian algorithm."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    el = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * el) // 451
    return date(year, (h + el - 7 * m + 114) // 31,
                ((h + el - 7 * m + 114) % 31) + 1)


def _observed(d):
    """A holiday falling on a weekend is observed on the following Monday."""
    if d.weekday() == 5:
        return d + timedelta(days=2)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def exchange_holidays(year):
    """ASX equity-market non-trading days.

    Needed because `trading_days()` only knows the PAST: the tape can say a session
    happened, never that a future one will. This stage seals for the NEXT session, so
    the first date it cares about is always beyond the tape -- and without this the
    fallback below read "weekday means open", which would have called an ASX holiday
    Monday a quiet session. That is the two-causes-look-identical failure this repo
    keeps paying for, and the Routine fires on Sundays, so a holiday Monday is not a
    corner case.

    ANZAC Day is deliberately NOT substituted when it falls on a weekend: unlike the
    other national holidays the ASX does not shift it. If that turns out to be wrong,
    a resolved run will show a session the tape has and this list denies, which is
    visible rather than silent.
    """
    e = easter(year)
    jun1 = date(year, 6, 1)
    days = {}

    def put(d, label):
        while d in days:                     # two observances cannot share a day
            d += timedelta(days=1)
        days[d] = label

    put(_observed(date(year, 1, 1)), "New Year's Day")
    put(_observed(date(year, 1, 26)), "Australia Day")
    put(e - timedelta(days=2), "Good Friday")
    put(e + timedelta(days=1), "Easter Monday")
    anzac = date(year, 4, 25)
    if anzac.weekday() < 5:                  # not substituted when it falls on a weekend
        put(anzac, "ANZAC Day")
    put(jun1 + timedelta(days=(7 - jun1.weekday()) % 7 + 7), "King's Birthday")
    # ORDER MATTERS AND THE COLLISION IS REAL. Christmas 2027 is a Saturday and Boxing
    # Day a Sunday, so both want Monday the 27th; the ASX keeps Christmas on the Monday
    # and pushes Boxing Day to the Tuesday. Written as a dict literal, the second entry
    # silently overwrote the first and the year came back with two Boxing Days and no
    # Christmas -- the right dates under the wrong names, which is exactly the kind of
    # thing that reads fine until somebody debugs a missing session by the label.
    put(_observed(date(year, 12, 25)), "Christmas Day")
    put(_observed(date(year, 12, 26)), "Boxing Day")
    return days


def market_open_on(day, days=None):
    """(open, basis). `open` is True / False / None.

    None means nothing could be established, and a caller that treats None as False has
    invented a holiday. The basis says which of three instruments answered, because
    "the tape says this session happened" and "no holiday rule forbids it" are
    different strengths of claim.
    """
    days = days if days is not None else trading_days()
    if days and day <= days[-1]:
        return (day in days), "ASX index tape"
    if day.weekday() >= 5:
        return False, "weekend"
    hol = exchange_holidays(day.year).get(day)
    if hol:
        return False, f"ASX holiday ({hol})"
    if not days:
        return None, ("the index tape could not be read, so nothing is established "
                      "about this session")
    return True, "beyond the tape: a weekday that is not an ASX holiday"


def next_session(after, days=None):
    """The first ASX session strictly after `after`. Beyond the tape, the next weekday."""
    days = days if days is not None else trading_days()
    later = [d for d in days if d > after]
    if later:
        return later[0]
    d = after + timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def prev_session(before, days=None):
    days = days if days is not None else trading_days()
    earlier = [d for d in days if d < before]
    if earlier:
        return earlier[-1]
    d = before - timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def sydney_event_date(vendor_epoch, session):
    """The Sydney calendar date of a print, from the vendor's UTC-stamped epoch.

    MEASURED, see the module docstring: 63 of 74 checked rows sit one day later in
    Sydney than the vendor says, and every exception is an afternoon lodgement. The
    rule applied here is the mechanism rather than the correlation -- convert the
    instant to Sydney time -- so it stays right through the daylight-saving change on
    2026-10-04, which a hardcoded `+1 day` would not.

    Returns (date, basis). `session` is used only when the epoch is a bare midnight,
    which is what the vendor serves for most rows: then a `bmo` row is the NEXT Sydney
    day and an `amc` row is the same one.
    """
    if vendor_epoch is None:
        return None, "no vendor date"
    inst = datetime.fromtimestamp(vendor_epoch, UTC)
    syd = inst.astimezone(SYD)
    if inst.hour or inst.minute:
        return syd.date(), "converted from the vendor's UTC instant to Sydney time"
    d = inst.date()
    if session == "bmo":
        return d + timedelta(days=1), ("vendor date is a bare UTC midnight; a pre-open "
                                       "Sydney print is the next calendar day (85% of "
                                       "rows measured 2026-09-22)")
    if session == "amc":
        return d, ("vendor date is a bare UTC midnight; a post-close Sydney print "
                   "shares the UTC date")
    return d + timedelta(days=1), ("vendor date is a bare UTC midnight and the session "
                                   "is UNRESOLVED; the pre-open majority is assumed and "
                                   "the row carries session_unresolved")


def window_for(session, event_date, days=None):
    """The measurement window, as dates off the tape.

    A `bmo` print lands before the 10:00 open, so the move is close(D-1) -> close(D)
    and the baseline has to be sealed on the evening of D-1. An `amc` print lands after
    the 16:00 close, so it is close(D) -> close(D+1), the same shape as the US stage.
    """
    d = event_date if isinstance(event_date, date) else date.fromisoformat(event_date)
    if session == "amc":
        return {"from_close": d.isoformat(),
                "to_close": next_session(d, days).isoformat(),
                "text": f"close {d} 16:00 AEST -> close {next_session(d, days)}"}
    return {"from_close": prev_session(d, days).isoformat(),
            "to_close": d.isoformat(),
            "text": f"close {prev_session(d, days)} 16:00 AEST -> close {d}"}

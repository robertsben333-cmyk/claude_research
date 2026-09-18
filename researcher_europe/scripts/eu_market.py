#!/usr/bin/env python3
"""What the three European markets have in common, and where they differ.

One module rather than three adapters in three files, because the differences are
small and enumerable -- a ticker suffix, a currency, a holiday rule, a confirmation
source -- while the regulatory spine is genuinely shared (MAR Article 17 ad-hoc
disclosure, the Transparency Directive's annual-plus-half-year floor, the Short
Selling Regulation's 0.5% public threshold). Keeping them in one table means a change
to the shape has to be made once and cannot drift between markets, which is the thing
this repo keeps paying for.

CURRENCY. The UK quotes in pence (GBp) on Yahoo and in GBX on the vendor calendar;
France and Germany quote in EUR. Moves are in percent so the ranking key is unaffected,
but the TURNOVER FLOOR is an absolute number and would mean three different things in
three currencies. Everything is therefore normalised to **USD** before the floor is
applied, using a live rate off Yahoo rather than a constant, and the rate used is
written into the universe file so a later reader can reproduce the cut.

THE SESSION IS THE WEAK POINT AND IT IS FLAGGED, NEVER GUESSED. 89.4% of UK results
announcements land before 08:00 London (339 of 379 measured RNS timestamps), so Europe
is a before-the-open market and the window is close(D-1) -> close(D). The vendor
calendar says `unknown` for 150 of 318 German and 238 of 346 French rows, and windowing
an unknown row as if it were pre-market understates the move -- it produced a spurious
German maximum realised move of 15.4% in the Phase 1 measurement where taking the larger
of the two adjacent windows gives 27.5%. So an unresolved session is carried as
`session_unresolved: true` and the resolver measures both windows rather than picking
one silently.
"""
from datetime import date, timedelta

# TradingView's public scanner is the forward calendar. Measured against the actual RNS
# record over 20 sampled days: 90 of its UK rows fell on a scraped day and 88 had a
# same-day results announcement from the same issuer -- a 2.2% phantom rate, against the
# US stage's `time-not-supplied` rate of 20 of 20 on 2026-09-17. It is still a VENDOR
# calendar and `event_occurred: false` has to stay reachable; see eu_resolve.py.
MARKETS = {
    "uk": {
        "name": "United Kingdom",
        "scanner": "uk",
        "exchange_prefix": "LSE",
        "yahoo_suffix": ".L",
        "currency": "GBP",          # quoted in pence; Yahoo reports GBp
        "tz": "Europe/London",
        "close_local": "16:30",
        "language": "en",
        "hunter": "unpriced-hunter-uk",
        # The confirmation source. Investegate mirrors RNS plus the EQS / GlobeNewswire
        # / PR Newswire feeds, carries the issuer's EPIC and a timestamp, and is
        # queryable BY DATE back to 1999 -- which TDnet is not, since it keeps ~31 days.
        "confirm": "https://www.investegate.co.uk/today-announcements/{date}",
        "confirm_name": "Investegate (RNS mirror)",
        "short_register": "FCA aggregated net short positions",
    },
    "de": {
        "name": "Germany",
        "scanner": "germany",
        "exchange_prefix": "XETR",
        "yahoo_suffix": ".DE",
        "currency": "EUR",
        "tz": "Europe/Berlin",
        "close_local": "17:30",
        "language": "de",
        "hunter": "unpriced-hunter-de",
        # EQS-News is the DGAP successor and carries the MAR Article 17 `ad-hoc` stream
        # plus Quartalsmitteilung / Halbjahresbericht corporate releases. It serves a
        # ~60-item server-rendered snapshot of the LIVE feed and does not paginate --
        # `?paged=2`, `/page/2/` and `?label=Reports` all return byte-identical HTML --
        # so it confirms today and yesterday and cannot be searched historically.
        # Resolve promptly or the confirmation is lost, exactly as for TDnet.
        "confirm": "https://www.eqs-news.com/",
        "confirm_name": "EQS-News (DGAP successor), same-day snapshot only",
        "short_register": "Bundesanzeiger Netto-Leerverkaufspositionen",
    },
    "fr": {
        "name": "France",
        "scanner": "france",
        "exchange_prefix": "EURONEXT",
        "yahoo_suffix": ".PA",
        "currency": "EUR",
        "tz": "Europe/Paris",
        "close_local": "17:35",
        "language": "fr",
        "hunter": "unpriced-hunter-fr",
        "confirm": "https://live.euronext.com/en",
        "confirm_name": "Euronext Paris company news (SPA; weakest of the three)",
        # NOT SOLVED. www.data.gouv.fr, which hosts the AMF's public register, is
        # unreachable by curl from this container -- every request including the site
        # root dies with `Recv failure: Connection reset by peer` and the agent proxy
        # logs `ws_closed_mid_exchange`. WebFetch reads the dataset page but cannot
        # deliver a 4.9 MB CSV. So French names run with `positioning` empty and their
        # lean falls back to the run-up, which is ALSO the free control. That is the
        # exact defect jp_positioning.py exists to fix, live for one of three markets,
        # and `lean_vs_free_control_rho` is reported per market so it stays visible.
        "short_register": None,
    },
}


def easter(y):
    """Anonymous Gregorian algorithm. Arithmetic, not a fetched fact."""
    a = y % 19
    b, c = divmod(y, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return date(y, month, day + 1)


def exchange_holidays(market, year):
    """The days the EXCHANGE is shut, which is not the same as the public holidays.

    Germany is the trap the brief names: German public holidays are partly
    Land-specific, and a generic holiday API returns Fronleichnam and Allerheiligen,
    on which XETRA trades normally. XETRA's own closed list is short and fixed, so it
    is written out here rather than filtered out of a list that was never about the
    exchange. Euronext Paris is likewise shorter than the French jours feries.

    The UK is the one case where the public list IS the exchange list, and gov.uk
    publishes it as JSON; eu_universe.py fetches it and falls back to this.
    """
    e = easter(year)
    good_friday = e - timedelta(days=2)
    easter_monday = e + timedelta(days=1)
    if market == "de":                              # XETRA / Frankfurt
        out = {good_friday, easter_monday,
               date(year, 1, 1), date(year, 5, 1),
               e + timedelta(days=50),              # Pfingstmontag
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26),
               date(year, 12, 31)}
    elif market == "fr":                            # Euronext Paris
        out = {good_friday, easter_monday,
               date(year, 1, 1), date(year, 5, 1),
               date(year, 12, 25), date(year, 12, 26)}
    else:                                           # LSE, fallback only
        out = {good_friday, easter_monday,
               date(year, 1, 1), date(year, 12, 25), date(year, 12, 26)}
    return {d.isoformat() for d in out}


# Half sessions. Not closures, so they are reported rather than used to skip a day --
# but a print into a 12:30 close has half the exit window the measurement assumes, and
# a reader is entitled to know which rows those are.
def half_session(market, day):
    d = date.fromisoformat(day) if isinstance(day, str) else day
    if market == "uk" and (d.month, d.day) in ((12, 24), (12, 31)):
        return "12:30 close"
    if market == "fr" and (d.month, d.day) in ((12, 24), (12, 31)):
        return "14:05 close"
    if market == "de" and (d.month, d.day) == (12, 30):
        return "14:00 close"
    return None


def yahoo_symbol(market, tv_symbol):
    """`LSE:RR.` -> `RR.L`, `XETR:SAP` -> `SAP.DE`, `EURONEXT:MC` -> `MC.PA`.

    A dot inside a UK ticker (RR., BT.A) is a real part of the EPIC and Yahoo keeps it,
    so it is left alone; a hyphenated class marker is not translated because no case in
    the sampled universes needed it. A symbol that does not resolve is dropped with a
    reason rather than silently skipped.
    """
    t = tv_symbol.split(":", 1)[1] if ":" in tv_symbol else tv_symbol
    return t + MARKETS[market]["yahoo_suffix"]

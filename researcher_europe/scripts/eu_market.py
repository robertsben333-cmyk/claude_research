#!/usr/bin/env python3
"""What the ten European markets have in common, and where they differ.

One module rather than ten adapters in ten files, because the differences are
small and enumerable -- a ticker suffix, a currency, a holiday rule, a confirmation
source -- while the regulatory spine is genuinely shared (MAR Article 17 ad-hoc
disclosure, the Transparency Directive's annual-plus-half-year floor, the Short
Selling Regulation's 0.5% public threshold). Keeping them in one table means a change
to the shape has to be made once and cannot drift between markets, which is the thing
this repo keeps paying for.

SEVEN MARKETS WERE ADDED ON 2026-09-19, ON THE OPERATOR'S INSTRUCTION: the four Nordics
(Stockholm, Copenhagen, Oslo, Helsinki), Warsaw, Milan and Madrid. They are the same
stage, the same scorer and the same $200k floor, and they are NOT equally instrumented.
Read `capability()` before trusting any of them: four are complete, one has a register
and a partial archive, and two have neither. That is carried in the data rather than
argued about, exactly as `anchor_covered` carries the cost of the $200k floor.

WHY THESE SEVEN, MEASURED 2026-09-19 against TradingView's forward calendar. Over the
ten sessions 2026-09-21 -> 10-02 they add SIX names, which looks like nothing -- and it
is, because late September is the UK's month and nobody else's. By MONTH of forward
events the picture inverts: October is the current stage's THINNEST month at 114 events
for UK+DE+FR, and the new seven carry **456** in it; November is 309 against 515. The
Nordics are the engine (Sweden 259 forward events in October, Finland 77, Norway 69),
and they report QUARTERLY -- measured median gaps of 91-98 days against the UK's 217 and
France's 204 -- so a Nordic name recurs four times a year where a UK one recurs twice.
That is the pooling argument `SUBMARKET.md` makes for the original three, and it is the
whole reason these seven are worth their code.

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
        # plus Quartalsmitteilung / Halbjahresbericht corporate releases. Its FRONT PAGE
        # is a ~60-item snapshot that does not paginate, which is what Phase 1 measured
        # and why this stage believed German confirmation expired after a day. Its
        # SEARCH does paginate -- `/search-results/page/<n>/` -- and goes back years,
        # carrying the date, news type, company, headline and ISIN per row. What it has
        # no query for is a whole DAY, so the German archive is assembled per issuer and
        # a German name that is not found resolves null, never false.
        "confirm": ("https://www.eqs-news.com/search-results/"
                    "?searchtype=news&searchword={issuer}"),
        "confirm_name": "EQS-News search (per issuer, paginated, back years)",
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
        # The AMF's own regulated-information archive, through its Opendatasoft API.
        # 536,868 records back to 2012, current to yesterday, queryable BY DATE with no
        # key -- and it carries the ISSUER'S OWN filing category, which neither
        # Investegate nor EQS does. Phase 1's "FR -- nothing readable" was true of
        # Euronext's SPA and was never tested against this.
        "confirm": ("https://www.info-financiere.gouv.fr/api/explore/v2.1/catalog/"
                    "datasets/flux-amf-new-prod/records"),
        "confirm_name": "AMF regulated-information flux (info-financiere.gouv.fr)",
        # SOLVED 2026-09-19. Phase 1 recorded www.data.gouv.fr as unreachable on four
        # connection resets; re-tested eighteen times it answers roughly one request in
        # three, so the register comes in two retried hops -- the dataset endpoint for
        # the resource's current direct URL, then the CSV off
        # object-api.infra.data.gouv.fr, which has never failed here. 40,696 per-holder
        # rows back to 2012 with publication start AND end dates, so the aggregate can
        # be reconstructed as of any past date: the French change is measured rather
        # than approximated, and it is backtestable. See eu_positioning.load_fr().
        "short_register": "AMF positions courtes nettes (data.gouv.fr, per-holder "
                          "history since 2012)",
    },
    # --- the Nordics, added 2026-09-19 --------------------------------------------
    #
    # ONE REGION, FOUR REGULATORS, TWO NEWS INFRASTRUCTURES. Sweden, Denmark and Finland
    # list on Nasdaq's Nordic markets and disclose through one feed
    # (`api.news.eu.nasdaq.com`), which carries the ISSUER'S OWN disclosure category --
    # `Interim report`, `Half Year financial report`, `Annual Report` -- so a Nordic
    # results release is classified by what the issuer filed it as, not by a headline
    # keyword. Only France had that until now. Norway is on Euronext and discloses
    # through Oslo Bors NewsWeb, which is better still: a true whole-day query, keyed by
    # TICKER rather than by issuer name, with English category labels.
    #
    # The short registers are four separate national files and all four read (measured
    # 2026-09-19). NORWAY'S carries a full dated event history, so its change is a
    # measurement rather than a cache diff -- the property that makes the FCA and AMF
    # files backtestable and Bundesanzeiger's not. Sweden's, Denmark's and Finland's are
    # snapshots and are diffed against the cache. Sweden's snapshot does carry the date
    # its level last changed, which is staleness rather than history and is worth
    # reading on its own.
    #
    # WHAT IS WEAKER HERE THAN THE BRIEF SUGGESTS: Nordic issuers publish in English as a
    # matter of course. That is a real dent in the language thesis this stage is testing,
    # and it is why `local_pass_note` matters more here than anywhere else -- a Nordic
    # `pre_local` delta of zero may mean the local pass found nothing, or it may mean
    # there was no local-only information to find. See `unpriced-hunter-nordic`.
    "se": {
        "name": "Sweden",
        "scanner": "sweden",
        "exchange_prefix": "OMXSTO",
        # The vendor's `sweden` scanner pools OMXSTO (663 names) with NGM (230). NGM is a
        # different venue and its names do not carry Yahoo's `.ST`, so a row from it
        # would be screened on a tape that is not its own. Filtered, not silently mapped.
        "exchange_allow": {"OMXSTO"},
        "yahoo_suffix": ".ST",
        "currency": "SEK",
        "tz": "Europe/Stockholm",
        "close_local": "17:30",
        "language": "sv",
        "hunter": "unpriced-hunter-nordic",
        "region": "nordic",
        "confirm": ("https://api.news.eu.nasdaq.com/news/query.action"
                    "?type=json&showCompany=true&limit=200&start={start}"),
        "confirm_name": "Nasdaq Nordic disclosure feed (issuer's own category; "
                        "paged back ~12 days, no date query)",
        "short_register": "Finansinspektionen aggregerade korta nettopositioner "
                          "(ODS, snapshot; the date is when the level last changed)",
    },
    "dk": {
        "name": "Denmark",
        "scanner": "denmark",
        "exchange_prefix": "OMXCOP",
        "exchange_allow": {"OMXCOP"},
        "yahoo_suffix": ".CO",
        "currency": "DKK",
        "tz": "Europe/Copenhagen",
        "close_local": "17:00",
        "language": "da",
        "hunter": "unpriced-hunter-nordic",
        "region": "nordic",
        "confirm": ("https://api.news.eu.nasdaq.com/news/query.action"
                    "?type=json&showCompany=true&limit=200&start={start}"),
        "confirm_name": "Nasdaq Nordic disclosure feed (issuer's own category; "
                        "paged back ~12 days, no date query)",
        # The one register of the ten published as an HTML table rather than a file, and
        # the only one whose threshold is 0.1% rather than 0.5% -- so a Danish zero is a
        # STRONGER statement than a Swedish or British one. 50 issuers when measured.
        "short_register": "Finanstilsynet aggregerede korte nettopositioner "
                          "(HTML table, 0.1% threshold)",
    },
    "no": {
        "name": "Norway",
        "scanner": "norway",
        "exchange_prefix": "OSL",
        "exchange_allow": {"OSL"},
        "yahoo_suffix": ".OL",
        "currency": "NOK",
        "tz": "Europe/Oslo",
        "close_local": "16:25",
        "language": "no",
        "hunter": "unpriced-hunter-nordic",
        "region": "nordic",
        # THE BEST ARCHIVE OF THE TEN AFTER INVESTEGATE. A real fromDate/toDate query,
        # and every row carries `issuerSign` -- the exchange ticker -- so confirmation
        # joins on a code rather than on a normalised company name, which is the weakest
        # link everywhere else in this stage.
        "confirm": ("https://api3.oslo.oslobors.no/v1/newsreader/list"
                    "?fromDate={date}&toDate={date}"),
        "confirm_name": "Oslo Bors NewsWeb (true day query, ticker-keyed, categorised)",
        "short_register": "Finanstilsynet SSR register (JSON, dated events per issuer)",
    },
    "fi": {
        "name": "Finland",
        "scanner": "finland",
        "exchange_prefix": "OMXHEX",
        "exchange_allow": {"OMXHEX"},
        "yahoo_suffix": ".HE",
        "currency": "EUR",
        "tz": "Europe/Helsinki",
        "close_local": "18:30",          # EET, = 17:30 CET
        "language": "fi",
        "hunter": "unpriced-hunter-nordic",
        "region": "nordic",
        "confirm": ("https://api.news.eu.nasdaq.com/news/query.action"
                    "?type=json&showCompany=true&limit=200&start={start}"),
        "confirm_name": "Nasdaq Nordic disclosure feed (issuer's own category; "
                        "paged back ~12 days, no date query)",
        "short_register": "Finanssivalvonta net short positions (JSON, per holder)",
    },
    # --- the south and CEE, added 2026-09-19 ---------------------------------------
    #
    # THESE THREE ARE THE WEAK LEGS AND THE FILE SAYS SO RATHER THAN AVERAGING IT AWAY.
    # Their vendor forward-date coverage is 0.20 (IT), 0.19 (ES) and 0.13 (PL) of their
    # universes against 0.88 for Finland and 0.81 for Norway, so the calendar itself sees
    # only a fifth of them -- which is France's regime (0.27), and France was measured to
    # be undercounted 3.6x by this vendor. Italy has a register and an archive; Spain and
    # Poland have neither, and a name from those two is hunted with NO positioning anchor
    # and NO way to reach `event_occurred: false`.
    "it": {
        "name": "Italy",
        "scanner": "italy",
        "exchange_prefix": "MIL",
        "exchange_allow": {"MIL"},
        "yahoo_suffix": ".MI",
        "currency": "EUR",
        "tz": "Europe/Rome",
        "close_local": "17:30",
        "language": "it",
        "hunter": "unpriced-hunter-it",
        "region": "south",
        # eMarket STORAGE is Borsa Italiana's officially appointed storage mechanism.
        # Both it and CONSOB sit behind a WAF that answers INTERMITTENTLY from this
        # container -- emarketstorage 7 of 8, the CONSOB short-selling page 2 of 5 -- so
        # both are retried rather than believed on one failure. That is the France
        # lesson: this repo has twice written a host off as blocked after four tries and
        # been wrong twice.
        "confirm": "https://www.emarketstorage.com/it/comunicati-finanziari",
        "confirm_name": "eMarket STORAGE (Borsa Italiana OAM; WAF-intermittent, retried)",
        "short_register": "CONSOB posizioni nette corte (PncPubbl.xlsx, per holder)",
    },
    "es": {
        "name": "Spain",
        "scanner": "spain",
        "exchange_prefix": "BME",
        "exchange_allow": {"BME"},
        "yahoo_suffix": ".MC",
        "currency": "EUR",
        "tz": "Europe/Madrid",
        "close_local": "17:30",
        "language": "es",
        "hunter": "unpriced-hunter-es",
        "region": "south",
        # NEITHER RESOLVES. The CNMV short-position grid is an ASP.NET postback behind a
        # cookie gate that returns no table when driven from here, and every
        # `Consulta-OIR` / `InformacionRelevante` path answers 403 on 8 of 8 tries. So a
        # Spanish name has no positioning anchor and cannot be confirmed or killed.
        "confirm": None,
        "confirm_name": "none reachable (CNMV OIR returns 403 from this container)",
        "short_register": "none reachable (CNMV grid is an ASP.NET postback that "
                          "returns no rows from this container)",
    },
    "pl": {
        "name": "Poland",
        "scanner": "poland",
        "exchange_prefix": "GPW",
        # The vendor's `poland` scanner pools GPW (384) with NewConnect (325). NewConnect
        # is the growth venue and almost nothing on it clears $200k/day, but it shares
        # Yahoo's `.WA`, so unlike Sweden's NGM it would screen on the right tape. It is
        # filtered anyway: a NewConnect name has no analyst coverage, no register and no
        # archive, so it would be hunted completely blind.
        "exchange_allow": {"GPW"},
        "yahoo_suffix": ".WA",
        "currency": "PLN",
        "tz": "Europe/Warsaw",
        "close_local": "17:00",
        "language": "pl",
        "hunter": "unpriced-hunter-pl",
        "region": "cee",
        # NEITHER RESOLVES, AND THESE ARE HARD FAILURES RATHER THAN INTERMITTENT ONES.
        # `www.gpw.pl/komunikaty-spolek` and `espi.pap.pl` each returned 0 of 8 -- an
        # empty reply and a proxy 502 respectively -- where emarketstorage returned 7 of
        # 8 on the same sweep, so the eight-try standard that rescued France and Italy
        # was applied here and did not rescue Poland. The KNF short register POSTs to
        # `rss.knf.gov.pl/RssOuterView/JSCRIPT` and answers 302 then 403 with a cookie.
        "confirm": None,
        "confirm_name": "none reachable (GPW and espi.pap.pl both 0 of 8 tries)",
        "short_register": "none reachable (KNF RssOuterView returns 403)",
    },
}

# What each market can actually do, measured on 2026-09-19 and NOT a statement of intent.
# Nothing downstream may assume a capability that is not listed here: `eu_resolve.py`
# reads `archive` to decide whether `event_occurred: false` is reachable, and
# `eu_priced_in.py` reads `register` to decide whether a zero is a truncated zero or an
# absence of information. A market whose source starts working is a change HERE.
#
#   archive:  "day"    a whole-day query exists -> `event_occurred: false` is reachable
#             "paged"  no date query, but the feed pages back far enough to cover the
#                      resolve window -> false is reachable INSIDE that window only
#             "issuer" per-issuer search only -> false is NOT reachable, ever
#             None     nothing reachable -> every row resolves null
#   register: True / False, i.e. whether a national short register downloads at all.
CAPABILITY = {
    "uk": {"archive": "day",    "register": True,  "history": "observed"},
    "de": {"archive": "issuer", "register": True,  "history": "estimated"},
    "fr": {"archive": "day",    "register": True,  "history": "estimated"},
    "se": {"archive": "paged",  "register": True,  "history": "estimated"},
    "dk": {"archive": "paged",  "register": True,  "history": "estimated"},
    "no": {"archive": "day",    "register": True,  "history": "estimated"},
    "fi": {"archive": "paged",  "register": True,  "history": "estimated"},
    "it": {"archive": "day",    "register": True,  "history": "estimated"},
    "es": {"archive": None,     "register": False, "history": "estimated"},
    "pl": {"archive": None,     "register": False, "history": "estimated"},
}

# How far back the Nasdaq Nordic feed can be paged before it stops being cheap. Measured:
# 200 items a page, `start=1000` reached 12 days back, so a week costs about 7 requests.
# `fromDate` is ACCEPTED AND IGNORED by that endpoint -- it returned the most recent 200
# items for a date a month old -- which is exactly the kind of silent success that would
# have produced a confident `event_occurred: false` for every Nordic name. Page and check
# the dates; never trust the filter.
NASDAQ_MAX_PAGES = 14


def capability(market, what=None):
    c = CAPABILITY.get(market, {"archive": None, "register": False,
                                "history": "estimated"})
    return c if what is None else c.get(what)


def false_reachable(market):
    """Can `event_occurred: false` ever be written for this market?

    This is the question TRT made expensive in the US stage and it has a different
    answer per market, so it is answered in one place. `paged` markets are reachable
    only while the print is still inside the feed's rolling window; the caller checks
    that by looking at the oldest row it actually paged to, never by assuming.
    """
    return capability(market, "archive") in ("day", "paged")


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


def midsummer_eve(year):
    """The Friday between 19 and 25 June. Stockholm and Helsinki both shut for it.

    Arithmetic rather than a fetched fact, like `easter()`. Getting it wrong costs a
    run: it lands in a week the Nordic calendar is otherwise busy.
    """
    for day in range(19, 26):
        d = date(year, 6, day)
        if d.weekday() == 4:
            return d
    return date(year, 6, 25)


def exchange_holidays(market, year):
    """The days the EXCHANGE is shut, which is not the same as the public holidays.

    Germany is the trap the brief names: German public holidays are partly
    Land-specific, and a generic holiday API returns Fronleichnam and Allerheiligen,
    on which XETRA trades normally. XETRA's own closed list is short and fixed, so it
    is written out here rather than filtered out of a list that was never about the
    exchange. Euronext Paris is likewise shorter than the French jours feries.

    The UK is the one case where the public list IS the exchange list, and gov.uk
    publishes it as JSON; eu_universe.py fetches it and falls back to this.

    THE SEVEN ADDED IN 2026-09 ARE HAND-ENTERED FROM EACH EXCHANGE'S PUBLISHED TRADING
    CALENDAR AND ARE NOT FETCHED. That is a real weakness and it is stated rather than
    hidden: a missing closure makes the stage seal baselines for a shut exchange and
    report an empty calendar as if the vendor were late, which are different faults
    with different fixes. The Nordic list is the one most likely to be wrong, because
    it carries three moving feasts plus Midsummer. `market_closed` in the universe file
    records which rule fired, so a wrong entry is visible in the output rather than only
    in this source.
    """
    e = easter(year)
    good_friday = e - timedelta(days=2)
    maundy_thursday = e - timedelta(days=3)
    easter_monday = e + timedelta(days=1)
    ascension = e + timedelta(days=39)
    whit_monday = e + timedelta(days=50)
    if market == "de":                              # XETRA / Frankfurt
        out = {good_friday, easter_monday,
               date(year, 1, 1), date(year, 5, 1),
               whit_monday,                         # Pfingstmontag
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26),
               date(year, 12, 31)}
    elif market == "fr":                            # Euronext Paris
        out = {good_friday, easter_monday,
               date(year, 1, 1), date(year, 5, 1),
               date(year, 12, 25), date(year, 12, 26)}
    elif market == "se":                            # Nasdaq Stockholm
        out = {good_friday, easter_monday, ascension,
               date(year, 1, 1), date(year, 1, 6),  # Trettondedag jul
               date(year, 5, 1), date(year, 6, 6),  # Nationaldagen
               midsummer_eve(year),
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26),
               date(year, 12, 31)}
    elif market == "dk":                            # Nasdaq Copenhagen
        # Store Bededag was abolished as a Danish public holiday in 2024 and the
        # exchange trades on it, so it is deliberately absent.
        out = {maundy_thursday, good_friday, easter_monday, ascension, whit_monday,
               date(year, 1, 1), date(year, 6, 5),  # Grundlovsdag
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26),
               date(year, 12, 31)}
    elif market == "no":                            # Oslo Bors
        out = {maundy_thursday, good_friday, easter_monday, ascension, whit_monday,
               date(year, 1, 1), date(year, 5, 1), date(year, 5, 17),
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26),
               date(year, 12, 31)}
    elif market == "fi":                            # Nasdaq Helsinki
        out = {good_friday, easter_monday, ascension,
               date(year, 1, 1), date(year, 1, 6),
               date(year, 5, 1), midsummer_eve(year),
               date(year, 12, 6),                   # Itsenaisyyspaiva
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26)}
    elif market == "pl":                            # GPW Warsaw
        out = {easter_monday, e + timedelta(days=60),   # Boze Cialo
               date(year, 1, 1), date(year, 1, 6),
               date(year, 5, 1), date(year, 5, 3),
               date(year, 8, 15), date(year, 11, 1), date(year, 11, 11),
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26)}
    elif market == "it":                            # Borsa Italiana
        out = {good_friday, easter_monday,
               date(year, 1, 1), date(year, 5, 1), date(year, 8, 15),
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26),
               date(year, 12, 31)}
    elif market == "es":                            # BME Madrid
        out = {good_friday, easter_monday,
               date(year, 1, 1), date(year, 1, 6), date(year, 5, 1),
               date(year, 12, 24), date(year, 12, 25), date(year, 12, 26),
               date(year, 12, 31)}
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
    if market in ("se", "fi") and (d.month, d.day) in ((1, 5), (4, 30), (12, 23)):
        return "13:00 close"
    if market == "no" and (d.month, d.day) == (12, 23):
        return "13:00 close"
    if market in ("it", "es") and (d.month, d.day) in ((12, 24), (12, 31)):
        return "14:00 close"
    return None


# The markets whose share classes the vendor writes with an underscore and Yahoo with a
# hyphen. Measured 2026-09-19: `OMXSTO:INVE_A` is `INVE-A.ST`, `OMXHEX:NDA_FI` is
# `NDA-FI.HE`, `OMXCOP:NOVO_B` is `NOVO-B.CO`. Getting this wrong does not raise -- Yahoo
# answers with an empty chart, the row is dropped as "no tape", and the day quietly loses
# its largest Nordic names, which are exactly the ones with two share classes.
UNDERSCORE_CLASS_MARKETS = {"se", "dk", "no", "fi"}


def yahoo_symbol(market, tv_symbol):
    """`LSE:RR.` -> `RR.L`, `XETR:SAP` -> `SAP.DE`, `OMXSTO:INVE_A` -> `INVE-A.ST`.

    A dot inside a UK ticker (RR., BT.A) is a real part of the EPIC and Yahoo keeps it,
    so it is left alone. A symbol that does not resolve is dropped with a reason rather
    than silently skipped.
    """
    t = tv_symbol.split(":", 1)[1] if ":" in tv_symbol else tv_symbol
    if market in UNDERSCORE_CLASS_MARKETS:
        t = t.replace("_", "-")
    return t + MARKETS[market]["yahoo_suffix"]

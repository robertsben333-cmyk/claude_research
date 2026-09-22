#!/usr/bin/env python3
"""The day archive per market: who announced what, on a date that has already passed.

WHY THIS EXISTS
---------------
Investegate gave the UK a full RNS mirror queryable BY DATE back to 1999, and that one
instrument bought two things nothing else in this stage could: a measured phantom rate
for the vendor calendar (2 of 90 UK rows, 2.2%) and a measured TRUE event count, which
turned out to be **2.2x the vendor's** -- 5.05 UK events a day above $1m/day of turnover
against the 2.3 the forward calendar gives. Germany and France had no equivalent, so
every German and French stream number in `SUBMARKET.md` rested on a vendor feed that is
known to undercount by more than a factor of two in the one market where it could be
checked, and `event_occurred: false` was unreachable for both.

This module is that instrument for the others. It is deliberately NOT one scraper per
market with a shape each: every market returns the same row --

    {market, issuer, isin, ticker_hint, ts, headline, category, is_results,
     classified_by, url}

-- so `eu_resolve.py` confirms every market through one code path and a measurement
written for one market runs on all of them. `day()` returns **None, not []**, where the
source could not be read: that distinction is the only thing standing between "nobody
announced anything" and "I could not look", and only the first may ever support
`event_occurred: false`.

WHAT EACH MARKET ACTUALLY GIVES, MEASURED 2026-09-19
------------------------------------------------------
  UK   Investegate `/today-announcements/<date>`, paginated, back to 1999. Every EPIC
       that published anything, with the headline. Classification is by HEADLINE and
       that is its weakness: six of the eight apparent Phase 1 calendar misses were
       this classifier, not the calendar -- Trustpilot's interims went out as "AI,
       Enterprise and US momentum fuel strong growth".

  FR   **info-financiere.gouv.fr, the AMF's own regulated-information archive, through
       its Opendatasoft API.** `flux-amf-new-prod`, 536,868 records back to 2012,
       current to yesterday, 45-70 items a day, queryable by date range with no key and
       no cookie. This is the closest structural analogue to RNS in this repo and it is
       BETTER than Investegate in the one way that matters here: every record carries
       the **issuer's own declared regulated-information subtype** --
       `Rapports financiers et d'audit semestriels`, `Rapports financiers et d'audit
       annuels`, `Information financiere trimestrielle` -- so a French results release
       is identified by what the issuer filed it as, not by what its headline says.
       That is the one fix for the Trustpilot failure mode and only France has it.
       Phase 1 recorded "FR -- nothing readable. Euronext company news is an SPA",
       which was true of Euronext and never tested against the AMF's own archive.

  DE   **EQS-News search, `/search-results/?searchtype=news&searchword=<issuer or
       ISIN>`, paginated at `/search-results/page/<n>/`.** Phase 1 recorded EQS as a
       "non-paginating snapshot of the live feed" that "confirms today and yesterday
       and nothing older". That is true of the FRONT PAGE and false of the search: one
       issuer's search returns 25 rows a page over 67 pages, each carrying the date,
       the EQS news type (Ad-hoc / Corporate / Advance financial reports / Directors'
       Dealings / AGM), the company name, the headline and the **ISIN**, back years.
       So German confirmation is historical after all.

       What it is NOT is a day archive: there is no query that returns everything
       published on a date (`searchword=` empty returns nothing, a one-letter word
       returns a sparse subset). So the German day archive is assembled per issuer,
       from a list of issuers the caller supplies -- which is exactly what confirmation
       needs and makes the stream measurement cost one request per issuer.

       And EQS's news type is not a results category: `Corporate` covers both
       "Hornbach Group continues to grow" and a store opening. So German classification
       falls back to the HEADLINE, in German and English, with the same weakness the UK
       has. Only France escapes it.

  SE/DK/FI  **The Nasdaq Nordic disclosure feed**, one endpoint for all three, carrying
       the issuer's own category -- so the France property now holds in four markets
       rather than one. **Its `fromDate` is accepted and IGNORED**: a request for a date
       a month old returns the most recent 200 rows, dated today. That is the most
       dangerous failure shape in this stage, a successful-looking request for the wrong
       day, so the filter is never passed and the feed is PAGED back instead, ~200 rows
       and roughly two days per request, about twelve days before it stops being cheap.

  NO   **Oslo Bors NewsWeb.** A true `fromDate`/`toDate` query, English category labels,
       and `issuerSign` on every row -- the only archive besides Investegate that lets
       confirmation join on a TICKER instead of a normalised company name. It also takes
       `issuer=<sign>` over a multi-year range, which is what gives Norway observed
       announcement history in `eu_priced_in.no_history()`.

  IT   **eMarket STORAGE**, Borsa Italiana's officially appointed storage mechanism,
       behind the same Radware WAF as CONSOB: measured 7 of 8 good, so retried rather
       than believed on one failure. **`data_to` is EXCLUSIVE** -- asking for
       `data_from=D&data_to=D` returns zero rows and looks exactly like a silent day,
       where `data_to=D+1` returns the 19 rows that exist.

  ES/PL **Nothing.** Every CNMV `Consulta-OIR` / `InformacionRelevante` path returns 403;
       `www.gpw.pl/komunikaty-spolek` and `espi.pap.pl` each returned 0 of 8 on the sweep
       where emarketstorage returned 7 of 8, so the eight-try standard that rescued
       France and Italy was applied and did not rescue these. `day()` returns None and
       every row from them resolves null.

CLASSIFICATION IS REPORTED, NEVER ASSUMED
-----------------------------------------
Every row says how it was classified: `issuer_category` where the source publishes the
issuer's own filing category (France, and the Nordics since 2026-09-19) and `headline`
everywhere else. The headline classifier carries Swedish, Norwegian, Danish, Finnish,
Italian, Spanish and Polish vocabulary as well as English, German and French, because
`delarsrapport` and `bokslutskommunike` have no English cognate and an English-only
classifier misses every Nordic quarter. A caller that
wants to know how much of its confirmation rests on a keyword list can count them. And
a row that is not classified as results is still returned -- `announced_unclassified` is
a human call, not an automatic kill, exactly as for the UK.
"""
import argparse
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_market import MARKETS, NASDAQ_MAX_PAGES                      # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
IG_DAY = "https://www.investegate.co.uk/today-announcements/{d}"
ODS = ("https://www.info-financiere.gouv.fr/api/explore/v2.1/catalog/datasets/"
       "flux-amf-new-prod/records")
EQS_SEARCH = "https://www.eqs-news.com/search-results/"
EQS_PAGE = "https://www.eqs-news.com/search-results/page/{n}/"

# The French subtypes that ARE a periodic results filing, by the issuer's own
# declaration. Codes rather than labels: the labels exist in French and English and
# have been reworded at least once (`filename: Ancien` vs `Nouveau` in the lookup
# table), the codes have not.
FR_RESULTS_SUBTYPES = {
    "Half yearly financial reports and audit reports/limited reviews",
    "Annual financial and audit reports",
    "Quarterly financial reporting",
}
# The SECOND place the issuer's own category appears, and the one that matters most.
# A French results release is very often filed as `Informations privilegiees` -- inside
# information -- rather than as a periodic report, and then `subtype_of_information`
# reads "Inside Information" and says nothing. But the AMF's title field carries its own
# "<type> / <sous-type>" label, and the sous-type IS the declaration: MedinCell,
# Theraclion, Implanet and Advicenne all filed "Informations privilegiees / Communique
# sur comptes, resultats" -- literally "news release on accounts, results" -- and a
# headline classifier reads that as no results vocabulary at all. Four of the seven
# French rows that first measured as `announced_unclassified` were this.
FR_TITLE_CATEGORY_RE = re.compile(r"""(?ix)(
   communiqu[ée]\s+sur\s+comptes |news\s+release\s+on\s+accounts
  |rapport\s+financier\s+(semestriel|annuel) |half[-\s]?year(ly)?\s+financial\s+report
  |information\s+financi[eè]re\s+trimestrielle |quarterly\s+financial\s+report
 )""")
# Headline classification, used for the UK and Germany and as a French fallback. The
# German half is the vocabulary Prime Standard and MAR releases actually use.
RESULTS_RE = re.compile(r"""(?ix)\b(
   interim\s+(results|report|accounts|management\s+statement)
  |half[-\s]?year(ly)?  |final\s+(audited\s+)?results
  |preliminary\s+(results|announcement|figures)
  |annual\s+(results|financial\s+report|report)
  |full[-\s]?year\s*(20\d\d\s*)?(results|figures)
  |audited\s+results
  |(q[1-4]|h[12]|9m|1h|first|second|third|fourth|nine[-\s]month|six[-\s]month)
      [-\s]*(quarter|half|year)?\s*(results|figures|report)
  |quarterly\s+(results|report|statement|reporting)
  |trading\s+(statement|update)  |results\s+for\s+the
  |quartalsmitteilung |quartalszahlen |quartalsbericht |zwischenmitteilung
  |halbjahres(finanz)?(bericht|zahlen|ergebnis)  |zwischenbericht
  |jahresabschluss |jahresergebnis |gesch[aä]ftszahlen |konzernabschluss
  |vorl[aä]ufige\s+(zahlen|ergebnisse) |umsatz\s+und\s+ergebnis
  |neunmonats |halbjahr  |gesch[aä]ftsjahr\s+20\d\d
  |r[ée]sultats\s+(annuels|semestriels|du|de|\d) |chiffre\s+d.affaires
  |r[ée]sultats\s+financiers |information\s+financi[eè]re\s+trimestrielle
  # --- Nordic. `delarsrapport` (SE/NO/DK) and `osavuosikatsaus` (FI) are the ordinary
  # words for an interim report and appear in the headline far more often than any
  # English term, because these releases are bilingual and the Swedish half leads.
  # `bokslutskommunike` / `tilinpaatostiedote` is the full-year release and has NO
  # English cognate at all -- an English-only classifier misses every Nordic Q4.
  |del[aå]rsrapport |delarsrapport |kvartalsrapport |halv[aå]rsrapport
  |bokslutskommunik[ée] |[aå]rsredovisning |[aå]rsrapport |resultatrapport
  |osavuosikatsaus |puolivuosikatsaus |tilinp[aä][aä]t[oö]stiedote |vuosikertomus
  |regnskab |[aå]rsregnskab |kvartalsregnskab
  # --- Italian
  |risultati\s+(del|di|annuali|semestrali|consolidati)
  |relazione\s+finanziaria\s+(semestrale|annuale) |resoconto\s+intermedio
  |bilancio\s+(consolidato|d.esercizio) |ricavi\s+(del|di|consolidati)
  # --- Spanish
  |resultados\s+(del|de|anuales|semestrales|trimestrales)
  |informaci[oó]n\s+financiera\s+(semestral|trimestral)
  |cuentas\s+anuales |estados\s+financieros
  # --- Polish
  |raport\s+(okresowy|kwartalny|p[oó][lł]roczny|roczny)
  |skonsolidowany\s+raport |sprawozdanie\s+finansowe |wyniki\s+finansowe
 )\b""")
# An EQS type that is a results release by construction, whatever the headline says.
# "Advance financial reports" is the WpHG pre-announcement of a publication date and is
# NOT the print itself, so it is deliberately not here.
DE_RESULTS_TYPES = {"Annual Report", "Half Year Report", "Quarterly Report"}

# THE CONJUNCTION RULE, and it is the one thing in this file that was measured into
# existence. Hornbach's Q2 print went out as "HORNBACH Holding AG & Co. KGaA: Sales and
# Adjusted EBIT in Q2 2026/27 above prior year level" -- a period, a line item, a
# direction, and not one word of results vocabulary. RESULTS_RE misses it exactly as the
# UK classifier missed Trustpilot's "AI, Enterprise and US momentum fuel strong growth".
# So a headline also counts as results when it names a REPORTING PERIOD and a FINANCIAL
# LINE ITEM together. Both halves are required: "Q2 store openings" has the period and
# no line item, "EBIT margin target raised" has the line item and no period.
PERIOD_RE = re.compile(r"""(?ix)(
   \bq[1-4]\b |\bh[12]\b |\b9m\b |\b6m\b |\b1h\b |\bfy\s?20\d\d
  |first\s+(quarter|half|six|nine) |second\s+(quarter|half) |third\s+quarter
  |nine[-\s]months? |six[-\s]months? |half[-\s]?year |full[-\s]?year
  |fiscal\s+year |financial\s+year
  |erste[ns]?\s+(quartal|halbjahr) |halbjahr |neunmonats |gesch[aä]ftsjahr
  |premier\s+semestre |1er\s+semestre |exercice\s+20\d\d )""")
FIGURE_RE = re.compile(r"""(?ix)(
   \bsales\b |\brevenue|\bebit\b |\bebitda\b |\bebt\b |net\s+(income|profit|loss)
  |operating\s+(profit|result|income) |earnings |\bturnover\b |order\s+(intake|book)
  |umsatz |ergebnis |konzernergebnis |betriebsergebnis |jahres[uü]berschuss
  |chiffre\s+d.affaires |r[ée]sultat |produit\s+net )""")


def looks_like_results(headline):
    h = headline or ""
    return bool(RESULTS_RE.search(h)) or bool(PERIOD_RE.search(h)
                                              and FIGURE_RE.search(h))


def sh(cmd, timeout=60):
    return subprocess.run(cmd, capture_output=True, timeout=timeout).stdout


def get(url, timeout=45):
    return sh(["curl", "-sSL", "--max-time", str(timeout), "-H", f"User-Agent: {UA}",
               url], timeout=timeout + 10).decode("utf-8", "replace")


def norm(s):
    """Same normalisation `eu_positioning` joins registers on. Legal forms off."""
    s = (s or "").upper()
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    s = re.sub(r"\b(PLC|LIMITED|LTD|GROUP|HOLDINGS|HOLDING|THE|SA|SE|AG|INC|COMPANY|"
               r"CO|NV|SPA|KGAA|AKTIENGESELLSCHAFT|SOCIETE|ANONYME|KG)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _row(market, issuer, isin, ts, headline, category, is_results, how, url,
         ticker_hint=None):
    return {"market": market, "issuer": issuer, "issuer_norm": norm(issuer),
            "isin": isin, "ticker_hint": ticker_hint, "ts": ts,
            "headline": (headline or "").strip(), "category": category,
            "is_results": bool(is_results), "classified_by": how, "url": url}


# --- UK ----------------------------------------------------------------------------
def uk_day(day, max_pages=15):
    """Every RNS announcement mirrored by Investegate on `day`.

    The EPIC is the join key here, not the issuer name, because Investegate publishes
    it and the vendor calendar's `name` field IS the EPIC.
    """
    out, seen = [], set()
    for pg in range(1, max_pages + 1):
        url = IG_DAY.format(d=day) + (f"?page={pg}" if pg > 1 else "")
        html = get(url)
        found = re.findall(
            r'/company/([A-Z0-9\.]+)".*?announcement-link"[^>]*>([^<]*)<', html, re.S)
        if not found:
            break
        before = len(seen)
        for code, head in found:
            key = (code.upper(), head.strip()[:120])
            if key in seen:
                continue
            seen.add(key)
            out.append(_row("uk", code.upper(), None, day, head,
                            None, looks_like_results(head), "headline",
                            f"https://www.investegate.co.uk/company/{code}",
                            ticker_hint=code.upper()))
        if len(seen) == before:
            break
    return out


# --- FR ----------------------------------------------------------------------------
def fr_day(day, page_size=100, max_pages=12):
    """Every item the AMF's regulated-information flux carries for `day`.

    ODS Explore v2.1: `where=` takes a date range, `limit` caps at 100 and `offset` at
    10,000, which is far above a French day (45-70 items).
    """
    out = []
    for pg in range(max_pages):
        qs = urllib.parse.urlencode({
            "limit": page_size, "offset": pg * page_size,
            "order_by": "uin_dat_amf",
            "where": (f"uin_dat_amf >= date'{day}' and "
                      f"uin_dat_amf < date'{day}T23:59:59'")})
        try:
            d = json.loads(get(f"{ODS}?{qs}"))
        except Exception:
            break
        res = d.get("results") or []
        for r in res:
            sub = r.get("subtype_of_information")
            head = r.get("informationdeposee_inf_tit_inf") or ""
            by_cat = (sub in FR_RESULTS_SUBTYPES
                      or bool(FR_TITLE_CATEGORY_RE.search(head)))
            out.append(_row(
                "fr", r.get("identificationsociete_iso_nom_soc"),
                r.get("identificationsociete_iso_cd_isi"),
                r.get("uin_dat_amf"), head,
                f"{r.get('type_of_information')} > {sub}",
                by_cat or looks_like_results(head),
                "issuer_category" if by_cat else "headline",
                r.get("url_de_recuperation"),
                ticker_hint=r.get("identificationsociete_iso_code_tkr_iso_cd_tkr")))
        if len(res) < page_size:
            break
    return out


# --- DE ----------------------------------------------------------------------------
_EQS_ITEM = re.compile(
    r'data-news-isin="([^"]*)".*?search-result-date\s*">([^<]*)<'
    r'.*?label--news-type">([^<]*)<.*?news__company--search-result">([^<]*)<'
    r'.*?grid__headline">([^<]*)<', re.S)


def _eqs_search(word, page=1):
    q = urllib.parse.urlencode({"searchtype": "news", "searchword": word})
    url = (f"{EQS_SEARCH}?{q}" if page == 1 else f"{EQS_PAGE.format(n=page)}?{q}")
    html = get(url)
    rows = []
    for isin, dtxt, typ, comp, head in _EQS_ITEM.findall(html):
        try:
            ts = datetime.strptime(dtxt.strip(), "%d %B %Y").date().isoformat()
        except ValueError:
            continue
        rows.append((isin, ts, typ.strip(), comp.strip(), head.strip()))
    return rows, url


LEGAL_RE = re.compile(r"(?i)\b(AG|SE|KGaA|KG|GmbH|Co|Holding|Holdings|Group|Gruppe|"
                      r"S\.?A\.?|N\.?V\.?|PLC|Inc|Vorzugsaktien|St)\b\.?")


def de_query(name):
    """The search word EQS actually answers, which is NOT the issuer's legal name.

    `searchword=HORNBACH Holding AG & Co. KGaA` returns **zero** rows; `HORNBACH`
    returns 25 and `Hornbach Holding` returns the same 25. The search is an AND over
    words, so every legal-form token and every ampersand narrows it to nothing. This
    cost a whole measurement run: nine German vendor rows all resolved `null` and
    looked like a coverage problem when they were a query problem. Two distinctive
    tokens, no punctuation.
    """
    s = LEGAL_RE.sub(" ", name or "")
    s = re.sub(r"[^A-Za-z0-9\u00c0-\u024f ]", " ", s)
    toks = [w for w in s.split() if len(w) > 1]
    return " ".join(toks[:2]) or (name or "").strip()


def de_issuer(query, since=None, until=None, max_pages=6, match=None):
    """Every EQS release for one issuer, newest first, optionally windowed.

    `query` is an ISIN where one is known and the company name otherwise; a name search
    returns other issuers' rows too, so `match` (a normalised name) filters them out
    rather than letting one issuer's stream contaminate another's.
    """
    out = []
    q = (query if re.fullmatch(r"[A-Z]{2}[A-Z0-9]{10}", (query or "").strip())
         else de_query(query))
    for pg in range(1, max_pages + 1):
        rows, url = _eqs_search(q, pg)
        if not rows:
            break
        stop = False
        for isin, ts, typ, comp, head in rows:
            if since and ts < since:
                stop = True
                continue
            if until and ts > until:
                continue
            if match and norm(comp) != match and not norm(comp).startswith(match):
                continue
            out.append(_row("de", comp, isin if isin.startswith(("DE", "LU", "AT", "NL",
                                                                "CH", "FR", "IE", "GB"))
                            else None, ts, head, typ,
                            typ in DE_RESULTS_TYPES or looks_like_results(head),
                            "issuer_category" if typ in DE_RESULTS_TYPES else "headline",
                            url))
        if stop:
            break
    return out


def de_day(day, issuers, max_pages=6):
    """The German day archive, assembled issuer by issuer.

    There is no all-issuers-on-a-date query on EQS, so the caller says which issuers to
    look at -- for confirmation that is the day's scheduled names, for a stream
    measurement it is the whole market. One request per issuer per page.
    """
    out = []
    for q, name in issuers:
        out.extend(de_issuer(q, since=day, until=day, max_pages=max_pages,
                             match=norm(name) if name else None))
    return out


# --- Nordics: SE / DK / FI on one Nasdaq feed ------------------------------------
NASDAQ_API = ("https://api.news.eu.nasdaq.com/news/query.action"
              "?type=json&showCompany=true&limit=200&start={start}")
# The feed's own `market` labels, measured 2026-09-19. It carries the Baltics and
# Iceland on the same endpoint, so a market filter is required or a Estonian print would
# confirm a Swedish name. First North is the growth segment of each country and is kept:
# a First North issuer that clears $200k/day is a legitimate row of this stage's
# universe, and excluding it here would make confirmation fail for names the universe
# accepted.
NASDAQ_MARKETS = {
    "se": ("Main Market, Stockholm", "First North Sweden"),
    "dk": ("Main Market, Copenhagen", "First North Denmark"),
    "fi": ("Main Market, Helsinki", "First North Finland"),
}
# The issuer's own disclosure category, where it is a periodic results filing. Matched
# case-insensitively because the feed writes the same category both ways -- `Half Year
# financial report` and `Half year financial report` both occur in one week's rows.
#
# `Financial Calendar` is deliberately NOT here. It is the announcement of a future
# publication date, the Nordic analogue of EQS's `Advance financial reports`, and
# counting it as results would confirm a print on the day the company said when the
# print would be.
NASDAQ_RESULTS_CATEGORIES = {
    "half year financial report", "half-yearly information",
    "interim report (q1 and q3)", "interim report", "quarterly report",
    "financial statement release",          # the Finnish term for the full-year result
    "annual financial report", "annual report",
}
# Oslo publishes English category labels on every row. Norway's Q1/Q3 reports are not
# mandated by the Transparency Directive and do not get their own category, so they
# arrive as inside information or as additional regulated information and are caught by
# the headline classifier instead -- which is why `looks_like_results` still runs for
# Norway even though its categories are good.
OSLO_API = ("https://api3.oslo.oslobors.no/v1/newsreader/list"
            "?fromDate={d}&toDate={d}")
OSLO_RESULTS_CATEGORIES = {
    "half year financial report", "annual financial report", "quarterly report",
}
# --- Italy -----------------------------------------------------------------------
# eMarket STORAGE is Borsa Italiana's officially appointed storage mechanism. Its Drupal
# view takes `data_from` and `data_to` as ISO dates, and **`data_to` IS EXCLUSIVE**:
# `data_from=2026-09-17&data_to=2026-09-17` returns ZERO rows and looks exactly like a
# day on which nothing was published, while `data_to=2026-09-18` returns the 19 rows
# that really exist. That single off-by-one would have written `event_occurred: false`
# for every Italian name ever hunted.
EMS_DAY = ("https://www.emarketstorage.com/it/comunicati-finanziari"
           "?data_from={d}&data_to={nxt}&page={page}")
EMS_MAX_PAGES = 8


def _get_retry(url, tries=8, min_bytes=1, timeout=45):
    """Fetch through a WAF that answers intermittently.

    CONSOB and eMarket STORAGE both sit behind Radware, which serves a ~15 kB captcha
    page instead of the document on a share of requests -- measured 7 of 8 good for
    emarketstorage and 2 of 5 for the CONSOB landing page on 2026-09-19. A single
    failure here is not evidence of anything, and this repo has twice declared a host
    blocked after four tries and been wrong. Returns "" when every try fails, so the
    caller reports an unavailable archive rather than an empty day.
    """
    for i in range(tries):
        try:
            body = get(url, timeout=timeout)
        except Exception:
            body = ""
        if body and len(body) >= min_bytes and "Radware" not in body[:2000]:
            return body
        time.sleep(2 + 2 * (i % 3))
    return ""


def nasdaq_day(d, market, max_pages=None):
    """Every Nasdaq Nordic disclosure for `market` on `d`, by paging back to it.

    **THE DATE FILTER ON THIS ENDPOINT IS ACCEPTED AND IGNORED.** `fromDate=2026-08-14`
    returns the most recent 200 items, dated today. That is the most dangerous kind of
    failure in this stage -- a successful-looking request whose rows are for the wrong
    day -- so the date is never passed and the feed is PAGED instead, 200 rows at a time,
    until its rows are older than the day wanted. Measured: `start=1000` reached 12 days
    back, so a week costs about 7 requests.

    Returns `None` (not an empty list) when the feed could not be paged back far enough,
    because "I could not see that day" and "that day was empty" are the two answers this
    stage may never confuse.
    """
    max_pages = max_pages or NASDAQ_MAX_PAGES
    want = set(NASDAQ_MARKETS.get(market, ()))
    out, reached = [], False
    for page in range(max_pages):
        try:
            data = json.loads(get(NASDAQ_API.format(start=page * 200), timeout=60))
            items = data["results"]["item"]
        except Exception:
            break
        if not items:
            break
        for x in items:
            ts = (x.get("published") or "")[:10]
            if ts < d:
                reached = True                  # paged past the day: it was covered
                continue
            if ts != d or x.get("market") not in want:
                continue
            cat = (x.get("cnsCategory") or "").strip()
            by_cat = cat.lower() in NASDAQ_RESULTS_CATEGORIES
            head = x.get("headline") or ""
            out.append(_row(market, x.get("company"), None, ts, head, cat,
                            by_cat or looks_like_results(head),
                            "issuer_category" if by_cat else "headline",
                            x.get("messageUrl")))
        if reached:
            break
    return out if reached else None


def oslo_day(d):
    """Every Oslo Bors NewsWeb message on `d`. A real day query, and ticker-keyed.

    The best-instrumented archive of the ten after Investegate: `fromDate`/`toDate`
    genuinely filter, and every row carries `issuerSign`, the exchange ticker, so
    Norwegian confirmation joins on a code rather than on a normalised company name --
    the weakest link everywhere else in this stage.
    """
    try:
        data = json.loads(get(OSLO_API.format(d=d), timeout=45))
        msgs = (data.get("data") or {}).get("messages") or []
    except Exception:
        return None
    out = []
    for m in msgs:
        cats = [c.get("category_en") or "" for c in (m.get("category") or [])]
        by_cat = any(c.strip().lower() in OSLO_RESULTS_CATEGORIES for c in cats)
        head = (m.get("title") or "").strip()
        out.append(_row("no", m.get("issuerName"), None,
                        (m.get("publishedTime") or "")[:10], head,
                        " / ".join(cats),
                        by_cat or looks_like_results(head),
                        "issuer_category" if by_cat else "headline",
                        f"https://newsweb.oslobors.no/message/{m.get('messageId')}",
                        ticker_hint=(m.get("issuerSign") or "").upper() or None))
    return out


def it_day(d, max_pages=EMS_MAX_PAGES):
    """Every eMarket STORAGE filing on `d`. Behind a WAF, so retried, and `data_to` is
    EXCLUSIVE -- see EMS_DAY."""
    nxt = (date.fromisoformat(d) + timedelta(days=1)).isoformat()
    out, seen, any_page = [], set(), False
    for page in range(max_pages):
        html_ = _get_retry(EMS_DAY.format(d=d, nxt=nxt, page=page), min_bytes=15000)
        if not html_:
            # Distinguish "the WAF beat us on page 0" from "there are no more pages":
            # only a failure on the FIRST page makes the day unreadable.
            if page == 0:
                return None
            break
        any_page = True
        rows = re.findall(r'<div class="views-row">(.*?)(?=<div class="views-row">'
                          r'|<div class="view-footer|$)', html_, re.S)
        if not rows:
            break
        before = len(seen)
        for r in rows:
            when = re.search(r'class="datetime">(\d{2})/(\d{2})/(\d{4})', r)
            comp = re.search(r'news-azienda"><a[^>]*>([^<]*)', r)
            pdf = re.search(r'href="(/sites/default/files/comunicati/[^"]+)"', r)
            if not comp:
                continue
            ts = (f"{when.group(3)}-{when.group(2)}-{when.group(1)}" if when else d)
            # The headline is the row text once the logo/company block is stripped.
            body = re.sub(r'<div class="azienda-wrapper".*?</div></div>', ' ', r,
                          flags=re.S)
            head = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ",
                                                            body))).strip()
            key = (comp.group(1).strip(), head[:120])
            if key in seen:
                continue
            seen.add(key)
            if ts != d:
                continue
            out.append(_row("it", comp.group(1).strip(), None, ts, head, None,
                            looks_like_results(head), "headline",
                            ("https://www.emarketstorage.com" + pdf.group(1))
                            if pdf else EMS_DAY.format(d=d, nxt=nxt, page=page)))
        if len(seen) == before:
            break
    return out if any_page else None


def day(market, d, issuers=None):
    """The day archive for one market, or None where none is reachable.

    None and [] are different answers and the difference is the whole point: [] means
    the source was read and carries nothing from anybody, None means the source could
    not be read. Only the first can ever support `event_occurred: false`.
    """
    if market == "uk":
        return uk_day(d)
    if market == "fr":
        return fr_day(d)
    if market == "de":
        return de_day(d, issuers or [])
    if market in NASDAQ_MARKETS:
        return nasdaq_day(d, market)
    if market == "no":
        return oslo_day(d)
    if market == "it":
        return it_day(d)
    if market in ("es", "pl"):
        # Measured 2026-09-19, with the eight-try standard that rescued France and
        # Italy: every CNMV `Consulta-OIR` path returns 403, and `www.gpw.pl` and
        # `espi.pap.pl` each scored 0 of 8 on the sweep where emarketstorage scored 7
        # of 8. So these two have no archive and every row from them resolves null.
        return None
    raise ValueError(market)


# The markets whose archive carries a TICKER, so confirmation can join on a code rather
# than on a normalised company name. Name matching is the weakest link in this stage --
# `norm()` strips legal forms and compares exactly, so a register spelling that differs
# by one word reads as silence -- and these two escape it.
TICKER_KEYED = {"uk", "no"}


def confirm(market, d, issuer_name, ticker=None, archive=None, issuer_query=None):
    """Did THIS issuer announce results on THIS date? The three-state answer.

    True  a results-classified announcement from this issuer on the date.
    None  the issuer announced something that did not classify, or the source could not
          be read. Never a kill: `announced_unclassified` is a human call, and an
          unreadable source is not evidence of absence -- the rule this repo adopted
          after TRT.
    False the source WAS read, carries the day, and this issuer is not in it at all.
    """
    if archive is None:
        archive = day(market, d, issuers=[(issuer_query or issuer_name, issuer_name)]
                      if market == "de" else None)
    if archive is None:
        # Three different causes, one answer: Spain and Poland have no archive at all,
        # the Nasdaq feed could not be paged back to the day, or the Italian WAF won
        # every retry. None of them is evidence that nothing was published.
        return None, ("source unavailable: " + (MARKETS.get(market, {})
                                                .get("confirm_name") or "no archive"))
    key = norm(issuer_name)
    mine = [r for r in archive
            if (ticker and r.get("ticker_hint") and
                r["ticker_hint"].upper() == str(ticker).upper())
            or (key and r["issuer_norm"] and
                (r["issuer_norm"] == key or r["issuer_norm"].startswith(key)
                 or key.startswith(r["issuer_norm"])))]
    if not mine:
        if market == "de":
            # EQS is searched per issuer, so "not found" can mean the search term
            # missed rather than that nothing was published. That is not a kill.
            return None, ("no EQS release found for this issuer on the date; EQS is "
                          "searched per issuer, so a name that does not match its EQS "
                          "spelling looks identical to silence")
        if market == "it":
            # MEASURED 2026-09-22. eMarket STORAGE is Borsa Italiana's appointed storage
            # mechanism but not the only authorised one, and it does not carry every
            # issuer: PHILOGEN is absent from its `azienda` dropdown, and day queries on
            # three dates it is known to have filed (2025-09-23, 2026-03-27, 2026-08-17)
            # returned 33, 99 and 24 rows with no Philogen row on any. The archive read
            # fine each time, so absence here is NOT silence, and killing on it is the
            # TRT mistake inverted -- retiring a name that did report. Two exchange-side
            # substitutes answered first try and are where an Italian check should go:
            # borsaitaliana.it/azioni/documenti/calendariobilancidividendi/CDA_today.pdf
            # (forward board meetings, every issuer) and the per-ISIN news list.
            return None, ("eMarket STORAGE carries the day and not this issuer, which "
                          "for Italy is NOT a kill: the mechanism is not universal "
                          "across Italian issuers (measured 2026-09-22 on PHILOGEN, "
                          "absent on three known filing dates). Check Borsa Italiana's "
                          "own CDA list or the per-ISIN news feed by hand.")
        return False, f"{MARKETS[market]['confirm_name']} carries the day and not this issuer"
    hit = next((r for r in mine if r["is_results"]), None)
    if hit:
        return True, (f"{hit['classified_by']}: {hit.get('category') or ''} "
                      f"| {hit['headline'][:90]}")
    return None, ("announced_unclassified: this issuer published on the day and nothing "
                  "matched the results classifier. A human call, not a kill -- read it: "
                  + " | ".join(r["headline"][:70] for r in mine[:3]))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("market", choices=["uk", "de", "fr", "se", "dk", "no",
                                       "fi", "it", "es", "pl"])
    ap.add_argument("--date", required=True, help="the day to read, or the FIRST day "
                                                  "with --days")
    ap.add_argument("--days", type=int, default=1)
    ap.add_argument("--issuer", action="append", default=[],
                    help="DE only: an issuer name or ISIN to search (repeatable)")
    ap.add_argument("--results-only", action="store_true")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    d0 = date.fromisoformat(a.date)
    all_rows = []
    for k in range(a.days):
        d = (d0 + timedelta(days=k)).isoformat()
        rows = day(a.market, d, issuers=[(x, x) for x in a.issuer])
        if a.results_only:
            rows = [r for r in rows if r["is_results"]]
        print(f"{d}: {len(rows)} rows, "
              f"{sum(1 for r in rows if r['is_results'])} results, "
              f"{len({r['issuer_norm'] for r in rows})} issuers")
        for r in rows[:200] if a.days == 1 else []:
            flag = "R" if r["is_results"] else " "
            print(f"  {flag} {(r['issuer'] or '')[:28]:<28} "
                  f"{(r['category'] or '')[:34]:<34} {r['headline'][:60]}")
        all_rows.extend(rows)
    if a.out:
        Path(a.out).write_text(json.dumps(all_rows, ensure_ascii=False, indent=1) + "\n",
                               encoding="utf-8")
        print(f"-> {a.out}")


if __name__ == "__main__":
    main()

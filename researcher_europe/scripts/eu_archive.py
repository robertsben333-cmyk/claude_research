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

This module is that instrument for the other two. It is deliberately NOT three scrapers
with three shapes: every market returns the same row --

    {market, issuer, isin, ticker_hint, ts, headline, category, is_results,
     classified_by, url}

-- so `eu_resolve.py` confirms three markets through one code path and a measurement
written for one market runs on all three.

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

CLASSIFICATION IS REPORTED, NEVER ASSUMED
-----------------------------------------
Every row says how it was classified: `issuer_category` where the source publishes the
issuer's own filing category (France only) and `headline` everywhere else. A caller that
wants to know how much of its confirmation rests on a keyword list can count them. And
a row that is not classified as results is still returned -- `announced_unclassified` is
a human call, not an automatic kill, exactly as for the UK.
"""
import argparse
import json
import re
import subprocess
import sys
import urllib.parse
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eu_market import MARKETS                                        # noqa: E402

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


def day(market, d, issuers=None):
    if market == "uk":
        return uk_day(d)
    if market == "fr":
        return fr_day(d)
    if market == "de":
        return de_day(d, issuers or [])
    raise ValueError(market)


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
        return None, "source unavailable"
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
    ap.add_argument("market", choices=["uk", "de", "fr"])
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

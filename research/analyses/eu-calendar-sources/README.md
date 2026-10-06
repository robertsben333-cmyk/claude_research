# Stage EU's calendar misses most reporters: what was measured and what fixes it

**Question.** On 2026-10-05 the operator saw many UK companies reporting on investing.com
that stage EU's universe did not carry. How much does the vendor calendar
(TradingView's scanner, `earnings_release_next_date`) miss, why, and what free sources
fill the gap in each of the ten markets?

**Headline.** The vendor's RECALL had never been measured (SUBMARKET.md's 2.2% UK phantom
rate is PRECISION). Over 2026-09-22 -> 10-05 it carried **45 of 126** UK equity results and
trading updates above ~$100k/day that Investegate's RNS record shows actually happened,
and it was sealed on 0 of the 4 that landed on 10-05. The mechanism, seen cleanly in
Germany: for many issuers the vendor skips the Q1/Q3 statement or trading update and dates
the next FULL report.

**What was shipped (branch `claude/clever-gates-as6min`, 2026-10-06).**

| source | markets | what it adds | file |
|---|---|---|---|
| issuer-dated RNS notices + financial calendars, off Investegate | uk | 43 of 126 alone; vendor+RNS **53 of 126**; 49 of 64 RNS-dated rows reported on the day | `researcher_europe/scripts/uk_rns_calendar.py`, table in `researcher_europe/analysis/uk-rns-calendar.json` |
| Yahoo v7 `quote` `earningsTimestamp`, FIRM dates only | all ten | ~32 names over seven sample dates (10-07..11-05), about 4-5 a day | `researcher_europe/scripts/eu_yahoo_calendar.py` |

Both merge in `eu_universe.py`; every row carries `calendar_source`
(`vendor`, `rns`, `yahoo`, `vendor+rns`, `vendor+yahoo`...), and `--no-rns --no-yahoo`
rebuilds the vendor-only universe every run before 2026-10-06 used.

## The UK measurement

`python3 researcher_europe/scripts/uk_rns_calendar.py measure --from 2026-09-22 --to 2026-10-05`.
Truth is every Investegate RNS that `eu_archive.looks_like_results` classifies as results,
minus notices/presentations/AGM results, for an EPIC in the vendor's primary-equity UK
universe with 10-day turnover at or above $100k. An RNS-dated row counts only if the
announcement dating it was published before 14:30 London on the business day before (the
13:30 UTC seal).

| | caught |
|---|---|
| vendor (as sealed in each day's `universe.json`) | 45 / 126 |
| RNS calendar alone (crawl from 2026-03-02) | 43 / 126 |
| either | 53 / 126 |

Extending the crawl from 2026-07-20 back to 2026-03-02 moved the RNS figure from 40 to 43:
**most missed issuers published nothing dated in the seven months before reporting**
(checked by searching every cached body of each missed EPIC for the event date). That is a
ceiling on this route, not a parser gap. The remaining misses are mostly AIM interims
(CKT, FAR, ROCK, TRP, AVCT, BZT) and trading updates (HLMA, AO., SSE, WPP, SRE, QTX)
whose dates live on company websites or are never announced.

**What does not work for the UK:** investing.com (Cloudflare bot wall; a TLS-impersonating
client also 403; a headless browser was refused by the session's permission classifier and
not pursued), lse.co.uk, sharecast, proactiveinvestors, ADVFN, MarketScreener,
directorstalk (403), digitallook (502), Shares/AJ Bell diary (redirect, no data).

## Not yet built, ranked (from the source probe below)

1. **Germany, EQS events search** -- ISIN-keyed, typed, issuer-entered, ~9 pages for all 753
   forward events; adds 1-3 liquid names a day in late October and 6 on 11-12.
2. **Poland, bankier.pl kalendarium** -- the issuers' statutory January schedules; needs a
   bankier-name -> GPW ticker map. Past week 09-24..09-30: vendor had no date for 4 of 15
   liquid names bankier scheduled.
3. **Norway, Euronext Oslo financial-events** -- 813 future events, roughly the vendor's
   coverage, with issuer dates that disagree with it on a few names.
4. **Finland, Inderes calendar** -- adds the Q1/Q3 business reviews the vendor lacks.
5. **Add `isin` to `TV_COLUMNS`** -- returned on 431 of 431 German rows; exact joins instead
   of name normalisation.
6. **Fix the resolver's classifier:** `eu_archive.looks_like_results` does not apply
   `eu_priced_in.NOTICE_RE`, so "Invitation to Q3 presentation" counts as a results release
   in the Nordic and Oslo archives.

France, Italy and Spain have no free forward source other than Yahoo that answered.

**Not measured:** past-day recall of Yahoo, EQS, bankier, Euronext Oslo and Inderes (each
was compared with the vendor forward, not against a resolved day). The first stage EU runs
under the merged universe are that measurement: split `eu_resolve.py` by
`calendar_source`.

---

# Appendix: the source probe (2026-10-06, verbatim)

## Forward earnings-date sources for stage EU (de fr se dk no fi it es pl)

Measured 2026-10-06 by a subagent from this container through the agent proxy, with curl (the repo's
`fetch` pattern). Every count below comes from a request made today. Scripts and raw JSON
are in a session scratchpad (not kept): `tv.py`, `yq.py`, `oslo_fe.py`, `bankier.py`, `eqs_ev.py`,
`de_cmp.py`, `pl_cmp.py` and `recall.py`. The repo was not modified.

"Liquid" means the TradingView row's `average_volume_10d_calc × close × fx` is at least
$100k a day, which is the non-US floor. Name joins are fuzzy unless they say ISIN.

## Headline findings

1. **Why TradingView misses names: for many issuers it skips the Q1/Q3 *quarterly
   statement* and dates the next FULL report.** Germany shows it cleanly. Taking the earliest
   EQS reporting event per ISIN against TV `earnings_release_next_date`, 188 dates are the
   same, 31 differ and 18 have no TV date. Nearly every difference is TV pointing at
   Feb–Apr 2027 while the issuer has a Q3 statement in Oct/Nov: Beiersdorf 10-27 (TV
   2027-03-04), Symrise 10-28, MTU 10-29, DWS 10-28, Delivery Hero 10-28, Heidelberg
   Materials 11-04, Scout24 11-04, Fielmann 11-05, flatexDEGIRO 10-21, ATOSS 10-23, and
   others. The same shape shows in FR (BNP 10-28 vs TV 2027-02-02), IT, ES and NO (Orkla,
   Aker). Finland's "business reviews" (Q1/Q3 liiketoimintakatsaus) are missing from TV for
   the same reason. This is very likely the mechanism behind the UK ~35%: trading updates and
   interim statements are not "earnings" to the vendor.
2. **TradingView's scanner exposes an `isin` column.** Adding `"isin"` to `TV_COLUMNS`
   returned an ISIN on 431 of 431 German rows. That allows exact joins with EQS, AMF and
   Euronext data, instead of the name normalisation `eu_archive.confirm()` currently relies on.
3. **Yahoo per-symbol dates (v7 `quote`, batched) are the cheapest broad complement**, and
   they carry many of the Q3 dates TV skips. The Yahoo screener calendar is useless (see
   below).

## Per-source results

### Yahoo `v1/finance/visualization` (entityIdType earnings): NOT USABLE
- HTTP 200 JSON with a crumb (the repo's crumb flow; first try answered "Too Many
  Requests" and a retry worked). Including `epsestimate` and similar fields in
  `includeFields` gave HTTP 500 "OpenSearch IOException"; a minimal field list works.
- Whole-world totals: 25 events on 2026-10-15, 5 on 10-21, 29 on 10-22, **0** on 10-06,
  10-07, 10-01, 09-24 and 09-30. The rows are US-bank earnings *calls* (USB, FITB, HBAN)
  plus their cross-listings (.F, .MI, .L). Zero European primary listings. Dead end.

### Yahoo `v7/finance/quote?symbols=…` (fields `earningsTimestamp[Start|End]`, `isEarningsDateEstimate`): USEFUL COMPLEMENT
- HTTP 200 JSON, 150 symbols per call. **The whole 9-market TV universe (3,414 symbols)
  took 18 s.** `quoteSummary?modules=calendarEvents` returns the same dates per symbol
  (checked on 9 bellwethers) but costs one call per name.
- Coverage of the TV universe (symbols with any earningsTimestamp): de 185/430, fr
  132/587, se 245/666, dk 55/135, no 134/275, fi 84/182, it 80/387, es 54/279,
  pl 35/473. The dates can be stale: MC.PA still shows 2026-07-27. The time-of-day is
  often a 15:30 UTC placeholder, so it does not give a session.
- **Liquid names with a date 2026-10-06…11-30:**

| mkt | TV | Yahoo | both | **Yahoo-only** | TV-only |
|---|---|---|---|---|---|
| de | 153 | 143 | 125 | **18** (DWS, Fielmann, EKT, GIL…) | 28 |
| fr | 38 | 39 | 25 | **14** (BNP, Crédit Agricole, Amundi, Ipsen…) | 13 |
| se | 269 | 197 | 191 | 6 (EQT, Bure, Lundbergs…) | 78 |
| dk | 43 | 38 | 36 | 2 | 7 |
| no | 128 | 88 | 85 | 3 (Aker, Orkla, SmartOptics) | 43 |
| fi | 66 | 57 | 53 | 4 | 13 |
| it | 72 | 56 | 36 | **20** (Reply, Ariston, Italmobiliare, Campari…) | 36 |
| es | 38 | 22 | 16 | 6 (Acerinox, Redeia, Meliá, CIE) | 22 |
| pl | 83 | 27 | 26 | 1 | 57 |

  On single near dates Yahoo is mostly a subset of TV. On 10-22 for se: TV 69, Yahoo 46,
  both 44. They probably share an upstream vendor for the names they both carry.
- Integration cost: very low. `eu_priced_in.crumb()` and `eu_market.yahoo_symbol()`
  already exist.

### Germany: EQS events search: BEST DE SOURCE
- `https://www.eqs-news.com/search-results/[page/N/]?searchtype=events&searchword=a&pageLimit=100`.
  HTTP 200, server-rendered HTML with no challenge. Each item carries `data-events-isin`,
  `data-events-category`, a date, the company and a title. Nine pages of 100 cover the
  whole forward list: 802 events for "a" and 801 for "e", 753 unique across both. The range
  is 2026-10-06 to 2028-01-13. ISINs: 585 DE, 86 CH, 24 AT, 24 LU, a handful of others.
- Categories are issuer-entered and typed: 145 "Publication quarterly statement
  (call-date Q3)", 94 "quarterly financial report (Q3)", 55 annual, 40 half-yearly, plus
  "Press Release – …", AGMs and roadshows. There is no time of day.
- 442 reporting events (dedup by ISIN and date); 351 have a DE ISIN and 350 join TV `germany` by ISIN.
- Per date, liquid, ISIN-joined:

| date | EQS liquid | TV liquid | both | EQS-only | TV-only |
|---|---|---|---|---|---|
| 10-20 | 2 | 1 | 1 | 1 | 0 |
| 10-21 | 3 | 1 | 1 | 2 | 0 |
| 10-22 | 3 | 2 | 1 | 2 | 1 |
| 10-28 | 7 | 4 | 4 | 3 | 0 |
| 10-29 | 10 | 10 | 9 | 1 | 1 |
| 11-05 | 25 | 26 | 23 | 2 | 3 |
| 11-12 | 46 | 43 | 40 | 6 | 3 |

- Caveats: only issuers that use EQS IR. Past-date recall was not tested, because the
  "Past" sort exists but was not scraped.
- Integration cost: low. One parser over about 9 pages.

### Germany: other sites
- boerse.de/termine/: 200, HTML, a short mixed list dominated by large caps and foreign
  names (Agrana, TSMC, SAP, L'Oréal…). Not counted.
- wallstreet-online.de/unternehmenstermine: 200, 2.9 MB, shows today's events only (38
  items). Date paging not tested. The "Radware" string on that page is a stock name, not a WAF.
- finanzen.net/termine/: 200 (served content; the "captcha" match was a false positive in
  scripts). /termine/quartalszahlen returned 404. Not parsed further.
- boerse-stuttgart.de/…/termine: **403 Cloudflare "Just a moment"**, so unreachable.
- boerse-frankfurt.de/unternehmenskalender, onvista /termine, ariva /aktien/termine,
  finanznachrichten termine, eqs-news /finanzkalender/: all 404 at the URLs tried.

### Norway: Euronext Oslo "Financial calendars": GOOD
- `https://live.euronext.com/en/markets/oslo/equities/financial-events?field_ofe_event_from_date_value=2&page=N`
  (2 = future events). HTTP 200, a Drupal HTML table (date, issuer, event), no challenge.
  18 pages gave **813 future events** running to 2026-12-31: 347 "Quarterly Report – Q3",
  159 Q4, 111 Annual Report, 57 Half-yearly, and others. Bond-only issuers are included
  (Avinor, savings banks). The "Past month" filter (value 4) returned no table.
- Against TV for the same dates (reports only, fuzzy names; issuers in TV's universe):
  10-15 Euronext 2 / TV 1 (+NEL); 10-20 3/3; 10-21 2 of TV's 5 matched (TV has NEL on
  10-21 where Euronext says 10-15); 10-22 Euronext 10 / TV 8, all 8 matched, +EAM Solar and
  Yara (TV dates Yara 10-23); 10-23 Euronext 4, TV 9, 4 matched. So it roughly equals TV,
  with issuer-sourced dates that disagree with TV on a few names.
- **The same view does not exist for Paris or Milan** (`/markets/paris|milan/equities/financial-events`
  returned 404). Per-issuer `/product/equities/<ISIN>-XPAR/financial-calendar` returned
  200 for LVMH but with **2005** data, so it is stale. For an Italian ISIN on XMIL it
  returned "Instrument not found".
- Integration cost: low.

### Poland: bankier.pl kalendarium: GOOD (only working PL source found)
- `https://www.bankier.pl/gielda/kalendarium/?eventType=10&navigation_type=week&navigation_start=<epoch seconds>`
  (10 = "Wyniki spółek"). HTTP 200, server-rendered HTML, no challenge. Results events per
  week: 09-21 69, 09-28 113, 10-05 0, 10-12 1, 10-19 2, 10-26 38, 11-02 43, 11-09 190,
  11-16 254, 11-23 138. Entries read like "Publikacja raportu za III kwartał 2026". Polish
  issuers must publish their periodic-report schedule in January, so the dates are
  issuer-sourced. The symbol is bankier's own short name (PKNORLEN, DINOPL), not the GPW
  ticker. There is no time of day.
- Forward, adjudicated by hand because the automatic name join failed on PKOBP, PKNORLEN
  and similar: TV liquid on 11-05 is 8; bankier has 6 of them that day, and Eurocash and
  Mostostal Zabrze are on 11-19. TV liquid on 11-19 is 14; bankier has 13 (all but
  UNIMOT), plus extras such as Eurocash, Kinopol and Ryvu.
- Past 09-24…09-30: bankier scheduled 15 liquid names (Pepco/Polenergia excluded as a
  mapping error). **TV's last-release date matches on 6. Four have no TV date at all**
  (Arlen, Robyg, MultiQure, OneMore), and five have a different TV date. This cannot be
  checked against actual filings, because the repo has no PL archive (GPW/ESPI blocked).
- stooq.pl/kal/ returned 404. strefainwestorow returned 404 at the URL tried.
- Integration cost: moderate. It needs a bankier-name→GPW map; the per-company page
  `/gielda/notowania/akcje/<NAME>/kalendarium` gives the link.

### Finland (and partly the Nordics): Inderes calendar: GOOD FOR FI
- `https://www.inderes.fi/en/markets/calendar`: 200. `__NEXT_DATA__` JSON with typed
  events (INTERIM_REPORT, BUSINESS_REVIEW, ANNUAL_REPORT, dividends) and period labels. The
  server-rendered page holds 200 events (2026-10-06…2027-01-26, `hasNextPage: true`) for
  region FINLAND by default. `?region=SWEDEN` / `?regions=SWEDEN` did not switch region, so
  Sweden, Denmark and Norway would need its GraphQL paging, which was not found or tested.
- FI against TV (fuzzy names): 10-21 Inderes 8 / TV 4, Inderes-only Digital Workforce,
  LapWall, Vincit, Witted (business reviews); 10-22 15/12, Inderes-only Fondia and Reka,
  plus Tallink and Telia (foreign listings); 10-23 12/7, Inderes-only Apetit, LeadDesk,
  Rebl, Sotkamo Silver, Ålandsbanken. It covers only companies Inderes follows.
- Integration cost: low for FI (one page plus JSON); unknown for SE/DK/NO.

### Sweden, Denmark, Finland: Nasdaq Nordic
- Disclosure feed `api.news.eu.nasdaq.com/news/query.action?...&cnscategory=Financial%20Calendar`:
  200 JSON, and the category filter works. The items are issuers announcing their 2027
  calendars (Wärtsilä, DSV, SRV on 10-05). The dates are free text inside the release, so
  they need a parser. This is a slow-accumulating, authoritative source; coverage not counted.
- The nasdaqomxnordic.com/news/calendar page (200) is a JS shell. Guessed `api.nasdaq.com/api/nordic/*calendar*`
  paths returned 404 (`/api/nordic/search` works but is irrelevant). No working calendar API found.

### France, Italy, Spain
- **France:** no forward calendar found other than Yahoo (+14 liquid names). MarketScreener
  (Zonebourse) returned **403 challenge**. The Euronext Paris market-wide view returned 404
  and the per-issuer page is stale. Past recall of TV against the AMF archive (`eu_archive.day`,
  NOTICE_RE-filtered, liquid): **09-24 6/14, 09-30 1/≈8** (excluding Société Générale
  SFH/SCF mis-joins), **10-01 0/3, 10-02 1/2**. The misses were real H1 reports (Riber,
  Robertet, ABC Arbitrage, Peugeot Invest, STIF, Voyageurs du Monde, North Atlantic
  Energies), mostly with a stale or 2027 TV date.
- **Italy:** borsaitaliana.it `CDA_today.pdf` (the repo's noted substitute) now returns
  **404**, as do the guessed calendario URLs. Euronext Milan financial-events returned 404.
  Only Yahoo was tested working (+20 liquid). Past TV recall against eMarket STORAGE was
  0/2 on 09-30 at the liquid floor; the sample is too small to mean anything.
- **Spain:** eleconomista agenda returned **403 Akamai "Access Denied"**. bolsamania
  returned a challenge-platform script plus a 404 page. expansion calendar returned 404.
  infobolsa: the proxy tunnel closed mid-exchange. BME "Agenda Corporativa" returned 200
  but as a JS shell; no API was found. Only Yahoo (+6 liquid) works.

### Keyed / paid (not signed up)
- Finnhub `calendar/earnings` returned 401 without a key. EODHD, FMP and Wall Street
  Horizon are keyed or paid. investing.com was not tried, as instructed.

## Past-date TV recall (Nordics), with a warning about the archive classifier
`recall.py` on 09-24/09-30/10-01/10-02 for se/dk/fi/no gave tiny liquid samples (0–2 per
day). Most apparent misses were **archive false positives**: Swedish "Invitation to
presentation of Q3 report" headlines (Atrium Ljungberg, Enea), Orkla's "Jotun Interim
Report", a Stolt-Nielsen conference notice, and covered-bond issuers. **`eu_archive.looks_like_results`
does not apply `eu_priced_in.NOTICE_RE`**, so `is_results` overcounts invitations in the
Nasdaq/Oslo archives. Any recall figure built on `is_results` should filter notices first.

## Ranking per market (reachability, coverage, cost)

| mkt | 1st | 2nd | 3rd |
|---|---|---|---|
| de | EQS events search (ISIN, typed, issuer-entered) | Yahoo v7 quote | — (Stuttgart CF-blocked; others 404) |
| fr | Yahoo v7 quote | — (MarketScreener blocked; Euronext Paris view 404) | not found |
| se | Yahoo v7 quote (small add) | Nasdaq Nordic "Financial Calendar" releases (needs text parsing) | Inderes (SE region not reachable via SSR) |
| dk | Yahoo v7 quote (small add) | Nasdaq Nordic Financial Calendar releases | — |
| no | Euronext Oslo financial-events (813 future events) | Yahoo v7 quote | — |
| fi | Inderes calendar (adds business reviews) | Yahoo v7 quote | Nasdaq Nordic Financial Calendar releases |
| it | Yahoo v7 quote (+20 liquid) | — (Borsa Italiana PDFs/pages 404 today) | not found |
| es | Yahoo v7 quote (+6) | — (eleconomista Akamai 403, bolsamania challenge) | not found |
| pl | bankier.pl kalendarium (issuer schedules) | Yahoo (adds ~nothing) | — |

Suggested order of integration: (1) the Yahoo v7 batch across all nine markets, a few
lines, about 18 s; (2) EQS events for DE; (3) bankier for PL; (4) Euronext Oslo for NO;
(5) Inderes for FI. Add `isin` to `TV_COLUMNS` regardless.

Not tested: past-date recall for EQS events, bankier, Euronext Oslo and Yahoo (none of the
forward sources was checked against a resolved day except via TV); Inderes regions other
than Finland; the Nasdaq Nordic calendar-text parse; and BME's underlying API.

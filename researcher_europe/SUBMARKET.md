# Which European submarket, and should it be built at all

Phase 1 of stage EU. Everything below was measured from this container on 2026-09-18
against real sampled dates. Where a number could not be measured it says so and does
not guess. Korea was killed on counts; the same standard applies here.

**Verdict: build, all three pooled from day one, with a $1m/day turnover floor and no
size-band cut.** The pooled stream clears the Japan bar on a median day and does not
clear it on every day. Three conditions are named at the end; two of them are real and
one of them (the French short register) was unsolved when this was written.

**Three things changed on 2026-09-19 and this file was amended rather than rewritten.**
The floor is now **$200k**, on the operator's instruction, for cross-market
comparability and stream depth — see "What the $200k floor adds" in §1 for what that
buys and what it costs, both measured. **The French short register is solved**: §4
carries the working path. And **seven more markets were added** — Stockholm, Copenhagen,
Oslo, Helsinki, Milan, Madrid and Warsaw — measured in **§10, appended at the end**.
Everything else below stands as measured on 2026-09-18, and §10 does not overwrite it:
the verdict in this header was about the original three and is left as it was written.

---

## 1. Stream

### The UK, measured against the actual RNS record

The Investegate day archive (`/today-announcements/<YYYY-MM-DD>`, paginated, back to
1999) is a full mirror of RNS plus the EQS / GlobeNewswire / PR Newswire feeds, with a
per-announcement timestamp, the issuer's EPIC, and the headline. It is reachable from
this container and it is **historical**, which TDnet is not — TDnet keeps ~31 days and
Japan's confirmation therefore expires. Four weeks were scraped in full: one in-season
(2–6 March), two off-season (12–16 January, 15–19 June) and the current week
(14–18 September). 7,764 announcements in total.

| date | all announcements | results (one per issuer) | ex investment trust | Notice of Results |
| --- | --- | --- | --- | --- |
| 2026-01-12 | 383 | 10 | 8 | 3 |
| 2026-01-13 | 381 | 22 | 22 | 2 |
| 2026-01-14 | 369 | 22 | 21 | 1 |
| 2026-01-15 | 406 | 30 | 30 | 4 |
| 2026-01-16 | 311 | 4 | 4 | 1 |
| 2026-03-02 | 772 | 22 | 19 | 1 |
| 2026-03-03 | 434 | 21 | 19 | 6 |
| 2026-03-04 | 408 | 13 | 12 | 3 |
| 2026-03-05 | 465 | 35 | 32 | 10 |
| 2026-03-06 | 403 | 3 | 3 | 3 |
| 2026-06-15 | 419 | 7 | 7 | 0 |
| 2026-06-16 | 363 | 20 | 16 | 4 |
| 2026-06-17 | 382 | 16 | 12 | 1 |
| 2026-06-18 | 381 | 12 | 11 | 0 |
| 2026-06-19 | 352 | 6 | 5 | 0 |
| 2026-09-14 | 477 | 18 | 16 | 3 |
| 2026-09-15 | 401 | 34 | 32 | 5 |
| 2026-09-16 | 361 | 34 | 32 | 2 |
| 2026-09-17 | 398 | 38 | 31 | 8 |
| 2026-09-18 | 309 | 12 | 6 | 5 |

Median 17 results-type announcements a day ex funds; 15.4 a day carried a usable price
window. **The floor matters more than the median**: 2026-03-06 and 2026-01-16 carried
three and four. Fridays are the thin day in this market, every week sampled.

With a turnover floor applied to the 307 events that resolved to a price window
(`analysis/phase1-uk-moves.json`, turnover converted to USD at 1.34 GBP and computed as
the median of the 20 sessions before the print):

| floor | median names/day | min | max | days at zero |
| --- | --- | --- | --- | --- |
| $200k/day | 7 | 1 | 21 | 0 of 20 |
| $1m/day | 4 | 1 | 17 | 0 of 20 |
| $5m/day | 2 | 0 | 8 | 3 of 20 |

**The UK alone does not clear the Japan bar.** Japan's quietest sampled day carried 11
names on TDnet and still matched half the US stage's daily universe. The UK at the same
$200k capacity bar the US and Japanese stages use bottoms out at one name.

### Germany and France, and why the calendar instrument had to change

*(Phase 1, 2026-09-18. **Both halves of this paragraph were wrong and are corrected in
"The German and French day archives" below**, added 2026-09-19. Kept because the search
that failed is worth knowing about.)*

There is no Investegate for Germany or France. EQS-News (the DGAP successor) serves a
~60-item server-rendered snapshot of the live feed and **does not paginate** —
`?paged=2`, `/page/2/` and `?label=Reports` all return byte-identical listings — so it
is a same-day confirmation surface and not a day archive. The Börse Frankfurt API is
reachable (`equity_key_data` returns a full record) but `company_calendar`,
`company_dates` and `equity_master_data` all return `{}` for every ISIN and parameter
combination tried. Nothing equivalent to the UK archive was found for either market
inside this session's budget, and that is an open risk, written up in §6. **Both were
found on 2026-09-19** — the AMF's own flux for France and the EQS *search* for Germany.

What both markets do have is a forward vendor calendar. TradingView's public scanner
(`scanner.tradingview.com/<market>/scan`, POST, no key) returns for every primary
listing: last release date, next scheduled release date, a session flag, close,
currency, 10-day average volume, market cap and sector. Universe sizes with
`type = stock`: **Germany 427, France 591, UK 1,078.**

**Its accuracy was measured, not assumed.** 90 of its UK `earnings_release_date` rows
fall on the 20 days scraped above. 82 of them have a results RNS from the same issuer on
that exact day. Six of the eight misses are gaps in my own headline classifier, checked
by reading the announcements: Barratt Redrow filed "Barratt Redrow Full Year 2026
Results", Pollen Street "Interim Accounts H126", Duke Capital "Annual Financial Report",
Water Intelligence "Audited Results for Year Ended 31 December 2025", DXS International
a "Timing of…" delay notice, and Trustpilot headlined its interims **"AI, Enterprise and
US momentum fuel strong growth"** — a marketing headline with no results vocabulary in
it at all. Only two rows (ITM Power, Petra Diamonds) had no announcement of any kind.

So the vendor calendar's phantom rate on the UK is **2 of 90, 2.2%**, against the US
stage's `time-not-supplied` rate of 20 of 20 on 2026-09-17. That is a completely
different object and it is the single most encouraging access number in this file.
It does not remove the need for a confirmation source; TRT was a 33%-of-equity mistake
and `event_occurred: false` has to be reachable here too.

### The German and French day archives, built 2026-09-19

Phase 1 said there was no Investegate for Germany or France. There is one for each; both
were found by looking in a different place, and the French one is in some ways better
than Investegate.

**France — `info-financiere.gouv.fr`, the AMF's own regulated-information archive.**
An Opendatasoft API, no key, no cookie: dataset `flux-amf-new-prod`, **536,868 records
back to 2012**, current to yesterday, queryable by date range and by issuer. Between 42
and 152 filings a day on the twenty sampled days. It is the French RNS, and Phase 1's
"FR — nothing readable" was a statement about Euronext's SPA that was never tested
against the regulator's own archive.

It has something neither Investegate nor EQS has: **the issuer's own declared filing
category** on every record — *Rapports financiers et d'audit semestriels / annuels*,
*Information financière trimestrielle* — plus a second, finer label inside the title
field. That second label is the one that matters. A French results release is very often
filed as *Informations privilégiées* (inside information) rather than as a periodic
report, with the AMF's own sous-type in the title: **"Informations privilégiées /
Communiqué sur comptes, résultats"** — literally *news release on accounts, results*.
MedinCell, Theraclion, Implanet and Advicenne all filed exactly that, and a headline
keyword classifier reads it as no results vocabulary at all. Over the twenty sampled days
**78 of 178 results rows are classified by the issuer's category and 100 by headline**,
and four of the seven French rows that first measured `announced_unclassified` were
category rows the headline pass had missed.

**Germany — the EQS-News *search*, not its front page.** Phase 1 measured
`eqs-news.com/` — a ~60-item snapshot that genuinely does not paginate — and concluded
German confirmation expires after a day. The search does not have that limit:
`?searchtype=news&searchword=<issuer>`, paginated at `/search-results/page/<n>/`, 25
rows a page and **67 pages for a single mid-cap**, each row carrying the date, the EQS
news type, the company, the headline and the **ISIN**. German confirmation is historical
after all.

Two things it is not. It has **no whole-day query** — `searchword=` empty returns
nothing and a one-letter word returns a sparse subset — so the German day archive is
assembled issuer by issuer, which means `event_occurred: false` is unreachable for
Germany by construction: "not found" cannot be told from "search term missed". And its
news type is not a results category (`Corporate` covers both a results release and a
store opening), so German classification falls back to the headline. **Only France
escapes the headline classifier.**

**The search word is not the issuer's legal name.**
`searchword=HORNBACH Holding AG & Co. KGaA` returns **zero** rows; `HORNBACH` returns 25.
The search ANDs over words, so every legal-form token and every ampersand narrows it to
nothing. This cost a whole measurement run, in which nine German vendor rows all resolved
`null` and looked like a coverage problem.

### What the archives say about the phantom rate and the true stream

**Phantom rate, vendor rows checked against the archive.** The vendor's
`earnings_release_date` is the issuer's LAST release, so only recent dates carry many
rows; that is the same limitation Phase 1's UK measurement had.

| | vendor rows on the 20 sampled days | results confirmed | announced, not classified | published on a different day | nothing at all |
| --- | --- | --- | --- | --- | --- |
| UK (Phase 1) | 90 | 82 | 6 | — | **2 (2.2%)** |
| France | 17 | 12 | 3 | 1 (Hipay, filed its H1 the day before) | **1 (Guerbet, 5.9%)** |
| Germany | 6 | 2 | 1 | — | 3 **not found, which is not a phantom** |

France's phantom rate is **1 of 17** on a small sample, and the one date error is a
different failure from a phantom and is worth separating. Germany's cannot be measured
with this instrument at all: three of its six rows returned nothing from EQS, and since
EQS is searched per issuer that is indistinguishable from an issuer who does not
distribute through EQS.

Of the three French rows that did not classify, two are results a human reads
immediately — Robertet's *"UN PREMIER SEMESTRE 2026 SOLIDE"* and Vente-unique's
*"accélère sa dynamique de croissance rentable au 1er semestre"* — and one, Aelis Farma,
filed *"Informations privilégiées / Autres communiqués"*, which is genuinely not a
results filing. **So the classifier misses about 2 of 14 real French results releases,
and the AMF category rescues four that a headline pass would have lost.**

**True daily event count against the vendor's own count.** Both sides unfiltered — every
listed name, no turnover floor, one issuer counted once a day — and measured on the week
where the vendor's last-release field is current:

| week | market | vendor rows/day | archive results issuers/day | ratio |
| --- | --- | --- | --- | --- |
| 2026-09-14 → 18 | UK | 13.6 | 23.4 (Phase 1 table) | **1.7×** |
| 2026-09-14 → 18 | France | 2.8 | **10.0** | **3.6×** |
| 2026-09-14 → 18 | Germany | 0.6 | 1.6 | 2.7× (on 3 and 8 events) |
| 2026-08-10 → 14 (the German peak) | Germany | 13.8 | 10.8 | **0.78×** |

Over all twenty sampled days France runs a **median of 5 and a mean of 6.2 results
issuers a day** against the 0.9 a day the vendor-derived table above gives for names
above $1m — different bases, so not directly comparable, but the direction is not in
doubt.

**So the UK's 2.2× undercount generalises to France and does NOT generalise to
Germany.** France's contribution to the pooled stream is materially larger than this
file claimed; Germany's, measured in its own August peak week, is if anything *smaller*
than the vendor says — though the EQS instrument is a lower bound, since it sees only
issuers who distribute through EQS and matches on name. Germany's seasonality, not the
calendar's accuracy, is what makes it thin outside November and August.

**One operational finding that came out of the same work.** Yahoo's European daily
closes lag: on 2026-09-19 `.PA` and `.DE` symbols carried timestamps for 09-17 and 09-18
with **null closes**, on liquid names (MC.PA) as well as thin ones, and `.L` was one
session behind. **A European run cannot be resolved the morning after the print.**
`eu_resolve.py` now carries `last_bar_date` and `move_pending` per row and warns when
every row is pending, so that is never read as a day on which nothing moved.

### Cadence, and how staggered the year-ends really are

For every name carrying both a last and a next scheduled release, the gap between them:

| market | n | ≤100d (quarterly) | 101–200d (semi) | >200d | median gap |
| --- | --- | --- | --- | --- | --- |
| Germany | 259 | **156 (60%)** | 42 | 61 | **97 days** |
| France | 161 | 17 (11%) | 49 | 95 | 204 days |
| UK | 793 | 27 (3%) | 246 | 520 | 217 days |

The brief's prior is confirmed: **Germany is the quarterly market**, because Prime
Standard issuers still owe quarterly statements under the Börsenordnung where the
Transparency Directive floor is annual-plus-half-year. France and the UK are
semi-annual.

But quarterly is not the same as continuous, and the seasonality measurement is the one
that reverses the ranking. Next scheduled release by month, forward twelve months:

| | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr | May | Jun | Jul |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Germany (259) | 9 | 33 | **153** | 14 | 2 | 8 | 22 | 14 | 2 | 1 | 1 |
| France (161) | 26 | 16 | 15 | 4 | 2 | **56** | **38** | 3 | 1 | 0 | 0 |
| UK (807) | 127 | 65 | 141 | 91 | 23 | 69 | **191** | 51 | 26 | 18 | 5 |

**Germany reports quarterly and all at once.** 153 of 259 forward events are in
November; January, June and July carry two, one and one. That is the Korea failure mode
in milder form — quarterly frequency does not help if every issuer is a December
year-end reporting in the same fortnight. On 2026-11-12 the German calendar carries 52
names and on 2026-06-xx it carries one.

**The UK is the staggered one.** Every month carries a non-trivial count, because UK
year-ends really are spread across December, March, June and September. This is exactly
the property Korea and China lack, and it is the property that makes a *daily* stage
possible rather than a seasonal one.

France is the thinnest of the three on both axes: semi-annual, and 94 of 161 forward
events in February–March.

### Pooled

Annualising each name's cadence over the names that carry one, above a $1m/day turnover
floor:

| market | names ≥$1m/day | ann. events | per trading day |
| --- | --- | --- | --- |
| Germany | 129 | 456 | 1.8 |
| France | 113 | 234 | 0.9 |
| UK | 320 | 590 | 2.3 |
| **pooled** | **562** | **1,280** | **5.1** |

**Those figures are a floor, not an estimate**, because the vendor calendar undercounts.
On the 20 scraped days the UK's measured count above $1m/day was 5.05 events a day
against the 2.3 this table gives — a factor of 2.2. If Germany and France undercount
similarly, the pooled true stream above $1m/day is **roughly 8 to 12 names on a median
day**, and above $200k/day roughly 12 to 15.

**Measured on 2026-09-19, that guess was half right.** With day archives for all three
markets (see "The German and French day archives" below), France undercounts by
**3.6×** on the week where the comparison is clean and Germany does **not** undercount
at all — 10.8 measured results issuers a day against 13.8 vendor rows in its August peak
week. So France's contribution to the pooled stream is larger than this table says and
Germany's is not, and the thin German months are seasonality rather than a bad feed.

That clears the Japan bar on the median day. It does not clear it on every day, and the
thin days are predictable: Fridays, the second half of December, August, and the whole
of June and July for Germany. Phase 1's recommendation was that **the stage tolerate a
two-name day rather than drop the turnover floor to fill the wave**, because dropping
the floor is how you end up ranking names nobody can trade and whose short register does
not resolve (§4). **The operator overruled that on 2026-09-19 and the floor is now
$200k.** The reasoning above is not withdrawn; the section below prices what the change
buys and what it costs, measured rather than argued.

### What the $200k floor adds, measured

Two measurements, one forward and one retrospective, because they answer different
questions.

**Forward — the live vendor calendar and the live tape, ten sessions 2026-09-21 →
2026-10-02, measured on 2026-09-19.** Every primary listing whose next scheduled release
falls on one of those days, with median 20-session turnover in USD off the same FX rates
the universe uses:

| | median names/day ≥$200k | ≥$1m | mean ≥$200k | mean ≥$1m | ten-day total ≥$200k | ≥$1m |
| --- | --- | --- | --- | --- | --- | --- |
| UK | 4.5 | 1.5 | 4.5 | 2.0 | 45 | 20 |
| Germany | 0.5 | 0.0 | 0.6 | 0.4 | 6 | 4 |
| France | 1.0 | 0.0 | 1.0 | 0.4 | 10 | 4 |
| **pooled** | **6.5** | **2.5** | **6.1** | **2.8** | **61** | **28** |

Per day, pooled: 4 / 9 / 9 / 14 / 1 / 4 / 9 / 9 / 1 / 1 at $200k against
2 / 4 / 3 / 7 / 0 / 1 / 5 / 4 / 1 / 1 at $1m. **It is not cosmetic.** The floor roughly
doubles the stream — 61 names against 28 over ten sessions — and it changes France and
Germany from markets that contribute nothing on a median day to markets that contribute
one and a half between them. It does not fix the
thin days: 2026-09-25 and 2026-10-01 carry one name at either floor, and the worst day
is still a one-name day.

**Retrospective — the 20-day UK RNS record** (`analysis/phase1-uk-moves.json`, the 307
events that resolved to a price window): 153 events above $200k against 101 above $1m, a
median day of 7 against 4 and a mean of 7.65 against 5.05. The floor is 1 either way.
On the German and French Phase 1 cohorts the same ratio is +37% (169 against 123) and
+34% (156 against 116).

### What it costs, measured on the same forward sample

The 33 names the lower floor adds over those ten sessions, against the national short
registers read the same day:

| | names ≥$1m with a disclosed short | names $200k–$1m with one |
| --- | --- | --- |
| UK / FCA | 16 of 20 (**80%**) | 8 of 25 (**32%**) |
| Germany / Bundesanzeiger | 1 of 4 | 0 of 2 |
| France / AMF | register unreadable at the time of this probe — see §4 | — |

So in the UK — the only one of the three with enough names here to say anything — **the
positioning anchor resolves on 80% of the names above $1m and 32% of the names the new
floor adds.** That is the cost, and it is smaller than Phase 1's "12% below $1m" implies,
because that figure pooled the $200k–$1m band with everything beneath it. The German
rows are too few to read and the French rows were taken before the AMF register was
solved (§4); re-measure both once several days have run.

**The cost is carried in the data rather than in this paragraph.** Every baseline seals
`anchor_covered` — true only where the register names that issuer, false for a truncated
zero and false for an unreadable register, with `anchor_coverage.state` keeping those two
apart — `anchor_quality.direction` pays a truncated zero 0.15 where a disclosure earns
0.45, and `eu_resolve.py` reports `by_anchor_covered`: the Spearman, the sign rate and
the count in each arm. If the names this floor bought rank at zero, a fortnight of pooled
days says so.

---

## 2. Move, and whether the tail is intact

None of the three has a daily price limit. All three have volatility interruptions and
auction pauses, which halt trading briefly and do not cap the close. Measured, rather
than asserted:

| | n events | median \|move\| | p90 | p99 | max | share >10% |
| --- | --- | --- | --- | --- | --- | --- |
| UK (RNS-confirmed, session from the RNS timestamp) | 307 | **2.81%** | 12.21% | — | **42.23%** | 13.7% |
| Germany (vendor dates, best of the two adjacent windows) | 293 | 3.12% | 8.91% | 15.43% | **27.49%** | — |
| France (same) | 306 | 4.19% | 12.86% | 24.24% | **51.84%** | — |
| Japan, for comparison (`researcher_japan/README.md`) | — | 2.87% | — | — | — | — |

**The tail is intact in all three.** This is the one place where Europe is
unambiguously better than Tokyo, whose 値幅制限 truncates exactly the events the hunt
most wants credit for.

Two honest caveats on the German and French rows. First, they use the vendor's
`earnings_release_time`, which is `unknown` for 150 of 318 German and 238 of 346 French
names; windowing an `unknown` row as if it were pre-market understates the move, and the
first pass did exactly that and produced a German maximum of 15.4% that was an artefact.
Taking the larger of the two adjacent windows gives the table above. **Getting the
session wrong roughly halves the measured move**, which makes the session field the most
load-bearing single item in the baseline and the thing most likely to quietly poison an
early result.

Second, the move barely varies with liquidity, which is a good property for the stage:
UK median |move| by turnover band is 2.70% (<$1m), 3.61% ($1–5m), 2.58% ($5–25m), 2.76%
(>$25m). **A turnover floor does not cost move size.** It only costs names.

### The session is the structural difference from both existing stages

Over 379 UK results announcements with a parseable RNS timestamp:

| | count | share |
| --- | --- | --- |
| before 08:00 London | 339 | **89.4%** |
| in session 08:00–16:30 | 31 | 8.2% |
| after the 16:30 close | 9 | 2.4% |

The vendor agrees: 662 of 799 UK rows are flagged pre-market. Germany is 156 pre / 150
unknown / 12 post; France is 52 pre / 238 unknown / 56 post — the French habit of
publishing quarterly revenue after the 17:35 close is real and is the reason France has
the largest `amc` share of the three.

**Europe is a before-the-open market.** The measurement window is therefore
`close(D-1) → close(D)` for a `bmo` name, not the `close(D) → close(D+1)` that the US
and Japanese stages use. The baseline has to be sealed the evening before the print,
which is a scheduling constraint neither existing stage has.

---

## 3. The anchor: options

**This was the hoped-for improvement over Japan and it did not materialise.**

- **Yahoo carries no European single-stock option chains.** With a valid crumb,
  `v7/finance/options` returns 21 expiries and 196 contracts for `AAPL` and **0 expiries,
  0 contracts** for `SAP.DE`, `ADS.DE`, `BARC.L`, `MC.PA` and `BNP.PA`. This is the
  cheapest possible source and it is empty.
- **Eurex's daily reference file downloads** —
  `.../20260918_productandinstrumentfiles.zip`, 4.06 MB, HTTP 200 from this container —
  but it contains trading parameters, order profiles, instrument sub-types and price
  range tables. It carries **no settlement prices, no open interest and no underlying
  ISIN mapping**, so an implied move cannot be computed from it.
- **Eurex "market statistics (online)"** is a JavaScript-rendered page; the
  `100!onlineStats` path 404s with any query string and no JSON endpoint was found.
- Euronext's derivatives pages 404 or return the SPA shell.

So: **`options` is `null` for Europe, exactly as it is for Japan**, and the coverage
fraction by size band that the brief asked for could not be produced because the coverage
could not be measured at all from a free source. What I can say with confidence is the
narrower structural point: even where a Eurex chain exists, weekly expiries exist only on
the very largest underlyings, so for a mid-cap the front expiry spanning a print is
usually a monthly one weeks away, and an *event*-implied move is not extractable from it
even with the data. The stage should not be built on the assumption that a paid feed
would fix this cheaply.

**Consequence.** Europe runs in the same anchor-less regime as Japan, which is the
regime that produced the worst number in this repo: ρ=+0.073, p=0.45 over 104 events on
the sealed backtest corpus (`backtest/FINDINGS.md` §33). That has to be in the README and
in the note. Europe does not refute it; it makes it testable in a third market.

---

## 4. The anchor: short-disclosure registers

This is where Europe genuinely beats Tokyo, and the margin is large.

### UK — FCA. The best short register in the repo.

Three files, all one plain GET, no cookie, no key:

| file | size | content |
| --- | --- | --- |
| `aggregated-current-net-short-positions.csv` | 21 KB | **419 issuers**, aggregated net short %, position date, most recent **2026-09-17** |
| `aggregated-historic-net-short-positions.csv` | 343 KB | 5,615 rows, every position that has gone below the threshold, with the date it did |
| `short-positions-daily-update.xlsx` | 3.14 MB | **108,850 per-holder rows back to 2012-10-31** |

The third one is the important one and it has no Japanese analogue. JPX's register rolls
off, which is why `jp_positioning.py` has to cache it — once a day drops off the index it
cannot be re-fetched. The FCA publishes the **whole history**, so a European positioning
anchor can be backtested against past events rather than only run forward, and
`short_change_pct_pts` is a real measured delta rather than the single previous value
JPX happens to carry in the same row.

Coverage of the UK results cohort (302 unique ex-fund issuers over the 20 sampled days,
matched on normalised company name against the current register):

| turnover band | with a disclosed net short ≥0.5% | |
| --- | --- | --- |
| < $1m/day | 22 / 190 | **12%** |
| $1–5m/day | 41 / 46 | **89%** |
| $5–25m/day | 20 / 27 | 74% |
| > $25m/day | 8 / 12 | 67% |
| overall | 94 / 302 | 31% |

Japan's JPX register resolved on **9 to 11 of 25 names**, 36–44%. The UK resolves on
**89% of the $1–5m band**, which is the band this stage most wants. That single row is
the strongest argument in this file for building.

It is also the strongest argument for the turnover floor: below $1m/day the register
resolves on 12% of names, so the cheap half of the universe is the half where the
substitute anchor stops working *and* where nothing can be traded. Both reasons point
the same way.

### Germany — Bundesanzeiger. Works, with a cookie.

`https://www.bundesanzeiger.de/pub/en/nlp?0--top~csv~form~panel-form-csv~resource~link`,
with a session cookie picked up from `/pub/en/nlp` first, returns a UTF-8 CSV:
**486 live disclosed positions as of 2026-09-17**, holder / issuer / ISIN / % / date.
Filtered to German ISINs that is **124 issuers** against 427 primary German stocks —
thinner than the UK in absolute terms, and the file carries only the current position,
so the change has to be built by caching successive days exactly as Japan does.

### France — AMF. **Solved on 2026-09-19. The Phase 1 diagnosis was wrong.**

Phase 1 recorded `www.data.gouv.fr` as unreachable: four attempts on three paths, four
`Recv failure: Connection reset by peer`, `ws_closed_mid_exchange` in the proxy log
including against the site root. Re-tested **eighteen times on 2026-09-19 the host
answers roughly one request in three**:

| path | successes |
| --- | --- |
| `https://www.data.gouv.fr/` | 2 of 3 |
| `/api/1/site/` | 4 of 9 |
| `/api/1/datasets/<slug>/` | 2 of 6 |
| `/api/1/datasets/r/c2539d1c-…` | 1 of 6 (302) |
| `object-api.infra.data.gouv.fr` | **every request** |

The tunnel dies inside the TLS exchange — 517 B sent, 39 B received, closed after 7s —
which is indistinguishable from a policy block and is not one. **Four attempts were
enough to conclude "blocked"; eight are enough to get the file.** A tight retry loop
also fails: 0 of 12 with no pause against ~1 in 3 with a 2–4 s backoff.

So the register comes in **two retried hops**, and `eu_positioning.load_fr()` does both:

1. Ask `/api/1/datasets/<slug>/` (up to 15 tries, backoff) for the resource's current
   direct URL. The filename carries an export timestamp
   (`export_od_vad_20260918111500_20260918123001.csv`) and changes daily, so it cannot
   be hard-coded; the stable `…/datasets/r/<uuid>` id 302s to it and is tried first.
2. Pull the CSV from `object-api.infra.data.gouv.fr`, which has not failed a request
   here. **5.1 MB, 40,696 per-holder rows back to 2012-10-06.**

Columns: holder, LEI, issuer, ratio, ISIN, position start date, publication start date,
publication **end** date. That last one is what makes France the best-instrumented
register of the three in one specific respect: a position is open exactly while its end
date is empty, so **the aggregate can be reconstructed as of any past date**.
`short_change_pct_pts` is therefore a measured delta over a stated window (10 calendar
days) rather than the UK file's best effort or Germany's cache-two-days-and-subtract,
and the anchor is backtestable, like the FCA's and unlike JPX's.

Read on 2026-09-19: **74 issuers carry an open position** — against 419 UK and 124
German, so France is the thinnest of the three on breadth — aggregating to Ubisoft
12.56% across 11 disclosed sellers (−0.42pp over ten days), Valeo 10.69% (+0.36),
Renault 9.59% (+1.17), Teleperformance 8.38% (+0.51), Viridien 7.04% (+0.49). Median
aggregate 1.59%.

**Two details that cost a run each.** The file is served with a UTF-8 BOM, so a
byte-exact `startswith(b'"Detenteur')` header check fails on a download that worked and
reports the register unreachable with the working URL printed beside it. And a register
that fails on the day is now served from cache for up to five days with
`stale_cache_days` set on every name — a disclosure register moves slowly, but a reader
is entitled to know the file was not today's.

`bdif.amf-france.org` is still an Angular SPA whose API was not found, and it is no
longer needed.

---

## 5. Access from this container

Every row tested with `curl` and, where it mattered, with `WebFetch`. The Japan finding
(`WebFetch` 403 where `curl` returns 200) **does not generalise**: on this egress path
the two mostly agree, and where they differ it goes both ways.

| source | `curl` | `WebFetch` | note |
| --- | --- | --- | --- |
| Investegate day archive | **200** | **ok** | full RNS mirror, historical, paginated, timestamped |
| LSE `londonstockexchange.com/news` | 200 | — | SPA; its `api.` host returns 405 on GET |
| FCA short-position files | **200** | — | three files, no cookie |
| EQS-News / dgap.de | **200** | **ok** | same-day snapshot only, no pagination |
| Bundesanzeiger net short positions CSV | **200** | — | needs a session cookie |
| Börse Frankfurt `api.boerse-frankfurt.de` | 200 | — | `equity_key_data` works; `company_calendar` returns `{}` |
| Eurex site + daily reference zip | **200** | — | no prices, no OI, no ISIN map |
| Euronext `live.euronext.com` | 200 root, 404 sub-pages | — | SPA |
| AMF `amf-france.org` | 200 root | — | data pages 404 |
| `bdif.amf-france.org` | 200 | — | SPA, API not found |
| **`www.data.gouv.fr`** | **~1 in 3** | reads HTML | intermittent, NOT blocked — retry with a backoff (2026-09-19) |
| `object-api.infra.data.gouv.fr` | **200** | — | serves the 5.1 MB AMF register; no failure seen |
| BALO (`journal-officiel.gouv.fr/balo`) | **200** | — | |
| TradingView scanner (POST) | **200** | — | the forward calendar, all three markets |
| Yahoo chart `.L` `.DE` `.PA` | **200** | — | bars fine |
| Yahoo options `.L` `.DE` `.PA` | 200, **empty** | — | zero chains |
| Handelsblatt | **200** | **ok** | |
| Börsen-Zeitung | **200** | **ok** | |
| manager-magazin, WirtschaftsWoche | **200** | — | |
| finanzen.net, wallstreet-online, ariva.de | 200 | — | calendars are JS-rendered |
| La Tribune, AOF, ABC Bourse | **200** | — | |
| **Les Echos / Investir** | 403 | **blocked** | both refuse |
| **Boursier.com, Zonebourse, actusnews** | 403 | — | |
| **Sharecast, Proactive, Investors' Chronicle** | 403 | 403 | |
| Citywire | 200 (212 bytes) | — | effectively empty |
| MarketScreener, Investing.com | 403 | — | |

**The German press is fully open on both tools. The French financial press is largely
shut** — Les Echos, Investir, Boursier, Zonebourse and actusnews all refuse. That was
one of two reasons France was the weakest leg; **the other, its unreadable short
register, was solved on 2026-09-19** (§4). The press one stands: France is carried on
Euronext, BALO, La Tribune, AOF and ABC Bourse, which is thinner than what Germany and
the UK get.

---

## 6. The edge thesis, tested rather than asserted

The premise is that local-language information is under-read by the marginal
price-setter. The measurable proxy for "is anyone reading this name at all" is sell-side
coverage. Yahoo `financialData.numberOfAnalystOpinions`, 14 names drawn per cell with a
fixed seed, from the names that actually reported:

| turnover band | Germany | France | UK |
| --- | --- | --- | --- |
| < $1m/day | 1 | 2 | 2.5 |
| $1–5m/day | **7** | **6** | **5** |
| $5–25m/day | 13 | 12.5 | 11 |
| > $25m/day | 17.5 | 19 | 16 |

Consistent across all three markets, which is itself reassuring about the instrument.

**The operator's mid-cap prior is right in direction and one band too high.** MDAX/SDAX,
SBF 120 ex-CAC 40 and the FTSE 250 mostly sit in the $5–25m band at 11–13 analysts —
well covered, and the thesis is weak there. The genuinely under-read band is
**$1–5m/day: five to seven analysts**, which is the FTSE SmallCap and the liquid end of
AIM, the SDAX tail and Scale, and Euronext compartments B and C. Below $1m coverage
collapses to one or two analysts but so does the short register (12%) and so does
tradeability.

**I am nevertheless recommending against cutting to that band, and the reason is
methodological rather than empirical.** Japan's whole selection design exists because any
cut that is not random is a second ranking the scorer cannot see, and the US run has
already paid for that once. Selecting the universe on the thesis makes the thesis
untestable: if the stage only ever hunts $1–5m names, no resolved run can ever say
whether the edge is in that band. So: **a $1m/day turnover floor for capacity and for
anchor coverage, then a seeded random draw**, with `median_turnover_usd_20d` and the
analyst count carried in every baseline so `eu_resolve.py` can rank the hunt's own
performance *by* band. Measure the thesis; do not select on it.

**Large caps.** The brief's suspicion that the thesis is false for SAP, LVMH and Shell is
almost certainly right — 16 to 19.5 analysts and saturated English coverage. The random
draw will occasionally hand a hunter one of them. That is fine and it is the control:
if the hunt earns nothing on the >$25m band and earns something on $1–5m, that is the
thesis confirmed with a within-sample control the stage got for free.

### MAR Article 17 as a hunting surface

Worth having and smaller than it sounds. EQS-News's live snapshot carried six `ad-hoc`
items out of ~60 on 2026-09-18 — the ones seen were Porsche SE adjusting its full-year
group result forecast, Villeroy & Boch adjusting its 2026 forecast, and Enapter
announcing preliminary H1 figures with a one-off expense. These are exactly the objects
the Japanese hunter is told to look for under 業績予想の修正: a pre-released number that
makes the print itself substantially less of an event. The category is well-structured,
timestamped and machine-readable, which Hong Kong's profit alerts are not.

The limit is retrieval, not structure: EQS's FRONT PAGE serves a rolling snapshot with
no pagination. **Its search does paginate and goes back years** (2026-09-19), so ad-hoc
releases can be read historically per issuer after all — enough for a backtest, as long
as the backtest is willing to iterate issuers, because there is no whole-day query.
RNS via Investegate and the AMF flux both can be read by date.

---

## 7. Answers to the three questions

**Which market to start with, or all three pooled?**
**All three, pooled, from day one.** Not because pooling is elegant but because no single
one of them is a daily market: the UK bottoms out at one eligible name on a Friday,
Germany puts 153 of 259 forward events in November and carries one in June, France is
semi-annual with 94 of 161 in February–March. They peak in different months — Germany
November and March, France February–March and September, the UK spread across March,
September, November and December — so pooling is what turns three seasonal calendars into
one stream. That is the entire structural argument for treating them as one stage, and it
is the same argument as the shared regulatory spine (MAR 17, the Transparency Directive
half-yearly floor, the SSR 0.5% threshold), only measurable.

If the build has to be phased, phase it **UK first**: it is the only one of the three with
a historical day-level announcement archive, a one-GET daily short register that resolves
on 89% of the target band, an open local press, and a measured 2.2% calendar phantom rate.
Germany second. France last — §4's data.gouv problem was the reason, and it was solved
on 2026-09-19.

**Which size band?**
$1m/day turnover floor, currency-normalised to USD, and **no band cut above it** — as
recommended on 2026-09-18. **The floor was moved to $200k on 2026-09-19 by the
operator**; the no-band-cut half of this answer is unchanged and the cost of the other
half is measured in §1. The
thin-coverage band is $1–5m/day (5–7 analysts), one band below the operator's prior, but
selecting on it would bake the thesis into the universe and make it unfalsifiable. Carry
turnover and coverage in the baseline and let the resolver rank by band.

**Does the pooled stream clear the Japan bar?**
**On a median day yes, on every day no.** Japan's bar was that the quietest sampled day
still carried ~11 names. Pooled Europe above $1m/day is ~8–12 on a median day and ~12–15
above $200k/day, but the distribution has a hard floor problem: Fridays, August, late
December and the German June–July gap will produce days with two or three eligible names.
That is a real cost and it is not fatal — a three-name day costs three hunters and
produces a three-name ranking, which is a weak day and not a broken stage. It becomes
fatal only if someone responds by dropping the turnover floor, which would trade a thin
day for a day of names that cannot be traded and whose short register does not resolve.

---

## 8. Conditions on the build

1. **The session field is the weakest load-bearing item.** 89% of UK results are pre-open
   and the vendor calls the session `unknown` for 150 of 318 German and 238 of 346 French
   names. Getting it wrong roughly halves the measured move — it produced a spurious
   German maximum of 15.4% on the first pass here. The universe must carry the session,
   its source, and an explicit `session_unresolved` flag, and the resolver must not
   silently guess.
2. ~~**The French short register is unsolved.**~~ **Closed 2026-09-19** — §4 has the
   working path, and a French name now carries a disclosed position, a measured change
   and a lean that is not the free control. `lean_vs_free_control_rho` stays reported per
   market, now as the alarm that a register has stopped resolving rather than as a
   standing caveat about France.
3. **No option anchor anywhere.** Europe runs in the regime that scored ρ=+0.073 on the
   sealed corpus. Nothing here refutes that and the stage should say so in its own note
   every time.

## 9. One note on the language experiment and the UK

The stage runs an English pass first, freezes it as `pre_local`, then runs a
local-language pass and revises — the `impact_sum_pre_lessons` pattern applied to
language, so that "searching in German and French earns rank correlation" becomes a
measured claim instead of a belief.

**For the UK the local language is English, so the UK number is not measuring the same
variable as the German and French ones.** The UK's second pass is a *domestic-source*
pass — RNS, Investegate, Citywire, Proactive, Sharecast, the Investors' Chronicle, the
domestic trade press — so the variable is source locality, not language. The mechanics are
kept identical so the three markets stay structurally comparable, but
`pre_local_variable` is carried in every hunter's output (`language` for DE and FR,
`source_locality` for the UK) and **`eu_resolve.py` reports the pre/post delta per market
and refuses to pool the UK delta with the other two.** Pooling them would report an
average of two different experiments.

---

*Research, not investment advice. Keep the disclaimer from `config/pipeline.yaml` on
every deliverable.*

---

## 10. The seven markets added on 2026-09-19

Measured from this container on 2026-09-19 against the live vendor calendar, the live
tape and the live regulator sites, to the same standard as Phase 1: where a number could
not be measured it says so.

**This was an instruction, not a proposal** — the operator asked for the Nordics, Poland,
Milan and Madrid at the same $200k floor, with the cap raised to 20. What follows is what
that buys and what it costs, so the decision is reviewable rather than merely recorded.

### 10.1 Stream — and the first measurement is misleading

Over the ten sessions **2026-09-21 → 10-02**, with the $200k floor applied to live
20-session median turnover, the seven new markets add **six names** to a pooled median of
seven a day. On that number alone they are not worth their code.

That window is the problem, not the answer. Late September is the UK's month. Counting
**all** forward vendor events by the month they fall in:

| month | UK+DE+FR | new seven | of which SE | uplift |
| --- | --- | --- | --- | --- |
| Sep 2026 | 161 | 13 | 2 | 0.08× |
| **Oct 2026** | **114** | **456** | **259** | **4.00×** |
| Nov 2026 | 309 | 515 | 215 | 1.67× |
| Dec 2026 | 109 | 56 | 13 | 0.51× |
| Jan 2027 | 27 | 3 | 1 | 0.11× |
| Feb 2027 | 133 | 38 | 3 | 0.29× |
| Mar 2027 | 250 | 70 | 0 | 0.28× |

**October is the existing stage's thinnest month of the autumn and the new seven carry
four times its whole stream in it.** November nearly doubles. February and March — the
French and UK months — are barely touched. That is the same complementarity the original
three-market pooling argument rests on, and it is the whole case for this change.

### 10.2 Cadence, which matters more than the count

Median gap between a vendor row's last and next scheduled release:

| market | median gap (days) | market | median gap (days) |
| --- | --- | --- | --- |
| Sweden | 98 | Poland | 91 |
| Denmark | 91 | Italy | 105 |
| Norway | 91 | Spain | 105 |
| Finland | 97 | *UK* | *217* |
| | | *France* | *204* |

The Nordics and Poland report **quarterly**. A Nordic name therefore recurs four times a
year where a UK one recurs twice, so a pooled sample fills at roughly twice the rate per
name — which matters for a stage whose binding constraint is how many resolved events it
can accumulate before anything can be said.

### 10.3 What is worse: the vendor barely sees three of them

Fraction of each market's primary-listing universe carrying an
`earnings_release_next_date`:

| market | universe | with a forward date | fraction |
| --- | --- | --- | --- |
| Finland | 181 | 160 | **0.88** |
| Norway | 274 | 221 | **0.81** |
| UK | 1078 | 807 | 0.75 |
| Germany | 427 | 259 | 0.61 |
| Sweden | 893 | 493 | 0.55 |
| Denmark | 134 | 62 | 0.46 |
| France | 591 | 161 | 0.27 |
| **Italy** | 389 | 78 | **0.20** |
| **Spain** | 278 | 54 | **0.19** |
| **Poland** | 709 | 89 | **0.13** |

Italy, Spain and Poland sit at or below France's coverage — and France was measured in §1
to be **undercounted 3.6× by this same vendor**. So those three are sampled rather than
screened. They are in because they were asked for and because a missed name costs
nothing; **they are not load-bearing and no note should present them as if they were.**

### 10.4 The anchor: five more registers, and two that do not exist

| market | source | result | change measurable? |
| --- | --- | --- | --- |
| Sweden | Finansinspektionen `GetBlankningsregisterAggregat` (ODS) | ✓ 342 issuers | cache diff only |
| Denmark | Finanstilsynet aggregated table (inline HTML) | ✓ 50 issuers, **0.1% threshold** | cache diff only |
| Norway | `ssr.finanstilsynet.no/api/v2/instruments` (JSON) | ✓ 96 issuers, **full dated event history** | **exact** |
| Finland | `finanssivalvonta.fi/api/shortselling/datatable/current` (POST) | ✓ 17 issuers, per holder | cache diff only |
| Italy | CONSOB `PncPubbl.xlsx` | ✓ 52 issuers, per holder, **WAF 2/5 — retry** | cache diff only |
| **Spain** | CNMV `posicionescortas` | **✗** ASP.NET postback, 0 rows on 8/8 | — |
| **Poland** | KNF `RssOuterView/JSCRIPT` | **✗** 302 then 403, every attempt | — |

Three things follow.

**Norway's is the best register in this stage.** A full dated event history per issuer
means the level *and* the change over any window are exact measurements, and the anchor
is backtestable — the property the FCA and AMF files have and Bundesanzeiger's does not.

**Denmark is not on the same scale as anybody else.** Finanstilsynet publishes from
**0.1%** where the SSR threshold is 0.5%, so Danish aggregates sum positions no other
register shows and read systematically higher for the same real crowding. Deliberately
**not rescaled**: a correction factor nobody has measured is worse than a difference
everyone can see. `threshold_pct` rides in the Danish rows.

**Spain and Poland have no anchor at all**, and both were given the **eight-try standard**
that rescued France in §4 and Italy here — on the same sweep, `emarketstorage.com`
scored 7 of 8 while `www.gpw.pl` and `espi.pap.pl` each scored 0 of 8. With no register a
name's `priced_lean_pct` falls back to `-0.05 × run_up_20d_pct`, which **is the free
control the whole stage is measured against**, so such a name cannot beat the benchmark
with anything that uses it.

### 10.5 Confirmation: who can ever be killed

| market | day archive | `event_occurred: false` |
| --- | --- | --- |
| Norway | Oslo Børs NewsWeb — true day query, **ticker-keyed**, categorised | yes |
| Italy | eMarket STORAGE — WAF 7/8, **`data_to` is EXCLUSIVE** | yes |
| SE / DK / FI | Nasdaq Nordic feed — issuer's own category, but **no date query** | only inside a ~12-day paged window |
| **Spain, Poland** | none reachable | **no** |

Two traps were found here and both are the silent kind:

- **The Nasdaq feed's `fromDate` is accepted and ignored.** A request for a date a month
  old returns the most recent 200 rows, dated today, with HTTP 200. Used naively it would
  have written a confident `event_occurred: false` for every Nordic name ever hunted. The
  code never passes the filter and pages back instead.
- **eMarket STORAGE's `data_to` is exclusive.** `data_from=D&data_to=D` returns zero rows
  and is indistinguishable from a day on which nothing was published; `data_to=D+1`
  returns the 19 rows that exist.

### 10.6 Access from this container

The financial **press** of all four new regions is more open than France's, which is the
one pleasant surprise. Three tries each: di.se, dn.se, placera.se, avanza.se, borsen.dk,
e24.no, kauppalehti.fi, hs.fi, mfn.se, milanofinanza.it, ilsole24ore.com, teleborsa.it,
borsaitaliana.it, expansion.com, bolsamania.com, parkiet.com, pb.pl, bankier.pl,
stockwatch.pl and strefainwestorow.pl **all 3/3**. Refusing: affarsvarlden.se (0/3),
cincodias.elpais.com (403), eleconomista.es (403), dn.no (2/3).

**Poland is the instructive case.** Its regulator and its exchange are both shut to this
container while its entire financial press is open — so a Polish name can be *researched*
and cannot be *anchored* or *confirmed*. Those are different failures and the stage
records them separately.

### 10.7 What would change the verdict

- If pooled days accumulate and `by_market` shows the Spanish and Polish arm ranking at
  zero while the anchored markets do not, **drop them**; they are already first in
  `europe_hunt.degrade_order` for exactly this reason.
- If the Nasdaq feed gains a working date query, Sweden, Denmark and Finland move from
  conditional to unconditional confirmation.
- If a Spanish or Polish register becomes reachable, add a loader and delete the entry
  from `eu_positioning.UNREACHABLE`. It is written to be re-tested, not believed.

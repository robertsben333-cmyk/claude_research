# researcher_europe — stage EU

The unpriced-information hunt, run over **ten European markets pooled** — the UK,
France, Germany, Sweden, Denmark, Norway, Finland, Italy, Spain and Poland. One signed
number per company (`impact_sum`, points of spot, unbounded) so the day's names can be
**ranked**. No call, no threshold, no direction label. Research only: **this stage places
no orders and reads no broker.**

It exists to ask whether the result the US stage is chasing is a property of the method
or a property of the US market — the same question stage J asks of Tokyo, now asked of a
third region with a different microstructure. Because it uses the same scorer, the same
key and the same measurement window, all three are directly comparable.

Alpaca carries none of these ten venues. Execution here is a separate decision to be
made later on Europe's own resolved numbers; what this stage does for that decision is
carry a turnover floor and a shortability signal in the universe, and say below what a
broker would still need.

## Status

**Nothing has resolved. There is no European result, good or bad.**

**Seven markets were added on 2026-09-19** — Stockholm, Copenhagen, Oslo, Helsinki,
Milan, Madrid and Warsaw — on the operator's instruction, with the cap raised from 12 to
20. Same $200k floor, same scorer, still no orders. What that change rests on, and what
it costs, is in "Ten markets and not three" below. The short version: it buys October and
November, which are exactly the months the original three are thinnest, and it brings in
two markets (Spain and Poland) that have **no positioning anchor and no way to confirm a
print after the fact**.

Built and validated end to end on 2026-09-18 against a real past date (2026-09-16: 22
vendor-scheduled rows across the three markets, 4 eligible above the $1m turnover floor,
4 baselines sealed, **4 of 4 confirmed by a real results RNS on Investegate** out of the
40 EPICs that filed one that day). That run used **synthetic findings** to exercise the
plumbing and ranked at ρ=−0.80, p=0.33 on four names, which is what random findings on
four names should do and **is not a result about anything**. Its baselines are stamped
`validation_only` and carry a note saying their tape was read after the print.

The retrospective-kill path was verified separately against two names the Phase 1
measurement had already identified as no-shows: on 2026-09-15 Investegate carried 37
results RNS and 296 issuers announcing anything, and **ITM Power and Petra Diamonds
appear in neither** — `event_occurred: false`. Trustpilot appears in the second list and
not the first, because its interims were headlined "AI, Enterprise and US momentum fuel
strong growth", and it correctly resolves to `announced_unclassified` — a human call,
not an automatic kill.

## The pieces

| | |
| --- | --- |
| `SUBMARKET.md` | Phase 1. Why these markets, with the counts. **Read it before changing any threshold here.** |
| `scripts/eu_market.py` | what the ten markets share, where they differ, and **`CAPABILITY`** — what each one's sources can actually do |
| `scripts/eu_universe.py` | the vendor forward calendar → today's names, USD turnover floor in six currencies, seeded random draw |
| `scripts/eu_priced_in.py` | the sealed baseline, in the shape `edge_score.py` reads |
| `scripts/eu_positioning.py` | eight national short registers, the substitute anchors |
| `scripts/eu_archive.py` | **the day archive per market** — Investegate, the AMF flux, EQS search, the Nasdaq Nordic feed, Oslo NewsWeb, eMarket STORAGE — one row shape, one classifier, one three-state `confirm()` |
| `scripts/eu_sheet.py` | ODS and XLSX with the standard library, because two registers are spreadsheets and this container has no `openpyxl` or `odfpy` |
| `scripts/eu_resolve.py` | confirmation, realised move, Spearman + permutation p, per-market stats, the anchor-coverage split, the language control |
| `researcher_us/scripts/edge_score.py` | **shared** — same scorer for all ten markets, so the numbers are comparable |
| `.claude/agents/unpriced-hunter-{uk,fr,de,nordic,it,es,pl}.md` | the hunters; same output contract, seven source worlds. The four added in 2026-09 are **generated from the German one** so the invariant contract cannot drift |
| `.claude/skills/researcher-europe-hunt/SKILL.md` | the run |
| `LESSONS.md` | what a finding has to carry here, grown from resolved runs |

## Ten markets and not three

Because none of them is a daily market on its own, and the counts are in `SUBMARKET.md`:

- **UK** — 17 results announcements a day ex funds at the median over four sampled
  weeks, but **three** on 2026-03-06 and four on 2026-01-16. Seven a day above a $200k
  turnover floor, with a floor of **one**. Fridays are thin every week sampled.
- **Germany** — the quarterly market: 60% of issuers report on a ≤100-day cadence
  because Prime Standard still owes quarterly statements where the Transparency
  Directive floor is annual-plus-half-year. But **153 of 259 forward events are in
  November**, and June carries one. Quarterly frequency does not help when every issuer
  is a December year-end reporting in the same fortnight — the Korea failure mode in
  milder form.
- **France** — semi-annual, median gap 204 days, **94 of 161 forward events in
  February–March**. The thinnest of the three on both axes.

They peak in different months, so pooling is what turns seasonal calendars into one
stream. Fridays, August, late December and the German June–July gap are thin whatever the
floor is, and **a thin day is a weak day, not a broken stage**.

### The seven added on 2026-09-19, and the measurement that justifies them

**The obvious test says they add nothing, and it is testing the one window where they
cannot help.** Over the ten sessions 2026-09-21 → 10-02, against the live vendor
calendar and the live tape, the seven new markets add **six names** to a pooled median of
seven a day. Late September is the UK's month and nobody else's.

By **month** of forward vendor events the picture inverts:

| month | UK+DE+FR | the new seven | note |
| --- | --- | --- | --- |
| Sep 2026 | 161 | 13 | the window the ten-session probe sampled |
| **Oct 2026** | **114** | **456** | October is the existing stage's *thinnest* month |
| Nov 2026 | 309 | 515 | |
| Dec 2026 | 109 | 56 | |
| Feb 2027 | 133 | 38 | |
| Mar 2027 | 250 | 70 | |

Sweden alone carries 259 October events. **The seven are worth their code in October and
November and add almost nothing in February and March**, which is precisely the
complementarity the original pooling argument is built on.

**And the cadence is better, which matters more than the count.** Measured median gap
between a vendor row's last and next release: Sweden 98 days, Denmark 91, Norway 91,
Finland 97, Poland 91, Italy 105, Spain 105 — against the UK's 217 and France's 204. The
Nordics report quarterly, so a Nordic name recurs four times a year where a UK one
recurs twice, and a pooled sample fills at twice the rate per name.

**What is worse, and it is not small.** The vendor carries a forward date for 0.88 of
Finnish and 0.81 of Norwegian issuers and for **0.20 of Italian, 0.19 of Spanish and 0.13
of Polish** ones. That is France's regime (0.27), and France was measured to be
undercounted 3.6× by this same vendor — so Milan, Madrid and Warsaw are seen through a
calendar that misses most of them.

### They are not equally instrumented, and that is carried in the data

`eu_market.CAPABILITY` is the measured table, from 2026-09-19:

| markets | short register | day archive | `event_occurred: false` | `history` |
| --- | --- | --- | --- | --- |
| **uk** | FCA, with history | Investegate, by date to 1999 | yes | **observed** |
| **no** | dated event history per issuer — the best of the ten | Oslo NewsWeb, true day query, **ticker-keyed** | yes | **observed** |
| **fr** | AMF, per-holder to 2012 | AMF flux, issuer's own category | yes | estimated |
| **it** | CONSOB xlsx, WAF-retried | eMarket STORAGE, WAF-retried | yes | estimated |
| **se dk fi** | national, snapshot only | Nasdaq Nordic, **paged, no date query** | only inside a ~12-day window | estimated |
| **de** | Bundesanzeiger, snapshot | EQS, per issuer only | **no** | estimated |
| **es pl** | **none reachable** | **none reachable** | **no** | estimated |

Three consequences worth stating plainly:

- **Norway is now the second-best-instrumented market in this stage**, after the UK. It
  is the only other one whose `history` carries observed announcement dates.
- **Spain and Poland run blind on both axes.** With no register, `priced_lean_pct` falls
  back to the 20-day run-up — which is also the free control the stage is measured
  against — so those names cannot beat the benchmark with anything that uses it, and
  their prints can never be confirmed or killed. Both were given the eight-try standard
  that rescued France and Italy and failed it. **A pooled ρ that does not say how much of
  it is `es`/`pl` is being oversold.**
- **Denmark is not on the same scale as anyone else.** Finanstilsynet publishes from
  **0.1%** where the SSR threshold is 0.5%, so Danish aggregates are systematically
  larger for the same real crowding. Deliberately not rescaled — a correction factor
  nobody has measured is worse than a difference everyone can see.

**The floor is $200k/day since 2026-09-19, down from $1m, on the operator's
instruction** — the same bar the US and Japanese stages screen on, so all ten markets
are cut the same way and their resolved numbers are comparable. Measured over the ten
sessions 2026-09-21 → 10-02 on the live vendor calendar and live tape, it is not
cosmetic: the pooled day goes from a median of **2.5 names to 6.5** and a mean of 2.8 to
6.1, and France goes from a median of 0 names a day to 1. What it costs is the anchor,
priced in `SUBMARKET.md` §"What the $200k floor adds"; `anchor_covered` rides in every
baseline and `eu_resolve.py` reports the Spearman split by it.

## Europe reports before the open, and that changes the window

339 of 379 UK results announcements with a parseable RNS timestamp landed **before 08:00
London**; 31 in session and 9 after the close. The vendor calendar agrees, and France has
the largest after-close share of the three because French issuers publish quarterly
revenue after the 17:35 Paris close.

So a `bmo` name is scored `close(D−1) → close(D)` and the baseline has to be sealed **the
evening before the print** — a scheduling constraint neither the US nor the Japanese stage
has. `eu_universe.py --date` therefore defaults to the next calendar day.

**Getting the session wrong roughly halves the number.** On the 2026-09-16 validation run
Barratt Redrow moved **+11.72%** over the correct bmo window and +1.78% over the amc one.
The first pass of the Phase 1 measurement windowed the vendor's `unknown` rows as if they
were pre-market and produced a German maximum realised move of 15.4% where the correct
window gives 27.5%. The vendor says `unknown` for 150 of 318 German and 238 of 346 French
rows, so this is not a corner case: `session_unresolved` rides in every baseline and the
resolver reports **both** windows for such a row rather than choosing one silently.

## The anchor problem, and how much of it was solved

Europe was expected to fix Japan's biggest hole. **It does not.** Measured:

- Yahoo returns 21 expiries and 196 contracts for `AAPL` with a valid crumb and **zero
  expiries and zero contracts** for `SAP.DE`, `ADS.DE`, `BARC.L`, `MC.PA` and `BNP.PA`.
- Eurex's daily product-and-instrument reference file downloads cleanly (4.06 MB, HTTP
  200) and carries trading parameters, order profiles and price-range tables — **no
  settlement prices, no open interest, no underlying ISIN map** — so no implied move can
  be computed from it. Its market-statistics page is JavaScript with no JSON endpoint.
- Euronext's derivatives pages return the SPA shell.

So `options` is all `null` and Europe runs in the same anchor-less regime as Japan, which
is the regime that produced ρ=+0.073, p=0.45 over 104 events on the sealed backtest corpus
(`backtest/FINDINGS.md` §33). Nothing here refutes that. It makes it testable in a third
market, on a tail that is not truncated.

What stands in its place is the Short Selling Regulation's 0.5% public threshold, and
**here Europe genuinely beats Tokyo**:

| | what it is | coverage | reachable? |
| --- | --- | --- | --- |
| **UK / FCA** | aggregated current net short positions, plus the **whole per-holder history back to 2012** | **89% of the $1–5m turnover band**, 74% at $5–25m, 67% above $25m, 12% below $1m | three plain GETs, no cookie |
| **DE / Bundesanzeiger** | current net short positions | 124 German issuers of 427 primary listings | one GET, needs a session cookie |
| **FR / AMF** | per-holder history since 2012 with publication start **and end** dates | 74 issuers with an open position | **yes, since 2026-09-19** — two retried hops |

Japan's JPX register resolved on 9 to 11 of 25 names. The FCA also publishes history,
which JPX does not — its file rolls off, which is why `jp_positioning.py` has to cache it.
So a European positioning anchor can be **backtested**, not only run forward.

**France was the hole and it is now closed (2026-09-19). The diagnosis that closed it
was wrong.** Phase 1 tried `www.data.gouv.fr` four times, got four connection resets
(`ws_closed_mid_exchange`, including the site root) and recorded the host as unreachable.
Re-tested eighteen times it answers **roughly one request in three**: the site root 2 of
3, `/api/1/site/` 4 of 9, the dataset endpoint 2 of 6. The tunnel dies inside the TLS
exchange — 517 B sent, 39 B received, closed after 7s — which is indistinguishable from
a policy block and is not one.

So the register comes in **two retried hops**: ask the dataset endpoint (up to 15 tries,
with a backoff) for the resource's current direct URL — the filename carries an export
timestamp and changes daily, so it cannot be hard-coded — then pull the CSV from
`object-api.infra.data.gouv.fr`, which has answered every request made to it. **5.1 MB,
40,696 per-holder rows back to 2012**, each with a position start date, a publication
start date and a publication **end** date.

That last column makes France the best-instrumented of the three in one respect: a
position is open exactly while its end date is empty, so the aggregate can be
reconstructed **as of any past date**, and `short_change_pct_pts` is a measured delta
over a stated window (10 calendar days) rather than the UK file's best effort or
Germany's cache-two-days-and-subtract. It is backtestable, like the FCA's and unlike
JPX's. What it does not fix is breadth: **74 French issuers carry an open position**
against 419 UK and 124 German.

Read on 2026-09-19 the register gives Ubisoft 12.56% across 11 disclosed sellers
(−0.42pp over ten days), Valeo 10.69% (+0.36), Renault 9.59% (+1.17), Teleperformance
8.38% (+0.51). A French name's lean is therefore no longer the free control, and
`lean_vs_free_control_rho` is still reported **per market** — because a register that
quietly stops resolving sends that number back toward 1.0 and nothing else would say so.
On the validation run the UK read **0.40**.

**A register that fails on the day is now used from cache if it is at most five days
old**, with `stale_cache_days` in every name's positioning block. A disclosure register
moves slowly; a reader still gets to see that the file was not today's.

**The weights are priors and nothing about them is measured in Europe.** They are the
Japanese priors, which are the US priors: a crowded short is treated as a positive lean
because the US run watched two shorts into 18%- and 23%-of-float names both squeeze more
than 20%; shorts building into a print is treated as negative because disclosed sellers
who must file their names are the closest thing these markets have to visible informed
flow. Europe has **no analogue of Japan's 信用倍率**, so the lean rests on two independent
components rather than three, and on one in France. `eu_resolve.py` ranks each component
separately for exactly this reason. **Replace the weights with measurement; do not defend
them.**

## The calendar is a vendor calendar, and its error rate was measured

TradingView's public scanner is the forward calendar for all ten markets. Against the
actual RNS record over 20 fully scraped days, **90 of its UK rows fell on a scraped day
and 88 had a same-day results announcement from the same issuer — a 2.2% phantom rate.**
The US stage's `time-not-supplied` rows were 20 of 20 phantom on 2026-09-17, so this is a
different object. It is not zero: on a ten-name day 2.2% is one phantom every five days,
and this repo ranked, traded and lost money on TRT, which never reported. `event_occurred:
false` is reachable and the confirmation pass is not optional.

**Its forward-date coverage is very uneven across the ten**, and that is a separate
failure from a phantom row. Measured 2026-09-19 as the fraction of each market's primary
universe carrying an `earnings_release_next_date`: UK 0.75, Finland 0.88, Norway 0.81,
Germany 0.61, Sweden 0.55, Denmark 0.46, France 0.27, **Italy 0.20, Spain 0.19, Poland
0.13**. A market at 0.13 is not being screened, it is being sampled.

**Eight of the ten markets have a day archive** — `scripts/eu_archive.py`, one row shape
over six sources, so `eu_resolve.py` confirms every market through one code path. It
returns **`None`, not `[]`**, where a source could not be read, because "nobody announced
anything" and "I could not look" are the two answers this stage may never confuse:

- **UK — Investegate**, a full RNS mirror queryable **by date back to 1999**. Stronger
  than Japan's TDnet, which keeps about 31 days: a UK run can be confirmed months later.
  Results are identified by **headline**, which is its weakness.
- **SE / DK / FI — the Nasdaq Nordic disclosure feed** (`api.news.eu.nasdaq.com`), one
  endpoint for three markets, carrying **the issuer's own release category** — so the
  property that made France the best-classified market now holds in four. **Its
  `fromDate` is accepted and IGNORED**: a request for a date a month old returns the most
  recent 200 rows, dated today. That is the most dangerous shape in this stage, a
  successful-looking request for the wrong day, so the filter is never passed and the
  feed is **paged** instead — about two days per request, roughly twelve days before it
  stops being cheap. Beyond that window it returns `None`. **Resolve a Nordic run within
  about a week.**
- **NO — Oslo Børs NewsWeb**, a true `fromDate`/`toDate` query with English category
  labels and `issuerSign` on every row. The only archive besides Investegate that lets
  confirmation join on a **ticker** rather than a normalised company name, which is the
  weakest link everywhere else here. Its per-issuer query is also what gives Norway
  observed announcement history.
- **IT — eMarket STORAGE**, Borsa Italiana's officially appointed storage mechanism,
  behind the same Radware WAF as CONSOB (measured 7 of 8 good, so retried rather than
  believed on one failure). **`data_to` is EXCLUSIVE** — `data_from=D&data_to=D` returns
  zero rows and looks exactly like a silent day, where `data_to=D+1` returns the 19 that
  exist.
- **ES / PL — nothing.** Every CNMV `Consulta-OIR` path returns 403; `www.gpw.pl` and
  `espi.pap.pl` each returned 0 of 8 on the sweep where emarketstorage returned 7 of 8.
- **FR — `info-financiere.gouv.fr`**, the AMF's own regulated-information archive,
  through an Opendatasoft API with no key: **536,868 records back to 2012**, current to
  yesterday, 45–110 items a day, queryable by date range. It is the only one of the
  three that carries the **issuer's own declared filing category** — *Rapports
  financiers et d'audit semestriels / annuels*, *Information financière trimestrielle* —
  so a French results release is identified by what the issuer filed it as rather than
  by what its headline says. That is the one real fix for the Trustpilot failure mode
  and only France has it. Phase 1 recorded "FR — nothing readable", which was true of
  Euronext and was never tested against the AMF's own archive.
- **DE — EQS-News *search***, `/search-results/?searchtype=news&searchword=…`,
  paginated at `/search-results/page/<n>/`, **back years**. Phase 1 measured the front
  page, which does not paginate, and concluded EQS "confirms today and yesterday and
  nothing older"; the search does not have that limit. Each row carries the date, the
  EQS news type, the company, the headline and the **ISIN**.

**`event_occurred: false` is now reachable for the UK and France and not for Germany**,
and that asymmetry is in every row's `confirmation_note`. EQS has no whole-day query, so
the German archive is assembled issuer by issuer and "not found" can mean the search
term missed rather than that nothing was published. A German name therefore resolves
`null`, never `false` — absence of a readable page is not absence of a release.

**The German search word is not the issuer's legal name.**
`searchword=HORNBACH Holding AG & Co. KGaA` returns **zero** rows and `HORNBACH`
returns 25: the search ANDs over words, so every legal-form token narrows it to
nothing. `eu_archive.de_query()` strips them and keeps two tokens. This cost a whole
measurement run, in which nine German vendor rows all resolved `null` and looked like a
coverage problem.

**The vendor undercounts the UK and France and not Germany.** On the 20 sampled days the
UK's measured count above $1m/day of turnover was 5.05 events a day against the 2.3 the
vendor's forward calendar gives — a factor of 2.2. With day archives for the original
three markets (2026-09-19) the same comparison gives **3.6× for France** on the week where the
vendor's last-release field is current — 10.0 results issuers a day against 2.8 vendor
rows — and **0.78× for Germany** in its August peak week, 10.8 against 13.8. So France's
contribution to the pooled stream is materially larger than `SUBMARKET.md`'s table says,
Germany's is not, and the thin German months are seasonality rather than a bad feed.

**Yahoo's European daily closes lag, so a run cannot be resolved the next morning.**
Measured 2026-09-19: `.PA` and `.DE` symbols carried timestamps for 09-17 and 09-18 with
**null closes**, on liquid names as well as thin ones, and `.L` was one session behind.
`eu_resolve.py` carries `last_bar_date` and `move_pending` per row and warns when every
row is pending, so an unresolvable morning is never read as a day on which nothing moved.

## The selection is random on purpose, and the floor is $200k

Two steps: drop everything below **$200k a day** of median 20-session turnover,
normalised to USD off a live FX rate written into the universe file; then if more than
`cap` survive, take a **random sample seeded by the date**.

It was **$1m until 2026-09-19** and that reason was measured: below $1m the FCA register
returns a disclosed position for 22 of 190 UK names (12%) against 41 of 46 (89%) in the
$1–5m band, so the cheap half of the universe is the half where the substitute anchor
stops working *and* nothing can be traded. The operator moved it to $200k for
cross-market comparability and stream depth, **cost accepted, not missed**.

The cost is carried rather than argued about. Every baseline seals **`anchor_covered`** —
true only where the register named this issuer, false for a truncated zero (register
read, issuer absent) and for an unreadable register — `anchor_quality.direction` pays a
truncated zero 0.15 where a disclosure earns 0.45, and `eu_resolve.py` reports
`by_anchor_covered` with the count in each arm. If the uncovered half ranks at zero,
that is readable within a fortnight instead of never.

Random, because any other cut is a second ranking the scorer cannot see. The US run has
already paid for this: its two highest-`hunt_priority` names got two hunters each, and
because the key is a sum those names carried the largest conviction by construction.

**And there is no size-band cut above the floor, deliberately, against the prior that
motivated this stage.** Sell-side coverage was measured at 1–2 analysts below $1m/day of
turnover, 5–7 at $1–5m, 11–13 at $5–25m and 16–19 above $25m, consistently across the
three markets it was measured on. The genuinely under-read band is $1–5m — one band *below* MDAX / SBF 120
ex-CAC 40 / FTSE 250. Cutting the universe to it would bake this stage's own thesis into
its universe and make it unfalsifiable. So `analyst_band` rides in every baseline and
`eu_resolve.py` ranks the hunt **by band**. Measure the thesis; do not select on it.

## Each hunter searches English and the local language in ONE pass

**Since 2026-09-22, on the operator's instruction.** One pass, both languages, moving
between them as the question demands: a German filing is often the reason to run a
particular English query, and an English wire item is often the reason to go and find the
German original.

English-only is the coverage the thesis says is already in the price. Local-only throws
away sell-side notes, wire copy and cross-border reporting that genuinely carry
information. Both halves are required; neither is the junior partner.

**What this replaced, and what it cost.** Until that day the hunt ran English first,
froze that draft as `pre_local`, and only then searched locally; `edge_score.py` carried
`diagnostics.impact_sum_pre_local` beside the key and `eu_resolve.py` ranked both against
the same realised move, so "searching in the local language earns rank correlation" was a
measured claim rather than a belief. It is gone, and the reason is not only the turns the
split cost: sequencing the two halves forbade them from informing each other, so the
control was being paid for out of the quality of the research it was measuring.
**Nothing measures the local half now**, and a freeze reconstructed after the fact is not
a freeze, so it cannot be recovered from a run later. The one thing that softens it: no
European day had resolved while the control ran, so `spearman_pre_local` never produced a
number against a real outcome. What was given up is a future measurement, not a result.

**What replaces it is prose.** Every hunter emits `language_note` — one line per thing
the local-language sources carried that the English ones did not, or the single line
'nothing the English sources did not already carry'. Nothing ranks it. `eu_resolve.py`'s
language-pass section still exists and reports 0 names on any run sealed after the merge;
that is the honest report of a retired control, not a hunter that forgot to freeze. The
dashboard's `Taal` tab still shows the runs that carry the field, labelled as history.

**The UK case was degenerate and the asymmetry survives the merge.** Its local language
is English, so its local half is a **domestic-source** half — RNS, Investegate, Citywire,
Proactive, Sharecast, the Investors' Chronicle, the domestic trade press — and the
variable is source locality, not language. A UK `language_note` saying the domestic
sources added nothing is an honest result and not a lazy hunt.

**The Nordic case is weaker than the others too, and for a different reason.** Nordic
issuers publish in English as a matter of routine — most releases go out in both
languages at once, which is not true in Germany, France or Italy. So the premise the
local half rests on is genuinely thinner there, and 'nothing the English sources did not
already carry' is the expected `language_note` more often than anywhere else in the
stage. What is reliably local in the Nordics is the **press and the retail forums**, not
the filing, and `unpriced-hunter-nordic` says so in as many words.

## Currencies, holidays and the things that differ per market

- **Currencies — six of them.** The UK quotes in pence (`GBp` on Yahoo, `GBX` on the
  vendor); France, Germany, Finland, Italy and Spain in EUR; Sweden in SEK, Denmark in
  DKK, Norway in NOK, Poland in PLN. Moves are in percent so the key is unaffected, but
  the turnover floor is an absolute number and would otherwise mean six different things.
  **Everything is normalised to USD**, off a live rate, and every rate is written into
  every universe file so the cut is reproducible. A currency whose rate does not resolve
  drops that market's names as "no fx" rather than screening them at the wrong size — a
  PLN name compared to a USD floor would pass at a quarter of its real turnover.
- **Ticker translation is per market.** The vendor writes Nordic share classes with an
  underscore and Yahoo with a hyphen: `OMXSTO:INVE_A` is `INVE-A.ST`, `OMXHEX:NDA_FI` is
  `NDA-FI.HE`. Getting this wrong does not raise — Yahoo answers with an empty chart, the
  row drops as "no tape", and the day silently loses its largest Nordic names, which are
  exactly the ones with two share classes.
- **The vendor's country scanner is not one exchange.** `sweden` pools OMXSTO (663) with
  NGM (230) and `poland` pools GPW (384) with NewConnect (325). NGM names do not take
  `.ST` at all, so they would be screened on somebody else's tape. `exchange_allow`
  filters the markets added in 2026-09 and is deliberately absent for uk/de/fr, whose
  output must stay byte-identical — the UK scanner has always carried 37 AQUIS rows.
- **Holidays are exchange holidays, not public holidays.** XETRA trades on Fronleichnam
  and Allerheiligen, which a generic German holiday list carries; Euronext Paris is
  shorter than the French jours fériés; Stockholm and Helsinki shut for **Midsummer Eve**,
  which moves (the Friday between 19 and 25 June) and is computed rather than listed.
  These are computed from Easter plus a fixed list in `eu_market.exchange_holidays()`.
  **The UK is the only one fetched live** — `gov.uk/bank-holidays.json`, cached. The other
  nine are hand-entered from each exchange's published trading calendar and are therefore
  the most likely thing in this module to be quietly wrong; `market_closed` in the
  universe file records which rule fired, so an error shows up in the output rather than
  only in the source. **The Nordic list is the one to check first**: three moving feasts
  plus Midsummer.
- **Half sessions** around Christmas and New Year are reported, not skipped — a print into
  a 12:30 close has half the exit window the measurement assumes and a reader is entitled
  to know which rows those are.

## What a broker would still need

Nothing in this stage places an order, and the fields below exist so that decision can be
made later rather than re-derived:

- `median_turnover_usd_20d` on every baseline, and the universe's `dropped` list with the
  reason, so capacity is visible per name.
- `positioning.short_ratio_pct` is a **disclosure** register, not a borrow feed. A name
  with no disclosed short is not necessarily borrowable and a name with one is not
  necessarily easy to borrow. Europe has no Alpaca-style shortability endpoint in this
  stage and there is no substitute for asking a broker.
- Three currencies means FX exposure on every position and a settlement cycle that is not
  the US one. Neither is modelled anywhere here.
- LSE, Euronext and XETRA all use closing auctions, and the UK small caps this stage
  reaches are quoted wide. The Phase 1 measurement says nothing at all about spread, which
  is the one cost that would matter most in the $1–5m band.

## This is research, not advice

A forecasting exercise over public information. Keep the disclaimer from
`config/pipeline.yaml` on every deliverable.

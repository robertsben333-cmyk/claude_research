# researcher_europe — stage EU

The unpriced-information hunt, run over the **UK, France and Germany pooled**. One
signed number per company (`impact_sum`, points of spot, unbounded) so the day's names
can be **ranked**. No call, no threshold, no direction label. Research only: **this stage
places no orders and reads no broker.**

It exists to ask whether the result the US stage is chasing is a property of the method
or a property of the US market — the same question stage J asks of Tokyo, now asked of a
third market with a different microstructure. Because it uses the same scorer, the same
key and the same measurement window, all three are directly comparable.

Alpaca does not carry LSE, Euronext or XETRA. Execution here is a separate decision to be
made later on Europe's own resolved numbers; what this stage does for that decision is
carry a turnover floor and a shortability signal in the universe, and say below what a
broker would still need.

## Status

**Nothing has resolved. There is no European result, good or bad.**

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
| `SUBMARKET.md` | Phase 1. Why these three, with the counts. **Read it before changing any threshold here.** |
| `scripts/eu_market.py` | what the three markets share and where they differ |
| `scripts/eu_universe.py` | the vendor forward calendar → today's names, USD turnover floor, seeded random draw |
| `scripts/eu_priced_in.py` | the sealed baseline, in the shape `edge_score.py` reads |
| `scripts/eu_positioning.py` | FCA / Bundesanzeiger / (AMF) short registers, the substitute anchors |
| `scripts/eu_resolve.py` | confirmation, realised move, Spearman + permutation p, per-market stats, the language control |
| `researcher_us/scripts/edge_score.py` | **shared** — same scorer for all three markets, so the numbers are comparable |
| `.claude/agents/unpriced-hunter-{uk,fr,de}.md` | the hunters; same output contract, three source worlds |
| `.claude/skills/researcher-europe-hunt/SKILL.md` | the run |
| `LESSONS.md` | what a finding has to carry here, grown from resolved runs |

## Why three markets and not one

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

They peak in different months, so pooling is what turns three seasonal calendars into
one stream. Fridays, August, late December and the German June–July gap are thin
whatever the floor is, and **a thin day is a weak day, not a broken stage**.

**The floor is $200k/day since 2026-09-19, down from $1m, on the operator's
instruction** — the same bar the US and Japanese stages screen on, so the three markets
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

TradingView's public scanner is the forward calendar for all three markets. Against the
actual RNS record over 20 fully scraped days, **90 of its UK rows fell on a scraped day
and 88 had a same-day results announcement from the same issuer — a 2.2% phantom rate.**
The US stage's `time-not-supplied` rows were 20 of 20 phantom on 2026-09-17, so this is a
different object. It is not zero: on a ten-name day 2.2% is one phantom every five days,
and this repo ranked, traded and lost money on TRT, which never reported. `event_occurred:
false` is reachable and the confirmation pass is not optional.

**The confirmation sources differ in strength and the difference is recorded per name:**

- **UK — Investegate**, a full RNS mirror queryable **by date back to 1999**. Stronger
  than Japan's TDnet, which keeps about 31 days: a UK run can be confirmed months later.
- **DE — EQS-News**, the DGAP successor, which serves a non-paginating snapshot of the
  live feed. It confirms today and yesterday and nothing older. Resolve promptly.
- **FR — nothing readable.** Euronext company news is an SPA. A French name that cannot
  be confirmed gets `event_occurred: null`, **never false**: absence of a readable page is
  not absence of a release, and turning an unreadable source into a retrospective kill
  would be inventing a fact.

**The vendor undercounts.** On the 20 sampled days the UK's measured count above $1m/day
of turnover was 5.05 events a day against the 2.3 the vendor's forward calendar gives — a
factor of 2.2. So the stream numbers above are floors. A better forward calendar for
Germany and France is the biggest single improvement available to this stage and it is not
built.

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
turnover, 5–7 at $1–5m, 11–13 at $5–25m and 16–19 above $25m, consistently across all
three markets. The genuinely under-read band is $1–5m — one band *below* MDAX / SBF 120
ex-CAC 40 / FTSE 250. Cutting the universe to it would bake this stage's own thesis into
its universe and make it unfalsifiable. So `analyst_band` rides in every baseline and
`eu_resolve.py` ranks the hunt **by band**. Measure the thesis; do not select on it.

## Each hunter searches English first, then locally — and that is measured too

The hunters run an **English pass**, freeze it as `pre_local`, then run a **local pass**
and revise. `edge_score.py` carries `diagnostics.impact_sum_pre_local` beside the key and
`eu_resolve.py` ranks both against the same realised move, so "searching in German and
French earns rank correlation" is a measured claim and not a belief.

English-only is the coverage the thesis says is already in the price. Local-only throws
away sell-side notes, wire copy and cross-border reporting that genuinely carry
information. Both passes are required.

**The ordering is load-bearing.** English first, then local. Running local first would
measure what English adds to a local reader, which is a different question, and the two
results do not transfer.

**The UK case is degenerate and is reported apart.** Its local language is English, so its
second pass is a **domestic-source** pass — RNS, Investegate, Citywire, Proactive,
Sharecast, the Investors' Chronicle, the domestic trade press — and the variable is source
locality, not language. `pre_local.variable` says which, and `eu_resolve.py` **refuses to
pool** the UK delta with the German and French ones, because averaging them reports the
mean of two different experiments. Be honest about what follows: the UK number measures a
weaker effect, and a UK zero is not evidence about language.

**Nothing pools on one day.** A delta on four to twelve names is noise, the same caveat
`researcher_japan` records for its own `impact_sum_pre_lessons`.

The hunters also carry a second freeze, `pre_lessons`, taken after **both** passes and
before `LESSONS.md` is opened, so the guidance file keeps its own separate control.

## Currencies, holidays and the things that differ per market

- **Currencies.** The UK quotes in pence (`GBp` on Yahoo, `GBX` on the vendor); France
  and Germany in EUR. Moves are in percent so the key is unaffected, but the turnover
  floor is an absolute number and would mean three different things in three currencies.
  **Everything is normalised to USD**, off a live rate, and the rate is written into every
  universe file so the cut is reproducible.
- **Holidays are exchange holidays, not public holidays.** XETRA trades on Fronleichnam
  and Allerheiligen, which a generic German holiday list carries; Euronext Paris is
  shorter than the French jours fériés. Those two are computed from Easter plus a fixed
  list in `eu_market.exchange_holidays()`. The UK is the one case where the public list is
  the exchange list, and `gov.uk/bank-holidays.json` is fetched and cached.
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

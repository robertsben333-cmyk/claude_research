# Edge hunt — 2026-09-04 → 2026-09-08 window

**Five companies, five rankable, zero phantom calendar rows.** Ranked most-positive to
most-negative on `edge_score`. There is no call, no threshold and no direction label in
this note or in `edge-scores.json`, by design.

| # | Ticker | Company | edge_score | edge_pct | confidence | baseline_quality | hunters | clusters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | UNFI | United Natural Foods | **+6.4** | +0.322 | 30.8 | 0.525 | 2 | 3 |
| 2 | WDH | Waterdrop | **+0.1** | +0.004 | 6.7 | 0.240 | 1 | 2 |
| 3 | ABM | ABM Industries | **0.0** | +0.002 | 5.9 | 0.400 | 1 | 2 |
| 4 | CAN | Canaan | **−10.6** | −0.531 | 7.7 | 0.240 | 2 | 2 |
| 5 | GMHS | Gamehaus Holdings | **−11.6** | −0.584 | 11.2 | 0.240 | 1 | 2 |

All five report **2026-09-08 `bmo`**. Every date *and* hour is confirmed from the
company's own press release. Read `edge-scores.json` unfiltered — no cutoff has been
applied and selection is the reader's.

## The score is a ranking key, not a forecast

`edge_score −11.6` does not mean "GMHS falls 11.6%". It means **last of five**. The
whole table spans `edge_pct` **+0.32 to −0.58 points of spot** — nine tenths of one
percent, end to end — against an option-implied event move of **12.02%** on the one
name with a live chain. After an adversary honestly discounted all 27 findings, very
little survived, which is the expected outcome and not a failure.

Compression does not weaken the test. Rank correlation reads order, not magnitude, so a
tightly compressed but strictly ordered table is exactly as falsifiable as a wide one.

**But the order here is only partly strict, and that is the honest caveat.** Three names
are meaningfully separated (UNFI +6.4, CAN −10.6, GMHS −11.6). **WDH and ABM are not** —
+0.1 against 0.0, a gap of 0.002 points of spot. Treat those two as tied, not as ranks 2
and 3. So this day yields roughly **three distinguishable positions across five names**,
a step back from the eight-distinct-scores of the second 2026-08-31 run.

## One day is an anecdote

Five names cannot produce a meaningful rank correlation. `edge_resolve.py` on this run
alone will return a number, and that number will be noise — with n=5 and two of the five
tied, the permutation p-value cannot clear any sensible bar. **The pooled figure across
many days is the result.** Nothing here should be read as evidence the method works or
does not.

## What drives the top and the bottom

### Rank 1 — UNFI, +6.4

The driving finding is the **best-surviving finding of the entire day** at
`priced_in_pct` **30**:

> US Foods' CFO said on 2026-08-13 that his fuel surcharge recovery rate ran "more like
> 70% for the quarter" versus "our typical 30%, 40%", turning an expected 2% fuel
> headwind into "less than half of that", explicitly because high diesel triggered
> additional customer surcharges that only activate at elevated price levels — the same
> tiered-surcharge mechanism UNFI described on 2026-06-09, in a quarter overlapping
> UNFI's 13 weeks to 2026-08-01.

Source: <https://www.fool.com/earnings/call-transcripts/2026/08/13/us-foods-usfd-q2-2026-earnings-call-transcript/> (2026-08-13)

**What the price already says:** nothing directional. There is no 25-delta skew, so the
chain states a 12.02% magnitude and no side. The tape is −4.1% over 5 days and −6.6%
over 20, and every published preview lists fuel as a *downside* risk while none mentions
surcharge recovery.

**What the adversary did to it:** conceded almost everything. It verified the US Foods
quotes verbatim, verified UNFI's own surcharge language, confirmed the read-across is
written nowhere, and noted the tape ran the *other* way ($47.90 on 2026-08-13 to $43.94
now) — i.e. the market spent the three weeks after that call pricing fuel pain, not
relief. Its only attack was on the joint: the transfer from foodservice distribution to
grocery wholesale. It kept its own size at +2.0, identical to the hunter's.

UNFI ranks first **despite five of its nine findings leaning negative**, because the
positive ones survived the adversary far better (`priced_in` 30 and 38) than the negative
ones (55 to 85). That is the adversary pass doing precisely its job.

### Rank 5 — GMHS, −11.6 — and why this rank is unsafe

The driving finding, `priced_in_pct` 55:

> On 2026-08-12 Gamehaus said it will "progressively optimize its third-party publishing
> business in casual titles, and in particular in the social casino category" and manage
> the portfolio "on a cash flow- and profitability-oriented basis… This approach took
> effect during the current quarter" — the quarter for which the 2026-09-08 release will
> issue its forward revenue guide.

Source: <http://www.prnewswire.com/news-releases/gamehaus-announces-strategic-shift-toward-ai-generated-content-302849250.html> (2026-08-12)

**What the price already says:** almost nothing, and this is the interesting part. The
adversary explicitly declined to treat the −5.99% / −5.19% sessions after that release as
evidence of pricing: they ran on **22,908 and 6,192 shares**, about $22k of total
turnover. On that book, "the market has priced this" is not an establishable claim in
either direction.

**But GMHS's rank rests on a baseline row that is wrong, and I verified it.** See below.

## The baseline defect that inverts this day's bottom rank

The GMHS adversary flagged, as unresolved, that the baseline's closest analogue might be
wrong-signed. I checked it against daily bars and **it is**:

| Date | Close | Volume |
| --- | --- | --- |
| 2025-09-08 | 1.73 | 583,200 |
| **2025-09-09** (FY25 annual print) | **2.29** | **22,504,000** |
| 2025-09-10 | 1.86 | 707,500 |

The baseline records that event as **−18.78%**. The actual overnight reaction was
**+32.37%**. The recorded number is the *next day's give-back* of a +32% pop.

The mechanism is a single line. `prior_prints` tags a session from the **EDGAR acceptance
time** (`amc` if at/after 16:00 ET). Gamehaus released at 06:00 ET but furnished its 6-K
later the same day, so the event was tagged `amc`; under `amc`, `reaction()` measures
event-day close → next close, which is 2.29 → 1.86. EDGAR acceptance time is the *filing*
time, not the *news* time, and for a foreign private issuer the 6-K routinely trails the
press release by hours.

**Why it matters for the ranking:** the GMHS hunter reasoned explicitly from "the one
clean analogue was −18.78%" and "all three clean earnings reactions on record are
negative", and ranked the name last of five. The single most heavily weighted item in
that reasoning has the **opposite sign**. Had the row read +32.37%, that hunt would very
plausibly not have been the day's most negative.

**Today's scores have not been changed, deliberately.** Re-running the baseline now —
with the findings already in hand and knowing which way the correction cuts — is exactly
how a scorer gets quietly tuned toward a result, and the sealing rule exists to prevent
it. So GMHS keeps rank 5 in this run's `edge-scores.json`, and this note records that
rank 5 is not trustworthy. `scripts/priced_in.py` now carries
`session_disagrees_with_volume`, which flags the conflict for **future** runs; validated
against GMHS in a scratch directory, it catches this row and no other of the eight.

## Sign balance — the pessimism is recurring

- **Hunts: 6 of 7 leaned negative.** Only UNFI-h2 (+1.8) was positive.
- **Findings: 19 of 27 leaned negative**, 7 positive, 1 exactly zero.

The second 2026-08-31 run was 6 of 8 negative. Two consecutive runs at roughly
three-quarters negative is more plausibly an artefact of **asking hunters to find what
the market has missed going into a print** than a fact about these twelve companies. If
it persists, the hunter prompt is generating pessimism rather than detecting it. Recorded
here so the pattern stays visible across days.

## The two-hunter split earned its cost again

Doubling up on the top two names by `hunt_priority` produced the day's most informative
output, and it exists only because neither hunter could see the other.

- **UNFI: the two hunters returned opposite signs** — h1 at **−3.0**, h2 at **+1.8**,
  from the same sealed baseline and the same window. Hunter dispersion 1.302 points, the
  highest of the day, and it is carried into `uncertainty_pct` rather than hidden by a
  gate. They independently found the *same* undisclosed fact — Matt Echols ceasing as
  Chief Corporate Affairs Officer effective 2026-08-24, visible only in a Form 4 with no
  8-K and no press release — and read it in opposite directions.
- **CAN: the two hunters converged** — −6.0 and −6.5, dispersion 0.605. Convergence is
  also information, and it is only credible because it was unforced.

h2 also **refuted a premise the sweep handed it**: told UNFI had "only 2 published EPS
estimates", it found nine analysts on FY26 and said so. A hunter contradicting its own
brief is the system working.

## What the adversary broke

All **27 of 27** findings carry a number, verified by `edge_brief.py --check`. The pass
judged both sides on every name. It produced **eight factual corrections**, which is a
different and more useful statement than "already priced":

**Refuted outright:**

1. **ABM#0** — the claim's own framing was wrong. Two of its three carriers cut guidance
   *before* ABM last guided (American 2026-04-23, Alaska April 2026, against ABM's
   2026-06-05), and American's route suspensions run 2026-08-05 to 2026-10-05, i.e. ABM's
   fiscal **Q4, not Q3**. ABM's own page says 800+ buses, not 1,000+.
2. **ABM#1** — "a stock that has not participated at all" is false. ABM set its 52-week
   high of $50.12 in late July, the same fortnight as the Comfort Systems and EMCOR
   prints, and traded $49.36 on 2026-07-30.
3. **GMHS#1** — sized the $200m shelf at "4.5x the market cap". The **cover page of the
   hunter's own source** states the Form F-3 General Instruction I.B.5 limitation:
   primary sales are capped at one third of a $23.5m non-affiliate float, roughly
   **$7.8m**, about 17% of market cap. Overstated by ~25x, refutable from page one of the
   cited document.
4. **UNFI-h2#3** — misquoted the investor-day target. The actual language is "~$800
   million target for **fiscal 2028**", not a FY24–FY27 target, so it obliges FY27 growth
   of +3% to +7% rather than the "flat FY27" the claim inferred.
5. **UNFI-h1#2** — "at least $40mm of one-off cyber insurance cash" double-counts. The
   same release shows $40mm of recoveries offset by $22mm of costs, which is why the
   reconciliation line reads ($18mm). Net flattering is ~$18mm, not $40mm.
6. **CAN-h2#0** — rested partly on an **investing.com page carrying an auto-populated Q2
   revenue "actual" of $31.20m for an event that has not happened**, mislabelled period
   09/2026, on a table whose EPS column is off ~7x for this issuer's Q1 2026. Struck as
   evidence. The underlying claim (consensus never marked to the company's $35–45m guide)
   partly survives on stockanalysis.com's independent $269.23m FY consensus.
7. **CAN-h1#2** — citation error: the 2026-07-31 hashrate-recovery data is in the
   2026-08-17 6-K, not the 2026-07-14 filing it was attributed to.
8. **GMHS#3** — "no company filing or press release on or around" 2026-08-31 is
   contradicted by a 6-K filed 2026-08-28, the immediately preceding session, which is a
   live candidate explanation for the spike the finding calls unexplained.

**Conceded the fact, rejected the sign or the size** — a distinct verdict, kept separate:
ABM#0 (facts conceded, the bridge from airline EPS to ABM's per-turn billing rejected),
CAN-h1#0 and CAN-h2#1 (encumbrance figures verified exactly, but BTC at $77.9k on
2026-09-03 against $58.5k at 2026-06-30 *improves* the pledge coverage, so the fact cuts
less hard now than when published), WDH#0 (every number verbatim correct, but it restates
management's *own* published 2026 guidance of ~40% growth with flat operating profit, so
it is not a discovery).

**Best survivor:** UNFI-h2#0 at `priced_in_pct` **30** (above). The only other finding
below 40 is UNFI-h2#1 at 38 (an expiring $109m buyback authorisation), and GMHS#3 at 30,
which carries zero directional size by construction.

The adversary also caught a **collapse the scorer would otherwise have double-counted**:
five of CAN's eight findings rest on the single 2026-05-19 Q1 release, and it named which
keys collapse into which.

## How much of the baseline was measured rather than inferred

This is the day's structural weakness and it is worse than on 2026-08-31.

- **Option chain: 1 of 5.** Only UNFI has a usable chain, and even that is marked
  *indicative only* — the ATM bid-ask spread is **39% of mid** on 1,765 contracts of
  front-expiry open interest. ABM's chain exists but the spread is **188% of mid** on 93
  contracts total, so it is discarded. WDH and GMHS have **no options market at all**;
  CAN's legs are not two-sided. `options` quality: UNFI 0.357, the other four **0.000**.
- **Market-implied direction: 0 of 5.** No name carries a `skew_25d_vol_points`. So
  `priced_direction` is **0.0 for every name**, which alone caps `baseline_quality` at
  0.75 no matter how good the rest is. The day's best is UNFI at 0.525.
- **Therefore `priced_lean_pct` is inferred for all five**, from the −0.05 × 20-day
  run-up fallback. The agreement discount (×0.55 when a finding agrees with the priced
  lean) fired on **UNFI, ABM, CAN and GMHS** against a lean derived from a *run-up*, not
  from anything the options market said. For CAN that lean is **−3.49%**, by far the
  largest, purely because the stock is +69.8% over 20 days — so CAN's negative findings
  were halved for "agreeing with the price" when the price has stated no direction at
  all. That is much weaker evidence of what is priced than the rule assumes.
- **Reaction history trustworthy: 2 of 5.** Only ABM and UNFI sit on exact 8-K item 2.02
  acceptance times. CAN (13-day median gap, monthly bitcoin-production 6-Ks), GMHS (3 of
  8 rows outside any reporting quarter, one tagged `intraday`) and WDH (three 6-Ks inside
  one quarter) are all the 6-K text-matcher defect.

A ranking built on four names with no chain and five names with no skew is measuring
something considerably weaker than "what the market priced".

## The clustering rule penalises primary-source work

`edge_score.py` clusters findings by **source domain**. Every SEC filing — a Q1 release,
a production 6-K, an F-3 cover page, a Form 4 — is `sec.gov`, one cluster, and within a
cluster only the largest single residual survives.

The effect on CAN: five findings drawn from **five distinct primary documents** collapsed
to one number. A hunter that works filings is penalised relative to one that cites five
different news sites, which is backwards — primary filings are the better evidence. It is
visible in the day's cluster counts: UNFI reached `k=3` largely because two of its
findings happened to sit on `eia.gov` and an aggregator.

**Not changed in this run.** Altering the scorer with today's findings in hand, knowing
it would raise CAN, is the same contamination as re-running the baseline. Recorded as a
design question for a future run: cluster on the document, not the domain.

## Names that could not be ranked

**None.** All five carry `rankable: true` — every event was confirmed, every name was
hunted, and no baseline came back `suspect`. The sweep killed nothing, because for the
second consecutive run the phantom rate was **zero**.

Withholding `--include-unknown` is what produced that. All 12 of today's Friday `amc`
calendar rows were `time-not-supplied` and were dropped; on the first 2026-08-31 run,
eight of eight such rows had no earnings event at all.

## Two things about the window worth recording

**A holiday bug, found and fixed before the universe was built.** `edge_universe.py
--window` skipped weekends but not NYSE holidays, so on the Friday before Labor Day it
resolved to **Monday 2026-09-07 — a closed market** — and returned **0 of 19 calendar
rows**. An empty universe would have looked exactly like a thin day and this run would
have stopped cheaply and wrongly. `get_earnings.py` already had `next_trading_day()`; the
window now uses it, and resolves 2026-09-04 `amc` + **2026-09-08** `bmo`.

**One baseline was amended before any hunter launched, and it was a downgrade.** WDH went
`fits_cadence` → `unknown`: its 85-day median gap is computed over a filing set holding
three 6-Ks inside one quarter, and the verdict read "last print 2026-07-24", which would
make 2026-09-08 a second print in the same quarter. CAN and GMHS were **deliberately not
upgraded** despite company-confirmed dates, because in both the matcher caught
non-earnings filings — the event is real but its history does not characterise it.
Net: one name lost an event multiplier it had not earned, none gained one.

The WDH hunter and the WDH adversary then both worked the same question independently and
**refined the amend**: the true last earnings print is **2026-06-17** (Q1 2026, +2.34%),
not 2026-07-24, making the gap to 2026-09-08 **83 days against an 85-day median** — so
the cadence axis in fact fits cleanly, and six of the eight rows are earnings rather than
five. The `unknown` verdict is therefore conservative on that specific axis, while the
median remains built on a contaminated set. Not re-amended mid-run, for the same reason
as above; it is the right starting point for the next run on this name.

## Spend

13 subagents against an `edge_hunt` cap of 20: 1 sweep + 7 hunters (2 each on UNFI and
CAN, 1 each on ABM, WDH, GMHS) + 5 adversaries, one per ticker. **Nothing was shed** and
no degradation step was taken.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.

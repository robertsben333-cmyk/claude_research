# Edge hunt — 2026-09-09 `amc` + 2026-09-10 `bmo`

**One signed number per company, so the day can be ranked. No call, no threshold, no direction label.**

Ranking key, as `edge-scores.json` names it in its own `ranking_key` field: **`impact_sum`**, in points of spot.
Beside it travels `conviction` (its absolute value), which is where the direction skill lives.

Window: 22 companies confirmed reporting between tonight's close and tomorrow's open. 8 were hunted; 14 sit
out of the ranking as `rankable: false` for budget, with the reason stated. 37 findings, every one judged by
an adversary. Join verified clean: 37 findings, 37 verdicts, nothing silently dropped.

---

## The ranking

| # | Ticker | `impact_sum` | `conviction` | ≥ floor (3.0) | control `-run_up_20d` | turnover $/day | chain |
| --- | --- | ---: | ---: | :---: | ---: | ---: | :---: |
| 1 | NAVN | **+9.75** | 9.75 | yes | +7.19 | $58.1m | live |
| 2 | AVAV | **+3.25** | 3.25 | yes | +26.73 | $179.4m | live |
| 3 | FLWS | **+1.50** | 1.50 | — | +11.88 | $0.71m | live |
| 4 | LMNR | **+1.50** | 1.50 | — | −7.65 | $0.93m | live |
| 5 | SKIL | **−2.50** | 2.50 | — | +29.22 | $0.29m | none |
| 6 | LSAK | **−3.35** | 3.35 | yes | +5.38 | $0.38m | none |
| 7 | KEQU | **−10.50** | 10.50 | yes | +0.52 | $0.07m | none |
| 8 | WLTH | **−15.50** | 15.50 | yes | −0.57 | $12.4m | none |

Not ranked (`no hunt`, shed for budget): AEO, COO, CULP, DBI, GLOO, IMPP, LAKE, LOVE, M, MCFT, SHOE, TEN, VNCE, YB.
They are in `edge-scores.json` with `rankable: false` rather than sorted into the table on a 0.

**Read the order, not the sign.** Below the conviction floor the sign of `impact_sum` has been a coin flip on
the evidence so far — 53% over 38 resolved events. Above it, the *rank* of conviction predicted whether the
sign was right at ρ=+0.514 (permutation p=0.0015). Five names here clear the floor: NAVN, AVAV, LSAK, KEQU,
WLTH. FLWS at +1.50 and LMNR at +1.50 are not a bullish view on either company; they are the middle of the
table, and reading them as one is the specific mistake this paragraph exists to prevent.

**`impact_sum` is not a forecast of the move.** It sums findings, and the same fact often appears in two
findings from two sources. See the double-counting section below — on this day that is not a theoretical
caveat.

---

## What drives the top and the bottom

### NAVN +9.75 — top of the table

Driving finding (`NAVN-h1#0`, sized +2.75, adversary `priced_in_pct` **72**): Navan guided fiscal Q2 to
$219–221m, flat sequentially on Q1's $220m, while the only observable prior year grew ~+9% over the same two
fiscal quarters; consensus of $220.5m sits on the guide midpoint to within $0.5m, i.e. the street modelled the
guide rather than the company's own seasonality.
Source: https://investors.navan.com/news-releases/news-release-details/navan-announces-third-quarter-fiscal-year-2026-results

The second-largest (`NAVN-h2#0`, +2.50, `priced_in_pct` 66) is independent in source: US airline-fare CPI ran
+26.2% y/y across May–July (Navan's fiscal Q2) against +14.2% across Feb–April, and Navan's revenue is a take
rate on booking dollars. Source: https://www.bls.gov/news.release/cpi.nr0.htm

**What the price already says:** the baseline is not agreeing. NAVN is −7.19% over twenty sessions with a
25-delta skew of +5.64 (puts bid) into a 14.06% option-implied move. Both hunters found the same tension and
neither could see the other. The adversary priced the cluster at 62–82 and did not break the arithmetic.

### WLTH −15.50 — bottom of the table

Driving finding (`WLTH-h1#0`, sized −5.50, `priced_in_pct` **55**): building fiscal Q2 revenue bottom-up from
Wealthfront's own published May and June monthly asset disclosures at the company's own last-reported take
rates lands near $94.5m against a consensus near $98m, while consensus EPS still implies a doubling off Q1's
$0.07. Source: https://www.sec.gov/Archives/edgar/data/1524566/000162828026040793/q127earningsrelease.htm

The lowest-`priced_in` finding on the name (`WLTH-h1#2`, −5.25, **50**) is the reaction-function claim: the
January print beat on EPS and the stock still fell 16.8% on a deposit outflow, and July and August flows are
both released for the first time tonight.

**What the price already says:** almost nothing usable. WLTH has no functioning option chain — a few hundred
contracts and an ATM spread wider than the mid — so the baseline's 14.35% "expected move" is the median of
three prior reactions, not a priced expectation, and there is no skew to check against. The stock ran +8.97%
in five sessions into the print on no company news.

---

## The control has its own line, and it is not beaten here

`-run_up_20d_pct` — one number off the sealed baseline, available before a single subagent was spawned —
ranks these eight names: **SKIL, AVAV, FLWS, NAVN, LSAK, KEQU, WLTH, LMNR.**

The hunt's ranking is **NAVN, AVAV, FLWS, LMNR, SKIL, LSAK, KEQU, WLTH.**

The two agree on AVAV and FLWS near the top and disagree sharply on the extremes: the control puts SKIL first
where the hunt puts it fifth, and puts LMNR last where the hunt puts it fourth. WLTH is bottom on the hunt and
seventh on the control. So the hunt is not merely re-deriving the control — but over the six resolved runs so
far that free number ranked at ρ=0.335 against the hunt's raw 0.407, a gap of 0.080 whose confidence interval
spans zero. **The stage has not been shown to beat it.** A day on which the hunt's order differs is not
evidence that the difference is information.

---

## Sign balance

Ten hunts across eight names. **Six leaned negative, four positive** — NAVN (×2), AVAV and FLWS positive;
WLTH (×2), LMNR, SKIL, LSAK, KEQU negative. At name level `impact_sum` splits 4 positive / 4 negative.

This is the same tilt recorded on 2026-08-31 (six of eight negative) and it remains more plausibly an artefact
of asking hunters to find what the market has *missed* into a print than a fact about these companies. Worth
watching across days; a single day cannot separate the two.

One internal inconsistency to flag: **LMNR's hunter wrote a summary `expected_move_pct` of −2.5 while its own
findings sum to +1.50.** The scorer uses the findings, correctly, but the hunter's narrative and its arithmetic
disagree in sign, and a reader of the hunt file alone would take away the opposite of the table.

---

## What the adversary broke

The pass judged all 37 findings on both sides. Median `priced_in_pct` **72**, mean 69.9, range 44–92. Only
three findings scored ≤50; eleven scored ≥80.

**Factually refuted:**

- `LMNR-h1#2` → **92**. The hunter read the December 2025 amendment as deferring Limoneira's debt-service
  coverage covenant to a test on 31 October 2026, six weeks after the fiscal year end. The adversary read the
  amendment as deferring it to **October 2027**. If the adversary is right the finding's entire mechanism is a
  year away and does not reach this print. This is the cleanest factual break of the day.
- `FLWS-h1#1` → **82**. The hunter claimed the short base "has not moved all year". Its own cited source shows
  9.30m shares on 13 March against 7.75m on 14 August. The claim is contradicted by the document it rests on.
  The same finding also **re-reported four fields of the sealed baseline** — total open interest, put/call
  ratio, ATM spread, average volume — as though they were discovered, which is not a finding at all.

**Conceded but sign-refused, which is a different thing:**

- `AVAV-h1#1` → **88**, with `reaches_this_print: false`. The BlueHalo lock-up schedule is real and genuinely
  unpublished; the adversary's objection is that it does not touch tonight's numbers.
- `WLTH-h2#3` → **88**. The September rate-hike odds are real and favourable, but wire-covered, visible in the
  +8.97% five-day run-up, and they do not reach a quarter that ended 31 July.

**Survived best:** `SKIL-h1#1` at **44** — the CFO-transition calendar (new CFO started 2026-05-20, the
outgoing CFO's advisory contract expired 2026-09-04, five days before the first quarter the new CFO can fully
own). Second, `LMNR-h1#3` at **45** — Interior's post-2026 Colorado River Record of Decision, issued 19 days
before this print, against Limoneira's stated intent to monetise Class 3 water rights in fiscal 2026. Neither
appears in any financial coverage of either company.

One genuine concession worth recording: on LSAK the adversary accepted that the link between the 30 June
goodwill impairment test and management's standing first-profitable-year promise is unpublished, while still
pricing the surrounding narrative at 60–80.

---

## Double-counting: the adversary found it in eight names of eight

This is the most important caveat on today's table. **Every one of the eight adversaries independently reported
that findings on its name rest on shared documents or mirror each other**, and `impact_sum` sums them anyway:

- **NAVN** — three duplicate pairs, including two findings reading the same Form 4 accession in opposite directions.
- **LMNR** — three of four rest on the same two 2026-06-09 filings; two are direct mirrors of one carton table,
  arguing opposite signs.
- **SKIL** — two findings on one SEC accession; two more point opposite ways on the same revenue line.
- **KEQU** — the breakeven arithmetic already assumes the gross margin that the steel finding then compresses
  again, charging the same margin twice.
- **AVAV** — the P550 and E-HEL findings are one fiscal-calendar observation applied twice with the sign flipped.
- **WLTH**, **FLWS**, **LSAK** — same pattern, recorded in each `interactions` field.

The cluster-max was built to stop exactly this, and `docs/EDGE_ANALYSIS.md` demoted it because it *lowered* the
measured rank correlation over six runs. That demotion is a measurement and stands. But today's evidence is that
the thing it was built to catch is present in 8 of 8 names, so the shipped key is summing acknowledged
duplicates by design. Both facts are true at once, and the resolution needs more resolved days, not a decision
taken here. `diagnostics.residual_sum` and `edge_score_legacy` are in the JSON for whoever runs that test.

**A discrepancy between the code and its own documentation, flagged rather than fixed.** `SKILL.md` and
`edge_score.py`'s docstring both describe `impact_sum` as "the hunters' signed per-finding sizes, added up".
The code does not do that: where the adversary returned a `size_check_pct`, the finding is re-sized to the
**mean of the hunter's number and the adversary's independent estimate** before summing
(`scripts/edge_score.py:206–211`). Today that mattered — the median hunter/adversary size disagreement was 0.5
points but the maximum was **11.0** (`KEQU-h1#0`: hunter −4.0, adversary −15.0, booked at −9.5), and KEQU's
rank depends on it — on the hunter's own number alone KEQU's `impact_sum` would be far smaller and it would not
sit seventh. Nothing was changed in this run; the two descriptions need reconciling by someone who can
check which version `docs/EDGE_ANALYSIS.md` measured at ρ=0.407.

---

## How much of the baseline was measured rather than inferred

**Four of the eight hunted names have a live option chain** — NAVN (14.06% implied), AVAV (11.87%),
FLWS (19.71%), LMNR (6.12%). The other four (SKIL, LSAK, KEQU, WLTH) have none, so `priced_lean_pct` falls back
to −0.05 × the 20-day run-up and the baseline's "expected move" is a historical median rather than a priced
expectation. Across the full 22-name window only 7 had a chain.

Four of eight is better than the 3-of-10 on 2026-08-31, and it is not an accident: **one name was swapped into
the hunt set specifically to raise it** (see the deviation note below). It is still the case that half this
ranking rests on names where "what the market priced" was inferred, not measured. Note also that FLWS's 19.71%
implied move is computed off a 6,544-contract chain with an ATM spread at 67% of mid — it is a number, not a
statement.

`edge_resolve.py` normalises by the expected move, so for four of these eight names the normalised correlation
is against a historical median. It is not an implied-move measure and should not be described as one.

---

## What this day would cost to trade

Capacity is not in the scorer and not in the budget, and on this day it is severe.

| | turnover | note |
| --- | ---: | --- |
| AVAV (rank 2) | $179.4m/day | tradeable at size |
| NAVN (rank 1) | $58.1m/day | tradeable at size |
| WLTH (rank 8) | $12.4m/day | tradeable |
| LMNR (rank 4) | $0.93m/day | below $1m |
| FLWS (rank 3) | $0.71m/day | below $1m |
| LSAK (rank 6) | $0.38m/day | below $1m |
| SKIL (rank 5) | $0.29m/day | below $1m |
| KEQU (rank 7) | **$0.07m/day** | ~2,000 shares; effectively untradeable |

**Only three of eight names clear $5m/day.** Five trade under $1m, and KEQU — which carries the second-largest
conviction in the table at 10.50 — turns over $70,000 a day and 368 shares changed hands on the session before
the print. A long top-third / short bottom-third book on this table would be long NAVN and AVAV and short KEQU
and WLTH; the KEQU leg does not exist at any meaningful size.

Worse, this is structural rather than bad luck. The shed to eight names was made on the sweep's `hunt_priority`,
which scores *room for something unpriced to exist* — and that is close to a measure of obscurity. It
systematically selected the illiquid tail and dropped the four largest, most liquid names in the window (M at
$115.7m/day, COO $108.5m, AEO $85.5m, and SHOE $10.6m). **The selection rule and the capacity constraint pull
in opposite directions, and nothing in the pipeline currently notices.**

---

## Names that could not be ranked, and why

All 14 were shed for **budget**, not for doubt about the event. The sweep confirmed **22 of 22** companies from
a company source — press release, IR page or 8-K exhibit — with **zero phantom calendar rows** and zero
unsettled sessions. That is the best confirmation rate any run of this stage has recorded, and it is structural:
this universe is made up of companies that pre-announce their reporting date and hour by wire.

Shed, in `hunt_priority` order: LAKE (71), SHOE (66), CULP (65), LOVE (64), GLOO (62), VNCE (61), MCFT (60),
IMPP (57), TEN (55), DBI (52), YB (48), AEO (44), COO (35), M (30).

Three things the sweep established that a later run should not have to rediscover:

- **SHOE's empty baseline is a bookkeeping artefact.** CIK 895447 is Shoe Carnival, renamed Shoe Station Group
  on 2026-06-11; `priced_in.py` discarded 105 prior prints as a predecessor entity. The history is recoverable.
- **GLOO and IMPP carry `cadence_implausible` and both events are real.** The flag correctly identified
  contaminated reaction histories — non-earnings 6-K/8-K filings read as prints — and incorrectly cast doubt on
  the dates. `baseline_history_trustworthy: false` on both; the flag is doing its job on history, not on dates.
- **Two consensus rows look mis-keyed rather than bearish**: CULP at $0.44 against −$0.02 a year ago on one
  estimate, and LAKE at −$0.02 against $0.36. Both single-estimate rows.

No baseline needed amending: no name in this run carried a `suspect` `event_plausibility` verdict, so nothing
was arithmetically barred from ranking. `edge_baseline_amend.py` exited non-zero on a stale per-run table
(CRMT/SUNB/YQ, from an earlier run) — the guard working as designed.

---

## One day is an anecdote

Eight names cannot produce a meaningful rank correlation. Nothing in this note is a result. The pooled figure
across many days is the result, and `scripts/edge_resolve.py --pool` is where it lives.

Two standing cautions that apply to this table as much as to any other:

- Over the six resolved runs, `edge_score`'s successor key has **not been shown to beat `-run_up_20d_pct`**, a
  number that costs nothing and is available before any agent runs. Until it does, the hunt has not been shown
  to add anything.
- The de-duplicated sample is 38 events over five independent days, and the raw impact sum's ranking p-value,
  corrected for the thirteen candidate statistics it was chosen from, is 0.056. That is a lead to run forward,
  not a finding.

Resolve this run after the 2026-09-10 close for the `amc` names and the 2026-09-11 close for FLWS:

```bash
python3 scripts/edge_resolve.py --run research/2026/09/2026-09-09/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'
```

Note that 2026-09-08's eight names are also awaiting resolution, and that five rows across 09-04 and 09-07 are
known duplicates — `--pool` double-counts them.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market
positioning, guidance, macro conditions, and management commentary rather than reported results alone.*

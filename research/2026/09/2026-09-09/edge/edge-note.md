# Edge hunt — 2026-09-09 `amc` + 2026-09-10 `bmo`

**One signed number per company, so the day can be ranked. No call, no threshold, no direction label.**

Ranking key, as `edge-scores.json` names it in its own `ranking_key` field: **`impact_sum`**, in points of
spot — the hunters' signed per-finding sizes, added up. Beside it travels `conviction` (its absolute value).

**All 22 companies in the window were hunted.** 24 hunts, 89 findings, 22 of 22 rankable. This is the first
run of this stage to cover its whole universe rather than a budget-selected subset.

---

## The ranking

| # | Ticker | `impact_sum` | `conviction` | ≥ floor (3.0) | hunters | findings | control `-run_up_20d` | turnover $/day | chain |
| --- | --- | ---: | ---: | :---: | :---: | ---: | ---: | ---: | :---: |
| 1 | NAVN | **+10.00** | 10.00 | yes | **2** | 6 | +7.19 | $58.1m | live |
| 2 | LOVE | **+5.50** | 5.50 | yes | 1 | 4 | +8.24 | $2.60m | — |
| 3 | VNCE | **+4.50** | 4.50 | yes | 1 | 3 | −9.50 | $0.62m | — |
| 4 | DBI | **+3.00** | 3.00 | yes | 1 | 4 | +16.75 | $2.59m | — |
| 5 | AVAV | **+2.50** | 2.50 | — | 1 | 3 | +26.73 | $179.4m | live |
| 6 | FLWS | **+2.50** | 2.50 | — | 1 | 4 | +11.88 | $0.71m | live |
| 7 | COO | **+1.40** | 1.40 | — | 1 | 3 | +12.30 | $108.5m | live |
| 8 | CULP | **+1.40** | 1.40 | — | 1 | 4 | +0.58 | $0.06m | — |
| 9 | TEN | **+1.30** | 1.30 | — | 1 | 5 | −14.13 | $10.25m | — |
| 10 | LMNR | **0.00** | 0.00 | — | 1 | 4 | −7.65 | $0.93m | live |
| 11 | AEO | **−1.00** | 1.00 | — | 1 | 3 | +0.78 | $85.5m | live |
| 12 | M | **−1.10** | 1.10 | — | 1 | 2 | +8.14 | $115.7m | live |
| 13 | IMPP | **−2.00** | 2.00 | — | 1 | 4 | −17.77 | $2.00m | — |
| 14 | LAKE | **−2.70** | 2.70 | — | 1 | 4 | +6.75 | $0.55m | — |
| 15 | LSAK | **−2.70** | 2.70 | — | 1 | 3 | +5.38 | $0.38m | — |
| 16 | SKIL | **−3.00** | 3.00 | yes | 1 | 4 | +29.22 | $0.29m | — |
| 17 | SHOE | **−3.50** | 3.50 | yes | 1 | 4 | +15.16 | $10.55m | — |
| 18 | GLOO | **−4.00** | 4.00 | yes | 1 | 5 | +3.76 | $0.35m | — |
| 19 | MCFT | **−4.00** | 4.00 | yes | 1 | 3 | +6.20 | $3.73m | — |
| 20 | YB | **−4.50** | 4.50 | yes | 1 | 4 | +2.69 | $0.31m | — |
| 21 | KEQU | **−5.00** | 5.00 | yes | 1 | 4 | +0.52 | $0.07m | — |
| 22 | WLTH | **−10.50** | 10.50 | yes | **2** | 9 | −0.57 | $12.4m | — |

Eleven of 22 clear the conviction floor. Below it the sign of `impact_sum` has been a coin flip on the
evidence so far (53% over 38 resolved events); above it the *rank* of conviction predicted sign-correctness
at ρ=+0.514 — but see the very next section before relying on that.

**`impact_sum` is not a forecast of the move.** It sums findings, and the same fact frequently appears twice.

---

## Read this before the table: the two extremes are partly an artefact

**NAVN and WLTH are the only two names hunted by two agents, and they are ranks 1 and 22.** They are also
the only two names in the entire table outside ±5.5.

| | mean `conviction` | max `conviction` |
| --- | ---: | ---: |
| the 2 double-hunted names | **10.25** | 10.50 |
| the 20 single-hunted names | **2.78** | 5.50 |

`impact_sum` is a *sum over findings*, so a name with two independent hunters contributes roughly twice as
many findings and lands roughly twice as far from zero. NAVN sums 6 findings and WLTH sums 9; every other
name sums 2 to 5. The two extremes of today's ranking are therefore substantially a function of **how many
agents were pointed at the name**, not of how much unpriced information was found.

This is not a hypothetical. `config/pipeline.yaml` set `double_hunt_top_n: 2` when this run started and
`0` by the time it finished (commit `a109692`, "remove the adversary outright and the double hunt with it"),
so the design has already moved away from it — but today's table was built under the old rule and carries
the artefact.

**And it may contaminate the headline historical result.** Every one of the six resolved runs used the same
double-hunt on its top names by `hunt_priority` — `SPWH-a/-b` on 09-01, `MEI-1/-2` on 09-02, `SWBI-a/-b` on
09-03, `UNFI` and `CAN` on 09-04, `UNFI-a/-b` on 09-07, `YQ-a/-b` on 09-08. So in every day of the pooled
sample, the highest-priority names also carry mechanically the largest `conviction`. The finding that "the
rank of conviction predicts whether the sign was right" (ρ=+0.514, permutation p=0.0015) is therefore
confounded with hunter count and with `hunt_priority` selection, and cannot be read as a pure statement
about conviction until that is separated. **This is the single most consequential thing in this note and it
is a defect in the measurement, not a result about today.** The test is cheap: re-run
`edge_decompose.py` normalising `impact_sum` by hunter count, or restricted to single-hunted names only.

---

## Nothing checked the findings

**There was no adversary pass on this run.** The stage's design changed today: the adversary became a weekly
audit (`5e44be2`) and was then removed outright (`a109692`). Today is Wednesday, not the audit day, and the
run was instructed not to run it.

Eight names — NAVN, WLTH, AVAV, FLWS, LMNR, SKIL, LSAK, KEQU — carry adversary verdicts from earlier in this
same run, made before the design changed. **The other fourteen have had no factual check of any kind.**

That asymmetry matters because on the eight that were checked, the adversary broke two findings on facts:

- `LMNR-h1#2` (`priced_in` 92) — the hunter read a December 2025 amendment as deferring Limoneira's
  debt-service covenant to a test on 31 October 2026. The adversary read the same amendment as deferring it
  to **October 2027**, a full year later, which puts the mechanism outside this print entirely.
- `FLWS-h1#1` (`priced_in` 82) — the hunter claimed the short base "has not moved all year"; its own cited
  source shows 9.30m shares on 13 March against 7.75m on 14 August. The same finding also re-reported four
  fields of the sealed baseline as though they were discoveries.

Two factual breaks in 37 checked findings is roughly a 5% error rate. Applied to the 52 unchecked findings on
the other fourteen names, the expectation is **two or three more errors of that kind sitting in this table
undetected**. Nothing in the pipeline will find them. `diagnostics.residual_sum` reads `n/a` for those
fourteen names for the same reason, and is not comparable across the two groups.

---

## What drives the top and the bottom

Because the two extremes are double-hunted, the honest illustrations are the largest **single-hunted** names
at each end.

### LOVE +5.50 — top of the single-hunted names

Driving finding (`LOVE-h1#0`, +4.5): Lovesac told its 11 June call it had been accepted for **$20.8m** of
IEEPA tariff refunds but had received only $3.6m, and put only that $3.6m into the guide — while CBP-wide
payout data show the wave ran through exactly Lovesac's fiscal Q2 (4 May – 2 Aug). Williams-Sonoma, with the
same 2 August quarter end, says substantially all of its $197.8m claim was collected by then; Arhaus had
$37.8m in hand by 6 August.
Source: https://www.fool.com/earnings/call-transcripts/2026/06/11/lovesac-love-q1-2027-earnings-transcript/

**What the price already says:** the opposite. LOVE carries a 25-delta skew near **+30.5**, the most extreme
in the universe — puts heavily bid — with a 24.85 put/call open-interest ratio and 20.8% of float short. The
finding cuts squarely against that positioning, which is what makes it interesting and also what makes it
risky.

### KEQU −5.00 — bottom of the single-hunted names

Driving finding (`KEQU-h1#0`, −4.0): Kewaunee ran a book-to-bill near **0.83 for all of FY26** — backlog fell
$214.6m → $205.0m → $192.9m → $183.2m → $165.9m across five consecutive quarters while quarterly revenue was
held flat near $70m — and the 10-K commits ≥90% of the 30 April backlog to shipping in FY27, i.e. ≥$149m
against $282m of FY26 revenue.
Source: https://www.sec.gov/Archives/edgar/data/55529/000005552926000020/kequ-20260430.htm

**What the price already says:** very little that is legible. No option chain, no conference call, one
estimate, and roughly 2,000 shares a day of volume. The 20-day run-up is −0.52%, i.e. flat.

---

## The control has its own line, and it is not beaten here

`-run_up_20d_pct` — one number off the sealed baseline, available before any subagent was spawned — ranks
the 22 names: **SKIL, AVAV, DBI, SHOE, COO, FLWS, LOVE, M, NAVN, LAKE, MCFT, LSAK, GLOO, YB, AEO, CULP,
KEQU, WLTH, LMNR, VNCE, TEN, IMPP.**

The hunt's order differs sharply. SKIL is the control's best name and the hunt's 16th. VNCE is the hunt's 3rd
and the control's 20th. TEN is the hunt's 9th and the control's 21st. Only LOVE, AVAV and DBI sit high on both.

Over the six resolved runs that free number ranked at ρ=0.335 against the hunt's raw 0.407, a gap of 0.080
whose confidence interval spans zero. **The stage has not been shown to beat it.** A day on which the two
orders disagree is not evidence that the disagreement carries information.

---

## Sign balance

**Twelve of 22 names are negative, nine positive, one exactly zero.** At hunt level, 14 of 24 hunts leaned
negative. That is a milder tilt than the 6-of-8 recorded on 2026-08-31 and the 6-of-10 on the first eight
names today, and it is the first time this stage has had a full universe to measure it on. It remains more
plausibly an artefact of asking hunters to find what the market has *missed* into a print than a fact about
these 22 companies.

Two internal inconsistencies worth flagging, both cases where a hunter's own summary disagrees with its
findings:

- **LMNR** wrote `expected_move_pct` −2.5 while its four findings sum to exactly **0.00**.
- **GLOO** wrote −4.0 and its findings sum to −4.00, but it also explicitly contradicted its sealed baseline,
  arguing the four "prints" the baseline flagged as contaminated are in fact genuine company disclosures. It
  may be right; nothing checked it.

---

## How much of the baseline was measured rather than inferred

**Seven of 22 names have a live option chain** — NAVN (14.06% implied), AVAV (11.87%), FLWS (19.71%), COO
(8.72%), AEO (13.33%), M (7.73%), LMNR (6.12%). The other fifteen have none, so `priced_lean_pct` falls back
to −0.05 × the 20-day run-up and the baseline's "expected move" is a historical median rather than a priced
expectation.

So **two thirds of this ranking rests on names where "what the market priced" was inferred, not measured**,
and `edge_resolve.py` normalises by that expected move — for fifteen of these names that is a historical
median, and the normalised correlation must not be described as an implied-move measure.

Three hunters found defects in their own sealed baselines, and two share one root cause worth fixing:

- **AEO and DBI**: `priced_in.py` discarded 30 and 31 genuine prior prints respectively because EDGAR lists a
  `formerNames` entry whose name string is **identical to the current name** — a cosmetic registrant-record
  refresh, not a predecessor entity. Both names came back with `event_plausibility: unknown` and a degraded
  `baseline_quality` as a direct result. A normalised string comparison before discarding history fixes it.
- **SHOE**: same empty history, but legitimately — CIK 895447 really was renamed from Shoe Carnival on
  2026-06-11. Those 105 prints are recoverable under SCVL, and the hunter reconstructed a ~6% base rate from
  them.
- **SHOE** also reports that the baseline's put/call open-interest ratio of 26.6 on 28,591 contracts — the
  loudest single number in the sweep — is a vendor artefact, most likely stitched across the ticker change.
  The real chain carries a few hundred contracts.
- **GLOO** and **IMPP** carry `baseline_history_trustworthy: false`; IMPP's hunter confirmed only about three
  of eight recorded "prints" are earnings, the rest being vessel, offering and proxy 6-Ks.

---

## What this day would cost to trade

**Only 8 of 22 names clear $5m/day of turnover. Ten trade under $1m.**

The extremes are the problem, as usual. A long top-third / short bottom-third book would be long NAVN
($58.1m), LOVE ($2.6m), VNCE ($0.62m), DBI ($2.6m), AVAV ($179.4m), FLWS ($0.71m), COO ($108.5m) and short
WLTH ($12.4m), KEQU ($0.07m), YB ($0.31m), MCFT ($3.7m), GLOO ($0.35m), SHOE ($10.6m), SKIL ($0.29m). Of
those fourteen positions, **seven trade under $1m a day** and KEQU turns over $70,000 with 368 shares
changing hands the session before its print.

Hunting the full universe rather than the top eight by `hunt_priority` has, however, fixed the *selection*
half of this problem: the four most liquid names in the window (AVAV $179m, M $116m, COO $108m, AEO $86m)
are now in the table instead of shed, and three of them land mid-pack rather than at the extremes — which is
itself a mild point in favour of the ranking not simply tracking obscurity.

---

## Universe and confirmation

The sweep confirmed **22 of 22** companies from a company source — press release, IR page or 8-K exhibit —
with **zero phantom calendar rows** and zero unsettled sessions, the best confirmation rate this stage has
recorded. It is structural: this universe consists entirely of companies that pre-announce their reporting
date and hour by wire. No name carried a `suspect` `event_plausibility` verdict, so no baseline amendment
was needed.

Two consensus rows the sweep flagged as likely mis-keyed were both run down by their hunters:

- **CULP** at $0.44 against −$0.02 a year ago is **not** a mis-key — it reconciles to the company's own
  guide plus a $7.0m IEEPA refund over 12.66m shares.
- **LAKE** at −$0.02 against $0.36 **is** wrong: Q2 FY26 GAAP EPS was $0.08 on $52.5m of sales, so the
  "earnings collapse" framing built on that row is meaningless.

---

## One day is an anecdote

Twenty-two names on one day cannot produce a meaningful rank correlation, and this particular day carries a
known artefact in both its extremes and no factual check on fourteen of its names. Nothing here is a result.

Two standing cautions:

- The stage has **not been shown to beat `-run_up_20d_pct`**, a number that costs nothing and is available
  before any agent runs.
- The de-duplicated sample is 38 events over five independent days, and the raw impact sum's ranking
  p-value, corrected for the thirteen candidate statistics it was chosen from, is 0.056 — a lead to run
  forward, not a finding.

Resolve after the 2026-09-10 close for the `amc` names and the 2026-09-11 close for the `bmo` names:

```bash
python3 scripts/edge_resolve.py --run research/2026/09/2026-09-09/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'
```

2026-09-08's eight names are also still awaiting resolution, and five rows across 09-04 and 09-07 are known
duplicates that `--pool` double-counts.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market
positioning, guidance, macro conditions, and management commentary rather than reported results alone.*

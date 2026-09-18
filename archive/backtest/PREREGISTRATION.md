# Analysis plan — pilot-40, three arms

**This is exploratory.** Nothing here is powered to prove anything and it is not trying
to. The aim is a strong indication and a set of things worth arguing about: where the
arms agree, where they split, what each one saw that the others missed, and which events
were knowable at all. Numbers are read as direction-of-travel, not as verdicts.

Written 2026-08-29, after batch 06 (5 of 40 events) and before the remaining 35.

What the plan is still for: fixing *what gets looked at* before the numbers are visible,
so the interesting-looking cut is not chosen after the fact. Two comparators are kept for
the same reason, and neither is about significance --

- **`always_down`**, because the sample skews down and a bearish arm will look skilful
  in it whatever the sample size. That is a confounder, not a power problem.
- **`last_reaction` at 62%**, because it is free and reads nothing. An arm that cannot
  beat a one-line rule has told us something regardless of intervals.

## What is being tested

Three research strategies, each reading the same sealed point-in-time corpus, each
emitting the same schema:

- **A — naive.** Predict, no method supplied.
- **B — plan-first.** Derive a forecasting method before reading any narrative, then apply it.
- **C — skill.** The live pipeline's own nine-area method plus its calibration rules.

## The trading scheme

Buy at **20:00 CET (14:00 ET)** on the last market session before the print — the event
date itself for `amc`, the prior trading day for `bmo`. Exit at the **next open**
(primary) or the **next close** (secondary). Long on an Up call, short on a Down call,
no position on Neutral.

**Long and short. Equal weight. Frictionless headline, with the cost drag flagged.**

Prices are frozen in `runs/pilot-40/trade_prices.json` — the 15-minute bar window slides
daily, so the snapshot is taken once and not refreshed. 37 of 40 events priced from exact
14:00 ET bars; 3 fell back to hourly bars, which are stamped on the half hour, and are
marked as such.

## How much weight each answer can bear

Not gates -- just how hard to lean on each number.

**Magnitude carries the most weight.** It is the one place where n=40 would have had
power anyway (Spearman moves at |rho| > 0.31, a top-8 overlap of 4 would be p=0.037), so
a clear signal here is worth acting on rather than merely noting.

**Direction carries the least.** SE is 7.9pp, so 50% and 70% are the same number at this
sample size. A direction result is a lead to follow, never a finding. Worth more than the
rate itself: *which* events each arm got right, and whether the arms were wrong on the
same ones.

**Abstention sits in between**, and its interesting output is qualitative anyway -- does
Neutral track events that genuinely did not move.

## The comparator, and why it is not the coin

Under this scheme, being long every event **loses money**: −0.25% to the open, −0.61% to
the close. 18 of 40 moved up. So *always short* is profitable in this sample, and Arm B's
first batch was three Lean Downs, two Neutrals and no ups.

**Every direction result is scored against `always_down`, not against a coin.** An arm
that leans bearish will look skilful here for reasons that have nothing to do with skill.

Floors, all computed before the arms ran:

| baseline | direction rate |
| --- | --- |
| always_down | 55% |
| always_up | 45% |
| momentum_20d | 48% |
| **last_reaction** | **62%** |
| coin | 50%, 5–95 interval 38%–62% |

Magnitude floor: the median-of-last-eight proxy forecasts |move| with **2.93pp median
absolute error**.

## What gets measured

### (c) Magnitude — the strongest lead

1. **Spearman rho** between `expected_abs_move_pct` and realised |move|.
   Reference points: 0.31 is where it would have been significant, and the proxy is what
   it has to beat to have added anything.
2. **Top-8 capture.** Of the eight largest realised moves — AAP 24.6%, PWR 17.3%,
   ENTG 15.5%, RBRK 13.1%, AVNT 12.5%, KEEL 12.4%, DUOL 9.4%, TILE 9.1% — how many fall
   in the arm's own top eight predicted. Null expectation is 1.6, so 4 is a real
   indication and 6 would be a strong one.
3. **Median absolute error** against the proxy's 2.93pp.
4. **The big ones by name.** Which of the six events that moved >=10% did each arm size
   correctly, and what did it cite. The most useful output of the exercise, and it does
   not depend on n at all.

### (a) Direction — a lead, not a finding

Mean return per directional call, equal weight, long/short, with a bootstrap interval for
scale. Read against `always_down` on the same events, never against zero and never
against a coin. Hit rate beside it, always next to the 62% rule.

More interesting than either: **which events, and did the arms miss the same ones.** Three
arms agreeing and all wrong says something quite different from three arms splitting.

### (b) Abstention

- coverage: share of events traded
- return per trade on the traded subset
- total return across all 40, so abstention's opportunity cost is visible

**The real test:** do Neutral-called events actually move less than directional ones? If
mean |realised move| on Neutral is not below that on directional calls, Neutral is a
hedge rather than a signal — the same fault the ledger found when the panel went 7-for-7
Neutral and recorded no view at all.

Compared with return per trade if the arm were forced to trade all 40 with the same
signs. If abstaining does not improve per-trade return, Neutral is costing coverage and
buying nothing.

### Calibration — reported regardless of outcome

Does `certainty` separate? High vs Low hit rate and return per trade. The archive found
this field running backwards — Med conviction returned −2.2% and Low returned +9.1%,
because the field was scoring how *legible* a setup felt, and a legible setup is already
priced. If High does not beat Low here, the field is decorative and should be said to be.

Same treatment for `evidence_quality`.

## Reporting rules

- **Stratified by coverage, never pooled.** News coverage tracks market cap almost
  monotonically (small-cap median 1 document, 20% starved entirely) while filings are
  uniform at ~41 per event. A pooled number is a market-cap average wearing a method's
  name.
- Every rate carries its floor beside it. A rate reported alone is the mistake `LEDGER.md`
  already made.
- Both exits reported; the open is primary.
- The 3 hourly-fallback events are flagged in any table they appear in.

## The brainstorm outputs — the actual point

None of these need a sample size, and they are what the exercise is for.

- **Knowability, per event.** Reading only the pre-cutoff corpus and blind to the
  forecasts, label each event: was the driver of the move findable beforehand? Cross that
  with who got it right. The direct answer to what an AI can and cannot see.
- **Disagreement map.** Every event where the arms split, and who was right. Batch 06
  already produced a three-way split on BKNG -- A Lean Up on travel-peer read-across, B
  Lean Down because Estimize sat above the sell side, C Neutral because both cases were
  concrete. Three readings of the same documents.
- **What evidence appears in `key_drivers` of right vs wrong calls.** Filings,
  consensus-versus-guidance, peer read-through, retail chatter, positioning. A category
  that shows up disproportionately in correct calls is the finding worth carrying back
  into the live skill.
- **Failure taxonomy.** Every miss classified: missing anchor, misread bar, guidance
  surprise nobody could have known, macro shock, sentiment misread, or a correct read the
  market simply disagreed with. That last category is the interesting one.
- **Does method transfer?** Arm B writes its method down before reading. Compare the
  methods it derives across batches -- convergence on the same rules is a reusable
  artefact whether or not B scores well.

## Known limitations, recorded now rather than discovered later

- **n=40.** Confirmatory power for magnitude only. Everything else is a hypothesis
  generator.
- **Batched inference.** Each agent forecasts every event sharing one date, so it can in
  principle calibrate across same-day names. Batches are per-date specifically so a later
  event's market context cannot leak backward into an earlier forecast — an earlier
  interleaved design spanned 30 days and would have leaked badly.
- **Sample skews down**, so bearish arms are flattered. Hence the `always_down`
  comparator.
- **Implied move is unavailable** retrospectively; the proxy is the median of the last
  eight realised reactions. The live pipeline gets a real option-implied move, so it is
  better anchored than any arm here.
- **`reasoning` is dropped** when arm output is transcribed to disk; `key_drivers` and
  `what_would_change_my_mind` are kept. Full reasoning survives only in the session
  transcript.
- **Frictionless.** A 0.5% round trip removes about 10% of the median 5.12% move, and
  more on the starved small-caps.

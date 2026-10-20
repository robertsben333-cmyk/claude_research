# Stage E-P — 2026-10-20 amc + 2026-10-21 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel. Since 2026-10-19 this
stage trades the Alpaca paper account (step 3s sells, step 6b buys).** All four judges ran
on their pinned agents: Opus 5 `claude-opus-5`, Opus 5.5 `claude-opus-5-5`, Sonnet 5.5
`claude-sonnet-5-5` and Fable 5.1 `claude-fable-5-1`. Each covered 19 of 19 packs. None of
them reported a model id in its output, so the pin in each agent's frontmatter is the record.
One day is an anecdote; judge this stage only pooled.

**Selected (mean percentile ≥ 80, all four judges present): NP long (83) and WFRD long (81).**
Both are amc tonight. ALK short (75) is the nearest miss. Under the old 3-of-4 consensus rule,
NP and WFRD would also be selected (k = 3 each).

## The panel table

Percentiles are each judge's own: the share of that judge's live sizes from earlier runs
with a smaller |impact_sum| (n = 95 each). `*` marks a name in that judge's own top 20%.
`k` and `panel_score` are the legacy z-based consensus and score, still written.
E[return] is what names at that `panel_pct` have earned on the panel's side: gross, on the
scorebord window, one number per percentile, flat at about +0.3% below a percentile of 50.
It translates the percentile; it is not a separate forecast.

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NP | amc | **yes** | 83 | long | 12 | 62L | 94L* | 90L* | 87L* | 3 | +1.78 | +0.40 | +3.08% [+1.01, +5.06] | 0.63 | 1.00 | 0.90 |
| 2 | WFRD | amc | **yes** | 81 | long | 7 | 70L | 86L* | 84L* | 83L* | 3 | +1.38 | +0.20 | +2.73% [+0.72, +4.68] | 0.61 | 1.00 | 1.10 |
| 3 | ALK | amc |  | 75 | short | 11 | 75S | 68S | 93S* | 65S | 2 | -0.98 | -0.60 | +2.03% [+0.38, +3.86] | 0.57 | 0.00 | 0.00 |
| 4 | MCB | amc |  | 64 | long | 20 | 34L | 84L* | 79L | 58L | 2 | +0.96 | +0.20 | +1.09% [-0.00, +2.65] | 0.56 | 0.00 | 0.00 |
| 5 | LAD | bmo |  | 58 | long | 21 | 79L | 75L | 27L | 52L | 1 | +0.81 | +0.70 | +0.66% [-0.18, +2.14] | 0.56 | 0.00 | 0.00 |
| 6 | NFLX | amc |  | 57 | short | 13 | 47S | 70S | 40S | 70S | 0 | -0.74 | -0.50 | +0.55% [-0.22, +2.03] | 0.56 | 0.00 | 0.00 |
| 7 | DHR | bmo |  | 55 | short | 12 | 66S | 55S | 64S | 36S | 0 | -0.66 | -0.40 | +0.40% [-0.28, +1.89] | 0.56 | 0.00 | 0.00 |
| 8 | PM | bmo |  | 53 | short | 15 | 33S | 46S | 64S | 70S | 0 | -0.59 | -0.70 | +0.35% [-0.33, +1.74] | 0.56 | 0.00 | 0.00 |
| 9 | ABT | bmo |  | 53 | short | 22 | 57S | 70S | 15S | 68S | 0 | -0.83 | -0.30 | +0.34% [-0.35, +1.67] | 0.56 | 0.00 | 0.00 |
| 10 | MHO | bmo |  | 51 | short | 12 | 32S | 50S | 64S | 58S | 0 | -0.61 | -0.90 | +0.31% [-0.40, +1.52] | 0.56 | 0.00 | 0.00 |
| 11 | WAB | bmo |  | 45 | long | 10 | 30L | 42L | 56L | 52L | 0 | +0.49 | +0.30 | +0.29% [-0.49, +1.10] | 0.56 | 0.00 | 0.00 |
| 12 | CB | amc |  | 28 | short | 19 | 18S | 30S | 7S | 58S | 0 | -0.25 | -0.60 | +0.29% [-0.56, +0.85] | 0.56 | 0.00 | 0.00 |
| 13 | LRN | amc |  | 23 | long | 59 | 62S | 0- | 90L* | 65L | 1 | +0.41 | +1.50 | +0.29% [-0.58, +0.83] | 0.56 | 0.00 | 0.00 |
| 14 | COF | amc |  | 21 | long | 31 | 33S | 40L | 40L | 36L | 0 | +0.40 | +0.15 | +0.29% [-0.59, +0.82] | 0.56 | 0.00 | 0.00 |
| 15 | UAL | amc |  | 20 | short | 20 | 10L | 13S | 40S | 36S | 0 | -0.30 | -0.25 | +0.29% [-0.60, +0.82] | 0.56 | 0.00 | 0.00 |
| 16 | ELV | bmo |  | 16 | long | 40 | 33S | 17L | 77L | 2L | 1 | +0.13 | -0.60 | +0.29% [-0.64, +0.81] | 0.56 | 0.00 | 0.00 |
| 17 | OZK | amc |  | 10 | long | 44 | 66L | 56S | 27L | 2L | 0 | +0.22 | +0.80 | +0.29% [-0.69, +0.80] | 0.56 | 0.00 | 0.00 |
| 18 | WGO | bmo |  | 7 | short | 39 | 30L | 68S | 15S | 23L | 0 | +0.05 | +0.10 | +0.29% [-0.71, +0.79] | 0.56 | 0.00 | 0.00 |
| 19 | IART | bmo |  | 1 | long | 37 | 58S | 0- | 40L | 23L | 0 | +0.18 | +0.40 | +0.29% [-0.76, +0.78] | 0.56 | 0.00 | 0.00 |

**Not hunted:**
- The sweep could not confirm ISRG, PEGA, TDY, OFG, NPB and HCSG.
- Shed for budget at 19 hunted names, lowest `hunt_priority` first: QCRH, TMO, BWB, SF,
  ORRF, EWBC, HWC, BKU, AMX, ONB, NEE, NTRS, NLY, T, CME, FCCO, ELS, MCO, ADC, UNF.

All of these sit in `edge-scores.json` as `rankable: false`.

**Baseline amendment (a deviation).** The baselines for NP and IART had sealed
`event_plausibility: suspect`. `edge_baseline_amend.py` upgraded them after the hunts:
- NP moved to `fits_cadence`: a company release confirms the print and the classifier had
  missed the 2026-07-21 Q2 8-K.
- IART moved to `unknown`: the 10-02 pre-announcement made the gap look short.

The skill says to amend before the searchers launch, and that was missed. This is an
event-existence flag, not a priced-in estimate, and the amend script ran symmetrically.

## The selected names

**NP — Neptune Insurance, long, panel_pct 83.** Opus 5.5, Sonnet 5.5 and Fable 5.1 sit at
87–94 long; Opus 5 is at 62 long. Every judge's note names the same item. The 10-Q shows
premium in force +31.8% and policies +29% at 30 June, with a higher ceding commission all
quarter. Against that sit a $199M full-year guide that implies only about +19% in H2, and a
Q3 revenue consensus of about $55M. On a thin name that gapped up on its last beat-and-raise
(+6.7% on 2026-07-21), that reads as a likely beat and raise.

The searcher's own sum is only +0.40, and the case against is real:
- It found a record-quiet Q3 hurricane season and the two slowest home-sale months of 2026.
  Both bear directly on the storm- and purchase-driven new business that feeds premium in
  force.
- The stock is already 16% below its post-Q2 high.
- The option chain is unusable and the turnover is about $15m a day.

**WFRD — Weatherford, long, panel_pct 81.** Opus 5.5, Sonnet 5.5 and Fable 5.1 sit at 83–86
long; Opus 5 is at 70 long. The judges lean on Halliburton's Q3, released this morning:
- Middle East/Asia was +8% q/q, with Q4 guided up, and that region is about 40% of WFRD's
  revenue.
- Mexico activity rose.

All of that lands on the segments behind WFRD's Q2 miss. The stock is 20% below its 31 August
level after four target cuts in October. **The case against:** the FY26 EBITDA guide still
needs Q4 at about $293M, a ~17% q/q ramp that management had already said was shrinking, so
a guide cut is the obvious way this goes wrong. The EPS bar is also disputed across three
sources, and the Halliburton print is public and a few hours old.

## Where the panel and the searcher disagree most

- **LRN.** The searcher's top name at +1.50 has a panel_pct of only 23, with the judges split:
  Opus 5 at 62 short, Opus 5.5 at 0, Sonnet 5.5 at 90 long, Fable 5.1 at 65 long. They do not
  agree on whether the Lone Star enrollment loss outweighs a crowded short and the activist
  buyback.
- **ALK.** The searcher is mild at −0.60; the panel has it third at 75 short, with Sonnet 5.5
  at 93 short on the Q3 fuel overrun against the guide.
- **OZK.** The searcher is at +0.80; the panel has it at 10, with the judges on both sides of
  the binary IQHQ/RaDD loan grading.
- **MHO.** The searcher's most negative name (−0.90) reaches only 51 short on the panel.

## Stage E

Stage E's Routine is stopped, and `<RUN>/edge/` does not exist for this date. There is no
comparison line and no ρ between stage E's `impact_sum` and `panel_pct`.

## What the numbers are not

- **`expected_return_pct` and `expected_edge_pct` are not forecasts to size on.** They are
  what names at that percentile have earned. Out of sample the correlation with the realised
  return was +0.12 over 148 names.
- **`p_up` decides nothing.** It is recorded only; it did not predict on the development names.
- **The book sizes on its own rule, not on these weights.** The weights in the table are
  research. The book (`execution.panel`) weights each selected name at panel_pct − 60, capped
  at 50% of equity.
- **The searcher's key cleared nothing.** None of the 19 searcher `impact_sum` values reaches
  the 2.8 floor; the largest is LRN at +1.50. The searcher leaned 10 positive and 9 negative.
- **Nothing checked the findings for factual error.** No adversary pass and no second
  searcher ran. The key is not reproducible to better than its own size: double-hunted pairs
  once differed by a median 2.40 points, and 4 of 12 had opposite signs.
- **Three of the 19 baselines had no usable option chain** (16 option straddle, 3 historical
  median). The free control `-run_up_20d_pct` is in `edge-scores.json` beside every name.

## Context: retail, search and volatility (not used for selection)

`edge-context.json` holds retail tilt ≥ 50, search spike < 1.0x and 20-day volatility ≥ 58%
for every name. The Google search half ran out of its time budget for most names. These
labels are context only; nothing ranks, selects or trades on them.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.

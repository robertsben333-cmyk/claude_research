# Forecast accuracy ledger

Maintained by stage 4 (`earnings-calibration`), the morning after each run. Every call
is scored against the realised move, whether or not the result is flattering.

Measurement convention, applied identically every day: **close before the print → close
after the first full session following it.**

## Summary

One run scored so far (2026-08-19). **n=1 for panelled calls — none of the figures
below are statistically meaningful yet; they are recorded honestly as the first data
point, not as a verdict on the pipeline.**

| Metric | Panelled calls | Deep-dive preliminary reads |
| --- | --- | --- |
| Calls scored | 1 | 4 |
| Direction hit rate | 100% (1/1) | 75% (3/4) |
| Mean absolute magnitude error | n/a (no signed estimate on the 1 call) | n/a (no magnitude estimate) |
| Median absolute magnitude error | n/a | n/a |
| Band hit rate | 100% (1/1) | n/a |
| Implied move broken | 0% (0/1) | n/a |
| Red-team reversal fired | 0% (0/1) | n/a |

**Panel vs. single deep researcher, the one head-to-head data point so far:** on WOLF,
the only panelled name, the seven-persona panel called Neutral / No Edge while the
stage-2 preliminary score (−20) called the actual direction (−9.4%) correctly. The
panel's hedge was defensible on its own terms (the move landed inside its band, below
its expected magnitude, and its stated reasoning — a two-sided fight between weak
fundamentals and an extreme short base — was accurate), but it is not evidence the
expensive stage beat the cheap one. Needs several dozen more panelled names before
this comparison means anything either way; tracking it explicitly every run from here.

### Calibration by certainty tier

The question this table exists to answer: **do High-certainty calls actually hit more
often than Low-certainty ones?** If they do not, the tiering is decorative and
`scripts/synthesize.py` needs fixing.

| Certainty | Calls | Direction hit rate |
| --- | --- | --- |
| High | — | — |
| Med | — (0 directional Med calls; WOLF was Med certainty but a Neutral call — see below) |
| Low | — | — |
| Neutral / No Edge | 1 | 100% (1/1) |

A `Neutral / No Edge` call is scored as a hit when the realised absolute move came in
below the expected move, and a miss when the stock moved hard and the panel had no view.
No directional (Strong/Lean Up/Down) calls have been scored yet, so the certainty-tier
question this table exists to answer is not yet answerable — flagging rather than
implying a verdict from an empty table.

## Runs

| Date | Names | Panelled | Direction hits | Mean abs error | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-08-19 | 4 (WOLF, BILL, BABA, HOV) | 1 (WOLF) | Panelled 1/1 (100%, Neutral-hit convention); Prelim 3/4 (75%) | n/a — panelled call had no signed estimate | WOLF: Neutral hit (band + below-expected-move), but the specific red-team squeeze case did not fire — a genuinely weak print/guide broke it this time instead of repeating May's squeeze. BILL: clean EPS+revenue beat, stock ~flat, prelim (+10) called the wrong sign on a near-noise move. BABA: profit −75% y/y but revenue/cloud growth strong; gapped down 4-5% intraday then reversed to close +1.26% — prelim (+10) right on the close. HOV: guided-breakeven miss, thin-evidence dossier, opened −6%, hit −15.2% intraday, closed −7.47% — prelim (−15) right despite thin evidence. |

# Forecast accuracy ledger

Maintained by stage 4 (`earnings-calibration`), the morning after each run. Every call
is scored against the realised move, whether or not the result is flattering.

Measurement convention, applied identically every day: **close before the print → close
after the first full session following it.**

## Summary

Two runs scored so far (2026-08-19, 2026-08-26). **n=3 for panelled calls — still far
too small to be statistically meaningful; recorded honestly as accumulating data
points, not as a verdict on the pipeline.**

| Metric | Panelled calls | Deep-dive preliminary reads |
| --- | --- | --- |
| Calls scored | 3 | 8 |
| Direction hit rate | 67% (2/3, Neutral-hit convention) | 63% (5/8) |
| Mean absolute magnitude error | n/a (no signed estimate on any of the 3 calls — all Neutral) | n/a (no magnitude estimate) |
| Median absolute magnitude error | n/a | n/a |
| Band hit rate | 67% (2/3) | n/a |
| Implied move broken | 33% (1/3) | n/a |
| Red-team reversal fired | 33% (1/3) | n/a |

**Panel vs. single deep researcher, three panelled names in:** every panelled call so
far — WOLF (08-19), OKTA and DLTR (08-26) — has been **Neutral / No Edge**. The panel
has not yet made a single directional call. Over the same three names, the cheap
stage-2 preliminary read called the actual direction correctly **3 for 3** (WOLF −20 →
−9.4%, OKTA +10 → +28.6%, DLTR −10 → −3.9%). This is not proof the panel adds nothing —
Neutral is a legitimate call when the panel genuinely splits, and it scored a hit on 2
of the 3 (WOLF, DLTR) under the below-expected-move convention — but the pattern is now
three-for-three on "panel hedges, cheap read calls it right," including one case (OKTA)
where the panel's hedge cost real information: three of its own seven personas leaned
bullish for reasons (de-risked positioning, a history of beating conservative guides)
that turned out to be exactly right, and the stock then broke its own implied move by
more than 2x while the panel had recorded no view at all. Worth watching closely over
the next several panelled names — if the panel keeps converging to Neutral while the
preliminary read keeps calling direction, that is evidence the synthesis step is
absorbing real, sourced disagreement into a null result too eagerly, not evidence that
Neutral is simply the right call every time.

### Calibration by certainty tier

The question this table exists to answer: **do High-certainty calls actually hit more
often than Low-certainty ones?** If they do not, the tiering is decorative and
`scripts/synthesize.py` needs fixing.

| Certainty | Calls | Direction/Neutral hit rate |
| --- | --- | --- |
| High | 2 (OKTA miss, DLTR hit) | 50% (1/2) |
| Med | 1 (WOLF hit) | 100% (1/1) |
| Low | 0 | — |

No directional (Strong/Lean Up/Down) calls have been scored yet — every panelled call
to date has been Neutral / No Edge (3/3), so the certainty-tier question this table
exists to answer is not yet answerable in its intended form. The only signal available
so far runs backwards from what the tiering should predict — High-certainty (2 calls)
has a *lower* hit rate than Med-certainty (1 call) — but n is far too small (2 vs 1) to
mean anything yet. Flagging rather than concluding; revisit once directional calls and
a larger sample exist.

A `Neutral / No Edge` call is scored as a hit when the realised absolute move came in
below the expected move, and a miss when the stock moved hard and the panel had no view.

## Runs

| Date | Names | Panelled | Direction hits | Mean abs error | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-08-19 | 4 (WOLF, BILL, BABA, HOV) | 1 (WOLF) | Panelled 1/1 (100%, Neutral-hit convention); Prelim 3/4 (75%) | n/a — panelled call had no signed estimate | WOLF: Neutral hit (band + below-expected-move), but the specific red-team squeeze case did not fire — a genuinely weak print/guide broke it this time instead of repeating May's squeeze. BILL: clean EPS+revenue beat, stock ~flat, prelim (+10) called the wrong sign on a near-noise move. BABA: profit −75% y/y but revenue/cloud growth strong; gapped down 4-5% intraday then reversed to close +1.26% — prelim (+10) right on the close. HOV: guided-breakeven miss, thin-evidence dossier, opened −6%, hit −15.2% intraday, closed −7.47% — prelim (−15) right despite thin evidence. |
| 2026-08-26 | 4 (OKTA, DLTR, NTNX, STDN) | 2 (OKTA, DLTR) | Panelled 1/2 (50%, Neutral-hit convention); Prelim 2/4 (50%) | n/a — both panelled calls Neutral, no signed estimate | OKTA: beat-and-raise, cRPO accelerated to +14% past the ~11% guide the two most bearish personas (−18 each) were leaning on; closed +28.63%, more than 2x the 13.0% implied move — Neutral call missed (band_hit true, but moved far harder than expected), red-team's in-line-guide reversal case did not fire, prelim (+10) right. DLTR: clean beat, weak Q3 EPS guide ($0.80-0.95 vs ~$1.39 consensus); gapped ~−9% at the open, recovered to close −3.92% — Neutral call hit but undershot even the low end of its own band; the red-team's specific mechanism (beat overshadowed by cautious guide) fired, just not to its stated −10% magnitude; prelim (−10) right. NTNX: beat-and-raise, +6.81% (within its 14.49% implied move), prelim (−10) wrong. STDN: continuation of its pre-print run into a modest reaction (+4.45%), panel-ineligible (no implied move, thin post-IPO trading history), prelim (−15) wrong. Deferred once already (logged 2026-08-27) because both OKTA's and DLTR's outcome windows resolve on the *current* day's close — same schedule-lag pattern flagged on 2026-08-20; now a third occurrence. |

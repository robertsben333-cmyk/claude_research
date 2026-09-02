# Forecast accuracy ledger

Maintained by stage 4 (`earnings-calibration`), the morning after each run. Every call
is scored against the realised move, whether or not the result is flattering.

Measurement convention, applied identically every day: **close before the print → close
after the first full session following it.**

## Summary

Three runs scored so far (2026-08-19, 2026-08-26, 2026-08-27). **n=5 for panelled
calls — still far too small to be statistically meaningful; recorded honestly as
accumulating data points, not as a verdict on the pipeline.** (2026-08-31 produced no
panelled or preliminary calls at all — stages 0-2 never ran that day — and is excluded
throughout; 2026-09-01 is scored, not this one — its outcome window does not close
until the 2026-09-02 US close, which has not happened yet as of this update.)

| Metric | Panelled calls | Deep-dive preliminary reads |
| --- | --- | --- |
| Calls scored | 5 | 13 |
| Direction hit rate | 60% (3/5, Neutral-hit convention) | 62% (8/13) |
| Mean absolute magnitude error | n/a (no signed estimate on any of the 5 calls — all Neutral) | n/a (no magnitude estimate) |
| Median absolute magnitude error | n/a | n/a |
| Band hit rate | 80% (4/5) | n/a |
| Implied move broken | 40% (2/5) | n/a |
| Red-team reversal fired | 20% (1/5) | n/a |

**Panel vs. single deep researcher, five panelled names in:** every panelled call so
far — WOLF (08-19), OKTA and DLTR (08-26), ESTC and AFRM (08-27) — has been
**Neutral / No Edge**. The panel has not yet made a single directional call. Through
the first three names the cheap stage-2 preliminary read had called direction correctly
3-for-3 while the panel hedged every time; that streak **broke on 2026-08-27**. ESTC's
preliminary read (−20, bearish) missed the largest single move recorded in this ledger
(+19.31%, a genuine beat-and-raise re-rating), and AFRM's preliminary read (−18) called
the wrong sign on a near-zero (+0.35%) move. Over all five panelled names the
preliminary read is now 3/5 (60%) and the panel (Neutral-hit convention) is also 3/5
(60%) — the two are running even, not one dominating the other. The "cheap read beats
the expensive panel" narrative from the first two runs does not hold up with two more
data points; it needs revising, not confirming, and it will take several more panelled
names before either signal is trustworthy. Separately, this is also the first
occurrence where a Neutral consensus (ESTC, −20.7) was close to crossing the −25
Lean Down threshold and still ended up on the wrong side of the actual move entirely —
the panel's own directional lean, had it been allowed to become a call, would have
been wrong too, so this is not simply "the synthesis step over-hedges a call that
would have been right."

### Calibration by certainty tier

The question this table exists to answer: **do High-certainty calls actually hit more
often than Low-certainty ones?** If they do not, the tiering is decorative and
`scripts/synthesize.py` needs fixing.

| Certainty | Calls | Direction/Neutral hit rate |
| --- | --- | --- |
| High | 3 (OKTA miss, DLTR hit, ESTC miss) | 33% (1/3) |
| Med | 2 (WOLF hit, AFRM hit) | 100% (2/2) |
| Low | 0 | — |

No directional (Strong/Lean Up/Down) calls have been scored yet — every panelled call
to date has been Neutral / No Edge (5/5), so the certainty-tier question this table
exists to answer is not yet answerable in its intended form. The signal available so
far continues to run **backwards** from what the tiering should predict — High
certainty (3 calls) has a *lower* hit rate than Med certainty (2 calls) — and the gap
has widened, not narrowed, as more calls accumulated (was 50% vs 100% on n=2 vs n=1;
now 33% vs 100% on n=3 vs n=2). In both new misses (OKTA, ESTC) and the earlier miss,
`certainty_score`'s stated driver was elevated red-team reversal risk (OKTA and ESTC
both cite it explicitly), and in neither case did the named reversal mechanism actually
fire. That raises a specific, checkable hypothesis: if `certainty_score` in
`scripts/synthesize.py` is weighting reversal-risk magnitude rather than panel
agreement, high reversal-risk names would systematically get tagged High certainty
right before an unhedged, uncalled move breaks them — the opposite of what "High
certainty" should mean. Worth inspecting the certainty-score formula directly rather
than waiting for more calls to accumulate the same pattern.

A `Neutral / No Edge` call is scored as a hit when the realised absolute move came in
below the expected move, and a miss when the stock moved hard and the panel had no view.

## Runs

| Date | Names | Panelled | Direction hits | Mean abs error | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-08-19 | 4 (WOLF, BILL, BABA, HOV) | 1 (WOLF) | Panelled 1/1 (100%, Neutral-hit convention); Prelim 3/4 (75%) | n/a — panelled call had no signed estimate | WOLF: Neutral hit (band + below-expected-move), but the specific red-team squeeze case did not fire — a genuinely weak print/guide broke it this time instead of repeating May's squeeze. BILL: clean EPS+revenue beat, stock ~flat, prelim (+10) called the wrong sign on a near-noise move. BABA: profit −75% y/y but revenue/cloud growth strong; gapped down 4-5% intraday then reversed to close +1.26% — prelim (+10) right on the close. HOV: guided-breakeven miss, thin-evidence dossier, opened −6%, hit −15.2% intraday, closed −7.47% — prelim (−15) right despite thin evidence. |
| 2026-08-26 | 4 (OKTA, DLTR, NTNX, STDN) | 2 (OKTA, DLTR) | Panelled 1/2 (50%, Neutral-hit convention); Prelim 2/4 (50%) | n/a — both panelled calls Neutral, no signed estimate | OKTA: beat-and-raise, cRPO accelerated to +14% past the ~11% guide the two most bearish personas (−18 each) were leaning on; closed +28.63%, more than 2x the 13.0% implied move — Neutral call missed (band_hit true, but moved far harder than expected), red-team's in-line-guide reversal case did not fire, prelim (+10) right. DLTR: clean beat, weak Q3 EPS guide ($0.80-0.95 vs ~$1.39 consensus); gapped ~−9% at the open, recovered to close −3.92% — Neutral call hit but undershot even the low end of its own band; the red-team's specific mechanism (beat overshadowed by cautious guide) fired, just not to its stated −10% magnitude; prelim (−10) right. NTNX: beat-and-raise, +6.81% (within its 14.49% implied move), prelim (−10) wrong. STDN: continuation of its pre-print run into a modest reaction (+4.45%), panel-ineligible (no implied move, thin post-IPO trading history), prelim (−15) wrong. Deferred once already (logged 2026-08-27) because both OKTA's and DLTR's outcome windows resolve on the *current* day's close — same schedule-lag pattern flagged on 2026-08-20; now a third occurrence. |
| 2026-08-27 | 5 (ESTC, AFRM, S, MRVL, RBRK) | 2 (ESTC, AFRM) | Panelled 1/2 (50%, Neutral-hit convention); Prelim 3/5 (60%) | n/a — both panelled calls Neutral, no signed estimate | ESTC: beat-and-raise (EPS $0.70 vs ~$0.58, cloud growth accelerated to 20% c/c), closed +19.31%, breaking the 12.9% implied move by ~1.5x — Neutral call missed (band_hit true only because the band spans 6.7-27.8 points), consensus score −20.7 leaned bearish (missed Lean Down by 4.3 points) and the actual move went the other way entirely; red-team's repeat-of-May reversal case did not fire; prelim (−20) wrong — the largest move scored to date and a miss. AFRM: revenue beat ~3.3%, large EPS beat looks non-operating; closed +0.35%, essentially flat — Neutral call hit (well below the 10.8% expected move) but undershot even the low end of its 5.4-22.9% band; red-team's Feb-2026-repeat credit-provision reversal case did not fire; prelim (−18) wrong on a near-noise move (same failure mode as BILL, 08-19). S: revenue beat but trimmed profit forecast, closed −5.15%, prelim (−15) right. MRVL: beat-and-raise but stock priced for perfection (P/E ~83), closed −10.28% on softer forward framing, prelim (−15) right. RBRK: clean beat (EPS $0.20 vs $0.04) but sell-the-news, closed −13.05%, prelim (−10) right on direction, understated magnitude ~3x. First run where the panel's prior "cheap read beats the panel" streak broke — preliminary read is now 3/5 (60%) across all panelled names to date, level with the panel's own 3/5 (60%). 2026-08-31 produced no panelled or preliminary calls (stages 0-2 never ran) and is excluded; a minimal `05-outcome.md` was written so the day stops showing as unscored. 2026-09-01 (DELL, CXM panelled; GIII, GTLB, MDB, CRDO prelim) checked but deferred — its outcome window needs the 2026-09-02 US close, which had not happened yet at scoring time; logged in that day's `_run-log.md` for the next stage-4 pass. |

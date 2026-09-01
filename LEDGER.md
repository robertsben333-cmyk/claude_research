# Forecast accuracy ledger

Maintained by stage 4 (`earnings-calibration`), the morning after each run. Every call
is scored against the realised move, whether or not the result is flattering.

Measurement convention, applied identically every day: **close before the print → close
after the first full session following it.**

## Summary

Three runs scored so far (2026-08-19, 2026-08-26, 2026-08-27). One further run
(2026-08-31) is recorded as blocked — a pipeline outage with zero calls made, not
scored either way. **n=5 for panelled calls — still small, but the certainty-tier
signal below has now shown the same direction twice in a row.**

| Metric | Panelled calls | Deep-dive preliminary reads |
| --- | --- | --- |
| Calls scored | 5 | 13 |
| Direction hit rate | 60% (3/5, Neutral-hit convention) | 62% (8/13) |
| Mean absolute magnitude error | n/a (no signed estimate on any of the 5 calls — all Neutral) | n/a (no magnitude estimate) |
| Median absolute magnitude error | n/a | n/a |
| Band hit rate | 60% (3/5) | n/a |
| Implied move broken | 40% (2/5) | n/a |
| Red-team reversal fired | 20% (1/5) | n/a |

**Panel vs. single deep researcher, five panelled names in:** every panelled call to
date — WOLF (08-19), OKTA and DLTR (08-26), ESTC and AFRM (08-27) — has been
**Neutral / No Edge**. The panel has still not made a single directional call across
five names. The cheap stage-2 preliminary read is at 8/13 (62%) across every
researched name including panelled ones, essentially indistinguishable from the
panel's 3/5 (60%) once both are measured the same way. That parity is new information:
through 08-26 the preliminary read was running a clean 3-for-3 ahead of the panel; the
08-27 run broke that streak in both directions at once — AFRM is the panel's
best-calibrated call yet (a genuinely split panel correctly flagged that direction hung
on the credit/margin guide, and the stock faded from its post-beat pop to close
essentially flat), while ESTC is a case where **both** methods missed together (panel
consensus −20.7, prelim −20, actual +19.31% on a guidance raise neither saw coming).
The pattern worth tracking now is not "panel hedges, prelim wins" so much as "both
methods lean on the same historical repeat-pattern story and both get burned when the
company breaks it" — see the certainty-tier note below, which points at the same root
cause.

### Calibration by certainty tier

The question this table exists to answer: **do High-certainty calls actually hit more
often than Low-certainty ones?** If they do not, the tiering is decorative and
`scripts/synthesize.py` needs fixing.

| Certainty | Calls | Direction/Neutral hit rate |
| --- | --- | --- |
| High | 3 (OKTA miss, DLTR hit, ESTC miss) | 33% (1/3) |
| Med | 2 (WOLF hit, AFRM hit) | 100% (2/2) |
| Low | 0 | — |

Still no directional (Strong/Lean Up/Down) calls scored — every panelled call to date
has been Neutral / No Edge (5/5) — so this table is still reading Neutral-hit rate, not
true directional calibration. But the signal is no longer a single data point running
backwards: **High-certainty calls have now missed twice out of three (OKTA, ESTC),
against Med-certainty going 2-for-2 (WOLF, AFRM).** Both High-certainty misses share a
mechanism worth naming directly: in each case the panel's certainty was driven by
*alignment* — a tight spread across personas (ESTC disparity 8.7) or a single strong
red-team reversal-risk score — around a specific "this company has a repeatable
beat-then-X pattern" thesis, and in both cases the company broke its own pattern this
quarter (OKTA accelerated instead of guiding conservatively; ESTC raised guidance
instead of hedging it). Certainty here is measuring *agreement on a historical
narrative*, not *validated forward-looking accuracy* — those are different things, and
conflating them is exactly how a tiering ends up decorative. n=3 vs n=2 is still too
small to force a fix, but this is now two independent High-certainty misses on the
same failure mode, not one. Worth a standing flag on `scripts/synthesize.py`'s
certainty scoring rather than a shrug at the sample size.

A `Neutral / No Edge` call is scored as a hit when the realised absolute move came in
below the expected move, and a miss when the stock moved hard and the panel had no view.

## Runs

| Date | Names | Panelled | Direction hits | Mean abs error | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-08-19 | 4 (WOLF, BILL, BABA, HOV) | 1 (WOLF) | Panelled 1/1 (100%, Neutral-hit convention); Prelim 3/4 (75%) | n/a — panelled call had no signed estimate | WOLF: Neutral hit (band + below-expected-move), but the specific red-team squeeze case did not fire — a genuinely weak print/guide broke it this time instead of repeating May's squeeze. BILL: clean EPS+revenue beat, stock ~flat, prelim (+10) called the wrong sign on a near-noise move. BABA: profit −75% y/y but revenue/cloud growth strong; gapped down 4-5% intraday then reversed to close +1.26% — prelim (+10) right on the close. HOV: guided-breakeven miss, thin-evidence dossier, opened −6%, hit −15.2% intraday, closed −7.47% — prelim (−15) right despite thin evidence. |
| 2026-08-26 | 4 (OKTA, DLTR, NTNX, STDN) | 2 (OKTA, DLTR) | Panelled 1/2 (50%, Neutral-hit convention); Prelim 2/4 (50%) | n/a — both panelled calls Neutral, no signed estimate | OKTA: beat-and-raise, cRPO accelerated to +14% past the ~11% guide the two most bearish personas (−18 each) were leaning on; closed +28.63%, more than 2x the 13.0% implied move — Neutral call missed (band_hit true, but moved far harder than expected), red-team's in-line-guide reversal case did not fire, prelim (+10) right. DLTR: clean beat, weak Q3 EPS guide ($0.80-0.95 vs ~$1.39 consensus); gapped ~−9% at the open, recovered to close −3.92% — Neutral call hit but undershot even the low end of its own band; the red-team's specific mechanism (beat overshadowed by cautious guide) fired, just not to its stated −10% magnitude; prelim (−10) right. NTNX: beat-and-raise, +6.81% (within its 14.49% implied move), prelim (−10) wrong. STDN: continuation of its pre-print run into a modest reaction (+4.45%), panel-ineligible (no implied move, thin post-IPO trading history), prelim (−15) wrong. Deferred once already (logged 2026-08-27) because both OKTA's and DLTR's outcome windows resolve on the *current* day's close — same schedule-lag pattern flagged on 2026-08-20; now a third occurrence. |
| 2026-08-27 | 5 (ESTC, AFRM, S, MRVL, RBRK) | 2 (ESTC, AFRM) | Panelled 1/2 (50%, Neutral-hit convention); Prelim 3/5 (60%) | n/a — both panelled calls Neutral, no signed estimate | ESTC: beat-and-*raise* (the opposite of its own three-print beat-then-fall history the panel's red-team case leaned on), closed +19.31%, 1.5x the 12.9% implied move — Neutral call missed (band_hit true, moved far harder than expected), reversal case did not fire, prelim (−20) also wrong — a rare case where both methods missed together. AFRM: FQ4 beat, popped +8.34% after hours then faded to close +0.35% — Neutral call hit cleanly (0.35% vs 10.8% expected), and the panel's own stated logic (direction hinges on the credit/margin guide, not the near-certain beat) is exactly what played out; prelim (−18) is a technical miss on a fractionally-positive, functionally-flat print. S: revenue/ARR beat, EPS doubled, but FY EPS guide cut ~11%; closed −5.15%, prelim (−15) right. MRVL: record beat plus an Alphabet warrant deal, popped then reversed on a "priced for perfection" read after a ~187% YTD run to close −10.28%, prelim (−15, explicit Lean Down) right. RBRK: large EPS/revenue beats, ran up +11.44% into the print then sold the news down to −13.05% close, prelim (−10) right. Not researched: IREN (stage 2 batch 2 stalled after wave 1, no closing run-log entry) — excluded, not scored as a miss. |
| 2026-08-31 | 0 — pipeline blocked | 0 | n/a — no calls made | n/a | Stages 0/1/2 produced no output at all (no universe, shortlist, dossiers, or ranking); stage 3 correctly refused to invent a ranking and published a pipeline-outage report instead of an advice note. Recorded here so the gap is visible in the archive, not folded into the hit-rate figures above — zero calls is neither a hit nor a miss. Matches the standing account issue already documented in `CLAUDE.md`/`docs/ROUTINES.md` (stages 0-4 not registered as Routines as of 2026-08-29). |

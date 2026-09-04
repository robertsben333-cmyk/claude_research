# Forecast accuracy ledger

Maintained by stage 4 (`earnings-calibration`), the morning after each run. Every call
is scored against the realised move, whether or not the result is flattering.

Measurement convention, applied identically every day: **close before the print → close
after the first full session following it.**

## Summary

Five runs scored so far (2026-08-19, 2026-08-26, 2026-08-27, 2026-09-01, 2026-09-02).
2026-08-31 was checked and found to have nothing to score (stages 0-2 never ran that
day — see its own `05-outcome.md`). **n=9 for panelled calls — bigger than it was, but
still small; the picture has shifted meaningfully since the last update and should keep
moving.**

| Metric | Panelled calls | Deep-dive preliminary reads |
| --- | --- | --- |
| Calls scored | 9 | 25 |
| Direction hit rate | 44% (4/9, Neutral-hit convention) | 44% (11/25) |
| Mean absolute magnitude error | n/a (no signed estimate on any panelled call — every one has been Neutral) | n/a (no magnitude estimate) |
| Median absolute magnitude error | n/a | n/a |
| Band hit rate | 67% (6/9) | n/a |
| Implied move broken | 56% (5/9) | n/a |
| Red-team reversal fired | 33% (3/9) | n/a |

**Panel vs. single deep researcher, nine panelled names in:** every panelled call to
date — WOLF, OKTA, DLTR, AFRM, ESTC, DELL, CXM, AI, SNOW — has still been **Neutral /
No Edge**. The panel has made zero directional calls across nine tries. The early
"cheap read beats the panel" story (WOLF/OKTA/DLTR all 3/3 as of 08-26, 75% overall
through that point) did **not** survive a larger sample: the preliminary read went 3/5
on 08-27, 3/6 on 09-01, and 0/6 on 09-02 — its worst day yet, missing every single name
including the two it shared with the panel (AI, SNOW) — pulling its running hit rate
down from 63% (5/8) to 44% (11/25). The panel's own hit rate over the same growth,
44% (4/9), has landed at **exactly the same number**. The honest read at n=25 total
scored calls is that **neither the panel nor the cheap preliminary read is beating a
coin flip on direction**, and the earlier apparent edge for the preliminary read was
small-sample noise, not a structural advantage. This matters directly for whether the
expensive stage-3 panel is worth its cost: so far, across every name it has looked at,
it has never once had a directional view to be right or wrong with, and when it hedges
to Neutral it is now getting the below-expected-move call wrong more often than right
(5 misses out of 9).

One qualitative bright spot: CXM (09-01) and AI (09-02) are the first two cases where a
persona's *specific stated mechanism* — not just the direction — played out exactly as
described (CXM: a soft guide undercutting a technical beat, from the red-team; AI: a
short-covering bid absorbing a weak guide, also from the red-team). Both still landed on
different sides of the Neutral hit/miss line (CXM missed on magnitude, AI hit), which is
itself informative: getting the mechanism right is not the same as getting the
below-expected-move sizing right.

### Calibration by certainty tier

The question this table exists to answer: **do High-certainty calls actually hit more
often than Low-certainty ones?** If they do not, the tiering is decorative and
`scripts/synthesize.py` needs fixing.

| Certainty | Calls | Direction/Neutral hit rate |
| --- | --- | --- |
| High | 5 (OKTA miss, DLTR hit, ESTC miss, AI hit, SNOW miss) | 40% (2/5) |
| Med | 4 (WOLF hit, AFRM hit, DELL miss, CXM miss) | 50% (2/4) |
| Low | 0 | — |

Still no directional (Strong/Lean Up/Down) calls have been scored — every panelled call
to date has been Neutral / No Edge (9/9) — so this table is still scoring the
below-expected-move convention rather than the tiering's intended target. But the
signal it does carry has now held in the same direction across three consecutive
ledger updates: High-certainty calls are hitting *less* often (40%) than Med-certainty
calls (50%). At n=5 vs n=4 this is still not statistically decisive, but "runs backwards
every time it's checked" is a different, more concerning pattern than "too small to
tell." The certainty tier is not yet earning its keep, and `scripts/synthesize.py`'s
certainty logic is due a direct look rather than more waiting for a bigger sample to
resolve it on its own.

A `Neutral / No Edge` call is scored as a hit when the realised absolute move came in
below the expected move, and a miss when the stock moved hard and the panel had no view.

## Runs

| Date | Names | Panelled | Direction hits | Mean abs error | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-08-19 | 4 (WOLF, BILL, BABA, HOV) | 1 (WOLF) | Panelled 1/1 (100%, Neutral-hit convention); Prelim 3/4 (75%) | n/a — panelled call had no signed estimate | WOLF: Neutral hit (band + below-expected-move), but the specific red-team squeeze case did not fire — a genuinely weak print/guide broke it this time instead of repeating May's squeeze. BILL: clean EPS+revenue beat, stock ~flat, prelim (+10) called the wrong sign on a near-noise move. BABA: profit −75% y/y but revenue/cloud growth strong; gapped down 4-5% intraday then reversed to close +1.26% — prelim (+10) right on the close. HOV: guided-breakeven miss, thin-evidence dossier, opened −6%, hit −15.2% intraday, closed −7.47% — prelim (−15) right despite thin evidence. |
| 2026-08-26 | 4 (OKTA, DLTR, NTNX, STDN) | 2 (OKTA, DLTR) | Panelled 1/2 (50%, Neutral-hit convention); Prelim 2/4 (50%) | n/a — both panelled calls Neutral, no signed estimate | OKTA: beat-and-raise, cRPO accelerated to +14% past the ~11% guide the two most bearish personas (−18 each) were leaning on; closed +28.63%, more than 2x the 13.0% implied move — Neutral call missed (band_hit true, but moved far harder than expected), red-team's in-line-guide reversal case did not fire, prelim (+10) right. DLTR: clean beat, weak Q3 EPS guide ($0.80-0.95 vs ~$1.39 consensus); gapped ~−9% at the open, recovered to close −3.92% — Neutral call hit but undershot even the low end of its own band; the red-team's specific mechanism (beat overshadowed by cautious guide) fired, just not to its stated −10% magnitude; prelim (−10) right. NTNX: beat-and-raise, +6.81% (within its 14.49% implied move), prelim (−10) wrong. STDN: continuation of its pre-print run into a modest reaction (+4.45%), panel-ineligible (no implied move, thin post-IPO trading history), prelim (−15) wrong. Deferred once already (logged 2026-08-27) because both OKTA's and DLTR's outcome windows resolve on the *current* day's close — same schedule-lag pattern flagged on 2026-08-20; now a third occurrence. |
| 2026-08-27 | 5 (AFRM, ESTC, S, MRVL, RBRK) — IREN never researched, excluded | 2 (AFRM, ESTC) | Panelled 1/2 (50%, Neutral-hit convention); Prelim 3/5 (60%, all researched names) | n/a — both panelled calls Neutral, no signed estimate | AFRM: EPS beat inflated by a one-time $1.45B tax benefit; gapped up 11%, ran to +16.7% intraday, gave it all back to close +0.35% — Neutral hit but undershot even the low end of its band; red-team's credit-provision reversal case did not fire; prelim (−18) wrong on a near-zero move. ESTC: clean beat-and-raise (guidance raised, not cautious) — the opposite of the red-team's repeat-of-May thesis, which did not fire; closed +19.31%, breaking the 13.4% expected move — Neutral call missed, High-certainty tier's second miss in three; prelim (−20) also wrong, breaking the earlier 3-for-3 prelim streak. S: beat on EPS/revenue but FY EPS guide fell short; closed −5.15%, prelim (−15) right. MRVL: record revenue, beat-and-raise on all guides, still closed −10.28% on stretched valuation; prelim (−15) right despite the strong print. RBRK: large beat, ARR +33%, guidance raised, still closed −13.06% with the sharpest intraday reversal of the run; prelim (−10) right. |
| 2026-08-31 | 0 — stages 0/1/2 never ran (no registered pipeline Routine that day) | 0 | Not scored — nothing to score | n/a | `04-advice.json` carries `status: blocked`, empty `ranked_names`. Only stage E and stage C ran; neither feeds stage 3. See its own `05-outcome.md`. |
| 2026-09-01 | 6 (DELL, MDB, GTLB, CRDO, CXM, GIII) | 2 (DELL, CXM) | Panelled 0/2 (0%, Neutral-hit convention); Prelim 3/6 (50%, all researched names) | n/a — both panelled calls Neutral, no signed estimate | DELL: EPS beat ~44%, revenue beat ~58% y/y, FY27 guidance raised $25B; closed +15.81%, breaking the 11.5% expected move — Neutral call missed (moved hard, no view); red-team's HP-style margin-squeeze reversal did not fire; prelim (+20) right. CXM: EPS beat but revenue missed and Q3 guidance came in below consensus; opened flat, rallied intraday, then reversed to close −8.55% at the day's low, breaking the 6.8% expected move — Neutral call missed, but the red-team's specific mechanism ("a beat isn't enough a third year running because guide stays soft") fired exactly as described; prelim (−25) right and was the only source, panel included, to flag the guide as the risk. GIII: revenue missed on planned license exits, EPS beat an uncertain-basis estimate, guidance raised anyway; closed −11.50%, prelim (−20) right. GTLB: clean beat-and-raise, gapped up 22% then faded to close +9.98%; prelim (−20) wrong on a genuinely strong print. MDB: beat every line and raised guidance, still closed −13.54% on a soft Q3/Atlas growth read; prelim (+10) wrong — the sharpest "beat everything, still fall" case scored to date. CRDO: beat on EPS/revenue, 7th straight triple-digit growth quarter, outlook reaffirmed, still closed −20.04% on gross-margin compression the headline didn't show; prelim (+10) wrong — the largest single-name magnitude miss scored to date. |
| 2026-09-02 | 6 (AI, SNOW, AVGO, PVH, NTAP, VSXY) | 2 (AI, SNOW) | Panelled 1/2 (50%, Neutral-hit convention); Prelim 0/6 (0%, all researched names) | n/a — both panelled calls Neutral, no signed estimate | AI: narrow EPS/revenue beat but Q2 guide below consensus; closed +3.61%, below the 11.3% expected move — Neutral call hit; red-team's short-covering/seller-exhaustion reversal case fired (weak guide didn't sink the stock); prelim (−22) wrong on a small move. SNOW: EPS/revenue beat, full-year guide raised to imply acceleration (36% vs. 34% prior); closed +16.56%, breaking the 14.0% expected move — Neutral call missed, the day's largest panelled magnitude break; red-team's "beat sells off anyway" thesis did not fire; prelim (−10) wrong. AVGO: EPS beat ~35.5%, revenue beat ~86% y/y, but Q4 guide landed just below consensus; closed −2.74%; prelim (+6) wrong. PVH: EPS beat leaned on a one-time tariff-refund benefit, revenue roughly flat, outlook reaffirmed; closed +0.24% — near-noise; prelim (−15) a technical miss on a near-zero move. NTAP: clean beat-and-raise; closed +2.55% after an initial sell-the-news dip; prelim (−10) wrong. VSXY: EPS beat leaned on tariff refunds, revenue slight miss, Q3 operating-income guide disappointed; gapped down and kept falling to close −13.17%, the largest single-name prelim miss scored to date; prelim (+12) wrong. Preliminary read went 0-for-6 today across every researched name, panelled included — its worst day since scoring began. |

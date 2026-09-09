# Forecast accuracy ledger

Maintained by stage 4 (`earnings-calibration`), the morning after each run. Every call
is scored against the realised move, whether or not the result is flattering.

Measurement convention, applied identically every day: **close before the print → close
after the first full session following it.**

## Summary

Seven runs scored so far (2026-08-19, 2026-08-26, 2026-08-27, 2026-09-01, 2026-09-02,
2026-09-04, 2026-09-07). 2026-08-31 was checked and found to have nothing to score
(stages 0-2 never ran that day — see its own `05-outcome.md`). The 2026-09-08 run
(TTAN, CHWY, plus four non-panelled names) was checked and found **not yet resolvable**:
TTAN/BRZE print AMC 09-08 and CHWY/ASO/SAIL/SIG print BMO 09-09, so both need the close
of 2026-09-09, which had not yet happened as of this check (08:25 CEST / 02:25 ET,
hours before the US open) — left unscored, to be picked up on or after 2026-09-10.
**n=13 for panelled calls.**

| Metric | Panelled calls | Deep-dive preliminary reads |
| --- | --- | --- |
| Calls scored | 13 | 29 |
| Direction hit rate | 62% (8/13, Neutral-hit convention) | 41% (12/29) |
| Mean absolute magnitude error | n/a (no signed estimate on any panelled call — every one has been Neutral) | n/a (no magnitude estimate) |
| Median absolute magnitude error | n/a | n/a |
| Band hit rate | 62% (8/13) | n/a |
| Implied move broken | 38% (5/13) | n/a |
| Red-team reversal fired | 38% (5/13) | n/a |

**Panel vs. single deep researcher, thirteen panelled calls in — but read the n
carefully:** every panelled call to date — WOLF, OKTA, DLTR, AFRM, ESTC, DELL, CXM, AI,
SNOW, and now ABM and UNFI (each scored *twice*, from two independent re-panels three
days apart around the same 2026-09-08 print) — has still been **Neutral / No Edge**. The
panel has made zero directional calls across thirteen tries. The panelled hit rate jumped
from 44% (4/9) to 62% (8/13) this update, because all four new calls hit — but those four
calls are two underlying outcomes (ABM +7.55%, UNFI +2.28%), each counted twice because
the same event got panelled on both 2026-09-04 and 2026-09-07. **Treat the 62% figure as
resting on 9 independent events, not 13** — the true underlying picture moved from 4/9
to 6/11 independent events (55%), a real but smaller improvement than the headline
number suggests. The preliminary read, over the same stretch, went 1/4 on the new calls
(only the 09-07 ABM read flipped correctly to +12 ahead of the print; the 09-04 ABM read
and both UNFI reads missed), pulling its running rate down from 44% (11/25) to 41%
(12/29). At n=9-11 independent events either way, this is still not enough to call a
structural edge for the panel over the cheap read, but the direction of travel this
update favors the panel, reversing last update's "exactly tied" finding — largely on the
strength of ABM's red-team persona naming a specific, falsifiable bull mechanism (EPS at
or above $1.04, margin up YoY, guidance floor raised) that then happened, in **both**
independent panels of that name.

**The re-panel pair is the most informative single comparison in the ledger.** Panelling
the identical ABM/UNFI event twice, three days apart, let the panel's own consensus score
move over time against a fixed, later-known outcome. On ABM the panel got *more* bearish
as the print approached (-8.9 → -16.7) while the cheap preliminary read flipped from wrong
(-18) to right (+12) over the same three days — the panel moved away from the truth while
the cheap read moved toward it, and the run's own chair-review flagged why: four of seven
personas leaned in part on one shared Ortex article for their bearish framing. That is a
concrete, fixable finding about source diversity, not "the market was irrational." See
`research/2026/09/2026-09-07/05-outcome.md` for the full side-by-side.

One qualitative bright spot: CXM (09-01), AI (09-02), and now ABM (09-04 *and* 09-07)
are cases where a persona's *specific stated mechanism* — not just the direction —
played out exactly as described (CXM: a soft guide undercutting a technical beat, from
the red-team; AI: a short-covering bid absorbing a weak guide, also from the red-team;
ABM: the red-team's own named "what would break my bearish call" scenario — EPS at or
above $1.04, margin up YoY, guidance floor raised — happened almost to the letter, in
independently-sourced form, in both the 09-04 and 09-07 panels). These still land on
different sides of the Neutral hit/miss line (CXM missed on magnitude, AI and ABM hit),
which is itself informative: getting the mechanism right is not the same as getting the
below-expected-move sizing right. ABM is now the strongest single case in the ledger for
the red-team persona's *named scenario* being better-calibrated than its own headline
direction score, across two independent runs.

### Calibration by certainty tier

The question this table exists to answer: **do High-certainty calls actually hit more
often than Low-certainty ones?** If they do not, the tiering is decorative and
`scripts/synthesize.py` needs fixing.

| Certainty | Calls | Direction/Neutral hit rate |
| --- | --- | --- |
| High | 5 (OKTA miss, DLTR hit, ESTC miss, AI hit, SNOW miss) | 40% (2/5) |
| Med | 8 (WOLF hit, AFRM hit, DELL miss, CXM miss, ABM 09-04 hit, UNFI 09-04 hit, ABM 09-07 hit, UNFI 09-07 hit) | 75% (6/8) |
| Low | 0 | — |

Still no directional (Strong/Lean Up/Down) calls have been scored — every panelled call
to date has been Neutral / No Edge (13/13) — so this table is still scoring the
below-expected-move convention rather than the tiering's intended target. The gap this
update went from concerning to stark: High-certainty calls hit 40% (2/5, unchanged) while
Med-certainty calls hit 75% (6/8, up from 50%) — and all four new calls landed in Med
(ABM's 09-04 read stayed Med on thin-sample/reversal-risk grounds; ABM's 09-07 read was
mechanically High but the chair overrode it to Med for shared-source dependency, which
turned out to be the right call — that overridden run hit). Caveat exactly as above: two
of those four Med calls are the same two events counted twice (ABM/UNFI, both runs), so
independent-event n for Med is really 6, not 8, and the true hit rate on independent
events is 4/6 (67%) — still comfortably above High's 40%, on a pattern that has now held
in the same direction across four consecutive ledger updates. "High-certainty calls hit
less often than Med" is no longer a small-sample curiosity; `scripts/synthesize.py`'s
certainty logic needs a direct look at why High correlates with worse outcomes here,
rather than more waiting for a bigger sample to resolve it on its own.

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
| 2026-09-04 | 2 (ABM, UNFI) | 2 (ABM, UNFI) | Panelled 2/2 (100%, Neutral-hit convention); Prelim 0/2 (0%) | n/a — both panelled calls Neutral, no signed estimate | Both report BMO 2026-09-08 (window rolled through the Labor Day holiday). ABM: adj EPS $1.04 beat (~$1.01 consensus), record revenue $2.3B +4.2% YoY, FY26 guide narrowed to $3.95-4.10 with the floor raised; closed $47.05→$50.60, +7.55% — Neutral hit (near-exact match to the 7.3% expectation, band held, implied not broken); red-team's named bull mechanism ("EPS ≥ $1.04, margin up, guidance floor raised" squeezes it 6-8%) is close to exactly what happened — reversal fired; prelim (−18) wrong-signed. UNFI: adj EPS $0.69 beat ($0.61 consensus), revenue $7.64B slight miss, first FY27 guide $3.00-3.50; closed $43.93→$44.93, +2.28% — Neutral hit (well below the 10.3% expectation, band undershot); red-team's 15-20% squeeze case did not fire; prelim (−8) technically wrong-signed on a near-noise move. Independently re-panelled again 2026-09-07 — see that run for the direct comparison. |
| 2026-09-07 | 2 (ABM, UNFI) — independent re-panel of the same 2026-09-08 event already forecast 2026-09-04 | 2 (ABM, UNFI) | Panelled 2/2 (100%, Neutral-hit convention); Prelim 1/2 (50%) | n/a — both panelled calls Neutral, no signed estimate | Same realised outcomes as 2026-09-04 above (ABM +7.55%, UNFI +2.28%), scored separately as an independently-sourced forecast one day closer to the print. ABM: Neutral hit again (7.4% expectation vs 7.55% actual); panel consensus moved *more* bearish than the 09-04 run (-8.9→-16.7) while prelim flipped from wrong to right (−18→+12) over the same three days — the panel moved away from the truth, the cheap read moved toward it; chair overrode certainty High→Med for four personas sharing one Ortex article, and that override was the right call. Red-team's own "what would break my case" scenario (EPS ≥ $1.04, margin up, guidance floor raised) again matches what happened almost exactly — reversal fired a second time. UNFI: Neutral hit again (10.4% expectation vs 2.28% actual, band undershot); prelim unchanged at −8 (wrong-signed, immaterial move); neither side's large-magnitude reversal case fired. This same-event, two-forecast pair is the most direct panel-vs-panel comparison in the ledger to date — see `research/2026/09/2026-09-07/05-outcome.md`. |

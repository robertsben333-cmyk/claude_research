# Outcome — 2026-08-27

Scored 2026-09-02. Measurement: close before the print → close after the first full
session following it, applied identically to every name below.

| Ticker | Panelled | Call | Expected move | Actual move | Direction | Band hit | Reversal fired |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ESTC | Yes | Neutral / No Edge | ±13.4% | **+19.31%** | Miss (moved hard, no view) | Yes | No |
| AFRM | Yes | Neutral / No Edge | ±10.8% | **+0.35%** | Hit (below expected) | No | No |
| S | No (prelim −15) | — | implied 11.36% (Phase-0) | **−5.15%** | Prelim hit | — | — |
| MRVL | No (prelim −15) | — | implied 10.28% (Phase-0) | **−10.28%** | Prelim hit | — | — |
| RBRK | No (prelim −10) | — | implied 12.9% (Phase-0) | **−13.05%** | Prelim hit | — | — |

## ESTC — miss

Non-GAAP EPS $0.70 vs ~$0.58 consensus, revenue $478M (+15% y/y), cloud revenue growth
accelerated to 20% c/c from 19% in Q4, and FY27 guidance raised. Shares were already
+6.8% into the print on peer momentum, then jumped further after hours and kept
climbing through the next session to close +19.31%, breaking the 12.9% implied move by
~1.5x. The Neutral call lands inside its own very wide band (6.7–27.8%) but is a clean
miss under the below-expected-move convention (19.31% >> 13.4%) — the panel's consensus
score (−20.7, all seven personas between −15 and −28) leaned bearish and missed a
Lean Down call by only 4.3 points, then the stock did the opposite of what all seven
leaned toward. The red team's specific case — a repeat of the 2026-05-27 pattern where
Elastic beat and still fell on a soft FY27 guide — did not fire; this time the guide
itself accelerated and the market read it as a genuine re-rating rather than sell-the-
news. The stage-2 preliminary read (−20) called the wrong direction, and on the largest
single move scored to date.

## AFRM — hit, but band far too wide

Revenue $1,165.96M vs ~$1,128.5M consensus (a real ~3.3% beat); the headline EPS beat
looks driven by a one-time item and the market did not trade it as an operating surprise.
Shares closed effectively flat, +0.35%, on a name that has moved double digits in 4 of
its last 6 quarters. The Neutral call was the honest read of the widest split seen on
any panelled name so far (consensus score −0.1, disparity 28.0 — four personas net
positive, three net negative) and scores a hit (0.35% << 10.8% expected), but the
realised move sits below even the low end of the 5.4–22.9% band — the panel sized the
magnitude far too generously in a quarter that turned out to be a non-event. The red
team's specific reversal case — a repeat of the 2026-02-05 pattern where Affirm beat,
raised guidance, and still fell 14.5% on a provision-for-credit-losses jump — did not
fire. The stage-2 preliminary read (−18) called the wrong sign on what is functionally a
noise-level move, the same failure mode as BILL on 2026-08-19.

## S — preliminary hit (not panelled)

Revenue beat, but a trimmed forward profit forecast outweighed it; shares slid through
the after-hours reaction and into the next session to close −5.15%. Preliminary read
(−15) called the direction correctly.

## MRVL — preliminary hit (not panelled)

Clean beat-and-raise on paper (revenue +1.2% above consensus, EPS +1.19% beat, Data
Center +46% y/y, FY27/FY28 outlooks both lifted) that still sold off −10.28% on
softer-than-hoped forward framing against a trailing P/E near 83 that priced in
near-perfection. Preliminary read (−15) called the direction correctly.

## RBRK — preliminary hit (not panelled)

Another clean beat (EPS $0.20 vs $0.04, revenue beat by $31M, subscription ARR +33% to
$1.66B) that sold off anyway, falling through the next full session to close −13.05% —
a textbook sell-the-news reaction where expectations had run ahead of the outlook.
Preliminary read (−10) called the direction correctly but understated the magnitude by
roughly 3x relative to its own scale.

## Where the process failed

**The panel's first genuine break from three straight Neutral-and-prelim-was-right
runs.** WOLF, OKTA and DLTR (2026-08-19, 2026-08-26) all saw the stage-2 preliminary
read call direction correctly while the panel hedged to Neutral. Today that pattern
broke on both names: ESTC's preliminary read (−20, bearish) was wrong on the single
largest move recorded in the ledger so far (+19.31%, a beat-and-raise the market treated
as a genuine re-rating, not a repeat of the company's own well-documented
"beats-but-falls-on-guidance" pattern), and AFRM's preliminary read (−18) called the
wrong sign on a near-zero move. Across the five panelled names now scored, the
preliminary read is 3/5 (60%), not the 3/3 it had been — the "cheap read keeps beating
the panel" narrative needs revising, not confirming. On these same five names the panel
itself (Neutral-hit convention) is also 3/5 (60%) — panel and preliminary read are now
running even, not one dominating the other. That is a much weaker basis for cutting
stage 3 than the picture after three names; more panelled names are needed before acting
on either signal.

**Certainty tiering keeps running backwards.** ESTC was tagged **High** certainty and
missed; AFRM was tagged **Med** and hit. Across all five panelled calls to date, High
certainty is now 1/3 (OKTA miss, DLTR hit, ESTC miss = 33%) and Med certainty is 2/2
(WOLF hit, AFRM hit = 100%). This is the same direction of anomaly flagged after
2026-08-26 with only 2 vs 1 calls; it has now grown to 3 vs 2 and the gap has widened
rather than closed. This is no longer just "flagging" territory — `certainty_score`'s
main driver in both ESTC and AFRM was red-team reversal risk (72 and 65, both tagged
High reversal-risk tier), and in neither case did the red-team's own named mechanism
fire. If certainty is being driven mainly by reversal-risk magnitude rather than by how
much the panel actually agrees, that would explain why High-certainty calls are not
outperforming — worth a direct look at how `certainty_score` is composed in
`scripts/synthesize.py` before more calls accumulate on the same drivers.

**Magnitude bands are still not calibrated to be informative.** ESTC's move landed
inside its band only because the band is 6.7–27.8 points wide (a >20-point span);
AFRM's fell below its own 5.4% floor. Band hit rate to date across all five panelled
calls is 4/5 (80%), which sounds good until you note the bands are wide enough that a
near-flat move (AFRM) is now the only miss on the low side and a >19% move (ESTC) still
counted as a "hit" on the high side. A band that is rarely missed is not obviously doing
useful work; this metric needs either tighter construction or a companion "how much of
the band did the move use" measure before it can distinguish a well-sized panel from a
hedge-everything one.

---

*This is a forecasting research exercise over public information. It is not investment
advice.*

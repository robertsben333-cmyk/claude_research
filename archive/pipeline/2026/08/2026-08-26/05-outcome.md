# Outcome — 2026-08-26

Scored 2026-08-28. Measurement: close before the print → close after the first full
session following it, applied identically to every name below.

| Ticker | Panelled | Call | Expected move | Actual move | Direction | Band hit | Reversal fired |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OKTA | Yes | Neutral / No Edge | ±13.4% | **+28.63%** | Miss (moved hard, no view) | Yes | No |
| DLTR | Yes | Neutral / No Edge | ±9.9% | **−3.92%** | Hit (below expected) | No | Yes (mechanism, not magnitude) |
| NTNX | No (prelim −10) | — | implied 14.49% | **+6.81%** | Prelim miss | — | — |
| STDN | No (prelim −15) | — | no implied move | **+4.45%** | Prelim miss | — | — |

## OKTA — miss

Revenue $805M (+11% y/y, beat), non-GAAP EPS $1.05 (beat), cRPO +14% y/y to $2.585B —
well past the ~11% Q3 guide the panel's two most bearish personas (Fundamental,
Options & Positioning, both −18) were leaning on. FY27 guidance raised on both revenue
and EPS. Shares jumped ~19% after hours and kept climbing the next session to close
+28.63%, more than double the 13.0% implied move. The Neutral call lands inside its own
wide band (6.7–31.6%) but is a clean miss under the "hit when the realised move comes in
below the expected move" convention — this is the textbook "panel had no view, stock
moved hard anyway" case. The stage-2 preliminary read (+10) called the direction right.

## DLTR — hit, but band too wide

Clean beat on both EPS ($2.70 vs $1.11) and revenue ($4.9B), but Q3 EPS guidance
($0.80–0.95) landed far below the ~$1.39 Street estimate. Shares gapped down as much as
~9% at the open before recovering through the session to close −3.92% — an intraday
reversal a close-to-close number hides. The Neutral call scores a hit (3.92% < 9.9%
expected), but the realised move actually falls *below* the low end of its own
4.9–23.3% band, so the panel's magnitude sizing overshot even on the correctly-hedged
side. The red-team's specific mechanism — a cautious forward guide overshadowing a
headline beat — is exactly what fired; only its stated −10% magnitude overshot the
close-to-close outcome. The stage-2 preliminary read (−10) called the direction right.

## NTNX — preliminary miss (not panelled)

Beat on revenue and ARR, raised FY27 guidance; stock rose 6.81%, comfortably inside the
14.49% implied move. Preliminary read (−10) called the wrong direction.

## STDN — preliminary miss (not panelled, panel-ineligible)

First commercial TRISO deliveries, growing backlog, still loss-making but well
capitalised. Stock rose 4.45% — a continuation of its pre-print run rather than a sharp
reaction. No implied move existed to size this against (thin post-IPO trading history),
which is exactly why it was excluded from the panel. Preliminary read (−15) called the
wrong direction.

## Where the process failed

**The panel converged to Neutral / No Edge on both panelled names for the third
straight panelled run** (WOLF on 2026-08-19, now OKTA and DLTR). In all three cases the
stage-2 preliminary read called the actual direction correctly; the seven-persona panel
has yet to make a single directional call (Strong/Lean Up or Down) — every panelled
verdict so far has hedged to Neutral. That is not automatically wrong (Neutral scored a
hit on WOLF and DLTR), but on OKTA it meant the panel explicitly declined to have a view
on a stock that then moved 28.6% — more than double its own implied move — in the
direction three of its own seven personas' central estimates already leaned. This is a
fixable finding, not market irrationality: the synthesis logic that collapses
persona spreads of ±18 to a "no edge" consensus of −1.4 (OKTA) may be discounting
genuine, sourced disagreement (two personas at −18 on cRPO/valuation, three at +8 to +12
on de-risked positioning) into a null call too readily. Worth checking whether
`scripts/synthesize.py`'s Neutral threshold is calibrated against enough historical
spread to justify how often it fires — three panelled runs, three Neutral calls is a
small sample, but it is now a pattern, not a coincidence.

**Magnitude bands remain uncalibrated in both directions**: OKTA's actual move sat at
the very top of its band (near the label "the implied move is roughly one standard
deviation, not a cap" — it needed almost the full band width to be correct), while
DLTR's actual move fell short of even the *low* end of its band. Two data points, two
band misses on opposite sides — too little to diagnose a systematic bias yet, but worth
tracking as band-hit rate accumulates.

---

*This is a forecasting research exercise over public information. It is not investment
advice.*

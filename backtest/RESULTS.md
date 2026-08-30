# Results — pilot-40, three arms, 37 events

Exploratory. Read as direction of travel, not verdicts. Criteria were fixed in
`PREREGISTRATION.md` before these numbers existed.

Three events left the sample: **FCN** (mis-dated, not an earnings event as drawn),
**VG** (mis-dated by 12.5h, pending re-harvest), **CW** (the results wire was in the
corpus). All 37 remaining events carry all three arms.

## The headline

| | arm A naive | arm B plan-first | arm C skill | floor |
| --- | --- | --- | --- | --- |
| direction rate | 72% (13/18) | 71% (12/17) | **55%** (12/22) | 62% free rule; coin 32–68% |
| return/trade, exit open | **+0.90%** | +0.45% | **−1.16%** | always_down +0.25% |
| return/trade, exit close | +2.16% | **+2.24%** | +0.11% | — |
| total return, exit close | +38.9% | +38.2% | +2.3% | — |
| magnitude rho | 0.316 | 0.291 | **0.333** | proxy 0.131 |
| magnitude median error | 3.35pp | **3.09pp** | **3.09pp** | proxy 3.64pp |
| top-8 capture | 4/8 | 4/8 | 4/8 | null 1.7 |

## 1. Magnitude is the real result

**All three arms beat the proxy on both measures.** Rank correlation roughly 0.29–0.33
against the proxy's 0.131, and median error 3.09–3.35pp against 3.64pp. Each arm put
**4 of the 8 biggest movers in its own top 8** — null expectation is 1.7, and 4 would
have been p≈0.04 had this been a powered test.

This was the pre-registered primary and it is the one place the answer is clean. The
arms know which prints are going to be large. They knew AAP, PWR, ENTG, RBRK and KEEL
were big events before they happened.

### But they under-scale, systematically

| | actual | A | B | C |
| --- | --- | --- | --- | --- |
| AAP | 24.6% | 11.0 | 10.5 | 8.5 |
| PWR | 17.3% | 7.5 | 7.5 | 7.0 |
| ENTG | 15.5% | 8.0 | 8.0 | 7.5 |
| AVNT | 12.5% | 4.5 | 4.3 | 4.2 |
| TILE | 9.1% | 5.0 | 2.5 | 3.0 |

Seven of the eight biggest movers came in under-forecast by all three arms, several by
half or more. **This is the most actionable finding in the study**: a consistent bias is
correctable in a way a coin flip is not. Roughly doubling `expected_abs_move_pct` above
some threshold would have improved every arm.

The one over-forecast, DUOL (9.4% actual against 12.5–13.0 predicted), is the exception
that shows the mechanism — all three read a name that had fallen 65% and had three
consecutive double-digit reactions, and extrapolated a tail that did not arrive.

## 2. Direction: A and B clear the free rule, C does not

72% and 71% sit above the 62% `last_reaction` rule, on 17–18 calls. The coin's 5–95
interval at that sample size is 32–68%, so this is **suggestive and not established** —
exactly what the plan said direction could be.

**Arm C, the live pipeline's own method, is the outlier at 55%.** It also traded most
(22 of 37 versus 17–18) and lost money at the open exit. The pattern that produces this
is visible in the call distribution:

```
A naive       Lean Down  7   Lean Up 11   Neutral 19
B plan-first  Lean Down 13   Lean Up  4   Neutral 20
C skill       Lean Down 13   Lean Up  9   Neutral 15
```

C abstains least and commits most. Its own instructions tell it Neutral is legitimate
only when evidence genuinely splits — and the effect of that wording appears to be
fewer abstentions and worse calls.

**No arm ever issued Strong Up or Strong Down.** In 111 forecasts the five-point scale
collapsed to three. `direction_score` never left ±26.

## 3. Abstention works, but not the way I predicted

At n=8 it looked like Neutral tracked events that moved less. Across 37 that is gone:

| | mean abs move on Neutral | on traded |
| --- | --- | --- |
| A | 4.50% | 4.99% |
| B | 4.76% | 4.72% |
| C | 3.74% | 5.42% |

Barely separated for A, not at all for B. **But abstention still pays**, on a different
mechanism — per-trade return against the same arm forced to trade all 37:

| | selective | forced |
| --- | --- | --- |
| A | **+0.90%** | −0.30% |
| B | **+0.45%** | −0.31% |
| C | −1.16% | −0.92% |

A and B turn a losing book into a winning one by choosing *which* events to trade. They
are not identifying quiet events; they are identifying events where they have an edge.
That is a more useful skill and a more surprising one.

For C, abstaining makes it slightly worse — it declines the wrong ones.

## 4. Calibration: the tier is nearly unused, but it separates

No arm issued a single High-certainty call. Where `Med` appears at all it beats `Low`:
A 5/5 versus 8/13, B 3/4 versus 9/13. C issued no Med calls at all — every one of its 22
directional calls was `Low`.

Direction of travel is right this time (the archive found the field running backwards),
but on 4–5 Med calls it is an anecdote.

## 5. Coverage does not explain the ranking

| | usable news | thin | starved |
| --- | --- | --- | --- |
| A | 10/14 (71%) | 2/2 | 1/2 |
| B | 8/10 (80%) | 2/5 | 2/2 |
| C | 8/15 (53%) | 1/4 | 3/3 |

All three went 6/7 on the news-starved events, off filings and anchors alone. The news
layer — the expensive half of the corpus, and the half that took a CC-NEWS sweep, three
providers and four leak fixes to build — **is not visibly what separates the arms**.

## What I would carry into the live pipeline

1. **Scale the magnitude forecasts up.** The under-scaling is systematic and large.
2. **Stop asking for direction with confidence.** 111 forecasts produced no Strong call
   and nothing past ±26 on a ±100 scale. The scale is aspirational.
3. **Let the method abstain more.** The arm that traded least made the most per trade;
   the arm that traded most lost money.
4. **Look hard at why C trails.** It is the current production method, it committed most
   often, and it scored worst on direction. The instruction to be exhaustive may be doing
   more harm than the instruction to treat Neutral as a real call does good.

## What this cannot support

n=37 with 17–22 directional calls per arm. The direction ranking (A≈B > C) is a lead,
not a finding. The sample skews down (18 of 40 up) and B is the most bearish arm by a
distance — 13 Lean Down against 4 Lean Up — so some of B's result is the sample rather
than the method. A is the more interesting case: it is the most balanced arm (11 up, 7
down) and still scored 72%.

The magnitude result is the one worth acting on.

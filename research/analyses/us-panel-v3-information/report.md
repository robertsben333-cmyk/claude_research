# US panel v3: what information moves the market reaction, and how sure the panel is

*Second pass, 2026-11-14. Stage E-P, us-panel.v3 (29 Oct to 12 Nov, 218 names, 11 run days) leads; us-panel.v2 is used only as a check on direction. The first pass is kept as `report-pass1.md`. Scripts: `hier.py` (the multilevel model), `hier2.py` (placebo, leave-one-day-out, certainty, modifiers), `hier3.py` (reaction given the print); output in `hier*-results.txt`.*

*Committed 2026-11-14 as the operator supplied it, as the basis for stage E-P v3b. `report-pass1.md`, the `hier*.py` scripts and their outputs were not part of what was supplied and are not in this folder.*

## The short version

1. **A point the judges size shows up in the move, but evidence type barely matters.** In v3 a judged point carries about 0.8 of a point of move, after removing what moved every stock that day (probability above zero 0.90). Letting each evidence type have its own weight explains no more than random labels do. Reweighting by type also does worse on held-out days than the judges' plain sum.
2. **Two leads hold across several different measures.** Evidence about **the bar against consensus** carries the least per judged point, in v3 and in v2. Evidence about **what the market already expects** (run-up, a stretched price, the price path into the print) carries the most. Neither is significant alone. Together they are the strongest signal in this review and point to one prompt change.
3. **Certainty is roughly right in scale and too narrow to use.** The judges' p_up is about calibrated in v3 (slope 0.71, probability above zero 0.87). But it barely moves: its standard deviation across names is 5.7 points. Above panel_pct 50, every band pays about the same, so a 90 is not surer than a 65.
4. **Once the release is known, the panel's score adds nothing.** The release explains only about a fifth of the move. The rest is the reaction (the call, the next guide, the price path), and that is where the misses are.

## How I measured it

Xavier's point taken: the target is the stock's reaction, not beat or miss. Every model below predicts the move itself.

- **The move is scaled by the sealed expected move**, so a 20%-volatility name and a 5% name count alike. The judges' sizes are scaled the same way.
- **Day effects are random effects.** On some days everything rose, and that should not count as skill. In v3 the day effect has a standard deviation of 0.29 expected moves; the name-level noise is 1.2. So days matter, but most of the variance is name noise.
- **Effects are partly pooled.** Each evidence type gets its own weight, drawn toward a common weight. Types with little evidence are pulled toward the average rather than reported at face value. Fitted by Gibbs sampling; I report the posterior mean, an 80% interval and the probability the effect is positive.
- **Two simulation checks.** A placebo shuffles the type labels across items 40 times. Leave-one-day-out refits on ten days and ranks the eleventh.
- **Near-significant leads count**, as Xavier asked. I call something a lead when at least three different measures point the same way with a probability around 0.8 or higher. Most of the indications are v3-only, and I say so where that is the case.

## 1. What the robot collects (v3)

Per name: about 7.7 filed findings, 3.5 rejected, 1.5 outside the window, 6.7 "searched and found nothing", about 19 sources. A third cite sec.gov.

| Evidence type | Share of items | Share of judge weight |
|---|---|---|
| Guidance and management commentary | 18% | 24% |
| Consensus and the bar | 14% | 16% |
| Positioning (short interest, options) | 10% | 13% |
| Customers, suppliers, orders, backlog | 9% | 10% |
| Peer read-through | 9% | 9% |
| Capital, financing, M&A, distress | 9% | 7% |
| Company's own other figures | 9% | 4% |
| Regulatory, legal, clinical, tariffs | 5% | 3% |
| Insider trades | 5% | 2% |
| Macro and industry data | 4% | 3% |
| Analyst actions, alternative data, price path, people, reaction history | 9% | 9% |

By line: reported quarter 32%, guidance 27%, positioning 17%. The judges never sized any of the 2,547 items the searcher rejected or set aside.

## 2. What holds value for the reaction

### Per evidence type (v3, judges' sizes, day effects removed)

| Type | Names | Weight per judged point | 80% interval | P(>0) | P(above the average type) |
|---|---|---|---|---|---|
| Customers, suppliers, orders | 92 | +1.32 | +0.49 to +2.13 | 0.98 | 0.86 |
| Positioning | 150 | +1.12 | +0.18 to +2.05 | 0.94 | 0.68 |
| Capital and financing | 107 | +1.09 | +0.11 to +2.05 | 0.92 | 0.65 |
| Guidance and management | 156 | +0.96 | +0.25 to +1.63 | 0.96 | 0.63 |
| Peer read-through | 104 | +0.58 | −0.52 to +1.56 | 0.78 | 0.33 |
| Company's own figures | 96 | +0.60 | −0.50 to +1.58 | 0.79 | 0.36 |
| **Consensus and the bar** | 141 | **+0.37** | −0.75 to +1.39 | 0.70 | **0.19** |
| *Average type* | | *+0.82* | *+0.01 to +1.55* | *0.90* | |

The smaller types (analyst actions, insider trades, alternative data, macro, reaction history) all sit near the average, between +0.68 and +0.90, because they have too few names to pull away from it.

**Placebo check.** With shuffled labels, the spread between types is larger than with the real labels in 82% of runs. So the type differences in this table are within noise. **Leave-one-day-out:** weighting by type ranks held-out days at rho −0.06, against +0.03 for the judges' plain sum and +0.07 for the panel score. A type-weighted score would not help.

What this does say is that **a judged point is worth roughly a point** (+0.82 in v3; +0.24 in v2, where it was not reliably above zero). The judges' scale is about right in v3. Gains have to come from better evidence, not from re-weighting the evidence there is.

### The leads that point the same way in several measures

**Lead A. Evidence on the bar against consensus is over-weighted.**

| Measure | v3 | v2 |
|---|---|---|
| Type model, consensus: P(above average) | 0.19 | 0.13 |
| Same, with the searcher's own sizes | 0.16 | 0.07 |
| Line model, reported quarter: P(above average) | 0.13 | 0.67 |
| Share of on-side weight from consensus, effect on side return | −0.08 (P>0 0.14) | +0.01 |
| Good print, long call: share right | 18 of 32 (56%) | 13 of 22 (59%) |

A beat against consensus is the normal case: two thirds of releases are positive. Evidence that "the quarter will beat consensus" is therefore mostly already expected, and the market trades against a higher bar.

**Lead B. Evidence on what the market already expects is under-weighted.** These are items about the run-up, a stretched price, the price against analyst targets, or a drawdown into the print.

| Measure | v3 | v2 |
|---|---|---|
| Share of on-side weight from these items, effect on side return (all names) | +0.13 per sd (P>0 0.96) | +0.05 (P>0 0.78) |
| Same, panel_pct 50-79 | +0.17 (P>0 0.93) | −0.08 |
| Same, panel_pct 60 and higher | +0.08 (P>0 0.81) | +0.04 (0.66) |
| Items pointing the right way, name level | 62% (p 0.08) | 57% |
| Given the release, the 20-day run-up still predicts the move | +0.09 per sd (P>0 0.80) | +0.20 (P>0 0.94) |

The plain run-up number does not do this alone: as a side modifier it reads −0.08 in v3. What helps is the searcher's researched read of positioning and expectations.

**Lead C. Management statements inside the quarter help (v3 only).** These are reaffirmations, "on track" remarks at conferences, and pre-releases. When one of them was the main item of a call at 60 or higher: 16 calls, 62% right, +10.2%. As a modifier: +0.11 per sd in 50-79 (P>0 0.82) and +0.09 at 60+ (0.85). In v2 it reads −0.03.

**Lead D. One-off items and peer read-throughs are weak (v3 only).** One-offs (refunds, settlements, impairments): items point the right way in 41% of names (p 0.09), the one-off line in 36% (p 0.05), and as a modifier in 50-79 −0.13 (P>0 0.12). Peer read-throughs: P(above average) 0.33, modifier −0.08 to −0.10 (P>0 0.15 to 0.20). v2 does not agree on peers.

**Lead E. Counterparty numbers are the best evidence per point (v3).** Customers and suppliers reporting on the same quarter, orders and backlog: weight +1.32, P(above average) 0.86, and the same ranking with the searcher's own sizes. v2 puts them at average.

**Lead F. A contested call is not a weak call.** In v3, more disagreement between the judges on p_up goes with a *better* side return (+0.12 per sd, P>0 0.94). This matches sel.v1's "three high, one out" (+7.0%, n 29, p 0.01). v2's mid band leans the other way (−0.07).

Leads that conflict between versions and should not be acted on: guide-gap arithmetic (v3 +0.09, v2 −0.11 at 60+), positioning as a modifier (v3 +0.08, v2 −0.15 at 60+), and the judges' move size against the option-implied move (negative on raw returns, positive on scaled returns).

## 3. How sure the panel is (goal b)

**Return on the panel's side per band, v3, day effects removed** (in expected moves, translated at each band's median expected move):

| panel_pct | Names | Effect | P(>0) | About |
|---|---|---|---|---|
| 0-29 | 71 | +0.06 | 0.67 | +0.5% |
| 30-49 | 41 | −0.13 | 0.22 | −1.1% |
| 50-59 | 18 | +0.09 | 0.70 | +1.2% |
| 60-69 | 21 | +0.16 | 0.82 | +2.0% |
| 70-79 | 21 | +0.16 | 0.79 | +2.1% |
| 80-89 | 19 | +0.13 | 0.76 | +1.8% |
| 90-100 | 15 | +0.09 | 0.68 | +1.3% |

Above 50 the score separates "something" from "nothing", but there is no gradient. A 90 is not surer than a 65. (v2 is flat to negative in every band.)

**The judges' p_up** is about calibrated in v3: probit slope +0.71 (80% interval −0.10 to +1.51, P>0 0.87), where 1 means calibrated and 0 means no information. The searcher's p_up has slope +1.18 (P>0 0.89). The problem is resolution: the judges' mean p_up has a standard deviation of only 5.7 points across names. They rarely commit, and when they do, the sizing does not sort the outcomes.

**What sorts the 50-79 band (v3, all features fitted together, partly pooled):** the market-cap band $0.3-10bn (+0.11, P>0 0.84), expectations items (Lead B, +0.17, 0.93), mid-quarter management statements (Lead C, +0.11, 0.82). Against: one-off items (−0.13, 0.12), peer items (−0.10, 0.20), consensus items (−0.07, 0.27). Judge certainty, the number of findings and the lowest judge's score sort nothing.

## 4. What it misses: the reaction after the release

For the 66 v3 names scored 60 or higher with a stage M release read, I modelled the move on the release read, the guide direction, the panel score and the pre-print evidence:

| Given the release, what still predicts the move (per sd) | v3 | v2 |
|---|---|---|
| Release read | +0.66 (P>0 1.00) | +0.54 (1.00) |
| Panel score from the day before | −0.08 (0.34) | −0.35 (0.04) |
| Judged evidence on the guidance line | +0.10 (0.78) | −0.06 |
| Judged evidence on the bar and the reported quarter | −0.09 (0.23) | +0.18 (0.90) |
| 20-day run-up, signed | +0.09 (0.80) | +0.20 (0.94) |

The release and the guide together explain only 22% of the scaled move in v3. Everything the panel knows works through anticipating the release. What decides the rest (the call, the next guide, what was already expected) is barely researched. The wrong 80+ calls show the same two shapes as in the first pass: longs whose beat was sold (FNKO, OMDA, AXTI, INSP, DOCN, ICHR, VFF) and shorts on a guide cut that became a beat and raise (IBTA, DUOL, CURI, HLF).

## 5. Reflection

My first pass asked whether the robot reads the quarter. That was the wrong target. Asking what moves the reaction gives a more useful answer.

- The robot's information is roughly priced at the right scale in v3, and its type mix is not the problem. More breadth or a different weighting by type will not help. The placebo and the held-out days both say so.
- The problem is what is missing. The panel researches the quarter against consensus, which the market treats as the base case. It does not research the bar the market really holds or how this stock will take the next guide.
- Certainty cannot be fixed by asking the judges to be bolder. Their p_up is already about calibrated. It can only improve if they are given the evidence the reaction turns on, and if the forecast is split so each part can be scored.
- What I cannot say yet: about 25 to 30 more v3-like run days are needed before an effect of 0.1 expected moves per sd (the size of Leads A to F) would show at a probability of 0.95. Each lead is a reason to change the prompt and measure, not a proven effect.

## 6. Prompt and process suggestions

Nothing has been changed. A searcher or judge change is a new prompt version, judged only on its own runs.

**Searcher (us-searcher.v4):**

1. **An expectations block, sized like any finding (Leads A and B).** Always file: the price path into the print (5 and 20 days, against the sector), the price against analyst targets, the whisper or buy-side bar if one is reported, last quarter's beat size and the stock's reaction to it, and the short-interest trend. The question each item answers is "what does the market already expect, and is the release likely to clear that, not consensus?"
2. **Always search for statements made inside the quarter (Lead C).** Conference remarks, reaffirmation 8-Ks, pre-releases and investor-day targets, dated after the last call.
3. **A next-guide item (section 4).** The likely direction of the next guide, with the street's next-quarter and full-year numbers against it.
4. **Counterparty numbers first (Lead E).** Customers, suppliers and distributors that reported on the same quarter, before generic peers. A peer read-through must name what links the two companies (same customers, same product, same channel).

**Judges (panel-judge, new version):**

5. **Treat a beat against consensus as the base case (Lead A).** Two thirds of prints beat. Size "the quarter beats consensus" small unless the expectations block shows the real bar is also cleared.
6. **Size one-offs and unlinked peer read-throughs small (Lead D).**
7. **Split p_up into three parts:** P(the quarter clears the real bar), the most likely guide direction, and the reaction under each. The final p_up and size stay as they are; the parts are recorded beside them.

**Process:**

8. **Score the three parts against stage M automatically.** Stage M already records the release read and the guide direction for every name at 60 or higher. A small resolver that joins the two would show each week which part of the forecast fails.
9. **Pre-register Leads A to F** with the new version and re-run `hier2.py` on its runs after about 20 run days. A lead that keeps its sign earns a stronger prompt instruction; one that flips gets dropped.
10. **Leave the selection rule alone**, apart from the shadow books already running (sel.v1, market-cap band). There is no gradient above 60 to exploit, and a contested call is not a weaker one.

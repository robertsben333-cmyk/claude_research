# Nine pre-registered hypotheses about stage E

Registered 2026-09-10. Nothing in this file changes the hunter, the scorer or the book.

Everything in `EDGE_ANALYSIS.md` was found by looking at the data that produced it.
That is how hypotheses are made and it is not how they are tested. This file fixes the
tests **before** the data that will settle them exists, so that nobody has to reconstruct
later whether a cut was chosen after the fact.

Score them with:

```bash
python3 edge/scripts/edge_hypotheses.py                     # all three samples
python3 edge/scripts/edge_hypotheses.py --since 2026-09-11  # the forward test alone
```

## The three samples

| | events | what it is |
| --- | --- | --- |
| **discovery** | 67 names, 303 findings, 7 days | `edge/ledger/` through 2026-09-10. Every hypothesis below was read off it. Its numbers exist so the forward test has something to be compared against, and for nothing else. |
| **corpus** | 73 names, 129 findings, 7 days | `edge/ledger/corpus/`, built by pointing `edge_ledger.py --runs 'backtest/runs/edge-corpus/*'` at the sealed backtest. Hunters saw a point-in-time capture and could not search past the print. Genuinely out of sample for anything read off the live runs. |
| **forward** | 0 | everything from 2026-09-11. This is the test. |

The corpus is not a clean replication and must not be read as one. Its limits are in
`backtest/FINDINGS.md` §33: every event runs on the historical-reaction anchor because
the option chain is unrecoverable retrospectively, 30 of the captures kept sweeping past
the print, and its hunters averaged 1.8 findings a name against 4.5 live. A category
that needs the open web is thin or absent there, and **absence is not disconfirmation**.

## The nine

Each row: the discovery estimate that generated it, the corpus reading where one exists,
and how many events the decision rule needs at 80% power (exact binomial, two-sided,
α = 0.05, computed by the script rather than quoted).

| # | claim | discovery | corpus | needs |
| --- | --- | --- | --- | --- |
| **H1** | a finding bridging a third-party series to the company is right < 50% | 3/15 findings, 1/8 as lead, p = 0.035 | 3 findings only — untestable | 49 |
| **H2** | a filing-led call beats the sample base rate by ≥ 10pp | 15/22 = 0.682 vs 0.537 | 18/31 = 0.581 vs 0.521 (+0.06) | 90 |
| **H3** | an aggregator-led call is below the base rate | 2/4 | **1/8 = 0.125** vs 0.521 | 49 |
| **H4** | a source > 60 days old beats one < 3 days old | 0.586 vs 0.400 | 0.588 vs 0.455 | 199 |
| **H5** | conviction ÷ implied move beats raw conviction **and** beats 1/implied | 0.273 vs 0.209 raw, **0.227 for the control** | 0.241 vs 0.025 raw, **0.264 for the control** | 90 |
| **H6** | the gate the money rides on, `\|impact_sum\| >= 3`, is right > 50% | 24/35; 17/24 single-hunted | 16/28 = 0.571 | 63 |
| **H7** | where the hunt and −run-up disagree, the hunt wins | 15/24 against 9/24 | **12/24 against 12/24** | 136 |
| **H8** | the NULL: the magnitude carries nothing, slope = 0 | slope −0.021, t = −0.09 | slope +0.187, t = +0.40 | — |
| **H9** | a free number, −implied move, predicts whether calls come out right | ρ = 0.227, p = 0.117 | **ρ = 0.264, p = 0.020** | 90 |

### H5 and H9 are the same finding, and the control is winning

H5 began as "normalise the conviction by how much the name can move" and looked like the
best thing in the file: on the corpus, where the raw key ranks at ρ = 0.025 and the whole
stage was declared dead, the ratio ranks at 0.241 with p = 0.035.

Then the obvious control was run. **`1/implied` on its own ranks at 0.264, p = 0.020** —
better than the ratio. The entire effect is that quiet names are easier to call, and no
hunting is required to know which names are quiet. On the live sample the ratio leads the
control by 0.046, which is nothing.

So H5 is registered in the only form that can settle anything: the ratio must beat
`1/implied` by at least 0.08, not merely beat the raw key. It starts life leaning
rejected. And the control was promoted to H9 in its own right, because if a free number
predicts call accuracy then **every rate in H2, H3, H4 and H6 has to be re-read
conditioned on it** before any of them means anything.

### The free control is not stable across the two samples

`-run_up_20d_pct` ranks the six fitted live days at +0.335 and is positive on 6 of 6 when
traded. On the corpus's 71 anchored events it ranks at **−0.266, p = 0.018** — the same
sign test, the opposite answer, and significant in the wrong direction. Whatever
`-run_up` is measuring, it is not stable across two samples drawn months apart. Any
statement of the form "the stage has not beaten the free control" inherits that
instability and should be read as being about one particular seven-day window.

### H1 was made partly untestable on purpose

The series-bridge instruction went into `.claude/agents/unpriced-hunter.md` on
2026-09-10, before this file existed, because the discovery evidence was strong enough to
act on and the book is live. That was right for the money and it starves the experiment:
if the category disappears the hypothesis stops being testable and the instruction stands
on 15 findings forever. The corpus offered no rescue — only 3 bridged findings exist
there, because a sealed capture rarely contains a macro series.

If the forward runs produce zero bridged findings for a month, the honest options are to
leave the instruction in place on weak evidence, or to lift it deliberately for a fixed
window and re-measure. Decide that in a month; do not drift into the first by default.

## What would make all of this cheap to settle

Every test above is thin because there are seven days of live data. Two things would fix
that faster than waiting:

- **Stage C is off.** It was disabled on 2026-09-09 and it is the only stage whose day
  cannot be redone. Every day it stays off is a permanent hole in the corpus that would
  otherwise give these hypotheses a second sample of 15 events a day at no model cost.
- **The corpus can be re-run.** `backtest/runs/edge-corpus/` already holds captures that
  the current hunter contract has never been applied to. Re-running it would not be a
  clean out-of-sample test of anything read off it, but it would give H2, H3, H4 and H9 a
  second reading at a hundred events instead of seventy.

## Rules for reading this file later

1. A hypothesis is settled by the **forward** column, not by the other two.
2. `discovery` numbers are not evidence for the thing they generated. They are printed to
   make a forward disagreement visible, and for nothing else.
3. Nine hypotheses on one sample is nine chances to find something. At α = 0.05, one
   false positive is the expected outcome. A single `supported` verdict among the nine is
   not a finding; two or three that also carry their mechanism are worth acting on.
4. If a hypothesis is rejected, write that into `EDGE_ANALYSIS.md` with the same weight a
   confirmation would get. The point of registering it is that the answer counts either
   way.

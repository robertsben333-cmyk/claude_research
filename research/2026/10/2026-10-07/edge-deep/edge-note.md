# Stage D (deep), 2026-10-07: test run

**This is stage D: three names drawn at random, one deep Opus 5.5 researcher each, no orders.**
Names: PEP (bmo 10-08), RGP (amc 10-07), TLRY (bmo 10-08). Three names on one day are an anecdote.
This is a test run on the branch `claude/us-deep-research-stage-b14oox`, not a live stage.

## The answer

All three researchers ended at **no trade**. Every key question came back at or just past
its priced answer, so all three numbers are small, slightly negative and well under the
2.8 floor (|impact_sum| p22 to p42 of Opus 5.5's own reference names).

| name | impact_sum | quick read (pre_research) | abs_move | p_up | decision | what would change it |
| --- | --- | --- | --- | --- | --- | --- |
| PEP | -0.70 | +0.30 (p_up 52) | 4.5 | 45 | no trade, medium | FY core cc EPS guide cut below +4% makes it a short |
| RGP | -0.80 | -2.00 (p_up 45) | 9.0 | 48 | no trade, low | FQ2 revenue guide midpoint ≥ ~$104m long, < ~$98m short |
| TLRY | -0.40 | +0.20 (p_up 48) | 10.0 | 46 | no trade, low | a cut or fuel caveat on the $68-75m FY27 EBITDA guide makes it a short |

Depth moved the number on every name, in both directions: PEP and TLRY went from a small
positive quick read to a small negative, and RGP's -2.0 quick read shrank to -0.8 once the
staffing data published since its July guide was read. Whether that movement is worth
anything is what the resolved names will say.

## Per name

**PEP.** Five questions: North America organic (30%), FY guide held at the low end (30%),
Q3 core EPS vs $2.30 (15%), International ≥6% (10%), an NA cost update or 2027 framing (10%).
The one unpriced tilt is input costs since the July call (Brent +29%, diesel +25%, corn +17%,
sugar +38%), which thickens the guide-cut tail; sized -0.5. NA a touch weaker than modelled,
-0.3. Q3 EPS carried by the pre-announced tariff refund and FX, +0.1.
Premortem: a low-end hold plus PFNA volume growth on share gains, with sentiment washed out
after two downgrades, gives a +4 to +7% relief move (Q2).

**RGP.** Five questions: the FQ2 revenue guide (35%), FQ1 revenue vs the $97-102m guide (15%),
run-rate SG&A (15%), the dividend (12%), cash at quarter end (8%). The FQ2 consensus of $105.6m
is inflated by one $115m estimate; RGP's own per-day run rate gives $96.7-103.6m, so the guide
likely prints "below consensus" (-0.5). Cash projected to ~$68m from $82.4m (-0.5). The CFO left
for a CFO role at Xponential, not over the quarter (+0.2).
Premortem: a guide with sequential growth (≥ ~$104m) on a name near its low with a 7.6% yield
and an activist gives +10 to +15% (Q1).

**TLRY.** Five questions: FQ1 revenue (15%), FQ1 adjusted EBITDA vs the ~$11.3-12.5m the guide
implies (25%), the FY27 guide (30%), cannabis (15%), dilution (5%). Diesel stayed at the level
that cost $2.3m of surcharges (-0.5); the September oil spike raises the odds of a qualified
guide (-0.5); shares up 8.5% in two months, about 6m likely ATM (-0.1); revenue at the top of
the bar on BrewDog's first full summer (+0.3); 13% of shares short at the 52-week low (+0.4).
Premortem: a clean reaffirmation squeezes the short base, +10 to +20% (Q3).

## What the test run taught about the stage

- **It finishes.** Each researcher took 25 to 29 minutes, about 80 tool calls and about 355k
  tokens, well inside the ceiling. Every hunt carries all six required blocks
  (`questions_frozen`, `pre_research`, `key_questions`, `premortem`, `pre_lessons`,
  `investment_decision`), and every `impact_sum` equals the sum of its findings.
- **The questions are good and checkable.** Every name froze a guidance question as its
  heaviest weight, which matches what these three stocks have historically traded on.
- **Depth shrank the signal toward zero on all three.** Read with care: this is the
  "depth buys confidence, not accuracy" history in reverse, and it may simply mean these
  were three names with nothing unpriced. All three p_up sit at 45-48, the mild pessimism
  LESSONS already warns about.
- **The option anchor was missing.** Baselines sealed before the US open have no two-sided
  chain, so PEP and TLRY sourced an implied move from published pages and RGP has no options.
  The proposed Routine time (10:00 ET) fixes this.

## Comparison with stage E and E-P

Not yet: stage E and E-P fire at 17:04 and 17:06 UTC. Added after they run.

## What the numbers are not

No hit rate exists until names resolve (RGP after tonight's close, PEP and TLRY before
tomorrow's open), and the pooled comparison needs weeks of days before it can say anything.

This is a forecasting exercise over public information, not investment advice.

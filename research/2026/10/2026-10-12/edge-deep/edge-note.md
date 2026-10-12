# Stage D — deep research, 2026-10-12 (window: bmo 2026-10-13)

**This is stage D: three names drawn at random (seed 13025361929859, pool of 9 confirmed names), one deep Opus 5.5 researcher each, no orders placed.** Names: ACI, DPZ, JNJ. Three names on one day are an anecdote.

Fired 17:36 UTC (13:36 ET); scored 18:13 UTC (14:13 ET), before the close. Researchers ran as `deep-question-researcher` (us-deep.v2, pinned claude-opus-5-5). Orchestrator model: claude-sonnet-5-5.

| ticker | impact_sum (key) | scaled | abs_move | p_up | quick first read (impact / p_up) | decision |
| --- | --- | --- | --- | --- | --- | --- |
| DPZ | -0.30 | -0.26 | 6.5 | 48 | -1.2 / 45 | no_trade, low |
| JNJ | -0.45 | -0.17 | 2.9 | 47 | +0.7 / 54 | no_trade, low |
| ACI | -1.00 | -0.48 | 8.0 | 47 | -1.0 / 45 | no_trade, low |

None clears the 2.8 conviction floor. Depth moved the number toward zero on DPZ and left ACI unchanged and flipped JNJ's sign (+0.7 to -0.45).

## ACI (Albertsons) — bmo 10-13
Key questions (answer / confidence / impact): Q1 guide held vs cut — more likely held than cut but a "low end" steer likelier than consensus ($1.79, flat 60 days) holds; diesel $6.20 vs $5.13-5.31 at guide-setting; Kroger held its guide through the spike (62%, -0.8). Q2 identical sales — probably -1.3 to -1.8% vs RBC -1% (Census grocery sales +0.5% Aug) (58%, -0.4). Q3 Q2 EPS ~$0.33 in line, fuel margins a small offset (55%, +0.2). Q4 strategic/leadership action — none seen (75%, 0).
Premortem: guide held, 18%-of-float short covers (Kroger template, +7%). Decision: **no_trade, low** — edge too small against a crowded short (59.5M shares, 18.15% of float, +9% m/m); would change on the FY26 outlook table. Out of window: Kroger trial 10-19.

## DPZ (Domino's) — bmo 10-13
Q1 US comp vs 1.1% bar — central +0.6%, but Kalshi already holds ~0.3% (60%, -0.3). Q2 guide "low single digits" held vs trimmed under new CEO — coin flip (50%, -0.1). Q3 international comps +0.5-1.5% (55%, +0.2). Q4 DPC Dash mark-to-market ~-$0.06 EPS (50%, -0.1).
Premortem: comp at/above 1% on 50%-off week, guide held, de-rated stock re-rates 6-10%. Decision: **no_trade, low**; would change on a Q4-to-date comp (>~2% long, flat/guide trim short).

## JNJ — bmo 10-13
Q1 sales ~$25.5bn vs $25.38bn mean, ~0.4% beat vs 1-4% habit (65%, -0.1). Q2 FY guide: euro 1.116 vs 1.15 assumed, street already at top of guide (55%, -0.2). Q3 EPS two-way around $2.53 on Sail IPR&D timing (50%, -0.05). Q4 DePuy deal on the day — unlikely (75%, 0). Q5 MedTech ~3-4% (55%, -0.1).
Premortem: Innovative Medicine beats far more than rebuilt; raise above ~$101.5bn. Decision: **no_trade, low**; would change on sales >=$25.8bn with raise (long) or reported guide cut (short).

## Comparison with stage E and E-P (files existed at note time; read only now)

| ticker | stage D impact_sum | stage E impact_sum | E-P panel_score | E-P selected |
| --- | --- | --- | --- | --- |
| ACI | -1.00 | -0.5 | +0.56 | no |
| DPZ | -0.30 | -2.1 | -1.06 | no |
| JNJ | -0.45 | -0.3 | -0.22 | no |

Signs disagree on ACI only: stage D and E negative, E-P panel positive (+0.56, not selected). DPZ and JNJ agree in sign across all three. No name selected by E-P.

## What these numbers are not
No hit rate exists until the names resolve (after the 10-13 bmo prints); the pooled comparison (`deep_compare.py`) needs weeks. Nothing checked findings beyond the researchers' own sourcing. Sign below the floor is a coin flip on the evidence so far. `impact_sum` ranks, it does not size. This is research, not investment advice.

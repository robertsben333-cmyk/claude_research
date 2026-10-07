# Stage D (deep) — 2026-10-07

**This is stage D: three names drawn at random (seed 110544768784710), one deep Opus 5.5 researcher each, no orders.** Names: LEVI (amc 10-07), PEP (bmo 10-08), TLRY (bmo 10-08). Three names on one day are an anecdote and cannot be ranked. Fired 17:36 UTC (13:36 ET); scored 18:18 UTC (14:18 ET), before the close. The pool was 9 confirmed names; RGP was not confirmed by a company source and was not in the pool's hunted set.

| ticker | impact_sum (key) | scaled | abs_move | p_up | quick first read (sum / abs / p_up) | decision |
| --- | --- | --- | --- | --- | --- | --- |
| LEVI | +0.75 | +0.80 | 10.0 | 54 | +1.6 / 9.5 / 55 | long, low |
| PEP | -0.35 | -0.27 | 4.5 | 47 | -0.8 / 4.5 / 48 | short, low |
| TLRY | -0.10 | -0.38 | 9.5 | 48 | 0.0 / 9.0 / 52 | no trade, low |

All three are far below the 2.8 conviction floor: below it the sign is a coin flip on the evidence so far. Depth moved the numbers by under one point of spot on each name.

## LEVI — long, low conviction
Frozen questions (priced answer → our answer, confidence, impact):
| Q | question | priced | ours | conf | impact |
| --- | --- | --- | --- | --- | --- |
| Q1 | FY26 adj EPS guide ex-refund at/above $1.54 consensus? | street holds a raise ($1.539) | probably not quite; midpoint ~$1.525 | 58 | -0.3 |
| Q2 | Q3 revenue beat $1.617bn? | upper half of 4-5% guide | yes, ~$1.63bn | 62 | +0.3 |
| Q3 | Q3 adj EPS beat $0.358 by ≥2c? | top of $0.34-0.36 guide | likely, $0.37-0.39 | 55 | +0.15 |
| Q4 | Material IEEPA tariff refund recognised? | not in estimates | probably yes, treatment uncertain | 60 | +0.3 |

Premortem: the FY guide at or below a pass-through (midpoint ≤ $1.51) with a trimmed implied Q4 repeats October 2025 (-12.55%). Decision: long, low. What would change it: new FY26 EPS midpoint ex-refund at or below ~$1.51.

## PEP — short, low conviction
| Q | question | priced | ours | conf | impact |
| --- | --- | --- | --- | --- | --- |
| Q1 | FY26 core cc EPS guide 4-6% kept, or cut below 4%? | low end held, no cut in estimates | held ~57%, formal cut ~38% | 57 | -0.4 |
| Q2 | Q3 organic ≥3%, PFNA ≥ flat? | ~$25.0B revenue, PFNA ~-1% | roughly in line, PFNA volume optics slightly better | 55 | +0.1 |
| Q3 | Q3 core EPS ≥ ~$2.30? | $2.28-2.30 | $2.30-2.33 | 65 | +0.05 |
| Q4 | 2027 headwind flagged? | unsourced | cautious cost language likely | 50 | -0.1 |

Premortem: a held guide at the low end plus PFNA volume growth gives a relief rally from a 5-year low with calls bid (July 2025: +7.45%). Decision: short, low. What would change it: a reaffirmed guide with Q4 energy and transport costs stated as hedged or offset.

## TLRY — no trade, low conviction
| Q | question | priced | ours | conf | impact |
| --- | --- | --- | --- | --- | --- |
| Q1 | Q1 revenue above $265-268m? | ~$265-268m | ~$270m | 60 | +0.2 |
| Q2 | FY27 adj EBITDA guide $68-75m reaffirmed? | reaffirm | reaffirm, maybe fuel-qualified; cut ~5% | 65 | -0.5 |
| Q3 | Cannabis revenue up y/y, GM ≥40%? | modest growth | ~$68-73m, GM ~40% | 60 | +0.2 |
| Q4 | GAAP loss near -$0.18? | -$0.18 | no differentiated view | 50 | 0.0 |
| Q5 | Dilution beyond the ~8.1m shares known? | no expectation | yes, ~6.0m unexplained (likely ATM) | 65 | -0.3 |

Premortem: a clean reaffirmation with Q1 adj EBITDA ≥ ~$15m meets 13-14% short interest and squeezes up. Decision: no trade. What would change it: a cut or qualified guide (short), or a clean reaffirm with strong EBITDA (long).

## Comparison with stage E and E-P (both files existed at 18:20 UTC; read only after scoring)
| ticker | D impact_sum | E impact_sum | E-P panel_score | E-P selected |
| --- | --- | --- | --- | --- |
| LEVI | +0.75 | +2.1 | +0.98 | no |
| PEP | -0.35 | +0.2 | +0.23 | no |
| TLRY | -0.10 | +0.3 | -0.01 | no |

Sign disagreements: PEP — D negative on a guide-trim tail from oil, E and E-P small positive. TLRY — D marginally negative (fuel and dilution), E slightly positive, E-P ~zero. LEVI: all three agree on positive; D is the smallest.

## What these numbers are not
No hit rate exists until the names resolve. The pooled comparison (`deep_compare.py`) needs weeks of days. Nothing here is a forecast of the move; `impact_sum` ranks and does not size. Nothing checked the findings beyond each researcher's own work.

**Process flags.** The three researchers shared one scratchpad directory. The PEP researcher reported its frozen questions were overwritten by the LEVI researcher's file at 17:52 UTC and restored from its own 17:45 freeze. It could not rule out that LEVI read PEP's files; the independence of the three freezes is therefore not fully clean. TLRY's craft-beer figures are snippet-only (HTTP 429). Sweep: RGP date unconfirmed by a company source.

This is research, not investment advice. Past reactions do not predict future ones.

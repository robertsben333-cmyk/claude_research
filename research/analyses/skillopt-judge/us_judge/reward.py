"""The per-name reward SkillOpt optimises, and the words the analyst sees.

r = (impact_sum / E) x (move / E), E = what the baseline priced (option-implied move,
else the median past reaction, else 5), floored at 1.

Why this and not a hit rate: the panel ranks names on |impact_sum| and trades the sign,
so what earns is a large number with the right sign on a name that moves more than was
priced. r is that, per name. It is scale-free in the move, it rewards size only when the
sign is right, and it charges size when the sign is wrong, so inflating every number
pays only if the judge is right more often than wrong. A no-view name scores 0.

soft = 0.5 + 0.5 tanh(r), in (0, 1); the gate compares mean soft.
hard (only used to split the analyst's batch into failures and successes):
  a view: 1 when its sign matches the move, else 0;
  no view: 1 when the move stayed inside what was priced, else 0 (a missed big move).
"""
from __future__ import annotations

import math


def sgn(x: float) -> int:
    return (x > 0) - (x < 0)


def score(impact: float | None, outcome: dict) -> dict:
    m, E = float(outcome['move_pct']), float(outcome['priced_move_pct'])
    s = float(impact or 0.0)
    r = (s / E) * (m / E)
    soft = 0.5 + 0.5 * math.tanh(r)
    if s:
        hard = int(sgn(s) == sgn(m))
        why = '' if hard else (f'Wrong sign: impact_sum {s:+.2f}, the stock moved {m:+.1f}% '
                               f'against {E:.1f}% priced.')
    else:
        hard = int(abs(m) <= E)
        why = '' if hard else (f'No view (impact_sum 0), but the stock moved {m:+.1f}% '
                               f'against {E:.1f}% priced.')
    return {'r': r, 'soft': soft, 'hard': hard, 'fail_reason': why}


def hidden_reference(impact: float | None, judged: dict | None, outcome: dict, sc: dict) -> str:
    j = judged or {}
    return (
        f"Realised move over the scored window (strategy exit): {outcome['move_pct']:+.2f}%.\n"
        f"Move the baseline priced: {outcome['priced_move_pct']:.2f}% ({outcome['priced_basis']}).\n"
        f"Judge said: impact_sum {float(impact or 0):+.2f}, abs_move_pct {j.get('abs_move_pct')}, "
        f"p_up {j.get('p_up')}.\n"
        f"Reward r = (impact/priced) x (move/priced) = {sc['r']:+.3f}.\n"
        "This is ONE draw of a noisy outcome: US earnings moves have a standard deviation near "
        "10 points, and about half of all signs are coin flips. Judge the reasoning, not the luck."
    )

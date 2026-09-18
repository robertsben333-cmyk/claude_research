# archive — retired experiments

Nothing in here runs. Nothing outside here reads it. It is kept because the
measurements are the reason the live pipeline is shaped the way it is, and a
result that cost forty days of runs is worth more than the disk it sits on.

Three things were retired on 2026-09-18, all for the same reason: measured
against what they cost, none of them beat a number that was already free.

## `pipeline/` — stages 1 to 4 of the daily advice pipeline

Triage, the deep-dive dossiers, the seven-persona panel, the advice note and the
calibration ledger. Stage 0 (the day's earnings universe) stays live under
`research/`, because stage E still reads it.

Scored over everything the stages ever produced, 2026-08-08 to 2026-09-18:

| Stage | Output | Result |
| --- | --- | --- |
| 2, deep dives | 75 dossiers, 20 days | direction 39/75 (52%), +0.69%/trade (t=0.49) against +1.24% for shorting the same names blind; within-day rank correlation −0.119; the ten highest-conviction reads went 4/10 and −4.99% |
| 3, the panel | 22 names, 154 persona verdicts, 14 days | 21 calls of Neutral and one Lean Down (wrong). The signed consensus it never acted on was right 6 of 22 (27%, p=0.026), rank correlation −0.102 |
| 4, the ledger | 9 outcome files, 15 scored calls | its headline `direction_hit` was implemented as "the option-implied move was not broken", so the reported 60% hit rate and 40% break rate are one statistic printed twice, and neither measures the panel |

Three findings are worth carrying forward rather than re-learning:

* **The panel could not make a call by construction.** `synthesize.py` calls
  anything inside ±25 Neutral, and averaging seven personas shrank the typical
  absolute score from 15.2 to 9.4. The largest consensus in 22 panels was 25.7.
* **Averaging correlated agents stacks their error, it does not cancel it.** The
  seven personas averaged 42% on direction; their consensus scored 27%, tied with
  the worst single member. Nineteen of 22 consensus scores were bearish while 15
  of the 22 names rose.
* **The panel's magnitude estimate was the option-implied move.** Correlation
  0.927 with it, median gap 0.65pp, and on level it lost to the free historical
  median (5.98pp against 4.92pp).

## `backtest/` — the sealed pilot-40 backtest and the edge corpus

`RESULTS.md` (three arms over 37 sealed events) and `runs/edge-corpus/` (stage E
re-run over 104 resolved events). The corpus run is the single most discouraging
number in the repo: ρ=+0.073, p=0.45. Read `FINDINGS.md` §33 for its caveats
before citing it either way.

## `claude_naive/` — stage N, the naive forecast run live

Arm A of the backtest, promoted to production and then disabled from outside this
repo on 2026-09-09. Its own `LEDGER.md` records why it deserved to stop: the
backtest's 72% direction came in at 60% live, and +27.0pp of its cumulative return
came from one day. Strip that day and eleven directional calls are 5/11 at −2.47%.

## If you are reverting this

Fine, but do it deliberately and say so in a run log. The evidence above is not a
mood; it is 75 dossiers, 22 panels, 154 persona verdicts and 141 sealed backtest
events. Bring a hypothesis that one of them would have caught.

## What still runs

Stage 0 (`earnings-universe`) and stage E (`earnings-edge-hunt`), plus the
performance dashboard. Stage E has its own measurement problem, written up in
`edge/EDGE_ANALYSIS.md`; it is not archived here because it is still placing money
and still being measured forward.

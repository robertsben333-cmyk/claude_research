# claude_naive — forecast ledger

Arm A of the pilot-40 backtest, run live. Every rate carries its floor.

Scheme: buy 14:00 ET (20:00 CET) the last session before the print, exit next open (primary) or next close. Long on Up, short on Down, flat on Neutral.

Backtest reference points, over 37 events: direction 72%, +0.90%/trade at the open, +2.16% at the close, magnitude median error 3.35pp against a 3.64pp proxy. Those had 18 directional calls behind them and were called a lead, not a finding.

## Pooled — 5 scored days (2026-08-31 … 2026-09-04)

31 events resolved of 39 forecast (2026-09-08's eight need the 2026-09-09 close; 2026-09-07 was skipped, no universe).

| | live, n=31 events / 15 directional | backtest, n=37 / 18 | floor |
| --- | --- | --- | --- |
| direction | 60% (9/15) | 72% | 62% (repeat last reaction) |
| return/trade, exit open | +1.80% | +0.90% | +0.25% (always_down) |
| return/trade, exit close | +0.88% | +2.16% | — |
| magnitude median abs error, raw | 4.63pp | 3.35pp | 3.64pp (base-rate proxy) |
| magnitude median abs error, scaled | 8.46pp | — | 3.64pp |

Read the return with care: +27.0pp of cumulative open-exit return comes from a single day.
2026-09-03 went 4/4 with large moves (LULU −17.4%, PATH −16.6%) and contributed +54.2pp on
its own. Strip that day and the remaining eleven directional calls are 5/11 with **−2.47%**
per trade. One day carries the entire result.

Magnitude, the part the backtest called answerable, has not transferred: median raw error
4.63pp against the 3.64pp proxy floor, and rank correlation between forecast and realised
absolute move is 0.120 — against 0.29-0.33 in the backtest. The scaled (correction) number
is worse than raw on every single day, 8.46pp pooled. The x2 large-move correction looks
like an artefact of the 37-event sample, exactly as `README.md` said it might be.

## 2026-08-31

- events forecast: 5, scored: 5, directional: 3, neutral: 2
- realised: 2/5 up, median |move| 4.02%
- **direction 3/3 (100%)** — floor: the free last-reaction rule scored 62% over the backtest's 37
- **return per trade, exit open: -1.47%** (total -4.4%) — always_down on the same events: -0.10%
- return per trade, exit close: +3.59% (total +10.8%)
- magnitude median error: **raw 2.66pp vs scaled 10.38pp** — the backtest's proxy floor was 3.64pp
  - the raw number is closer on this batch; the correction is not helping here

| ticker | call | pred | scaled | actual | dir | open | close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RZLV | Neutral | 16.0 | 32.0 | -17.30 | - |  |  |
| MMED | Neutral | 8.0 | 12.8 | +10.66 | - |  |  |
| NIO | Lean Down | 9.0 | 14.4 | -4.02 | hit | +5.64 | +6.22 |
| YEXT | Lean Down | 12.0 | 24.0 | -3.55 | hit | -13.40 | +3.33 |
| MDT | Lean Up | 4.0 | 4.0 | +1.53 | hit | +3.35 | +1.22 |

## 2026-09-01

- events forecast: 8, scored: 8, directional: 3, neutral: 5
- realised: 4/8 up, median |move| 9.63%
- **direction 1/3 (33%)** — floor: the free last-reaction rule scored 62% over the backtest's 37
- **return per trade, exit open: -9.43%** (total -28.3%) — always_down on the same events: -0.52%
- return per trade, exit close: -7.30% (total -21.9%)
- magnitude median error: **raw 2.16pp vs scaled 5.39pp** — the backtest's proxy floor was 3.64pp
  - the raw number is closer on this batch; the correction is not helping here

| ticker | call | pred | scaled | actual | dir | open | close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CRDO | Lean Up | 12.0 | 24.0 | -20.04 | miss | -10.44 | -21.46 |
| DELL | Neutral | 8.5 | 13.6 | +15.81 | - |  |  |
| MDB | Neutral | 11.0 | 22.0 | -13.54 | - |  |  |
| GTLB | Lean Down | 10.5 | 21.0 | +9.98 | miss | -21.93 | -9.45 |
| PANW | Lean Down | 7.5 | 12.0 | -9.28 | hit | +4.09 | +9.00 |
| CXM | Neutral | 9.0 | 14.4 | -8.55 | - |  |  |
| BF-B | Neutral | 5.5 | 8.8 | +3.87 | - |  |  |
| OLLI | Neutral | 7.0 | 11.2 | +2.12 | - |  |  |

## 2026-09-02

- events forecast: 8, scored: 8, directional: 4, neutral: 4
- realised: 3/8 up, median |move| 5.94%
- **direction 1/4 (25%)** — floor: the free last-reaction rule scored 62% over the backtest's 37
- **return per trade, exit open: +0.79%** (total +3.2%) — always_down on the same events: +0.17%
- return per trade, exit close: -2.86% (total -11.4%)
- magnitude median error: **raw 3.40pp vs scaled 8.05pp** — the backtest's proxy floor was 3.64pp
  - the raw number is closer on this batch; the correction is not helping here

| ticker | call | pred | scaled | actual | dir | open | close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SNOW | Neutral | 12.0 | 24.0 | +16.55 | - |  |  |
| CIEN | Lean Up | 11.0 | 22.0 | -10.36 | miss | +0.54 | -10.02 |
| CPB | Neutral | 6.0 | 9.6 | -6.94 | - |  |  |
| TTC | Neutral | 4.5 | 4.5 | -6.84 | - |  |  |
| HPE | Neutral | 5.5 | 8.8 | +5.04 | - |  |  |
| AVGO | Lean Up | 8.5 | 13.6 | -2.74 | miss | -4.69 | -3.16 |
| NTAP | Lean Down | 7.0 | 11.2 | +2.55 | miss | +12.16 | -0.43 |
| FIVE | Lean Down | 9.0 | 14.4 | -1.28 | hit | -4.83 | +2.19 |

## 2026-09-03

- events forecast: 8, scored: 8, directional: 4, neutral: 4
- realised: 2/8 up, median |move| 4.12%
- **direction 4/4 (100%)** — floor: the free last-reaction rule scored 62% over the backtest's 37
- **return per trade, exit open: +13.54%** (total +54.2%) — always_down on the same events: +3.92%
- return per trade, exit close: +10.91% (total +43.7%)
- magnitude median error: **raw 8.07pp vs scaled 15.10pp** — the backtest's proxy floor was 3.64pp
  - the raw number is closer on this batch; the correction is not helping here

| ticker | call | pred | scaled | actual | dir | open | close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GWRE | Neutral | 11.0 | 22.0 | -19.93 | - |  |  |
| LULU | Lean Down | 9.5 | 15.2 | -17.38 | hit | +17.81 | +15.79 |
| PATH | Lean Down | 12.0 | 24.0 | -16.63 | hit | +12.07 | +17.67 |
| ZS | Lean Down | 12.0 | 24.0 | -4.50 | hit | +7.40 | +5.56 |
| IOT | Lean Up | 12.0 | 24.0 | +3.74 | hit | +16.90 | +4.63 |
| DOCU | Neutral | 9.0 | 14.4 | +3.70 | - |  |  |
| PL | Neutral | 22.0 | 44.0 | -1.25 | - |  |  |
| AMBA | Neutral | 15.0 | 30.0 | -0.77 | - |  |  |

## 2026-09-04

- events forecast: 2, scored: 2, directional: 1, neutral: 1
- realised: 2/2 up, median |move| 4.92%
- **direction 0/1 (0%)** — floor: the free last-reaction rule scored 62% over the backtest's 37
- **return per trade, exit open: +2.32%** (total +2.3%) — always_down on the same events: -0.40%
- return per trade, exit close: -7.89% (total -7.9%)
- magnitude median error: **raw 5.38pp vs scaled 12.29pp** — the backtest's proxy floor was 3.64pp
  - the raw number is closer on this batch; the correction is not helping here

| ticker | call | pred | scaled | actual | dir | open | close |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ABM | Lean Down | 6.5 | 10.4 | +7.55 | miss | +2.32 | -7.89 |
| UNFI | Neutral | 12.0 | 24.0 | +2.28 | - |  |  |

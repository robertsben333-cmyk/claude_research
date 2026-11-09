# Pre-registration: can 1-minute price and volume tell when an earnings move is priced in?

Written 2026-11-09 15:30 UTC, before any price for this study was fetched. Thread "Detect when earnings move is priced in" (Xavier). Nothing below changes after outcomes are computed; anything added later is labelled exploratory.

## What is new compared with earlier work

Earlier studies in this project asked whether a feature measured at ONE fixed moment (the first minute, 09:30, 10:30) predicts the rest of the day. All failed or faded out of sample (first-minute-exit, first-hour-bmo, exit-model). None used the full path from the release onward (after-hours for amc, pre-market, regular session) and none tried to detect a STATE, "the reaction has stopped". This study does both:

1. Data: Alpaca SIP 1-minute bars with volume from the release window onward: amc from 16:00 ET on the event day through 16:00 on the reaction day; bmo from 04:00 to 16:00 on the reaction day. Plus 15-minute bars 04:00-20:00 over the 20 prior sessions, to know each name's normal volume at each clock time.
2. A settlement detector: abnormal volume (volume relative to the name's normal at that clock time) that has decayed relative to its own peak since the release.
3. A direction signal for the part not yet priced: recent trend and price against the release-window VWAP, both in the move's direction.

## Definitions (decided now)

- Release start R: amc 16:00 ET event day; bmo 04:00 ET reaction day. Reference price P0: prior regular close (amc: event-day close; bmo: prior session close).
- Checkpoints t: amc 16:30, 17:30, 19:00 (event day), 07:00, 08:30, 09:25, 09:35, 09:45, 10:00, 10:30, 11:00, 12:00 (reaction day). bmo: 07:00, 08:30, 09:25, 09:35, 09:45, 10:00, 10:30, 11:00, 12:00. Price at t = close of the last 1-min bar before t (at most 30 min stale in extended hours, else missing).
- Move so far M_t = (P_t / P0 − 1) × 100; direction d = sign(M_t). An observation counts only if |M_t| ≥ 2% (known at t).
- Forward return F_t = d × (P_{t+} − P_t) / P0 × 100, two horizons: to the next checkpoint (F1) and to 13:00 on the reaction day (F13, primary; only for t ≤ 12:00).
- Features at t, all in the move's direction:
  - TR: d × return over the last 30 min (60 min before 09:30), divided by the 1-min realised volatility since R × √(window minutes).
  - VW: d × (P_t − VWAP since R) / P0 × 100.
  - AV: volume in the 15 min to t divided by the name's average volume in the same 15-min clock slot over the prior 20 sessions (floor 100 shares).
  - DEC: AV(t) / max AV over all 15-min windows since R (1 = still at peak, near 0 = decayed).
- Settled(t) = DEC < 0.30. Direction signal D_t = z(TR) + z(VW), z-scores from the development half, winsorised at ±3.

## Hypotheses

- **H1 (unpriced part is predictable while active):** among unsettled observations, ρ(D_t, F13) ≠ 0. Theory is two-sided (informed flow still arriving → continuation; liquidity overshoot → reversal), so the sign is reported, not assumed.
- **H2 (settled = priced in):** among settled observations, |ρ(D_t, F13)| < 0.05 and mean F13 not different from 0 (|t| < 2). Supported only if H1 holds and |ρ_unsettled| − |ρ_settled| has a day-bootstrap 95% interval above 0.
- **H3 (useful as an exit):** dynamic exit. From the first decision point (amc: 09:25 using after-hours and pre-market data, exit at the open if the rule says exit; bmo: 10:00), at each later checkpoint and then every 30 min to 15:30: exit if settled, or if D_t points against the position (sign of d × D_t × side < 0, using H1's development-half sign of ρ; if dev ρ ≤ 0 the rule follows reversal). Otherwise hold; at 15:55 exit regardless. Compared with the static exit (amc open, bmo 13:00).
  - Market-wide: both a long and a short per event, averaged, so the rule earns only by predicting direction.
  - Our calls: stage E-P us-panel.v2 and us-panel.v3 separately (never pooled), all calls and strong calls (panel ≥ 80, four judges); the Aug-Sep backtest names separately.

## Samples

- Development: reaction days 31 Aug to 20 Oct 2026. z-scores and the H3 sign come from here only. Results here are descriptive.
- **Holdout: reaction days 21 Oct to 6 Nov 2026. All verdicts are read here.** Earlier studies in this project used part of this period for other features; these features have not been computed on it.

## Verdict rules

- H1 passes: holdout |ρ| ≥ 0.05 with within-day permutation p < 0.05, same sign as development.
- H2 as stated above.
- H3 passes: holdout market-wide gain per day with t ≥ 2. On our calls, reported with n, t and p; with n below about 100 per version it is too small to tell and will be called that.

## Exploratory (labelled as such)

Settle threshold 0.2 and 0.5; F1 instead of F13; amc and bmo apart; the share of the close-to-close move already present at each checkpoint (how long "priced in" takes), as a descriptive curve.

## Amendment 1 (2026-11-09 16:05 UTC, before any outcome was analysed)

A plumbing check on one event (MDT) showed that abnormal volume in extended hours is hundreds of times normal, so DEC relative to the peak since the release reads ~0.01 for every regular-session checkpoint and would call everything "settled" at the open. That makes H2 and H3 degenerate by construction. Change: DEC's peak is taken within the regime of the checkpoint, i.e. since R for checkpoints before 09:30 and since 09:30 for checkpoints from 09:35. Nothing else changes. No outcome statistic had been computed.

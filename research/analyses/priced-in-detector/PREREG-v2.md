# Pre-registration v2: spreads and order flow at our decision moments

Written 2026-11-09 17:15 UTC, after version 1 failed (see report.md) and before any quote or trade for this version was fetched. Xavier asked to try the different approach and include more recent data.

## What changes from version 1, and why

1. **Two questions, kept apart.** (a) Size: does the tape tell how much the price will STILL move? (b) Direction: does it tell which way? A priced-in move is one where (a) is small. (b) is what an exit needs.
2. **Markers from the quotes and trades, not bars** (Alpaca SIP quotes and trades):
   - abnormal spread: time-weighted relative bid-ask spread in the 5 minutes before the decision, divided by the same 5 minutes five sessions earlier (spreads widen while market makers fear informed traders and narrow once the news is absorbed);
   - spread decay: that spread divided by the spread in an earlier window on the same day;
   - order imbalance OI: (buyer-initiated − seller-initiated volume) / volume, trades signed by the prevailing quote (at or above the ask = buy, at or below the bid = sell, else above/below the midpoint), in the move's direction;
   - retail imbalance RI (Boehmer, Jones, Zhang and Zhang 2021): off-exchange trades (exchange D) with a sub-penny price, fraction 0.6-1.0 cents = retail buy, 0.0-0.4 = retail sell; (buy − sell)/(buy + sell), in the move's direction.
3. **One row per event per decision moment**, not twelve checkpoints:
   - amc at 09:25 (sell at the open vs hold to 13:00);
   - bmo at 09:25 (sell at the open vs hold to 13:00, the current exit);
   - bmo at 12:55 (sell at 13:00 vs hold to the close).
4. **Moves measured in units of the name's own volatility** (20-day daily volatility from 15-minute closes), and results split by liquidity (above/below the median 20-day dollar volume of the sample) as an exploratory cut.

Windows: decision 09:20-09:25 (decay reference 08:00-08:05) and 12:50-12:55 (reference 09:50-09:55); normal-day windows at the same clock time five sessions before the reaction day.

## Outcomes

d = sign of the move from the prior close to the decision price. σ = 20-day daily volatility in %.
- 09:25 rows: F = d × (P13:00 − Popen) / P0 × 100. 12:55 rows: F = d × (Pclose − P13:00) / P0 × 100.
- Size outcome: |F| / σ. Direction outcome: F.

## Hypotheses and verdict rules (read on the holdout only)

- **HA (size):** abnormal spread predicts |F|/σ, positive. Passes if ρ ≥ 0.10 with within-day permutation p < 0.05, in each of the three decision sets or pooled across them (pooled reported as primary).
- **HB (direction):** OI predicts F; RI predicts F. Theory is split (order-flow continuation vs attention-driven reversal), so the sign is taken from development and must repeat. Passes if |ρ| ≥ 0.07, p < 0.05, same sign as development.
- **HC (exit), only meaningful if HB passes:** for each position, hold past the current exit if the signal that passed HB, oriented by its development sign, favours our side; otherwise take the current exit. amc at 09:25: current exit = open, alternative = 13:00. bmo at 09:25: current exit = 13:00, alternative = sell at the open if the signal is against us. bmo at 12:55: current = 13:00, alternative = close if the signal is with us. Market-wide (long and short averaged per event), per-day t ≥ 2 to pass; our calls per version (us-panel.v2, v3 apart), reported with n, t, p.

## Samples

- Market-wide: events with |move at the decision| ≥ 2%.
- Development: reaction days 31 Aug to 20 Oct. **Holdout: 21 Oct to the latest complete day, including 9 Nov if its close is in.**
- All earlier exploratory work in this thread used bar data only; no quote or trade feature has been computed on any period.

# Pre-registration v3: target (B), options (C), and a combined model

Written 2026-11-09 18:35 UTC, before any options data or target ratio was computed. Xavier: "let's try b and c, and see if we can combine ideas".

## B: priced in = the price has reached a target

- **B1 (our calls, new):** progress = move so far at the decision / the panel's own `expected_move_pct` (both signed; progress > 1 means the price has already gone further than the panel expected). Theory says a target not yet reached gives continuation toward it, so the sign is **negative**: the higher the progress, the less is left on our side. Outcome: our-side return from the decision to the alternative exit.
- **B2 (stage M, re-measured):** gap = side × (release_read_move_pct − pre-market move). The earlier exit-model study already found this contrarian (ρ −0.33, n 76, mornings to 6 Nov), so the sign is fixed at **negative** from that study. Only mornings after 6 Nov are new, which is today alone, so this is reported, not judged.
- **B3 (market-wide):** |move so far| / sealed option-implied move. Follow-up 4 found overshoot then fade; it vanished on the 28 Oct–6 Nov re-check. Sign **negative** (more beyond the implied move, more reversal), reported on the holdout.

## C: what the options market says after the release

Alpaca option trade bars (15-minute), nearest expiry after the reaction day, strikes within ±15% of spot. Options trade only from 09:30, so C uses decision moments **09:45** (amc and bmo: exit at 09:45 vs hold to 13:00) and **12:55** (bmo: exit at 13:00 vs hold to the close).
- **Remaining implied move:** ATM straddle at the decision (last trades of the ATM call and put in the 15 min before) divided by the same straddle at the prior close (15:00-16:00 bars). Low = the crush is complete.
- **C1 (size):** the remaining straddle as % of spot predicts the remaining |move| / σ, sign **positive**. Passes: holdout ρ ≥ 0.10, p < 0.05, and the partial ρ after the move so far stays ≥ 0.05.
- **C2 (direction):** (call volume − put volume) / (call + put volume) in the 15 min before the decision, in the move's direction. Sign from development; passes at |ρ| ≥ 0.07, p < 0.05, same sign in the holdout.

## Combined model

- **Direction score** = z(C2) × sign_dev + z(order imbalance from v2) × sign_dev + z(B3) × (−1), with missing parts at 0 and z-scores from development. Applied at 09:45 and 12:55 for options rows (for 09:45 the order imbalance comes from 09:20-09:25, the latest v2 window). **Passes** if holdout ρ ≥ 0.07, p < 0.05. Exit rule as in v2 HC (hold to the alternative exit only when the score favours our side) is judged market-wide with per-day t ≥ 2; our calls per version.
- **Size score** = z(spread decay) + z(remaining straddle) + z(move so far / σ). Reported with ρ against remaining |move| / σ; no trading verdict, because size alone cannot change the expected return of an exit.

Development 31 Aug to 20 Oct, holdout 21 Oct to the latest complete day. Prompt versions never pooled.

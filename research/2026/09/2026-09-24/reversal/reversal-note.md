# Stage R — reversal note — drop date 2026-09-24, window to close 2026-09-25

Screened intraday at 2026-09-24 15:04 EDT (bars not final). SPY on the day at the screen: −0.09%. Names above the floors: 80. Hunted: 15 of 15. Rankable: 15. Above the conviction floor (|impact_sum| ≥ 3.0): **1, JAGX at −3.50**. **Health Care is 8 of the 15 names (53%)**, so treat today's ranking as one bet, not fifteen.

## Answer first

- **The only name above the floor is JAGX at −3.50, a continuation call. The one mechanism behind it is supply.** Jaguar Health refreshed its Ladenburg ATM at 09:22 ET today to $9.82m of room, about 115% of its market cap at the screen. It sold about $4.69m through the same programme between 09-03 and 09-23. Before the open it also disclosed 547,898 3(a)(9) exchange shares (about 43% of the share count) issued to Streeterville on 09-23. Those shares are freely tradable because they tack the note's holding period.
- **Every non-zero number is negative, and every one of them is leg 2, supply.** The hunters found ATMs (JAGX, TVRD, VEEA, SLDB, BW), resale shelves or registered holders (OBX, NCT, AMTX), and the last day of a VWAP exchange-pricing period (BYND). **Leg 1 is empty for the second day running**: no `repricing` finding at all, so no overshoot is promoted and none carries a `mechanism_in_window`.
- **Six names hunted to zero**: BLSM, EOSE, KPLT, MEDS, RCKT and ZBIO. Nothing that could be sourced lands inside the window. A zero is an answer, not a missing hunt.
- **No reversal run has beaten a free control yet.** The 2026-09-22 run resolved today on only 5 of its 15 names: `impact_sum` ρ −0.30 (p 0.69), `neg_atr14` −0.60, `neg_ret_d` +0.10. The hunt does not beat the free controls, and **a run that does not beat the free controls has established nothing**. The 2026-09-23 run is still pending, because its window closes at today's close.

## Ranked table

Legs are the hunters' own finding sums by `leg`. Lean = `priced_lean_pct`. Band prior = phase-0 cross-section expectation for the name's drop band and turnover band. Half-spread is Corwin-Schultz, a floor; **0.00 means UNKNOWN**, never narrow.

| # | ticker | fall % | impact_sum | leg1 repricing | leg2 new info | overshoot_pct | more_to_come_pct | lean | −ret_d | −ATR14 | vol× | turnover $m | half-spread % | band prior % | cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BLSM | -6.9 | +0.00 | +0.00 | +0.00 | 0.0 | 0.0 | -1.71 | 6.9 | -11.1 | 1.24 | 3.4 | +0.00 | -1.77 | no_identifiable_cause |
| 2 | EOSE | -11.2 | +0.00 | +0.00 | +0.00 | 0.0 | 0.0 | -0.78 | 11.2 | -10.8 | 1.82 | 93.7 | +0.31 | +0.20 | no_identifiable_cause |
| 3 | KPLT | -15.1 | +0.00 | +0.00 | +0.00 | 0.0 | 0.0 | -1.06 | 15.1 | -15.8 | 2.37 | 1.3 | +1.37 | -0.39 | no_identifiable_cause |
| 4 | MEDS | -5.2 | +0.00 | +0.00 | +0.00 | 0.0 | 0.0 | -1.72 | 5.2 | -44.9 | 0.85 | 0.3 | +1.44 | -1.04 | no_identifiable_cause |
| 5 | RCKT | -8.3 | +0.00 | +0.00 | +0.00 | 0.0 | 0.0 | +0.41 | 8.3 | -8.6 | 2.21 | 4.5 | +0.58 | -0.23 | no_identifiable_cause |
| 6 | ZBIO | -8.1 | +0.00 | +0.00 | +0.00 | 0.0 | 0.0 | +0.56 | 8.1 | -6.7 | 1.21 | 17.0 | +0.84 | -0.20 | no_identifiable_cause |
| 7 | AMTX | -6.8 | -0.30 | +0.00 | -0.30 | 0.0 | -0.3 | -0.98 | 6.8 | -8.2 | 1.08 | 1.2 | +0.93 | -1.77 | no_identifiable_cause |
| 8 | BW | -8.0 | -0.30 | +0.00 | -0.30 | 0.0 | -0.3 | +0.93 | 8.0 | -9.2 | 1.28 | 28.7 | +0.00 | +0.30 | no_identifiable_cause |
| 9 | SLDB | -6.8 | -0.30 | +0.00 | -0.30 | 0.0 | -0.3 | -0.76 | 6.8 | -7.0 | 0.93 | 8.8 | +0.38 | -1.73 | no_identifiable_cause |
| 10 | TVRD | -18.9 | -0.75 | +0.00 | -0.75 | 0.0 | -0.8 | -2.50 | 18.9 | -13.2 | 3.99 | 0.2 | +0.80 | +0.34 | no_identifiable_cause |
| 11 | NCT | -12.4 | -1.00 | +0.00 | -1.00 | 0.0 | -1.0 | -0.08 | 12.4 | -56.5 | 0.69 | 4.3 | +0.21 | -0.33 | no_identifiable_cause |
| 12 | OBX | -7.0 | -1.00 | +0.00 | -1.00 | 0.0 | -1.0 | -1.48 | 7.0 | -12.2 | 0.65 | 6.6 | +1.83 | -1.73 | index_or_flow |
| 13 | VEEA | -6.2 | -1.00 | +0.00 | -1.00 | 0.0 | -1.0 | -0.45 | 6.2 | -39.2 | 0.92 | 0.6 | +0.00 | -1.04 | catalyst_passed |
| 14 | BYND | -9.1 | -1.50 | +0.00 | -1.50 | 0.0 | -1.5 | -1.43 | 9.1 | -9.7 | 2.04 | 11.5 | +0.07 | -0.20 | dilution_or_going_concern |
| 15 | JAGX | -25.4 | -3.50 | +0.00 | -3.50 | 0.0 | -3.5 | -3.42 | 25.4 | -87.5 | 43.63 | 0.2 | +0.00 | -0.17 | dilution_or_going_concern |


## The name above the floor

**JAGX, −3.50 (leg 2 −3.50, leg 1 0).**

- *What caused the fall.* This is day three of unwinding a float squeeze. The stock rose about 1,100% on 09-22 on an FDA fee-waiver headline, with about 520k shares outstanding after the 1-for-15 split of 09-17, then fell 74% on 09-23. Today's leg came after two pre-market filings: the 06:01 ET 8-K disclosing the Streeterville exchange shares, and the 09:22 ET 424B5 resetting the ATM. The fall came on **43.6× normal volume**.
- *What the hunt thinks the reaction got wrong.* The gap priced the *announcement* of the ATM capacity, not how much of it is still unsold. ATM fills are invisible until the next 10-Q, so an agent working a programme larger than the market cap can keep printing into the 09-25 session.
- *Base rate.* The number is negative, so it is not fighting phase 0; it agrees with it. The median faller is −1.00% at the next close. Falls on over 15× volume do −2.44%. JAGX's own 24 comparable falls have a median of −5.94%. Its phase-0 band prior (−40..−25, turnover under $1m) is −0.17%.
- *Tradability.* The median 20-day turnover is **$0.22m**, right at the floor. The half-spread estimate is **unknown** (the estimator floored at zero). ATR14 is 87.5%. A short needs a borrow that is unlikely to exist on a 1.3m-share float mid-squeeze. **This is research, not a trade.**
- The emitted `impact_sum` is the findings sum, −3.5. The hunter's own view was −4.0, pulled toward the name's own history; only the sum is ranked.
- One discrepancy to carry: `rev_universe` put the fall at −23.7% and the baseline, sealed a minute later, at −25.4%. The screener's unadjusted −74.1% is the pre-split 09-23 comparison and should be ignored.

## Critical read

- **The legs.** `overshoot_pct` is 0.0 on all 15 names. `more_to_come_pct` carries the whole ranking, from 0 to −3.5. Which leg carries the result is what this stage is trying to learn, and today supplies no evidence about leg 1 at all. That is now two days out of three with no repricing finding.
- **Supply, supply, supply.** Nine of the nine non-zero names land on `supply`. Most are standing ATMs that *can* sell on any day, sized small (−0.3 to −1.0) because nothing dates a draw into the window. Only two are dated: JAGX, with a refresh filed today, and BYND, where the third and last VWAP day of the note-exchange pricing is 09-25 itself. BYND's hunter found the relief once the seller finishes, but that falls on 09-28, so it went to `outside_window` (+2.0) and is not in the number.
- **The hunt and the lean agree more than usual.** The rank correlation of `impact_sum` with `priced_lean_pct` is +0.25 across the 15 names. JAGX tops both, since the lean also reads −3.42.
- **What cuts against the continuation read.** Nine of the fifteen fell on under 1.3× volume (OBX 0.65×, NCT 0.69×, MEDS 0.85×, VEEA 0.92×, SLDB 0.93×). Phase 0 puts that under-2× bucket at **+1.46%** the next session. Several hunters halved their own view for this reason (NCT −1.0→−0.5, VEEA −1.0→−0.5, OBX −1.0→−0.8, SLDB −0.3→−0.2, BW −0.3→−0.2). The key is the findings sum, not the view, so those haircuts are not in the ranking.
- **Health Care, 8 of 15.** Several hunters point at a cooling XBI and the 09-23 Immunovant lupus miss (possible sympathy for ZBIO; unsourced). A sector sell-off is the most ordinary way for eight biotechs to fall on one day, so it is a correlated exposure the scorer cannot see.
- **No name is positive, so there is no rebound thesis to price against the base rate.** The median faller does −1.00% at the next close, and the median is negative in every cut phase 0 took. That is close-to-close, and this screen was taken at 15:04 ET.

## What it would cost to trade

Summed estimated half-spreads over the 15 names come to **8.75 points** (mean 0.58, round trip ≈ 1.17), and three of the fifteen read UNKNOWN. The predictions have a standard deviation of **0.90 points**. The whole day's spread of predictions is smaller than one round trip. Phase 0 measured the gross one-session edge at ±0.35% against ~1.06 points round trip, so **one session is not tradeable**, and nothing in today's ranking changes that.

## Caveats every reader needs

- **The spot is the 15:04 EDT screen price, not a close.** The scored window is today's close → the 09-25 close. Phase 0's base rates are close-to-close, which is a different population. In the worst 15 at 15:00 vs at the close: 86.4% overlap, and the 15:00→close move has mean −0.24%, median 0.00%, sd 4.54%.
- **The live bar lags on several names.** The screener's change and the adjusted fall differ by −3 to −5pp on OBX, BLSM, AMTX, SLDB, MEDS and VEEA; for example, AIRS read −14.6% on the screener and −5.8% adjusted, and was not hunted. The universe may therefore have missed names that fell harder. This is recorded in the run log and not corrected.
- **Short interest is published about 8 business days after settlement.** Every figure here is the 2026-08-31 settlement, and several predate a reverse split (JAGX, NCT, VEEA) or a squeeze (JAGX, MEDS). The position carried INTO the fall cannot be observed.
- **`next_earnings_estimated` is Zacks's cadence algorithm, not a company announcement**, on every name.
- **No name has a usable option chain** (`no_options_market`, `unusable_chain` or `crumb_failed`), except BYND (front straddle 4.77%, spread 29% of mid) and EOSE (7.7%, spread 67% of mid). Stage R runs effectively anchor-less (FINDINGS §33: ρ=+0.073, p=0.45).
- **Contamination.** Hunters on JAGX, BYND, BLSM and EOSE saw same-day or earlier prices in search snippets. Each states that nothing dated after the screen was used, and JAGX excluded a snippet that might have been later.
- **The 2026-09-22 resolve covers only 5 of 15 names**, the same row-dropping defect the 09-23 note recorded. `lean_vs_free_control_rho` read 0.0 on those five. See `../resolve-2026-09-22.json`. The 09-23 run's `resolve.json` is all-pending by construction.
- This stage places no orders.

---
*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*

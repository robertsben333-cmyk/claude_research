# Stage R — reversal note — drop date 2026-09-29, window to close 2026-09-30

Screened intraday at **2026-09-29 15:04 EDT** (bars not final). SPY on the day at the screen: **−0.09%**. Names above the floors: 47. Hunted: 15 of 15. Rankable: 15. Above the conviction floor (|impact_sum| ≥ 3.0): **three names, CTNT −5.00, LGHL −3.00 and OPTT −3.00**. The largest sector is Consumer Discretionary, **3 of 15 (20%)**, so this is not a sector bet. It is one *pattern* bet again, though. Eleven of the fifteen hunts name live issuer or holder supply: an ATM, an equity line, a toxic convertible, an effective shelf or S-8, or an unfiled exchange 8-K. That is a correlated exposure the scorer cannot see.

The scored window is **today's close → 2026-09-30 close**. The screen is an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close, and the 15:00→close move was mean −0.24%, median 0.00%. **Phase 0's base rates below are close-to-close and this screen is not**, so they are priors about a neighbouring population, not this one.

## Answer first

- **All three floor-clearers are leg 2, supply, and none has a leg-1 finding, so no `mechanism_in_window` question arises on the repricing side.** Each one's leg-2 finding does name its in-window mechanism, given below.
  - **CTNT −5.00.** This is the second split-adjusted session after a 1-for-150 reverse split. The Aug-21 $35.28m Pacific Century ATM took Class A shares from 2.96m to 199.8m (pre-split) by 09-22, and it is still open against a market cap of about $4m. The same issuer's previous ATM kept selling after its April split. What the reaction missed: sales made after 09-22 are invisible until the next filing, and the ATM draws daily with no new document. The mechanism is the ATM itself, open on 09-30. **Base rate:** the median faller does −1.00% the next close, and the −25..−15 band averages **+0.27%**. This name's own 24 comparable falls have a median of −6.45%. The hunter's range is −20 to +10.
  - **LGHL −3.00.** A 6-K at 09:15 ET today disclosed a $3.0m senior secured convertible issued 09-28. It converts at 90% of the lowest 10-day VWAP into registered ADSs, which is roughly 10× a normal day's turnover. What the reaction missed: the holder's convert-and-sell flow has barely started, and the fall came on 1.06× volume. The mechanism is a conversion price that resets lower each day, so the holder has an incentive to sell from the first sessions. **Base rate:** −1.00% median faller; the −25..−15 band averages +0.27%; under-2× volume averages **+1.46%**. This name's own 48 falls have a median of +0.39%. The hunter's own `expected_move_pct` is −2.0, which it held back for exactly that tension. The key follows the finding sum.
  - **OPTT −3.00.** An 8-K after the close on 09-25 swapped the Series C-1 notes into Series D notes. The D notes convert at any time at 93% of the lowest 7-day VWAP, up to 19.99% of shares before a stockholder vote. The stock has fallen three legs since (−35% from 09-22) on 0.69× volume. What the reaction missed: tomorrow's conversions price below today's close. The mechanism is that the conversion right has been live since 09-25 with no leak-out found. **Base rate:** −1.00% median faller; −25..−15 band +0.27%; under-2× volume +1.46%. This name's own 27 falls have a median of 0.0%. The hunter's `expected_move_pct` is −2.5.
- **Below the floor, it is mostly the same finding at smaller sizes.**
  - WHLR −1.5: an Item 3.02 8-K for the 09-23 preferred-for-common exchanges falls due today and was not filed at the screen.
  - NCI −1.5: an effective $100m F-3; the baby-shelf limit is measured at pre-crash prices.
  - SWMR −1.0: the Lucid equity line, re-effective since 09-18.
  - NCT −1.0: an S-8 effective on filing, plus a $200m F-3.
  - FTCI −1.0: the minimum-cash covenant test of $10.0m on **09-30**, against $10.075m at June 30. This is the one dated solvency item in the day.
  - CUE −0.8: an open $36.8m Jefferies ATM.
  - INDP −0.5: an undrawn $100m H.C. Wainwright ATM.
  - EAF −0.3: an Evercore ATM. The likely cause of the fall is the preliminary US anti-dumping margin on Indian graphite electrodes, which came in far below the petition.
- **Four zeros: CABO, CCG, INSE and USDEW.**
  - CABO: the dated catalysts sit just **outside** the window. The MBI acquisition closes 10-01, and S&P has flagged a further cut to B on that close.
  - INSE: the cause is fully identified. Brazil's online-betting ban was signed 09-25 and quantified by the company at 09:00 ET today. The STF ruling cannot land before 10-01.
  - CCG: no identifiable cause.
  - USDEW: see the defect note below. All of these went to `outside_window`, as the brief requires.
- **Leg 1 is empty again: zero repricing findings in 15 hunts.** `overshoot_pct` is 0 on every name. That makes it 2 names out of 105 over the seven hunted days since 09-22.
- **No reversal run has beaten a free control yet.**
  - The 09-25 run is now resolved: `impact_sum` **ρ −0.024 (p 0.94, 14 names)** against `neg_ret_d` −0.429, `neg_atr14` +0.152 and `neg_vol_spike` +0.108.
  - Pooled 09-22 → 09-25 at d1 over 59 names and 4 days: `impact_sum` **ρ −0.165 (perm p 0.22)**, against `neg_atr14` −0.015, `neg_ret_d` −0.071 and `neg_vol_spike` +0.020.
  - `lean_vs_free_control_rho` is **0.054** pooled (−0.132 on 09-25 alone), so the lean is not the free control in disguise.
  - The legs split: leg 1 (`overshoot_pct`) reads **+0.147 (p 0.29)** and leg 2 (`more_to_come_pct`) **−0.212 (p 0.12)**. Leg 2 is still the wrong sign for its pre-registered hypothesis, and it is the leg every floor-clearer today sits on.
  - Over 09-22 → 09-25 the conviction book (NUR, JAGX and DBGI short) returned **−1.45% gross** against **+3.99%** for shorting every name.
  - **A run that does not beat the free controls has established nothing.** The 09-28 run is pending, because its window closes at today's close. See `../resolve-2026-09-25.json` and `../resolve-pool-0922-0925.json`.

## Ranked table

The two leg columns are the hunters' own finding sums, split by `leg`. Lean = `priced_lean_pct`. Band prior is the phase-0 cross-section expectation for the name's drop band and turnover band (close-to-close). Half-spread is Corwin-Schultz, which is a floor. **0.00 means UNKNOWN (EAF, FTCI, NCT, WHLR, OPTT, CTNT), never narrow.** Fall % is the baseline's sealed `ret_d`.

| # | ticker | fall % | impact_sum | leg1 repricing | leg2 new info | overshoot_pct | more_to_come_pct | lean | −ret_d | −ATR14 | vol× | turnover $m | half-spread % | band prior % | cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CABO | -11.4 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | -0.44 | 11.4 | -16.4 | 2.27 | 5.8 | +1.82 | -0.29 | no_identifiable_cause |
| 2 | CCG | -19.4 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +1.54 | 19.4 | -21.6 | 1.73 | 0.5 | +0.38 | +0.34 | no_identifiable_cause |
| 3 | INSE | -16.0 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | -1.61 | 16.0 | -9.5 | 5.14 | 1.1 | +0.31 | -0.39 | litigation_or_regulatory |
| 4 | USDEW | -10.2 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.96 | 10.2 | -20.1 | 1.04 | 0.4 | +3.73 | +0.40 | sympathy |
| 5 | EAF | -12.9 | -0.30 | +0.00 | -0.30 | +0.0 | -0.3 | -0.57 | 12.9 | -12.7 | 1.57 | 6.4 | +0.00 | -0.29 | litigation_or_regulatory |
| 6 | INDP | -13.1 | -0.50 | +0.00 | -0.50 | +0.0 | -0.5 | -0.67 | 13.1 | -22.3 | 0.63 | 3.0 | +0.18 | -0.33 | no_identifiable_cause |
| 7 | CUE | -10.8 | -0.80 | +0.00 | -0.80 | +0.0 | -0.8 | -1.15 | 10.8 | -20.7 | 1.1 | 5.9 | +0.78 | -0.29 | no_identifiable_cause |
| 8 | FTCI | -13.4 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | +0.45 | 13.4 | -12.4 | 6.4 | 0.5 | +0.00 | +0.40 | no_identifiable_cause |
| 9 | NCT | -18.4 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | -1.01 | 18.4 | -113.9 | 0.69 | 3.9 | +0.00 | -0.39 | no_identifiable_cause |
| 10 | SWMR | -10.4 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | -3.08 | 10.4 | -22.0 | 2.88 | 16.5 | +1.27 | -0.29 | no_identifiable_cause |
| 11 | NCI | -31.1 | -1.50 | +0.00 | -1.50 | +0.0 | -1.5 | -5.40 | 31.1 | -93.8 | 2.22 | 7.0 | +0.27 | -0.87 | no_identifiable_cause |
| 12 | WHLR | -19.8 | -1.50 | +0.00 | -1.50 | +0.0 | -1.5 | -2.77 | 19.8 | -49.5 | 0.78 | 1.0 | +0.00 | -0.39 | dilution_or_going_concern |
| 13 | LGHL | -16.5 | -3.00 | +0.00 | -3.00 | +0.0 | -3.0 | +0.37 | 16.5 | -30.0 | 1.06 | 0.4 | +1.27 | +0.34 | dilution_or_going_concern |
| 14 | OPTT | -17.1 | -3.00 | +0.00 | -3.00 | +0.0 | -3.0 | +0.15 | 17.1 | -33.0 | 0.69 | 0.8 | +0.00 | +0.34 | dilution_or_going_concern |
| 15 | CTNT | -21.4 | -5.00 | +0.00 | -5.00 | +0.0 | -5.0 | -3.78 | 21.4 | -651.6 | 1.04 | 5.7 | +0.00 | -0.35 | dilution_or_going_concern |

## What it would cost to trade

The sum of the estimated half-spreads over the 15 names is **10.0 points** (mean 0.67, median 0.27), and six of those are unknown rather than zero. So a round trip averages at least **1.3 points a name**, before borrow. The whole day's predictions span **5.0 points** (sd 1.38), and 12 of the 15 sit inside ±1.5, **inside one round trip**.

The three floor-clearers are all thin ($0.4–5.7m a day), all shorts, and all on names where a convertible holder or ATM agent is also selling. That is exactly where borrow is scarcest and dearest, and this table cannot see borrow. Phase 0's gross one-session edge is ±0.35% against about 1.06 points of spread, and nothing today changes that.

## Critical read

- **Labels a reader must carry.** `next_earnings_estimated` is a Zacks cadence algorithm, not a company date (the TRT failure). Every earnings date the hunters cite today is one of those. Short interest is the 2026-09-15 settlement, published about eight business days late, so **the position carried into these falls is not observable on any name**. On OPTT, CABO and EAF the Nasdaq short-interest endpoint returned 503 as well.
- **No finding shows a draw dated inside the window.** An ATM, an equity line or a convertible proves the seller *can* sell tomorrow. CTNT's 67× share count and LGHL's same-day 6-K are the strongest evidence that it *has* sold. ATM and conversion flows are not disclosed one by one. The pooled leg-2 rank so far carries the wrong sign, so the day's biggest bet is also its least supported one.
- **Contaminated history fields.** Several names moved through reverse splits in the last 90 days: CTNT (1:150 on 09-28), OPTT (1:30 on 09-14), NCT (25:1 on 09-17), WHLR (1:9 on 09-22), CCG (35:1 on 07-20) and CUE (1:30 in April). Their ATR and run-up fields cross the split: **CTNT's −651.6 ATR**, NCT's −113.9 and CCG's +1937% 60-day run-up are artefacts, not moves. Each hunter said so and did not size on them. The corporate-action kill did not fire, because today's falls are not split days. On NCI the screener's raw change (−83.8%) differs from the adjusted one by 52.6pp. The hunter identified 09-28 as an 83.75% collapse from $14.65 and today as a further −31%, so the sealed fall is today's leg only.
- **Screen defect, reported and not fixed: USDEW is a warrant, not common stock.** It is the public warrant of StableCoinX (ex-TLGY SPAC), with an $11.50 strike and 2031 expiry. `rev_universe.py` claims to screen listed common stocks, and phase 0's base rates were computed on common stocks only, so USDEW is outside the population every prior here describes. Its hunt returned zero findings, so it does not affect the conviction names. It sits in the ranking at 0.00 and will enter the resolved sample unless the screen is fixed. Per the rules, nothing was moved today. The fix is a warrant/unit/right suffix filter in `rev_universe.py`, left for a development session.
- **Two hunters withheld part of their sum and the key did not.** LGHL's `expected_move_pct` is −2.0 against −3.0, and OPTT's is −2.5 against −3.0. Both cut for the same reason: the fall came on under 2× volume, where phase 0 measured +1.46%. Nothing ranks `expected_move_pct`. It is recorded so a reader does not read LGHL's and OPTT's −3.0 as firmer than the hunters did.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

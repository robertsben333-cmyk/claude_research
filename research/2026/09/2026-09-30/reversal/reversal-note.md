# Stage R — reversal note — drop date 2026-09-30, window to close 2026-10-01

Screened intraday at **2026-09-30 15:04 EDT** (bars not final). SPY on the day at the screen: **+0.33%**. Only **38 names** passed the floors, so the worst 15 reach down to falls of 6–7%: five of the fifteen fell less than 10% at the screen. All 15 were hunted and all 15 are rankable. Above the conviction floor (|impact_sum| ≥ 3.0): **one name, CDT at −4.00**.

The largest sector is Health Care, **4 of 15 (27%)**, and Consumer Discretionary also has 4, so this is not a sector bet. It is one *pattern* bet again, though. Eight of the fifteen hunts name live issuer or holder supply: a discount convertible, an ATM, a resale shelf, placement shorting or a 10% holder selling out. That is a correlated exposure the scorer cannot see.

The scored window is **today's close → 2026-10-01 close**. The screen is an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close, and the 15:00→close move was mean −0.24%, median 0.00%. That churn is likely higher today, because the bottom of this list sits at −6% to −8% where names swap in and out easily. **Phase 0's base rates below are close-to-close and this screen is not**, so they are priors about a neighbouring population, not this one.

## Answer first

- **One floor-clearer, CDT −4.00. It is leg 2 (supply) and has no leg-1 finding.**
  - **Cause:** a dilution spiral on the second session after a 1-for-25 reverse split (market-effective 09-29). There was no news today, and the fall is entirely intraday on 1.26× volume. The supply comes from three sources:
    - J.J. Astor's senior secured convertible converts at 70% of the lowest 20-day VWAP, into a resale registration effective since 09-17.
    - An open A.G.P. ATM, with 80% of its proceeds pledged to repaying that note.
    - 12.1m pre-split Sarborg acquisition shares registered for resale.
  - **What the reaction missed:** the holder converts at about 30% below the lowest VWAP, so it profits from selling at any price above roughly $0.95, against a $1.355 spot. Weekly installments have been running since 09-21, so the seller is not finished.
  - **Mechanism:** conversion at the lender's option and ATM draws on any trading day, including 10-01, with no new filing needed. This name closed lower after all 12 of its September falls.
  - **Base rate:** the median faller does **−1.00%** the next close. CDT's band (−7.5..−5) prior is **−1.77%**, and phase 0 has only 7 events in that band (mean −2.49%). This name's own 271 falls have a median of −2.51%.
  - **The number to discount:** the hunter's own `expected_move_pct` is −3.5, cut from −4.0 because volume was ordinary.
- **Leg 1 found one repricing finding in 15 hunts: NCT −1.00, and it does carry a `mechanism_in_window`.** A 13D/A filed today is the first document to state the as-converted effect of the CEO's 1.625m Class B shares at $0.40, which were not consolidated: 58.7% of the equity. The mechanism is a wider overnight audience reading that document. The hunter sized it small because the Form 4 had already disclosed the same purchase on 09-25. Every other name's `overshoot_pct` is 0. QNC's hunter filed a dilution-arithmetic overshoot without a mechanism in `outside_window`, as the brief requires, and it is not promoted here.
- **Leg 2 carries everything else.** Eight names sit between −1.0 and −2.5 on supply findings: EMAT, MNOV, INDP, JAGX, VEEA, JLHL and LGHL, plus CDT above the floor. Six are zeros with no identifiable cause or nothing dated inside the window: ADV, CCG, GRNQ, QNC, TANH and XLAB.
- **No reversal run has beaten a free control yet.**
  - The **2026-09-28 run is now resolved at d1** (15 names, 0 pending).
  - `impact_sum` read **ρ +0.115 (perm p 0.68)**, against `neg_atr14` −0.200, `neg_ret_d` +0.107 and `neg_run_up_20d` **+0.389**.
  - `lean_vs_free_control_rho` is **−0.589**, so the lean is not the free control in disguise. As a ranker it read ρ −0.557 (p 0.04), the wrong way.
  - All ten finding-bearing names on 09-28 were leg 2 only, so leg 1 and `overshoot_pct` could not be ranked.
  - **A run that does not beat the free controls has established nothing.** This one beat `neg_atr14` and lost to `neg_run_up_20d` on one day with nothing significant.
  - The 2026-09-29 run is pending, because its window closes at today's close. See `../resolve-2026-09-28.json`.

## Ranked table

The two leg columns are the hunters' own finding sums, split by `leg`. Lean = `priced_lean_pct`. Band prior is the phase-0 cross-section expectation for the name's drop band and turnover band, close to close. Half-spread is Corwin-Schultz, which is a floor. **+0.00 means UNKNOWN (MNOV, NCT, INDP, JAGX, VEEA, CDT), never narrow.** Fall % is the baseline's sealed `ret_d`.

| # | ticker | fall % | impact_sum | leg1 repricing | leg2 new info | overshoot_pct | more_to_come_pct | hunter expected_move | lean | −ret_d | −ATR14 | vol× | turnover $m | half-spread % | band prior % | cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ADV | -11.8 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | -0.40 | 11.8 | -6.7 | 0.99 | 1.6 | +0.66 | -0.33 | no_identifiable_cause |
| 2 | CCG | -9.5 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | +0.27 | 9.5 | -24.0 | 0.75 | 0.5 | +0.38 | +0.50 | no_identifiable_cause |
| 3 | GRNQ | -14.0 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | +0.73 | 14.0 | -22.4 | 0.06 | 1.1 | +0.06 | -0.33 | no_identifiable_cause |
| 4 | QNC | -7.7 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | -0.56 | 7.7 | -12.6 | 1.05 | 2.0 | +0.55 | -0.23 | management_or_governance |
| 5 | TANH | -7.0 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | -0.45 | 7.0 | -23.4 | 0.13 | 0.6 | +1.26 | -1.04 | no_identifiable_cause |
| 6 | XLAB | -11.8 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | -2.34 | 11.8 | -23.1 | 0.56 | 0.2 | +0.33 | +0.40 | no_identifiable_cause |
| 7 | EMAT | -14.8 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | -1.0 | -1.18 | 14.8 | -20.3 | 1.66 | 3.6 | +1.08 | -0.33 | dilution_or_going_concern |
| 8 | MNOV | -11.2 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | -0.7 | +0.17 | 11.2 | -26.2 | 1.01 | 0.5 | +0.00 | +0.40 | clinical_or_binary_readout |
| 9 | NCT | -20.6 | -1.00 | -1.00 | +0.00 | -1.0 | +0.0 | -1.5 | -1.73 | 20.6 | -153.6 | 4.66 | 1.9 | +0.00 | -0.39 | dilution_or_going_concern |
| 10 | INDP | -17.9 | -1.50 | +0.00 | -1.50 | +0.0 | -1.5 | -1.0 | -0.04 | 17.9 | -27.3 | 0.71 | 3.0 | +0.00 | -0.39 | equity_offering |
| 11 | JAGX | -16.7 | -1.50 | +0.00 | -1.50 | +0.0 | -1.5 | -2.0 | -1.47 | 16.7 | -134.7 | 3.78 | 0.6 | +0.00 | +0.34 | dilution_or_going_concern |
| 12 | VEEA | -13.6 | -1.50 | +0.00 | -1.50 | +0.0 | -1.5 | -1.5 | -0.38 | 13.6 | -58.7 | 0.51 | 0.7 | +0.00 | +0.40 | no_identifiable_cause |
| 13 | JLHL | -8.7 | -2.00 | +0.00 | -2.00 | +0.0 | -2.0 | -1.5 | -0.47 | 8.7 | -11.5 | 3.62 | 0.4 | +0.03 | +0.50 | equity_offering |
| 14 | LGHL | -6.4 | -2.50 | +0.00 | -2.50 | +0.0 | -2.5 | -2.0 | -0.45 | 6.4 | -36.9 | 324.85 | 0.4 | +1.27 | -1.04 | dilution_or_going_concern |
| 15 | CDT | -6.6 | -4.00 | +0.00 | -4.00 | +0.0 | -4.0 | -3.5 | -2.18 | 6.6 | -55.0 | 1.26 | 1.2 | +0.00 | -1.77 | dilution_or_going_concern |

## For each name with a finding, the base rate it argues against

Every number here is negative, so none is a rebound thesis. The drift phase 0 measured runs the same way, so these are cheaper claims than a bounce would be. They are still claims about **one session**, where the median is −1.00% and gross edge is about ±0.35%.

- **CDT −4.00** (above the floor): see above.
- **LGHL −2.50.**
  - **Cause:** a 09:15 ET treasury-swap 6-K gapped the ADS up 46%, and it was sold down 36% intraday on **325× volume**. That came one day after a new $3m convertible at 90% of the lowest 10-day VWAP. The sealed fall (−6.4%) understates the intraday give-back.
  - **Mechanism:** the note is convertible immediately, and the **10-01 quarterly interest date** is payable in ADSs at 90% of the 5-day VWAP. This is the one finding today that names a date inside the window.
  - **Base rate:** >15× volume averages −2.44% next session in phase 0. This name's own 219 falls have a median of 0.0%. The hunter's `expected_move_pct` is −2.0.
- **JLHL −2.00.** Day two after a Reg D placement at $0.30 against about $5.9. Placement holders hold 3.0m shares-equivalent, twice the float, and the SPA leaves them free to short from signing. Band prior (−10..−7.5) is **+0.59%**, which is why the hunter's `expected_move_pct` is −1.5.
- **INDP −1.50.**
  - **Cause:** today's 8-K extended an unfunded $24m PIPE to 10-16.
  - **Supply:** a 58.9m-share resale shelf with no lock-up, and a live $100m ATM that had not been drawn as of 09-04.
  - **Base rate:** this name's own 26 falls are a coin flip (median +0.23%). The hunter's `expected_move_pct` is −1.0.
- **JAGX −1.50.** An effective $9.8m ATM about equal to the market cap. It is the only equity channel open until the 11-06 vote. Own history median −2.88%. The hunter's `expected_move_pct` is −2.0.
- **VEEA −1.50.** An unwinding pump after a non-binding merger term sheet. An effective ATM and a 90%-of-market convertible, at an issuer with $0.9m of cash. Band prior +0.40%.
- **EMAT −1.00.** A pending resale S-1/A for 7.5m Yorkville conversion shares that could go effective overnight. The previous one took two days. The cause is inferred, not sourced (35% confidence).
- **MNOV −1.00.** Day three after a Phase 2 miss on 09-28. A 9.9% holder began an accelerated disposal on 09-25 and now sits under the Form 4 threshold. Own history median 0.0%. The hunter's `expected_move_pct` is −0.7.
- **NCT −1.00** (leg 1, mechanism stated): see above. Its 153.6 ATR is a reverse-split artefact.

## What it would cost to trade

The sum of the estimated half-spreads over the 15 names is **5.6 points** (mean 0.37, median 0.06), and six of those are unknown rather than zero. So a round trip averages **at least 0.75 points a name, with unknown spreads on six of the fifteen, before borrow**. The whole day's predictions span **4.0 points** (sd 1.12), and **12 of the 15 sit inside ±1.5**, which is about one round trip on these names. The single floor-clearer, CDT, trades about $1.2m a day, has an unknown spread, and is a short on a name where a convertible holder and an ATM agent are also selling. That is where borrow is scarcest and dearest, and this table cannot see borrow. Phase 0's gross one-session edge is ±0.35% against about 1.06 points of spread, and nothing today changes that.

## Critical read

- **Labels a reader must carry.**
  - `next_earnings_estimated` is a Zacks cadence algorithm, not a company date (the TRT failure).
  - Short interest is the 2026-09-15 settlement, published about eight business days late, so **the position carried into these falls is not observable on any name**. On QNC the Nasdaq short-interest endpoint returned 503.
- **No finding shows a draw dated inside the window, with one exception.** An ATM, a convertible or a resale shelf proves the seller *can* sell tomorrow, not that it will. LGHL's 10-01 interest date is the one dated item. Leg 2's pooled rank so far has carried the wrong sign for its pre-registered hypothesis (−0.212 over 09-22 → 09-25), so the day's only floor-clearer rests on the least-supported kind of finding.
- **Contaminated history fields.** Reverse splits in the last 90 days: CDT (1:25 on 09-29 and 1:10 in July), NCT (25:1 on 09-17), JAGX (1:15 on 09-17), CCG (35:1 on 07-20), TANH (1:50 on 09-03), GRNQ (1:10 on 08-06), VEEA (1:20 on 08-28) and LGHL (ADS ratio on 09-10). Their ATR and run-up fields cross the splits: **NCT −153.6, JAGX −134.7, VEEA −58.7, CDT −55.0**, and INDP's +149% 20-day run-up is real, from a September run. Each hunter flagged the artefacts and did not size on them.
- **Baseline defect, reported and not fixed: `spot_basis` is mislabelled on an intraday seal.** Every baseline today says "unadjusted close of the drop day", but `spot` is the live 15:04 ET screen price. The TANH hunter caught it. The number is right and the label is wrong. The fix belongs in `rev_priced_in.py` for a development session, because nothing moves on a live run.
- **LGHL's sealed fall hides its day.** −6.4% close-to-screen, but +46% gap then −36% intraday, `gap_share` −7.2. Phase 0's drop-size band prior (−1.04) describes a quiet −6% faller, which this is not.
- **Hunters withheld part of their sum and the key did not**, on CDT (−3.5 vs −4.0), JLHL (−1.5 vs −2.0), LGHL (−2.0 vs −2.5), INDP (−1.0 vs −1.5) and MNOV (−0.7 vs −1.0). In every case the reason was ordinary volume or a positive own-history median. JAGX and NCT went the other way (−2.0 vs −1.5, −1.5 vs −1.0). Nothing ranks `expected_move_pct`.
- **Fewer names on the floor than usual.** Only 38 of 5,981 names passed, against 47 yesterday. The bottom third of this list is 6–8% fallers, a band phase 0 barely sampled (7 events in −7.5..−5).

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

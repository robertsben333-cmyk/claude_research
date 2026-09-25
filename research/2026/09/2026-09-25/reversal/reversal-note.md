# Stage R — reversal note — drop date 2026-09-25, window to close 2026-09-28

Screened intraday at 2026-09-25 15:04 EDT (bars not final). SPY on the day at the screen: +0.45%. Names above the floors: 52. Hunted: 15 of 15. Rankable: 15. Above the conviction floor (|impact_sum| ≥ 3.0): **2, IPEX at −5.00 and DBGI at −3.50**, both continuation calls, both leg 2, both on supply. **Health Care is 7 of the 15 names (47%)**, just under the half-line, so the day is less concentrated than 09-24's (53%) but it is still a correlated exposure the scorer cannot see.

The window runs over a weekend: today's close → **Monday 2026-09-28's close**.

## Answer first

- **IPEX, −5.00: a de-SPAC closing-day dump with the seller barely started.** Inflection Point V closed its merger with GOWell Technology today (release 13:30 ET) and trades as **GOW from 2026-09-28**. Only about 1.15m public shares are left after 7.48m were redeemed. About 5.1m more become freely tradeable at closing: 1.78m from rights conversion and 3.34m sponsor and underwriter shares whose lock-up was removed on 08-31. Today's volume was roughly 0.35–0.5m shares, so most of that supply has not traded yet.
- **DBGI, −3.50: an open $100m Aegis ATM at a going-concern issuer.** The issuer has $1.4m of cash against a $12.9m working-capital deficit. Its share count rose 70% in seven weeks (547,534 → 933,509). A $1.0m note instalment is due 10-23. The ATM can sell on Monday with no filing.
- **Leg 1 appears for the first time in three days, on one name: BYND +1.50, and it carries a `mechanism_in_window`.** The three-day VWAP window (Sep 23–25) that fixes the share count for the $15m 2027-note exchange ends at today's close. The price-setting seller is therefore finished and dated. BYND is the only positive number on the day, and the only overshoot. It is below the floor.
- **Nine names hunted to zero**: CRMT, FISN, KLRA, KPLT, LONA, TRT, VOGX, ZTG and, at +0.3, effectively MEDS. Several of them have a real, dated second shoe just **outside** the window: CRMT's lender waiver expires 10-01 (the 8-K itself carries "complete loss" and bankruptcy language), ZTG's 12:1 consolidation EGM is on 09-30, LONA's $146m Series A warrants at $6.35 lapse around 10-19, and KLRA's IPO lock-up ends 10-13. They are filed in `outside_window` and do not reach the ranking, as the brief requires. A zero is an answer, not a missing hunt.
- **No reversal run has beaten a free control yet.** The 09-22 and 09-23 runs pool at d1 over 30 names: `impact_sum` ρ **−0.167** (p 0.38), against `neg_atr14` −0.148 and `neg_ret_d` −0.021. `lean_vs_free_control_rho` is 0.107, so the lean is not the free control in disguise. The hunt's sign is negative, and none of these numbers is distinguishable from zero. **A run that does not beat the free controls has established nothing.** Leg 2 alone (`more_to_come_pct`) reads −0.223 at d1 and −0.328 at the open (p 0.10). That is the wrong sign for the hypothesis and the thing to watch. Leg 1 has 1 name in that sample, so it cannot be ranked. The 09-24 run is still pending, because its window closes at today's close. See `../resolve.json` and `../resolve-2026-09-24.json`.

## Ranked table

The two leg columns are the hunters' own finding sums, split by `leg`. Lean = `priced_lean_pct`. Band prior = the phase-0 cross-section expectation for the name's drop band and turnover band (close-to-close). Half-spread is Corwin-Schultz, which is a floor; **0.00 means UNKNOWN**, never narrow.

| # | ticker | fall % | impact_sum | leg1 repricing | leg2 new info | overshoot_pct | more_to_come_pct | lean | −ret_d | −ATR14 | vol× | turnover $m | half-spread % | band prior % | cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BYND | -8.3 | +1.50 | +1.50 | +0.00 | +1.5 | +0.0 | -1.45 | 8.3 | -10.4 | 1.97 | 11.9 | +0.13 | -0.20 | equity_offering |
| 2 | MEDS | -9.7 | +0.30 | +0.00 | +0.30 | +0.0 | +0.3 | -0.87 | 9.7 | -52.4 | 1.21 | 0.3 | +1.37 | +0.50 | no_identifiable_cause |
| 3 | CRMT | -19.5 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | -0.67 | 19.5 | -28.8 | 3.38 | 0.5 | +1.21 | +0.34 | dilution_or_going_concern |
| 4 | FISN | -9.4 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.32 | 9.4 | -10.7 | 1.86 | 1.8 | +1.17 | -0.23 | short_report |
| 5 | KLRA | -6.0 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | -0.05 | 6.0 | -8.8 | 1.24 | 12.3 | +0.59 | -1.73 | no_identifiable_cause |
| 6 | KPLT | -10.9 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | -0.27 | 10.9 | -17.3 | 4.85 | 1.6 | +1.07 | -0.33 | no_identifiable_cause |
| 7 | LONA | -31.7 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | -1.56 | 31.7 | -27.1 | 8.54 | 0.2 | +1.04 | -0.17 | no_identifiable_cause |
| 8 | TRT | -13.5 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | -2.46 | 13.5 | -17.0 | 9.44 | 1.6 | +0.15 | -0.33 | earnings_miss |
| 9 | VOGX | -8.8 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | -2.10 | 8.8 | -16.1 | 0.23 | 3.9 | +1.18 | -0.23 | no_identifiable_cause |
| 10 | ZTG | -10.4 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +1.66 | 10.4 | -29.5 | 0.40 | 0.6 | +1.48 | +0.40 | customer_or_contract_loss |
| 11 | NEOV | -6.3 | -0.40 | +0.00 | -0.40 | +0.0 | -0.4 | -0.69 | 6.3 | -13.4 | 1.39 | 4.4 | +0.00 | -1.77 | earnings_miss |
| 12 | ARTL | -9.1 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | -0.10 | 9.1 | -32.9 | 2.78 | 0.4 | +1.25 | +0.50 | no_identifiable_cause |
| 13 | OBX | -6.8 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | -2.34 | 6.8 | -13.1 | 0.52 | 7.4 | +1.83 | -1.73 | index_or_flow |
| 14 | DBGI | -9.1 | -3.50 | +0.00 | -3.50 | +0.0 | -3.5 | -0.57 | 9.1 | -25.6 | 0.63 | 1.4 | +0.25 | -0.23 | dilution_or_going_concern |
| 15 | IPEX | -59.8 | -5.00 | +0.00 | -5.00 | +0.0 | -5.0 | -1.79 | 59.8 | -70.5 | 16.68 | 0.3 | +0.53 | -1.79 | index_or_flow |

## The names above the floor

**IPEX, −5.00 (leg 2 −5.00, leg 1 0; no `repricing` finding, so no `mechanism_in_window` question arises).**

- *What caused the fall.* It is the closing day of the business combination with GOWell Technology (GlobeNewswire, 13:30 ET). The fall has the textbook de-SPAC shape: a −4.9% gap, then −57.7% intraday, on 16.7× volume. The float is about 1.15m public shares after 7,475,610 redemptions. The sponsor and underwriter lock-up on 3,337,500 shares was terminated in the 08-31 8-K. Rights for 8,890,625 × 1/5 ≈ 1.78m shares convert on consummation.
- *What the hunt thinks the reaction got wrong.* The close prices the stock that has traded so far. It does not price the roughly 5.1m zero- or low-cost shares that first trade in full on Monday under the new symbol. Rights-arbitrage holders who redeemed and kept the rights sell whatever the price.
- *Base rate.* The number is negative, so it agrees with phase 0 rather than fighting it. The median faller is −1.00% at the next close. The ≤−40% band averages −4.00% and falls on over 15× volume −2.44%. The name has no comparable falls of its own (n=0). The hunter's own view was −6.0; only the findings sum, −5.0, is ranked.
- *Tradability.* Median 20-day turnover is **$0.3m**, near the floor. The half-spread floor estimate is 0.53%. ATR14 is 70.5%. There is no option chain, and borrow on a ~1m-share float on closing day is unlikely. **This is research, not a trade.**
- **Resolver caveat:** the ticker becomes **GOW on 2026-09-28**. If `rev_resolve.py` fetches bars by `IPEX` only, this row may resolve as missing or stale. Check it before reading the 09-25 resolve.

**DBGI, −3.50 (leg 2 −3.50, leg 1 0; no `repricing` finding).**

- *What caused the fall.* There was no news and no EDGAR filing since 09-11. The −9.1% (gap −3.3%, intraday −5.9%) came on only 0.63× volume. It continues an −83% 60-day slide at a going-concern microcap that funds itself through an open ATM. The cause is inferred from the supply pattern, not from a dated document (hunter confidence 40%).
- *What the hunt thinks the reaction got wrong.* An ATM is a flow, and the close discounts only the share count to date. In this name's dilution regime since 08-18, 9 of 12 comparable falls were followed by a lower close, with a median of −8.46%.
- *Base rate.* The number is negative, so it agrees with phase 0. **What cuts against it is the volume:** 0.63× sits in the under-2× bucket, which phase 0 puts at **+1.46%** the next session, and the −10..−7.5 drop band averages +0.59%. The hunter cut its own view from −3.5 to −2.5 for that reason; the ranked key is the −3.5 findings sum. The name's 3-year history (n=169) has a median of only −0.84%.
- *Tradability.* Median turnover is **$1.4m**, the half-spread floor 0.25% and ATR14 25.6%. There is no option chain. There is also a non-binding $77.58 a share take-private proposal, whose go-shop ends 10-05, outside the window. That is a large two-sided tail sitting under a short.

## Critical read

- **The legs.** `more_to_come_pct` carries 14 of the 15 names, from +0.3 to −5.0. `overshoot_pct` is non-zero on one name: BYND at +1.5, with a dated, document-backed `mechanism_in_window` (the end of the VWAP averaging window, per the 09-23 8-K). That is the first repricing finding in three days. It sits below the floor, and it is a single observation. Its own risk is also stated: up to 848,265 true-up shares are delivered on or about 09-28 and could be sold that day.
- **Supply again.** Every non-zero negative lands on `supply`: IPEX (de-SPAC unlock), DBGI, ARTL and NEOV (ATMs), and OBX (a 29.16m-share PIPE resale registration effective since 09-10). This is the third day running on which leg 2 means "somebody can still sell". Across the 09-22 and 09-23 runs that leg ranked with the **wrong sign** (d1 ρ −0.22, open ρ −0.33, neither significant). If it keeps doing that, sized ATM findings are the first thing to look at in the post-mortem. Do not move anything on it yet.
- **The zeros are honest and costly.** CRMT, ZTG, LONA and KLRA each have a hard dated event 2–18 days out. The window rule keeps all of them at 0, so the ranking says nothing about the names where the most is at stake. That is the design, and it is worth remembering when a zero-heavy day ranks at noise.
- **The hunt and the lean barely agree.** The rank correlation of `impact_sum` with `priced_lean_pct` is +0.06 across the 15 names. So today's ranking is not the baseline restated.
- **TRT is in the universe, and this time it really reported.** The FY2026 results 8-K and the 10-K were both filed on 2026-09-24. This is the name whose 09-17 cadence prior cleared stage E's floor without a print (see CLAUDE.md). Today's hunter treats it as day two of a post-results liquidation and finds nothing dated in the window.
- **Volume cuts against continuation on four names.** VOGX (0.23×), ZTG (0.40×), OBX (0.52×) and DBGI (0.63×) fell on under-2× volume, which phase 0 puts at +1.46% the next session. Two of those four carry negative numbers (OBX −1.0, DBGI −3.5). Both hunters shaded their own view toward zero for this reason; the key is the unshaded findings sum.
- **Rebound thesis priced against the base rate.** BYND at +1.50 is fighting the median faller's −1.00% next close. Its band (−10..−7.5, turnover $5–25m) has a cross-section prior of −0.20%. Its own 82 comparable falls have a median of −1.97% with a 34% up-rate, and the option skew pays for downside (+9.9 vol points). MEDS at +0.30 (a conference talk on 09-28) is fighting its band prior of +0.50% and its own median of −1.93%; it is a rounding error either way. Every phase-0 figure here is close-to-close, and this screen was taken at 15:04 ET.
- **Weekend window.** The scored window spans Saturday and Sunday. That is more time for an 8-K to land (CRMT's lender talks, a DBGI definitive agreement, an IPEX/GOW shell 20-F) than a weekday window gives. Hunters were told the window, but no phase-0 cut separates Friday drops.

## What it would cost to trade

The summed estimated half-spreads over the 15 names come to **13.24 points**: a mean of 0.88, a round trip of about 1.77, and one name (NEOV) UNKNOWN. The predictions have a standard deviation of **1.55 points**. So the whole spread of the day's predictions is smaller than one average round trip. The two floor-clearers trade $0.3m and $1.4m a day, with no option chain and a doubtful borrow. Phase 0 measured the gross one-session edge at ±0.35% against about 1.06 points round trip. **One session is not tradeable**, and nothing today changes that.

## Caveats every reader needs

- **The spot is the 15:04 EDT screen price, not a close.** The scored window is today's close → the 09-28 close. Phase 0's base rates are close-to-close, which is a different population. Of the worst 15 at 15:00, 86.4% are still in the worst 15 at the close, and the 15:00→close move has a mean of −0.24%, a median of 0.00% and an sd of 4.54%.
- **Short interest is the 2026-09-15 settlement**, published about eight business days late, on every name. The position carried INTO the fall cannot be observed.
- **`next_earnings_estimated` is Zacks's cadence algorithm, not a company announcement**, on every name. Several hunters say so explicitly.
- **Only two names have a chain at all**: BYND (front straddle 10.56% over 7 days, 25-delta skew +9.93, ATM spread 18.5% of mid) and NEOV (21-day straddle 26.7%, ATM spread 35% of mid, so indicative only). Stage R runs effectively anchor-less (FINDINGS §33: ρ=+0.073, p=0.45).
- **Contamination.** Hunters on TRT, BYND, ZTG and IPEX met search snippets carrying same-day or undated quotes, or an article dated 09-26. Each states that it excluded them and used no price after the screen instant.
- **Hunter concurrency was capped at 8 in this session**, so seven hunters (ARTL, DBGI, VOGX, BYND, OBX, NEOV, KLRA) started 2–5 minutes after the first eight. None was shed, and all 15 hunted the same window from the same sealed baselines.
- This stage places no orders.

---
*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.*

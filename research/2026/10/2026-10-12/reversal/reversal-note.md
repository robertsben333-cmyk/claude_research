# Stage R — reversal note — drop date 2026-10-12, window to close 2026-10-13

The screen ran intraday at **2026-10-12 15:05 EDT** while the session was still open, so the bars are not final.
- **SPY at the screen:** **−0.16%**, so these fallers are idiosyncratic and not a market day.
- **Universe:** 5,967 names screened, **47 passed the floors** ($200k median 20-day turnover, $1 price), and the worst 15 were hunted. The cap equals K, so nothing was shed.
- **Baselines:** all 15 were sealed before any hunter ran, and all 15 are rankable.
- **Conviction floor:** |impact_sum| ≥ 2.8. **No name clears it.**

**Sector concentration:** Consumer Discretionary 5 (33%), Technology 4, Health Care 3, Finance 2, Basic Materials 1. No sector is above half and the universe raises no warning. The exposure that cuts across sectors is the same as on every run since 10-02: **every non-zero negative finding is about supply.** It takes these forms:
- registered-direct paper still being sold (BIAF)
- debt-settlement shares at a fifth of spot (DAIC)
- variable-price convertible notes with registered resale (IMCC, QMLS)
- an open at-the-market offering (CD, DBGI)
- post-merger lock-up release (OPNW)

**Repeat names from 2026-10-09:** BIAF, AIFA, SDEV and IMCC were hunted again. SDEV is on its fourth appearance, sixth straight down day of its pump unwind.

The scored window is **today's close → the 2026-10-13 close**. The screen ran an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close (never fewer than 11), and the 15:00→close move was a coin flip (mean −0.24%, median 0.00%, sd 4.54%). **Phase 0's base rates below are close-to-close and this screen is not**, so they are priors from a neighbouring population, not this one.

## Answer first

- **This is a non-day.** `impact_sum` runs from **−1.50 to +1.00**.
  - Seven of 15 hunts returned zero in-window findings: AIFA, GRRR, JELD, MSGY, REAX, SDEV and SUGP.
  - Nine causes are `no_identifiable_cause`. Only DAIC (sell-the-news on its own Envoy acquisition release, 84× volume) and BIAF (the 10-08 registered direct) have a cause the hunter would put above 50% confidence.
- **Leg 1 (repricing) is empty.** `overshoot_pct` is 0.0 on all 15 names. No hunter filed a repricing finding, so no `mechanism_in_window` exists to report and nothing was promoted from opinion.
- **Leg 2 (new information) carries every non-zero number.** `more_to_come_pct` is −1.0 to −1.5 on seven names, all supply, all small. SAIQ's +1.0 is the only positive leg 2 number.
- **The one positive number, SAIQ +1.00, is not a rebound call.** The finding is that no dilution route can open inside the window: about 91% of its shares sit with a locked WISeQey/SEALSQ group, there is no ATM, and no resale registration is filed. **The base rate it argues against:** the median faller is −1.00% at the next close. The cross-section prior for SAIQ's band (−25…−15%, under $1m of turnover) is +0.27% to +0.41%. But its own volume is 14.7× normal, where phase 0 measured −2.44% over 15×. Its own hunter's scaled number is **−2.50** (abs 25, p_up 45), so the two measurements disagree in sign. Read it as "one route for a second shoe removed", not as a buy.
- **Nothing here is worth trading.** The spread of predictions across the day is 2.5 points (−1.5 to +1.0), on names with 14-day ATRs of 8% to 106%. The sum of estimated half-spreads is 4.88 points over the six names where the estimator returned a number. On the other nine (marked `*`) it floored at zero, which means the true spread is unmeasured, not that it is free. One session is not tradeable in phase 0 (gross ±0.35% a day against a ~1.06-point round trip), and the predictions are smaller than that round trip.

## Ranked table

`leg1 / leg2` = `overshoot_pct` / `more_to_come_pct`. Free controls are `−ret_d` (rank by size of fall) and `−atr14` (phase 0's best free ranker, ρ=−0.126). `*` = the half-spread estimator floored at zero, so the spread is unmeasured.

| # | ticker | fall | impact_sum | leg1 / leg2 | priced_lean | −ret_d | −atr14 | vol × | turnover (med20) | half-spread | cause |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SAIQ | -19.0% | +1.00 | +0.0 / +1.0 | -10.54% | 19.0 | -58.4 | 14.67 | $0.73m | 0.0*% | no_identifiable_cause |
| 2 | AIFA | -13.6% | +0.00 | +0.0 / +0.0 | -0.99% | 13.6 | -17.2 | 2.16 | $0.30m | 0.0*% | no_identifiable_cause |
| 3 | GRRR | -9.1% | +0.00 | +0.0 / +0.0 | +0.03% | 9.1 | -8.1 | 2.76 | $6.65m | 0.0*% | customer_or_contract_loss |
| 4 | JELD | -15.3% | +0.00 | +0.0 / +0.0 | -1.62% | 15.3 | -14.2 | 0.75 | $2.33m | 0.8848% | no_identifiable_cause |
| 5 | MSGY | -22.9% | +0.00 | +0.0 / +0.0 | +0.71% | 22.9 | -69.7 | 1.51 | $0.25m | 0.8934% | no_identifiable_cause |
| 6 | REAX | -9.1% | +0.00 | +0.0 / +0.0 | -0.26% | 9.1 | -8.4 | 0.67 | $11.77m | 0.0*% | sector_or_macro |
| 7 | SDEV | -9.8% | +0.00 | +0.0 / +0.0 | -0.09% | 9.8 | -105.7 | 0.56 | $21.92m | 0.3766% | no_identifiable_cause |
| 8 | SUGP | -14.1% | +0.00 | +0.0 / +0.0 | -1.22% | 14.1 | -19.4 | 0.69 | $0.57m | 0.0*% | no_identifiable_cause |
| 9 | BIAF | -17.7% | -1.00 | +0.0 / -1.0 | -1.41% | 17.7 | -21.8 | 0.95 | $1.67m | 0.0*% | equity_offering |
| 10 | DAIC | -20.1% | -1.00 | +0.0 / -1.0 | -2.88% | 20.1 | -21.2 | 83.75 | $0.92m | 0.8946% | corporate_action |
| 11 | OPNW | -10.0% | -1.00 | +0.0 / -1.0 | -0.18% | 10.0 | -35.8 | 0.43 | $0.76m | 0.0*% | no_identifiable_cause |
| 12 | QMLS | -17.9% | -1.00 | +0.0 / -1.0 | -5.17% | 17.9 | -18.1 | 1.78 | $2.13m | 0.0*% | sympathy |
| 13 | CD | -19.3% | -1.50 | +0.0 / -1.5 | +2.53% | 19.3 | -24.0 | 1.27 | $1.27m | 0.229% | no_identifiable_cause |
| 14 | DBGI | -9.6% | -1.50 | +0.0 / -1.5 | -0.54% | 9.6 | -19.8 | 0.21 | $1.11m | 1.5992% | no_identifiable_cause |
| 15 | IMCC | -9.8% | -1.50 | +0.0 / -1.5 | -0.45% | 9.8 | -24.8 | 0.33 | $0.60m | 0.0*% | dilution_or_going_concern |

`impact_scaled`, the hunter's second, separate measurement (v3), is in `score-report.md` and `edge-scores-scaled.json`. It is not the key and is not ranked on here.

## The negative names, two sentences each

None clears the floor. These are the names that carry a non-zero leg 2 number. Each negative number agrees with the phase 0 base rate (the median faller is −1.00%) rather than fighting it.
- **IMCC −1.50.** Third straight decay day on 0.33× volume after a resale F-3 for 170% of shares outstanding, filed 10-08 and not yet effective. The hunt says the price holds the fall but not the mechanics: the variable-price notes convert at 90% of the lowest 20-day VWAP, so today's low resets the next conversion lower.
- **DBGI −1.50.** No-news fall on 0.21× volume. An effective $100M Aegis ATM is tied to a $1.0m note payment due by 10-23, against a ~$3.4m market cap.
- **CD −1.50.** Second ~20% fall unwinding a +195% run. A $300M H.C. Wainwright ATM (about 39% of market cap) is open on an effective shelf, so any bounce can be sold into.
- **QMLS −1.00.** No company cause; labelled sympathy with CoreWeave and Nebius funding worries, at 30%. ATW convertible notes convert at 93% of the lowest 8-day VWAP, and the holder can accelerate installments on any day.
- **DAIC −1.00.** Sell-the-news on its own Envoy closing release: +30% pre-market, then −32.7% intraday on 84× volume. LHT I's 2.8M settlement shares at $0.386 exceed the 2.34M shares outstanding on 09-24.
- **BIAF −1.00.** Second leg after the 10-08 $4.0m registered direct at $6.12. Up to ~653k registered share-equivalents sit with one underwater investor, offset in part by the ATM being set to zero and a 30-day standstill.
- **OPNW −1.00.** Post-merger unwind ($8.98 → $4.03 since 09-30) on 0.43× volume. Legacy holders are rotating out; the next lock-up tranche is at day 60 (~11-29), outside the window.

## Labels that stop a reader over-trusting a number

- Every `next_earnings_estimated` date in these baselines is Zacks's cadence algorithm served by Nasdaq, **not a company announcement** (the TRT failure). Several hunters cited them only in `outside_window`.
- Short interest is FINRA's 09-30 settlement, published about eight business days later, so **the position carried into today's fall is not observable**. The change between the last two settlements is.
- No name has a usable option chain (`crumb_failed` or `unusable_chain`), so the stage ran anchor-less, the regime `archive/backtest/FINDINGS.md` §33 priced at ρ=+0.073.

## Resolution of the previous run, and the pooled record

- **2026-10-09 is not scoreable yet.** Its window closes at today's close (10-09 was a Friday), so all 15 rows are `move_pending` (`../resolve-2026-10-09.json`). Its `lean_vs_free_control_rho` is −0.21, so the lean is not the free control in disguise.
- **Pooled d1 over the twelve live runs 2026-09-22 → 2026-10-07 (178 names, 12 days):**
  - hunt `impact_sum` **ρ = −0.008, p = 0.93**
  - `neg_atr14` (free control) ρ = +0.128, p = 0.11
  - `neg_ret_d` (free control) ρ = −0.132, p = 0.075
  - leg 1 ρ = +0.028, leg 2 ρ = −0.015
  - `lean_vs_free_control_rho` −0.03
  - conviction book at the 2.8 floor, one spread: 15 legs, **−5.66% net per leg** (t −0.57) against +1.96% for shorting every name.
- **The hunt has not beaten the free controls, and on this record it has established nothing.** Only five overshoot findings with a mechanism exist in the whole pool, which is too few to say which leg carries anything. No constant was moved on any of this.

## Shed and caveats

- Nothing was shed: all 15 names were hunted. The harness allows 8 concurrent subagents, so the last seven hunters launched as slots freed. All 15 hunts were written by about 15:16 ET.
- The `requests` module was missing from the container and was installed with pip before the screen. That is an environment gap, not a code change.
- Two hunters (CD, GRRR) saw a quote of uncertain timestamp near the screen instant in a fetched page. Both excluded it and logged it.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

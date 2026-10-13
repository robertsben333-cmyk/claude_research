# Stage R — reversal note — drop date 2026-10-13, window to close 2026-10-14

The screen ran intraday at **2026-10-13 15:05 EDT** while the session was still open, so the bars are not final.
- **SPY at the screen:** **−0.04%**, so these fallers are idiosyncratic and not a market day.
- **Universe:** 5,964 names screened, **46 passed the floors** ($200k median 20-day turnover, $1 price), and the worst 15 were hunted. The cap equals K, so nothing was shed.
- **Baselines:** all 15 were sealed before any hunter ran, and all 15 are rankable.
- **Conviction floor:** |impact_sum| ≥ 2.8. **No name clears it.**

**Sector concentration:** Health Care 7 (47%), Industrials 4, Technology 2, Finance 1, Utilities 1. That is just under half and the universe raises no warning, but the seven biotech names (CUE, UPB, CRVO, BIAF, VBIO, MDCX, FTH) are close to one bet. The exposure that cuts across sectors is the same as on every run since 10-02: **every non-zero negative finding is about supply.** It takes these forms:
- variable-price convertible notes and preferred stock (ZBAO, VIVK, VBIO, DAIC)
- open at-the-market offerings (MDCX, FTH, SHIM, UPB)
- registered resale paper (BIAF, CRVO, PSNY)
- post-merger float release (OPNW)

**Repeat names from 2026-10-12:** BIAF, DAIC and OPNW were hunted again. For each it is the next leg of the same unwind.

The scored window is **today's close → the 2026-10-14 close**. The screen ran an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close (never fewer than 11), and the 15:00→close move was a coin flip (mean −0.24%, median 0.00%, sd 4.54%). **Phase 0's base rates below are close-to-close and this screen is not**, so they are priors from a neighbouring population, not this one.

## Answer first

- **This is a non-day again.** `impact_sum` runs from **−2.50 to +0.50**.
  - Only CUE returned zero in-window findings.
  - Ten causes are `no_identifiable_cause`. Five carry a cause the hunter could name:
    - CRVO: the 10-12 nfvPPA Phase 2a biomarker data, at 75% confidence
    - MDCX: the bleed after its 50:1 reverse split, at 70%
    - BIAF: the 10-08 registered direct
    - DAIC: the Envoy sell-the-news
    - VBIO, VIVK and ZBAO: dilution from convertibles
- **Leg 1 (repricing) is empty.** `overshoot_pct` is 0.0 on all 15 names. No hunter filed a repricing finding, so no `mechanism_in_window` exists to report. Several overshoot candidates were considered and filed in `outside_window` or rejected because nothing closes the gap by tomorrow's close:
  - CUE: now below its pre-rise price
  - UPB: trading near cash
  - DCX: a deep discount to the book value of its token holdings
- **Leg 2 (new information) carries every non-zero number.** `more_to_come_pct` ranges from −0.2 to −2.5, all supply.
- **The bottom of the ranking is the most specific it has been.** These names have dated, mechanical sellers whose conversion price resets lower with every down day:
  - ZBAO: 3i notes with no price floor, and an installment lookback that covers 10-14
  - VIVK: three convertible note facilities at 80% of recent prices
  - VBIO: 3i Series B and C preferred convertible into 4.3× the common
  - DAIC: notes convertible at or below $1.50 against about $2 spot, plus a closing 8-K that is due
- **The one positive number, DCX +0.50, is not a rebound call.** The finding is that an SPA standstill bars new issuance through 10-21, which removes the commonest overnight second shoe.
  - **The base rate it argues against:** the median faller does −1.00% by the next close.
  - DCX traded at 46× normal volume, and phase 0 measured −2.44% for falls on over 15× volume.
  - DCX's own last 12 comparable falls continued 10 times.
  - Its own hunter's scaled number is **−1.92** (abs 12, p_up 42). The two measurements disagree in sign, so read it as "one route removed", not a bounce.
- **Nothing here is worth trading.** The predictions span 3.0 points (−2.5 to +0.5), on names with 14-day ATRs of 8% to 61%. The estimated half-spreads sum to **7.58 points** over the ten names where the estimator returned a number. On the other five (marked `*`) it floored at zero, which means the spread is unmeasured, not free. Phase 0 found one session untradeable: a gross edge of ±0.35% a day against a round trip of about 1.06 points.

## Ranked table

`leg1 / leg2` = `overshoot_pct` / `more_to_come_pct`. The free controls are `−ret_d` (rank by size of fall) and `−atr14` (phase 0's best free ranker, ρ=−0.126). `*` means the half-spread estimator floored at zero, so the spread is unmeasured.

| # | ticker | fall | impact_sum | leg1 / leg2 | priced_lean | −ret_d | −atr14 | vol × | turnover (med20) | half-spread | cause |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DCX | -8.6% | +0.50 | +0.0 / +0.5 | -0.56% | 8.6 | -60.6 | 45.98 | $1.24m | 0.0*% | no_identifiable_cause |
| 2 | CUE | -15.7% | +0.00 | +0.0 / +0.0 | -1.30% | 15.7 | -15.1 | 0.85 | $6.94m | 0.63% | no_identifiable_cause |
| 3 | CRVO | -11.1% | -0.20 | +0.0 / -0.2 | -0.94% | 11.1 | -11.6 | 2.25 | $0.58m | 0.54% | clinical_or_binary_readout |
| 4 | FTH | -7.0% | -0.20 | +0.0 / -0.2 | -0.76% | 7.0 | -11.4 | 0.70 | $9.03m | 0.93% | no_identifiable_cause |
| 5 | UPB | -11.6% | -0.30 | +0.0 / -0.3 | -0.39% | 11.6 | -9.1 | 0.76 | $3.80m | 0.24% | no_identifiable_cause |
| 6 | SHIM | -9.2% | -0.40 | +0.0 / -0.4 | +0.72% | 9.2 | -8.0 | 1.08 | $0.31m | 0.15% | no_identifiable_cause |
| 7 | CEPL | -12.3% | -0.50 | +0.0 / -0.5 | -2.11% | 12.3 | -11.2 | 2.05 | $1.87m | 0.49% | no_identifiable_cause |
| 8 | OPNW | -17.6% | -0.50 | +0.0 / -0.5 | -0.59% | 17.6 | -42.1 | 0.58 | $0.76m | 0.0*% | no_identifiable_cause |
| 9 | PSNY | -6.7% | -0.50 | +0.0 / -0.5 | -0.77% | 6.7 | -8.9 | 1.62 | $1.74m | 0.0*% | no_identifiable_cause |
| 10 | BIAF | -10.0% | -1.00 | +0.0 / -1.0 | -0.93% | 10.0 | -24.0 | 3.18 | $1.59m | 0.0*% | equity_offering |
| 11 | MDCX | -7.1% | -1.00 | +0.0 / -1.0 | +0.01% | 7.1 | -23.3 | 0.87 | $0.44m | 0.60% | corporate_action |
| 12 | DAIC | -7.9% | -1.80 | +0.0 / -1.8 | -0.61% | 7.9 | -22.1 | 6.01 | $0.93m | 1.13% | corporate_action |
| 13 | VBIO | -7.7% | -2.00 | +0.0 / -2.0 | -0.71% | 7.7 | -34.4 | 0.69 | $0.54m | 1.32% | dilution_or_going_concern |
| 14 | VIVK | -15.7% | -2.50 | +0.0 / -2.5 | +0.78% | 15.7 | -58.5 | 8.21 | $0.43m | 0.27% | dilution_or_going_concern |
| 15 | ZBAO | -27.6% | -2.50 | +0.0 / -2.5 | -1.84% | 27.6 | -49.1 | 1.69 | $0.79m | 1.28% | dilution_or_going_concern |

`impact_scaled`, the hunter's second and separate measurement (v3), is in `score-report.md` and `edge-scores-scaled.json`. It is not the key and nothing here is ranked on it.

## The largest negative names, two sentences each

None clears the floor. Each negative number agrees with the phase 0 base rate (the median faller is −1.00%) rather than fighting it.
- **ZBAO −2.50.** This is the second session after a 1-for-50 reverse split, with no news. The 3i convertible notes lost their floor price on 09-17 and convert at 92% of the lowest 10-day price; the next installment is 10-17, so the holder sells inside the window. A resale registration of about 180% of shares outstanding is also effective, held by PIPE buyers about 91% underwater.
- **VIVK −2.50.** This follows a 1-for-15 split on 10-05, and on 10-06 J.J. Astor converted into about 21% of the post-split share count. Three convertible note facilities are still converting at prices that reset lower after every down day, and nothing sourced shows them finished.
- **VBIO −2.00.** 3i's Series B and C preferred convert into about 8.5M shares against 1.95M common. The common count rose 51% in three weeks, and 3i bought more Series B on 10-07.
- **DAIC −1.80.** This is day two of the sell-the-news unwind after the Envoy closing release. Notes convertible at or below $1.50 can be sold into the window. The Envoy closing 8-K, which carries the Blink note's conversion terms, is due between 10-13 and 10-16.

## Labels that stop a reader over-trusting a number

- Every `next_earnings_estimated` date in these baselines is Zacks's cadence algorithm served by Nasdaq, **not a company announcement** (the TRT failure). The hunters cited them only in `outside_window`.
- Short interest is FINRA's 09-30 settlement, published about eight business days later, so **the position carried into today's fall is not observable**. The change between the last two settlements is observable.
- No name has a usable option chain, so the stage ran without an option anchor. `archive/backtest/FINDINGS.md` §33 priced that regime at ρ=+0.073.
- Two hunters inferred the cause rather than reading it in a source: VIVK (note-holder selling) and SHIM (a possible ATM draw). Both say so in their files.

## Resolution of the previous runs, and the pooled record

- **2026-10-12 is not scoreable yet.** Its window closes at today's close, so all 15 rows are `move_pending` (`../resolve-2026-10-12.json`). Its `lean_vs_free_control_rho` is −0.29, so its lean is not the free control in disguise.
- **2026-10-09 is now resolved at d1** (`../resolve-2026-10-09.json`, 15 names). On one day it established nothing:
  - hunt ρ **+0.231** (p 0.41)
  - `neg_ret_d` ρ +0.246 (p 0.37)
  - `neg_atr14` ρ −0.139 (p 0.61)
  - `lean_vs_free_control_rho` −0.21
- **Pooled d1 over the 13 live runs 2026-09-22 → 2026-10-09** (193 names; `../resolve-pooled-0922-1009.json`):
  - hunt `impact_sum` **ρ = +0.011, p = 0.88**
  - `neg_atr14` ρ = +0.107, p = 0.15
  - `neg_ret_d` ρ = −0.102, p = 0.16
  - leg 1 ρ = +0.048, leg 2 ρ = +0.000
  - `lean_vs_free_control_rho` −0.04
  - The resolver's conviction book (floor 3.0 as printed, no cost) has 16 legs at **−4.81% per leg** (t −0.53).
  - Overshoot findings with a mechanism: 7 in the whole pool, mean move −3.54%.
- **The hunt has not beaten the free controls, and on this record it has established nothing.** Seven repricing findings are too few to say which leg carries anything. No constant was moved.

## Shed and caveats

- Nothing was shed: all 15 names were hunted. The harness allows 8 concurrent subagents, so the last seven hunters launched as slots freed. All 15 hunts were written by about 15:13 ET.
- The `requests` module was again missing from the container and was installed with pip before the screen. That is an environment gap, not a code change.
- CUE's hunter excluded a "live" $25.79 quote it judged an unreliable widget. No hunter used a price dated after the screen instant.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

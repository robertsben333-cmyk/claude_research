# Stage R — reversal note — drop date 2026-10-07, window to close 2026-10-08

Screened intraday at **2026-10-07 15:05 EDT** with the session still open, so the bars are not final. SPY at the screen was **−0.23%**. 5,962 names were screened, **65 passed the floors**, and the worst 15 were hunted. All 15 baselines sealed (19:05:56 UTC) before any hunter ran, and all 15 are rankable. **No name clears the conviction floor (|impact_sum| ≥ 2.8).**

**Sector concentration:** Health Care 5 of 15 (33%), Consumer Discretionary 3, Technology 2, Miscellaneous 2, Industrials 1, Energy 1, Finance 1. No sector is above half and the universe file raises no warning. As on 10-02, 10-05 and 10-06, the shared exposure cuts across sectors: **every non-zero leg-2 finding but two is about supply** (ATMs, an equity line, de-SPAC rights shares, an IPO lock-up, an S-8/F-3 shelf). The two exceptions are AUUD (a promised CEO letter) and PMVP (a lock-up that *prevents* supply).

**Repeat names:** MKDW and SDEV were also hunted on 10-06. ALMR, YFOR, ABSI, AUUD, CBAT, PMVP, DFDV, GLND, NCT and XPON are on at least their second straight down day.

The scored window is **today's close → 2026-10-08 close**. The screen ran an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close, and the 15:00→close move was a coin flip (mean −0.24%, median 0.00%). **Phase 0's base rates below are close-to-close and this screen is not**, so read them as priors from a neighbouring population.

## Answer first

- **Nothing clears the floor. Today is a non-day for this stage.** `impact_sum` runs from **−2.00 to +2.00**, and 11 of 15 names sit inside −1.0…+0.3. Four hunts returned zero findings (CBAT, GLND, SDEV, XPON) and eight causes are `no_identifiable_cause`.
- **Leg 1 (repricing) produced nothing: `overshoot_pct` is 0 on all 15 names.** No hunter found a `mechanism_in_window` that closes a gap before the next close, so no overshoot is promoted. Every non-zero number is leg 2 (`more_to_come_pct`).
- **The only positive number of note is AUUD +2.00** (p72 of the Opus 5.5 reference): a CEO letter the company said on 10-06 it would issue "later this week". It lands inside the window only if it goes out Thursday 10-08, so the hunter sized it at about half. **Base rate it argues against:** the median faller is −1.00% next session. AUUD's own 150 comparable falls have a median of −0.66% (42.7% up). Its band prior (−10..−7.5 fall, <$1m turnover) is +0.50%, and the under-2× volume cut (0.75×) is +1.46%. The volume prior is on its side and its own history is not. Its `impact_scaled` is only +0.56.
- **The most negative names are supply stories**, none at the floor:
  - **YFOR −2.00:** a $20m Spartan ATM (filed 10-05) against about $7.8m of Class A float. The same agent sold an identical $20m facility to completion earlier in 2026.
  - **SAIQ −2.00:** a de-SPAC listed 10-02. Its float is about 96% rights-conversion shares on a near-zero cost basis, and it fell on 18× volume. Its own history is only n=4.
  - **NCT −1.50:** an effective S-8 and a $200M F-3 after two reverse splits.
  - **MKDW −1.50:** a $100m ATM against about $36m of equity, hunted for the second day running.
- **SDEV, the 7.9× volume name, is a zero.** It is day three after a Fugazi short report. Its 212.9m-share resale S-3 is not yet effective, so the hunter placed it outside the window (sized −4 there).

## Resolution: has the hunt beaten a free control?

**No reversal run has beaten a free control yet. This run establishes nothing either, because nothing cleared the floor.**

- **2026-10-06 run:** all 14 names are pending, because its window closes at today's close (`../resolve-2026-10-06-pending.json`).
- **2026-10-05 run, now resolved** (`../resolve-2026-10-05.json`, 15 names, d1). `lean_vs_free_control_rho` is −0.18, so the lean is not the free control in disguise.

  | ranker | ρ at d1 | perm p |
  | --- | --- | --- |
  | `impact_sum` (the hunt) | +0.344 | 0.21 |
  | `neg_atr14` (free control) | +0.250 | 0.37 |
  | `neg_ret_d` (free control) | −0.093 | 0.76 |

  The conviction cut put the sign right on 6 of 10 names. **One day of 15 names is noise.**
- **Pooled d1, every resolved live run 09-21 → 10-05** (`../resolve-pooled-0921-1005.json`: 11 runs, 149 rankable names, 10 days; synthetic 09-11 excluded). `lean_vs_free_control_rho` pooled is −0.00.

  | ranker | ρ at d1 | perm p |
  | --- | --- | --- |
  | `impact_sum` (the hunt) | **+0.053** | 0.55 |
  | `neg_atr14` (free control) | +0.124 | 0.14 |
  | `neg_ret_d` (free control) | −0.147 | 0.08 |
  | leg 1 alone | +0.062 | 0.48 |
  | leg 2 alone | +0.038 | 0.67 |

  **The hunt has not beaten `neg_atr14` and has established nothing.**
  - The pooled conviction book was 16 legs, **+2.41% gross per leg, t 0.56**, with a CI of [−5.7, +10.9].
  - This pool mixes hunter prompt versions, so it is a stage-level reading, not a judgement of any one version (`rev.v7` today).
  - `neg_ret_d` is negative again: the deeper fallers kept falling harder, which is phase 0's direction.

## Ranked table

How to read the columns:
- Leg columns are the hunters' finding sums split by `leg`.
- Lean = `priced_lean_pct`.
- Band prior is phase 0's cross-section expectation, close to close.
- Half-spread is Corwin-Schultz over the 21 sessions before the drop, a floor; **"unk" means the estimator failed, never narrow**.
- Fall % is the sealed `ret_d` at the screen.

| # | ticker | fall % | vol× | impact_sum | leg1 repricing | leg2 new info | p_up | abs_move | lean | −ATR14 | turnover $m | half-spread % | band prior % | own-history median next % | cause | n findings |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AUUD | -8.3 | 0.75 | +2.00 | +0.00 | +2.00 | 54 | 7.0 | -0.15 | -18.5 | 0.3 | 0.17 | +0.50 | -0.66 (n 150) | management_or_governance | 1 |
| 2 | PMVP | -6.8 | 0.74 | +0.30 | +0.00 | +0.30 | 49 | 4.0 | -1.32 | -9.6 | 0.9 | 0.97 | -1.04 | -1.54 (n 63) | no_identifiable_cause | 1 |
| 3 | CBAT | -9.7 | 0.60 | +0.00 | +0.00 | +0.00 | 50 | 6.0 | +2.08 | -14.2 | 0.6 | 0.23 | +0.50 | 3.31 (n 35) | no_identifiable_cause | 0 |
| 4 | GLND | -9.3 | 0.30 | +0.00 | +0.00 | +0.00 | 50 | 9.5 | -1.16 | -39.8 | 34.1 | 1.05 | +0.30 | -2.29 (n 25) | short_report | 0 |
| 5 | SDEV | -14.0 | 7.94 | +0.00 | +0.00 | +0.00 | 50 | 11.0 | -0.14 | -50.3 | 3.1 | 0.95 | -0.33 | 0.0 (n 57) | short_report | 0 |
| 6 | XPON | -6.8 | 0.41 | +0.00 | +0.00 | +0.00 | 50 | 5.5 | -1.11 | -11.5 | 0.2 | 1.17 | -1.04 | -1.17 (n 171) | no_identifiable_cause | 0 |
| 7 | ABSI | -9.8 | 1.09 | -0.30 | +0.00 | -0.30 | 51 | 5.0 | +0.54 | -10.2 | 36.2 | 0.20 | +0.30 | 0.72 (n 62) | no_identifiable_cause | 1 |
| 8 | ACRS | -7.2 | 2.34 | -0.30 | +0.00 | -0.30 | 46 | 5.5 | -0.76 | -11.7 | 14.9 | 0.47 | -1.73 | 0.0 (n 73) | no_identifiable_cause | 2 |
| 9 | DFDV | -6.3 | 1.03 | -0.30 | +0.00 | -0.30 | 48 | 6.0 | -0.76 | -12.9 | 11.2 | 0.58 | -1.73 | 0.0 (n 195) | sector_or_macro | 1 |
| 10 | GRML | -9.9 | 0.34 | -0.50 | +0.00 | -0.50 | 47 | 9.0 | +0.01 | -58.3 | 33.6 | unk | +0.30 | -0.22 (n 131) | no_identifiable_cause | 3 |
| 11 | ALMR | -12.5 | 1.66 | -1.00 | +0.00 | -1.00 | 45 | 6.0 | -2.07 | -11.0 | 13.7 | 0.54 | -0.29 | -4.84 (n 3) | no_identifiable_cause | 1 |
| 12 | MKDW | -16.5 | 1.33 | -1.50 | +0.00 | -1.50 | 42 | 10.0 | -2.27 | -59.9 | 0.3 | 1.00 | +0.34 | -4.3 (n 37) | no_identifiable_cause | 1 |
| 13 | NCT | -11.3 | 3.24 | -1.50 | +0.00 | -1.50 | 40 | 12.0 | -0.66 | -67.2 | 0.8 | unk | +0.40 | -1.49 (n 57) | no_identifiable_cause | 1 |
| 14 | SAIQ | -29.3 | 18.32 | -2.00 | +0.00 | -2.00 | 45 | 30.0 | -15.00 | -58.1 | 0.5 | unk | -0.17 | -32.29 (n 4) | index_or_flow | 1 |
| 15 | YFOR | -11.5 | 0.73 | -2.00 | +0.00 | -2.00 | 40 | 7.0 | -0.86 | -16.6 | 0.4 | 0.55 | +0.40 | -1.84 (n 83) | equity_offering | 1 |

## Floor-clearers

None. With no floor-clearer there is no `mechanism_in_window` to report, and none of the 15 names filed a repricing finding at all.

## What the day would cost to trade

- **Prediction spread:** the predictions span **4.0 points** (−2.00 to +2.00), and the middle eleven span 1.3.
- **Spread cost:** the known Corwin-Schultz half-spreads sum to **7.9 points over the 12 names where the estimator returned a value**. GRML, NCT and SAIQ are "unk", so the sum is a floor, and it is blind to the widening the drop itself causes.
- **Bottom line:** phase 0 measured the one-session gross edge at about ±0.35% against about 1.06 points of round-trip spread. **The spread is larger than anything this ranking separates**, and there is no floor book to trade.

## Labels a reader must carry

- **`next_earnings_estimated`** in every baseline is Zacks's cadence algorithm, not a company announcement (the TRT failure). Where the hunters cite one (ALMR, XPON, GRML, ACRS, ABSI, DFDV, SDEV), it is filed outside the window as an estimate.
- **Short interest** is published about eight business days after settlement. Every figure the hunters quote is the 09-15 settlement, so the position carried into this fall is not observable.
- **ALMR's cause is an inference.** Its IPO lock-up ends around 10-13, so it is outside the window. The −1.0 is "the pre-expiry seller is not finished", and no document shows that selling.
- **The AUUD letter's date is unknown.** "Later this week" admits 10-08 or 10-09, and only the former is in the window.
- **SAIQ's float is derived**, from the CAC vote 8-K and the IPO description of securities. It is not a disclosed number. The 424B3 holding the lock-up terms exceeded the fetch limit.
- **Unreachable sources:**
  - EDGAR full-text search returned HTTP 500 to the GLND hunter.
  - The Nasdaq short-interest API returned 503 to SDEV and NCT.
  - Several IR pages returned 503 (ALMR, ACRS, ABSI, NCT).

## Shed

- Nothing was shed. Hunters ran 8 at a time (the session's concurrency cap) and all 15 hunts were written by 19:13 UTC (15:13 ET).
- The container lacked `requests` and it was pip-installed before the screen; the screen ran at 15:05 ET.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.* This stage places no orders.

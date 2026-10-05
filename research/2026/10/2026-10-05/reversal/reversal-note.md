# Stage R — reversal note — drop date 2026-10-05, window to close 2026-10-06

Screened intraday at **2026-10-05 15:04 EDT**, with the session still open, so the bars are not final. SPY on the day at the screen was **+0.83%**. 5,977 names were screened and **36 passed the floors**. All 15 of the worst were hunted and all 15 are rankable. **One name clears the conviction floor (|impact_sum| ≥ 2.8): WHLR −3.00.**

**Sector concentration:** Health Care 6 of 15 (40%), Finance 3, Technology 2, Consumer Staples 2, Real Estate 1, Consumer Discretionary 1. No sector is above half, so the universe file raises no warning. The real shared exposure is the same as on 10-02: every non-zero finding except two of MEDS's (short interest and press-release cadence) is about **issuer or holder supply**. That covers redemptions settled in stock, warrant shares, underwater registered-direct holders, a resale registration and possible private placements. The scorer cannot see this.

**This was a mild day for falls.** The 15th-worst name was down only −4.5% at the screen, and 10 of 15 were down less than 10%. Phase 0 counts only falls of 5% or more, so **the −4.5 to −5% falls (SEAT, GRML, GCTK) are at or just below the edge of the population its base rates describe.**

**Five of today's fifteen were also hunted on 10-02**: WHLR, WCT, HOST, GCTK and GRML. They are repeat fallers, the same names in the same supply spirals. A reader holding the 10-02 ranking holds part of this one already.

The scored window is **today's close → 2026-10-06 close**. The screen ran an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close, and the 15:00→close move was a coin flip (mean −0.24%, median 0.00%). **Phase 0's base rates below are close-to-close and this screen is not**, so read them as priors from a neighbouring population, not this one.

## Answer first

- **One floor-clearer, WHLR −3.00, short side, leg 2 (supply). It has no leg-1 finding.**
- **Leg 1 found nothing for the third run running.** There are zero `repricing` findings in 15 hunts, and every `overshoot_pct` is 0. No overshoot is promoted here.
- **Seven of fifteen hunts are non-results or close to it.** BGS, MAAS, NNNN, PAAI and SEAT returned no findings at all. GRML (+0.25) and MEDS (+0.25) are offsetting findings that net to near zero. In 13 of 15 names the cause of the fall is `no_identifiable_cause`. That is the honest answer on a day when most of these names fell 5–7% on ordinary or thin volume with nothing filed.
- **The spread is narrow and leans down.** `impact_sum` runs from **−3.00 to +0.50**. The positive numbers are "no supply can land in the window" findings, not rebound theses: VOGX has no shelf and HOST and GRML have lock-ups or no-financing covenants. Every one of them carries a negative `impact_scaled`.
- **`overshoot_has_mechanism` is still uninformative.** Eight hunters set it to `true` while filing no repricing finding: VOGX, HOST, GRML, BGS, NNNN, CRDL, GCTK and WCT. This is the same hunter-contract defect recorded on 10-02. It is recorded again in the run log, and nothing here relies on it.
- **No reversal run has beaten a free control yet.**
  - The **2026-10-01 run is now resolved at d1** (15 names, 0 pending; `../resolve-2026-10-01.json`).
    - `impact_sum` read **ρ +0.324 (perm p 0.24)**. The free controls read `neg_atr14` +0.196 (p 0.50), `neg_vol_spike` +0.296, `neg_ret_d` **−0.614 (p 0.018)** and `neg_run_up_20d` −0.004. The baseline's own lean read +0.163.
    - `lean_vs_free_control_rho` is **0.029**, so the lean is not the free control in disguise.
    - Leg 2 alone read +0.324, the whole result. Leg 1 had no names, so it is not rankable.
    - The conviction book was one short: ONEN returned **+2.60% gross (+2.24% net of one spread)**, against −0.87% for shorting everything.
  - **On 10-01 the hunt beat every free control at d1, on one day, at p 0.24.** That is not significant, and one leg is one observation. It is the first day on which the hunt led `neg_atr14`; on 09-29 and 09-30 it lost to it. Three days and fifteen names each establishes nothing yet.
  - **`neg_ret_d` ranked at −0.61 on 10-01**, so the deepest fallers kept falling hardest. That is phase 0's "deeper falls continue harder" in one day's cross-section.
  - The **2026-10-02 run is pending**: its window closes at today's close (`../resolve-2026-10-02.json`, all 15 `move_pending`).

## Ranked table

How to read the columns:
- The two leg columns are the hunters' own finding sums, split by `leg`. Lean = `priced_lean_pct`.
- Band prior is phase 0's cross-section expectation for the name's drop band and turnover band, close to close.
- Half-spread is Corwin-Schultz, which is a floor. **"unk" means the estimator returned 0 or failed. It never means narrow.**
- `mech?` is the hunter's `overshoot_has_mechanism` flag, which is uninformative where leg 1 is 0 (see above).
- Fall % is the sealed `ret_d` at the screen.

| # | ticker | fall % | impact_sum | leg1 repricing | leg2 new info | overshoot_pct | more_to_come_pct | p_up | abs_move | lean | −ATR14 | vol× | turnover $m | half-spread % | band prior % | cause | mech? | n findings |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | VOGX | -5.1 | +0.50 | +0.00 | +0.50 | +0.0 | +0.5 | 45 | 8.0 | -4.19 | -22.0 | 0.40 | 3.3 | 0.67 | -1.77 | no_identifiable_cause | True | 1 |
| 2 | HOST | -15.7 | +0.30 | +0.00 | +0.30 | +0.0 | +0.3 | 44 | 9.0 | -2.67 | -49.0 | 0.67 | 1.1 | 0.07 | -0.39 | no_identifiable_cause | True | 1 |
| 3 | GRML | -4.9 | +0.25 | +0.00 | +0.25 | +0.0 | +0.2 | 48 | 9.0 | -1.12 | -42.8 | 1.01 | 23.1 | unk | -1.73 | no_identifiable_cause | True | 2 |
| 4 | MEDS | -6.8 | +0.25 | +0.00 | +0.25 | +0.0 | +0.2 | 45 | 9.0 | -2.35 | -50.5 | 0.59 | 3.3 | 0.84 | -1.77 | no_identifiable_cause | False | 3 |
| 5 | BGS | -6.7 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 3.0 | -1.41 | -5.4 | 1.62 | 6.1 | 0.13 | -1.73 | no_identifiable_cause | True | 0 |
| 6 | MAAS | -7.4 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 6.0 | -1.66 | -16.6 | 0.97 | 2.9 | 0.80 | -1.77 | no_identifiable_cause | False | 0 |
| 7 | NNNN | -13.5 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 7.5 | +1.48 | -11.9 | 0.31 | 1.5 | 1.32 | -0.33 | no_identifiable_cause | True | 0 |
| 8 | PAAI | -5.6 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 5.0 | -0.45 | -49.2 | 0.46 | 0.8 | unk | -1.04 | no_identifiable_cause | False | 0 |
| 9 | SEAT | -4.5 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 4.0 | -0.99 | -8.1 | 1.65 | 0.4 | 0.61 | -1.04 | no_identifiable_cause | False | 0 |
| 10 | NCPL | -5.7 | -0.50 | +0.00 | -0.50 | +0.0 | -0.5 | 48 | 6.5 | -0.76 | -27.0 | 0.09 | 5.5 | 0.24 | -1.73 | no_identifiable_cause | False | 1 |
| 11 | CRDL | -7.1 | -0.60 | +0.00 | -0.60 | +0.0 | -0.6 | 47 | 4.5 | -0.64 | -8.6 | 2.31 | 2.3 | 0.45 | -1.77 | no_identifiable_cause | True | 1 |
| 12 | GCTK | -5.0 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | 42 | 8.0 | -1.53 | -28.2 | 0.72 | 0.4 | unk | -1.04 | dilution_or_going_concern | True | 1 |
| 13 | WCT | -22.5 | -1.00 | +0.00 | -1.00 | +0.0 | -1.0 | 45 | 15.0 | -2.97 | -94.7 | 1.11 | 7.0 | 0.78 | -0.35 | no_identifiable_cause | True | 1 |
| 14 | SGRX | -11.1 | -2.00 | +0.00 | -2.00 | +0.0 | -2.0 | 44 | 9.0 | +0.17 | -21.2 | 10.09 | 0.3 | 1.19 | +0.40 | no_identifiable_cause | False | 1 |
| 15 | WHLR | -23.7 | -3.00 | +0.00 | -3.00 | +0.0 | -3.0 | 40 | 14.0 | -2.46 | -96.8 | 3.27 | 0.9 | unk | +0.34 | dilution_or_going_concern | False | 1 |

## The floor-clearer: cause, what the reaction missed, and the base rate

- **WHLR −3.00** (−23.7% at the screen, 3.27× volume, ATR14 96.8%).
  - **Cause:** today is the **Series D Holder Redemption Date**, the 37th monthly one. Redemptions are settled in **new common at a 10-day reference VWAP**. The hunter reconstructed that VWAP at roughly $3.5–4.5 against a $1.58 spot, which means many more shares per dollar redeemed. It continues a dilution spiral: Series B → common 3(a)(9) exchanges on Sep 2, 8 and 23, a 1-for-9 reverse split effective Sep 21, and a 60-day return of −97%. 10-02's hunt flagged this same redemption date at −3.00.
  - **What it missed:** the 8-K reporting the shares issued in this round is expected **before the 10-06 open**, on the Sep 9 precedent. The recipients can sell inside the window. The share count is not yet public, and the reference VWAP is the hunter's reconstruction, not a published number, so the finding is capped at −3 (range −10 to +1).
  - **Mechanism in window:** leg 2 only (a dated supply event). There is no leg-1 finding, so **there is no repricing `mechanism_in_window`**.
  - **Base rate:** this is a short-side number, so it argues with the drift rather than against it. The −25..−15 band prior is **+0.34%** (<$1m turnover band +0.41%), and phase 0's −25..−15 band averaged +0.27% next session. The name's own 68 comparable falls had a **median next close of −4.63%** and rose 38.2% of the time. Volume of 3.27× is between phase 0's under-2× (+1.46%) and over-15× (−2.44%) cuts.

## Names near the floor (not floor-clearers, stated for context)

- **SGRX −2.00** (−11.1%, **10.1× volume**, turnover of about 85% of the share count in one day). It is the third heavy-volume fall in four sessions. The finding is an inferred, undated warrant and debenture overhang ($14.5m of convertible debentures against about a $2.1m market cap). Its band prior is +0.40%, and the volume cut argues the same way as the finding.
- **WCT −1.00 / GCTK −1.00.** Both are underwater or in-profit offering holders with no lock-up. WCT is the third leg of a post-pump collapse (−79% on 10-01). GCTK's 43.4m-share resale S-1 is not yet effective, so it is filed outside the window.

## What the day would cost to trade

- **Prediction spread:** the predictions span **3.5 points**, from −3.00 to +0.50.
- **Whole-day spread cost:** the known Corwin-Schultz half-spreads sum to **7.1 points over the eleven names where the estimator returned a value**. Four names are "unk", so that sum is a floor.
- **Floor book:** WHLR's spread is "unk". It trades about $0.9m a day, and a short in it is almost certainly hard to borrow.
- **Bottom line:** phase 0 measured the one-session gross edge at about ±0.35% against ~1.06 points of round-trip spread. **On this day the spread is larger than anything the ranking separates, more so than on 10-02.**

## Labels a reader must carry

- **`next_earnings_estimated`** in every baseline is Zacks's cadence algorithm, not a company announcement. That is the TRT failure. Several hunters cited such dates (SGRX, PAAI, SEAT, CRDL), and all of them filed those dates as estimates outside the window.
- **Short interest** is published about eight business days after settlement. Every figure the hunters quote is the 09-15 settlement, so the position carried into this fall is not observable. Nasdaq's short-interest API returned 503 to the PAAI and BGS hunters.
- **CRDL's `pre_lessons` is not a strict freeze.** The hunter opened LESSONS.md before writing the draft into the file. LESSONS.md is empty, so the numbers are equal either way.

## Shed

Nothing was shed. All 15 names were hunted. Hunters ran 8 at a time (the session's concurrency cap), and all 15 hunts were written by 19:11 UTC.

**This stage places no orders, and nothing here moves a floor, weight or horizon.**

---

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._

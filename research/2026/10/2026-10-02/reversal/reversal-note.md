# Stage R — reversal note — drop date 2026-10-02, window to close 2026-10-05

Screened intraday at **2026-10-02 15:04 EDT**, with the session still open, so the bars are not final. SPY on the day at the screen was **+0.69%**. 5,999 names were screened and **50 passed the floors**. All 15 of the worst were hunted and all 15 are rankable. **Four names clear the conviction floor (|impact_sum| ≥ 2.8), and all four are negative**: JAGX −6.00, AKAN −3.50, GCTK −3.00 and WHLR −3.00.

**Sector concentration: Health Care is 8 of 15 (53%).** That is above half, so the universe file flags the day as **one bet, not fifteen**. The pattern under the sector label is the stronger correlation. Ten of the eleven names with findings rest only on live issuer or holder **supply**: an open ATM, variable-price convertibles, a firm-commitment F-1, monthly redemptions settled in stock, an equity line, a distributing holder, or post-offering holders sitting on gains. The eleventh, NBTX, is the absence of supply. The scorer cannot see this shared exposure.

The scored window is **today's close → 2026-10-05 close**. That spans a weekend, so it is one session, not one calendar day. The screen ran an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close, and the 15:00→close move was a coin flip (mean −0.24%, median 0.00%). **Phase 0's base rates below are close-to-close and this screen is not**, so read them as priors from a neighbouring population, not this one.

## Answer first

- **Four floor-clearers, all short-side, all leg 2 (supply), none with a leg-1 finding.**
- **Leg 1 found nothing again: zero `repricing` findings in 15 hunts, and every `overshoot_pct` is 0.** Several candidate overshoots went to `outside_window` because no mechanism closes them by the 10-05 close, so none is promoted here:
  - **FHTX:** trades at or below net cash after the Lilly exit.
  - **NKTR:** the two-day −28% on durability data.
  - **NBTX:** the CFO handover.
  - **USDEW:** no cause found.
- **A data-quality note on `overshoot_has_mechanism`.** Eight hunters set it to `true` while filing no repricing finding and `overshoot_pct` 0: HOST, NBTX, GLND, FHTX, TRDA, USDEW, SWMR and GCTK. With nothing to attach it to, the flag carries no information on those rows, and `rev_resolve.py`'s `by_overshoot_mechanism` split will mis-bucket them. This is recorded as a hunter-contract defect in the run log, and nothing here relies on it.
- **The whole day leans down and the spread is narrow.** `impact_sum` runs from **−6.00 to +0.50**. The two positives (HOST, NBTX, each +0.5) are "no supply can land in the window" findings, not rebound theses.
- **No reversal run has beaten a free control yet.**
  - The **2026-09-30 run is now resolved at d1** (15 names, 0 pending; `../resolve-2026-09-30.json`).
  - `impact_sum` read **ρ +0.160 (perm p 0.57)**, against `neg_atr14` **+0.271** (p 0.33), `neg_vol_spike` +0.296, `neg_ret_d` +0.014 and `neg_run_up_20d` −0.529. The baseline's own lean read **+0.349** (p 0.21), better than the hunt.
  - `lean_vs_free_control_rho` is **0.004**, so the lean is not the free control in disguise.
  - Leg 2 alone read +0.176. Leg 1 had one name, so it is not rankable.
  - The conviction book was one short: CDT returned **+8.09%** on the short, against +2.00% for shorting everything. One leg is one observation.
  - **The hunt lost to `neg_atr14` on 09-30, as it did on 09-29. A run that does not beat the free controls has established nothing.**
  - The **2026-10-01 run is pending**: its window closes at today's close.

## Ranked table

How to read the columns:
- The two leg columns are the hunters' own finding sums, split by `leg`. Lean = `priced_lean_pct`.
- Band prior is phase 0's cross-section expectation for the name's drop band and turnover band, close to close.
- Half-spread is Corwin-Schultz, which is a floor. **"unk" means the estimator returned 0 or failed. It never means narrow.**
- `mech?` is the hunter's `overshoot_has_mechanism` flag, which is uninformative where leg 1 is 0 (see above).
- Fall % is the sealed `ret_d` at the screen.

| # | ticker | fall % | impact_sum | leg1 repricing | leg2 new info | overshoot_pct | more_to_come_pct | p_up | abs_move | lean | −ATR14 | vol× | turnover $m | half-spread % | band prior % | cause | mech? | n findings |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HOST | -7.2 | +0.50 | +0.00 | +0.50 | +0.0 | +0.5 | 42 | 9.0 | -1.59 | -42.1 | 1.57 | 1.1 | 0.23 | -1.77 | no_identifiable_cause | True | 1 |
| 2 | NBTX | -8.5 | +0.50 | +0.00 | +0.50 | +0.0 | +0.5 | 53 | 5.5 | +0.56 | -8.4 | 1.64 | 4.5 | unk | -0.23 | management_or_governance | True | 1 |
| 3 | GLND | -15.5 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 12.0 | +3.12 | -25.8 | 1.11 | 21.3 | 1.22 | -0.35 | short_report | True | 0 |
| 4 | NKTR | -7.1 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 5.0 | +0.23 | -10.5 | 1.72 | 78.2 | 0.11 | -1.24 | clinical_or_binary_readout | False | 0 |
| 5 | FHTX | -29.8 | -0.50 | +0.00 | -0.50 | +0.0 | -0.5 | 47 | 12.0 | +0.99 | -17.9 | 4.57 | 1.5 | 0.17 | -0.90 | clinical_or_binary_readout | True | 1 |
| 6 | TRDA | -6.8 | -0.50 | +0.00 | -0.50 | +0.0 | -0.5 | 48 | 4.0 | -0.86 | -7.6 | 0.81 | 2.3 | 0.37 | -1.77 | no_identifiable_cause | True | 1 |
| 7 | USDEW | -13.2 | -0.50 | +0.00 | -0.50 | +0.0 | -0.5 | 52 | 12.0 | +5.67 | -27.2 | 1.02 | 0.7 | 2.84 | +0.40 | no_identifiable_cause | True | 1 |
| 8 | SWMR | -6.1 | -0.90 | +0.00 | -0.90 | +0.0 | -0.9 | 45 | 7.0 | -2.10 | -17.6 | 1.05 | 24.3 | 1.44 | -1.73 | no_identifiable_cause | True | 2 |
| 9 | GRML | -13.8 | -1.10 | +0.00 | -1.10 | +0.0 | -1.1 | 47 | 14.0 | -0.52 | -39.8 | 1.52 | 9.0 | unk | -0.29 | dilution_or_going_concern | False | 3 |
| 10 | LGHL | -5.5 | -2.00 | +0.00 | -2.00 | +0.0 | -2.0 | 44 | 10.0 | -0.65 | -38.5 | 1.47 | 0.5 | 1.66 | -1.04 | dilution_or_going_concern | False | 1 |
| 11 | WCT | -25.1 | -2.00 | +0.00 | -2.00 | +0.0 | -2.0 | 44 | 18.0 | -2.41 | -82.9 | 2.69 | 7.0 | 0.78 | -0.87 | no_identifiable_cause | False | 1 |
| 12 | GCTK | -17.0 | -3.00 | +0.00 | -3.00 | +0.0 | -3.0 | 42 | 11.0 | -0.91 | -28.7 | 2.10 | 0.3 | unk | +0.34 | dilution_or_going_concern | True | 3 |
| 13 | WHLR | -6.5 | -3.00 | +0.00 | -3.00 | +0.0 | -3.0 | 40 | 12.0 | -2.05 | -54.3 | 0.82 | 0.6 | unk | -1.04 | dilution_or_going_concern | False | 1 |
| 14 | AKAN | -11.8 | -3.50 | +0.00 | -3.50 | +0.0 | -3.5 | 42 | 8.0 | -0.28 | -15.5 | 0.66 | 0.8 | 0.30 | +0.40 | equity_offering | True | 2 |
| 15 | JAGX | -7.7 | -6.00 | +0.00 | -6.00 | +0.0 | -6.0 | 35 | 12.0 | -0.60 | -164.5 | 2.15 | 0.9 | unk | +0.50 | dilution_or_going_concern | False | 2 |

## Floor-clearers: cause, what the reaction missed, and the base rate

Every number here is negative, so none is a rebound thesis. Phase 0's drift runs the same way, which makes these cheaper claims than a bounce would be. They are still claims about **one session**, where the median faller is **−1.00%** and the gross edge is about ±0.35%. **None of the four carried a leg-1 finding, so none has a repricing `mechanism_in_window`.** Each one's leg-2 mechanism is standing supply that can sell on 10-05.

- **JAGX −6.00** (−7.7% at the screen, 2.15× volume).
  - **Cause:** a dilution cascade after the 1-for-15 reverse split on 09-17. About 1.21m freely tradable Streeterville 3(a)(9) exchange shares were issued on 09-23 and 09-25 against ~1.95m outstanding. This is the twelfth fall of more than 5% since 09-04.
  - **What it missed:** the Ladenburg ATM still has **$9.82m** open (424B5, 09-24), which is more than the company's equity value at spot, and the 2021 note is not cancelled. The hunter's `p_up` is 35.
  - **Base rate:** the −10..−7.5 band prior is **+0.50%** (n=157). The name's own last 12 falls had a median next close of about −11.6%, with 2 of 12 up.
- **AKAN −3.50** (−11.8%, 0.66× volume).
  - **Cause:** a preliminary F-1 on 10-01 for a **$15m firm-commitment offering**, about 10× a ~$1.5m market cap. The company has $755k of cash and going-concern doubt.
  - **What it missed:** the offering could price overnight. The hunter thinks a fresh F-1 inside one session is unlikely (−2.0, tail to −25). January 2026 VWAP-discount notes keep converting (−1.5).
  - **Base rate:** the −15..−10 band prior is **+0.40%**. Volume under 2× averages **+1.46%** next session in phase 0, so this name argues against the volume cut as well as against the median.
- **GCTK −3.00** (−17.0%, 2.1× volume).
  - **Cause:** an overhang from September convertibles at **80% of the lowest 15-day VWAP**, plus a registered direct at $2.04 now underwater and a 43.4m-share resale S-1 against ~0.8m shares outstanding.
  - **What it missed:** today's VWAP lowers Monday's conversion price (−2.0). The Nasdaq Panel needs a **$1.00 closing bid through 11-09**, and spot is $1.17 with a 28.7% ATR (−1.5). A six-month no-issuance covenant offsets a little (+0.5).
  - **Base rate:** the −25..−15 band prior is **+0.34%**. Phase 0's −25..−15 band averaged +0.27% next session.
- **WHLR −3.00** (−6.5%, 0.82× volume).
  - **Cause:** a 96% slide over 60 days on stock-settled preferred exchanges and redemptions after a 1-for-9 reverse split on 09-21.
  - **What it missed:** the next **Series D Holder Redemption Date is 2026-10-05**, the window session itself, settled in common at a VWAP-linked price that today's fall lowers. The date is public; the share count is not.
  - **Base rate:** the band prior is **−1.04%**. The name's own 319 falls rose next day 33.5% of the time. Volume under 2× (+1.46%) argues the other way.

## What the day would cost to trade

- **Prediction spread:** the predictions span **6.5 points**, from −6.00 to +0.50.
- **Whole-day spread cost:** the known Corwin-Schultz half-spreads sum to **9.1 points over the ten names where the estimator returned a value**. Five names are "unk", so that sum is a floor.
- **Floor book:** of the four floor names only AKAN has an estimate (0.30). JAGX, GCTK and WHLR are unknown, all trade under $1m a day, and all four would be shorts in names that are hard to borrow.
- **Bottom line:** phase 0 measured the one-session gross edge at about ±0.35% against ~1.06 points of round-trip spread. **On this day the spread is larger than anything the ranking separates.**

## Labels a reader must carry

- **`next_earnings_estimated`** in every baseline is Zacks's cadence algorithm, not a company announcement. That is the TRT failure.
- **Short interest** is published about eight business days after settlement. Every figure the hunters quote is the 09-15 settlement, so the position carried into this fall is not observable.
- **USDEW is a warrant**, not common stock: StablecoinX warrants with an $11.50 strike. The screen let it through while rejecting other W-suffix tickers. It is outside phase 0's population, so its base rates do not apply. Recorded as a screen defect.

## Shed

Nothing was shed. All 15 names were hunted. Hunters ran 8 at a time (the session's concurrency cap), and all 15 hunts were written by 19:11 UTC.

**This stage places no orders, and nothing here moves a floor, weight or horizon.**

---

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._

# Stage R — reversal note — drop date 2026-10-01, window to close 2026-10-02

Screened intraday at **2026-10-01 15:04 EDT** (bars not final). SPY on the day at the screen: **+0.22%**. **46 names** passed the floors. The worst 15 reach down to −6.5%, and four of them (GLAS, NCT, BNR, INDP) fell less than 7.5% at the screen. All 15 were hunted and all 15 are rankable. Above the conviction floor (|impact_sum| ≥ 3.0) there is **one name: ONEN at −3.00, which sits exactly on the floor.**

The two largest sectors are Consumer Discretionary and Health Care, with **5 of 15 each (33%)**, so this is not a sector bet. It is a *pattern* bet again, though. **Nine of the eleven non-zero hunts rest only on live issuer or holder supply**: an effective ATM, a discount convertible, a forward-purchase holder, a registered-direct buyer, a lock-up expiry or zero-cost warrants. The other two non-zero names are SVRN, a crypto-treasury premium unwind, and LQDA, expected analyst cuts after a patent loss. The scorer cannot see this correlated exposure.

The scored window is **today's close → 2026-10-02 close**. The screen is an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close, and the 15:00→close move was a coin flip (mean −0.24%, median 0.00%). **Phase 0's base rates below are close-to-close and this screen is not**, so they are priors about a neighbouring population, not this one.

## Answer first

- **One floor-clearer, ONEN −3.00. It is leg 2 (supply) and has no leg-1 finding**, so `overshoot_has_mechanism` is false.
  - **Cause:** day 6 of a post-de-SPAC unwind. Hennessy VII merged into ONE Nuclear on 09-23 after 13.8m shares were redeemed. Today the stock gapped down 6.5% and fell a further 5.0% intraday to $1.91, on 2.9× volume. No company release was found today.
  - **What the reaction missed:** a Schedule 13D accepted overnight (09-30, 21:15 ET) shows New Circle, the forward-purchase counterparty, holding **4,987,103 shares and free to sell them**. That is about 45 sessions of current turnover. The FPA gives it no reason to hold: early termination costs it the $10.61 reset price, and the ~$53m prepayment is already paid.
  - **Mechanism in the window:** standing, unrestricted supply that can be sold on 10-02.
  - **Base rate:** the median faller does **−1.00%** the next close. ONEN's band (−15..−10, n=1,608) has a phase-0 prior of **+0.39%**. This name's own 8 comparable falls have a median of **−17.97%** (25% up). The ATR is 85%, so −3.0 is small against the name's noise.
- **Leg 1 found nothing today: zero repricing findings in 15 hunts.** Every `overshoot_pct` is 0. Three hunters considered a rebound case and filed it in `outside_window` or `rejected_candidates` because no mechanism closes it before the 10-02 close, which the brief requires; none is promoted here:
  - **LQDA:** PAH is not covered by the infringed claims.
  - **GLAS:** the DEA stay leaves the April medical order intact.
  - **BBGI:** the deleveraging from the offering.
- **Leg 2 carries everything.** Ten names sit between −0.45 and −2.00, almost all on supply: JAGX, KDK, NCT, EMAT, BBGI, INDP, NEXR, SVRN, LQDA and GLAS. Four are zeros (BNR, CCG, WW, XLAB): no identifiable cause, nothing dated inside the window.
- **The whole day leans down and the spread is narrow.** `impact_sum` runs from 0.00 to −3.00. Hunter `p_up` runs from 40 to 50, and nothing is above 50.
- **No reversal run has beaten a free control yet.**
  - The **2026-09-29 run is now resolved at d1** (15 names, 0 pending; `../resolve-2026-09-29.json`).
  - `impact_sum` read **ρ +0.034 (perm p 0.90)**, against `neg_atr14` **+0.356** (p 0.19), `neg_ret_d` −0.511, `neg_run_up_20d` −0.141 and `gap_share` −0.526.
  - `lean_vs_free_control_rho` is **−0.314**, so the lean is not the free control in disguise. As a ranker the lean read +0.021.
  - All 11 finding-bearing names on 09-29 were leg 2 only, so leg 1 and `overshoot_pct` could not be ranked.
  - The conviction book (3 shorts: LGHL, OPTT, CTNT) returned −6.30% gross. LGHL alone was −25.9% against the short, versus +1.02% for shorting everything.
  - **A run that does not beat the free controls has established nothing.** 09-29 lost to `neg_atr14`. On 09-28 the hunt beat `neg_atr14` and lost to `neg_run_up_20d`. Nothing is significant.
  - The 2026-09-30 run is pending, because its window closes at today's close.

## Ranked table

The two leg columns are the hunters' own finding sums, split by `leg`. Lean = `priced_lean_pct`. Band prior is the phase-0 cross-section expectation for the name's drop band and turnover band, close to close. Half-spread is Corwin-Schultz, which is a floor. **"unk" means unknown (the estimator returned 0 or failed), never narrow.** Fall % is the baseline's sealed `ret_d` at the screen.

| # | ticker | fall % | impact_sum | leg1 repricing | leg2 new info | overshoot_pct | more_to_come_pct | hunter expected_move | p_up | abs_move | lean | −ret_d | −ATR14 | vol× | turnover $m | half-spread % | band prior % | cause |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BNR | -6.4 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | 50 | 6.0 | -0.07 | 6.4 | -11.2 | 0.72 | 0.6 | +1.33 | -1.04 | no_identifiable_cause |
| 2 | CCG | -13.2 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | 50 | 9.0 | +0.09 | 13.2 | -30.6 | 0.49 | 0.5 | +0.38 | +0.40 | no_identifiable_cause |
| 3 | WW | -10.2 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | 50 | 5.5 | -0.81 | 10.2 | -10.8 | 1.55 | 3.8 | +1.48 | -0.33 | no_identifiable_cause |
| 4 | XLAB | -11.4 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | +0.0 | 50 | 12.0 | -3.82 | 11.4 | -25.5 | 1.78 | 0.2 | +0.68 | +0.40 | no_identifiable_cause |
| 5 | GLAS | -7.1 | -0.45 | +0.00 | -0.45 | +0.0 | -0.5 | -0.5 | 45 | 4.5 | -0.76 | 7.1 | -9.6 | 2.77 | 7.0 | +0.22 | -1.73 | litigation_or_regulatory |
| 6 | LQDA | -12.4 | -0.56 | +0.00 | -0.56 | +0.0 | -0.6 | -0.6 | 46 | 7.0 | -1.00 | 12.4 | -24.7 | 17.22 | 73.4 | +0.40 | +0.20 | litigation_or_regulatory |
| 7 | SVRN | -20.1 | -0.60 | +0.00 | -0.60 | +0.0 | -0.6 | -0.6 | 48 | 15.0 | -3.57 | 20.1 | -25.7 | 0.94 | 5.1 | +1.82 | -0.35 | sector_or_macro |
| 8 | NEXR | -14.6 | -0.84 | +0.00 | -0.84 | +0.0 | -0.8 | -0.8 | 44 | 7.0 | -0.47 | 14.6 | -22.2 | 0.52 | 0.3 | +0.72 | +0.40 | dilution_or_going_concern |
| 9 | INDP | -6.5 | -0.90 | +0.00 | -0.90 | +0.0 | -0.9 | -0.9 | 45 | 9.0 | -1.68 | 6.5 | -29.0 | 0.47 | 3.0 | unk | -1.77 | dilution_or_going_concern |
| 10 | BBGI | -12.4 | -0.96 | +0.00 | -0.96 | +0.0 | -1.0 | -1.0 | 42 | 6.0 | +0.50 | 12.4 | -13.2 | 0.99 | 0.6 | +0.20 | +0.40 | equity_offering |
| 11 | EMAT | -14.7 | -1.12 | +0.00 | -1.12 | +0.0 | -1.1 | -1.1 | 42 | 7.0 | -1.68 | 14.7 | -24.2 | 1.10 | 4.0 | +0.87 | -0.33 | dilution_or_going_concern |
| 12 | NCT | -7.1 | -1.20 | +0.00 | -1.20 | +0.0 | -1.2 | -1.2 | 45 | 12.0 | -1.40 | 7.1 | -158.2 | 0.67 | 1.3 | unk | -1.77 | dilution_or_going_concern |
| 13 | KDK | -12.8 | -1.60 | +0.00 | -1.60 | +0.0 | -1.6 | -1.6 | 40 | 8.0 | -0.30 | 12.8 | -18.8 | 3.10 | 6.3 | unk | -0.29 | index_or_flow |
| 14 | JAGX | -10.4 | -2.00 | +0.00 | -2.00 | +0.0 | -2.0 | -2.0 | 40 | 10.0 | -0.76 | 10.4 | -148.4 | 1.99 | 0.7 | unk | +0.40 | dilution_or_going_concern |
| 15 | ONEN | -11.2 | -3.00 | +0.00 | -3.00 | +0.0 | -3.0 | -3.0 | 40 | 15.0 | -9.93 | 11.2 | -85.4 | 2.92 | 0.4 | +0.18 | +0.40 | index_or_flow |

## For each name with a finding, the base rate it argues against

Every number here is negative, so none is a rebound thesis. Phase 0's drift runs the same way, so these are cheaper claims than a bounce would be. They are still claims about **one session**, where the median faller is −1.00% and the gross edge is about ±0.35%. The phase-0 band priors for the −7.5..−5 band (GLAS, INDP, NCT) rest on **7 events** and are not usable.

- **ONEN −3.00** (on the floor): covered above.
- **JAGX −2.00.**
  - **Cause:** a dilution cascade. Three Streeterville note-for-stock exchanges issued about 1.21m freely tradable shares into a ~520k-share post-split float between 09-23 and 09-25.
  - **Mechanism:** a Ladenburg ATM (~$9.8m available, re-supplemented 09-24) is larger than the ~$7.8m market cap and can be drawn on 10-02. The 2021 note is not stated as retired, so another exchange can land in the window.
  - **Base rate:** band prior +0.39%. The name's own 121 falls have a median of −1.66% (36% up).
- **KDK −1.60.**
  - **Cause:** the one-year SPAC lock-up ended on 09-24. A co-founder filed Form 144s for 3.4m shares from 09-25, and the stock is −35% over 5 sessions, falling on 3.1× volume through a positive AWS release.
  - **Mechanism:** sponsor and pre-merger holders sell without filing. The supply is not observable and probably not finished (`seller_is_finished_pct` 15).
  - **Base rate:** band prior +0.39%. The name's own 7 falls have a median of −0.30%.
  - **Process note:** the hunter filed its AWS-overshoot rejection under `contradicted_by_document` because the shared rejection reasons have no "no mechanism" option.
- **NCT −1.20.**
  - **Cause:** a second 25-for-1 reverse split (09-17), a spike to $14.31 intraday and about −90% since. The CEO bought 1.625m Class B shares at $0.40 on 09-25, already public.
  - **Mechanism:** zero-cost warrants from the July unit offering can be exercised on any session. The unexercised count is unknown, so it is sized small.
  - **Base rate:** the band prior is unusable (n=7). The name's own 98 falls have a median of −1.12%.
- **EMAT −1.12.**
  - **Cause:** Yorkville convertible supply. The facility converts at 95% of the lowest 5-day VWAP; about $12.4m of the May debenture remains, and a new $30.9m facility was funded on 09-17.
  - **Caveat:** newly converted shares have no registered route until the 09-24 S-1/A goes effective, and those figures are snippet-only.
  - **Base rate:** band prior +0.39%. The name's own 14 falls have a median of −2.73%.
- **BBGI −0.96.**
  - **Cause:** a $5.0m registered direct at $14.00 (357k shares, 35% of Class A) delivered at the 09-30 closing. Only ~161k shares have traded since, so the inferred flipper is probably not finished.
  - **Offset:** a 60-day issuance standstill (+0.2) rules out a second issuer raise tonight.
  - **Base rate:** band prior +0.39%. The name's own 37 falls have a median of **+0.58%** (51% up), so this one argues against its own history.
- **INDP −0.90.**
  - **Cause:** the $24m PIPE purchasers missed the 09-29 funding date (8-K 09-30, extended to 10-16), on top of a +104% 20-day run-up.
  - **Mechanism:** an effective $100m H.C. Wainwright ATM can sell into 10-02.
  - **Base rate:** the band prior is unusable (n=7). The name's own 178 falls have a median of −1.62%.
- **NEXR −0.84.**
  - **Cause:** a resale F-3 registering 3.5m shares, more than twice the 1.64m outstanding, behind a toxic convertible at 88% of the lowest VWAP. The F-3 is not effective.
  - **Base rate:** band prior +0.39%. The name's own 75 falls have a median of −1.14%.
- **SVRN −0.60.**
  - **Cause:** a $3.8m NEAR Intents exploit (CoinDesk 10:18 ET) hit the only Nasdaq-listed NEAR treasury, after a +669% month.
  - **Findings:** premium unwind −1.5, against service restoration (+0.5) and no dilution route (+0.4).
  - **Base rate:** band (−25..−15, n=5,827) prior +0.27%. The name's own 24 falls have a median of −6.07%.
- **LQDA −0.56.**
  - **Cause:** a Delaware court ruled on 09-30 that Liquidia's Yutrepia infringes the '327 patent claims covering the PH-ILD indication, and the stock fell 57% that day. Four analysts cut before today's open; at 17× volume the stock gapped −20.6% and recovered 10.4% intraday by the screen.
  - **Finding:** inferred further analyst cuts (8 of 12 not updated), small weight.
  - **Outside the window:** the real second shoe, the remedies filing due ~10-07, is filed in `outside_window` at −8.
  - **Base rate:** >15× volume averages **−2.44%** next session in phase 0. The name's own 12 falls have a median of −1.94%.
- **GLAS −0.45.**
  - **Cause:** cannabis-sector derating after the DEA ALJ stayed the Schedule III hearing (09-29). The only in-window line is an open $100m ATM.
  - **Base rate:** the band prior is unusable (n=7). The name's own 61 falls have a median of 0.0%.

## What it would cost to trade

The day's predictions span **3.00 points** (0 to −3.00), and ten of fifteen sit within 1.2 points of zero. The Corwin-Schultz half-spreads that are known (11 names) sum to **8.28 points**, an average of 0.75 per name, and **four are unknown** (INDP, NCT, KDK, JAGX). Those four include two of the three largest predictions.

For ONEN, a round trip at the floor estimate is **0.36 points** against a −3.0 prediction on an 85% ATR, but the estimate is blind to the widening the drop itself causes. **Every name is short-side.** None of the 15 baselines was checked for borrow, and on ONEN, JAGX, NCT and NEXR the float is tiny or newly issued. **One session is not tradeable on phase 0's measurement** (gross ±0.35% against ~1.06 points of round trip), and nothing today changes that.

## Labels the reader must not over-trust

- `next_earnings_estimated` (KDK 11-11, JAGX 11-13, INDP ~11-11, WW 11-05) is Zacks's cadence algorithm, **not a company announcement**. Trusting a cadence date like this caused the TRT failure.
- Short interest is published about eight business days after settlement, so every position quoted here is the **09-15 settlement**, before every one of these falls.

## Critical read

- **Contamination.** The JAGX hunter's WebSearch summary showed a 2026-10-01 "close" of $3.89 (−13.56%), dated after the 15:04 ET screen. The hunter discarded it and it entered no number. The CCG hunter saw a Benzinga October premarket-movers headline and did not open it. BNR and WW hunters saw snippets labelled 10-01 that matched the 09-30 close. No hunter reports using a post-screen price.
- **Typos in two hunt files, with no numeric effect, left as written:**
  - **BBGI:** the PIK springing-maturity date is written "2026-09-30-2027" where the source says 2027-09-30.
  - **INDP:** "4/1 amendment" should read 9/4.
- **ONEN sits exactly on the floor.** A 0.01-point change in one finding would drop the day to zero floor-clearers. Its single finding is an inference that a holder who *may* sell *will* sell into 10-02.
- **Leg 1 was empty again**, for the third day running. The leg-1 hypothesis cannot be tested until hunters file a mechanism-bearing overshoot. That could mean the brief is strict, or that such cases are rare; one day cannot tell them apart.
- **Nothing here moves a floor, weight or horizon.**

---

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._

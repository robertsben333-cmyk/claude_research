# Stage R — reversal note — drop date 2026-10-06, window to close 2026-10-07

Screened intraday at **2026-10-06 15:04 EDT** with the session still open, so the bars are not final. SPY at the screen was **+0.69%**. 5,977 names were screened and **40 passed the floors**. The worst 15 were taken. **XTND was dropped before hunting** because its baseline came back `too_little_history`. The other 14 were hunted and all 14 are rankable. **One name clears the conviction floor (|impact_sum| ≥ 2.8): SXTC −8.00.**

**Sector concentration:** Health Care 5 of 15 (33%), Technology 3, Consumer Discretionary 3, Industrials 2, Basic Materials 1, Finance 1. No sector is above half, so the universe file raises no warning. As on 10-02 and 10-05, the real shared exposure cuts across sectors and the scorer cannot see it. **Every non-zero finding but two is about issuer or holder supply**: equity lines and SEPAs, ATMs, resale registrations, pre-paid purchase facilities, reset warrants and a registered direct. The two exceptions are DCX's and NXH's small leg-1 items. On this day the fifteen names amount to one supply bet.

**Repeat names:** MEDS was also hunted on 10-05. Several others (NXH, SSM, CXAI, MKDW, IMC, BENF, TNMG, RDIB) are on their second or third straight down day.

The scored window is **today's close → 2026-10-07 close**. The screen ran an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close, and the 15:00→close move was a coin flip (mean −0.24%, median 0.00%). **Phase 0's base rates below are close-to-close and this screen is not**, so read them as priors from a neighbouring population, not this one.

## Answer first

- **One floor-clearer: SXTC −8.00, short side, leg 2 (supply). It has no leg-1 finding.** It is the deepest faller of the day (−33.2% at the screen, 11.6× volume) and the hunt's largest number in several runs (p100 of the Opus 5.5 reference).
- **Leg 1 produced findings for the first time in four runs, and both are small.**
  - **DCX +1.00** (repricing): its warrant reset window closed at the 10-05 close, so from now on the warrant holders gain from a higher price. Mechanism in window: yes, though it is the hunter's reading of the warrant terms.
  - **NXH +0.30** (repricing): the final 424B5 filed today carries a 90-day issuer lock-up, so the remaining ATM cannot be drawn. Mechanism in window: the overnight audience reads the document.
  - `overshoot_pct` is non-zero only on these two names. No overshoot without a mechanism is promoted.
- **Three hunts are non-results: IMC, MEDS and RDIB**, with no findings and p_up 50. Nine of the 14 causes are `no_identifiable_cause`. Most of the day's names fell 5–12% on thin volume (8 of 14 under 1× normal) with nothing filed.
- **The spread is narrow apart from SXTC.** `impact_sum` runs from **−8.00 to +0.50**, and 13 of 14 names sit inside −2.00…+0.50. DCX's +0.50 is the only positive number. It is the net of a +1.0 repricing finding, a −1.5 warrant-supply finding and a +1.0 no-new-issuance finding, and its `impact_scaled` is **−2.08**. So even the top name is not a rebound thesis.
- **`overshoot_has_mechanism` is still uninformative.** It is `true` on 12 of 14 names but only two filed a repricing finding. This hunter-contract defect is recorded for the fourth run running and nothing here relies on it.
- **No reversal run has beaten a free control yet**, and the pooled reading says so plainly:
  - **2026-10-05 run:** all 15 names are pending, because its window closes at today's close (`../resolve-2026-10-05.json`). `lean_vs_free_control_rho` is **−0.18**, so the lean is not the free control in disguise.
  - **Pooled d1, every resolved live run 09-21 → 10-02** (10 runs, 134 names, 9 days; synthetic 09-11 excluded):

    | ranker | ρ at d1 | perm p |
    | --- | --- | --- |
    | `impact_sum` (the hunt) | **+0.020** | 0.82 |
    | `neg_atr14` (free control) | +0.109 | 0.22 |
    | `neg_ret_d` (free control) | −0.153 | 0.08 |
    | leg 1 alone | +0.066 | 0.47 |
    | leg 2 alone | +0.003 | 0.98 |

    `lean_vs_free_control_rho` pooled is −0.04. **The hunt has not beaten `neg_atr14` and has established nothing.**
  - The pooled conviction book, |impact_sum| ≥ floor, was 15 legs, **+1.47% gross per leg, t 0.32**, with a CI of [−6.7, +10.5].
  - **This pool mixes hunter prompt versions** (the brief changed three times on 09-22 and since). Per CLAUDE.md that makes it a stage-level reading, not a judgement of any one version.
  - `neg_ret_d` is negative again, so the deeper fallers kept falling harder. That is phase 0's direction.

## Ranked table

How to read the columns:
- Leg columns are the hunters' finding sums split by `leg`.
- Lean = `priced_lean_pct`.
- Band prior is phase 0's cross-section expectation for the drop band and turnover band, close to close.
- Half-spread is Corwin-Schultz, a floor; **"unk" means the estimator failed, never narrow**.
- Fall % is the sealed `ret_d` at the screen.
- **DCX's −ATR14 of −282 is an artefact of the 160-for-1 consolidation on 09-28 inside the ATR window.** Do not read it as volatility.

| # | ticker | fall % | impact_sum | leg1 repricing | leg2 new info | overshoot_pct | more_to_come_pct | p_up | abs_move | lean | −ATR14 | vol× | turnover $m | half-spread % | band prior % | cause | mech? | n findings |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DCX | -11.8 | +0.50 | +1.00 | -0.50 | +1.0 | -0.5 | 42 | 13.0 | -1.21 | -282.0 | 1.23 | 0.8 | 0.08 | +0.40 | dilution_or_going_concern | True | 3 |
| 2 | IMC | -7.1 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 7.5 | +0.67 | -13.2 | 0.54 | 0.5 | 1.14 | -1.04 | no_identifiable_cause | True | 0 |
| 3 | MEDS | -6.4 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 10.0 | -2.27 | -31.5 | 0.55 | 3.3 | 0.42 | -1.77 | no_identifiable_cause | False | 0 |
| 4 | RDIB | -5.5 | +0.00 | +0.00 | +0.00 | +0.0 | +0.0 | 50 | 4.5 | -0.45 | -12.1 | 0.35 | 0.5 | 1.10 | -1.04 | no_identifiable_cause | True | 0 |
| 5 | NXH | -11.2 | -0.40 | +0.30 | -0.70 | +0.3 | -0.7 | 44 | 7.0 | -0.84 | -13.2 | 5.46 | 8.6 | 0.52 | -0.29 | equity_offering | True | 3 |
| 6 | YARW | -6.7 | -0.40 | +0.00 | -0.40 | +0.0 | -0.4 | 46 | 4.5 | -1.31 | -12.8 | 0.50 | 2.4 | 0.79 | -1.77 | no_identifiable_cause | True | 1 |
| 7 | TNMG | -5.7 | -0.50 | +0.00 | -0.50 | +0.0 | -0.5 | 47 | 7.0 | -1.50 | -20.5 | 0.36 | 0.4 | 1.10 | -1.04 | no_identifiable_cause | True | 1 |
| 8 | CXAI | -9.6 | -0.60 | +0.00 | -0.60 | +0.0 | -0.6 | 46 | 6.0 | -0.09 | -10.3 | 1.85 | 0.2 | 0.43 | +0.50 | no_identifiable_cause | True | 1 |
| 9 | SSM | -8.2 | -0.60 | +0.00 | -0.60 | +0.0 | -0.6 | 46 | 12.0 | +0.88 | -32.2 | 2.44 | 0.4 | unk | +0.50 | no_identifiable_cause | True | 1 |
| 10 | YDES | -24.9 | -0.75 | +0.00 | -0.75 | +0.0 | -0.8 | 53 | 8.0 | +0.46 | -22.8 | 0.51 | 2.3 | 3.93 | -0.39 | no_identifiable_cause | False | 1 |
| 11 | BENF | -5.9 | -0.80 | +0.00 | -0.80 | +0.0 | -0.8 | 44 | 6.0 | -1.80 | -41.3 | 0.22 | 2.1 | unk | -1.77 | no_identifiable_cause | True | 1 |
| 12 | MKDW | -11.6 | -2.00 | +0.00 | -2.00 | +0.0 | -2.0 | 42 | 8.0 | -0.80 | -68.0 | 0.68 | 0.3 | 1.00 | +0.40 | dilution_or_going_concern | True | 1 |
| 13 | SDEV | -19.0 | -2.00 | +0.00 | -2.00 | +0.0 | -2.0 | 40 | 13.0 | -1.51 | -42.8 | 31.67 | 2.2 | 1.46 | -0.39 | dilution_or_going_concern | True | 1 |
| 14 | SXTC | -33.2 | -8.00 | +0.00 | -8.00 | +0.0 | -8.0 | 35 | 25.0 | -3.43 | -31.4 | 11.56 | 0.2 | 0.50 | -0.17 | dilution_or_going_concern | True | 2 |

## The floor-clearer: cause, what the reaction missed, and the base rate

- **SXTC −8.00** (−33.2% at the screen, 11.6× volume, gap only −1.9%, ATR14 31.4%, ~$1.8m market cap).
  - **Cause (inferred, 55%):** nothing was filed or published today. The hunter reads the fall as continued selling under a **157.5M-share resale registration for Smart Mart Limited**, effective since 2026-09-16, against 1.32M Class A shares outstanding. Smart Mart's pre-paid purchase price resets to **50% of the lowest close**, so every new low cheapens its next purchase. Today's volume roughly equals the whole float.
  - **What it missed** (two leg-2 findings):
    - **−5.0:** the registration is effective, so shares can be sold on 10-07 with no new filing, and today's new 52-week low resets the investor's price lower again.
    - **−3.0:** twice in 2026 a comparable fall came the day before a registered direct off the effective shelf. On 01-08/09 the next close was −87.9%; on 07-22/23 it was −83.5%. The −3.0 is probability-weighted, and remaining baby-shelf capacity is unverified.
  - **Mechanism in window:** leg 2 only. There is **no repricing finding, so no `mechanism_in_window` on leg 1**. The hunter explicitly rejected "a 33% fall with no news is an overshoot".
  - **Base rate:** this is a short-side number, so it argues with the phase-0 drift, not against it. The −40..−25 band averaged **−0.76%** next session, and the <$1m turnover band +0.41%. The name's own 19 comparable falls had a **median next close of −5.96%** and rose 36.8% of the time. 11.6× volume is just under phase 0's over-15× cut (−2.44%).
  - **Tradeability:** about $0.22m median turnover and a $1.38 stock. A short here is almost certainly hard or impossible to borrow.

## Names near the floor (stated for context, not floor-clearers)

- **SDEV −2.00** (−19.0%, **31.7× volume**). Day two after a −47% fall. On 10-05 an 8-K spelled out ~219m fully diluted shares and $83.2m left on the ATM. The finding is that unspent ATM plus exercisable $0.05 pre-funded warrants, with the stock still ~3.3× fully diluted NAV. The band prior is +0.27% (−25..−15) and the over-15× volume cut is −2.44%; the volume cut argues the same way as the finding.
- **MKDW −2.00** (−11.6%, 0.68× volume). A $100M ATM against a ~$42M company. Every next close after this name's falls since the ATM opened has been negative, 6 of 6. The band prior is +0.39%.

## What the day would cost to trade

- **Prediction spread:** the predictions span **8.5 points** (−8.00 to +0.50), but **2.5 points without SXTC**.
- **Spread cost:** the known Corwin-Schultz half-spreads sum to **12.5 points over the 12 names where the estimator returned a value**. BENF and SSM are "unk", so the sum is a floor. YDES alone is 3.9.
- **Floor book:** one short in a $0.2m-a-day name that probably cannot be borrowed.
- **Bottom line:** phase 0 measured the one-session gross edge at about ±0.35% against ~1.06 points of round-trip spread. **Outside SXTC the spread is larger than anything this ranking separates.**

## Labels a reader must carry

- **`next_earnings_estimated`** in every baseline is Zacks's cadence algorithm, not a company announcement (the TRT failure). Where the hunters cite such a date (SSM, CXAI, NXH), it is filed outside the window as an estimate.
- **Short interest** is published about eight business days after settlement. Every figure the hunters quote is the 09-15 settlement, so the position carried into this fall is not observable. Nasdaq's short-interest API returned 503 to the SDEV and IMC hunters.
- **EDGAR full-text search (efts) returned HTTP 500** to several hunters (YDES, SSM, IMC, TNMG). They fell back on the baseline's sealed text probes.
- **DCX's warrant reset price (~$3.4) is the hunter's estimate from the 10-05 bar.** No filing publishes it. NXH's lock-up is "subject to certain exceptions" that were not read.

## Shed

- **XTND was dropped before hunting** (`too_little_history`).
- Nothing else was shed. Hunters ran 8 at a time (the session's concurrency cap), and all 14 hunts were written by 19:12 UTC (15:12 ET).

**This stage places no orders, and nothing here moves a floor, weight or horizon.**

---

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._

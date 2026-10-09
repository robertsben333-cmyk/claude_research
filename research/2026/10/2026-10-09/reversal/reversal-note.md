# Stage R — reversal note — drop date 2026-10-09, window to close 2026-10-12

The screen ran intraday at **2026-10-09 15:05 EDT**, with the session still open, so the bars are not final.
- **SPY at the screen:** **+0.65%**. These 15 names fell on an up day.
- **Universe:** 5,963 names screened, **46 passed the floors**, and the worst 15 were hunted.
- **Baselines:** all 15 were sealed at 19:05 UTC, before any hunter ran, and all 15 are rankable.
- **Floor:** **one name clears the conviction floor (|impact_sum| ≥ 2.8): GMEX at −3.00.**

**Next session:** Monday 2026-10-12. It is Columbus Day, and US equity markets are open. The window spans a weekend, so it holds two nights of news flow and one session.

**Sector concentration:** the sectors are spread out, so this is not one sector bet.

| Sector | Names of 15 |
| --- | --- |
| Health Care | 4 (27%) |
| Technology | 4 |
| Consumer Discretionary | 3 |
| Finance | 3 |
| Miscellaneous | 1 |

No sector is above half, and the universe file raises no warning. The shared exposure cuts across sectors, as on 10-02 through 10-07: **every non-zero negative finding is about supply.** The supply takes six forms:
- convertible-note and warrant issuance (GMEX, APUS)
- resale registrations (SDEV, IMCC)
- at-the-market offerings (MVIS, LGCL, SDEV, ARQQ)
- registered-direct paper still being sold (BIAF, IMCC)
- an annual-meeting share issuance (AIFA)

**Repeat name:** SDEV was also hunted on 10-06 and 10-07. This is its third appearance, and the fifth straight down leg of its Fugazi short-report unwind.

The scored window is **today's close → the 2026-10-12 close**. The screen ran an hour early. Over 45 sessions, 86.4% of the worst 15 at 15:00 ET were still the worst 15 at the close, and the 15:00→close move was a coin flip (mean −0.24%, median 0.00%). **Phase 0's base rates below are close-to-close and this screen is not**, so read them as priors from a neighbouring population.

## Answer first

- **This is close to a non-day.** `impact_sum` runs from **−3.00 to +0.40**, and 10 of 15 names sit inside −0.5…+0.4.
  - Four hunts returned zero findings: CCG, DUOT, EOSE and FGC.
  - Seven causes are `no_identifiable_cause`.
- **Leg 1 (repricing) is almost empty.** Only two names carry a repricing finding:
  - IMCC at −1.5 is a repricing *down*. Its mechanism in the window is a wider weekend audience reading an after-close F-3.
  - ARQQ at +0.4 is a repricing *up*. Its mechanism is an H.C. Wainwright note, dated only by last year's pattern.
  - No overshoot-and-bounce finding with a dated mechanism exists.
  - Every other number is leg 2 (`more_to_come_pct`).
- **GMEX −3.00 is the only floor-clearer. It is a short-side, leg-2 supply call. It has no repricing leg, so `mechanism_in_window` does not apply.**
  - **Cause:** −13.4% at the screen, after −27% on 10-08, on almost no volume (0.19×). There has been no filing since 2026-09-23.
  - **The finding:** the company's own consolidation releases show Class A shares going from 0.90m to 6.77m in eleven weeks. That came from secured notes payable in shares and from reset warrants. A second 1-for-9 consolidation followed on 09-28, and nothing on file says the issuance has stopped.
  - **What the hunt says the price got wrong:** the price treats the fall as a thin-tape wobble, while the share count says it is a continuous supply machine.
  - **The base rate it argues with:** the median faller does −1.00% at the next close, so a negative number is going *with* phase 0, not against it. GMEX's own band prior (−15…−10 fall, <$1m turnover) is **+0.40%**. The under-2× volume cut is **+1.46%**, and at 0.19× GMEX is about as low-volume as a faller gets. **Both cross-section priors point the other way from the hunt.** Its own history is on the hunt's side: six of its last seven drops continued.
  - **Cost:** the Corwin-Schultz half-spread is 0.48% (round trip 0.97%, a floor), on $0.36m of median daily turnover. Its `impact_scaled` is −2.88 (p96), so the two measurements agree.
- **The only positive numbers are RGP +0.40 and NCPL +0.30.** Both are offsetting findings, not rebound theses.
  - RGP has no ATM, no shelf, no going-concern language and no borrowings, so there is no second shoe.
  - NCPL has no usable prospectus, and a Nasdaq bid-price cure notice could land at any time.
  - **Base rates they argue against:** the median faller is −1.00%. RGP's band prior is **−1.77%**, against its own 31 falls at +0.59% median. NCPL's band prior is −0.30%, against its own 83 falls at a 0.0% median.
  - Neither is near the floor, and neither should be read as a call.

## Resolution: has the hunt beaten a free control?

**No reversal run has beaten a free control yet. The last two resolved runs both lose to their controls at d1.**

**2026-10-08: there is no stage R run directory, and the 10-08 run log carries no stage R entry.** Either the Routine did not fire that day or it published nothing. Check `list_triggers` before reading this as a code failure. So the previous run is **2026-10-07**.

**2026-10-07 run, now resolved** (`../resolve-2026-10-07.json`, 15 names, d1). `lean_vs_free_control_rho` is −0.22, so the lean is not the free control in disguise.

| ranker | ρ at d1 | perm p |
| --- | --- | --- |
| `impact_sum` (the hunt) | **−0.525** | 0.05 |
| `neg_atr14` (free control) | −0.171 | 0.56 |
| `neg_ret_d` (free control) | +0.043 | 0.88 |
| `neg_run_up_20d` (free control) | +0.604 | 0.02 |
| `gap_share` (free control) | +0.675 | 0.01 |

The hunt ranked the wrong way round at the close.
- **It did rank the open:** ρ +0.46 at `open1`, and the conviction cut had the sign right on 10 of 11 at the open, then 4 of 11 at the close.
- **Leg 1 was empty on that day,** so every number there was leg 2.
- **One day of 15 names is noise, and a negative ρ is not a signal to flip.**

**2026-10-06 run, now resolved** (`../resolve-2026-10-06.json`, 14 names, d1). `lean_vs_free_control_rho` is 0.00.

| ranker | ρ at d1 | perm p |
| --- | --- | --- |
| `impact_sum` (the hunt) | −0.093 | 0.74 |
| `neg_atr14` (free control) | **+0.547** | 0.04 |
| `neg_ret_d` (free control) | −0.169 | 0.57 |
| leg 1 alone (`overshoot_pct`) | −0.112 | |
| leg 2 alone (`more_to_come_pct`) | −0.013 | |

- **The repricing leg:** two names carried a `mechanism_in_window`, and the overshoot sign was right on **0 of 2** (mean move −4.26%).
- **The one floor-clearer was an SXTC short.** SXTC rose 126%.

**A run that does not beat the free controls has established nothing, and these two have not.** The pooled reading in the 10-07 note (09-21 → 10-05) stands: the hunt is at ρ +0.05 against `neg_atr14` at +0.12.

## Ranked table

How to read the columns:
- **Fall %** is the sealed `ret_d` at the screen.
- **L1 / L2** are the hunter's `overshoot_pct` and `more_to_come_pct`.
- **Lean** is `priced_lean_pct`.
- **Band prior** is phase 0's cross-section expectation, close to close.
- **Half-spread** is Corwin-Schultz over the 21 sessions before the drop. It is a floor, and **"unk" means the estimator failed, never that the spread is narrow.**
- **Seller fin.** is `seller_is_finished_pct`.
- **News bal.** is `news_flow_balance`.

| # | ticker | fall % | vol × | impact_sum | L1 | L2 | lean | band prior | turnover $m | half-spread % | cause | seller fin. | news bal. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RGP | −6.02 | 1.98 | +0.40 | 0 | +0.4 | −0.44 | −1.77 | 1.28 | 0.65 | earnings_miss | 45 | +20 |
| 2 | NCPL | −11.45 | 0.75 | +0.30 | 0 | +0.3 | −0.13 | −0.30 | 5.70 | unk | litigation_or_regulatory | 40 | 0 |
| 3 | CCG | −8.93 | 0.64 | 0.00 | 0 | 0 | +0.22 | +0.50 | 0.29 | 0.38 | no_identifiable_cause | 0 | 0 |
| 4 | DUOT | −6.85 | 2.29 | 0.00 | 0 | 0 | −1.16 | −1.77 | 4.93 | 0.74 | no_identifiable_cause | 0 | 0 |
| 5 | EOSE | −8.73 | 1.43 | 0.00 | 0 | 0 | +0.45 | +0.30 | 87.57 | unk | no_identifiable_cause | 10 | 0 |
| 6 | FGC | −5.98 | 0.97 | 0.00 | 0 | 0 | −0.47 | −1.04 | 0.47 | 0.71 | no_identifiable_cause | 0 | 0 |
| 7 | ARQQ | −9.98 | 2.63 | −0.10 | +0.4 | −0.5 | +1.49 | −0.20 | 5.23 | unk | earnings_miss | 35 | −15 |
| 8 | BIAF | −14.81 | 2.13 | −0.30 | 0 | −0.3 | −1.25 | −0.33 | 1.67 | unk | equity_offering | 50 | 0 |
| 9 | AIFA | −7.75 | 4.01 | −0.50 | 0 | −0.5 | −0.04 | +0.50 | 0.27 | unk | no_identifiable_cause | 20 | −20 |
| 10 | APUS | −14.88 | 0.86 | −0.50 | 0 | −0.5 | −0.90 | −0.33 | 1.04 | unk | no_identifiable_cause | 20 | −15 |
| 11 | LGCL | −8.13 | 2.05 | −1.00 | 0 | −1.0 | +0.27 | +0.50 | 0.21 | unk | no_identifiable_cause | 10 | −40 |
| 12 | MVIS | −8.78 | 3.38 | −1.50 | 0 | −1.5 | −0.24 | −0.23 | 1.71 | 0.42 | dilution_or_going_concern | 20 | −60 |
| 13 | SDEV | −18.14 | 1.45 | −1.50 | 0 | −1.5 | −2.62 | −0.35 | 13.42 | 0.38 | short_report | 30 | −60 |
| 14 | IMCC | −6.39 | 0.52 | −2.50 | −1.5 | −1.0 | −1.01 | −1.04 | 0.60 | unk | dilution_or_going_concern | 10 | −35 |
| 15 | **GMEX** | −13.40 | 0.19 | **−3.00** | 0 | −3.0 | −0.87 | +0.40 | 0.36 | 0.48 | dilution_or_going_concern | 10 | −40 |

**Two labels to carry with every name:**
- Every `next_earnings` date the hunters cite is Zacks's cadence estimate, not a company announcement. That is the TRT failure.
- Short interest is published about eight business days after settlement, so the position carried *into* this fall is not observable.

## The two legs, apart

- **`overshoot_pct` (leg 1):** non-zero on 2 of 15 names, summing to −1.1.
  - IMCC −1.5 has a mechanism in the window: a weekend audience for an F-3 filed at 16:06 ET on 10-08.
  - ARQQ +0.4 has a mechanism that is dated only by last October's analyst-note pattern. It is the weakest mechanism on the page.
  - **No overshoot opinion without a mechanism has been promoted.**
- **`more_to_come_pct` (leg 2):** non-zero on 11 of 15, summing to −9.1.
  - Nine names are negative and all nine are supply.
  - Two names are positive: RGP and NCPL, where a second shoe is structurally blocked.
  - BIAF nets to −0.3. Its ATM was cut to zero and a 30-day issuance ban is in place, but the registered-direct holder may still be selling.

**Volume, the cheapest phase-0 separator:**
- Only AIFA (4.0×) is above 3.5×, and none is near the 15× continuation cohort.
- Eight names are under 1.5×, the cohort that averaged **+1.46%** next session.
- Of the six names the hunt leans hardest negative on, IMCC (0.52×), GMEX (0.19×) and SDEV (1.45×) all sit in that under-2× bounce cohort. **That is the tension to watch at resolution.**

## What the ranking would cost to trade

- **Spread of the predictions:** 3.40 points top to bottom (+0.40 to −3.00). Excluding GMEX, it is 2.9 points.
- **Measured half-spreads:** where the estimator worked (7 names), they run 0.38–0.74%, a round trip of about 0.8–1.5 points each. That is a floor on spreads that widen on the drop day. The other eight names are "unk", which means unmeasured, not cheap.
- **What that leaves:** a one-session long-RGP / short-GMEX pair predicts about 3.4 points gross, against at least about 2.3 points of round-trip spread on the two legs. Add borrow on a $0.36m-a-day microcap that has just been reverse-split twice.
- **The rest of the table:** every name except GMEX and IMCC predicts less than its own round-trip spread.
- **Conclusion:** on a one-session horizon this ranking is not tradeable after costs, which is phase 0's finding repeated.

## Critical read of the floor-clearer

- **GMEX's −3.0 rests on one finding. Its source is real:** the company's own consolidation releases.
- **The weak link:** the inference that dated issuance is happening *this weekend*. No document dates a conversion inside the window.
- **Against it:** volume at 0.19× says almost nobody is selling. That fits supply that has dried up as well as supply that drips.
- **Repeat pattern:** this is the same "undated standing supply right" pattern that put an SXTC short above the floor on 10-06. SXTC then rose 126%.
- **Read it as a lead, not a call.**

**Shed:** nothing. All 15 names were hunted and scored. No floor, weight or horizon was changed.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone. 

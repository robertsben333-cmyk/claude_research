# Stage EU — Europe ranking for 2026-10-28

**One name clears the 2.8 conviction floor: DBV (DBV Technologies), −3.40, short side.** The issuer itself has not confirmed that it reports on 28 October. Earnings Whispers has 4 November, so this may be a phantom row (see below). Apart from DBV, the keys run from 8TRA +1.10 down to SALME −1.70, so the rest of the day sits inside ±2.

**The panel selected three names, all with at least 3 of 4 judges in their own top 20%:**
- DBV short: `panel_pct` 96, 4 of 4 judges.
- SALME (Salmon Evolution) short: `panel_pct` 86, 4 of 4 judges.
- 8TRA (TRATON) long: `panel_pct` 81, 3 of 4 judges.

All three sit at the hunters' own extremes. On this day the panel and the hunt agree.

**SRT (SRT Marine Systems) is not ranked.** Its hunter found no results event. There is no Notice of Results, and the vendor row carries an estimated 12:00 placeholder.

## The universe

- 88 names were scheduled for Wednesday 2026-10-28 and 53 cleared the $100k turnover floor.
- 20 were drawn at the cap. The draw was **random among the eligible names**, seeded `eu-2026-10-28` (`selection.method`).
- Drawn by market (`by_market`): fi 5, no 4, uk 3, fr 2, se 2, dk 2, de 1, es 1, it 0, pl 0.
- Eligible by market: fi 11, no 8, se 7, de 7, uk 6, fr 5, dk 4, es 3, it 1, pl 1.
- **Concentration** (`selection.market_concentration`): the largest market is Finland at 25%, and eight markets are represented. The Nordics are 13 of 20 names, so this is a Nordic-heavy day but not a one-market day.

**Calendar sources:**
- Yahoo's firm-date calendar read `unavailable` on all ten markets.
- bankier (PL) read `unavailable`.
- The UK RNS crawl, EQS (DE), Euronext Oslo (NO), Inderes and the Nasdaq Nordic financial calendar (FI/SE/DK) all read.

**Ranking key and sealed spots.**
- The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`.
- Baselines were sealed on Tuesday 2026-10-27 at about 14:10 UTC, while the European markets were still open. **Every sealed spot and run-up is an intraday price, not a close.**

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session, sealed → per the hunter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | de | 8TRA | TRATON | **+1.10** (p72) | no | +0.60 | 5.0 | 56 | bmo → bmo (last results 08:00 CEST) |
| 2 | se | ACAST | Acast | **+0.80** (p60) | no | +0.39 | 6.5 | 53 | bmo → bmo (07:00 CET, invitation) |
| 3 | es | ELE | Endesa | **+0.70** (p55) | no | +0.32 | 3.2 | 55 | bmo → bmo (prior 9M ~07:30; Q1 2026 was 17:51) |
| 4 | fi | VALMT | Valmet | **+0.70** (p55) | no | +0.65 | 6.5 | 55 | bmo → bmo (~09:00 EET, notice) |
| 5 | dk | AOJ_B | Brdr. A & O Johansen B | **+0.50** (p44) | no | +0.75 | 7.5 | 55 | amc → amc (H1 at 18:00 CEST) |
| 6 | uk | CGEO | Georgia Capital | **+0.50** (p44) | no | +0.24 | 4.0 | 53 | bmo? → bmo (Notice of Results, 07:00) |
| 7 | no | BNOR | BlueNord | **+0.30** (p29) | no | +0.06 | 1.4 | 52 | bmo → bmo (07:00 CET, NewsWeb) |
| 8 | uk | GSK | GSK | **+0.30** (p29) | no | +0.10 | 5.0 | 51 | bmo → bmo (07:00 GMT, IR page) |
| 9 | fr | AIR | Airbus | **+0.10** (p14) | no | +0.14 | 3.5 | 52 | amc → amc (pre-close call) |
| 10 | no | PHO | Photocure | **+0.10** (p14) | no | +0.00 | 6.0 | 50 | bmo → bmo (08:00 CET, NewsWeb) |
| 11 | dk | JYSK | Jyske Bank | **0.00** (p5) | no | 0.00 | 2.5 | 50 | bmo? → bmo by pattern (07:30 local) |
| 12 | fi | LASTIK | Lassila & Tikanoja | **−0.30** (p29) | no | 0.00 | 6.0 | 50 | bmo → bmo (08:00 EET, notice) |
| 13 | fi | SANOMA | Sanoma | **−0.30** (p29) | no | −0.50 | 5.0 | 45 | bmo → bmo (~08:30 EET) |
| 14 | no | TEL | Telenor | **−0.70** (p55) | no | −0.44 | 5.5 | 46 | bmo → bmo (invitation) |
| 15 | fi | UPM | UPM-Kymmene | **−0.70** (p55) | no | −0.45 | 4.5 | 45 | bmo → bmo (09:30–10:00 EET) |
| 16 | fi | ORNAV | Orion A | **−1.00** (p69) | no | −0.40 | 5.0 | 46 | bmo → **~12:00 EET, in session** (issuer notice) |
| 17 | se | PEAB_B | Peab B | **−1.10** (p72) | no | −0.66 | 5.5 | 44 | bmo → bmo (08:00 CET, issuer) |
| 18 | no | SALME | Salmon Evolution | **−1.70** (p84) | no | −0.84 | 6.0 | 43 | bmo → bmo (06:30 CET, NewsWeb) |
| 19 | fr | DBV | DBV Technologies | **−3.40** (p97) | **yes** | −1.30 | 6.5 | 40 | amc → amc (EDGAR/AMF timestamps); **date unconfirmed by issuer** |
| — | uk | SRT | SRT Marine Systems | not ranked | — | — | 2.2 | 50 | hunter found no event: no Notice of Results, vendor date estimated |

How to read the table:
- `impact_scaled` is the hunter's second, separate measurement. It is not the key, and the floor does not apply to it.
- Bracketed figures are percentiles of |value| among 655 names sized by Opus 5.5. They describe scale, not rank.
- Ties (ELE/VALMT, AOJ_B/CGEO, BNOR/GSK, AIR/PHO, LASTIK/SANOMA, TEL/UPM) carry no order.
- **LASTIK's two numbers disagree.** Its findings net −0.3, but `p_up` 50 gives 0.00.
- **AOJ_B's** scaled number is larger than its key. That comes from `abs_move_pct` 7.5 on an EBITDA-guide narrowing.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.**
- All four ran on their own pinned `-intl-` agents, with no fallback, and each covered 19 of 19 packs.
- Selection rule for this market: `consensus`, 3 of 4 judges in their own top 20%.
- Each judge's top 20% starts at Opus 5 |1.62|, Opus 5.5 |0.91|, Sonnet 5.5 |0.80| and Fable 5.1 |0.96|. Those thresholds come from 150 live sizes per member, taken from runs before this one.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DBV | **yes** | 96 | short | 2 | 96S* | 97S* | 93S* | 96S* | 4 | −2.22 | −3.40 |
| 2 | SALME | **yes** | 86 | short | 3 | 81S* | 87S* | 89S* | 89S* | 4 | −1.45 | −1.70 |
| 3 | 8TRA | **yes** | 81 | long | 9 | 89L* | 66L | 84L* | 84L* | 3 | +1.26 | +1.10 |
| 4 | ORNAV | no | 75 | short | 14 | 73S | 83S* | 89S* | 53S | 2 | −1.20 | −1.00 |
| 5 | PEAB_B | no | 69 | short | 16 | 50S | 85S* | 84S* | 56S | 2 | −0.97 | −1.10 |
| 6 | VALMT | no | 70 | long | 11 | 73L | 83L* | 69L | 53L | 1 | +1.00 | +0.70 |
| 7 | LASTIK | no | 62 | short | 18 | 35S | 57S | 80S* | 76S | 1 | −0.90 | −0.30 |
| 8 | CGEO | no | 55 | long | 19 | 63L | 47L | 80L* | 30L | 1 | +0.70 | +0.50 |
| 9 | ACAST | no | 56 | long | 8 | 60L | 43L | 61L | 62L | 0 | +0.75 | +0.80 |
| 10 | UPM | no | 59 | short | 13 | 42S | 69S | 73S | 51S | 0 | −0.73 | −0.70 |
| 11 | SANOMA | no | 52 | short | 3 | 53S | 51S | 49S | 56S | 0 | −0.65 | −0.30 |
| 12 | ELE | no | 28 | long | 7 | 17L | 37L | 30L | 30L | 0 | +0.38 | +0.70 |
| 13 | TEL | no | 31 | short | 10 | 19S | 40S | 22S | 41S | 0 | −0.38 | −0.70 |
| 14 | GSK | no | 26 | long | 6 | 33L | 15L | 28L | 29L | 0 | +0.36 | +0.30 |
| 15 | AOJ_B | no | 27 | long | 8 | 37L | 21L | 17L | 32L | 0 | +0.35 | +0.50 |
| 16 | PHO | no | 28 | short | 20 | 60S | 9S | 17S | 26S | 0 | −0.30 | +0.10 |
| 17 | BNOR | no | 6 | long | 1 | 5L | 5L | 5L | 8L | 0 | +0.11 | +0.30 |
| 18 | AIR | no | 7 | long | 16 | 6S | 15L | 30L | 9S | 0 | +0.04 | +0.10 |
| 19 | JYSK | no | 0 | – | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 | 0.00 |

**DBV, short, 4 of 4.**
- **Main item: the toddler BLA guide.** DBV guided the ages 1–3 BLA for "second half of 2026" in March and April. The July release dropped that date. ClinicalTrials.gov puts COMFORT Toddlers' primary completion at 2026-11, so the guidance line very probably slips. The slip itself is the hunter's inference; no source says it.
- **Supporting items:**
  - The stock fell the session after 8 of its last 9 releases.
  - The runway restatement is a knife-edge: going-concern language depends on runway "into Q4 2027".
  - MPM BioImpact has sold below 5% (AMF filing). At that point further sales no longer have to be disclosed.
- **Case against:**
  - **The event may not happen on this date.** TradingView, AJ Bell and Divaltis say 28 October, and Q3 2025 printed on exactly 2025-10-28. But DBV has published no "to report Q3" notice, while it gave its Q2 notice two days ahead, and Earnings Whispers says 4 November.
  - The AMF register shows shorts at 2.89%, slightly covering. A further guide slip may already be expected by holders of a pre-commercial biotech.

**SALME, short, 4 of 4.**
- **Main item: the 2026 harvest guide.** The ~6,000t guide needs about 1,694t in Q4, 41% above Q4 2025 and near the record Q1 2026. The 8 October operational update did not reaffirm it, so a second trim is live.
- **Second item:** a first 2027 guide is likely in this report, on the Q3 2025 precedent, and the judges read it as likely to come in low.
- **Case against:**
  - Q3 harvest, price and weight were all pre-released on 8 October (−3.5% that day).
  - The stock is −23.5% over 60 days.
  - Norwegian spot salmon reached NOK 70/kg in week 42; that figure is snippet only.
  - Shorts are 2.59% and flat.
  - No Q3 consensus could be sourced.

**8TRA, long, 3 of 4** (Opus 5.5 at 66, outside its top 20%).
- **Main item: Q3 order intake.** It is the only line that is new in the release. Counterparties point the same way: Volvo truck orders +26% (23 October), Daimler NA, and Traton's own pre-close comments on NA 2027 order books.
- **Supporting item:** Traton has filed no MAR ad-hoc for Q3. It files one when a quarter deviates sharply from consensus.
- **Case against:**
  - The pre-close on 1 October already talked Q3 margins down.
  - The company-posted consensus page would not render, so the bar is unsourced.
  - The findings agree with the run-up lean (+0.35), which is the free control.
  - A VW stake placement could follow the print. It is filed outside the window at −3.0, and the March 2025 precedent came at an 8% discount right after results.

**Where the panel and the hunters disagree:**
- **PHO.** The hunter is +0.10 and the panel is short (28). Opus 5 at 60S weighed the US deceleration, the Asieris receivable and the capital-raising CFO more heavily than the guide-raise finding.
- **ELE.** The hunter's +0.70 ties for third on the key, but the panel puts it at 28. The judges discount a guide-raise argument built on one broker's numbers for a stock at an all-time high.
- **AIR.** Two judges are long and two short, and all are near zero.
- **No floor-clearer was missed.** DBV, the only name above the floor, was selected.

**What the panel numbers are not:**
- `panel_score` ranks and does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed until this market has about 200 panel names of its own.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but on 48 names. Nothing about this market's panel is established.

## The floor-clearer, and the name the key ranks top

- **Bottom, DBV −3.40.** The driver is finding 1, the toddler BLA guide slip (−2.0, guidance), resting on DBV's March and April releases against ClinicalTrials.gov's COMFORT Toddlers record, primary completion 2026-11. The full source list is in `hunts/DBV.json`.
  - Read the event risk first. If DBV does not report on 28 October, the window is an ordinary session and the name should resolve as `event_occurred: false`.
  - France's AMF flux cannot reach that kill (since 2026-09-28), so it will have to be settled by hand from the issuer's own release.
- **Top, 8TRA +1.10.** The driver is the order-intake finding (+1.0, orders), from Volvo's Q3 report of 23 October and Traton's 12 October unit-sales release. It is far below the floor.

## Unranked and flagged

- **SRT: not ranked.** There is no Notice of Results on Investegate, against the pattern of SRT's two previous finals. The IR page says "Next webcast to be announced". The vendor row is a 12:00 placeholder with an estimated publication type. The finals are due by 2026-12-31 under AIM rule 19.
- **DBV: date unconfirmed by the issuer** (see above).
- **Sealed `session_unresolved`:** CGEO, JYSK and SRT. All three hunters settled CGEO and JYSK as bmo (CGEO from its own RNS notice; JYSK from the 07:30 pattern, with no time published). SRT has no event.
- **Releases inside the session:** ORNAV releases at ~12:00 EET, and UPM's 09:30–10:00 EET straddles the 10:00 open. Both are still inside close(10-27) → close(10-28).
- **Prior release outside the usual slot:** ELE's Q1 2026 came after the close (17:51). If 9M does the same, the reaction falls outside the sealed window.
- **amc names (window close(10-28) → close(10-29)):** AIR, DBV and AOJ_B, as sealed.

## Instrumentation, every time

- **`options` is null in all ten markets.** Europe runs in the anchor-less regime that priced ρ = +0.073, p = 0.45 over 104 events on the sealed corpus (`archive/backtest/FINDINGS.md` §33).
- **Short registers.** These read: uk, de, fr, se, dk, no and fi. Spain has none reachable. No Italian or Polish name was drawn.
- **Positioning anchors.**
  - **5 of 20 names carry `anchor_covered: true`:** CGEO 1.50%, GSK 1.21%, DBV 2.89%, JYSK 0.83% (on Denmark's 0.1% threshold, not on the 0.5% scale) and SALME 2.59%.
  - The other 15 are truncated zeros, not anchors.
- **Spain and Poland:** 1 name (ELE). It has no positioning anchor, its lean is the run-up and therefore the free control, and it can never be confirmed or killed after the fact.
- **Germany:** 1 name (8TRA). It cannot reach `event_occurred: false` either.
- **France since 2026-09-28:** AIR and DBV cannot be killed by the AMF flux. AIR is a Dutch issuer and does not file there at all.
- **Nordic names to resolve within about a week:** ACAST, PEAB_B (se); AOJ_B, JYSK (dk); LASTIK, ORNAV, SANOMA, UPM, VALMT (fi). The Nasdaq Nordic feed pages back only about 12 days.
- **`lean_vs_free_control_rho` from the previous resolved run** (2026-10-16): Sweden 0.60. No other market reported one on that run.
- **The lean's weights** are priors borrowed from the US runs and measured nowhere in Europe.
- **`history.basis`.** Only 7 names carry observed histories: uk CGEO, GSK and SRT (`observed_rns`), and no BNOR, PHO, SALME and TEL (`observed_newsweb`). The other 13 are **estimated from cadence**: a scale, not a record of dates. Several hunters (VALMT, ORNAV) found their real report-day moves far larger than the cadence-estimated scale.
- **Conviction floor.** Only DBV is above 2.8. Over the whole US sample the sign was a coin flip below the floor.

**Already public and guidance.** Every hunt recorded `already_public` items and a guidance line in `new_in_release`. The pre-releases that matter most:
- **JYSK:** the full Q3 P&L and a raised guide went out on 12 October. That is why it is sized at 0.
- **ORNAV:** the guide was raised on 20 October, so the release itself is half-empty.
- **SALME:** Q3 operations were pre-released on 8 October.
- **GSK:** an aide-memoire flagged the Q3 headwinds on 8 October.
- **SRT:** FY26 was pre-released in July.
- **BNOR:** a merger target pinned to Vår Energi at 9.7153 VAR + NOK 76.83, so its own print should hardly matter.

Likely guidance changes named by the hunters:
- SALME: a 2026 trim and a first 2027 guide.
- DBV: the toddler BLA date.
- SANOMA: the range narrowed, likely by raising the low end, which would land below a consensus already at 223.
- PHO and AOJ_B: an upward narrowing.
- LASTIK: the guide is conditioned on fuel prices.

**language_note highlights.** These are prose and rank nothing:
- **Finnish Inderes notes** were the only source of a Q3 consensus for SANOMA, UPM and VALMT, and of the post-upgrade estimates for ORNAV.
- **French copy** carried Airbus's Bloomberg consensus, and AMF filings carried MPM's sale of DBV shares.
- **Spanish sources** carried the Jefferies preview and the definition of Endesa's guided metric.
- **Norwegian sources** added only Telenor's outage inspection.
- **UK domestic sources** added nothing beyond RNS.

**One day is not a result.** This is one day of 19 ranked names, Nordic-heavy, with one floor-clearer whose event date is itself in doubt.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

# Stage EU — Europe ranking for 2026-10-26

**No name clears the 2.8 conviction floor.** The hunters' keys run from ALLEI +1.00 to BVXP and KREATE, tied at −0.20, so the whole day sits inside ±1. **The panel selected one name: BVXP short, all 4 of 4 judges in their own top 20%, `panel_pct` 96, spread 2.** The hunter sized the same name at only −0.20, so this is where the panel and the hunt part most.

Seven names were scheduled for Monday 2026-10-26, cleared the $100k turnover floor and were all hunted, which is under the cap of 20, so no draw was needed. They come from five markets: uk 2 (AMC, BVXP), pl 2 (KTY, OPL), se 1 (ALLEI), fi 1 (KREATE) and it 1 (SGF). The largest market is the UK at 29% (`selection.market_concentration`), so the day is not one market's.

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. Sealing took place on Friday 2026-10-23 at about 13:50 UTC, while the European markets were still open. **Every sealed spot is therefore an intraday price, not a close.**

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session, sealed → per the hunter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | ALLEI | Alleima | **+1.00** (p67) | no | +0.65 | 6.5 | 55 | bmo → **11:30 CET, in session** (issuer invitation) |
| 2 | it | SGF | Sogefi | **+0.70** (p54) | no | +0.32 | 8.0 | 52 | bmo? → **amc** (last three releases 18:48, 20:20 and 19:05) |
| 3 | uk | AMC | Airtel Money (Airtel Mobile Commerce) | **+0.60** (p50) | no | +0.44 | 5.5 | 54 | bmo? → bmo, inferred from a 12:00 GMT webcast; no release time stated |
| 4 | pl | OPL | Orange Polska | **+0.50** (p43) | no | +0.29 | 4.8 | 53 | amc → amc (Q2 21:26, Q1 18:08) |
| 5 | pl | KTY | Grupa Kęty | **+0.30** (p29) | no | +0.18 | 3.0 | 53 | bmo? → **amc** (Q1 17:07, H1 17:06) |
| 6 | uk | BVXP | Bioventix | **−0.20** (p20) | no | −0.72 | 9.0 | 46 | bmo? → bmo (every results RNS at 07:00) |
| 7 | fi | KREATE | Kreate Group | **−0.20** (p20) | no | +0.66 | 5.5 | 56 | bmo → bmo by pattern (07:30); time not yet published |

How to read the table:
- `impact_scaled` is the hunter's second, separate measurement. It is not the key, and the floor does not apply to it.
- Bracketed figures are percentiles of |value| among names sized by Opus 5.5. They describe scale, not rank.
- BVXP and KREATE are tied, so their order carries no information.
- KREATE's two numbers disagree in sign. Its up-lean comes from the stock's own report-day history (up on each of the last four), which moves `p_up` and is not filed as a finding.

## Sessions: two of the seven are probably on the wrong window

- **KTY and SGF were sealed `bmo?` (`session_unresolved`), and both hunters found from the issuer's own release timestamps that they report after the close.**
  - KTY: Bankier timestamps for its last two reports, 17:07 and 17:06 CEST.
  - SGF: eMarket STORAGE timestamps for its last three, 18:48, 20:20 and 19:05.
  - The sealed close(10-23) → close(10-26) window therefore holds no release for either. Because both rows are `session_unresolved`, `eu_resolve.py` measures BOTH windows, and the amc one, close(10-26) → close(10-27), is the one to read.
- **ALLEI releases at about 11:30 CET, inside the Stockholm session.** The sealed window still contains the whole reaction.
- **AMC's bmo is an inference.** It rests on a 12:00 GMT webcast "on the day of results". AMC and BVXP were both `session_unresolved`, and BVXP's bmo is backed by six 07:00 RNS releases.
- **OPL** is amc as sealed: close(10-26) → close(10-27).

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.**
- All four ran on their own pinned `-intl-` agents, with no fallback, and each covered 7 of 7 packs.
- Selection rule for this market: `consensus`, 3 of 4 judges in their own top 20%.
- Each judge's top 20% starts at Opus 5 |1.80|, Opus 5.5 |0.90|, Sonnet 5.5 |0.72| and Fable 5.1 |1.00|. Those thresholds come from 123 live sizes per member, taken from runs before this one.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BVXP | **yes** | 96 | short | 2 | 98S* | 97S* | 94S* | 96S* | 4 | −2.32 | −0.20 |
| 2 | ALLEI | no | 75 | long | 7 | 64L | 82L* | 75L | 80L* | 1 | +1.08 | +1.00 |
| 3 | AMC | no | 58 | long | 8 | 70L | 52L | 63L | 49L | 0 | +0.69 | +0.60 |
| 4 | SGF | no | 26 | long | 42 | 42S | 58L | 63L | 23L | 0 | +0.53 | +0.70 |
| 5 | KREATE | no | 38 | long | 18 | 29L | 35L | 19L | 68L | 0 | +0.42 | −0.20 |
| 6 | OPL | no | 31 | long | 8 | 28L | 19L | 40L | 38L | 0 | +0.41 | +0.50 |
| 7 | KTY | no | 10 | long | 6 | 6L | 3L | 19L | 11L | 0 | +0.14 | +0.30 |

Each member's figure is its percentile (0–100) against its own live range: L is long, S is short, and `*` marks the member's own top 20%. The judges' raw sizes on BVXP were Opus 5 −3.05 (`p_up` 34), Fable 5.1 −2.16 (38), Opus 5.5 −1.80 (40) and Sonnet 5.5 −1.4 (42).

**BVXP, selected short (4 of 4, `panel_pct` 96, spread 2).**
- **What the judges name:** FY26 (to 30 June) is the first release that can show royalties, which are paid in arrears. Those royalties come off a half in which the payers were soft:
  - Siemens Healthineers Diagnostics, which pays the troponin royalties, posted comparable revenue −5.5% in Apr–Jun and guided another mid-single-digit decline (https://medtechspectrum.com/company-results/60/25906/siemens-healthineers-lowers-fy2026-revenue-outlook-despite-strong-order-momentum.html).
  - Roche Diagnostics grew +3% CER, with China pricing the drag (https://www.roche.com/media/releases/med-cor-2026-07-23).
- **The tape into the print:** the stock went from 1,500p to 2,000p (+23% over 20 sessions, +9.3% over five) with no RNS since 24 June. This is a one-analyst AIM name trading about $350k a day with a ~5% bid-offer. Its last three FY results days closed −2.1%, −10.3% and −15.7%. The FY25 one came with a dividend cut from 87p to 80p.
- **Nothing is pre-released:** the last statement was "in line with expectations" on 30 March (https://www.investegate.co.uk/announcement/rns/bioventix--bvxp/interim-results/9496897).
- **Strongest case against:**
  - Roche's pTau217 blood test was FDA-cleared on 24 August. Bioventix says its antibodies sit in three of the leading IVD companies' research-use pTau217 assays, so a positive neuro statement is the upside tail (the hunter sizes it −1.5 to +5).
  - The board has said reserves will hold the dividend "at historic levels", which removes the FY25-style cut.
  - The run-up is itself the baseline's lean (−1.15) and the free control. A name selected on it is partly the control wearing the panel's clothes.
  - The hunter halved its own run-up finding for exactly that reason and kept the sum at −0.20.

**Where the panel and the hunters disagree most:**
- **BVXP:** the hunters sized it −0.20, the panel 96 short. The judges weighted the run-up and the FY reaction history far more heavily than the hunter, who discounted both under the lessons file's "positioning is the thing to beat" rule.
- **KREATE:** the hunters sized it −0.20, the bottom key, while the panel is 38 long. Fable 5.1 reads the 22 September guide raise (eight days before quarter-end) as more than priced.
- **SGF** has the day's widest spread (42). Opus 5 is short on OPmobility's 7 October target cut and the July sale of a beat, while Opus 5.5 and Sonnet 5.5 are long on the conservative-guide arithmetic.
- **ALLEI**, the hunters' top key, is the panel's second at 75, with two of four judges in their own top 20%.

**What these numbers are not:**
- `panel_score` ranks and does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales are still mostly the frozen E-P seed, with 123 live sizes each against the ~200 this market needs.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but nothing about this market's panel is established.

## The finding driving the top and the bottom

**Top: ALLEI +1.00**, three findings.
- **+0.9:** the single-source Factset bar of SEK 244m adjusted EBIT (Börsvärlden, 2026-10-23, "Alleima väntas redovisa 244 miljoner kronor i justerat rörelseresultat", i.e. Alleima expected to report SEK 244m adjusted operating profit; https://borsvarlden.com/artiklar/alleima-vantas-redovisa-244-miljoner-kronor-i-justerat-rorelseresultat-factset) implies a Q2→Q3 drop of 275m. That is larger than 2025's 257m drop, and the 2025 quarter carried an extended maintenance stop at Sandviken (https://attachment.news.eu.nasdaq.com/ac54b868fac990455c169e72674f45caf). About SEK 50m of year-on-year savings comes on top.
- **+0.4:** Swedish engineering peers' Q3 orders (Sandvik, Atlas Copco, SKF).
- **−0.3:** nickel fell after the guided +SEK 100m metal-price effect. That hits reported EBIT, not adjusted.

**Bottom, tied: BVXP −0.20 and KREATE −0.20.**
- **BVXP:**
  - **−0.6:** soft royalty payers (above).
  - **−0.5:** the newsless run-up.
  - **+0.5:** pTau217.
  - **+0.2:** the dividend hold.
  - **+0.2:** the CFO buying on 24 June.
- **KREATE:**
  - **−0.5:** order backlog risk. About 15m of announced Q3 intake against about 210m of revenue; holding the record 886m needs more than 200m (https://www.inderes.fi/en/analyst-comments/kreate-q326-preview-expectations-for-yet-another-record-breaking-quarter).
  - **−0.3:** H1 free cash flow of −3.2m.
  - **+0.3** and **+0.3:** a Q3 inside the guide raised on 22 September, which is already priced (+11.6% that day).

## Names that could not be ranked

None. All 7 are rankable and confirmed by their issuers' own calendars.

## Pre-released, or a likely guidance event (`already_public` / `new_in_release`)

- **Pre-released:**
  - **KTY:** the Q3 headline numbers came out on 24 September (revenue 1,615m PLN, EBITDA 325m, net 201m, in line with PAP consensus; https://grupakety.com/wp-content/uploads/2026/09/2026_3Q_szacunki.pdf). What is live is the stale FY2026 forecast. It implies a Q4 EBITDA of 170m against 205m a year ago, and Kęty raised its guide while preparing the Q3 report in 2021 and 2023. No update notice has come.
  - **AMC:** Q1 is public via the prospectus, and Q2 was described as "in line" on 23 September.
  - **KREATE:** the upward profit warning of 22 September covers most of the quarter.
- **Likely guidance or new-information events:**
  - **OPL:** a possible second FY2026 raise. The street's EBITDAaL of PLN 3.677bn sits at or below the >6% guide (https://www.parkiet.com/rekomendacje/art45215371-orange-polska-w-gronie-faworytow-sezonu-wynikow-iii-kwartalu), against a +23% 20-day run-up.
  - **SGF:** the FY guide implies an H2 adjusted EBIT margin of about 4.5%, against 6.7% in Q3 2025 (https://www.emarketstorage.com/sites/default/files/comunicati/2026-08/20260805_187878.pdf).
  - **BVXP:** the first FY27 outlook.
  - **AMC:** the first interim dividend as a listed company. Research is blacked out until after 19 November.
- **Fully new numbers:** ALLEI, with no profit warning or trading update.

## What the day can and cannot say

**Universe and calendar**
- `selection.method`: "all 7 eligible names (at or under the cap)", seed `eu-2026-10-26`. 12 were scheduled and 5 were dropped below the floor. No market was closed.
  - Eligible and hunted are the same: uk 2, pl 2, se 1, fi 1, it 1, and de/fr/dk/no/es 0.
- **Calendar sources:**
  - The UK RNS calendar added AMC.
  - **Yahoo's calendar endpoint read `unavailable` on all ten markets.**
  - Issuer calendars dated 4 SE (Inderes), 1 FI (Inderes and Nasdaq financial calendar) and 3 PL (bankier) rows for the target. EQS (DE) and Euronext Oslo (NO) read with 0.
  - By hunted row: KREATE vendor+Inderes+Nasdaq financial calendar, ALLEI vendor+Inderes, KTY and OPL vendor+bankier, AMC RNS. **SGF and BVXP are vendor-only.** Both were confirmed by their issuers' own calendars during the hunt.

**Anchors and registers**
- **`options` is null in all ten markets.** Europe runs in the anchor-less regime, which on the sealed US corpus ranked at ρ=+0.073, p=0.45 over 104 events.
- **Short registers read for se, fi, it and uk.** Poland's KNF register is unreachable.
- **`anchor_covered: true` on 1 of 7:** ALLEI, 1.81% disclosed net short, unchanged since 10-14.
  - AMC, BVXP, KREATE and SGF are truncated zeros: the register was read and does not name them, which is not evidence that nobody is short.
  - KTY and OPL have no register at all.
- **Spain 0, Poland 2 (KTY, OPL), Germany 0.**
  - The two Polish names carry no positioning anchor, so their `priced_lean_pct` is the run-up, which is also the free control. They cannot be confirmed or killed after the fact.
  - SGF (Italy) cannot reach `event_occurred: false` either, because eMarket STORAGE is not universal.
- **`lean_vs_free_control_rho`:** the last resolved European run (2026-10-16) carries it only for Sweden, 0.6. That is one market on a handful of names, so not a measurement. The runs from 10-19 onward are unresolved.
  - **The 2026-10-15 run's two wrong Nordic kills (NDA_FI, ERIC_A) are still waiting on a fix, and the Nasdaq Nordic feed's window for that date closes around 10-27.**
- The lean's weights are priors borrowed from the US runs and measured nowhere in Europe.

**History basis**
- `history.basis` is observed for AMC and BVXP (`observed_rns`). AMC's history holds 0 events, because it listed on 9 October.
- **It is estimated for the other five** (ALLEI, KREATE, KTY, OPL, SGF): a scale, not a record of dates.

**Floor and language**
- **No name sits above the 2.8 conviction floor.** Over the whole US sample, the sign was a coin flip below it.
- `language_note`: the Polish press (Parkiet, StockWatch, Bankier) carried what no English source had:
  - OPL's company-collected 8-broker consensus and the PKO upgrade;
  - the timestamps that settle KTY and OPL as amc;
  - KTY's entire forecast arithmetic, all from Polish issuer filings.
- eMarket STORAGE alone carried SGF's release times.
- ALLEI's only bar was Swedish-language wire copy.
- KREATE's Forssa data-centre contract exists only as a Finnish press release: "Kreate on kirjannut urakan arvon kolmannen neljänneksen tilauskantaansa" (Kreate has booked the contract value in its Q3 order backlog).
- On BVXP and AMC the domestic sources (Investegate, the issuers' own IR pages) settled dates and sessions but added no view.

**One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.

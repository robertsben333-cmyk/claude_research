# Stage EU — Europe researcher, event date 2026-11-12

Sealed 2026-11-11 ~14:43 UTC (15:43 Amsterdam), while the European markets were still trading. The sealed spots are **intraday prices, not closes**. The scored window is close(2026-11-11) → close(2026-11-12) for bmo names, measured by `eu_resolve.py` from daily bars. Ranking key: `impact_sum` (from `edge-scores.json`). Conviction floor: 2.8.

**Answer first:** no name reaches the 2.8 floor. The hunter's largest numbers are SIE −2.20 and SYNSAM −2.00; the top is SMWH at +1.00. The four-model panel selects three names, **all short**: **SYNSAM** (4 of 4, panel_pct 92), **SIE** (3 of 4, 87) and **XPLRA** (3 of 4, 83). Over the whole US sample the sign below the floor was a coin flip. One day is not a result.

## Ranked table

| # | ticker | mkt | session | impact_sum | abs_move | p_up | impact_scaled | anchor | history |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SMWH | uk | bmo | +1.00 | 8.0 | 47 | −0.48 | yes | observed_rns |
| 2 | OHB | de | bmo | +0.50 | 5.5 | 51 | +0.11 | no | est. |
| 3 | VBK | de | bmo? | +0.50 | 7.0 | 53 | +0.42 | no | est. |
| 4 | REY | it | bmo? (in-session, ~12:30–14:00 CET) | +0.45 | 5.0 | 53 | +0.30 | no | est. |
| 5 | 1U1 | de | bmo? | +0.30 | 3.2 | 52 | +0.13 | no | est. |
| 6 | DIB | it | bmo? → **amc** | +0.20 | 5.0 | 51 | +0.10 | no | est. |
| 7 | KAR | se | bmo | +0.10 | 7.0 | 50 | +0.00 | no | est. |
| 8 | COK | de | bmo | +0.00 | 3.5 | 50 | +0.00 | yes | est. |
| 9 | TFIN | it | bmo? (likely amc; pinned to a cash bid) | −0.05 | 0.3 | 45 | −0.03 | no | est. |
| 10 | MN | it | bmo? (in-session) | −0.20 | 3.0 | 47 | −0.18 | no | est. |
| 11 | VH2 | de | bmo? | −0.20 | 3.5 | 47 | −0.21 | yes | est. |
| 12 | BRBY | uk | bmo? (07:00 pattern) | −0.50 | 7.0 | 47 | −0.42 | yes | observed_rns |
| 13 | BKHT | de | bmo | −0.60 | 5.0 | 47 | −0.30 | no | est. |
| 14 | ENDUR | no | bmo (07:00 CET) | −0.60 | 5.0 | 48 | −0.20 | no* | observed_newsweb |
| 15 | GENO | no | bmo (07:00) | −0.70 | 9.0 | 47 | −0.54 | no | observed_newsweb |
| 16 | XPLRA | no | bmo | −0.70 | 9.0 | 45 | −0.90 | no* | observed_newsweb |
| 17 | GLJ | de | bmo? (07:03 pattern) | −1.70 | 5.5 | 44 | −0.66 | yes | est. |
| 18 | SYNSAM | se | bmo | −2.00 | 6.0 | 40 | −1.20 | no | est. |
| 19 | SIE | de | bmo | −2.20 | 6.0 | 42 | −0.96 | no | est. |

`impact_scaled` is the hunter's second, separate measurement: (2·p_up/100 − 1)·abs_move. It is not the key, and nothing should be ranked on it. SMWH is the one name where the two disagree in sign: the findings are small positives (peer trading, cost levers, an 11.48% short), while p_up sits below 50 because this name fell on all three guidance events in the past year.

\* The baselines read 0.0 for XPLRA and ENDUR because the register's issuer name failed to join. Their hunters found Finanstilsynet positions of **2.48%** (XPLRA: Citadel, Two Sigma, Liontrust; built from 1.50% in September) and **0.51%** (ENDUR, listed as "ENDÚR": JPMorgan AM, since 14 Oct). The sealed baselines are left as sealed.

**Not ranked:** CAR (pl). The vendor's 2026-11-12 date is a **phantom**: Inter Cars' own ESPI schedule (RB 2/2026) puts the Q3 report on **2026-11-17**, probably after the close (https://www.stockwatch.pl/komunikaty-spolek/intercars,terminarz-raportow-2026-01-26,espi,20260126_171200_0000340159). Poland has no day archive, so this cannot be written as `event_occurred: false` by the resolver; it rests on the issuer's own filing.

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing. All four members ran and none used a fallback. Selection rule: 3 of 4 judges put the name in their own top 20%. How the judges read their inputs:

- Sonnet 5.5 read the shared core and `LESSONS.md` in full, but only the first part of the Nordic definition, and did not open the DE, UK or IT definitions.
- Opus 5 read the DE definition in full and applied the shared core to the other markets.
- Opus 5.5 and Fable 5.1 read only the market-specific sections of the IT and UK definitions (Fable 5.1 also of the Nordic one).

| rank | ticker | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SYNSAM | **yes** | 92 | short | 5 | 92S* | 96S* | 84S* | 96S* | 4 | −2.00 | −2.00 |
| 2 | SIE | **yes** | 87 | short | 6 | 85S* | 91S* | 78S | 92S* | 3 | −1.53 | −2.20 |
| 3 | XPLRA | **yes** | 83 | short | 7 | 75S | 82S* | 81S* | 94S* | 3 | −1.29 | −0.70 |
| 4 | VBK | | 72 | long | 10 | 84L* | 65L | 60L | 80L* | 2 | +1.05 | +0.50 |
| 5 | GLJ | | 58 | short | 17 | 34S | 82S* | 56S | 60S | 1 | −0.76 | −1.70 |
| 6 | GENO | | 46 | short | 45 | 40S | 74S | 26L | 94S* | 1 | −0.74 | −0.70 |
| 7 | SMWH | | 58 | long | 16 | 70L | 74L | 56L | 34L | 0 | +0.86 | +1.00 |
| 8 | BRBY | | 46 | short | 12 | 56S | 52S | 51S | 26S | 0 | −0.67 | −0.50 |
| 9 | ENDUR | | 39 | short | 10 | 54S | 43S | 28S | 34S | 0 | −0.46 | −0.60 |
| 10 | REY | | 33 | long | 9 | 39L | 36L | 18L | 40L | 0 | +0.43 | +0.45 |
| 11 | VH2 | | 26 | short | 3 | 30S | 28S | 24S | 23S | 0 | −0.32 | −0.20 |
| 12 | OHB | | 17 | long | 35 | 40S | 18L | 56L | 34L | 0 | +0.31 | +0.50 |
| 13 | DIB | | 26 | long | 21 | 59L | 0- | 26L | 19L | 0 | +0.29 | +0.20 |
| 14 | KAR | | 21 | long | 13 | 42L | 13L | 10L | 18L | 0 | +0.19 | +0.10 |
| 15 | BKHT | | 18 | short | 16 | 42S | 13S | 0- | 15S | 0 | −0.19 | −0.60 |
| 16 | MN | | 12 | short | 10 | 7S | 28S | 4S | 9S | 0 | −0.13 | −0.20 |
| 17 | 1U1 | | 6 | long | 20 | 34L | 8L | 8L | 23S | 0 | +0.13 | +0.30 |
| 18 | TFIN | | 3 | short | 2 | 5S | 4S | 4S | 0- | 0 | −0.03 | −0.05 |
| 19 | COK | | 3 | long | 5 | 12L | 0- | 0- | 0- | 0 | +0.00 | +0.00 |

Each judge's own top 20% starts at: opus5 |1.12|, opus55 |0.80|, sonnet55 |0.70|, fable51 |0.96|, each read against 200 live sizes.

**SYNSAM (selected, short, 4 of 4).**

- GfK's Swedish optical panel for Jul–Sep 2026 shows the market flat: total SEK 3,115m against 3,118m, spectacles −0.1%, after +5.9% in Q2 (https://optikbranschen.se/wp-content/uploads/2026/11/2026-Q3.pdf). It is an image-only trade-association PDF with no wire copy.
- Synsam has outgrown that panel by 1.8–3.0 points a quarter, which puts Sweden (about half of sales, the highest margin) at roughly 2–3% organic against 8.9% in Q2. The CEO said in August the Q2 trend was continuing into Q3.
- The 5-estimate Modular consensus (sales SEK 1,885m, +8.9%) sits above Nordea, the one note that read the panel, and the stock rose 12.9% over 20 days.
- **The case against:** Nordea had already seen the data ("optikmarknaden krympte något", the optical market shrank slightly); NOK translation adds about +2.3 points; the buyback runs at about 12% of volume. Opus 5 also kept Fielmann's Q3 (+5.1%, guidance confirmed), which the hunter had dropped, as an offsetting finding. There is no positioning anchor.

**SIE (selected, short, 3 of 4).**

- Siemens' own compiled consensus has FY26 EPS pre-PPA at €11.68, above the top of the company's raised €11.20–11.50 guide. A Q4 inside the guide therefore misses the bar.
- The FY27 first guide is the line the reaction turns on. Last year's first guide closed −9.35% on the day and was later raised twice. RBC and JPMorgan (9 Nov; JPMorgan took Siemens off its focus list) expect the outlook to be at best in line.
- **The case against:** electrification peers were strong (ABB comparable orders +40%, Schneider organic +16.9% with guide raised), no ad-hoc or pre-release has been filed, and the run-up is flat. Sonnet 5.5 is the one judge that does not put it in its top 20%.

**XPLRA (selected, short, 3 of 4).**

- The only sourced bar is Redeye's preview of 5 Nov, which cites consensus of NOK 525m sales and EBIT 40m, while Redeye itself sits 22% below consensus on EBITDA.
- NOK is about 9% stronger against EUR year on year, and the emporia consolidation is loss-making.
- **The case against:**
  - The bar comes from a single source.
  - Nordea raised its 2026–28 EBITDA estimates by 24–41% on 3 Nov.
  - The 2.48% short (Citadel, Two Sigma, Liontrust; about 12 days of volume) is squeeze fuel if the print surprises up.
  - The last two prints moved −9.6% and −31% on a roughly $224k-a-day stock.

**Where the panel and the hunter disagree most.** Nothing crosses the floor, so there is no unselected floor-clearer.

- **GLJ** has the hunter's third-largest number (−1.70), but only Opus 5.5 puts it in its top 20% (panel_pct 58).
- **VBK** is the hunter's +0.50 (rank 3), and the panel's largest long (72). Two judges (Opus 5, Fable 5.1) put it in their top 20%, on CropEnergies' and Green Plains' ethanol margins over Verbio's Q1 months.
- **GENO** has the widest split (sd 45): Fable 5.1 sizes it at its 94th percentile short, Sonnet 5.5 leans long.
- **OHB**: Opus 5 is short and the other three are long (sd 35). Opus 5 signed the findings by this name's habit of selling good news.

**What these numbers are not.** `panel_score` ranks; it does not forecast. There is no `expected_edge_pct` off the US. `p_up` is recorded and decides nothing. Each member's scale is still mostly the frozen E-P seed until Europe has about 200 panel names of its own. The EU panel has no measured edge: ρ +0.22, p 0.19 on 45 names (2026-10-21). In the four-model re-judge the judges ranked Europe better than the live hunt, but nothing about this market's panel is established. The three selected names are all short and from two markets (Sweden, Norway) plus Germany's largest name, so they do not share one macro read, but they do share one direction.

## Top and bottom names in the hunter ranking

- **SMWH (+1.00).** The FY26 year was pre-released on 16 Sep (headline pre-tax profit about £75m against RBC's £78m). What is new is the first FY27 guide and the new Executive Chair's priorities. The positives are peers firming after the pre-close (SSP UK & Ireland LFL +9% for Jul–Sep), the documented cost levers and a crowded 11.48% short. No FY27 consensus could be sourced, so every size is capped small.
- **SIE (−2.20)** and **SYNSAM (−2.00)**: see the panel paragraphs above.

## Session corrections: read these before resolving

The sweep does not run in this stage, so sessions marked `bmo?` were assumed. Hunters cite timestamps for most of them:

- **DIB** (Digital Bros): it releases after the Milan close (Q1 FY26 at 17:36 UTC; 9M at 19:09 CEST). The sealed bmo window holds no print. Window: close 12 Nov → close 13 Nov.
- **TFIN** (Trevi): likely late afternoon. It does not matter here, because the stock is pinned to Webuild's unconditional €5.165 cash OPA (acceptance to 20 Nov).
- **REY** (Reply) and **MN** (Mondadori) release inside the session (Reply around 12:30–14:00 CET, Mondadori around 13:30–14:30). The sealed window holds the whole reaction.
- **VH2** (Vorwerk): the report has no timestamp, and the call is at 17:00 CET. The Q3 numbers were already pre-released by ad-hoc on 21 Oct, together with a second guide raise.
- Hunters confirmed bmo from the issuer's own calendar or release stamps for 1U1, BRBY, ENDUR, GENO, GLJ and VBK.

## What this day is, and what it is not

- **Selection:** a random sample of 20 from 116 eligible names, seed `eu-2026-11-12`; 190 names were scheduled across the ten markets above the $100k floor.
  - Hunted by market (`by_market`): de 8, it 4, no 3, uk 2, se 2, pl 1; fr, dk, fi and es 0.
  - Eligible by market: de 48, it 22, uk 12, se 12, no 9, es 5, pl 3, fr 2, dk 2, fi 1.
  - No market was closed.
- **Market concentration:** Germany is the largest at 40% (8 of 20), and 6 markets are represented. This is a German-weighted day; the German names include Siemens, and the industrial names share its macro read.
- **Calendar sources:** UK RNS calendar read (18 dated), Yahoo read in all ten markets, and EQS events, Inderes and Euronext Oslo all read. Bankier (pl) read `unavailable` (HTTP 403); that is the calendar CAR came from without an issuer check.
- **Options:** null in all ten markets. Europe runs in the anchor-less regime, which on the sealed US corpus produced ρ +0.073, p 0.45 over 104 events.
- **Short registers:**
  - Resolved: de, it, no, se and uk. pl: none reachable.
  - **5 of 20 names carry `anchor_covered: true`**: BRBY 4.98%, SMWH 11.48%, COK 6.19%, GLJ 1.12% and VH2 1.7%. Every other zero is a truncated zero at the 0.5% threshold, not an anchor, apart from the two Norwegian joins the hunters corrected (XPLRA, ENDUR).
- **Spain and Poland:** 1 name (CAR, pl) has no positioning anchor and cannot be confirmed or killed after the fact; it is the day's phantom anyway.
- **Germany:** 8 names cannot reach `event_occurred: false`; neither can the 4 Italian ones.
- **Nordic resolve deadline:** the Swedish names (SYNSAM, KAR) must be resolved within about a week, because of the Nasdaq Nordic feed's paging limit. Norway's NewsWeb has a true day query.
- **History basis:** UK (BRBY, SMWH) is `observed_rns`, and Norway (ENDUR, GENO, XPLRA) is `observed_newsweb`. **The other 15 are `estimated_from_cadence`**: a scale, not a record of dates. KAR's hunter replaced it with an observed table from Swedish Finwire copy.
- **Lean:** the lean's weights are priors borrowed from the US runs and measured nowhere in Europe. The last value of `lean_vs_free_control_rho` on record is se 0.60 (resolved run of 2026-10-16).
- **Already public vs new in release:**
  - Pre-released or guided: COK (Q3 ad-hoc of 26 Oct and revenue guide cut), VH2 (all of Q3 on 21 Oct, guide raised), SMWH (FY26 pre-close), 1U1 (the €60m one-off and reported-EBITDA guide on 10 Sep), BKHT (now mostly a cash holding).
  - Likely guidance lines, where the hunters put the move: SIE (first FY27 guide), SMWH (first FY27 guide), GLJ (new-business and earnings guides stretched), GENO (NOK 1.5bn revenue target), BRBY (FY27 outlook restated), 1U1 (service-revenue guide), BKHT (IHSE guide).
- **What the local-language sources added (`language_note` highlights):**
  - SYNSAM: the load-bearing GfK panel exists only as a Swedish PDF, and the Nordea preview and Modular consensus are in Swedish wire copy.
  - SIE: the RBC and JPMorgan preview notes came through German dpa-AFX copy.
  - 1U1: the parent's 6m-share standing buy order, a broadband price rise and the IR note on the stale consensus were German-only.
  - CAR: only the Polish ESPI filings carried the correct report date.
  - TFIN: the whole bid structure (mandatory conversion, ICOP's no-raise) was Italian-only.
  - XPLRA: Norwegian press named Two Sigma as short, which led the hunter to the register.
- **Controls:** the `pre_lessons` freeze ran on all 20 hunts. The `pre_local` control is retired, so `eu_resolve.py`'s language-pass section will report 0 names.
- **Provenance:** uk.v7, de.v7, nordic, it and pl definitions, all on claude-opus-5-5 (alias timeline); see `provenance.json`.
- **One day is not a result.**

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

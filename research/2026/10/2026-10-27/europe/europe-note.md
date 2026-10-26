# Stage EU — Europe ranking for 2026-10-27

**No name clears the 2.8 conviction floor.** The hunters' keys run from VNV +0.80 down to VRLA −2.00, so the whole day sits inside ±2. **The panel selected one name: VRLA (Verallia) short, 3 of 4 judges in their own top 20%, `panel_pct` 79, spread 4.** It is also the hunters' own most negative name, so on this day the panel and the hunt agree at the bottom. **But VRLA releases after the Paris close**, so the window that holds its reaction is close(10-27) → close(10-28), not the sealed one.

**The universe.**
- 57 names were scheduled for Tuesday 2026-10-27 and 40 cleared the $100k turnover floor.
- 20 were drawn at the cap, by a random sample seeded `eu-2026-10-27` among the eligible names (`selection.method`).
- Drawn by market (`by_market`): fi 5, se 4, de 3, no 2, pl 2, and uk, fr, it, es 1 each.
- Eligible by market: se 10, fi 8, pl 5, fr 4, no 4, de 3, uk 2, it 2, es 2, dk 0.
- **Concentration:** the largest market is Finland at 25% (`selection.market_concentration`). Nine markets are represented and the Nordics are 11 of 20 names, so this is a Nordic-heavy day but not a one-market day.

**The ranking key and the sealed spots.**
- The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`.
- Sealing took place on Monday 2026-10-26 at about 13:50 UTC, while the European markets were still open. **Every sealed spot and run-up is therefore an intraday price, not a close.**

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session, sealed → per the hunter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | VNV | VNV Global | **+0.80** (p59) | no | +0.66 | 5.5 | 56 | bmo → bmo (invitation; last three at 08:00 CET) |
| 2 | de | VIB3 | Villeroy & Boch pref | **+0.60** (p50) | no | +0.18 | 4.5 | 52 | bmo? → bmo by pattern (last three at 08:00) |
| 3 | se | ASSA_B | ASSA ABLOY B | **+0.40** (p36) | no | +0.50 | 5.0 | 55 | bmo → bmo (08:00 per calendar) |
| 4 | no | ELO | Elopak | **+0.40** (p36) | no | +0.36 | 6.0 | 53 | bmo → bmo (07:00 CET, NewsWeb invitation) |
| 5 | se | PREV_B | Prevas B | **+0.40** (p36) | no | +0.48 | 8.0 | 53 | bmo → bmo (08:30 CET, invitation) |
| 6 | uk | HSBA | HSBC Holdings | **+0.10** (p14) | no | +0.20 | 5.0 | 52 | bmo → bmo (07:00 London precedent) |
| 7 | fi | TIETO | Tieto | **0.00** (p5) | no | −0.28 | 7.0 | 48 | bmo → bmo (08:00 per MFN calendar) |
| 8 | fi | TYRES | Nokian Tyres | **0.00** (p5) | no | +0.18 | 9.0 | 51 | bmo → **~13:00 EET, in session** (issuer notice) |
| 9 | pl | KRU | KRUK | **−0.20** (p20) | no | −0.24 | 6.0 | 48 | bmo? → **amc** (four interim reports since 3Q25 at 17:13–17:19) |
| 10 | no | SATS | SATS | **−0.20** (p20) | no | 0.00 | 6.5 | 50 | bmo → bmo (07:00 CET, NewsWeb invitation) |
| 11 | de | P911 | Porsche AG | **−0.30** (p29) | no | +0.33 | 5.5 | 53 | bmo → bmo (documents 07:30 CET, IR page) |
| 12 | pl | BDX | Budimex | **−0.40** (p36) | no | −0.30 | 7.5 | 48 | bmo? → **amc, inferred** (last two quarterlies 18:18 and 19:33) |
| 13 | fi | FIA1S | Finnair | **−0.50** (p43) | no | −0.32 | 4.0 | 46 | bmo → bmo (09:00 EET, issuer calendar) |
| 14 | se | HANZA | Hanza | **−0.50** (p43) | no | −0.28 | 7.0 | 48 | bmo → bmo (07:30, MFN) |
| 15 | fi | GOFORE | Gofore | **−0.60** (p50) | no | −0.33 | 5.5 | 47 | bmo? → bmo by pattern; time not found |
| 16 | it | YACHT | Ferretti | **−0.70** (p55) | no | −0.48 | 6.0 | 46 | bmo? → **in session** (past filings 09:39–11:27 CET) |
| 17 | fi | GRK | GRK Infra | **−0.80** (p59) | no | −0.75 | 7.5 | 45 | bmo → bmo (~08:30 EET, invitation) |
| 18 | es | ENC | Ence | **−0.90** (p63) | no | −0.36 | 6.0 | 47 | amc → amc ("a cierre de mercado", issuer filing) |
| 19 | de | BEI | Beiersdorf | **−1.40** (p76) | no | −0.80 | 5.0 | 42 | bmo? → bmo (webcast 09:00) |
| 20 | fr | VRLA | Verallia | **−2.00** (p87) | no | −0.72 | 6.0 | 44 | bmo? → **amc** ("communiqué de presse après bourse", issuer calendar) |

How to read the table:
- `impact_scaled` is the hunter's second, separate measurement. It is not the key, and the floor does not apply to it.
- Bracketed figures are percentiles of |value| among 610 names sized by Opus 5.5. They describe scale, not rank.
- Ties (ASSA_B/ELO/PREV_B, TIETO/TYRES, KRU/SATS, FIA1S/HANZA) carry no order.
- **P911's two numbers disagree in sign.** Its findings net −0.3, but `p_up` 53 from a company-steered low bar gives +0.33.
- **TYRES's two numbers disagree in sign.** Its findings net 0.0 and `p_up` sits at 51.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.**
- All four ran on their own pinned `-intl-` agents, with no fallback, and each covered 20 of 20 packs.
- Selection rule for this market: `consensus`, 3 of 4 judges in their own top 20%.
- Each judge's top 20% starts at Opus 5 |1.80|, Opus 5.5 |0.90|, Sonnet 5.5 |0.72| and Fable 5.1 |1.10|. Those thresholds come from 130 live sizes per member, taken from runs before this one.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | VRLA | **yes** | 79 | short | 4 | 74S | 83S* | 82S* | 76S | 3 | −1.16 | −2.00 |
| 2 | ENC | no | 72 | short | 19 | 41S | 88S* | 83S* | 76S | 2 | −1.15 | −0.90 |
| 3 | GRK | no | 80 | short | 10 | 71S | 73S | 82S* | 95S* | 2 | −1.14 | −0.80 |
| 4 | PREV_B | no | 79 | long | 8 | 67L | 88L* | 83L* | 76L | 2 | +1.12 | +0.40 |
| 5 | BEI | no | 74 | short | 10 | 63S | 85S* | 83S* | 66S | 2 | −1.03 | −1.40 |
| 6 | VNV | no | 68 | long | 9 | 63L | 58L | 83L* | 66L | 1 | +0.88 | +0.80 |
| 7 | ELO | no | 59 | long | 20 | 45L | 82L* | 33L | 76L | 1 | +0.80 | +0.40 |
| 8 | BDX | no | 58 | short | 13 | 35S | 64S | 69S | 63S | 0 | −0.80 | −0.40 |
| 9 | GOFORE | no | 51 | short | 14 | 32S | 66S | 43S | 63S | 0 | −0.67 | −0.60 |
| 10 | YACHT | no | 51 | short | 6 | 48S | 58S | 43S | 54S | 0 | −0.63 | −0.70 |
| 11 | ASSA_B | no | 36 | long | 10 | 34L | 26L | 33L | 52L | 0 | +0.44 | +0.40 |
| 12 | TIETO | no | 36 | short | 10 | 22S | 39S | 32S | 48S | 0 | −0.44 | 0.00 |
| 13 | FIA1S | no | 28 | short | 10 | 12S | 30S | 39S | 29S | 0 | −0.39 | −0.50 |
| 14 | VIB3 | no | 27 | long | 9 | 28L | 30L | 36L | 12L | 0 | +0.39 | +0.60 |
| 15 | TYRES | no | 18 | long | 38 | 42S | 30L | 62L | 22L | 0 | +0.35 | 0.00 |
| 16 | HANZA | no | 13 | short | 30 | 55S | 30L | 6S | 22S | 0 | −0.22 | −0.50 |
| 17 | HSBA | no | 9 | short | 8 | 2L | 17S | 3S | 18S | 0 | −0.15 | +0.10 |
| 18 | P911 | no | 12 | short | 18 | 8S | 10L | 39S | 10S | 0 | −0.14 | −0.30 |
| 19 | SATS | no | 8 | long | 9 | 2L | 23L | 6L | 0 | 0 | +0.11 | −0.20 |
| 20 | KRU | no | 1 | short | 27 | 26L | 23L | 39S | 15S | 0 | +0.04 | −0.20 |

Each member's figure is its percentile (0–100) against its own live range: L is long, S is short, and `*` marks the member's own top 20%. On VRLA the judges' raw sizes were Opus 5 −1.44 (`p_up` 38), Opus 5.5 −0.98 (43), Fable 5.1 −0.96 (42) and Sonnet 5.5 −0.80 (41).

**VRLA, selected short (3 of 4, `panel_pct` 79, spread 4).**
- **What the judges name:**
  - The company wrote the ~€700m 2026 EBITDA guide subject to no significant deterioration in the Middle East. The original reads: "Sous réserve de l'absence d'une détérioration significative de la situation au Moyen-Orient, Verallia réaffirme ses perspectives 2026" (H1 release, https://fr.ftp.opendatasoft.com/datadila/INFOFI/BWR/2026/07/FCBWR168876_20260728.pdf).
  - French PEG gas for November has since gone from about €44 to €85.88/MWh, and Cal-27 from €55.95 to €70.06 in three weeks (https://selectra.info/energie/actualites/prix-gaz/2026-10-19).
  - Q2's margin slipped to 21.4% from 22.5%, with the inflation spread turning negative.
  - O-I Glass, whose Q2 European operating profit fell 93%, reports its Q3 hours later inside the same amc window.
  - The free float is about 15%: BWGI holds 77.17%.
- **Strongest case against:**
  - More than 80% of 2026 energy is hedged.
  - The stock rose about 12% off the 1 October sector low while gas rose, so the market may already be pricing pass-through.
  - A guide cut at Q3 2025 moved the stock only −0.35%.
  - No Q3 consensus was sourced, so the bar is the company's own arithmetic.
  - The Capital Markets Day on 18 November is the more natural venue for any 2027 energy statement.

**Where the panel and the hunt part.**
- **PREV_B:** the hunter put it at +0.40, while two judges put it in their own top 20% long (`panel_pct` 79). The judges weigh the peer utilisation read against a freshly lowered single-analyst bar more than the hunter did.
- **GRK:** the hunter put it at −0.80; Fable 5.1 put it at its 95th percentile short. The judges size the 6 October regulatory halt of the Google Muhos/Kajaani earthworks harder.
- **ENC:** the hunter put it at −0.90. Opus 5.5 and Sonnet 5.5 have it in their top 20% short; Opus 5 does not (41).
- **Opposite signs:** HSBA (hunter +0.10, panel short 9) and SATS (hunter −0.20, panel long 8) disagree in sign, but both are near zero on both measures. KRU's members split 2–2 on side.

**What the panel numbers are not.**
- `panel_score` ranks and does not forecast, and there is no `expected_edge_pct` off the US.
- Certainty (`p_up`) is recorded and decides nothing.
- Each member's scale still leans on the frozen E-P seed until Europe has about 200 panel names of its own; today it has 130 live sizes per member.
- In the four-model re-judge the judges ranked Europe better than the live hunt (ρ +0.33/+0.34 on 48 names). That is a development number, not a result: nothing about this market's panel is established.

## Sessions: four of the twenty are probably on the wrong window

- **VRLA, KRU and BDX were sealed `bmo?` (`session_unresolved`), and their hunters found that each reports after the close.**
  - VRLA: the issuer's own calendar says "après bourse".
  - KRU: MFN timestamps of 17:13–17:19 Warsaw.
  - BDX: inferred from two prior 18:18 and 19:33 releases. Budimex's own time for 27 October was not observed.
  - **For all three, the sealed close(10-26) → close(10-27) window holds no release.** Because the rows are `session_unresolved`, `eu_resolve.py` measures BOTH windows, and the amc one, close(10-27) → close(10-28), is the one to read.
- **ENC** was sealed amc and confirmed amc, so its window is close(10-27) → close(10-28).
- **Releases inside the session:** TYRES (~13:00 EET) and YACHT (Milan intraday, after the Hong Kong close) release during the session. The sealed window still contains the whole reaction.
- **Bmo by pattern only:** GOFORE, VIB3 and BEI rest on the issuer's pattern or a webcast time rather than a stated release timestamp.

## What every European note must say

- **Options:** `options` is null in all ten markets. **Europe runs in the anchor-less regime**, the one that produced ρ=+0.073, p=0.45 over 104 events on the sealed US corpus.
- **Short registers read for de, fi, fr, it, no, se and uk. Spain and Poland have none.** Only 3 of 20 names carry `anchor_covered: true`:
  - BEI 0.51%;
  - HANZA 1.2%, slightly covering;
  - TYRES 3.18%, flat.

  Every other name read a truncated zero, which is not an anchor. The KRU hunter separately read the Polish register through a mirror (rksgpw.com) at 2.21% and building. That is hunter evidence; it is not in the baseline.
- **Spain and Poland: 3 names** (ENC, BDX, KRU). They have no positioning anchor and no reachable day archive, so they can never be confirmed or killed after the fact.
- **Germany: 3 names** (BEI, P911, VIB3). They cannot reach `event_occurred: false` either, and nor can France (VRLA) or Italy (YACHT).
- **Nordic resolve deadline: 9 names from se and fi** (ASSA_B, HANZA, PREV_B, VNV, FIA1S, GOFORE, GRK, TIETO, TYRES). **Resolve this run within about a week** or their confirmations go null.
- **`lean_vs_free_control_rho`:** the latest resolved European run is 2026-10-16. It reports this only for se, at 0.60. **The lean's weights are priors borrowed from the US runs and have been measured nowhere in Europe.**
- **History basis:** only HSBA (`observed_rns`) and ELO and SATS (`observed_newsweb`) carry observed announcement dates. **The other 17 carry `estimated_from_cadence`, which is a scale, not a record of dates.** Several hunters found the estimated scale understated the name's real report-day moves; ASSA_B, PREV_B, VNV and TIETO each say so.
- **Above the floor:** none of the 20. Over the whole US sample the sign was a coin flip below the floor.
- **Already pre-released (`already_public`):**
  - FIA1S: positive profit warning on 13 October, with Q3 revenue and comparable EBIT plus a raised FY guide.
  - KRU: estimated Q3 net profit released 16 October.
  - VIB3: guide cut and dividend cap by ad-hoc on 18 September.

  On the first resolved days, a pre-released period moved 3.1% against 7.4% when the numbers were new.
- **Likely guidance change (`new_in_release`):** P911 (revenue and BEV-share guide likely trimmed), YACHT (needs H2 growth), GRK (narrowing of 70–95 MEUR), VRLA (the conditional guide), BDX (new strategy with Q3), TIETO and TYRES (narrowing), KRU (the 2.5 bn PLN investment target is out of reach).
- **Nobody re-judged anything here; one day is not a result.**

## Top and bottom, with the finding behind each

- **Top, VNV +0.80.** Voi is 21.9% of VNV's portfolio. Voi's own Q3 report (22 October, p.5) attributes a jump in its incentive cost to "a higher company valuation following Lime's IPO, higher peer-group multiples and the strong performance in 2026", which points to a markup of the stake (https://attachment.news.eu.nasdaq.com/a9f27c00e6682f573e340d5a5a3852937). It is partly priced: VNV is up 7.9% since Voi reported.
- **Bottom, VRLA −2.00.** The conditional guide against doubled French gas, as above (guidance −1.5), plus Q2 margin arithmetic (−0.4) and an O-I read-across inside the window (−0.5).
- **Next, BEI −1.40.** Goldman relays Nielsen data showing NIVEA −6% in Europe over the 12 weeks to 6 September, against a Visible Alpha Consumer bar of −1.0% organic (10 analysts). The stock ran +11.6% into the print and sits above the mean target.

## Language notes worth quoting

- **GRK:** the Muhos/Kajaani halt order was carried only by Finnish regional press (Kaleva), and GRK's English releases never name the site. The link to GRK comes via a local paper and Inderes and is unverified in a primary document.
- **YACHT:** the CEO's internal letter, "il miglior autunno nella storia di questa azienda" ("the best autumn in the company's history"), appeared only in Il Resto del Carlino.
- **P911:** Jefferies' read of the pre-close call, "überwiegend negativ" ("predominantly negative"), appeared only in German.
- **BDX:** the CEO's statement that the strategy comes "wraz z publikacją wyników za trzeci kwartał" ("together with the publication of the Q3 results") was found only in Polish.
- **Nordic names:** most hunters reported that the Swedish, Finnish and Norwegian sources added little beyond the bilingual filings, which is the expected answer there.

## Not ranked

None. All 20 drawn names were hunted and all 20 are rankable. No hunt returned empty.

## Process

- Fired 13:35 UTC; session started 13:45 UTC.
- **Hunters:** one per name, in four waves capped at eight concurrent subagents. All twenty used their market's own agent, with the Nordic hunter told its submarket.
- **Panel:** four judges in one wave.
- **Publishing:** everything was published to `main`.
- **Orders:** this stage places no orders and reads no broker.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

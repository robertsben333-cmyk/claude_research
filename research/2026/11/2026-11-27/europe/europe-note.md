# Stage EU — Europe ranking for 2026-11-27 (Fri)

Sealed Thursday 2026-11-26 at about 14:40 UTC, while the European markets were still trading. The sealed spots are **intraday prices, not closes**. The event date is Friday 2026-11-27.

**Answer first: an eleven-name day spread over four markets, almost half of it Oslo, and the hunters found nothing large.** No name clears the 2.8 conviction floor. The largest |impact_sum| is DDRIL at −1.50. **The panel selects three names:**
- **DDRIL** short, panel_pct 92, 4 of 4 judges in their own top 20%
- **NTT** long, 89, 4 of 4
- **MDV** long, 82, 3 of 4

The IBKR handoff (rule: panel_pct ≥ 70 with all four judges) carries all three: SELL DDRIL, BUY NTT and BUY MDV. **One day is not a result.**

**Read this before the panel table.** Two names have no print in the window and are not ranked: **NORAM** published Q3 on 11-24, and **RVRC** published Q1 on 11-19. For RVRC, 11-27 is the ex-dividend day for SEK 1.50, about −2.8% on the unadjusted close. **Four Polish names release after the close by their issuers' pattern: MDV, NTT, PLW and VGO.** Their reaction falls in close(11-27) → close(11-30), not in the sealed bmo window. Two of those four are panel selections. A position held only to the executor's 15:35 Amsterdam flatten on 11-27 exits **before** their print.

## Ranked on `impact_sum` (the key, per `edge-scores.json` `ranking_key`)

| # | ticker | mkt | session (hunter's check) | impact_sum | floor | impact_scaled | abs_move | p_up | already public | new in release |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | MDV | pl | **amc** (Q1 17:55, H1 ~22:00 precedent) | +0.40 (p40) | no | +0.30 | 5.0 | 53 | **Q3 pre-released** 6 Nov (rev 3.20bn PLN, adj. EBITDA 450m); early-Nov LFL | likely November sales update; cash flow and net debt |
| 2 | PLSV | no | bmo (~07:00 CET, issuer invite) | +0.40 (p40) | no | +0.09 | 4.5 | 51 | Fontis sale; bond paydown; Jade/Safira awards; CFO exit; Seagems review | Q3 against FY EBITDA guide $175–190m |
| 3 | VGO | pl | **amc** (Q3'25 17:10, H1 17:52 precedent) | +0.40 (p40) | no | +0.36 | 4.5 | 54 | **Q3 revenue pre-released** 14 Oct (34.5m PLN, +48%) | Q3 EBITDA/margin only |
| 4 | PLW | pl | **amc** (pattern; no timestamp yet) | +0.10 (p14) | no | +0.18 | 4.5 | 52 | H1; CMS slip to Q1 2027 | Q3 numbers (nothing pre-released) |
| 5 | VTURA | no | bmo (before Oslo open, issuer) | +0.10 (p14) | no | +0.27 | 4.5 | 53 | ENH all-share LOI 5.50x (11 Sep) | Q3; capex re-estimate; deal status |
| 6 | GXI | de | bmo? (date per EQS notice, no time) | −0.30 (p32) | no | −0.07 | 3.5 | 49 | **H1 pre-released** 30 Sep; 9M 30 Oct; FY guide reiterated | delayed final H1 report: cash flow, net debt, outlook wording |
| 7 | NTT | pl | **amc** (H1 at 20:46 precedent) | −0.30 (p32) | no | +0.72 | 9.0 | 54 | H1; peer Action Q3 ~4x | Q3 numbers (nothing pre-released); cash flow |
| 8 | ENH | no | bmo (06:00 CET, issuer invite) | −0.40 (p40) | no | −0.09 | 4.5 | 49 | 2026 distribution guide; Ventura LOI | Q3; rig contract cover for 2027 |
| 9 | DDRIL | no | bmo (07:30 CET, issuer notice) | −1.50 (p85) | no | −1.04 | 6.5 | 42 | Blackford sale; "Borgland on contract from Nov 2026" guide | Q3 (not pre-released); **Borgland start date** |

Not ranked: **NORAM** (hunter found no event on this date: Q3 out 2026-11-24 17:13 UTC, https://newsweb.oslobors.no/message/687324) and **RVRC** (Q1 out 2026-11-19 07:30 CET, https://view.news.eu.nasdaq.com/view?id=b6ce67ae034d1ae607c54745ed4a58807&lang=en&src=listed; next report 2027-02-11). The resolver should set `event_occurred: false` on both. The RVRC ex-dividend drop must not be scored as a reaction.

**NTT is the one name whose two measurements disagree in sign:** its findings sum to −0.30, but `impact_scaled` is +0.72. The hunter's `p_up` of 54 also counts the four straight positive next-session reactions to its prints.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran, with no fallback. Each judge's own top 20% starts at |0.98| (Opus 5), |0.68| (Opus 5.5), |0.56| (Sonnet 5.5) and |0.80| (Fable 5.1), measured on 200 live sizes each.

| rank | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DDRIL | bmo | **yes** | 92 | short | 6 | 98S* | 96S* | 82S* | 92S* | 4 | −2.00 | −1.50 |
| 2 | NTT | amc (hunter) | **yes** | 89 | long | 4 | 92L* | 92L* | 88L* | 82L* | 4 | +1.55 | −0.30 |
| 3 | MDV | amc (hunter) | **yes** | 82 | long | 8 | 70L | 86L* | 91L* | 82L* | 3 | +1.21 | +0.40 |
| 4 | ENH | bmo | no | 60 | short | 9 | 62S | 52S | 54S | 74S | 1 | −0.66 | −0.40 |
| 5 | VGO | amc (hunter) | no | 65 | long | 8 | 74L | 58L | 73L | 56L | 0 | +0.77 | +0.40 |
| 6 | GXI | bmo? | no | 39 | short | 4 | 38S | 37S | 46S | 34S | 0 | −0.37 | −0.30 |
| 7 | PLSV | bmo | no | 16 | long | 33 | 40S | 37L | 46L | 20L | 0 | +0.29 | +0.40 |
| 8 | PLW | amc (hunter) | no | 25 | long | 10 | 40L | 29L | 12L | 20L | 0 | +0.24 | +0.10 |
| 9 | VTURA | bmo | no | 18 | long | 18 | 48L | 9L | 0- | 14L | 0 | +0.14 | +0.10 |

`*` = in that judge's own top 20%.

**DDRIL short (92, 4/4).** All four judges rest on one item. Two AIS services (https://www.vesselfinder.com/vessels/details/8758469 and Maritime Optima) put the Borgland Dolphin moored in Las Palmas with no destination on 26 Nov. The company's own Pareto deck of 16 Sep (https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=682425) guided it "on contract from November 2026". There is a second, small item: a book loss on the Blackford sale, USD 10m cash plus 15m contingent against an 18m book value. **The case against:** "on contract" may count from departure, so a slip of a few weeks can sit inside the guide. The stock ran +10.3% over 5 days into the print. It is a two-analyst, $0.3m-a-day name with no register anchor. Opus 5 sized it at −3.20, about twice the other three.

**NTT long (89, 4/4).** The judges cite peer Action's Q3 2026 net profit of 35.8m PLN, about 4x a year earlier (https://xyz.pl/?p=276886, original: "To czterokrotny wzrost zysku w porównaniu z III kw. 2025 r."). They also cite management's H1 language on margins carried by cheaply bought inventory. Nobody covers the name, so no Q3 number exists to be priced. **The case against:** Q2 was probably padded by KPO school-laptop deliveries, which ended by 31 Aug (an inference). H1 operating cash flow was −14.2m PLN. The stock has doubled since 30 Sep. 20-day realised volatility is 116% annualised, so the panel_pct here is as much a size read as a direction read. **The hunter's own findings point the other way (−0.30).** This is the day's sharpest disagreement between the hunter and the panel.

**MDV long (82, 3/4; Opus 5 at 70).** The judges cite three things. Both 2026 full reports carried a post-quarter sales update that moved the stock. Early-November LFL was strong: CCC above +40%, HalfPrice above +20%. There is a crowded disclosed short of about 4.1%, but that figure is a search snippet the hunter could not open, so it is not confirmed. **The case against:** Q3 headline numbers were pre-released on 6 Nov, and the stock rose about 14% on them. Inventory is up 21%, so cash flow and net debt are the new risk. And the print is amc, so the sealed window probably holds nothing.

**Where the panel and the hunter disagree.** NTT has the opposite sign (hunter −0.30, panel long 89). PLSV is split even within the panel: Opus 5 short, the other three long, sd 33. No name is above the conviction floor, so there is no above-floor name the panel left out.

**What the numbers are not.** `panel_score` ranks and does not forecast. There is no `expected_edge_pct` off the US. `p_up` is recorded and decides nothing. The member scales are this market's own 200 live sizes per judge. In the four-model re-judge the judges ranked Europe better than the live hunt (ρ +0.33/+0.34 on 48 names), and the EU panel measured ρ +0.22, p 0.19 on 45 names on 2026-10-21. **Nothing about this market's panel is established.** In the judges' own words, three of four sized the Polish names on the hunters' amc window. Opus 5 noted that if the sealed bmo window is used, all four Polish names should read 0.

## What the day is and is not

- **Selection:** `all 11 eligible names (at or under the cap)`. 42 scheduled, 11 eligible above $100k a day, all 11 hunted. No random draw was needed.
- **By market:** no 5, pl 4, de 1, se 1. **`market_concentration`: Oslo is 45.5% of the day (5 of 11), and four of those five are offshore drillers/rigs** (DDRIL, ENH, NORAM, VTURA; PLSV is offshore services). **VTURA and ENH are one exposure:** ENH is bidding for VTURA in an all-share deal at 5.50x, and both report the same morning. Over 9 ranked names that is a correlated block the scorer cannot see.
- **Calendar sources:** vendor plus Euronext Oslo for most Norwegian rows; Yahoo added GXI; Nasdaq Financial Calendar added RVRC (a phantom); Inderes for SE read; **bankier (pl issuer calendar) read `unavailable`, HTTP 403.** The UK had one RNS-dated name (NOG), which did not clear the floor.
- **Phantoms: 2 of 11** (NORAM, RVRC), both added or confirmed by an issuer-calendar or vendor row that pointed at a past release. As on 11-25, a calendar date pointing at a past release is the failure mode. NORAM's 11-27 is a distribution payment date and RVRC's is an ex-dividend day.
- **`session_unresolved` at the seal:** GXI, MDV, NORAM, NTT, PLW, RVRC, VGO. The hunters settled them as follows: GXI date confirmed with no time, so bmo is kept; MDV, NTT, PLW and VGO **amc** on the issuers' pattern; NORAM and RVRC no event. Getting the session wrong roughly halves the move.
- **Options:** `null` in all ten markets. Europe runs in the anchor-less regime (ρ=+0.073, p=0.45 over 104 events on the sealed corpus).
- **Short registers:** NO read (as of 11-25), SE read (as of 11-26), DE (Bundesanzeiger) read, PL none reachable. **`anchor_covered: true` on 2 names of 11** (GXI 2.86%, RVRC 2.18%). The five Norwegian names were read and are not named: a truncated zero, not an anchor.
- **Spain/Poland:** **4 of 11 names are Polish** (MDV, NTT, PLW, VGO). They have no positioning anchor, so their `priced_lean_pct` is the free control. They cannot be confirmed or killed after the fact. **1 is German** (GXI), which cannot reach `event_occurred: false` either.
- **`lean_vs_free_control_rho`:** the last resolved run (2026-10-16) carries only a Swedish reading, 0.60. No Norwegian or Polish reading exists from a resolved run.
- **The lean's weights are priors** borrowed from the US runs and measured nowhere in Europe.
- **`history.basis`:** observed for the five Norwegian names (`observed_newsweb`). **Estimated from cadence** for GXI, MDV, NTT, PLW, VGO and RVRC: that is a scale, not a record of dates.
- **Conviction floor 2.8:** no name clears it. Over the whole US sample, the sign below the floor was a coin flip.
- **Language notes worth quoting:** Börsen-Zeitung carried GXI's 4.75x year-end covenant target ("So muss das Verhältnis der Nettoschulden zum bereinigten operativen Ergebnis (Ebitda) bis zum Ende des Geschäftsjahres auf das 4,75-Fache zurückgeführt werden"), which is in no English EQS release. Every Polish name's session timestamps came from Polish sources only. The Nordic names added nothing beyond English, as expected.

## Driving the top and bottom

- **Top (MDV +0.40, tied with PLSV and VGO):** a November sales update is the likely new line (+1.0), against the first cash-flow and net-debt figures after the inventory build (−1.0). Modivo calendar: https://modivoplatform.com/relacje-inwestorskie/kalendarium ("27 lis 2026 – Skonsolidowany raport za III kwartał 2026/27").
- **Bottom (DDRIL −1.50):** Borgland Dolphin moored in Las Palmas against a November contract start (−1.2), https://www.vesselfinder.com/vessels/details/8758469. Report time: https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=687155 (Friday 27 Nov, 07:30 CET).

## Execution

The panel's book was handed to the IBKR executor at about 15:05 UTC (`ibkr-handoff.json`). At sealed spots on EUR 10,000 the offline plan is SELL DDRIL 27.9%, BUY NTT 40.7%, BUY MDV 31.3%. VGO (65) and ENH (60) are below 70. What the server sent and what filled is on branch `eu-ibkr-log`. **The EU panel has no measured edge yet.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

# Stage EU — Europe ranking for 2026-10-23

**No name clears the 2.8 conviction floor.** The hunters' largest key is ALLIGO_B at +1.50; the smallest are EQV1V and MTRS, tied at −1.30. **The panel selected two names, both long and both backed by all 4 judges: TOM and KNOW, each with a `panel_pct` of 86.**

Twenty names were drawn at random from 63 eligible. **12 of the 20 are Swedish** (`selection.market_concentration`: se 60%, five markets), plus 4 Norwegian, 2 Finnish, 1 UK and 1 Italian. Most of the day is Stockholm. One of the twenty has **no event in the window** (MGN), so 19 are ranked.

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were sealed on Thursday 2026-10-22 at about 13:50 UTC, while the European markets were still open. **Every sealed spot is therefore an intraday price, not a close.** All 20 rows are bmo, so the realised move is close(10-22) → close(10-23), taken from daily bars. One name releases during the session (EPEN, below), but that window still contains its reaction.

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session (per issuer) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | ALLIGO_B | Alligo | **+1.50** (p78) | no | +0.70 | 7.0 | 55 | bmo, 08:00 CEST |
| 2 | se | KNOW | Knowit | **+1.40** (p75) | no | +1.05 | 7.5 | 57 | bmo, 07:30 CET |
| 3 | no | TOM | TOMRA Systems | **+1.10** (p71) | no | +0.80 | 10.0 | 54 | bmo, 07:00 CEST (NewsWeb 684301) |
| 4 | it | ENI | Eni | **+1.00** (p67) | no | +0.40 | 4.0 | 55 | bmo per SoldiOnline; Eni's IR page lists the day, exact time not found |
| 5 | se | SAAB_B | Saab | **+0.90** (p63) | no | +0.60 | 6.0 | 55 | bmo, 07:30 CET |
| 6 | no | GJF | Gjensidige Forsikring | **+0.70** (p54) | no | +0.48 | 4.0 | 56 | bmo, 07:00 CET (NewsWeb 683855) |
| 7 | se | BUFAB | Bufab | **+0.60** (p50) | no | +0.78 | 6.5 | 56 | bmo, 07:30 CET |
| 8 | se | LIAB | Lindab | **+0.60** (p50) | no | +0.32 | 8.0 | 52 | bmo, from the prior 07:00 releases and the Inderes calendar |
| 9 | se | INDT | Indutrade | **+0.30** (p28) | no | +0.28 | 7.0 | 52 | bmo, ~07:30 CEST |
| 10 | uk | EVOK | Evoke | **+0.25** (p24) | no | +0.04 | 2.0 | 51 | sealed `bmo?`; issuer notice says 07:00 BST |
| 11 | se | MCAP | MedCap | **+0.20** (p20) | no | +0.84 | 7.0 | 56 | bmo, 06:30, matching its last four reports |
| 12 | se | EPEN | Ependion | **−0.10** (p14) | no | +0.34 | 8.5 | 52 | **13:00 CEST, in session** |
| 13 | se | VOLCAR_B | Volvo Car | **−0.10** (p14) | no | 0.00 | 6.5 | 50 | bmo, 07:00 (MFN calendar) |
| 14 | se | BHG | BHG Group | **−0.20** (p20) | no | −0.34 | 8.5 | 48 | bmo, 07:00 CEST by pattern |
| 15 | no | MEDI | Medistim | **−0.35** (p32) | no | 0.00 | 6.0 | 50 | sealed `bmo?`; NewsWeb webinar at 09:00, prior releases 06:30 UTC |
| 16 | fi | HIAB | Hiab | **−0.40** (p35) | no | −0.45 | 7.5 | 47 | bmo, ~08:00 EEST |
| 17 | se | MSAB_B | Micro Systemation | **−0.80** (p58) | no | −0.27 | 4.5 | 47 | bmo, 07:00 |
| 18 | fi | EQV1V | eQ | **−1.30** (p74) | no | −0.40 | 4.0 | 45 | bmo, ~08:00 EET |
| 19 | se | MTRS | Munters | **−1.30** (p74) | no | −0.48 | 8.0 | 47 | bmo, 07:30 CEST |

`impact_scaled` is the hunter's second, separate measurement. It is not the key, and the floor does not apply to it. Bracketed figures are percentiles of |value| among names sized by Opus 5.5; they describe scale, not rank. Three pairs are tied: BUFAB/LIAB, EPEN/VOLCAR_B and EQV1V/MTRS. Order inside a tie carries no information.

**Session checks:**
- **EPEN releases in session, not before the open.** Ependion's invitation (Nasdaq Nordic, 2026-10-13) puts the Q3 report at 13:00 CEST on 23 October, and every earlier Ependion report also came at 13:00. The scored window, close(10-22) → close(10-23), still contains the whole reaction, so the measurement holds. The opening print, however, is pre-release.
- **`session_unresolved`**: EVOK and MEDI. The hunters settled both as bmo from the issuers' own notices.
- **ENI** is the one bmo row without an issuer timestamp. Eni's investor page lists the press release and a 14:00 CEST call on 23 October, and SoldiOnline says the release comes before the Piazza Affari open.

**Pre-released, or a likely guidance event (`already_public` / `new_in_release`):**
- **Pre-released:** MSAB_B released its Q3 revenue and EBIT as inside information on 14 October; the stock rose 20.6% that day. VOLCAR_B issued a profit warning on 2 October, withdrawing its full-year volume and cash-flow outlooks; the stock fell 7.35% that day. For both, the headline is worth about zero, and what remains is detail: for MSAB_B, how much of revenue was one defence order, plus cash; for VOLCAR_B, the promised "further decisive actions".
- **Likely guidance events, which are where large moves are likelier:**
  - MTRS: the new CEO's first report, three weeks before a capital markets day, against an H2 margin guide that SEB already models below.
  - ENI: an extraordinary-dividend decision is due in October, and the cash-flow guide was set at Brent $85 against a Q3 average of $97.
  - HIAB: the first quarter with Labrie consolidated.
- **EVOK is under a live all-share offer from Bally's Intralot**, at about a 19% spread to spot, so its quarter is close to noise.
- **No numeric guidance at all:** most of the Swedish names. Their whole quarter is new, which is why most `abs_move_pct` sit at 6–10.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.**
- All four ran on their own pinned `-intl-` agents, with no fallback, and each covered 19 of 19 packs.
- Selection rule for this market: `consensus`, meaning 3 of 4 judges put the name in their own top 20%. That membership is read against `member_reference` q80: Opus 5 1.44, Opus 5.5 0.96, Sonnet 5.5 0.76, Fable 5.1 1.12.
- The percentile columns are read against each judge's live range (104 live sizes each), whose top 20% starts at Opus 5 |1.80|, Opus 5.5 |0.91|, Sonnet 5.5 |0.80| and Fable 5.1 |1.10|.
- That is why TOM's Opus 5 (1.44, exactly on its q80) and KNOW's Sonnet 5.5 (0.80) count toward k=4 while reading 73 and 80 in the table.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TOM | **yes** | 86 | long | 9 | 73L | 94L* | 81L* | 94L* | 4 | +1.55 | +1.10 |
| 2 | KNOW | **yes** | 86 | long | 5 | 92L* | 89L* | 80L | 84L* | 4 | +1.53 | +1.40 |
| 3 | BHG | no | 74 | short | 14 | 86S* | 56S | 64S | 88S* | 2 | −1.13 | −0.20 |
| 4 | ALLIGO_B | no | 69 | long | 11 | 85L* | 75L | 55L | 62L | 1 | +0.88 | +1.50 |
| 5 | HIAB | no | 0 | long | 45 | 73L | 33S | 41S | 0 | 1 | −0.19 | −0.40 |
| 6 | SAAB_B | no | 68 | long | 6 | 58L | 70L | 73L | 72L | 0 | +0.88 | +0.90 |
| 7 | MSAB_B | no | 61 | short | 13 | 64S | 60S | 41S | 79S | 0 | −0.81 | −0.80 |
| 8 | BUFAB | no | 63 | long | 7 | 61L | 75L | 62L | 55L | 0 | +0.77 | +0.60 |
| 9 | MTRS | no | 64 | short | 10 | 51S | 79S | 64S | 60S | 0 | −0.74 | −1.30 |
| 10 | MCAP | no | 55 | long | 7 | 49L | 67L | 50L | 55L | 0 | +0.62 | +0.20 |
| 11 | EQV1V | no | 55 | short | 12 | 43S | 73S | 47S | 56S | 0 | −0.61 | −1.30 |
| 12 | EPEN | no | 47 | short | 10 | 56S | 48S | 30S | 54S | 0 | −0.58 | −0.10 |
| 13 | MEDI | no | 48 | short | 5 | 56S | 43S | 43S | 51S | 0 | −0.53 | −0.35 |
| 14 | GJF | no | 42 | long | 12 | 36L | 59L | 47L | 27L | 0 | +0.52 | +0.70 |
| 15 | LIAB | no | 36 | long | 4 | 34L | 33L | 36L | 43L | 0 | +0.42 | +0.60 |
| 16 | ENI | no | 32 | long | 4 | 25L | 33L | 36L | 33L | 0 | +0.38 | +1.00 |
| 17 | VOLCAR_B | no | 20 | short | 22 | 31S | 19L | 36S | 30S | 0 | −0.37 | −0.10 |
| 18 | INDT | no | 23 | long | 8 | 16L | 30L | 14L | 33L | 0 | +0.28 | +0.30 |
| 19 | EVOK | no | 12 | long | 6 | 5L | 19L | 6L | 17L | 0 | +0.16 | +0.25 |

Each member's figure is its percentile (0–100) against its own live range: L is long, S is short, and `*` marks the member's own top 20% on that range. Fable 5.1 sized HIAB at exactly 0, which is why it shows no side.

**TOM, selected long (4 of 4, `panel_pct` 86, spread 9).**
- **Evidence the members name:**
  - On 16 October the Australian miner PLS took its final investment decision on the P2000 expansion. That turns TOMRA's earlier 22-sorter award for X-ray ore sorters, which was conditional on the decision, into a firm order (https://news.metal.com/newscontent/104162375-pls-approves-final-investment-decision-for-p2000-expansion-at-pilgangoora-smm-analysis).
  - The decision came two days after TOMRA compiled its own published consensus, in which Recycling order intake is 56 (max 59), flat on Q2. The stock did not move on it.
  - Recycling orders are the line behind this name's recent +11.9% and −25.6% report days. TOMRA re-guides every division every quarter, so `abs_move_pct` is about 9–10 for every member.
- **Strongest case against:**
  - The contract value is not public.
  - Opus 5 notes TOMRA has sold off on five of its last six prints.
  - The UK reverse-vending letter of intent (about 2,000 machines) is mostly priced.
  - France dropping its deposit scheme on 7 September is a −8.3% day already in the tape.

**KNOW, selected long (4 of 4, `panel_pct` 86, spread 5).**
- **Evidence the members name:**
  - Modular Finance's four-contributor consensus of 20 October has EBITA at 59.7m SEK, below last year's adjusted Q3 of 62.5m. Meanwhile Q2 adjusted EBITA rose 14% on comparable sales of −0.9%, with better utilisation and about 5% fewer staff.
  - Insiders bought into the quarter. The Norway country head bought 5,700 shares at 94.20 on 22 September, seen only in the Swedish FI register, after July buys by the CEO and others.
  - AFRY rose 16% on its Q3 margin beat.
- **Strongest case against:**
  - The new CEO's 2 September reorganisation probably puts one-off costs into reported EBITA, so the headline may read as a miss. The bar does not say whether it is reported or adjusted.
  - Pure IT-services peers were weak on 21–22 October: Columbus cut its margin guide, Vincit fell 5.2% and Softronic 8.3%.
  - This name has moved −18.8% on a print as well as +13.4% and +13.7%.

**Where the panel and the hunters disagree most:**
- **BHG** is the panel's third name (74 short, 2 of 4: Opus 5 and Fable 5.1 in their own top 20%), while the hunter sized it at only −0.20. The judges weighted the +12% peer-driven run-up into a name that sold its last two sales beats.
- **ALLIGO_B**, the hunters' top key (+1.50), is 69 on the panel. Only Opus 5 has it in its top 20%, and Sonnet 5.5 discounts the peer proxies.
- **EQV1V and MTRS**, the hunters' joint-bottom keys (−1.30), read 55 and 64 short: the same side, much smaller.
- **ENI** is +1.00 by the hunter, the fourth-largest positive key, but 32 on the panel. All four judges keep it small on a 3–4% move.
- **HIAB** has the widest spread of the day (45). Opus 5 is long (73) on the order book against a proxy-driven de-rating, Opus 5.5 and Sonnet 5.5 lean short, and Fable 5.1 is exactly flat. The mean comes out at 0.
- **VOLCAR_B** has opposite sides across members: Opus 5.5 is long (19), the other three short (30–36). All are small.

**What these numbers are not:**
- `panel_score` ranks and does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- Each member's scale still leans on the frozen E-P seed: 104 live sizes against the ~200 this market needs.
- In the four-model re-judge the judges ranked Europe better than the live hunt, but nothing about this market's panel is established.

## The finding driving the top and the bottom

**Top: ALLIGO_B +1.50.** Seven small findings, all leaning the same way.
- **+0.8:** Bergman & Beving, the closest Nordic counterparty, reported the same July–September quarter on 21 October. It saw increased construction and manufacturing activity in Sweden and Finland and a wait-and-see Norway (https://view.news.eu.nasdaq.com/view?id=b69d5f724020f1d9844d71f50701e77fa&lang=en&src=listed). That came after ABG set the only available bar on 8 October (organic +3%, adjusted EBITA 177m; https://borsvarlden.com/finwire/CRF00F389A).
- **+0.4:** Byggmax like-for-like sales +5.1%.
- **+0.4:** the CEO bought 7,500 B shares at SEK 135.50 on 2 September, found only in the Swedish FI insider register. The original reads: "Samuel Alteborg | Verkställande direktör (VD) | Förvärv | … | 7 500 | Antal | 135,50 | SEK" (CEO, acquisition, 7,500 shares at SEK 135.50).
- The bar rests on a single broker, so every finding is capped.

**Bottom, tied: EQV1V −1.30 and MTRS −1.30.**
- **eQ:**
  - **−0.6:** the single-analyst bar (Inderes, published in Finnish on 16 October: Q3 EBIT 8.0 MEUR) needs about 1.7 MEUR of paid private-equity performance fees on top of the 0.9 MEUR catch-up. Q2 delivered 0.73 MEUR, and Inderes overestimated Q2 by 12%.
  - **−0.4:** the full-year estimate implies a Q4 EBIT of about 12.3 MEUR, against recent quarters of 5.6–8.0.
- **Munters:**
  - **−1.2:** an outlook reset in the new CEO's first report. SEB already forecasts organic growth "långt under bolagets guidning från det andra kvartalet" (far below the company's guidance from the second quarter) (https://www.placera.se/telegram/munters-seb-sanker-riktkurs-ser-osakrare-dct-produktionsokning-usa-20260928).
  - **−0.6:** no inside-information data-centre order was flagged in Q3.
  - **+0.5:** five broker target cuts have already lowered the bar.

## Names that could not be ranked

- **MGN (Magnora) — phantom.** Magnora's own filings put the Q3 report on **30 October 2026**, not 23 October:
  - its financial calendar on Oslo Børs NewsWeb (filed 2026-06-09, msg 675695) lists "30.10.2026 - Quarterly Report - Q3";
  - its Q3 invitation (filed 2026-10-22 13:00 CEST, msg 684598, about 40 minutes before the seal) says Friday 30 October at 10:00 CET (https://api3.oslo.oslobors.no/v1/newsreader/message?messageId=684598).

  The row came from the vendor calendar alone (`calendar_source: vendor`). Norway's day archive is ticker-keyed, so the resolver can confirm the kill.

## What the day can and cannot say

**Universe and calendar**
- `selection.method`: a random sample of 63 eligible names, seed `eu-2026-10-23`. 108 were scheduled across the ten markets, and no market was closed.
  - Eligible by market: se 50, no 5, fi 4, uk 1, de 1, fr 1, it 1, dk/es/pl 0.
  - Hunted: se 12, no 4, fi 2, uk 1, it 1.
- **Calendar sources:**
  - The UK RNS calendar added EVOK.
  - Yahoo read on all ten markets and added nothing.
  - Issuer calendars dated 93 SE, 20 FI, 5 NO, 2 DE and 1 PL rows for the target. **Inderes read `read_short` for Sweden.**
  - By hunted row: 10 are vendor+Inderes+Yahoo, 3 vendor+Euronext Oslo+Yahoo, 2 vendor+Inderes+Nasdaq financial calendar+Yahoo, 2 vendor+Inderes, 1 vendor+Yahoo, 1 RNS, and **1 vendor-only (MGN, the phantom)**.

**Anchors and registers**
- **`options` is null in all ten markets.** Europe runs in the anchor-less regime, which on the sealed US corpus ranked at ρ=+0.073, p=0.45 over 104 events.
- **Short registers read for se, no, fi, it and uk** (as of 10-21/10-22). **`anchor_covered: true` on 4 of 20:** MTRS 5.37%, EVOK 2.26%, LIAB 1.40% and BHG 0.59%. The other 16 are truncated zeros: the register was read and does not name them, which is not evidence that nobody is short.
- **Spain 0, Poland 0, Germany 0.** No name today lacks a register, and none is in a market where a phantom cannot be killed. Italy (ENI) cannot reach `event_occurred: false`, because eMarket STORAGE is not universal; Eni files elsewhere.
- **`lean_vs_free_control_rho`:** the last resolved European run (2026-10-08) carries it only for the UK, at 1.0 on 3 names, which is not a measurement. The runs of 10-09 through 10-22 are unresolved. **The Nordic rows of 10-13 to 10-16 are now past or at the ~12-day limit of the Nasdaq Nordic feed.** Resolve them at once, or their kills become unreachable.
- The lean's weights are priors borrowed from the US runs and measured nowhere in Europe.

**History basis**
- `history.basis` is observed for EVOK (`observed_rns`) and for GJF, MEDI, MGN and TOM (`observed_newsweb`). **It is estimated for the other 15**: a scale, not a record of dates.
- Hunters rebuilt the real report-day moves on ALLIGO_B (median 7.6% against the baseline's 3.17%), BHG (~11% against 3.27%), EPEN (~8.8% against 2.66%), INDT (~5.9% against 2.33%), KNOW (~7.7% against 3.1%) and SAAB_B (~6%).
- MEDI's *observed* NewsWeb history counts webinar invitations as prints: 1.8% against about 3.4% on real results days. This is the same classifier defect Norway's history had with "Invitation to Q4 results", so it is worth a look in `eu_priced_in.py`.
- This is why most `abs_move_pct` sit well above the baselines' proxies.

**Floor and language**
- **No name sits above the 2.8 conviction floor.** Over the whole US sample, the sign was a coin flip below it.
- `language_note`: on the Swedish names, the Swedish wire (Finwire/Placera, Börsvärlden, EFN, Nyhetsbyrån Direkt) carried what no English source had:
  - the broker bars and consensus (INDT, MTRS, SAAB_B, BHG, LIAB);
  - the report-day reaction tables (KNOW, INDT);
  - two insider purchases found only in the FI register (ALLIGO_B's CEO, KNOW's Norway head);
  - Volvo Cars' hiring freeze;
  - Munters' Speria bid deadline.

  eQ's only bar was a Finnish-language Inderes preview. ENI's consensus segment split and the dividend mechanism came from Italian sources. On EVOK, GJF, TOM and MEDI the local sources added nothing. Issuer releases across the Nordics were bilingual and added nothing.
- **One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.

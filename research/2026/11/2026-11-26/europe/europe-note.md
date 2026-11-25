# Stage EU — Europe ranking for 2026-11-26 (Thu)

Sealed Wednesday 2026-11-25 at about 14:45 UTC, while the European markets were still trading. The sealed spots are **intraday prices, not closes**. The event date is Thursday 2026-11-26.

**Answer first: twenty names, half of them British, and the hunters found nothing large.** No name clears the 2.8 conviction floor. The largest |impact_sum| is 1.40: FSG at −1.40, and CMCX at +1.20 at the top. **The panel selects two names, each with at least 3 of 4 judges in their own top 20%:**
- **CMCX** long, panel_pct 98, 4/4
- **FSG** short, panel_pct 80, 3/4

DIA (74 short, 2/4) sits just below the selection. The IBKR handoff (rule: panel_pct ≥ 70 with all four judges) carries BUY CMCX, SELL FSG and SELL DIA. **One day is not a result.**

**Four of the twenty have no print in the window and are not ranked.** CBOX, IGP and PCIP released their results on 24 or 25 Nov; the vendor's 26 Nov date is only each company's Investor Meet Company presentation. HUNT already reported Q3 on 20 Nov. **Four Polish names release after the close by their hunters' issuer evidence**: ACP, DIA, ENT and MDG. Their reaction falls in close(26 Nov) → close(27 Nov), not in the sealed bmo window. VOX moved its report to the evening of 25 Nov, so the sealed window does hold it.

## Ranked on `impact_sum` (the key, per `edge-scores.json` `ranking_key`)

| # | ticker | mkt | session (hunter's check) | impact_sum | floor | impact_scaled | abs_move | p_up | already public | new in release |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CMCX | uk | bmo (07:00 RNS; date moved from 19 Nov) | +1.20 (p79) | no | +1.76 | 11.0 | 58 | FY27 guide raised 1 Jul; CEO bought ~£5m in Oct | **H1 not pre-released**; FY27 guide vs consensus sitting on its floor |
| 2 | VOX | pl | bmo-equivalent (moved to 25 Nov after the close) | +0.40 (p40) | no | +0.60 | 7.5 | 54 | H1 outlook; NFZ rule changes | Q3, no pre-release |
| 3 | ACP | pl | **amc** (Q1 18:35, H1 17:53) | +0.30 (p32) | no | +0.36 | 4.5 | 54 | Formula Systems' record Q3 (25 Nov, ~half the group) | group Q3; backlog |
| 4 | DFENS | no | bmo (07:00 CET, issuer notice) | +0.20 (p22) | no | −0.38 | 9.5 | 48 | 2026 guide; post-Q2 orders | **first 2027 guide** |
| 5 | HFD | uk | bmo (07:00 RNS) | +0.10 (p14) | no | +0.18 | 4.5 | 52 | **H1 sales pre-released** 21 Oct; FY27 PBT guide | H1 PBT; possible narrowing of £55–65m |
| 6 | SANION | se | bmo (08:00 CET) | +0.10 (p14) | no | +0.24 | 6.0 | 52 | **Q3 one-off income and stake sale pre-released** | little; pipeline timelines |
| 7 | CIG | pl | bmo (08:38 press stamp, last year) | −0.10 (p14) | no | −0.14 | 3.5 | 48 | game delay (24 Nov); refinancing | Q3 back-catalogue numbers |
| 8 | SREI | uk | bmo (09:00 webcast) | −0.10 (p14) | no | −0.12 | 3.0 | 48 | Picton merger; October lettings | 30 Sep NAV; strategy update |
| 9 | MDG | pl | **amc** (H1 18:13, Q3 estimate 17:06) | −0.20 (p22) | no | −0.16 | 4.0 | 48 | **Q3 revenue and EBITDA pre-released** 13 Oct | takeover LOI status; cash flow |
| 10 | PARKEN | dk | bmo-equivalent (releases ~14:30–15:00 in session) | −0.20 (p22) | no | −0.18 | 4.5 | 48 | guide cut in May; strategic review 13 Oct | Q3; possible review line |
| 11 | SAFE | uk | bmo (07:00 RNS) | −0.30 (p32) | no | +0.07 | 3.5 | 51 | **FY EPS guide given twice** (3 Sep, 15 Oct) | Q4 KPIs; pipeline phasing |
| 12 | MAB | uk | bmo (07:00 RNS) | −0.40 (p40) | no | −0.40 | 5.0 | 46 | **FY26 pre-released** 24 Sep | first ~8 weeks of FY27; outlook |
| 13 | DIA | pl | **amc** (H1 17:08) | −0.50 (p47) | no | −0.52 | 6.5 | 46 | Q2 margin; FY guide | Q3, no pre-release; **margin guide at risk** |
| 14 | ENT | pl | **amc** (PAP 17:59–19:27) | −0.70 (p60) | no | −0.30 | 5.0 | 47 | TUI 2027 contract (20 Nov) | Q3 peak quarter; FX on leases |
| 15 | LTHM | uk | bmo (07:00 RNS, inferred) | −1.00 (p74) | no | −0.20 | 5.0 | 48 | **4 of 6 months pre-released** at AGM | Aug–Sep; H2 outlook; dividend |
| 16 | FSG | uk | bmo (07:00 RNS) | −1.40 (p83) | no | −0.60 | 6.0 | 45 | **AUM/FUM and H1 EBITDA direction pre-released** 8 Oct | FY27 outlook against consensus FUM of £10.7bn |

Not ranked (hunter found no event on this date): **CBOX** (H1 out 25 Nov 07:00), **IGP** (H1 out 24 Nov), **PCIP** (FY out 24 Nov), **HUNT** (Q3 out 20 Nov). For CBOX, IGP and PCIP the vendor date is a presentation date, not a phantom company; HUNT should resolve `event_occurred: false`.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.** All four members ran, with no fallback. Each judge's own top 20% starts at |0.98| (Opus 5), |0.70| (Opus 5.5), |0.56| (Sonnet 5.5) and |0.80| (Fable 5.1), measured on 200 live sizes each.

| rank | ticker | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CMCX | **yes** | 98 | long | 1 | 99L* | 98L* | 98L* | 99L* | 4 | +3.37 | +1.20 |
| 2 | FSG | **yes** | 80 | short | 11 | 94S* | 64S | 86S* | 74S | 3 | −1.17 | −1.40 |
| 3 | DIA | | 74 | short | 7 | 75S | 64S | 83S* | 74S | 2 | −0.98 | −0.50 |
| 4 | VOX | | 60 | long | 35 | 84L* | 70L | 0- | 87L* | 2 | +0.96 | +0.40 |
| 5 | ACP | | 68 | long | 5 | 68L | 62L | 68L | 74L | 1 | +0.86 | +0.30 |
| 6 | DFENS | | 67 | long | 11 | 68L | 51L | 68L | 82L* | 1 | +0.86 | +0.20 |
| 7 | MAB | | 56 | short | 10 | 44S | 64S | 47S | 68S | 0 | −0.65 | −0.40 |
| 8 | ENT | | 52 | short | 5 | 47S | 55S | 47S | 59S | 0 | −0.56 | −0.70 |
| 9 | LTHM | | 49 | short | 3 | 54S | 45S | 47S | 49S | 0 | −0.52 | −1.00 |
| 10 | MDG | | 34 | short | 22 | 30S | 51S | 54S | 0- | 0 | −0.41 | −0.20 |
| 11 | HFD | | 31 | long | 20 | 44L | 51L | 0- | 29L | 0 | +0.37 | +0.10 |
| 12 | CIG | | 31 | short | 9 | 18S | 30S | 32S | 45S | 0 | −0.31 | −0.10 |
| 13 | SREI | | 12 | long | 8 | 20L | 12L | 0- | 18L | 0 | +0.17 | −0.10 |
| 14 | PARKEN | | 14 | short | 9 | 7S | 10S | 12S | 29S | 0 | −0.13 | −0.20 |
| 15 | SAFE | | 1 | short | 30 | 6L | 20L | 52S | 23L | 0 | +0.13 | −0.30 |
| 16 | SANION | | 0 | – | 0 | 0- | 0- | 0- | 0- | 0 | +0.00 | +0.10 |

**CMCX (selected, long, 4/4).** The judges name three things: H1 (Apr–Sep) has not been pre-released on a name whose own results days moved a median 16.8%; consensus FY27 net operating income of £552.5m sits on the company's own "at least £550m" floor; and the CEO, who holds about 64.6%, bought about £5m after the half closed and said in an issuer press release that the low-volatility headwind hurting peers "is not reflected in CMC's performance" (https://www.cmcmarkets.com/group/press-releases/in-conversation-with-lord-peter-cruddas-cmc-markets-evolution-and-continued-growth-strategy). The stock has given back the whole post-purchase rally (716p → 651p). **The strongest case against:** IG guided Jul–Sep revenue −14% with OTC retention down from ~80% to ~70% (https://www.financemagnates.com/forex/igs-otc-retention-slips-with-q3-revenue-expectation-at-14-lower/), the FCA register shows shorts building (0.96% → 1.16%), and the CEO statement has been public since 7 Oct.

**FSG (selected, short, 3/4).** The 8 Oct trading update said fundraising timing "remains an important factor in the delivery of near-term consensus expectations", yet the consensus the company itself published on 2 Nov still has FY27 FUM at £10.7bn against £9.1bn at the half (https://www.foresight.group/shareholders/consensus-estimates/). Last year's in-line interims fell 11.3%. **The strongest case against:** the shares already fell 11% (481p → 428p) since 4 Nov with no news, a buyback is running, and the short register is flat at 1.48%. Opus 5.5 placed it at only 64S.

**Where the panel and `impact_sum` disagree most.** No name clears the floor, so there is no floor-clearer the panel left out. LTHM is the hunter's second-largest negative (−1.00) and sits at panel_pct 49. VOX splits the judges: Opus 5 and Fable put it in their own top 20% long and Sonnet 5.5 at zero (sd 35). SAFE and SREI flip sign between the hunter and the panel, both on sizes too small to matter.

**What the numbers are not.** `panel_score` ranks and does not forecast. There is no `expected_edge_pct` off the US. Certainty (`p_up`) is recorded and decides nothing. The member scales are still mostly the frozen E-P seed until this market has about 200 panel names of its own. In the four-model re-judge the judges ranked Europe better than the live hunt, but Japan and Australia worse, so nothing about this market's panel is established. **The EU panel has no measured edge** (2026-10-21: ρ +0.22, p 0.19 on 45 names).

**Session caution on the handoff.** DIA's hunter settles its release as **after the Warsaw close on 26 Nov** (H1 filed 17:08; PAP: "Spółka w czwartek po zamknięciu opublikowała wyniki finansowe", "the company published results on Thursday after the close"). A position flattened at 15:35 Amsterdam on 26 Nov exits before that print. Four of the judges sized DIA on the close(26)→close(27) window.

## The top and bottom name

- **Top, CMCX +1.20.** Driving finding (+2.0, guidance line): the CEO's ~£5m post-period purchase and his on-record claim that the low-volatility headwind is not hitting CMC. https://www.cmcmarkets.com/group/press-releases/in-conversation-with-lord-peter-cruddas-cmc-markets-evolution-and-continued-growth-strategy
- **Bottom, FSG −1.40.** Driving finding (−2.0, guidance line): the company's own consensus caveat set against a consensus that has not moved down to it. https://www.investegate.co.uk/announcement/rns/foresight-group-holdings-limited-npv--fsg/trading-update-for-the-six-months-ended-30-09-2026/9812186

## What the day is made of

- **Selection:** "all 20 eligible names (at or under the cap)". 49 scheduled, 20 eligible above the $100k floor, all 20 hunted, so there was no random draw today. By market: **uk 10, pl 6, no 2, se 1, dk 1**; de, fr, fi, it and es 0.
- **Market concentration:** the UK is 50% of the day across 5 markets. Half the ranking is one market's day.
- **Calendar sources:** the UK rows came from the vendor, the issuers' own RNS notices (11 dated for the target: SREI, SAFE, IGP and others) and Yahoo (CMCX). The Polish issuer calendar (bankier) read `unavailable` (HTTP error). The four misdated UK rows (CBOX, IGP, PCIP, plus HUNT in Norway) are the cost of that: the RNS-sourced and vendor rows took a presentation date for a results date.
- **`session_unresolved`:** 15 of 20 baselines were sealed with an assumed session (all but DFENS, FSG, HFD, SANION and HUNT). The hunters settled most of them; four Polish names turned out to be amc.
- **Options:** `options` is null in all ten markets. Europe runs in the anchor-less regime that priced at ρ=+0.073, p=0.45 over 104 events on the sealed corpus.
- **Short registers and anchors:** the FCA (UK), Finanstilsynet (NO), the DFSA register (DK) and Finansinspektionen (SE) all read. **7 of 20 names carry `anchor_covered: true`** (CMCX, FSG, HFD, SAFE, SREI, DFENS, SANION). The rest are truncated zeros or unreadable, which is not an anchor.
- **Spain and Poland:** **6 of 20 names are Polish** (ACP, CIG, DIA, ENT, MDG, VOX); none Spanish. They have no positioning anchor (the KNF register returns 403 here) and no reachable day archive, so their `priced_lean_pct` is the free control itself and they can never be confirmed or killed after the fact. No German names today.
- **`lean_vs_free_control_rho`:** the last resolved European run (2026-10-16) reported it for Sweden only, at 0.60. The lean's weights are priors borrowed from the US runs and have been measured nowhere in Europe.
- **History basis:** only the 11 UK names (`observed_rns`) and the 2 Norwegian ones (`observed_newsweb`) carry real dated announcement history. **ACP, CIG, DIA, ENT, MDG, VOX, PARKEN and SANION are `estimated_from_cadence`**: a scale, not a record of dates. VOX's hunter found the estimated history placed Q1 on the wrong date with the wrong sign.
- **Conviction floor:** no name sits above 2.8. Over the whole US sample the sign was a coin flip below the floor.
- **Pre-released periods** (`already_public`): HFD (H1 sales), SANION (Q3 one-off income), MDG (Q3 revenue/EBITDA), MAB (FY26), LTHM (4 of 6 months), FSG (AUM/FUM and EBITDA direction), SAFE (FY EPS guide). **Likely guidance events** (`new_in_release`): CMCX (FY27 guide vs floor), DFENS (first 2027 guide), FSG (FY27 outlook), DIA (margin guide), HFD (range narrowing), MAB (FY27 outlook).
- **Language notes worth quoting:** for the Polish names the Polish sources carried what mattered (release timestamps, PAP consensus tables, the Medicalgorithmics takeover terms, Voxel's date change); for PARKEN every release is in Danish only, including the guide and the sale-review wording. The UK and Nordic hunters report the local sources added nothing the English ones did not.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

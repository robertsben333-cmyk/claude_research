# Stage EU — Europe ranking for 2026-10-22

**The answer: no name clears the 2.8 conviction floor. The largest hunter key is LINC at +1.20; the smallest is AXFO at −1.50. The panel selected two names, both 4 of 4 judges: AXFO short and KJELL long.** Twenty names were drawn at random from 75 eligible, and **15 of the 20 are Swedish** (`selection.market_concentration`: se 75%, five markets). So this is a Stockholm Thursday, and any pooled statement about it is mostly about Swedish names. Two of the twenty have **no event in the window** (REJL_B, ORY), so 18 are ranked.

The ranking is on `impact_sum`, the `ranking_key` in `edge-scores.json`. The baselines were sealed on Wednesday 2026-10-21 at about 13:45 UTC with the European markets still open, so **every sealed spot is an intraday price, not a close**. The realised move comes from daily bars: close(10-21) → close(10-22) for bmo, close(10-22) → close(10-23) for amc. One sealed session is known to be wrong (EAST, below).

| # | market | ticker | company | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move_pct | p_up | session |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | se | LINC | Linc | **+1.20** (p72) | no | +0.35 | 3.5 | 55 | sealed `bmo?`; all eight prior reports went out 07:00 on MFN |
| 2 | se | KJELL | Kjell Group | **+0.80** (p58) | no | +0.60 | 7.5 | 54 | bmo. Issuer: 07:00 CEST |
| 3 | uk | SBRY | J Sainsbury | **+0.70** (p54) | no | +0.50 | 5.0 | 55 | bmo, ~07:00 London by pattern |
| 4 | se | VIMIAN | Vimian | **+0.50** (p42) | no | +0.70 | 7.0 | 55 | bmo. Issuer: 07:45 |
| 5 | se | ARJO_B | Arjo | **+0.30** (p28) | no | +0.10 | 5.0 | 51 | bmo. Issuer: 07:00 CEST |
| 6 | se | COOR | Coor | **+0.20** (p19) | no | +0.12 | 6.0 | 51 | bmo. Issuer: 07:30 CEST |
| 7 | fr | DIM | Sartorius Stedim | **+0.10** (p14) | no | 0.00 | 7.5 | 50 | bmo, ~07:00 CEST by pattern |
| 8 | se | PRISMA | Prisma Properties | **+0.10** (p14) | no | +0.24 | 3.0 | 54 | bmo. Issuer: 07:00 CEST |
| 9 | se | BEIJ_B | Beijer Ref | **−0.10** (p14) | no | −0.18 | 4.5 | 48 | bmo. 08:00 per Finwire |
| 10 | se | LOGI_B | Logistea | **−0.20** (p19) | no | −0.28 | 3.5 | 46 | bmo. Issuer: 07:30 CEST |
| 11 | se | EAST | Eastnine | **−0.30** (p28) | no | −0.14 | 3.5 | 48 | **sealed amc; the issuer says 14:00 CET in session** |
| 12 | se | INTEA_B | Intea Fastigheter | **−0.40** (p35) | no | −0.16 | 4.0 | 48 | bmo, 07:30 by pattern |
| 13 | es | VIS | Viscofan | **−0.40** (p35) | no | −0.32 | 4.0 | 46 | amc, from secondary sources only (issuer and CNMV unreachable) |
| 14 | se | SVED_B | Svedbergs | **−0.70** (p54) | no | −0.60 | 6.0 | 45 | bmo. Issuer: 07:30 |
| 15 | no | ATEA | Atea | **−0.90** (p62) | no | −0.39 | 6.5 | 47 | bmo. NewsWeb notice: 08:00 presentation |
| 16 | se | SEB_A | SEB A | **−0.95** (p63) | no | −0.48 | 4.0 | 44 | bmo. Issuer: 06:30 |
| 17 | se | SWED_A | Swedbank A | **−1.10** (p70) | no | −0.42 | 3.5 | 44 | bmo. Issuer: 07:00 |
| 18 | se | AXFO | Axfood | **−1.50** (p77) | no | −0.84 | 7.0 | 44 | bmo. Issuer: 07:00 CET |

`impact_scaled` is the hunter's second, separate measurement; it is not the key and no floor applies to it. Bracketed figures are percentiles of |value| among names sized by Opus 5.5: scale, not rank. DIM/PRISMA and INTEA_B/VIS tie; order inside a tie carries no information.

**One sealed window is wrong, per the issuer:**
- **EAST is in session, not the sealed amc.** Eastnine's own invitation (Nasdaq Nordic, 2026-10-15) puts the Q3 report at 14:00 CET on 22 October, during trading (https://view.news.eu.nasdaq.com/view?id=bcb318f18337b489c9feef1ff18a356d4&lang=en&src=listed). The reaction is in close(10-21) → close(10-22); the sealed window would mostly miss it. The hunter's `session_check` opens with "bmo". Check what `eu_resolve.py` takes for this row.
- **`session_unresolved`**: LINC (settled bmo by the hunter on eight prior 07:00 releases), ORY and REJL_B (no event, below).
- **VIS** is amc on a Rankia forum post, TipRanks and the issuer's own pattern; viscofan.com and CNMV were unreachable, so this window is not issuer-confirmed.

**Pre-released, or a guidance event (`already_public` / `new_in_release`):**
- **Nothing pre-released the period.** No name filed a profit warning or trading update with the quarter's numbers. Partial pre-releases: EAST gave the post-deal pro forma earnings capacity on 25 Sep; SEB_A's 30 Sep pre-close steers (NII drag, NFI at the lower end) sit below the FactSet bar; ARJO_B and SWED_A pre-announced their one-offs (tariff refund claim; NPL writeback and DFS cost).
- **Likely guidance events, the likelier large moves:** **SBRY** (FY27 £975m–£1,075m likely narrowed and restated for continuing ops after Argos), **VIS** (FY EBITDA guide already at the low end in July; Q3 European gas up sharply), **DIM** (6–10% cc guide likely confirmed or narrowed), **SEB_A / SWED_A** (first capital statements since FI's 14 Oct IRB decision on SEB).
- **No numeric guidance at all:** most of the Swedish names, so their whole quarter is new.

## Panel

**Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing.** All four ran on their own pinned `-intl-` agents, no fallback, each covering 18 of 18 packs. Selection rule for this market: `consensus`, 3 of 4 judges in their own top 20%. Each judge's top 20% starts at Opus 5 |1.80|, Opus 5.5 |0.96|, Sonnet 5.5 |0.90|, Fable 5.1 |1.12|, on 86 live sizes each.

| rank | ticker | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | hunter impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AXFO | **yes** | 86 | short | 3 | 91S* | 85S* | 83S* | 87S* | 4 | −1.38 | −1.50 |
| 2 | KJELL | **yes** | 82 | long | 4 | 78L | 88L* | 80L* | 83L* | 4 | +1.37 | +0.80 |
| 3 | SEB_A | no | 70 | short | 14 | 78S | 46S | 78S | 79S | 1 | −1.05 | −0.95 |
| 4 | SVED_B | no | 57 | short | 4 | 63S | 57S | 51S | 58S | 0 | −0.70 | −0.70 |
| 5 | ATEA | no | 56 | short | 5 | 62S | 56S | 48S | 58S | 0 | −0.65 | −0.90 |
| 6 | LINC | no | 46 | long | 13 | 42L | 65L | 48L | 30L | 0 | +0.57 | +1.20 |
| 7 | VIMIAN | no | 41 | long | 28 | 13L | 73L | 14L | 65L | 0 | +0.55 | +0.50 |
| 8 | SWED_A | no | 45 | short | 5 | 38S | 43S | 51S | 48S | 0 | −0.50 | −1.10 |
| 9 | ARJO_B | no | 36 | long | 8 | 33L | 46L | 41L | 24L | 0 | +0.49 | +0.30 |
| 10 | VIS | no | 36 | short | 17 | 31S | 36S | 14S | 60S | 0 | −0.43 | −0.40 |
| 11 | DIM | no | 32 | short | 6 | 30S | 43S | 27S | 30S | 0 | −0.39 | +0.10 |
| 12 | LOGI_B | no | 23 | short | 4 | 23S | 29S | 23S | 16S | 0 | −0.31 | −0.20 |
| 13 | EAST | no | 17 | short | 5 | 13S | 13S | 17S | 24S | 0 | −0.22 | −0.30 |
| 14 | INTEA_B | no | 13 | short | 10 | 7S | 21S | 0 | 24S | 0 | −0.17 | −0.40 |
| 15 | PRISMA | no | 8 | long | 3 | 8L | 10L | 10L | 4L | 0 | +0.14 | +0.10 |
| 16 | BEIJ_B | no | 6 | short | 11 | 16S | 7L | 2L | 16S | 0 | −0.06 | −0.10 |
| 17 | SBRY | no | 3 | long | 22 | 28S | 6L | 35L | 0 | 0 | +0.05 | +0.70 |
| 18 | COOR | no | 2 | short | 3 | 7S | 0 | 0 | 0 | 0 | +0.00 | +0.20 |

Each member's figure is its percentile 0-100 against its own live range, L long / S short; `*` marks its own top 20%. KJELL's Opus 5 size (+1.80) sits exactly on that member's q80, which is why it reads 78 without a star in the live reference yet counts toward k=4 against `member_reference`.

**AXFO, selected short (4 of 4, spread 3, the tightest agreement of the day).**
- **Evidence the members name:** ICA Gruppen's May–Aug tertial has ICA stores +4.6% against a +4.2% market, with prices cut by more than the VAT, so the rest of the market, Willys included, grew below it — the line the last two report days turned on (−14.9%, −9.1%) (https://www.placera.se/telegram/ica-gruppen-okade-omsattningen-och-lyfte-rorelseresultatet-20260930). Into that, the stock has re-rated +19% off its Q2 report-day close on four buy upgrades against a flat EBIT consensus (Modular 1,101m, Infront 1,091m; https://borsvarlden.com/artiklar/axfood-vantas-redovisa-1-101-miljoner-i-justerat-rorelseresultat-modular). Six of the last eight report days fell.
- **Strongest case against:** food inflation is returning (Matpriskollen: 19% of items repriced up in September against 10% in August), which gives management a constructive outlook line; comps are easier than Q2; and Handelsbanken's preview already expects Willys below the index, so part of this is the bar.

**KJELL, selected long (4 of 4).**
- **Evidence the members name:** one analyst, a revenue estimate (632 MSEK, Yahoo) and no published quarterly profit bar, against a gross margin of 44.0% in H1 versus an adjusted 41.6% in Q3 2025 — 10–15 MSEK of gross profit on a 16.7 MSEK adjusted EBITA base (https://view.news.eu.nasdaq.com/view?id=bb8164d4a122de08170b4a9a4c7194ab1&lang=en&src=listed). Clas Ohlson's organic +8% (Aug) and +12% (Sep) corroborate demand; three board members bought after Q2, the last on 9–10 Sep.
- **Strongest case against:** the CEO called the cost base too high and flagged autumn ERP-preparation costs; Q3 2025's +103 MSEK operating cash flow came from a working-capital release that will not repeat; Kjell pre-released both of its last two awkward quarters and has not this time, which is weak evidence of nothing awful, not of a beat; and the bar is a single revenue estimate.

**Where the panel and the hunters disagree most:**
- **LINC**, the hunters' top name (+1.20), is only 46 on the panel: Fable 5.1 (30) and Opus 5 (42) discount a NAV discount built from public prices.
- **SBRY** +0.70 by the hunter is a coin flip on the panel (3, with Opus 5 on the short side).
- **DIM** carries opposite signs (hunter +0.10, panel short 32), both small.
- **SWED_A**: the hunter's −1.10 is the day's second-largest negative key, but no judge has it in its own top 20%.
- **SEB_A** is the panel's third name (70 short); three judges sit at 78–79, just under their own cut, and Opus 5.5 at 46.
- **VIMIAN** has the widest spread (28): Opus 5.5 and Fable 5.1 lean long on the unreleased Delaware ruling, Opus 5 and Sonnet 5.5 barely move.

**What these numbers are not:** `panel_score` ranks and does not forecast; there is no `expected_edge_pct` off the US; `p_up` is recorded and decides nothing; each member's scale still leans on the frozen E-P seed (86 live sizes against the ~200 this market needs); and while the four-model re-judge had the judges ranking Europe better than the live hunt, nothing about this market's panel is established.

## The finding driving the top and the bottom

**Top: LINC +1.20.** Two findings, both inference. +0.7: the discount to NAV widened to about 16–17% after the buyback stopped on 21 Sept, against 3–10% at recent month-ends, on the hunter's own reconstruction of the 30 Sept NAV from public prices (https://mfn.se/a/linc-ab/substansvarde-2026-08-31). +0.5: the buyback (311,436 of 650,000 shares bought) can restart once the closed period ends with the report (https://mfn.se/a/linc-ab/aterkop-av-aktier-i-linc-14-september-2026-21-september-2026). No NAV estimate is published, so `print_vs_bar_pct` is 0.

**Bottom: AXFO −1.50.** −0.8 on positioning: the sell-side swung to buy and the stock re-rated +19% into a flat-EBIT print where six of the last eight report days fell (https://borsvarlden.com/artiklar/axfood-vantas-redovisa-1-101-miljoner-i-justerat-rorelseresultat-modular). −0.6 on the quarter: the ICA tertial implies Willys below market (https://www.placera.se/telegram/ica-gruppen-okade-omsattningen-och-lyfte-rorelseresultatet-20260930), original: "ICA-butikerna ökade sin försäljning med 4,6 procent under tertialet, jämfört med marknadens tillväxt på 4,2 procent" (ICA stores grew sales 4.6% in the tertial, against market growth of 4.2%).

## Names that could not be ranked

- **REJL_B (Rejlers) — phantom.** The Q3 report was moved to **3 November 2026 at 08:30 CET** to match Multiconsult's calendar after the merger. Source: Rejlers' inside-information release of 2026-09-07, "Därav kommer Rejlers Q3-rapport att publiceras den 3 november 2026" (Hence Rejlers' Q3 report will be published on 3 November 2026), https://view.news.eu.nasdaq.com/view?id=b434b654cf59e0e0d0fbc79db38deb0e9&lang=sv&src=listed, and the issuer's calendar https://www.rejlers.com/se/investerare/kalender/. The row was **added by Yahoo's calendar**, which still carried the date printed in the H1 report. Worth a look at the Yahoo source in `eu_universe.py`: a Yahoo-only row with a stale date produced a phantom.
- **ORY (Oryzon Genomics) — not confirmed.** No issuer date; Oryzon does not pre-announce results dates. TradingView's 2026-10-22 12:00 UTC looks like a placeholder; LSEG (via AJ Bell) and GuruFocus put Q3 on 2026-11-06. Past Q3 releases ran 24 Oct–7 Nov and came after the Madrid close. The hunter returned `event_confirmed: false`.

## What the day can and cannot say

- `selection.method`: random sample of 75 eligible, seed `eu-2026-10-22`. Eligible by market: se 45, uk 8, no 8, fi 7, de 3, es 3, fr 1, dk/it/pl 0. Hunted: se 15, es 2, uk 1, fr 1, no 1. 128 scheduled across the ten markets; no market closed.
- **Calendar sources:** the UK RNS calendar dated 9 rows for the target (added INCH, IES, PSON); Yahoo read on all ten markets and added one row (REJL_B, a phantom); Inderes added 11 SE and 2 FI rows (LINC among them), EQS added 1 DE, Euronext Oslo 1 NO. None read `unavailable`.
- **`options` is null in all ten markets.** Europe runs in the anchor-less regime, which on the sealed US corpus ranked at ρ=+0.073, p=0.45 over 104 events.
- **Short registers resolved for se, uk, no, fr** (and the others read where names were drawn); **es is unreachable**. **`anchor_covered: true` on 4 of 20** (AXFO 3.91%, COOR 1.86%, SBRY 6.73%, VIMIAN 1.63%). Fourteen are truncated zeros (register read, name absent) and two (ORY, VIS) have no register at all.
- **Spain: 2 names (ORY, VIS), Poland: 0.** Those have no positioning anchor and can never be confirmed or killed after the fact; ORY is unranked anyway, so one ranked Spanish name. **Germany: 0**; France 1 (DIM), which since 2026-09-28 cannot reach `event_occurred: false` either.
- **`lean_vs_free_control_rho`**: the last resolved European run (2026-10-08) carries it only for the UK, at 1.0 on 3 names, which is not a measurement. The runs of 10-13 → 10-21 are unresolved; **the Nordic rows of 10-13 to 10-16 are at or near the ~12-day limit of the Nasdaq Nordic feed and should be resolved now**, or their kills become unreachable.
- The lean's weights are priors borrowed from the US runs and measured nowhere in Europe.
- **`history.basis`**: observed for SBRY (`observed_rns`) and ATEA (`observed_newsweb`); **estimated for the other 18**, a scale and not a record of dates. Several hunters found the estimated dates wrong (ATEA's Q2 row misdated by a day; AXFO, KJELL, SVED_B, VIMIAN, PRISMA and BEIJ_B report-day moves recomputed from the real dates), and that is why most `abs_move_pct` sit well above the baseline's proxy.
- **No name sits above the 2.8 conviction floor.** Over the whole US sample the sign was a coin flip below it.
- `language_note`: on the Swedish names the Swedish wire (Finwire/Placera, Börsvärlden, EFN) carried the consensus bars and the report-day reaction tables that no English source had (AXFO, ARJO_B, LOGI_B, SVED_B's disputed SB1 bar, VIMIAN's Modular consensus); issuer releases were bilingual and added nothing. On SBRY the domestic UK sources added nothing; on VIS the guide language and short disclosures came only from Spanish sources; on DIM the exact guidance wording came from the French AMF filing.
- **One day is not a result.**

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.

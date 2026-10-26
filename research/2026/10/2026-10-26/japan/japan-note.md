# Stage J — Japan ranking for 2026-10-26

**Funnel:** 8 scheduled, 5 eligible, 5 hunted, 5 ranked. Three names were dropped on the ¥15m median-turnover floor.
- **Selection:** `all 5 eligible names (at or under the cap)`. The date-seeded random draw (seed `jp-2026-10-26`) had nothing to cut, so no judgement entered the cut.
- **Calendar:** sheets `kessan09_1023` (as of 2026-10-22, 2,920 rows), `kessan08_1002` (2026-10-01) and `kessan` (4 rows).
- **Prompt and model:** `jp.v5`, hunters on claude-opus-5-5 (alias timeline); orchestrator flag not recorded.

**Release times**, as each hunter found them (from each company's prior 短信 timestamps and kabutan's 10-23 schedule, not from a notice for today):
- **Inside the session (1):** 6923 at 15:00. It enters at the sealed 10:06 JST spot (3,572), which already holds that morning's −1.3%.
- **At or after the close (4):** 2211, 7970 and 8060 at 15:30, and 3635 at 16:00. These are measured from the 10-26 close to the 10-27 close.
- **Check 8060:** kabutan's 10-23 list puts 8060 under 取引時間中の発表 (in-session), but every 短信 since 2025-01 was stamped 15:30. The hunter used 15:30; the resolver reads the actual TDnet time.

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`):

| # | code | name | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 7970 | 信越ポリマー (H1) | **+1.90** (p85) | no | +0.54 | 4.5 | 56 |
| 2 | 6923 | スタンレー電気 (H1) | **+1.00** (p68) | no | +0.17 | 2.8 | 53 |
| 3 | 8060 | キヤノンMJ (Q3) | **+0.50** (p43) | no | +0.12 | 3.0 | 52 |
| 4 | 2211 | 不二家 (Q3) | **0.00** (p5) | no | −0.09 | 1.5 | 47 |
| 5 | 3635 | コーエーテクモHD (H1) | **−0.50** (p43) | no | −0.14 | 2.3 | 47 |

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing.
- All four members ran on their pinned `-intl-` agents, with no fallback.
- Selection rule `consensus`: 3 of 4 judges in their own top 20% on the panel's side.
- Each judge's own top 20% starts at: opus5 |1.60|, opus55 |1.00|, sonnet55 |1.05|, fable51 |1.32| (143 live sizes each).

| rank | code | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 7970 | no | 77 | long | 10 | 64L | 89L* | 71L | 85L* | 2 | +1.20 | +1.90 |
| 2 | 3635 | no | 46 | short | 18 | 19S | 69S | 49S | 45S | 0 | −0.49 | −0.50 |
| 3 | 6923 | no | 20 | long | 45 | 49S | 72L | 42L | 16L | 0 | +0.30 | +1.00 |
| 4 | 2211 | no | 23 | short | 7 | 18S | 30S | 15S | 31S | 0 | −0.24 | 0.00 |
| 5 | 8060 | no | 4 | short | 31 | 6L | 0- | 31L | 54S | 0 | +0.06 | +0.50 |

**No name was selected.** 7970 came closest (k = 2): Opus 5.5 and Fable 5.1 put it in their own top 20%, Opus 5 (+1.10) and Sonnet 5.5 (+0.80) did not. All four judges sized 7970 long and as the day's largest name, the same top the hunter picked.

**Where the panel and the hunter disagree most:**
- **6923 Stanley Electric:** the hunter has +1.00, rank 2, but the judges split by sign (sd 45). Opus 5 is short at −0.77: Honda's August Japan output fell 32.3% after the Kumamoto quake, and the street's FY ordinary consensus has not moved in four weeks. The other three judges are long on the FX room and a possible unannounced buyback.
- **8060 Canon MJ:** the hunter has +0.50, but the panel nets to zero. Fable 5.1 is −0.60, Opus 5.5 0.00, Opus 5 +0.16 and Sonnet 5.5 +0.25. The buyback upside is offset by the +13.4% run-in to an all-time high.
- **3635 Koei Tecmo:** ranks 2nd on the panel by size because all four judges are short. The hunter has the same sign and puts it last.
- No name sits above the conviction floor, so there is no floor-clearer the panel skipped.

**What the numbers are not:**
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- The member scales rest on 143 live Japanese sizes each, short of the ~200 at which this market's own range takes over.
- In the four-model re-judge the judges ranked Japan *worse* than the live hunt (ρ −0.25 to −0.31), so nothing about this market's panel is established.
- Pooled over 9 resolved panel days, the JP panel's 13 selected names are 6 of 13 at +0.51% (t 0.22).

## What drives the top and bottom

**Top, 7970 Shin-Etsu Polymer (+1.90).**
- **The main finding (+0.8, guidance; range −1.5 to +2.5):** Q1 operating profit of ¥4,148m was 25.9% of the FY plan and about 10% above the July IFIS Q1. The FY plan only matches consensus, and Q2 laps a weak ¥3,290m base, so an H1 beat and a possible FY raise are open. Source: https://tdnet-pdf.kabutan.jp/20260723/140120260723598058.pdf
- **Smaller findings:**
  - Competitor Miraial (4238) guides wafer-container demand at roughly +65% y/y for Aug–Oct (+0.6): https://kabutan.jp/stock/news?code=4238&b=n202609150791
  - Last year's H1 print brought a buyback and a dividend raise, and a repeat is plausible (+0.4): https://kabutan.jp/stock/news?code=7970&b=n202510240464
  - Margin shorts quadrupled (+0.1).
- **Against it:** the stock sold off 8.9% on an in-line Q1 and fell 4.2% on last year's H1 despite the buyback.

**Bottom, 3635 Koei Tecmo (−0.50).**
- **The main finding (−0.3, guidance):** H1 was pre-released on 10-19 (OP 70 → 115億円) with the full-year plan held in the same document. Consensus FY EPS (about 110, 9 analysts) already sits above the plan, so a held plan is the expected outcome. Last year the same sequence ended at −1.84% the day after the print. Source: https://www.release.tdnet.info/inbs/140120261019552780.pdf
- **Smaller findings:**
  - Crowded margin longs at a 信用倍率 of 24.86 (−0.2).
  - The pre-released H1 itself is sized 0.0.
- This is a near-zero, not a short.

**Names that could not be ranked:** none. All five events were confirmed by the hunters for 2026-10-26.

## Standing caveats

- **No option anchor; substituted by positioning.**
  - JPX short register (as of 2026-10-23, 610 codes): none of the five names is on it. That is a real zero, truncated at 0.5%, so the register components carry no information today.
  - 信用倍率 resolved for all five: 3635 24.86, 7970 2.14, 8060 1.89, 6923 1.57, 2211 0.74.
  - `baseline_quality` read 0.60 on all five, against 0.725 on the 2026-09-11 universe.
  - The lean's component weights are **priors** with no Japanese measurement behind them.
- **`lean_vs_free_control_rho`:** the last resolved runs, both resolved this morning, read 0.5 (10-21) and −1.0 (10-22), each on 3 names, which is meaningless at that size. The larger days read 0.4 (10-20, 4 names) and 0.531 (10-15, 25 names). It has not climbed back toward 1.0.
- **`history` is an estimated cadence**: a scale for how much the name moves, not a record of dates. The 8060 hunter recomputed reactions on real release dates and got a median of about 2.1%. No date in the baseline is cited here as a fact.
- **Signs on the key:** 3 positive, 1 exactly zero, 1 negative, all small. The first resolved days were five of seven negative.
- **Conviction floor:** no name sits above the 2.8 floor. Over the whole US sample, the sign below the floor was a coin flip.
- **Price limits:** the daily 値幅制限 truncates the tail. That is unlikely to bind at today's sizes.
- **One day is not a result.** Five names on one day establish nothing about whether these companies can be ranked; ρ comes only from pooled resolved days. 10-21 and 10-22 were resolved in this run; 10-23 resolves after today's close.

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._

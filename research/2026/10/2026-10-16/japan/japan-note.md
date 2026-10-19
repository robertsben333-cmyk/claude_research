# Stage J — Japan ranking for 2026-10-16

**Answer first.** Two Tokyo names were hunted, both J-REITs whose fiscal period ended in August, and both release at 15:30 JST, after the close. The day is close to empty. **3462 Nomura Real Estate Master Fund ranks first at +0.25**, carried by a buyback the fund has not disclosed. **2972 Sankei Real Estate ranks last at +0.00**: its units are pinned to a ¥125,000 tender offer and its period result was pre-released on 09-25. Neither name clears the 2.8 conviction floor. The four-model panel selects nothing.

- **Funnel:** 3 scheduled → 2 eligible above the ¥15m median 20-day turnover floor → 2 hunted. 2411 GENDAI AGENCY was dropped on turnover (¥7.4m/day).
- **Draw:** `selection.method` is "all 2 eligible names (at or under the cap)", with seed `jp-2026-10-16`. No random draw was needed because the eligible set is below the cap of 25.
- **Calendar:** JPX sheets `kessan08_1002` (as_of 2026-10-01) and `kessan09_1009` (as_of 2026-10-08).
- **Provenance:** prompt `jp.v5`; hunters ran on claude-opus-5-5, per the alias timeline.
- **Orders:** this stage places none.

## Ranked table (`score_report.py`)

| # | ticker | session | impact_sum (key) | floor | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3462 | amc | **+0.25** (p23) | no | +0.04 (p14) | 1.1 | 52 |
| 2 | 2972 | amc | **+0.00** (p5) | no | +0.00 (p7) | 0.3 | 50 |

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing. All four members ran, none through a fallback.

| rank | ticker | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3462 | – | 16 | long | 14 | 5L | 40L | 11L | 10L | 0 | +0.16 | +0.25 |
| 2 | 2972 | – | 0 | – | 0 | 0 | 0 | 0 | 0 | 0 | +0.00 | +0.00 |

- **Selected:** none. No judge put either name in its own top 20%.
- **Agreement:** the panel and the hunter agree on sign and on order for both names. Every member sized 2972 at exactly 0 (the tender pin), and every member sized 3462 small and positive: a possible buyback, net of interest-cost pressure on the new guide.
- **What the panel numbers are not:**
  - `panel_score` ranks; it does not forecast.
  - There is no `expected_edge_pct` off the US.
  - `p_up` is recorded and decides nothing.
  - The member scales are still mostly the frozen E-P seed.
  - In the four-model re-judge, the judges ranked Japan worse than the live hunt. Nothing about this market's panel is established.

## Top and bottom

- **Top, 3462, +0.25.** The main finding is a possible 自己投資口取得 (+0.4, range −0.3 to +2.0), announced with these results.
  - The fund did this at its October 2024 print and rose 2.18% the next session, its largest of the last six print reactions: https://kabutan.jp/stock/news?code=3462&nmode=0&date=20241000
  - Peer GLP REIT announced a ¥10bn buyback with its results on 10-15.
  - Units now trade at 134,600, below the 2024 level.
  - Nothing has been disclosed, so this is an inference.
  - Against it, refinancing at 2.84% 7-year fixed weighs on the Feb-2027 guide (−0.2): https://tdnet-pdf.kabutan.jp/20260824/140120260824525088.pdf
  - The hunter found no 四季報/IFIS consensus, so every size is capped small.
- **Bottom, 2972, +0.00.** City Index Fifth is tendering at ¥125,000 per unit, running 2026-09-28 to 2026-11-10. Spot is ¥125,100, and the units have closed within ¥125,000–125,400 every session since 09-28: https://kabutan.jp/stock/news?code=2972&b=n202609280155
  - The period result and distribution (¥3,681) were pre-released on 09-25, so the print has nothing to reprice.
  - The real catalyst is the tender outcome on 11-10, outside the window.
  - The baseline's +19.26% 20-day run-up and 3.77% move proxy are both the tender jump, not a scale for this print.

## Unranked

None. Both names are rankable.

## Standing caveats

- **No option anchor; it is substituted by positioning.**
  - Neither name is on the JPX short register at or above 0.5% (a real zero, truncated by the threshold).
  - 信用倍率 resolved for 3462 (20.73) and is null for 2972.
  - The lean is therefore mostly the run-up term: 2972's −0.96 is the tender jump, and 3462's −0.34 is margin overhang plus run-up.
  - The lean weights are priors with no Japanese measurement behind them.
- **`lean_vs_free_control_rho`** was **0.406** on the last resolved run (2026-10-13), so the lean has not collapsed back into the free control.
- **`history`** is an estimated cadence: a scale, not a record of dates.
- **Release times:** both 15:30 JST as the hunters found them, from prior 決算短信. None releases inside the session, so both windows run from the 10-16 close to the 10-19 close.
- **Signs:** zero negative, one positive and one zero. On the first resolved Japanese days, five of seven calls were negative.
- **Conviction floor:** no name is above 2.8. Over the whole US sample, the sign was a coin flip below the floor.
- **Price limits:** daily 値幅制限 truncate large moves. This is irrelevant at these sizes.
- **One day is not a result.** Two REIT names, one of them structurally pinned, cannot be ranked against each other in any meaningful way.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

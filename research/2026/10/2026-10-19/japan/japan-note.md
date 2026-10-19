# Stage J — Japan ranking for 2026-10-19

**Answer first.** Four Tokyo names were hunted. All four are J-REITs reporting their August-2026 period, and all four release after the 15:30 JST close. Every number is small.

- **Top: 3295 Hulic Reit, +0.40.** It is carried by the sponsor asset swap feeding the first Aug-2027 guide.
- **Bottom: 3488 CENTRAL REIT, −0.40.** It is carried by BOJ hikes that its floating debt has not yet passed into the DPU guide.

No name clears the 2.8 conviction floor. The four-model panel selects nothing.

- **Funnel:** 4 scheduled, 4 eligible above the ¥15m median 20-day turnover floor, 4 hunted.
- **Draw:** `selection.method` is "all 4 eligible names (at or under the cap)", with seed `jp-2026-10-19`. No random draw was needed, because the eligible set is below the cap of 25.
- **Calendar:** two JPX sheets were read: `kessan08_1002` (as_of 2026-10-01) and `kessan09_1016` (as_of 2026-10-15). Hunters 3295, 3488 and 8984 re-confirmed the date on kabutan. 3481's date rests on the JPX sheet and its cadence, because its IR calendar returned 403.
- **Provenance:** prompt `jp.v5`. Hunters ran on claude-opus-5-5, per the alias timeline.
- **Orders:** this stage places none.

## Ranked table (`score_report.py`)

| # | ticker | session | impact_sum (key) | floor | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3295 | amc | **+0.40** (p33) | no | +0.08 (p17) | 0.8 | 55 |
| 2 | 8984 | amc | **+0.30** (p27) | no | +0.13 (p22) | 1.3 | 55 |
| 3 | 3481 | amc | **+0.10** (p14) | no | +0.00 (p7) | 1.2 | 50 |
| 4 | 3488 | amc | **-0.40** (p33) | no | -0.13 (p22) | 0.8 | 42 |

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing. All four members ran, and none ran through a fallback.

| rank | ticker | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3481 | – | 25 | short | 14 | 39S | 2S | 26S | 32S | 0 | −0.34 | +0.10 |
| 2 | 8984 | – | 19 | long | 8 | 6L | 25L | 22L | 24L | 0 | +0.23 | +0.30 |
| 3 | 3488 | – | 25 | short | 15 | 13S | 16S | 19S | 50S | 0 | −0.22 | −0.40 |
| 4 | 3295 | – | 11 | long | 5 | 6L | 12L | 19L | 9L | 0 | +0.16 | +0.40 |

- **Selected:** none. No judge put any name in its own top 20%. The top-20% thresholds were opus5 |1.68|, opus55 |1.10|, sonnet55 |1.08| and fable51 |1.44|, each over 121 live sizes.
- **Largest disagreement, 3481.** The hunter nets it to +0.10: a −0.30 guide on refinancing (0.26% → 2.41–2.47% fixed) against a +0.35 peer-led buyback chance. All four judges put it on the short side. Opus 5 sized the refinancing at −1.00 and discounted the buyback as cash-constrained by the Daito acquisition. The panel ranks it first by size; the hunter ranks it third.
- **The panel's smallest, 3295.** It is the hunter's top name and the panel's smallest. The judges read the swap arithmetic as public for three weeks.
- **What the panel numbers are not:**
  - `panel_score` ranks; it does not forecast.
  - There is no `expected_edge_pct` off the US.
  - `p_up` is recorded and decides nothing.
  - The member scales are still mostly the frozen E-P seed.
  - In the four-model re-judge, the judges ranked Japan worse than the live hunt. Nothing about this market's panel is established.

## Top and bottom

**Top, 3295 Hulic Reit, +0.40.**
- The main finding is +0.3 on guidance. The 2026-09-25 sponsor asset swap (QUARTZ SHINSAIBASHI and the Eastnet Building in, three older assets out) adds an estimated +¥423m NOI per period plus a ¥199m exchange gain. The first Aug-2027 guide, due with this print, is the first to carry a full period of it, under a stated DPU ≥ ¥4,000 policy: https://tdnet-pdf.kabutan.jp/20260925/140120260925540059.pdf
- A second finding, +0.1, is the beat-or-meet habit on its own DPU forecast.
- Against it: the swap has been public three weeks, and the last seven print reactions were all under 1%.

**Bottom, 3488 CENTRAL REIT, −0.40.**
- The main finding is −0.5 on guidance. The April DPU forecasts (¥3,343 Aug-2026, ¥3,143 Feb-2027) were struck on 1M TIBOR as of 2026-02-27, with only 55.4% of ¥25.2bn of debt fixed: https://tdnet-pdf.kabutan.jp/20260417/140120260417506041.pdf
  - The BOJ has since hiked 0.75% → 1.25%: https://www.dir.co.jp/report/research/economics/japan/20260918_026078.html
  - On about ¥11.2bn of floating debt that is roughly ¥106 a unit, about 3.4% of the Feb-2027 DPU, landing in the revised and first guides at this print.
  - The name has no coverage, and its margin long is crowded (信用倍率 4,359).
- The other finding is +0.1 for a likely small beat on the reported period.
- Against it: an actual −4.8% guide cut in April moved the units only −0.36% over the window.

**8984 (+0.30)** rests on a possible unit buyback. One was announced at both prior August-period prints, and the units trade at about 0.69x NAV: https://tdnet-pdf.kabutan.jp/20260416/140120260415504786.pdf

## Unranked

None. All four names are rankable.

## Standing caveats

- **No option anchor; it is substituted by positioning.**
  - None of the four is on the JPX short register at or above 0.5% (as of 2026-10-16). That is a real zero, truncated by the threshold, with no change.
  - 信用倍率 resolved for all four: 3295 49.19, 3481 9.63, 3488 4,359, 8984 185.
  - The lean is therefore margin overhang plus run-up: −0.59, −0.28, −1.83 and −0.87.
  - The lean weights are priors with no Japanese measurement behind them. `jp_resolve.py` ranks each component separately.
- **`lean_vs_free_control_rho`** was **0.406** on the last resolved run (2026-10-13). It has not climbed back toward 1.0, so the lean has not collapsed into the free control.
- **`history`** is an estimated cadence: a scale, not a record of dates.
- **Release times, as the hunters found them:** 3295 15:30, 3481 15:30, 3488 15:30, 8984 15:45 (inferred; past prints were 15:30–16:00). None releases inside the session, so every window runs from the 10-19 close to the 10-20 close.
- **Signs:** one negative (3488) and three positive. On the first resolved Japanese days, five of seven calls were negative.
- **Conviction floor:** no name is above 2.8. Over the whole US sample, the sign was a coin flip below the floor.
- **Correlated exposure:** all four are J-REITs sharing one driver, the domestic rate path. Their 20-day moves track the REIT ETF 1343 (−4.3% to −5.2%), so the day is closer to one sector bet than four independent names.
- **Price limits:** daily 値幅制限 truncate large moves. This is irrelevant at these sizes.
- **Run note:** two hunters collided on a shared scratch file. 3295's hunter re-fetched its own bars before using them.
- **One day is not a result.** Four sub-1-point REIT calls on one rate theme cannot establish anything about ranking.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

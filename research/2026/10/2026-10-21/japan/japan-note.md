# Stage J — Japan ranking for 2026-10-21

**Funnel:** 5 scheduled, 3 eligible, 3 hunted. Two names were dropped on the ¥15m median-turnover floor: 4929 アジュバン (¥1.9m) and 5576 オービーシステム (¥5.9m).
- **Selection:** `all 3 eligible names (at or under the cap)`. The date-seeded random draw (seed `jp-2026-10-21`) had nothing to cut.
- **Calendar:** sheets `kessan09_1016` (as of 2026-10-15), `kessan08_1002` (2026-10-01) and `kessan` (3 rows).
- **Prompt and model:** `jp.v5`, hunters on claude-opus-5-5.

**Release times**, as each hunter found them from prior 短信 timestamps:
- **296A at 11:30 JST.** It releases inside the session, so it enters at the sealed 10:05 spot (¥1,198).
- **8953 at 15:30 and 3290 at 16:30.** Both release at or after the close, so their window runs from the 10-21 close to the 10-22 close.

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`):

| # | code | name | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 296A | Reiwa Accounting HD (H1) | **+0.50** (p42) | no | +0.24 | 4.0 | 53 |
| 2 | 8953 | Japan Metropolitan Fund | **+0.35** (p32) | no | +0.08 | 0.8 | 55 |
| 3 | 3290 | One REIT | **+0.25** (p23) | no | +0.03 | 0.8 | 52 |

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence. The panel ranks beside `impact_sum` and replaces nothing. All four members ran on their pinned models, with no fallback.

| rank | code | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 296A | no | 68 | long | 9 | 57L | 64L | 80L* | 71L | 1 | +0.86 | +0.50 |
| 2 | 8953 | no | 22 | long | 11 | 29L | 36L | 17L | 8L | 0 | +0.24 | +0.35 |
| 3 | 3290 | no | 9 | long | 6 | 2L | 16L | 11L | 5L | 0 | +0.10 | +0.25 |

**No name was selected.** Only Sonnet 5.5 put 296A in its own top 20%, so k = 1 against the 3 needed.

The panel agrees with the hunter on order and sign for all three names. Every judge sized 296A larger than the hunter did, at +0.6 to +1.05 against +0.50: they weight the full-year upgrade binary more heavily.

What the numbers are not:
- `panel_score` ranks; it does not forecast.
- There is no `expected_edge_pct` off the US.
- `p_up` is recorded and decides nothing.
- Member scales are still mostly the frozen E-P seed (129 live sizes each).
- In the four-model re-judge the judges ranked Japan *worse* than the live hunt, so nothing about this market's panel is established.

## What drives the top and bottom

**Top, 296A Reiwa Accounting (+0.50).**
- **The main finding (+1.0, guidance).** On 9/14 the company raised H1 operating profit 20% to ¥1,054m but held the full-year plan at ¥2,160m. That plan implies H2 OP about 5% below last year after H1 grew 28.5%. The company's own H1 share of the year (41–44%) runs the full year at about ¥2.4–2.56bn, so an upgrade at this print is live; the hunter puts it at about 30%.
- **Source:** https://tdnet-pdf.kabutan.jp/20260914/140120260910533968.pdf
- **Against it:**
  - Implied Q2 slowed to about +10% OP year on year (−0.2), from https://tdnet-pdf.kabutan.jp/20260721/140120260717595695.pdf.
  - The 8/21 中期経営計画 promises a capital increase (−0.3), from https://tdnet-pdf.kabutan.jp/20260821/140120260821524177.pdf.
  - Last year the company held the plan at the same point and raised it only in March.
  - Margin longs are crowded (信用倍率 5.03) after a +59% run since July.

**Bottom, 3290 One REIT (+0.25).**
- **A near non-result.** On 2026-09-28 the REIT reaffirmed its Aug-2026 DPU of ¥2,440 after the period had ended, raised Feb-2027 to ¥2,475 and gave a first Aug-2027 guide of ¥2,780. All of this was filed before the print and sized at 0, from https://tdnet-pdf.kabutan.jp/20260928/140120260928541004.pdf.
- **The only live item (+0.15).** A further above-appraisal property sale could come with the 短信. The manager is running sale processes on about 15% of the portfolio, per https://tdnet-pdf.kabutan.jp/20260928/140120260928541062.pdf. The timing is the hunter's inference.

**8953 JMF (+0.35).**
- **The main finding.** The first Aug-2027 DPU guide comes with this release. The Life Shimodera land sale (about ¥290 a unit of gain) points to a guide at or above ¥2,970, per https://tdnet-pdf.kabutan.jp/20260917/140120260916537271.pdf.
- **Why it stays small:** the last four guide raises moved the units −0.34% to −2.26% the next session.

**Names that could not be ranked:** none. All three were rankable.

## Standing caveats

- **No option anchor; substituted by positioning.**
  - All three names are absent from JPX's short register (as of 2026-10-20). That is a real zero, truncated at 0.5%, so there is no change to read.
  - 信用倍率 resolved for all three: 296A 5.03, 3290 591, 8953 236. The two REITs carry extreme margin-long overhangs, and that overhang drives their negative leans (−1.31 and −0.80).
  - The lean's component weights are **priors** with no Japanese measurement behind them.
- **`lean_vs_free_control_rho`:** 0.531 on the last resolved run, 2026-10-15 (25 names). Earlier runs read 0.789 on 10-14, 0.406 on 10-13 and 0.367 on 10-09. It has not collapsed back to 1.0, so the positioning sources are still resolving. The 10-16 run (2 names) withheld it, and 10-19 and 10-20 are unresolved.
- **`history` is an estimated cadence**: a scale for how much the name moves, not a record of dates.
- **Signs:** 3 positive, 0 negative. The first resolved days were five of seven negative; today has no negatives at all, which is itself a tilt to watch.
- **Conviction floor:** no name sits above the 2.8 floor. Over the whole US sample, the sign below the floor was a coin flip.
- **Correlated exposure:** two of three names are J-REITs with August periods, and both drifted down on rates. The scorer cannot see that correlation.
- **Price limits** (値幅制限) truncate the tail, but they are irrelevant at today's sizes. 296A has hit limit-up before (on its 中計).
- **One day is not a result.** Three names cannot be ranked meaningfully against each other, and ρ is withheld below five at resolution.

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._

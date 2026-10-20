# Stage J — Japan ranking for 2026-10-20

**Funnel:** 5 scheduled / 4 eligible (1 dropped on the ¥15m median-turnover floor) / 4 hunted. Selection: `all 4 eligible names (at or under the cap)`; the date-seeded draw (seed `jp-2026-10-20`) did not need to cut. All four release at **15:30 JST, after the close** (per each hunter's prior-短信 timestamps), so none enters at the sealed spot; window = 2026-10-20 close → 2026-10-21 close. Prompt `jp.v5`, hunters on claude-opus-5-5.

Ranked on `impact_sum` (the `ranking_key` in `edge-scores.json`):

| # | code | name | impact_sum (key) | floor 2.8 | impact_scaled (v3) | abs_move | p_up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5933 | Alinco (Q2) | **+0.70** (p53) | no | +0.25 | 2.5 | 55 |
| 2 | 8968 | Fukuoka REIT | **+0.45** (p37) | no | +0.15 | 1.1 | 57 |
| 3 | 3466 | LaSalle LOGIPORT REIT | **+0.40** (p34) | no | +0.11 | 1.4 | 54 |
| 4 | 3226 | Mitsui Fudosan Accommodations Fund | **+0.00** (p5) | no | −0.04 | 0.9 | 48 |

## Panel

Four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing. All four members ran, no fallback.

| rank | code | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | impact_sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3466 | no | 42 | long | 16 | 52L | 64L | 23L | 30L | 0 | +0.52 | +0.40 |
| 2 | 5933 | no | 41 | long | 20 | 18L | 59L | 61L | 24L | 0 | +0.43 | +0.70 |
| 3 | 8968 | no | 33 | long | 16 | 25L | 59L | 17L | 30L | 0 | +0.29 | +0.45 |
| 4 | 3226 | no | 19 | short | 4 | 18S | 17S | 17S | 26S | 0 | −0.22 | +0.00 |

No name selected: no judge put any name in its own top 20% (k = 0 everywhere). Disagreements with the hunters: the panel puts 3466 first where the hunter put it third (Opus 5 sized the gain-supported FP27/8 guide at +0.50); all four judges put 3226 on the short side where the hunter netted to zero (funding-cost drag on the 43期 guide weighted more heavily). Two judges (Opus 5, Opus 5.5) restored the 5933 FX-loss item the hunter dropped as "contradicted by document" without naming the document — a fair criticism of the hunt. What the numbers are not: `panel_score` ranks and does not forecast; no `expected_edge_pct` off the US; `p_up` decides nothing; member scales are still mostly the frozen E-P seed (125 live sizes each); and in the four-model re-judge the judges ranked Japan *worse* than the live hunt, so nothing about this market's panel is established.

## What drives the top and bottom

- **Top, 5933 Alinco (+0.70):** Q1 operating profit ¥782m is 55.9% of an unchanged H1 OP plan of ¥1,400m (48.7% a year ago), so Q2 needs only ¥618m vs ¥613m last year — a modest H1 beat is likely. +0.6. Source: Q1 決算短信, https://tdnet-pdf.kabutan.jp/20260717/140120260717595946.pdf. Against it: the progress rate was public and bought in July (+3.1%), Q1 included pull-forward procurement, all three prior H1 prints fell, 信用倍率 12.1x.
- **Bottom, 3226 Mitsui Fudosan Accommodations (0.00):** three findings net to zero; the negative carrying it is the funding-cost drag on the first 43期 DPU guide (BOJ at 1.0% since June; ¥13bn/¥14bn refinancing; 41期 maturities at 0.25% rolled at 1.43%), −0.15, source https://www.naf-r.jp/file/ir_library_term-46c6aab89fcf47da99b4b391559cf8b76903f5db.pdf, offset by +0.20 for ¥6.36bn of acquisitions outside the 42期 forecast (https://tdnet-pdf.kabutan.jp/20261001/140120261001544166.pdf).

No name was unrankable.

## Required caveats

- **Signs:** 3 positive, 0 negative, 1 zero. The first resolved Japanese days were five of seven negative; today leans the other way, on three J-REITs whose prints are mostly pre-released.
- **Conviction floor:** none of the four is above 2.8 (largest 0.70, p53 of the Opus 5.5 reference). Over the whole US sample the sign was a coin flip below the floor, so this ranking is near-noise by construction.
- **Option anchor substituted:** no Japanese single-stock options. Positioning components resolved for all four: JPX short register (all four absent, a real zero at the 0.5% threshold, as of 2026-10-19) and 信用倍率 (3226 41.0x, 3466 26.0x, 5933 12.1x, 8968 7.6x). With every short position at zero, the lean is the margin overhang plus run-up; `anchor_quality.direction` 0.6. The lean's weights are **priors** with no Japanese measurement behind them.
- **`lean_vs_free_control_rho`** from the last resolved runs (resolved this session): **0.531** on 2026-10-15 and **0.789** on 2026-10-14 (0.406 on 10-13). 0.789 is drifting toward 1.0 — watch it: if it reaches 1.0 the positioning sources have stopped carrying information and the lean is the run-up alone. Those days ranked at ρ −0.067 (10-14) and +0.085 (10-15), both noise.
- **`history` is an estimated cadence**, a scale and not a record of dates. The 5933 hunter found the estimated-date proxy (1.7%) understates actual-date reactions (~3.3% median).
- **Price limits** (値幅制限) truncate the tail; irrelevant at today's sizes.
- **Three of four names are J-REITs** with August fiscal periods reporting together: a correlated exposure to the REIT index (1343 fell 5–7% over 20 days) that the scorer cannot see.
- **One day is not a result.** Four names cannot be ranked meaningfully against each other (ρ is withheld below five at resolution).

_This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone._

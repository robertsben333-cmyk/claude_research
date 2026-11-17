# Stage E-P — 2026-11-17 amc + 2026-11-18 bmo

**This is stage E-P: Opus 5.5 searchers, then a blind four-model panel sized their evidence. Since 2026-10-19 this stage also trades its book, on the live and paper Alpaca accounts (step 6b, after this note).**
All four judges ran: Opus 5 (`claude-opus-5`), Opus 5.5, Sonnet 5.5 and Fable 5.1. Each was pinned and none fell back.
One day is an anecdote.

Window: 32 calendar rows. The sweep confirmed 29; KNDI, CAAP and CISS were phantoms (vendor projections or no quarterly report). 20 names were searched under the `hunted_names` cap, in `hunt_priority` order. Shed for the cap: GLNG, AUNA, HAFN, IRIX, TJX, GBDC, LOW, GLAD and NVDA. All 20 searches finished (`hunt_status`: 0 unfinished).

## The panel

Every rankable name, in `panel_score.py` order. `panel_pct` runs 0-100 and the side sits in its own column. Each member is shown as its own percentile, with L or S for its side and `*` where it is in its own top 20%.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | JMIA | bmo 11-18 | **yes** | 84 | short | 9 | 72S | 88S* | 78S* | 96S* | 3 | -1.38 | -1.10 | +3.16% [+1.09, +5.16] | 0.63 | 1.0 | 1.00 |
| 2 | ICCM | bmo 11-18 | **yes** | 84 | short | 16 | 55S | 91S* | 94S* | 94S* | 3 | -1.74 | -1.20 | +3.12% [+1.05, +5.11] | 0.63 | 1.0 | 0.91 |
| 3 | FEAM | amc 11-17 | **yes** | 82 | short | 9 | 69S | 82S* | 84S* | 94S* | 3 | -1.35 | -3.50 | +2.96% [+0.92, +4.93] | 0.62 | 1.0 | 1.03 |
| 4 | ENRD | bmo 11-18 |  | 74 | short | 12 | 64S | 75S | 94S* | 65S | 1 | -1.04 | -1.40 | +1.93% [+0.35, +3.73] | 0.56 | 0.0 | 0.00 |
| 5 | BLSH | bmo 11-18 |  | 64 | short | 8 | 54S | 60S | 74S | 70S | 0 | -0.92 | -0.40 | +1.14% [+0.02, +2.72] | 0.56 | 0.0 | 0.00 |
| 6 | LZB | amc 11-17 |  | 62 | short | 23 | 23S | 70S | 84S* | 70S | 1 | -1.02 | -0.90 | +0.94% [-0.07, +2.44] | 0.56 | 0.0 | 0.00 |
| 7 | GLBE | bmo 11-18 |  | 60 | long | 20 | 26L | 68L | 78L* | 68L | 1 | +0.96 | +0.30 | +0.83% [-0.12, +2.29] | 0.56 | 0.0 | 0.00 |
| 8 | PRE | bmo 11-18 |  | 52 | long | 23 | 14L | 60L | 76L | 60L | 0 | +0.82 | -0.50 | +0.33% [-0.36, +1.63] | 0.56 | 0.0 | 0.00 |
| 9 | SQM | amc 11-17 |  | 44 | short | 19 | 17S | 57S | 66S | 37S | 0 | -0.60 | -0.80 | +0.29% [-0.49, +1.07] | 0.56 | 0.0 | 0.00 |
| 10 | JJSF | bmo 11-18 |  | 44 | long | 22 | 43L | 57L | 66L | 8L | 0 | +0.68 | +0.40 | +0.29% [-0.49, +1.05] | 0.56 | 0.0 | 0.00 |
| 11 | IIIV | amc 11-17 |  | 42 | long | 12 | 49L | 22L | 54L | 42L | 0 | +0.60 | +1.50 | +0.29% [-0.50, +1.00] | 0.56 | 0.0 | 0.00 |
| 12 | ZTO | amc 11-17 |  | 40 | short | 11 | 32S | 52S | 28S | 50S | 0 | -0.55 | +0.05 | +0.29% [-0.51, +0.94] | 0.56 | 0.0 | 0.00 |
| 13 | TGT | bmo 11-18 |  | 35 | long | 16 | 28L | 62L | 30L | 20L | 0 | +0.40 | -0.30 | +0.29% [-0.54, +0.87] | 0.56 | 0.0 | 0.00 |
| 14 | PONY | bmo 11-18 |  | 34 | long | 38 | 32S | 57L | 59L | 50L | 0 | +0.69 | +0.60 | +0.29% [-0.55, +0.86] | 0.56 | 0.0 | 0.00 |
| 15 | DLB | amc 11-17 |  | 30 | short | 32 | 20L | 46S | 30S | 65S | 0 | -0.47 | +0.20 | +0.29% [-0.56, +0.85] | 0.56 | 0.0 | 0.00 |
| 16 | ZKH | bmo 11-18 |  | 17 | long | 13 | 4L | 38L | 12L | 14L | 0 | +0.24 | +1.10 | +0.29% [-0.63, +0.81] | 0.56 | 0.0 | 0.00 |
| 17 | CSHR | bmo 11-18 |  | 14 | long | 23 | 8L | 16L | 16S | 48L | 0 | +0.19 | -0.40 | +0.29% [-0.66, +0.81] | 0.56 | 0.0 | 0.00 |
| 18 | KRNT | bmo 11-18 |  | 14 | short | 12 | 22S | 16S | 6L | 22S | 0 | -0.27 | -0.20 | +0.29% [-0.66, +0.81] | 0.56 | 0.0 | 0.00 |
| 19 | BRBR | bmo 11-18 |  | 7 | short | 51 | 43L | 68S | 47S | 45L | 0 | +0.04 | +1.20 | +0.29% [-0.71, +0.79] | 0.56 | 0.0 | 0.00 |
| 20 | ZIM | bmo 11-18 |  | 6 | long | 2 | 4L | 8L | 6L | 4L | 0 | +0.13 | -0.40 | +0.29% [-0.72, +0.79] | 0.56 | 0.0 | 0.00 |

**Selected (panel_pct ≥ 80, all four judges): JMIA, ICCM and FEAM, all short.** All three were also selected under the old 3-of-4 rule (k = 3).

`expected_return_pct` restates the percentile, not a separate forecast. Every name at the same `panel_pct` carries the same expected return. It is gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50.

## The selected names

- **JMIA (bmo, short, 84).** Every judge's note leads on one item: Omdia has African smartphone shipments at −39% YoY in Q3 (−7% in Q2), published 30 Oct, after Jumia last spoke. Transsion's −27% revenue corroborates it. That lands on the GMV guide (+15–25%) and the Q4 breakeven message, with phones and electronics about 30% of GMV. Pleasant Lake cutting its stake from 7.48% to 4.5% adds supply.
  *Against:* it is an industry proxy on one segment. GMV is value, not units, and Transsion raised ASPs. The stock is at a 52-week low with call-heavy open interest (put/call 0.29). The searcher itself put it at only −1.10.
- **ICCM (bmo, short, 84).** About $8M of estimated cash against a $4.8M market cap. The going-concern doubt is likely repeated, and a proxy-documented chairman RSU tranche vests only on a financing of at least $6.5M, which is more than the market cap. A reverse-split vote follows on 11-19, and the last three prints were sold (−3.2%, −8.9%, −11.5%).
  *Against:* it is hard to borrow, with an undated 578.9% borrow fee and a +20% spike on a patent release on 11-09, so squeeze convexity. **Turnover is $0.10m/day, below the $200k floor, so the book cannot trade it.**
- **FEAM (amc, short, 82).** The quarter was already filed in the 10-Q on 11-16. Tonight turns on the funding gap (about $24m peak need against $15.6m cash, going-concern language, no committed facility) and the first loss-making weeks of Searles Valley. The searcher's own key is the only name above the 2.8 floor (−3.50).
  *Against:* the stock is already −39% over 20 days, a debt facility backed by customer contracts would be a relief, and it is thin at $0.52m/day (expect a limited-liquidity warning).

## Where the panel and the searcher disagree most

- **IIIV:** the searcher's top long (+1.50) is only 42 on the panel; Opus 5.5 has it at 22. The crowded short and the buyback did not carry the judges against the FY27-guide risk.
- **BRBR:** the searcher has +1.20, but the panel is 7 and split by side (Opus 5 and Fable long, Opus 5.5 and Sonnet short, sd 51).
- **ZKH:** +1.10 from the searcher against 17 on the panel, because the judges gave the inside-guide GMV beat little weight.
- **ICCM and JMIA:** the searcher had −1.20 and −1.10, below its floor; the panel puts both in the top 16%.

## Stage E

There is no `research/2026/11/2026-11-17/edge/` (stage E's Routine is stopped), so there is no overlap or ρ with stage E's `impact_sum` today.

## What the numbers are not

- `expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have earned. Its out-of-sample record is weak: +0.12 correlation with the realised return over 148 names. It is not a forecast to size on.
- The weights in this table are research.
- `p_up` is recorded and decides nothing.
- No adversary pass and no second searcher checked the findings, so a factually wrong item enters at full size.
- The key is not reproducible to better than its own size: four of twelve double-hunt pairs once came back with opposite signs.
- Sign balance of the searcher's key: 8 positive, 12 negative.
- 10 of the 20 hunted names had a usable option chain; the rest lean on realised volatility or reaction histories the searchers rebuilt. The foreign issuers' baselines carry no 6-K reaction history, because `SEC_USER_AGENT` is not set here.

## Searcher scores (comparison arm)

**Stage E-P (searcher), 2026-11-17**: ranked on `impact_sum` (version 2, each finding sized on its own); conviction floor 2.8 applies to it only.
V2 at `session_close`, matrix as of 2026-11-17T18:08:13+00:00.
Brackets: percentile of |value| among reference names sized by Opus 5.5 (impact_sum n=957, impact_scaled n=974): live runs to date plus the blind re-judges, September Opus 5.5 hunts left out. Scale, not rank.

| # | ticker | session | impact_sum (key) | floor | impact_scaled (v3) | abs_move | p_up | V2 grounded | retail ≥50 | search quiet | vol ≥58 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | IIIV | amc | **+1.50** (p84) | no | +0.63 (p73) | 10.5 | 53 | +0.90 | yes (56) | n/a (sparse) | no (36) |
| 2 | BRBR | bmo | **+1.20** (p78) | no | +0.68 (p75) | 17.0 | 52 | +1.49 | yes (74) | n/a (sparse) | yes (61) |
| 3 | ZKH | bmo | **+1.10** (p76) | no | +0.88 (p83) | 11.0 | 54 | +1.34 | yes (67) | n/a (sparse) | yes (95) |
| 4 | PONY | bmo | **+0.60** (p54) | no | +0.48 (p63) | 12.0 | 52 | +0.60 | yes (63) | n/a (sparse) | yes (60) |
| 5 | JJSF | bmo | **+0.40** (p39) | no | +0.28 (p43) | 7.0 | 52 | +0.29 | no (42) | n/a (sparse) | no (30) |
| 6 | GLBE | bmo | **+0.30** (p31) | no | +1.04 (p87) | 13.0 | 54 | +0.63 | no (43) | n/a (failed) | no (44) |
| 7 | DLB | amc | **+0.20** (p22) | no | -0.48 (p63) | 8.0 | 47 | -0.14 | no (34) | n/a (sparse) | no (23) |
| 8 | ZTO | amc | **+0.05** (p9) | no | -0.22 (p36) | 5.5 | 48 | -0.05 | no (24) | n/a (failed) | no (17) |
| 9 | KRNT | bmo | **-0.20** (p22) | no | +0.00 (p6) | 6.0 | 50 | -0.54 | yes (52) | n/a (sparse) | no (40) |
| 10 | TGT | bmo | **-0.30** (p31) | no | +0.42 (p58) | 7.0 | 53 | -0.43 | no (32) | no (1.05x) | no (40) |
| 11 | BLSH | bmo | **-0.40** (p39) | no | -0.88 (p83) | 11.0 | 46 | -0.24 | yes (60) | yes (0.90x) | yes (91) |
| 12 | CSHR | bmo | **-0.40** (p39) | no | -0.18 (p31) | 9.0 | 49 | -0.09 | yes (64) | n/a (sparse) | yes (68) |
| 13 | ZIM | bmo | **-0.40** (p39) | no | -0.11 (p21) | 5.5 | 49 | -0.10 | no (44) | n/a (sparse) | no (30) |
| 14 | PRE | bmo | **-0.50** (p46) | no | -0.22 (p36) | 11.0 | 49 | -0.29 | yes (70) | n/a (failed) | yes (74) |
| 15 | SQM | amc | **-0.80** (p64) | no | -0.42 (p58) | 7.0 | 47 | -0.81 | no (36) | n/a (sparse) | no (49) |
| 16 | LZB | amc | **-0.90** (p68) | no | -0.72 (p77) | 12.0 | 47 | -0.20 | yes (57) | no (1.07x) | no (42) |
| 17 | JMIA | bmo | **-1.10** (p76) | no | -1.20 (p90) | 15.0 | 46 | -2.40 | yes (72) | n/a (failed) | yes (62) |
| 18 | ICCM | bmo | **-1.20** (p78) | no | -1.00 (p86) | 10.0 | 45 | -1.84 | yes (98) | n/a (failed) | yes (111) |
| 19 | ENRD | bmo | **-1.40** (p82) | no | -1.10 (p88) | 11.0 | 45 | -2.59 | yes (64) | n/a (failed) | yes (83) |
| 20 | FEAM | amc | **-3.50** (p98) | yes | -1.92 (p96) | 12.0 | 42 | -7.34 | yes (78) | n/a (failed) | yes (100) |

Not ranked: AUNA: no hunt

Not ranked: CAAP: no hunt

Not ranked: CISS: no hunt

Not ranked: GBDC: no hunt

Not ranked: GLAD: no hunt

Not ranked: GLNG: no hunt

Not ranked: HAFN: no hunt

Not ranked: IRIX: no hunt

Not ranked: KNDI: no hunt

Not ranked: LOW: no hunt

Not ranked: NVDA: no hunt

Not ranked: TJX: no hunt

`session` is when the print lands: `amc` after the close, `bmo` before the open; `?` = not confirmed by the sweep, `n/a` = no print (stage R).
`impact_scaled` is the hunter's second, separate measurement, (2·p_up/100 − 1)·abs_move. It is not the key and is never pooled with it.
`retail`, `search` and `vol` are context for the reader, shown for every name whatever its score: retail tilt ≥ 50, a Google search spike under 1.0x on the last complete day, and 20-day realised volatility ≥ 58% annualised. Nothing ranks, selects, sizes or trades on them.

## Context: retail, search and volatility (not used for selection)

The retail ≥ 50, search quiet and vol ≥ 58 columns above come from `edge_context.py`. They are context only: nothing ranks, selects, sizes or trades on them.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

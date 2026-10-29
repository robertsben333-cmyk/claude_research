# Stage E-P — 2026-10-29 amc + 2026-10-30 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel.** Since 2026-10-19 it is the only stage trading the Alpaca paper account (step 6b, after this note is published).
All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), natively, 20 of 20 names each, one part, no fallback.
One day is an anecdote.

Universe: 167 names (117 amc 10-29, 50 bmo 10-30), all baselines sealed before any agent. The sweep checked 24: 14 company-confirmed, 10 unconfirmed, 0 phantoms, 143 unchecked. All 14 confirmed plus the 6 highest-priority unconfirmed (REAL, AXTI, COUR, STOK, PINS, GDYN) were searched; every one of the 20 searchers then confirmed its event (PINS without a company notice: options expiry, third-party calendars and the CFO 8-K). Shed: CVCO, RDDT, MSTR, STRZ (unconfirmed) and every unchecked name. **No searcher hit a search budget** (`hunt_status.py check`: 0 unfinished of 20). AMZN and INTC sealed empty baselines (`bars_failed: HTTPError`); their searchers sourced spot and implied move from the press, so V2 could not be computed for them.

## Panel table

`panel_pct` is the mean of the judges' own percentiles, 0-100, with the side in its own column. A member cell is that judge's percentile against its own live range: L/S gives its side, `*` marks a name in that judge's own top 20%. `E[return]` is what names at this percentile have earned on the panel's side: one number per percentile, gross, on the scorebord window, and flat at about +0.3% below a percentile of 50. It translates the percentile; it is not a separate forecast.

| # | ticker | session | selected | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | w_equal | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AXTI | amc | yes | 97 | long | 2 | 100L* | 96L* | 97L* | 95L* | 4 | +2.36 | +4.50 | +4.88% [+2.97, +6.59] | 0.72 | 1.0 | 1.00 |
| 2 | CRI | bmo |  | 77 | long | 4 | 82L* | 75L | 72L | 80L* | 2 | +1.07 | +2.80 | +2.30% [+0.49, +4.17] | 0.58 | 0.0 | 0.00 |
| 3 | CDNA | amc |  | 74 | long | 18 | 48L | 94L* | 68L | 86L* | 2 | +1.11 | +3.40 | +1.90% [+0.33, +3.69] | 0.56 | 0.0 | 0.00 |
| 4 | PTCT | amc |  | 71 | long | 6 | 76L | 78L | 62L | 67L | 0 | +0.99 | +1.20 | +1.63% [+0.25, +3.35] | 0.56 | 0.0 | 0.00 |
| 5 | PINS | amc |  | 68 | long | 25 | 25L | 83L* | 77L | 86L* | 2 | +1.17 | +1.00 | +1.40% [+0.14, +3.04] | 0.56 | 0.0 | 0.00 |
| 6 | ATEC | amc |  | 63 | short | 16 | 86S* | 68S | 44S | 54S | 1 | -0.73 | -1.00 | +1.04% [-0.02, +2.59] | 0.56 | 0.0 | 0.00 |
| 7 | SPSC | amc |  | 57 | short | 12 | 71S | 60S | 58S | 39S | 0 | -0.63 | -0.50 | +0.56% [-0.22, +2.05] | 0.56 | 0.0 | 0.00 |
| 8 | INTC | amc |  | 54 | long | 16 | 71L | 48L | 30L | 67L | 0 | +0.68 | -0.40 | +0.36% [-0.31, +1.78] | 0.56 | 0.0 | 0.00 |
| 9 | REAL | amc |  | 53 | short | 24 | 90S* | 27S | 58S | 36S | 1 | -0.53 | -0.50 | +0.34% [-0.35, +1.67] | 0.56 | 0.0 | 0.00 |
| 10 | ALHC | amc |  | 52 | short | 32 | 84S* | 30S | 10S | 82S* | 2 | -0.76 | -0.90 | +0.32% [-0.38, +1.58] | 0.56 | 0.0 | 0.00 |
| 11 | AMZN | amc |  | 51 | long | 14 | 48L | 66L | 30L | 62L | 0 | +0.66 | +0.40 | +0.31% [-0.39, +1.55] | 0.56 | 0.0 | 0.00 |
| 12 | MIAX | amc |  | 50 | short | 22 | 40S | 78S | 62S | 20S | 0 | -0.56 | -0.20 | +0.30% [-0.42, +1.46] | 0.56 | 0.0 | 0.00 |
| 13 | GDYN | amc |  | 31 | short | 10 | 46S | 34S | 20S | 24S | 0 | -0.36 | -0.40 | +0.29% [-0.56, +0.85] | 0.56 | 0.0 | 0.00 |
| 14 | COLM | amc |  | 21 | long | 23 | 56L | 26L | 3S | 4L | 0 | +0.19 | +0.30 | +0.29% [-0.59, +0.82] | 0.56 | 0.0 | 0.00 |
| 15 | CPRI | bmo |  | 18 | long | 32 | 17L | 27L | 58L | 32S | 0 | +0.28 | +0.90 | +0.29% [-0.62, +0.82] | 0.56 | 0.0 | 0.00 |
| 16 | COUR | amc |  | 17 | long | 31 | 34S | 48L | 20L | 34L | 0 | +0.35 | +0.70 | +0.29% [-0.63, +0.81] | 0.56 | 0.0 | 0.00 |
| 17 | FND | amc |  | 15 | long | 23 | 52L | 9S | 0- | 16L | 0 | +0.14 | -0.70 | +0.29% [-0.65, +0.81] | 0.56 | 0.0 | 0.00 |
| 18 | STOK | amc |  | 13 | long | 14 | 36L | 14L | 0- | 4L | 0 | +0.14 | +0.20 | +0.29% [-0.66, +0.81] | 0.56 | 0.0 | 0.00 |
| 19 | OSPN | amc |  | 13 | short | 13 | 34S | 8S | 0- | 9S | 0 | -0.15 | +0.20 | +0.29% [-0.67, +0.81] | 0.56 | 0.0 | 0.00 |
| 20 | SUPN | amc |  | 7 | long | 7 | 20L | 4L | 2L | 4L | 0 | +0.10 | +0.35 | +0.29% [-0.71, +0.79] | 0.56 | 0.0 | 0.00 |

**Selected (panel_pct >= 80, all four judges present): AXTI long (97).** The old 3-of-4 rule selects the same one name. Next: CRI 77 (2 of 4 in own top), CDNA 74, PTCT 71, PINS 68. A one-name book.

## The selected name

- **AXTI (long, 97; every judge in its own top 20%, sd 2).** AXT's Q3 revenue guide (~$66M) counts only revenue already covered by Chinese export permits, and consensus sits on that floor; the same construction printed $47.6M against a $34M guide last quarter (+28.7% reaction). Short interest is 18.3% of shares outstanding and rose into a sector sell-off with no company news; substrate prices kept rising. The searcher rebuilt the reaction history on the five real prints (median |move| ~21% against a 12.4% straddle), because three baseline rows were not earnings. *Against:* skew is −14.6 (calls already bid), the stock rose 10.6% on 10-28 on the Tongmei funding 8-K, Q4 consensus already equals stated year-end indium-phosphide capacity so the first Q4 guide may disappoint, and permit timing has missed before (Q4 2025). The date rests on Earnings Whispers "confirmed", a Quiver Quant citation of the IR notice and a Business Wire headline seen as a snippet — not on a fetched company page.

## Where the panel and the searcher disagree most

- **CDNA:** searcher +3.40 (p97, above the 2.8 floor) against panel_pct 74. Opus 5 put it at 48: an ordinary beat at a 52-week high above most targets, with a 2026 history of selling beats.
- **CRI:** searcher +2.80 (p95, at the floor) against panel_pct 77; two judges in their own top 20%, two not.
- **REAL and ALHC:** searcher −0.5 and −0.9; Opus 5 at 90S and 84S, the others far lower (27-58), so the panel lands at 52-53.
- **PINS:** Opus 5 at 25L (a CFO three days in sets the first Q4 guide) against 77-86L for the other three.

## Stage E comparison

Stage E's `<RUN>/edge/` does not exist: its Routine is stopped since 2026-10-19. No overlap and no Spearman ρ.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct`) is what names at that percentile have earned, with a weak out-of-sample record (correlation +0.12 with the realised return over 148 names) — not a forecast to size on. The weights are research. `p_up` is recorded and decides nothing. Nothing checked the findings for factual error (no adversary, one searcher per name), and the key is not reproducible to better than its own size (four of twelve double-hunted pairs once came back with opposite signs). Searcher sign balance: 12 positive, 8 negative. Below the 2.8 floor the searcher's sign has been a coin flip; three names clear it (AXTI, CDNA, CRI). The free control `-run_up_20d_pct` is in `edge-scores.json`.

## Context: retail, search and volatility (not used for selection)

From `edge-context.json` (context only; nothing ranks, selects or sizes on it). AXTI: retail tilt 66, search quiet (0.94x), 20-day vol 109% annualised. The full per-name table is in the score_report output in the closing reply.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

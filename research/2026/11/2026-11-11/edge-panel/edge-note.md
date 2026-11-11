# Stage E-P — 2026-11-11 amc + 2026-11-12 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel.** The panel's book is traded on the Alpaca paper account in step 6b. Stage E's Routine is stopped, so this stage is the only one connected to the account.
**All four members ran on their pinned agents:** Opus 5 (`claude-opus-5`), Opus 5.5 (`claude-opus-5-5`), Sonnet 5.5 (`claude-sonnet-5-5`) and Fable 5.1 (`claude-fable-5-1`). Each covered 20/20 names in one part, with no fallback and no retry.
**One day is an anecdote.** Only the pooled record says anything.

Universe 124 names (34 amc 11-11, 90 bmo 11-12). The sweep checked 33, confirmed 29, found 4 unconfirmed and 0 phantoms, and left 91 unchecked. The 20 hunted were the top 20 confirmed names by `hunt_priority`; the rest were shed (see the run log). All 20 searches completed (`hunt_status`: 0 unfinished).

## Panel table (every rankable name)

Each judge is shown as a percentile of its own live range, 0-100, with L/S for its side; `*` marks a name in that judge's own top 20%. `E[ret]` is the expected return at that panel_pct, the translation of the percentile and not a separate forecast. It is gross, on the scorebord's window, with an 80% band and the hit rate, and it is flat at about +0.3% below a percentile of 50.

| rank | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[ret] [80%] | p_right | w_eq | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CURI | 2026-11-11 amc | **yes** | 94 | short | 9 | 78S | 100S* | 98S* | 100S* | 3 | -2.82 | -3.80 | +4.56% [+2.55, +6.37] | 0.71 | 1.00 | 0.75 |
| 2 | CTVA | 2026-11-11 amc | **yes** | 87 | short | 4 | 80S* | 90S* | 91S* | 88S* | 4 | -1.52 | -1.90 | +3.67% [+1.57, +5.66] | 0.66 | 1.00 | 1.25 |
| 3 | CAE | 2026-11-11 amc |  | 74 | short | 10 | 90S* | 60S | 70S | 76S | 1 | -1.06 | -1.60 | +1.92% [+0.34, +3.71] | 0.56 | 0.00 | 0.00 |
| 4 | NBIS | 2026-11-12 bmo |  | 53 | long | 26 | 72L | 11L | 78L* | 49L | 1 | +0.89 | +2.30 | +0.34% [-0.35, +1.67] | 0.56 | 0.00 | 0.00 |
| 5 | TTEK | 2026-11-11 amc |  | 47 | short | 11 | 61S | 41S | 33S | 54S | 0 | -0.63 | -1.40 | +0.29% [-0.46, +1.25] | 0.56 | 0.00 | 0.00 |
| 6 | CINT | 2026-11-11 amc |  | 38 | long | 11 | 54L | 42L | 32L | 24L | 0 | +0.43 | +0.85 | +0.29% [-0.53, +0.90] | 0.56 | 0.00 | 0.00 |
| 7 | ITRG | 2026-11-11 amc |  | 37 | short | 9 | 50S | 26S | 32S | 38S | 0 | -0.43 | -1.10 | +0.29% [-0.54, +0.89] | 0.56 | 0.00 | 0.00 |
| 8 | LUNR | 2026-11-12 bmo |  | 36 | short | 10 | 22S | 42S | 33S | 49S | 0 | -0.44 | +1.00 | +0.29% [-0.54, +0.89] | 0.56 | 0.00 | 0.00 |
| 9 | DGII | 2026-11-11 amc |  | 36 | long | 17 | 14L | 33L | 62L | 36L | 0 | +0.42 | +0.40 | +0.29% [-0.54, +0.88] | 0.56 | 0.00 | 0.00 |
| 10 | AVEX | 2026-11-11 amc |  | 31 | long | 30 | 6L | 14L | 83L* | 22L | 1 | +0.26 | +0.50 | +0.29% [-0.56, +0.86] | 0.56 | 0.00 | 0.00 |
| 11 | YETI | 2026-11-12 bmo |  | 30 | short | 15 | 6S | 30S | 42S | 44S | 0 | -0.39 | +0.50 | +0.29% [-0.56, +0.85] | 0.56 | 0.00 | 0.00 |
| 12 | ALVO | 2026-11-11 amc |  | 26 | long | 9 | 38L | 16L | 18L | 33L | 0 | +0.33 | +0.20 | +0.29% [-0.57, +0.84] | 0.56 | 0.00 | 0.00 |
| 13 | EZPW | 2026-11-11 amc |  | 17 | long | 9 | 2L | 17L | 25L | 24L | 0 | +0.27 | +0.30 | +0.29% [-0.63, +0.81] | 0.56 | 0.00 | 0.00 |
| 14 | XNDU | 2026-11-11 amc |  | 14 | short | 15 | 8L | 13S | 33S | 19S | 0 | -0.25 | +1.00 | +0.29% [-0.66, +0.81] | 0.56 | 0.00 | 0.00 |
| 15 | ASND | 2026-11-12 bmo |  | 13 | short | 8 | 20S | 5S | 5S | 24S | 0 | -0.21 | -0.10 | +0.29% [-0.66, +0.81] | 0.56 | 0.00 | 0.00 |
| 16 | AGBK | 2026-11-11 amc |  | 11 | long | 9 | 2L | 6L | 25L | 10L | 0 | +0.16 | +1.20 | +0.29% [-0.68, +0.80] | 0.56 | 0.00 | 0.00 |
| 17 | DDI | 2026-11-11 amc |  | 5 | long | 2 | 2L | 6L | 7L | 4L | 0 | +0.10 | -0.20 | +0.29% [-0.73, +0.78] | 0.56 | 0.00 | 0.00 |
| 18 | VYLR | 2026-11-11 amc |  | 4 | long | 3 | 6L | 0- | 7L | 6L | 0 | +0.10 | +0.10 | +0.29% [-0.73, +0.78] | 0.56 | 0.00 | 0.00 |
| 19 | ENS | 2026-11-11 amc |  | 0 | short | 28 | 6L | 18L | 48S | 22L | 0 | +0.20 | +0.30 | +0.29% [-0.76, +0.78] | 0.56 | 0.00 | 0.00 |
| 20 | ACOG | 2026-11-11 amc |  | 0 | short | 29 | 50S | 16L | 18L | 16L | 0 | +0.22 | -0.10 | +0.29% [-0.76, +0.78] | 0.56 | 0.00 | 0.00 |

**Selected (panel_pct >= 80, all four members present): CURI short 94 and CTVA short 87.** CAE (short, 74) is next. With two strong names, the 2026-11-11 top-up rule (70-79 names on a one-name day) does not apply. The 3-of-4 consensus verdict agrees: CURI k=3, CTVA k=4.

## The selected names

**CURI (CuriosityStream), short, panel_pct 94, 2026-11-11 amc.** All four judges cite the same primary-document item. In the Q2 10-Q (https://www.sec.gov/Archives/edgar/data/1776909/000162828026056713/curi-20260630.htm), Q2's record $23.2m revenue included $8.5m recognised upfront from a $10m Curiosity Brands licence, paid in instalments from 2027, plus $5.3m of barter licence fees. Remaining performance obligations for the rest of 2026 are only $1.9m. Yet the single-source Q3 revenue bar of $20.3m (finviz, 2026-11-03) needs about $11m of licensing, roughly double the ex-one-off run rate. The second item is dividend funding: cash was $5.4m, H1 operating cash flow was −$3.0m against $9.9m of dividends, and a revolver liquidity test applies. **Strongest case against:** the 10-Q has been public since August and the stock has already given back its entire Q2 jump to sit 1% above its 52-week low. The CEO bought 50k shares in the open market after the 10-Q (Form 4, 2026-08-27/28). A 14% yield means a dividend cut is partly priced. The quarterly bar has one source. The option-implied move is about 23% on a wide chain, and Opus 5 held this off its own extreme (78th percentile) for these reasons.

**CTVA (Corteva, post-spin crop protection), short, panel_pct 87, 2026-11-11 amc.** Five crop-protection peers reported after Corteva last spoke, all weaker: FMC like-for-like revenue −22% with quarter-end channel destocking (2026-10-29), Syngenta, Bayer core CP −6%, ADAMA LatAm −8% and UPL LatAm −8%. Corteva's crop-protection consensus still carries about +4% year on year ($1.77bn, Earnings Whispers 2026-11-03). Judges also note the headline risk that consolidated Q3 statements, with seed still inside, may read as a miss against the CP-only $0.09. **Strongest case against:** CTVA fell more than 4% on FMC's 10-15 warning and is −10.75% over 20 days, so part of this is priced. At about 6x 2026 EBITDA it sits below post-spin targets of $15-20 against $11.96. Some peers say volume shifted into Q4. The baseline reaction history describes the pre-spin company, so the move scale rests on a thin post-spin option chain (9.5% implied).

## Where the panel and the searcher disagree most

- **AGBK:** the searcher has +1.2, the panel 11 long. The judges read twelve small, capped findings on a disputed bar as near-zero.
- **NBIS:** the searcher has +2.3, the panel 53 long. Opus 5.5 put it at only the 11th percentile, against Opus 5 at 72 and Sonnet 5.5 at 78, with Vineland/Microsoft delivery risk set against the GPU price rise.
- **LUNR:** the searcher has +1.0, the panel 36 short. The judges weighted the backlog-conversion shortfall against the guide low end over the bookings and crowded-short items.
- **XNDU** (+1.0 against 14 short) and **YETI** (+0.5 against 30 short) are the same pattern: positive positioning items that the judges shrank.

## Stage E

Stage E's `<RUN>/edge/` does not exist for this date; its Routine is stopped. There is no overlap or ρ to report.

## What the numbers are not

`expected_return_pct` (and `expected_edge_pct`, the same expectation as a signed move) is what names at that percentile have earned, gross, on the scorebord window. Its out-of-sample record is weak, a correlation of +0.12 with the realised return over 148 names, so it is not a forecast to size on. The weights are research. The book is sized by `execution.panel` in `alpaca_trade.py` (panel_pct − 60, 50% cap a name), not by these columns. Certainty (`p_up`) is recorded and decides nothing. One searcher name clears the 2.8 `impact_sum` conviction floor: CURI at −3.8. NBIS at +2.3 does not.

## Not ranked

104 universe names were not hunted. 91 were unchecked by the sweep, 4 were unconfirmed (OPRX, TWST, PLGO, AGRO), and 9 were confirmed but below priority 42 (TNK, ECO, CEPU, FNV, HBM, OR, TK, BSRT, BN). All sit in `edge-scores.json` as `rankable: false` ("no hunt"). There were no unfinished searches.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

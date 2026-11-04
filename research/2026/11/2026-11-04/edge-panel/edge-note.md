# Stage E-P — 2026-11-04 amc + 2026-11-05 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel. Since 2026-10-19 it trades the Alpaca paper account (step 6b), on the panel's rule only.**
Members that ran: all four, each as its pinned agent — `panel-judge-opus5` (claude-opus-5), `panel-judge-opus55` (claude-opus-5-5), `panel-judge-sonnet55` (claude-sonnet-5-5), `panel-judge-fable51` (claude-fable-5-1). No fallback and no retry; every judge covered 20 of 20 packs.
One day is an anecdote.

Universe 504 names (277 amc 11-04, 227 bmo 11-05). The sweep checked 26 names: 22 were company-confirmed, 4 were unconfirmed (DAVE, WRBY, HUBS, SNAP) and 0 were phantoms; the other 478 were not checked. Cap 20: SHAK and TRIP were shed on the lowest hunt_priority, along with the 4 unconfirmed names. All 20 searchers finished (`search_complete: true`, 0 unfinished).

## Panel table (every rankable name)

Member percentiles are each judge's own 0-100 percentile against its last 200 live sizes, with the side as L/S (`*` = in that judge's own top 20%). `E[ret]` is the expected return at this panel_pct, with its 80% band and `p_right`.

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[ret] (80% band) | p_right | w_eq | w_tilt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | U | bmo | **yes** | 93 | long | 2 | 94L* | 94L* | 90L* | 94L* | 4 | +1.93 | +1.60 | +4.54% [+2.52, +6.35] | 0.71 | 1 | 1.25 |
| 2 | CAVA | amc | **yes** | 85 | short | 9 | 94S* | 88S* | 70S | 89S* | 3 | -1.56 | -0.40 | +3.40% [+1.29, +5.41] | 0.65 | 1 | 0.96 |
| 3 | BYND | amc | **yes** | 82 | short | 10 | 85S* | 65S | 84S* | 93S* | 3 | -1.36 | +0.10 | +2.84% [+0.82, +4.81] | 0.62 | 1 | 1.00 |
| 4 | ROOT | amc | | 79 | short | 6 | 88S* | 72S | 78S | 80S | 2 | -1.17 | -1.00 | +2.54% [+0.59, +4.46] | 0.60 | 0 | 0 |
| 5 | FSLY | amc | | 77 | long | 11 | 74L | 60L | 86L* | 89L* | 2 | +1.24 | +0.60 | +2.27% [+0.48, +4.15] | 0.58 | 0 | 0 |
| 6 | ELF | amc | | 73 | short | 15 | 94S* | 61S | 80S* | 56S | 2 | -0.98 | -0.10 | +1.81% [+0.30, +3.57] | 0.56 | 0 | 0 |
| 7 | CORZ | bmo | | 65 | long | 16 | 91L* | 65L | 50L | 54L | 1 | +0.81 | +1.60 | +1.18% [+0.04, +2.77] | 0.56 | 0 | 0 |
| 8 | LMND | bmo | | 52 | short | 9 | 38S | 54S | 62S | 52S | 0 | -0.68 | +0.60 | +0.33% | 0.56 | 0 | 0 |
| 9 | RUN | amc | | 50 | short | 16 | 45S | 58S | 70S | 26S | 0 | -0.63 | +0.10 | +0.29% | 0.56 | 0 | 0 |
| 10 | CHYM | amc | | 50 | short | 9 | 48S | 38S | 50S | 62S | 0 | -0.58 | -0.50 | +0.29% | 0.56 | 0 | 0 |
| 11 | PTON | bmo | | 46 | short | 24 | 45S | 12S | 44S | 82S* | 1 | -0.49 | +0.70 | +0.29% | 0.56 | 0 | 0 |
| 12 | CELH | bmo | | 45 | long | 48 | 35S | 81L* | 84L* | 51L | 2 | +1.01 | +0.60 | +0.29% | 0.56 | 0 | 0 |
| 13 | SEZL | amc | | 44 | short | 34 | 74S | 0 | 23S | 80S | 1 | -0.66 | +1.10 | +0.29% | 0.56 | 0 | 0 |
| 14 | OSCR | bmo | | 37 | long | 47 | 38S | 80L* | 34L | 74L | 1 | +0.70 | +0.70 | +0.29% | 0.56 | 0 | 0 |
| 15 | WOLF | amc | | 25 | long | 43 | 68L | 52L | 44S | 22L | 0 | +0.48 | +1.80 | +0.29% | 0.56 | 0 | 0 |
| 16 | LEU | amc | | 23 | long | 56 | 86L* | 23L | 47L | 66S | 1 | +0.38 | +1.30 | +0.29% | 0.56 | 0 | 0 |
| 17 | JOBY | amc | | 21 | long | 19 | 44L | 4S | 9L | 36L | 0 | +0.32 | +0.40 | +0.29% | 0.56 | 0 | 0 |
| 18 | EOSE | bmo | | 8 | short | 38 | 22S | 38S | 56L | 29S | 0 | -0.38 | -0.10 | +0.29% | 0.56 | 0 | 0 |
| 19 | FIG | amc | | 8 | short | 48 | 56S | 12L | 61L | 51S | 0 | -0.24 | -0.20 | +0.29% | 0.56 | 0 | 0 |
| 20 | NVAX | bmo | | 4 | long | 34 | 64L | 16S | 16S | 15S | 0 | -0.22 | +0.80 | +0.29% | 0.56 | 0 | 0 |

How to read this table:
- **Selection rule:** a name is selected when panel_pct >= 80 and all four members are present. The old 3-of-4 rule would pick the same three names (U k=4; CAVA and BYND k=3).
- **Expected return:** this is the translation of the percentile, not a separate forecast. Every name at the same panel_pct carries the same number. It is gross, on the scorebord's window, and flat at about +0.3% below a percentile of 50.
- **What decides nothing:** the weights are research; the book is placed by `execution.panel` in `alpaca_trade.py`.

## The selected names

**U (Unity), long, 93; all four judges in their own top 20%.** The evidence is the searcher's lead finding:
- In Q2, Vector grew about 23% q/q against management's own 12-13% plan, and runtime engine data only began feeding it at the end of Q2.
- The Q3 Grow guide ($380-385m) implies only 19-21%.
- Consensus revenue sits on the guide midpoint ($565.5m Zacks, unchanged 30 days).
- The stock paid +18% and +15% on its last two Vector beat-and-raise prints.
- A BofA note says only Unity 6 games feed runtime data so far.

Strongest case against: the 25-delta skew pays 7 vol points for downside, insiders made 17 sales and no buys in six months, and the stock is up 146% off its 52-week low. It sold a weak guide hard (-26% in 2026-02, on a beat). The searcher also lists AppLovin's arbitration over Unity's Ad Quality SDK as an unresolved negative. AppLovin's own print, reportedly tonight, is a read-through of unknown sign.

**CAVA, short, 85; three judges in their top 20% (sonnet55 at 70).** Every judge's note names two items:
- The Street's FY same-restaurant-sales estimate (6.8%) sits above the top of management's own 4.5-6.5% guide, so a floor-only raise lands below the bar.
- Chipotle's CFO said on 2026-10-28 that "October trends have softened, consistent with the broader industry", which is the quarter-to-date line CAVA comments on tonight.

All of this comes after a +17% five-day run-up. Strongest case against: the Baird checks after the 2026-10-14 menu launch (from a paywalled preview), short interest of 13-15% that has been rising, and Placer foot traffic that implies roughly in-line comps. The put skew (+16.5) already leans the same way as the panel.

**BYND (Beyond Meat), short, 82; three judges in their top 20% (opus55 at 65).** The judges' common items:
- The stock fell after all 8 of its last 8 prints, including Q2 2026, which beat revenue consensus by 10-13% and fell 13.4%.
- There is a live financing overhang: the 2026-09-23 note exchange is floored at $7.40 against a $7.43 spot, ATM access is gone, and about $14.5m of 2027 notes remain.

Strongest case against: a crowded and rising short (about 34% of the share class, 6.9 days to cover), and options pay for upside (skew -8.4). **BYND is not lendable at Alpaca on this snapshot**, so the book drops it; check borrow at IBKR before calling it untradeable.

## Where the panel and the searcher disagree most

- **CAVA**: the searcher has -0.40, near zero; the panel has 85 short.
- **BYND**: the searcher has +0.10 (scaled -1.20); the panel has 82 short. The searcher's crowded-short finding offset its own reaction-history negative, and three judges weighted it less.
- **WOLF**: the searcher's top name (+1.80, p87 of its own range); the panel has 25 long, with the judges split.
- **LEU**: the searcher has +1.30; the panel has 23 long. Fable 5.1 is on the short side and only Opus 5 is in its top 20%.
- **SEZL**: the searcher has +1.10; the panel has 44 short. Opus 5.5 gives exactly 0, while Opus 5 and Fable 5.1 lean short.

## Stage E comparison

Stage E's `<RUN>/edge/edge-scores.json` does not exist (its Routine is stopped), so there is no overlap or Spearman ρ against stage E's impact_sum today.

## What the numbers are not

- **The expected return** (`expected_return_pct`, and `expected_edge_pct` on the selected names) is what names at that percentile have earned in the past. Its out-of-sample record is weak: +0.12 correlation with the realised return over 148 names. It is not a forecast to size on.
- **Certainty (`p_up`)** is recorded and decides nothing.
- **The searcher's `impact_sum`** ranks the comparison arm; no name clears the 2.8 floor today.
- **The baseline** has a live option chain for all 20 hunted names. The SEZL and EOSE reaction histories are not earnings base rates (implausible cadence); both searchers rebuilt them from confirmed releases.
- **Nothing checked the findings** beyond the four judges' reading of them. A factually wrong item enters at full size.
- **Sign balance (searcher):** 14 of 20 hunts leaned positive. The judges leaned the other way: Opus 5 put 13 of 20 on the short side.

## Context: retail, search and volatility (not used for selection)

These labels are context only; nothing selects, sizes or trades on them. See `score_report.py`'s table: retail >= 50, search quiet and vol >= 58, per name.

## Unfinished searches

None. All 20 searchers returned `search_complete: true`.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

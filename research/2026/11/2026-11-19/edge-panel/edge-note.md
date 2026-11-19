# Stage E-P — 2026-11-19 amc + 2026-11-20 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel.** All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1); no fallback was used and none is missing. One day is an anecdote.

**Answer first.** The panel selects one name, **GRSD short** (panel_pct 81, two of four judges in their own top 20%). It cannot be traded on this account: Alpaca will not lend it and it turns over $0.19m a day, under the $200k floor. BSP long (panel_pct 79) is the only name in the 70-79 top-up band. The top-up applies only when exactly one strong name is *in the book*, so with GRSD dropped it does not apply. **Step 6b therefore buys nothing on either account**, and both accounts stay flat after step 3s sold EVAX and MMS.

## The panel table

Each judge's figure is its own percentile, 0-100, of its live range; `*` marks that judge's own top 20%. E[return] is the gross expected return at that `panel_pct`, on the scorebord window, read off one curve. It is the same for every name at the same percentile and flat at about +0.3% below 50. It translates the percentile into a return and is not a separate forecast.

| # | ticker | session | sel | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | k | panel_score | searcher impact_sum | E[return] (80% band) | P(right) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GRSD | amc 11-19 | **yes** | 81 | short | 12 | 67 S | 74 S | 96 S* | 88 S* | 2 | -1.28 | -2.80 | +2.77% [+0.76, +4.73] | 0.61 |
| 2 | BSP | bmo 11-20 | | 79 | long | 11 | 64 L | 75 L | 93 L* | 84 L* | 2 | +1.24 | +2.50 | +2.49% [+0.57, +4.41] | 0.59 |
| 3 | ROST | amc | | 68 | long | 9 | 72 L | 75 L | 72 L | 52 L | 0 | +1.07 | +0.90 | +1.39% [+0.14, +3.03] | 0.56 |
| 4 | KEYS | amc | | 57 | long | 11 | 39 L | 62 L | 66 L | 60 L | 0 | +0.84 | +2.40 | +0.56% | 0.56 |
| 5 | GLOB | amc | | 56 | long | 13 | 72 L | 36 L | 60 L | 57 L | 0 | +0.76 | +0.70 | +0.48% | 0.56 |
| 6 | FRO | bmo | | 55 | long | 12 | 47 L | 54 L | 74 L | 45 L | 0 | +0.68 | +1.10 | +0.38% | 0.56 |
| 7 | NGVC | amc | | 53 | short | 12 | 38 S | 54 S | 72 S | 50 S | 0 | -0.68 | -1.70 | +0.35% | 0.56 |
| 8 | BULL | amc | | 52 | long | 7 | 47 L | 44 L | 60 L | 59 L | 0 | +0.71 | +0.80 | +0.33% | 0.56 |
| 9 | GRRR | amc | | 52 | short | 14 | 44 S | 60 S | 70 S | 34 S | 0 | -0.71 | +0.70 | +0.32% | 0.56 |
| 10 | POST | amc | | 40 | short | 15 | 22 S | 60 S | 30 S | 50 S | 0 | -0.52 | -1.40 | +0.29% | 0.56 |
| 11 | GAP | amc | | 40 | long | 20 | 44 L | 10 L | 38 L | 66 L | 0 | +0.54 | -0.70 | +0.29% | 0.56 |
| 12 | EARN | amc | | 30 | long | 8 | 38 L | 24 L | 38 L | 21 L | 0 | +0.38 | +0.20 | +0.29% | 0.56 |
| 13 | INTU | amc | | 23 | long | 21 | 7 S | 50 L | 17 L | 30 L | 0 | +0.30 | +0.90 | +0.29% | 0.56 |
| 14 | MOG.A | bmo | | 14 | short | 12 | 34 S | 4 S | 8 S | 8 S | 0 | -0.16 | -0.30 | +0.29% | 0.56 |
| 15 | ESTC | amc | | 13 | short | 37 | 56 S | 16 L | 30 L | 42 S | 0 | -0.16 | -0.90 | +0.29% | 0.56 |
| 16 | BKE | bmo | | 11 | long | 15 | 18 L | 3 L | 30 L | 8 S | 0 | +0.17 | +0.20 | +0.29% | 0.56 |
| 17 | WRD | bmo | | 10 | long | 14 | 20 L | 28 L | 8 S | 0 | 0 | +0.14 | +0.60 | +0.29% | 0.56 |
| 18 | ESE | amc | | 10 | long | 8 | 18 L | 4 L | 17 L | 0 | 0 | +0.16 | +0.70 | +0.29% | 0.56 |
| 19 | RLX | bmo | | 7 | short | 16 | 16 L | 0 | 23 S | 22 S | 0 | -0.15 | -0.10 | +0.29% | 0.56 |
| 20 | MATW | amc | | 6 | long | 22 | 26 L | 13 L | 30 S | 15 L | 0 | +0.24 | +0.50 | +0.29% | 0.56 |

Each member's own top 20% starts at |2.56| for opus5, |1.76| for opus55, |1.60| for sonnet55 and |2.00| for fable51, measured against the last 200 live sizes before today. `weight_equal` and `weight_precision_tilt` are in `edge-scores-panel.json`; they are research and nothing trades them.

## The selected name

**GRSD (Grandstand), short, amc 11-19.**
- **Evidence the judges' notes name:**
  - Catena Media pre-released Q3 on 2026-10-16: revenue -29%, which it blamed on generative search across affiliates.
  - GRSD's own Q2 already showed casino -22% and marketing -10%.
  - The FY guide ($165-170m revenue, $45-50m adj. EBITDA) needs a record Q4, so a fourth guidance cut in a row is the base case.
  - Covenants: a maximum of 3.0x leverage on about $122m of debt, with a $26.5m earnout due. A Q3 adj. EBITDA under about $8.6m breaches the covenant on gross debt.
- **Strongest case against:**
  - The stock is already -42% over 20 days, -59% since the August reaffirm and 2% above its 52-week low.
  - The last print without a cut bought +19%.
  - Better Collective's Q3 North America (+28%) supports the non-SEO two-thirds of revenue.
  - The equity is a roughly $26m stub, so any relief is violent.
- **Tradability:** thin ($0.19m a day) and not lendable at Alpaca on this snapshot; check borrow at IBKR before calling it untradeable. It is the searcher's only floor-clearer (-2.80). V2 grounded reads -6.78.

## Where the panel and the searcher disagree most

- **KEYS:** the searcher's +2.40 is its second-largest, while the panel reads only 57 long. Opus 5 sits at its own 39th percentile, because the supply-capped Q1 guide offsets the peer reads.
- **GRRR:** the searcher has +0.70 long, the panel 52 short. Three of four judges lean short on the convertible-note overhang and the unconfirmed Batam ramp.
- **GAP:** the searcher has -0.70, the panel 40 long. Opus 5 and Fable weigh the tariff relief left out of the guide above the UBS traffic note.
- **GLOB:** Opus 5 puts it at its own 72nd percentile long, on a 25.5% short with 10.7 days to cover; Opus 5.5 has only 36.

## Stage E comparison

Stage E's Routine is stopped and there is no `<RUN>/edge/` for 2026-11-19, so there is no stage E `impact_sum` to correlate. Overlap: 0 names, ρ not computable.

## Names not ranked

BJ, IESC and GEOS were shed before hunting. The sweep could not confirm their event from a company source, and `edge_degrade_order` drops unconfirmed names first, which left exactly 20 confirmed names for 20 slots. MOG.B is a second share class of Moog: `share_class.py` did not fold it, so it was dropped by hand (one issuer is one event).

No unfinished searches: `hunt_status.py` read 0 of 20 unfinished.

## Standing caveats

- **What the numbers are not.** `expected_return_pct` (and `expected_edge_pct` on the selected name) is what names at that percentile have earned. Its out-of-sample record is weak: correlation +0.12 with the realised return over 148 names. It is not a forecast to size on. Certainty (`p_up`) is recorded and decides nothing.
- **Nothing checked the findings.** There is no adversary and no second searcher, so a factually wrong finding reaches the judges unchallenged.
- **Reproducibility.** When paired hunts ran, a third of pairs came back with opposite signs. This is a standing property of every ranking.
- **Anchor.** 9 of 23 baselines carry an option-implied move: INTU, ROST, KEYS, ESTC, GAP, BULL, GLOB, MOG.A and BKE, plus BSP and BJ whose chains are noisy. The rest fall back to a historical median.
- **Foreign filers.** BSP, FRO, BULL, GLOB, GRRR, RLX and WRD have no reaction history in the baseline, because `SEC_USER_AGENT` is unset and EDGAR refused 6-K lookups with 403.
- **Sign balance (searcher).** 13 names lean long and 7 short.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

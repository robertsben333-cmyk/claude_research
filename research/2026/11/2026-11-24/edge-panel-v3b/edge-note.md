# Edge hunt (panel v3b) — 2026-11-24 amc + 2026-11-25 bmo

**This is stage E-P v3b: Opus 5.5 searchers and four blind judges on the v3b prompts, no orders.** All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), no fallback; all 20 searchers ran as `unpriced-searcher-v3b` and every hunt carries the v3b fields. One day is an anecdote: v3b is judged only by `v3b_compare.py`, pooled, against the pre-registration.

Universe 24 rows (11 amc, 13 bmo). Sweep confirmed 22; URBN and ADXN unconfirmed (vendor-only) and shed, HDL and OMSE shed at the 20-name cap on lowest hunt_priority. 20 hunted, 20 rankable.

## Panel (own history, `panel-history-v3b.json`; selection panel_pct >= 80, all four judges)

| # | ticker | sess | sel | panel_pct | side | sd | E-P-scale pct | opus5 | opus55 | sonnet55 | fable51 | k | searcher impact_sum | E[return] (80% band) | p_right | mean p_clears_real_bar | modal guide_direction |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PSNY | bmo | yes | 96 | short | 2 | 97 | 94S* | 99S* | 94S* | 98S* | 4 | -5.10 | +4.83% [+2.89, +6.55] | 0.721 | 31 | cut |
| 2 | NNOX | bmo | yes | 92 | short | 1 | 93 | 91S* | 92S* | 94S* | 94S* | 4 | -2.00 | +4.42% [+2.38, +6.27] | 0.701 | 32 | no_guide |
| 3 | DELL | amc | yes | 80 | long | 4 | 79 | 78L | 86L* | 77L | 78L | 1 | +1.30 | +2.61% [+0.62, +4.55] | 0.603 | 54 | raise |
| 4 | HPQ | amc |  | 76 | short | 6 | 76 | 76S | 79S* | 84S* | 68S | 2 | -2.20 | +2.19% [+0.45, +4.05] | 0.577 | 35 | initiate |
| 5 | AMBA | amc |  | 67 | short | 12 | 66 | 62S | 56S | 62S | 87S* | 1 | -2.80 | +1.33% [+0.11, +2.96] | 0.56 | 45 | initiate |
| 6 | NTNX | amc |  | 63 | long | 14 | 63 | 66L | 74L | 40L | 72L | 0 | +2.20 | +1.05% [-0.02, +2.60] | 0.56 | 54 | maintain |
| 7 | BZ | bmo |  | 57 | long | 9 | 56 | 52L | 72L | 48L | 56L | 0 | +1.70 | +0.54% [-0.23, +2.02] | 0.56 | 55 | maintain |
| 8 | QFIN | amc |  | 54 | long | 19 | 53 | 22L | 74L | 63L | 58L | 0 | -1.20 | +0.36% [-0.31, +1.80] | 0.56 | 53 | maintain |
| 9 | YSG | bmo |  | 52 | short | 10 | 50 | 50S | 48S | 40S | 68S | 0 | -1.90 | +0.32% [-0.38, +1.59] | 0.56 | 43 | initiate |
| 10 | ADSK | amc |  | 44 | short | 8 | 42 | 56S | 42S | 36S | 40S | 0 | -1.00 | +0.29% [-0.49, +1.06] | 0.56 | 42 | raise |
| 11 | BBAR | amc |  | 42 | short | 8 | 40 | 32S | 37S | 44S | 52S | 0 | -1.10 | +0.29% [-0.51, +0.98] | 0.56 | 42 | cut |
| 12 | GDS | bmo |  | 31 | long | 25 | 29 | 62L | 8L | 4L | 48L | 0 | +1.20 | +0.29% [-0.56, +0.85] | 0.56 | 46 | maintain |
| 13 | CLSK | amc |  | 9 | long | 22 | 9 | 22S | 40L | 4L | 16L | 0 | +1.20 | +0.29% [-0.69, +0.80] | 0.56 | 42 | no_guide |
| 14 | LI | bmo |  | 9 | short | 8 | 8 | 18S | 4L | 14S | 9S | 0 | +0.10 | +0.29% [-0.69, +0.80] | 0.56 | 48 | initiate |
| 15 | DE | bmo |  | 8 | short | 26 | 8 | 26L | 34S | 33S | 8L | 0 | +0.10 | +0.29% [-0.70, +0.79] | 0.56 | 46 | initiate |
| 16 | WDAY | amc |  | 7 | short | 24 | 6 | 37S | 20L | 25S | 12L | 0 | +1.20 | +0.29% [-0.71, +0.79] | 0.56 | 47 | maintain |
| 17 | NOAH | amc |  | 6 | short | 7 | 6 | 3S | 17S | 2L | 6S | 0 | +0.80 | +0.29% [-0.72, +0.79] | 0.56 | 48 | maintain |
| 18 | GOTU | bmo |  | 4 | short | 16 | 4 | 28S | 4S | 16L | 0- | 0 | -0.50 | +0.29% [-0.74, +0.78] | 0.56 | 49 | initiate |
| 19 | DSX | bmo |  | 3 | long | 1 | 3 | 3L | 3L | 2L | 6L | 0 | +1.15 | +0.29% [-0.74, +0.78] | 0.56 | 50 | no_guide |
| 20 | GASS | bmo |  | 3 | short | 2 | 3 | 0- | 2S | 4S | 6S | 0 | -0.35 | +0.29% [-0.74, +0.78] | 0.56 | 42 | no_guide |

`*` = in that judge's own top 20%. `E[return]` is stage E-P's calibration curve (fitted 2026-10-14 on 148 resolved E-P panel names), **not** one fitted on v3b; it is what names at that percentile have earned on the panel's side, gross, scorebord window, flat at about +0.3% below 50, with a weak out-of-sample record (corr +0.12). It translates the percentile; it is not a separate forecast. Weights are research; nothing trades.

## Selected names

**PSNY** (short, panel_pct 96, E-P scale 97).
- opus5: A release postponed two days before its date 'to conclude the quarter-end closing process' on a company with going-concern language, a club loan whose minimum-revenue and cash covenants the published arithmetic cannot reach, and only $100m of the $400m Geely facility committed; every confirmed print in the record fell double digits. The MSCI micro-cap forced selling is the one part of the -43% that is non-informational.
- opus55: The company's own volume arithmetic needs a +6-17% Q4 to meet its guide, the amended covenants look out of reach, and a delayed close points to charges; the MSCI-forced 43% slide is the main offset.
- sonnet55: Volume arithmetic points to a second guide cut, covenant and funding disclosure is due, and the postponed close hints at charges; the 43% index-driven slide to $2.78 offsets only part of it.
- fable51: Rests on i1 (the amended covenants, a $3.30B 2026 revenue floor against $1.36B in H1, that the delayed close must address) and i0 (the volume-guide arithmetic needing Q4 +6-17% after Q3 +1%), with a delayed close that points to charges (i2); the MSCI-mechanical 43% slide (i3) is the offset and the reason p_up is not lower.

**NNOX** (short, panel_pct 92, E-P scale 93).
- opus5: Revenue is pre-released so there is no upside in the number; what is live is a Yorkville SEPA priced at 97% of the lowest VWAP that registers 40% of the share count and is rewarded for selling into any print-day rally, plus a vote 90 minutes before the call that doubles authorised shares and sets a 1:20-1:50 reverse split. The squeeze path from the +59.8% day is the real but smaller tail.
- opus55: The Yorkville SEPA prices off the lowest VWAP and caps any print-day rally, and the same-morning vote more than doubles issuable shares, against a pre-released quarter; the cost-cut quantification and short base are the upside tail.
- sonnet55: A going-concern Yorkville SEPA that sells into any rally plus the reverse-split and authorised-share vote at 07:00 cap the upside, with the cost plan and a 52-week-low price the only offsets.
- fable51: Rests on i0 (the Yorkville SEPA priced at 97% of the lowest three-day VWAP, which sells into any print-day rally) and i1 (the same-morning vote to more than double authorised shares); the unquantified cost plan (i4) and the 108x-volume reflex (i8) are the upside tail, so the size stays large and the certainty does not.

**DELL** (long, panel_pct 80, E-P scale 79).
- opus5: Two counterparties on the same quarter (Nvidia's enterprise/AI-cloud bucket +195%, HPE server revenue +95% with Cloud & AI margin above its own guide) against a stock down 41% in 20 days whose own estimates have risen; the live risk, sized large, is HPE being sold 16% today on the FY27 margin guide, which Dell could repeat on memory.
- opus55: Nvidia's +195% enterprise/neocloud data-center counterparty print and HPE's same-quarter server margins, into a stock down 41% whose last three beat-and-raises were bought; HPE being sold on its margin guide is the main offset.
- sonnet55: Nvidia's same-quarter AI-enterprise numbers and a 41% drawdown to half the mean target with light shorts favour a bought beat-and-raise, but HPE's 16% sale on a margin step-down and a whisper above consensus cap the lean.
- fable51: Rests on same-quarter counterparties (i0 Nvidia enterprise/AI-cloud +195%, i1 HPE server revenue +95% with margins above guide) into a stock down 41% with consensus FY EPS still rising (i7); the HPE beat-and-raise sold on the margin guide (i2) is the live risk and keeps p_up under 60.

Strongest case against: PSNY is down ~43% in nine sessions, mostly on MSCI's forced micro-cap move, and a Geely support or waiver on the call would squeeze a low-float name (short interest ~1.5% of float, so no squeeze fuel either way). NNOX's revenue and cash were pre-released, so the print itself carries little; the risk to the short is a cost-cut programme with dollar figures (the 11-10 cost-cut day ran +59.8%) or a failed share-authorisation vote. DELL is the lone long and only one judge has it in its own top 20%; HPE's same-quarter beat-and-raise fell ~16% on a margin step-down, the exact analog that hurts a long. Sources for every item are in `hunts/<T>.json`.

## Panel vs searcher, largest disagreements

- QFIN: searcher impact_sum -1.20, panel long 54 (judges weight the 2.4x-guide valuation over the sector negatives).
- GDS: searcher +1.20, panel only 31 long (Opus 5.5 and Sonnet 5.5 near zero on the DayOne/export-rule offset).
- CLSK, WDAY, DSX: searcher +1.15 to +1.20, panel <= 9 (judges net them to zero).
- AMBA: searcher -2.80 (above the 2.8 floor), panel 67 short; only Fable 5.1 has it in its top 20%.

## Comparison with stage E-P

Stage E-P's `edge-panel/edge-scores-panel.json` did not exist when this note was written (about 19:05 UTC); not waited for. The comparison is `v3b_compare.py`, pooled.

## Context: retail, search and volatility (not used for selection)

Context only; nothing ranks, selects or sizes on it. See the `retail ≥50`, `search quiet` and `vol ≥58` columns of `score_report.py`'s table (from `edge-context.json`).

## Not ranked
- URBN, ADXN: unconfirmed by the sweep (vendor-only dates; URBN likely 11-25 amc, outside the window). Shed.
- HDL, OMSE: confirmed but shed at the 20-name cap (lowest hunt_priority).

No unfinished searches (`hunt_status.py`: 0 of 20). Nothing checks a finding for being factually wrong; the double-hunt reproducibility gap is unmeasured.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

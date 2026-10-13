# Stage E-P — 2026-10-13 amc + 2026-10-14 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel, no orders.** All four
members ran on their pinned agents (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1); none
reported a model id in its output, so the pinned ids are recorded. **One day is an anecdote.**

**Headline: the panel selected nothing.** No name reached 3 of 4 members in their own top
20%. SOTK came closest (k=2, Opus 5 and Fable 5.1), then PGR (k=1, Opus 5). The searcher's
own key put no name over the 2.8 conviction floor either (largest |impact_sum| 0.97, BAC).
It is a quiet, large-cap day: eight of nine names are >$48bn and the evidence is almost
entirely peer read-through (JPM/GS/C/WFC printed 10-13) and public macro.

## The panel table

`*` = in that member's own top 20%. Weights are zero because nothing is selected.

| # | ticker | session | selected | k (in own top 20%) | sign agree | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | searcher impact_sum | expected_edge_pct | w_equal | w_tilt | control −run_up_20d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SOTK | bmo | no | 2 | 4/4 | -1.15 | -1.33* | -0.55 | -0.97 | -1.63* | -0.40 | — | 0.0 | 0.0 | -56.22 |
| 2 | PGR | bmo | no | 1 | 4/4 | -0.47 | -1.22* | -0.45 | -0.36 | -0.48 | -0.95 | — | 0.0 | 0.0 | -1.01 |
| 3 | BAC | bmo | no | 0 | 4/4 | +0.52 | +0.56 | +0.48 | +0.62 | +0.40 | +0.97 | — | 0.0 | 0.0 | +9.34 |
| 4 | MS | bmo | no | 0 | 4/4 | +0.50 | +0.89 | +0.50 | +0.50 | +0.48 | +0.45 | — | 0.0 | 0.0 | +8.92 |
| 5 | ASML | bmo | no | 0 | 4/4 | +0.47 | +0.22 | +0.61 | +0.36 | +0.58 | +0.20 | — | 0.0 | 0.0 | -6.68 |
| 6 | STT | bmo | no | 0 | 4/4 | +0.46 | +0.44 | +0.48 | +0.57 | +0.34 | +0.80 | — | 0.0 | 0.0 | +6.79 |
| 7 | FAST | bmo | no | 0 | 3/4 | -0.28 | -0.17 | +0.00 | -0.40 | -0.60 | -0.10 | — | 0.0 | 0.0 | -3.06 |
| 8 | AZZ | amc (10-13) | no | 0 | 3/4 | +0.26 | +0.33 | +0.00 | +0.40 | +0.18 | +0.40 | — | 0.0 | 0.0 | -3.76 |
| 9 | BLK | bmo | no | 0 | 2/4 | -0.03 | -0.06 | +0.08 | +0.00 | -0.35 | +0.35 | — | 0.0 | 0.0 | -1.47 |

## Selected names

None. `expected_edge_pct` therefore does not apply to any row.

The two closest:

- **SOTK (k=2, all four negative).** Every member named the same items: a 56% 20-day
  run-up to within 1.8% of the 52-week high on two press-released orders that ship in
  FY2028, against the company's own flat-to-modest FY27 guide that implies a weak H2
  (Northland cut FY27 EPS to $0.10 on 2026-09-30), and three of four confirmed prints sold.
  Strongest case against: no option market and negligible short interest, a ~$0.11bn name (Nasdaq calendar market cap)
  where an order-driven backlog headline can carry the open; the searcher
  itself expects the print to beat (+1.0% vs bar). Retail tilt 72, vol 77%.
- **PGR (k=1, all four negative).** Opus 5 sized a possible unaccrued Florida
  excess-profits catch-up (the $950M charge of September 2025, stock −5.78% that day)
  at −2.2; the others at about −0.4 to −0.6. That item is an inference, no document
  states a 2026 accrual, and Florida rate cuts argue against it. Strongest case against:
  a hurricane-free September and a likely EPS beat (`print_vs_bar_pct` +3.0).

## Where the panel and the searcher disagree most

- **SOTK**: searcher −0.40, panel −1.15 (the strongest name on the panel). The judges
  weighted the run-up/guide mismatch more than the searcher, who sized backlog +0.5.
- **BLK**: searcher +0.35, panel −0.03 (sign agreement 2/4). Fable 5.1 read the bond-rout
  AUM item harder; Opus 5 cut it as contradicted by Invesco's own AUM.
- **ASML**: searcher +0.20, panel +0.47. The judges weighted customer capex above the
  2027-bar risk.

## Against stage E

Stage E's `edge-scores.json` exists: 9 names, the same nine, none over the floor.
**Spearman ρ, stage E `impact_sum` vs `panel_score`: +0.745 (n=9)**; stage E vs this
searcher +0.427; this searcher vs the panel +0.850. Largest disagreements with stage E:
PGR (E +0.30, panel −0.47) and STT (E +0.20, panel +0.46).

## Control

`−run_up_20d_pct` ranks the day at ρ +0.60 against `panel_score` and +0.65 against the
searcher's key, so neither order is far from the free control today. It is dominated by
SOTK (−56.2).

## What the numbers are not

`expected_edge_pct` is a shrunk in-sample prior, not a forecast, and no name carries it
today. The weights are research; nothing trades them. `p_up` is recorded and decides
nothing. Below the floor the searcher's sign is a coin flip on the evidence so far (53%
over 38 events); `impact_sum` ranks and does not size. Nothing checked the findings for
factual error, and the key has not been shown reproducible to better than its own size
(twelve double-hunted pairs, median gap 2.40 points, four opposite signs). Eight of nine
names have a live option chain (SOTK none). Two judges (Opus 5, Opus 5.5) noted that
`config/panel-judge.md` asks the findings to sum to (2·p_up/100−1)·abs_move while the
shared core says the two must not be fitted; recorded, not resolved here.

## Searcher table and notes

Sign balance of the searcher's key: 6 positive, 3 negative. Flags per name are in
`edge-scores.json` (most are "findings split, sum nets opposing theses"; SOTK and PGR
carry a print/reaction sign split). V2 grounded was written at 17:31 UTC, before the
first print; it is in `edge-scores-grounded.json`.

Universe: 9 of 26 calendar rows; with `--include-unknown` 13, `session_resolve.py` killed
UNTY and confirmed none of BMRA, FNGR, NXTT, which stayed out. The sweep confirmed 9 of 9
from company sources, 0 phantoms.

## Context: retail, search and volatility (not used for selection)

Context only; nothing ranks, selects or sizes on these. Only SOTK is retail ≥50 (72) and
vol ≥58 (77%); its search series failed. Search quiet (<1.0x): STT, MS, AZZ, BLK. PGR sparse.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.

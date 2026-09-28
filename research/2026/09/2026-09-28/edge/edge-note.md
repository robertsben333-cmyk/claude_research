# Edge hunt — 2026-09-28 amc + 2026-09-29 bmo

**Answer first: no name clears the conviction floor.** All nine hunts returned sums
inside ±1 point of spot, so the day ranks but nothing on it carries a sign worth
reading. Ranking key per `edge-scores.json`: **`impact_sum`** (signed, points of spot).
Book rule `|impact_sum| ≥ 3.0` selects **zero names**, so there is no trade today.
Separately, no broker call could be made this session (see "Execution").

| # | ticker | session | pre-lessons | post-lessons (key) | V2 | floor | tradable | control −run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TRAK | amc 09-28 | +1.10 | **+0.90** | +0.41 | no | thin ($0.68m/day) | +0.72 |
| 2 | KMX | bmo 09-29 | +0.50 | **+0.40** | +0.17 | no | yes ($123m) | +7.68 |
| 3 | POCI | amc 09-28 | +0.30 | **+0.20** | −0.05 | no | no (below $200k floor, $0.19m) | −8.07 |
| 4 | IDT | amc 09-28 | +0.00 | **+0.00** | +0.00 | no | yes ($18m) | +0.25 |
| 5 | JEF | amc 09-28 | +0.00 | **+0.00** | +0.00 | no | yes ($104m) | +10.33 |
| 6 | MTN | amc 09-28 | +0.30 | **+0.00** | +0.00 | no | yes ($122m) | +3.70 |
| 7 | CCL | bmo 09-29 | −0.70 | **−0.50** | −0.39 | no | yes ($504m) | +10.16 |
| 8 | SANG | amc 09-28 | −0.90 | **−0.50** | −0.37 | no | no ($0.03m US line) | +9.36 |
| 9 | UEC | bmo 09-29 | −1.50 | **−0.90** | −0.58 | no | yes ($78m) | +26.21 |

The pre-lessons and V2 columns are measured beside the key and not traded. V2 is calibrated
today (177 ledger observations). The tradable column comes from the sealed baselines' spot × 20-day
volume. `alpaca_trade.py assets` could not be run because it contacts the broker. Borrow was
therefore not checked, and it does not matter today because no name is selected.

## What drives the top and bottom

- **TRAK +0.90.** Q4 FY26 revenue should carry about $0.73m from SPAR Group: part of a
  $2.325m one-year services contract, paid in SGRP stock, plus a $151.5k/month IT
  agreement that appears only in SPAR's 10-Q. Against a one-source $6.02m bar, the hunter
  puts print_vs_bar at +7%. Source: SPAR 10-Q
  <https://www.sec.gov/Archives/edgar/data/1004989/000143774926027494/sgrp20260630_10q.htm>
  and TRAK 8-K <https://www.sec.gov/Archives/edgar/data/50471/000143774926019434/trak20260603_8k.htm>.
  The price says the stock is −51% off its high with a persistently crowded short (~15 days
  to cover). It sold its last two growth prints (−10.5%, −8.8%) and bought a miss.
- **KMX +0.40.** CarMax's own ABS servicer reports through August show no new
  deterioration in the Tier 1 book. The 2025-3 trust tracks 2024-3 at the same age:
  <https://www.sec.gov/Archives/edgar/data/2074530/000207453026000047/a2025-3ex991091526.htm>.
  A soft revenue comparison offsets faster wholesale depreciation. The price says +5.27 vol
  points of put skew, and six of the last eight prints fell.
- **UEC −0.90.** Q3's opex run-rate ($40.8m, mineral spend nearly doubled) puts Q4 near
  −$0.06 before marks against a −$0.04 bar:
  <https://www.sec.gov/Archives/edgar/data/1334933/000143774926019889/R4.htm>. Revenue
  depends on a discretionary inventory sale that management passed on at higher prices in
  Q3. The price says −26% in 20 days, calls bid (skew −10.7) and ~14% short (undated).
  Both findings run against positioning.
- **CCL −0.50 / SANG −0.50.** CCL: the Q4 guide will be struck at ~$106 spot Brent, below
  the Street's Q4 cut. That is offset by a likely small Q3 beat of its own guide. SANG: an
  inferred year-end goodwill impairment (60% of its size is `one_off`) plus post-guide
  freight costs.

## Names that could not be ranked

None: 9 of 9 were rankable. All nine were confirmed from company sources by the sweep, and none
was a phantom. The 23 `time-not-supplied` rows were checked with `session_resolve.py`: 1 was
killed by EDGAR, 0 were confirmed by press release, and 22 were left out on the 20/20 phantom
base rate.

## Critical read of the floor-clearers

There are none. The largest conviction is 0.90 (TRAK, UEC), under a third of the floor.
Nothing is recommended. Even TRAK, the top row, would be *not recommended*: it rests on a
one-source bar and on related-party revenue paid in OTC stock, and it is thin (limited-liquidity
warning at $0.68m/day).

## What the table does not say

- **Order is not sign.** Below the floor the sign has been a coin flip (53% over 38
  events). Above it, rank of conviction predicted sign-correctness at ρ=+0.514. Every row
  today is below the floor, so no row here is a bullish or bearish view.
- **`impact_sum` is not a forecast of the move.** It ranks and does not size, and findings
  from one document can be counted twice.
- **Control.** `−run_up_20d_pct` orders the day almost the reverse of the hunt: Spearman
  **−0.67** between the two. UEC is the control's top long (+26.2) and the hunt's bottom
  name. Over the resolved sample the hunt has not been shown to beat this free control,
  and on the larger 105-event sample the control itself returned −0.42% per trade.
- **Sign balance:** 3 positive, 3 zero, 3 negative. For once there is no negative lean.
- **Nothing checked the findings.** There is no adversary and no second hunter, so a
  factually wrong finding enters at full size.
- **Reproducibility.** When the stage double-hunted, paired hunters differed by a median
  2.40 points, and 4 of 12 pairs had opposite signs. Every gap in today's table is smaller
  than that.
- **Baseline measured versus inferred.** 6 of 9 names have a live option chain (JEF, MTN,
  IDT, CCL, KMX, UEC). TRAK, SANG and POCI take the run-up fallback lean and a historical
  median. The sweep flagged TRAK's and SANG's baseline histories as untrustworthy. TRAK's
  rows are off by one session; SANG's are 6-K noise.
- **Capacity.** Two names (POCI, SANG) are below the $200k turnover floor and one (TRAK)
  is thin, and TRAK is the top of the ranking. The bottom (UEC, CCL, SANG) is mostly
  liquid.
- **One day is an anecdote.** Nine names cannot produce a meaningful rank correlation. The
  pooled `edge_resolve.py` figure is the result.

## Execution

`execution.enabled` is true, but this session's permission classifier refused every
`alpaca_trade.py` broker call as a real-world transaction. That covered `verify --fix
--submit` and even read-only `status`. Step 0b therefore did not run. The repo's order records show
no leg due today (last book 09-22, exits dated 09-23), but the broker state was not read.
Step 7 would have selected zero names in any case.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.

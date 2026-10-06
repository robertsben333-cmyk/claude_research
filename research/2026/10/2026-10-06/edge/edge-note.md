# Edge hunt — 2026-10-06 amc (window: 10-06 amc + 10-07 bmo)

**Answer first.** Six names, all reporting after today's close; all six confirmed by company sources, zero phantoms. Ranked on `impact_sum` (the file's `ranking_key`). **PENG is the only name at the conviction floor (+2.80, exactly 2.8)**; nothing clears the book's `impact_scaled` floor of 1.76 (PENG +1.60), so **no book would have been placed even with execution reachable**. One day of six names is an anecdote.

| # | ticker | session | pre-lessons | post-lessons (key) | scaled | V2 | floor | tradable | control (−run_up_20d) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PENG | amc 10-06 | +4.00 | **+2.80** | +1.60 | +4.25 | yes | yes — $95.4m/day, ok | −15.96 |
| 2 | NEOG | amc 10-06 | +2.20 | **+1.50** | +0.78 | +1.45 | – | yes — $56.6m/day, ok | −2.61 |
| 3 | SAR | amc 10-06 | +0.50 | **+0.40** | −0.50 | +0.15 | – | yes long; short = elsewhere (not lendable at Alpaca) — $2.2m/day | +8.31 |
| 4 | STZ | amc 10-06 | +0.50 | **+0.20** | +0.31 | +0.17 | – | yes — $253.7m/day, ok | +4.35 |
| 5 | AXIL | amc 10-06 | −0.40 | **−0.10** | −0.32 | +0.34 | – | no — $0.08m/day, below floor | +0.81 |
| 6 | WS | amc 10-06 | −2.00 | **−1.50** | −0.96 | −1.03 | – | yes — $12.9m/day, Alpaca borrow yes | −10.26 |

Pre-lessons, scaled and V2 are measured beside the key, not traded. V2 is calibrated today (180 ledger observations at `session_close`). Borrow was asked live at 17:2x UTC.

## What drives the top and bottom

**PENG +2.80.** The largest finding (+1.5, reported quarter) is that June–August memory peers ran hot. Micron reported $54.23B against its own $50B guide, and ADATA posted record months. Penguin's Q4 guide assumed less memory-pricing help than in Q3. Source for the guide: the company's Q3 prepared remarks (https://s204.q4cdn.com/917347554/files/doc_financials/2026/q3/PENG-Q3-FY26-Earnings-Call-Prepared-Remarks-for-posting.pdf). Micron: https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000018/a2026q4ex991-pressrelease.htm. The second finding (+1.0, guidance) is that the FY27 guide may come in above the company's preliminary "~30%". **What the price already says:** the option skew is −21.8 vol points (calls bid), and the stock is up 16% over 20 days. The market leans the same way, so the hunt agrees with the price rather than contradicting it.

**WS −1.50.** The company's own pro forma (8-K/A Ex. 99.2, https://www.sec.gov/Archives/edgar/data/1968487/000119312526356964/d417231dex992.htm) shows the Kloeckner deal is heavily EPS-dilutive: combined 9M FY26 diluted EPS $0.56 against $1.30 standalone. This is the first full quarter carrying it, against an aggregator EPS bar ($0.92–1.16) that looks legacy-only. Kloeckner's German H1 report adds a cut to its Americas outlook (−0.5). **What the price says:** the stock is +10% over 5 and 20 sessions into the print, there is no usable chain, and short interest is 3.5% of float (not crowded).

## Names that could not be ranked

None. All six are rankable. ARTW (time-not-supplied, $0.02bn) was checked with `session_resolve.py`, came back unresolved with only a cadence prior, and was not hunted.

## Critical read of the floor-clearer

**PENG.**
- **Which line does it land on?** +1.5 on the reported quarter and +1.0 on guidance. Guidance is the line that has paid. The quarter finding is a peer proxy (Micron, ADATA), not company data.
- **Do the hunter's two numbers agree?** Yes in sign: `print_vs_bar_pct` +4.0 and `expected_move_pct` +1.6. The reaction is under half the +2.8 sum. The hunter says the gap is the priced-in lean (calls bid, +16% run-up).
- **Bar and positioning.** The quarter bar is sourced but the two sources disagree on EPS ($0.77 vs $0.61). The FY27 sell-side bar is unsourced, so the guidance finding is capped. Short interest is 12–19.5% of float, partly convert-arb hedging after the July $650M zero-coupon convertible.
- **Liquidity.** Not thin.
- **Flags.** None.
- **Verdict.** *Recommended with a named reservation.* The size is mostly a peer proxy that the options market already leans toward. It sits exactly on the floor, and the book's own key (`impact_scaled` +1.60) does not select it.

## What the note must also say

- **Order vs sign.** Below the floor the sign is a coin flip on the evidence so far (53% over 38 events). Above it, the rank of conviction predicted sign-correctness at ρ=+0.514. NEOG +1.5 and WS −1.5 are not directional views.
- **`impact_sum` is not a forecast of the move.** It ranks; it does not size, and the same fact in two findings is counted twice.
- **The control.** The −run_up_20d ranking is SAR, STZ, AXIL, NEOG, WS, PENG: nearly the hunt's order reversed (Spearman about −0.20 between the two on six names). Over the six resolved runs the hunt has not been shown to beat this free control, and on the larger 105-event sample the control itself returns −0.42% per trade.
- **Sign balance.** 4 names lean positive and 2 negative.
- **Nothing checked the findings.** There is no adversary pass and no second hunter. A factually wrong finding enters the key at full size.
- **Reproducibility.** Paired hunts had a median gap of 2.40 points, and 4 of 12 pairs had opposite signs. PENG's +2.80 sitting exactly on the 2.8 floor is well inside that noise.
- **Measured vs inferred baseline.** 3 of 6 names have a live option chain (STZ, PENG, NEOG). WS, SAR and AXIL take the historical-median fallback; WS's chain exists but is unusable.
- **Cost to trade.** 5 of 6 clear the $200k turnover floor. AXIL ($80k/day) cannot be traded. The top of the ranking (PENG) is liquid. The bottom (WS) is shortable at Alpaca. SAR's short side would need IBKR borrow.
- **Session changes.** NEOG and AXIL switched to amc from a bmo history. NEOG also holds an Investor Day at 09:00 ET on 10-07, inside the window, which is why its abs_move is 13%.
- **Hunter versions.** These are `us.v9` hunters on claude-opus-5-5. Every hunt returned `pre_lessons` and `print_vs_bar_pct`.

## Context: retail, search and volatility (not used for selection)

These labels are context only. Nothing ranks, selects or trades on them.

- PENG: retail 61 (≥50), search sparse, vol 74% (≥58)
- NEOG: retail 62 (≥50), search 1.19x (not quiet), vol 53%
- SAR: retail 42, search sparse, vol 21%
- STZ: retail 24, search 1.15x (not quiet), vol 19%
- AXIL: retail 59 (≥50), search sparse, vol 44%
- WS: retail 40, search sparse, vol 41%

## Execution

`execution.enabled` is true. Step 0b (`verify --fix --submit`) was refused by the session's auto-mode permission classifier, the 7th run in a row since 09-28. Nothing was sold from this session. Step 7: `plan` selected **0 names** (best was PENG at 1.60 < 1.76 on `impact_scaled`), so no order was owed and none was sent.

---
This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

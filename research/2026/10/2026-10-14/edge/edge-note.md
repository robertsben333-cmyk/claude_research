# Edge hunt — 2026-10-14 amc + 2026-10-15 bmo

**Answer first: no name clears the conviction floor, so there is no book today.** 17 names were in the window, the sweep confirmed 17 of 17 (0 phantom rows), and 17 hunters ran (one per name). `edge-scores.json` names its ranking key as **`impact_sum`**. The largest is BNY at +1.85 against a floor of 2.8. The book selects on `impact_scaled` at 1.76, and the largest there is CMTL at −1.50. This is a near-null day: the hunters found mostly sector and peer proxies inside company guides, and no company-level number the market lacks.

## Ranked table

| # | ticker | session | pre-lessons | **post-lessons (key)** | scaled | V2 | floor | tradable | control −run_up_20d |
|---|---|---|---|---|---|---|---|---|---|
| 1 | BNY | bmo 10-15 | +2.10 | **+1.85** | +0.56 | +0.57 | no | yes (long, $549m/d, ok) | +11.27 |
| 2 | PLD | bmo 10-15 | +1.60 | **+1.55** | +0.91 | +0.56 | no | yes (long, $497m/d, ok) | +0.76 |
| 3 | SCHW | bmo 10-15 | +1.50 | **+1.00** | +0.40 | +0.58 | no | yes (long, $770m/d, ok) | +9.07 |
| 4 | EDUC | amc 10-14 | +1.30 | **+0.80** | −0.45 | +0.09 | no | **no** ($0.03m/d, below floor) | −1.15 |
| 5 | MAN | bmo 10-15 | +1.00 | **+0.60** | +0.74 | +0.35 | no | yes (long, $44m/d, ok) | +11.56 |
| 6 | PNC | bmo 10-15 | +0.40 | **+0.40** | +0.25 | +0.16 | no | yes (long, $425m/d, ok) | +7.57 |
| 7 | MRSH | bmo 10-15 | +0.50 | **+0.30** | +0.16 | +0.06 | no | yes (long, $526m/d, ok) | −0.84 |
| 8 | HOMB | amc 10-14 | +0.30 | **+0.20** | +0.11 | +0.13 | no | yes (long, $42m/d, ok) | +5.21 |
| 9 | WIT | bmo 10-15 | +0.00 | **+0.10** | −0.21 | +0.23 | no | yes long; short **elsewhere** (not lendable at Alpaca, check IBKR) | −6.55 |
| 10 | BSVN | bmo 10-15 | −0.10 | **+0.00** | −0.06 | +0.05 | no | yes ($2.6m/d, ok, borrow yes) | −1.20 |
| 11 | USB | bmo 10-15 | −0.10 | **−0.10** | −0.11 | −0.07 | no | yes (short, borrow yes, $439m/d) | +6.24 |
| 12 | EQBK | amc 10-14 | −0.20 | **−0.20** | −0.09 | −0.04 | no | yes (short, borrow yes, $5.4m/d) | +5.55 |
| 13 | ERIC | bmo 10-15 | +0.40 | **−0.20** | +0.00 | −0.47 | no | yes ($80m/d, ok) | +3.64 |
| 14 | FHN | bmo 10-15 | −0.50 | **−0.40** | −0.30 | −0.06 | no | yes (short, borrow yes, $125m/d) | +5.95 |
| 15 | TSM | bmo 10-15 | −0.10 | **−0.40** | −0.18 | −0.31 | no | yes (short, borrow yes, $4.1bn/d) | −3.41 |
| 16 | CMC | bmo 10-15 | −0.50 | **−0.60** | −0.55 | −0.66 | no | yes (short, borrow yes, $73m/d) | +1.88 |
| 17 | CMTL | amc 10-14 | −1.00 | **−0.70** | −1.50 | −0.91 | no | yes but **thin** ($0.34m/d, borrow yes) | +14.77 |

Pre-lessons, scaled and V2 are measured beside the key, not traded. V2 is calibrated today (186 ledger observations at `session_close`). All sessions were confirmed from company sources by the sweep. SCHW's date is company-implied (the "Fall Business Update" pattern), and WIT's comes from aggregator coverage of its exchange filing.

## What drives the top and the bottom

- **BNY +1.85.** The main finding is a peer read-through (+0.8). State Street printed today (2026-10-14) with NII flat on the quarter (about $864M against $860M) and raised its FY NII and fee guidance, while BNY consensus assumes NII about −3% on the quarter. BNY's own FY NII guide implies $1.36–1.39bn a quarter for H2, below consensus of about $1.40bn (+0.6), so a guide raise is plausible. Price: −11.3% over 20 days and −3.6% today in sympathy with STT; skew +2.1 (downside paid) on a wide chain. Sources: STT's Q3 release via the hunter's file; BNY Q2 materials. See `hunts/BNY.json`.
- **PLD +1.55.** One finding carries the name (+1.2, guidance). H1 Core FFO ex-promote was $3.12, and the FY guide of $6.22–6.30 implies $1.55–1.59 a quarter for H2. That sits below the Q2 run rate of $1.60 while occupancy is rising, so a third raise is plausible. Source: https://ir.prologis.com/news-events/press-releases/detail/1044/prologis-reports-second-quarter-2026-results. The stock rose on all 7 prior prints, so the market already expects a raise.
- **CMTL −0.70 (scaled −1.50).** The fiscal year-end print should present the Gilat S&S sale as held-for-sale or discontinued, against a consolidated consensus near $109M (−0.6). Allerium's book-to-bill was 0.32x with no award releases since March (−0.6). An August 8-K waiver plus prepayment helps liquidity (+0.4, https://www.sec.gov/Archives/edgar/data/23197/000002319726000084/cmtl-20260730.htm). Thin at $0.34m a day, −14.8% over 20 days, and no usable chain.
- **CMC −0.60.** Korean rebar imports kept rising against management's June view (−1.0, guidance), and Fastmarkets expects October scrap up about 6.6% (−0.5). Against that, the steel spread supports the quarter (+0.3). The hunter's two numbers disagree in sign: print +2.0% vs the bar, stock −0.6%.

## Names that could not be ranked

None. All 17 are rankable. EDUC is rankable but untradable, with turnover of $26k a day.

## How to read this table

- **The order and the sign are separate questions.** Below the floor the sign has been a coin flip on the evidence so far (53% over 38 events). Above it, the rank of conviction predicted sign-correctness at ρ=+0.514. Every name today is below the floor. Do not read FHN at −0.40 as a bearish view.
- **`impact_sum` is not a forecast of the move.** It double-counts facts that appear in two findings. It ranks; it does not size.
- **Free control.** −run_up_20d ranks today's names at Spearman **ρ=+0.10 against the key**, so the hunt's order is nearly orthogonal to it. Over the early six resolved runs the control ranked at ρ=0.335 against the hunt's raw 0.407. On the larger 105-event sample the control loses money. The stage has not been shown to beat it.
- **Sign balance.** 9 positive, 1 zero, 7 negative: no pessimism skew today.
- **Nothing checked the findings.** There is no adversary pass and no second hunter, so a factually wrong finding enters the key at full size. Two specific soft spots:
  - Several hunters cite an FOMC hike on 2026-09-16. HOMB and BSVN cite the Fed's own page; FHN says it rests on secondary calendars.
  - Several bars are single-source: CMTL, HOMB, BSVN and EDUC have none, and TSM's Q4 gross-margin bar comes from Yuanta alone.
- **The key is not reproducible to better than its own size.** In the double-hunt era, twelve paired names had a median gap of 2.40 points, and four of the twelve came back with opposite signs. Every |impact_sum| today is under 2.
- **How much of the baseline was measured.** 10 of 17 names had a live option chain (BNY, PLD, SCHW, MAN, PNC, MRSH, USB, ERIC, TSM, CMC). The other 7 fall back to a historical median, and the sweep marked 4 histories untrustworthy (TSM, ERIC, WIT, SCHW). Their hunters were told to discard them.
- **What trading the day would have cost.** 15 of 17 clear $1m a day; EDUC is below the floor and CMTL is thin. The bottom of the ranking (CMTL) is thin, while the top (BNY, PLD) is liquid. Every short except WIT is lendable at Alpaca on this snapshot. None of this matters today because nothing clears the floor.
- **One day is an anecdote.** Seventeen names cannot produce a meaningful rank correlation. The pooled figure is the result.

## Critical read of the floor-clearers

There are none. The nearest candidates are BNY on the key and CMTL on scaled. The hunter itself calls BNY's case a peer proxy plus guide arithmetic, which is partly priced. CMTL's scaled −1.50 is mostly its size (abs_move 15) times a mild p_up of 45, on a thin name. Neither would be recommended on today's evidence.

## Context: retail, search and volatility (not used for selection)

These labels are context only. Nothing ranks, selects or trades on them.

- Retail tilt ≥ 50: EDUC (51), CMTL (79). All other names are below 50.
- Search quiet (<1.0x on 2026-10-13): EDUC (0.98x), ERIC (0.85x). PLD, MRSH, WIT and FHN are not quiet. BNY, SCHW, PNC, HOMB and EQBK failed to fetch; MAN, BSVN, USB, TSM, CMC and CMTL are sparse.
- Vol ≥ 58%: none. CMTL is highest at 56.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

# Edge hunt — 2026-09-25 amc + 2026-09-28 bmo

**Answer first: nothing to trade today. No name clears the conviction floor of 3.0, and the largest score is GNS at −1.30.** All five ranked names print on Monday 2026-09-28 before the open. Four of the five trade below the $200k/day turnover floor. The hunters found nearly nothing the price does not already hold, and the table reflects that.

Ranking key (from `edge-scores.json`): `impact_sum`, signed, in points of spot.

| # | ticker | session | pre-lessons | post-lessons (key) | V2 | floor | tradable | control (−run_up_20d) |
|---|---|---|---|---|---|---|---|---|
| 1 | KNDI | bmo 2026-09-28 | +1.50 | **+0.50** | +0.41 | – | no: $0.05m/day, below floor | +6.25 |
| 2 | ADXN | bmo 2026-09-28 | +0.50 | **+0.00** | +0.00 | – | no: $0.13m/day, below floor | +4.94 |
| 3 | NTWK | bmo 2026-09-28 | +0.50 | **+0.00** | +0.00 | – | no: $0.14m/day, below floor | −23.20 |
| 4 | MITQ | bmo 2026-09-28 | −1.50 | **−0.10** | −0.40 | – | no: $0.10m/day, below floor | −6.28 |
| 5 | GNS | bmo 2026-09-28 | −2.00 | **−1.30** | −1.25 | – | elsewhere: $0.55m/day, thin; Alpaca will not lend it, check IBKR | +20.51 |

The pre-lessons and V2 columns are measured beside the key and are not traded. V2 is calibrated today: 177 ledger observations at `session_close`.

## What drives the top and bottom

- **KNDI (+0.50), the top name.** FY2025 20-F Note 22 shows the H2-2025 loss drivers were accrued in full: the $33.0M Coleman judgment plus fees and $6.93M of retroactive anti-dumping exposure. It also shows the NGCL guarantee settled on 2026-01-09 and about $28M of pledged deposits released in Feb–Mar 2026. So H1 2026 is unlikely to repeat roughly $59M of charges. Source: https://www.sec.gov/Archives/edgar/data/1720250/000121390026048312/R29.htm. On price, the stock is +15% over five days off its 52-week low, and the only options chain is unusable, so there is no skew. Flag: the bar is unsourced (no analyst coverage and no company guide). A −2.0 Nasdaq bid-price item (compliance deadline 2026-11-02) sits outside the window and is kept out of the key.
- **GNS (−1.30), the bottom name.** The hunter finds that GNS's two formal prints (auditor-reviewed H1 2025, audited FY2025) fell 5.6% and 5.0% on their first session, while its four unaudited management-number releases each rose 5–12%. Monday's print is the formal, reviewed kind. Price rows: https://finance.yahoo.com/quote/GNS/history/?period1=1757980800&period2=1759536000. A second finding, −0.3, is that H1 revenue of about $6.5M is only 30–32% of the $20–22M FY guide. On price, the stock is at its 52-week low, −20.5% over 20 days, with short interest at 5.0% of float. The sample is two observations, and the IFRS line may be a profit on AI-treasury marks this time.

## Names not ranked

- **IVA**, the only amc row, was not hunted. The sweep found no company source for a 2026-09-25 amc print. The IR page has no date and the last 6-K is dated 09-03. The only support is Nasdaq's calendar. Last year's H1 went out on a Monday before the open, and French rules require the report by 30 September. It sits in the table as `not ranked: no hunt`.
- **The 16 `time-not-supplied` rows.** This was a thin day, so they were checked with `session_resolve.py`: EDGAR killed ENLV outright and no press release confirmed any row. The sweep then tested all of them against company sources. CHRN, GRFS, AIV, AIAI and PBM are phantoms with the period already filed or not yet due. The other eleven have no company date. None was hunted.

## Critical read of the floor-clearers

None. No name clears 3.0. Three rows are worth a word anyway:

- MITQ's hunter expects the number and the stock to go opposite ways: print +10% against the company's own $5.3M guide, stock −0.1%. On the true release days, the last three guide beats moved −0.3%, −1.9% and +4.3%. Last year's Q4 print fell 25.4% on the next-quarter guide.
- NTWK and ADXN came back as honest zeros with no finding standing. NTWK's only draft finding said Q4 would land at the reaffirmed guide; it was dropped because that sits inside the guided range and the last "record quarter, guide reaffirmed" print sold off 6.5%.
- **Not recommended, any of them.** They are below the floor, so the sign has meant nothing on the pooled sample. Four of the five cannot be traded at the turnover floor anyway.

## Standing caveats

- **The order is not the sign.** Below the floor the sign has been a coin flip: 53% over 38 events. Above the floor, the rank of conviction predicted sign-correctness at ρ=+0.514, or about +0.36 once rebuilt from a single hunter. Every row today is below the floor. Do not read GNS −1.30 as a bearish view. `impact_sum` ranks names and does not forecast the size of the move.
- **Control.** Ordering by `−run_up_20d_pct` gives GNS, KNDI, ADXN, MITQ, NTWK. The hunt puts GNS at the opposite end (last against first), and NTWK is last on both. On the larger pooled sample the control has stopped working (−0.42% per trade over 105 events). The stage has still not been shown to beat a free control cleanly.
- **Sign balance:** 1 positive (KNDI), 2 negative (MITQ, GNS), 2 zero.
- **Lessons control:** every hunter shrank its draft after reading `LESSONS.md`. The absolute sum fell from 6.0 to 1.9 across the five names. Direction was unchanged on every name, and ADXN and NTWK went to zero.
- **Nothing checked the findings.** There was no adversary pass and no second hunter.
- **The key is not reproducible to better than its own size.** Twelve double-hunted pairs had a median gap of 2.40 points, and four of the twelve had opposite signs.
- **Measured versus inferred baseline:** 0 of 6 names had a usable option chain. IVA, KNDI and NTWK have unusable chains; GNS, MITQ and ADXN have no options market. Every `priced_lean_pct` is the run-up fallback, and every "expected move" is a historical median. Four of the six baselines carry `cadence_implausible` or too few prints, so their reaction histories are 6-K artefacts. The hunters rebuilt them from confirmed releases.
- **Capacity:** one name of five ranked (GNS, $0.55m/day and thin) clears the turnover floor, and Alpaca will not lend it. Both extremes of today's ranking are effectively untradeable. This is a research result, not a signal.
- **One day is an anecdote.** Five names cannot produce a meaningful rank correlation.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

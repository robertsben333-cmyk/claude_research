# Edge hunt — 2026-10-12 amc + 2026-10-13 bmo

**Answer first: nothing clears either floor today, so there's no book.** All nine names report before the open on 2026-10-13. The hunts found little that isn't already priced. Five big banks plus UNH and JNJ were pre-guided at mid-quarter conferences, and every hunter reported mostly that. The largest key is DPZ at −2.10, below the 2.8 floor. The largest scaled value is DPZ at −0.78, below the 1.76 floor the book selects on. Ranking key (`edge-scores.json` `ranking_key`): `impact_sum`.

| # | ticker | session | pre-lessons | **post-lessons (key)** | scaled | V2 | floor | tradable | control −run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | UNH | bmo 10-13 | +2.00 | **+1.00** | +0.84 | +0.40 | no | yes, $1.85bn/day, ok | +1.97 |
| 2 | GS | bmo 10-13 | +1.40 | **+0.90** | +0.43 | +0.34 | no | yes, $1.97bn/day, ok | +9.79 |
| 3 | C | bmo 10-13 | +0.70 | **+0.50** | +0.24 | +0.22 | no | yes, $1.24bn/day, ok | +3.64 |
| 4 | JPM | bmo 10-13 | +0.60 | **+0.50** | +0.20 | +0.21 | no | yes, $2.78bn/day, ok | +4.54 |
| 5 | WFC | bmo 10-13 | +0.30 | **+0.05** | +0.00 | +0.01 | no | yes, $1.19bn/day, ok | +5.77 |
| 6 | FBK | bmo 10-13 | −0.50 | **−0.30** | −0.06 | −0.04 | no | yes, $34.6m/day, ok, Alpaca lends | +3.03 |
| 7 | JNJ | bmo 10-13 | −0.30 | **−0.30** | −0.21 | −0.08 | no | yes, $1.76bn/day, ok, Alpaca lends | +1.16 |
| 8 | ACI | bmo 10-13 | −1.40 | **−0.50** | −0.48 | −0.55 | no | yes, $94.4m/day, ok, Alpaca lends | +3.18 |
| 9 | DPZ | bmo 10-13 | −2.30 | **−2.10** | −0.78 | −1.30 | no | yes, $240m/day, ok, Alpaca lends | +3.25 |

The pre-lessons, scaled and V2 columns are measured beside the key and are not traded. Since 2026-10-02 the book selects on `impact_scaled` at 1.76. V2 is calibrated on 186 shadow-ledger observations.

## What drives the extremes

- **DPZ −2.10 (bottom).** The FY26 "low single digit" US comp guide was held on 2026-07-20 even though H1 was +0.9% and +0.1%. Q3 laps +5.2%. This is new CEO Joe Jordan's first print, which is a natural moment to reset the guide (−1.5). Source: https://www.tradingview.com/news/marketbeat:86ccc8664094b:0-domino-s-pizza-q2-earnings-call-highlights/. Placer.ai QSR visits were negative in August and September, and Domino's Pizza Enterprises (DMP) on the ASX was −5.8%. What the price already says: put skew +4.75 is paying for downside, and the stock is +5.4% over five days. The US-comp consensus could not be sourced, so the hunter capped sizes.
- **UNH +1.00 (top).** The July guide's arithmetic implies an H2 medical cost ratio (MCR) near 90.9%, no better than H2 2025, while H1 2026 ran about 180bp better year on year. UNH has raised guidance at every 2026 print. Source: https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000191/earningsrelease2q26_7152.htm. What the price already says: the street's FY EPS (~$19.84) already sits in the upper half of the $19.50–20.00 guide. Call skew is −3.93, which already pays for upside. The last two raises closed only +1.2% and +0.5%. A −0.5 finding on 2027 Medicare Advantage star ratings (CMS, 2026-10-08) offsets part of it.
- **GS +0.90.** Strength in equities (Solomon on 2026-09-16; Jefferies posted record equities) is set against a bar that was cut after the 2026-09-16 guide. Consensus is disputed across providers ($12.90 to $16.26), so every size is capped.

## Names that could not be ranked

None: 9 of 9 are rankable. Six `time-not-supplied` rows (UNTY, FNGR, RMCF, NCPL, BMRA, MSS) were checked with `session_resolve.py` and none was confirmed by press release. They were not hunted.

## What the note must also say

- **The order is not the sign.** No name clears the 2.8 conviction floor. Below the floor the sign is a coin flip on the evidence so far: 53% over 38 events. Above it, rank of conviction predicted sign-correctness at ρ=+0.514. None of today's numbers should be read as a directional view. `impact_sum` is not a forecast of the move; it ranks and does not size, and findings that rest on one document can double-count.
- **Control.** −run_up_20d ranks GS, WFC, JPM, C, DPZ, ACI, FBK, UNH, JNJ. The hunt's order agrees with it only weakly, at Spearman +0.28 across the 9 names. The stage has not yet beaten this free control on the pooled sample, and one day of nine names is an anecdote.
- **Sign balance.** 5 names lean positive and 4 lean negative. Every bank but FBK leans slightly positive. All six bank names print within one day of each other, so they are one correlated sector bet: rates, the Fed hike of 2026-09-16, and the 10-year near 5%. The scorer cannot see that.
- **Nothing checked the findings.** There is no adversary and no second hunter, so a factually wrong finding enters at full size.
- **Reproducibility.** When the stage was double-hunted, paired hunters differed by a median 2.40 points, and 4 of 12 pairs had opposite signs. Every gap in today's table between UNH and ACI is smaller than that.
- **Baseline.** All 9 names have an option chain marked `ok`. FBK's is unusable in substance: open interest is 33 and the spread is 66% of mid. Its 12% "implied move" is not a market price. So 8 of 9 baselines are measured and 1 is effectively inferred.
- **Capacity.** Every name clears the $200k turnover floor and none is thin; FBK is the smallest at $34.6m/day. The extremes are tradable; they are just not strong.
- **Lessons control.** LESSONS.md shrank every sum toward zero: UNH 2.0→1.0, ACI −1.4→−0.5, GS 1.4→0.9. The ordering is mostly unchanged.

## Context: retail, search and volatility (not used for selection)

These are context only; nothing ranks, selects or trades on them. Retail tilt is below 50 for all 9; ACI is highest at 47. 20-day realised volatility is below 58% for all 9; ACI is highest at 30%. The Google Trends search spike failed for every name, so "search quiet" reads n/a.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

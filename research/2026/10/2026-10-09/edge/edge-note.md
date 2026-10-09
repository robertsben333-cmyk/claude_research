# Edge hunt — 2026-10-09 amc + 2026-10-12 bmo

**Three names ranked, none near the floor, no book.** Ranking key is `impact_sum`, as `edge-scores.json` names it. Every name was hunted on the operator's instruction (17:30 UTC), after the sweep had confirmed none of them. That instruction is recorded in `sweep.json` as `operator_override`.

## Ranked table

| # | ticker | session | pre-lessons | post-lessons (key) | scaled | V2 | floor | tradable | control (−run_up_20d) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | HIFS | amc 10-09 (date doubtful) | −0.50 | **−0.10** | −0.18 | −0.15 | no | not checked (broker calls denied) | see baseline |
| 2 | GLDG | amc 10-09 | −0.70 | **−0.30** | −0.10 | −0.25 | no | not checked | see baseline |
| 3 | RMCF | bmo 10-12 (likely amc 10-12 or later) | −0.40 | **−0.50** | −0.52 | −0.54 | no | not checked | see baseline |

- **What trades on what:** the pre-lessons, scaled and V2 columns are measured beside the key. None of them is traded on.
- **Floors:** `impact_sum` has a 2.8 floor and the book selects on `impact_scaled` at 1.76. The largest name today is 0.50 on the key and 0.52 scaled, so nothing is near either floor and no book was placed.
- **Tradable column:** it could not be filled. The `assets` broker lookup was refused by the auto-mode classifier. All five names are thin microcaps.

## What drives each name

- **RMCF (−0.50):**
  - The revised franchise agreements are cutting royalties: Q1 FY27 royalties were $1.232m against $1.655m a year earlier, and units fell from 253 to 250.
  - Transition and strategic-review costs point to a wider loss. Source: the Q1 FY27 release, https://www.sec.gov/Archives/edgar/data/0001616262/000121390026078026/ea029805101ex99-1.htm.
  - Partly offset by the sale-leaseback paying down the breached-covenant notes, and by strategic-review optionality.
  - There is no consensus at all. The stock is up 20% over 5 days on the sale-leaseback 8-K.
  - The release probably lands after the close on 10-12 or later (last year: 2025-10-13 at 16:05). If so, there is no print inside this window.
- **GLDG (−0.30):**
  - The likely disclosure of ATM dilution at depressed prices to fund the Q3 drilling. Source: the Q2 6-K, https://www.sec.gov/Archives/edgar/data/0001538847/000143774926023556/ex_985515.htm.
  - A markdown of its listed holdings, which goes through OCI and is already quoted daily.
  - The Q2 release moved the stock 0.0%.
- **HIFS (−0.10):** the drivers offset.
  - Negative: a near-flat equity book halves GAAP EPS from Q2's $11.49, and the Fed hike of 2026-09-17 bears on a wholesale-funded margin.
  - Positive: a record core EPS of about $5.1–5.4 once Q2's one-offs drop out, and 16.6% of float short into a possible clean credit table.
  - **The date is doubtful.** Every 2026 release came on the third Friday after quarter end, which points to 2026-10-16.

## Not ranked

- **NCPL:** the hunter found no event. The auditor resigned on 2026-08-12, four years of accounts have been withdrawn, and no filing date has been given (8-K 2026-09-25).
- **MSS:** the hunter found no event. The 10-K is overdue with the audit unfinished, the Nasdaq plan deadline is 2026-10-19, and nothing has been announced.

## Caveats

- **Sign balance:** all three ranked hunts lean negative (3 of 3).
- **The day is noise:** every rankable name is below the conviction floor, and below the floor the sign has been a coin flip (53% over 38 events). Above it, conviction rank predicted whether the sign was right at ρ=+0.514. Today none of these signs means anything.
- **Not a forecast:** `impact_sum` ranks the names; it does not forecast the size of the move.
- **Nothing checked the findings:** there is no adversary pass and no second hunter.
- **Key noise:** the key is not reproducible to better than its own size. When names were double-hunted, the median gap was 2.40 points and 4 of 12 pairs had opposite signs.
- **No measured baseline:** none of the five names has an option chain, so every baseline is a historical fallback.
- **Free control:** the stage has still not beaten −run_up_20d_pct. One day of three names is an anecdote.
- **Dates and sessions are unconfirmed:** at least two of the three ranked names may print outside the window (HIFS on 10-16, RMCF after the close on 10-12). The resolver will then measure a window with no print in it.

## Context: retail, search and volatility (not used for selection)

These labels are context only. Nothing ranks, selects, sizes or trades on them.

| ticker | retail ≥50 | search quiet | vol ≥58 |
| --- | --- | --- | --- |
| HIFS | no (40) | n/a (sparse) | no (25) |
| GLDG | yes (56) | n/a (sparse) | no (37) |
| RMCF | yes (80) | no (1.17x) | no (57) |

## Execution

- **Execution is enabled** (paper account, `exit_mode: amc_open`).
- **Broker calls were denied by the auto-mode classifier.** The account was flat at 10:15 UTC.
- **No name met the benchmark**, so 0 orders were placed and gross exposure is 0%.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

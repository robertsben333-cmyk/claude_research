# Edge hunt — 2026-10-09 amc + 2026-10-12 bmo

**No names could be ranked today.** No company-confirmed earnings event falls inside the window, so no hunters ran and nothing was bought. The ranking key named in `edge-scores.json` is `impact_sum`; no name has a value for it.

## Ranked table

There are no ranked rows. All five calendar rows are listed below with the reason each could not be ranked.

| ticker | calendar date | session | why not ranked | control (−run_up_20d) |
| --- | --- | --- | --- | --- |
| HIFS | 2026-10-09 | ? | **Unconfirmed.** Hingham never pre-announces its dates and has not released Q3. Its 2026 releases came on the third Friday after quarter end, which points to 2026-10-16, outside this window; a StockTwits listing also says 10-16. If it does post at 16:01 ET today, that release is in the window as an amc print. It files with the FDIC, so EDGAR cannot test it. | see baseline |
| GLDG | 2026-10-09 | ? | **Not an earnings event.** It files interim 6-Ks with no release and no call. Same verdict as the 2026-10-08 sweep. | see baseline |
| RMCF | 2026-10-12 | ? | **Unconfirmed.** It always pre-announces its calls and has not announced one. Last year's pattern points to an amc release on 10-12, which is outside the window. | see baseline |
| NCPL | 2026-10-12 | ? | **Phantom.** NT 10-K filed, 10-K still unfiled, a non-reliance 8-K (Item 4.02) and Nasdaq delinquency notices. | see baseline |
| MSS | 2026-10-12 | ? | **Phantom.** NT 10-K and NT 10-Q filed, Nasdaq delinquency notices, and no results since 2025-03-18. | see baseline |

Source URLs for each verdict are in `sweep.json`.

## How the window was checked

- `edge_universe.py --window` returned 0 of 7 calendar rows with a confirmed session.
- Because the day was thin, the five `time-not-supplied` rows went through `session_resolve.py`. It carried 4 rows as unresolved and dropped HIFS for `no_cik`. HIFS was added back by hand because it is an FDIC filer.
- Baselines were sealed provisionally and committed before any agent launched. None of the five names has an option chain.
- One `edge-sweep` agent confirmed none of the five: 2 phantoms and 3 unconfirmed.

## What this day says

- Phantom rate on today's `time-not-supplied` rows: at least 2 of 5, and 0 of 5 confirmed.
- A day with no confirmed names is a real answer. It is not a failed run.
- One day is an anecdote, and the stage has still not been shown to beat the free control (−run_up_20d_pct). Today adds nothing to either question.
- V2 (`edge-scores-grounded.json`) was written but grounds nothing: there is no hunt to ground.

## Execution

- **Execution is enabled** (paper account, `exit_mode: amc_open`).
- **Step 0b did not run.** The auto-mode classifier denied every broker call (`verify`, `status`) for the third day running, even in the exact form of the allow rule. Nothing was held: Close AMC at 10:15 UTC found the account flat, and 2026-10-08 placed no book.
- **No book was planned or placed.** With no rankable name, no name meets the benchmark.

This is research, not financial advice. Earnings reactions are highly uncertain and can be driven by market positioning, guidance, macro conditions, and management commentary rather than reported results alone.

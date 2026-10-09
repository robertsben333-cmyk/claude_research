# Stage E-P — 2026-10-09 amc + 2026-10-12 bmo

**This is stage E-P: Opus 5.5 searchers and a blind four-model panel. It places no orders.**
All four judges ran on their pinned models (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1), with no fallback.
One day is an anecdote, and this one is three names that probably do not print in the window.

**Read this first: the three ranked names are ranked on an operator override.** No company
announced a date, the sweep confirmed none of the five calendar rows, and every searcher set
`event_confirmed: false`. On the operator's instruction ("a quick search confirms GLDG has
earnings amc today; be less critical and run it") the override was applied to GLDG, HIFS and
RMCF. Each of those hunts carries `event_confirmed_override`, and the searcher's own verdict is
kept in `event_confirmed_searcher`. NCPL and MSS were not overridden: both are documented
delinquent filers with no filing date, and NCPL has no auditor (resigned effective 2026-08-12).
If the prints do not land in the window, the resolver should treat these rows as non-events
(`event_occurred: false`).

## Panel

| # | ticker | session | selected | consensus_k | sign agree | panel_score | opus5 z | opus55 z | sonnet55 z | fable51 z | searcher impact_sum | expected_edge_pct | weight |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RMCF | bmo 10-12 (likely amc, see below) | no | 0 | 4/4 | −0.39 | −0.59 | −0.19 | −0.56 | −0.21 | −0.50 | — | — |
| 2 | GLDG | amc 10-09 (unconfirmed) | no | 0 | 3/4 | −0.09 | +0.00 | −0.07 | −0.19 | −0.11 | −0.20 | — | — |
| 3 | HIFS | amc 10-09 (unconfirmed) | no | 0 | 1/4 | +0.00 | +0.00 | +0.03 | +0.00 | −0.04 | +0.00 | — | — |

No judge put any name in its own top 20%, so nothing is selected and no weights apply. Every
judge's sizes are small because every judge weighted for the print probably falling outside the
sealed window. RMCF is the only name where all four lean the same way (negative): the Q1 FY27
10-Q shows a structural 26% royalty cut and G&A up 28%, going-concern language and a breached
covenant (5.3x against a 2.0x maximum), and the stock ran up 18% on the Durango sale-leaseback
([10-Q](https://www.sec.gov/Archives/edgar/data/1616262/000119312526303159/rmcf-20260531.htm)).
**The case against:** RMCF prints after the close (Q2 FY26 came 2025-10-13 at 4:05 PM EDT,
[release](https://ir.rmcf.com/news-events/press-releases/detail/301/rocky-mountain-chocolate-factory-reports-second-quarter)),
so a 10-12 print is outside the 10-12 bmo window. The board's strategic review gives the
distribution an upside tail.

**Where the panel and the searcher disagree:** they don't. All four judges and the searcher
order the three the same way.

**Against stage E:** stage E ranked the same three names (HIFS −0.10, GLDG −0.30, RMCF −0.50).
Spearman ρ between stage E's `impact_sum` and `panel_score` is **1.0 on n=3**. With three names,
a rank correlation of 1.0 comes up one time in six, so this means nothing.

## Searcher table

Ranked on `impact_sum`. 0 of 3 clear the 2.8 floor. The `impact_scaled` values are −0.65, −0.04
and +0.00. V2 grounded (written before the first print) is −0.30, −0.50 and −0.10 for RMCF,
GLDG and HIFS. All of these sit far below any floor, so below the floor the sign is a coin flip.

## Not ranked

- **NCPL:** no event. Its auditor resigned and FY2022–25 financials were declared non-reliable
  ([8-K](https://www.sec.gov/Archives/edgar/data/1414767/000149315226038853/form8-k.htm)).
- **MSS:** no event. The 10-K and 10-Q are both delinquent with no date given
  ([notice](https://finviz.com/news/396554/maison-solutions-inc-receives-additional-nasdaq-notification-regarding-delayed-filing-of-quarterly-report-on-form-10-q)).

## Standing caveats

- Nothing checked the searchers' findings for factual errors.
- The key is not reproducible to better than its own size (the double hunt measured a median
  gap of 2.40 points, with opposite signs on 4 of 12).
- No name has an option chain, so every baseline is inferred, not priced.
- All five names are micro caps; RMCF trades about $100k a day.
- `expected_edge_pct` is a shrunk in-sample prior and not a forecast. Nothing trades the weights.
- `p_up` is recorded and decides nothing.

## Context: retail, search and volatility (not used for selection)

See `edge-context.json`. These labels are context only.

This is research, not financial advice. Earnings reactions are highly uncertain
and can be driven by market positioning, guidance, macro conditions, and
management commentary rather than reported results alone.

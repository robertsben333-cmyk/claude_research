# Stage E-P — 2026-11-27 amc + 2026-11-30 bmo

**This is stage E-P: Opus 5.5 searchers, a blind four-model panel.** It normally trades the panel's book on the live and paper Alpaca accounts at step 6b. **Today it cannot.** The day after Thanksgiving is a US half day: the market closed at 13:00 ET, before this run fired at 13:07 ET. `open` refuses a closed market, so no book was placed today. What happened is in the run log and in `alpaca-orders*.json`.

All four judges ran on their pinned models: Opus 5, Opus 5.5, Sonnet 5.5 and Fable 5.1. No fallback was used. **One day is an anecdote, and this is a three-name day.**

**The window was thin because of the holiday.**
- **Confirmed sessions:** the calendar gave 4 names with a session: CHA, HMR, BOSC and PWRL, all 11-30 bmo.
- **Unknown-session rows:** 19 rows had `time-not-supplied`. `session_resolve.py` killed 2 and carried 17.
- **Sweep:** of the 23 rows, the sweep confirmed 3 on company sources:
  - HMR, 11-30 bmo, from the company release.
  - BOSC, 11-30 bmo, from the company release.
  - NAT, 11-30 bmo. The company letter dates Q3 to Monday 11-30, so the calendar's 11-27 was wrong.
- **Dropped:** CHA had no company date, so it was not confirmed. PWRL is a monthly-NAV fund. Seven rows were phantoms.
- **Hunting:** 3 searchers, none shed, all three searches complete.

All three prints come Monday 11-30 before the open. The window runs from Friday's half-day close to Monday's close. Any position in these names would have had to be entered before 13:00 ET today, before this run had a single searcher out.

## The panel

| rank | ticker | session | selected (mean ≥ 80) | panel_pct | side | sd | opus5 | opus55 | sonnet55 | fable51 | consensus_k | panel_score | searcher impact_sum | E[return] (80% band) | p_right | weight_equal | weight_precision_tilt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | HMR | bmo 11-30 | **yes** | 98 | short | 1 | 98 S* | 96 S* | 100 S* | 100 S* | 4 | -2.85 | -6.10 | +4.99% [+3.13, +6.66] | 0.73 | 1.00 | 0.89 |
| 2 | BOSC | bmo 11-30 | **yes** | 83 | long | 3 | 78 L | 84 L* | 87 L* | 82 L* | 4 | +1.29 | +2.00 | +3.03% [+0.98, +5.01] | 0.63 | 1.00 | 1.11 |
| 3 | NAT | bmo 11-30 | no | 18 | long | 8 | 12 L | 31 L | 15 L | 12 L | 0 | +0.23 | -0.20 | +0.29% [-0.62, +0.82] | 0.56 | 0 | 0 |

How to read the table:
- **Member columns:** each is that judge's own percentile against its last 200 live sizes, 0–100. L or S gives the side, and `*` marks a judge's own top 20%.
- **E[return]:** what names at that percentile have earned on the panel's side. It is one number per percentile, gross, measured on the scorebord window, and flat at about +0.3% below a percentile of 50. It translates the percentile; it is not a separate forecast.
- **Weights:** research only. No order is sized on them today.

**HMR short (98) and BOSC long (83) clear the mean-percentile rule, with all four judges present.**
- **Book rule (`execution.panel`):** weight is `panel_pct` − 60, so 38 / 23, with a 50% cap per name. That gives about HMR 50% short and BOSC 50% long.
- **Liquidity:** both names are THIN, under $1m a day. HMR trades $0.31m/day and BOSC $0.26m/day, so either would carry a limited-liquidity warning.
- **Not placed:** none of this was placed, because the market was shut.

## HMR: short, 98, all four judges in their own top 20%

**The case rests on price, not on a company number.**
- **The run-up:** HMR rose 57% in three sessions into the print, from 0.93 on 11-23 to 1.46 on the 11-27 half-day close. The searcher found no 6-K, no EDGAR filing since 09-09, and no news behind it (https://stockanalysis.com/stocks/hmr/history/). The half day traded about 583k shares, roughly 10% of a 6.04m-share float.
- **Past prints:** all three 2026 prints were sold on release: Q4 2025 −5.1%, Q1 2026 −20.4% after a +29% run-in, and Q2 2026 −10.8% despite a revenue beat. The searcher rebuilt these from Yahoo daily bars.
- **Supply:** a registered $20m B. Riley equity facility with 11.08m shares for resale (https://www.sec.gov/Archives/edgar/data/2029471/000091957426003772/p12151143_pos-am.htm) gives the company a way to sell into the spike.
- **Positioning:** short interest is about 0.3% of float, so nothing cushions a fall.
- **Opus 5's extras:** it also weighted that the run came while mid-size tanker spot halved in November. It readmitted a Clarksons record-Q3 item the searcher had rejected as unfetchable.

**The strongest case against.**
- **Mildly good quarter:** the $0.04 EPS bar and a stale $21.5–22.5m revenue consensus sit well below Q2's actual $29m.
- **Strong Q4 read:** peers' Q4 bookings are at extremes (Teekay Suezmax $272k/day, DHT VLCC $509k/day), and Heidmar earns commissions on Suezmax and Aframax pools.
- **Thin sources:**
  - The baseline carried no reaction history: the 6-K archive went unread with `SEC_USER_AGENT` unset.
  - The EPS bar was seen in search snippets only.
- **Tradability:** at 152% realised volatility on $0.31m/day, a short this size is hard to hold and borrow can move.
- **What decides it:** the size rests on a pattern — the run-up and how past prints were received — not on a document.

## BOSC: long, 83, three of four judges in their own top 20%

**The case is the company's own arithmetic.**
- **The release:** on 2026-11-17, with Q3 already closed, BOS restated that full-year 2026 revenue and net income will exceed 2025 ($50.6m and $3.6m). It reported a record $35m backlog: about $11m due in Q4 and about $24m in 2027 (https://www.stocktitan.net/news/BOSC/bos-reports-record-backlog-of-35-million-up-45-from-year-end-3zp2zf7fbb3g.html).
- **What it implies:** a net-income floor that needs more than $1.5m in H2 points to Q3 EPS of roughly $0.08–0.11. Against that, three analysts sit at $0.06 and have not revised since 11-07.
- **Small additions:**
  - The shekel weakened about 2.9% in Q3 (a proxy).
  - The backlog timing gives visibility into 2027.

**The strongest case against.**
- **A floor, not a constraint:** "exceed 2025" is a floor. Consensus Q3 plus a roughly $1.1m Q4 is internally consistent with it, so the arithmetic is suggestive, not binding.
- **Flat guides get sold:** this holder base sold flat guides twice in 2026 (−10.2% and −9.7%). The print will reiterate rather than raise.
- **The thinnest judge:** Opus 5 put it at its 78th percentile, just outside its top 20%.
- **Liquidity:** turnover is about $0.26m a day.

## Where panel and searcher disagree

- **NAT:** the searcher's −0.20 is a non-result, and all four judges filed it as a small long, at percentiles 12–31. Neither view is a call. The disagreement is over which way the dividend step-down and the $144k/day Q4 fixtures net. Opus 5 readmitted a vice-chairman purchase and the ~8%-of-float short base, both of which cushion the negatives.
- **HMR:** the searcher, at −6.10, is the largest it wrote today. The judges sized it smaller in raw terms (−3.0 to −5.1) but at the very top of each of their own ranges. On rank they agree.

## Stage E

Stage E wrote no `edge/` today; its Routine has been stopped since 2026-10-19. There is no overlap and no Spearman ρ.

## Searcher table and context

| ticker | impact_sum | pre-lessons | impact_scaled | V2 | floor 2.8 | tradable | -run_up_20d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOSC | +2.00 | +1.80 | +1.05 | +1.50 | - | yes (long), thin, $0.26m/day | -1.1 |
| NAT | -0.20 | -0.10 | +0.00 | -0.03 | - | yes, $27.6m/day, borrow ok | +20.5 |
| HMR | -6.10 | -6.40 | -4.50 | -17.20 | yes | yes (short), thin, $0.31m/day, borrow ok | +18.0 |

The pre-lessons, scaled and V2 columns are measured beside the key, not traded. V2 was written before the first print (calibrated on 184 ledger observations).

**Signs:**
- **Searchers:** one hunt leaned positive (BOSC), one negative (HMR) and one flat (NAT).
- **Judges:** they leaned long on BOSC and NAT and short on HMR.
- **Control:** the free control (−20-day run-up) points long on HMR and NAT, the opposite of the panel on HMR. HMR's 20-day run-up is −18%, but its 5-day is +44.6%, and the 5-day move is the one the case rests on.

**Option chains:** none of the three names has a usable one. NAT's chain is indicative only, with the ATM spread at 60% of mid. So every expected move here is a historical or searcher estimate, not a priced one.

### Context: retail, search and volatility (not used for selection)

These labels are context only. Nothing selects or sizes on them.
- **BOSC:** retail 72.6, so ≥50 yes. 20-day volatility 46.4%. Search data too sparse to read.
- **NAT:** retail 71.2, yes. Volatility 48.3%. Search spike 0.95x, quiet.
- **HMR:** retail 75.6, yes. Volatility 151.8%, so ≥58 yes. The search query failed.

## What the numbers are not

- **`expected_return_pct`:** this is what names at that percentile have earned. Out of sample it has a weak record, correlating +0.12 with the realised return over 148 names. It is not a forecast to size on.
- **`p_up`:** recorded, and it decides nothing.
- **No fact-checking:** nothing checked the findings, so a factually wrong finding enters at full size.
- **Reproducibility:** the key is not reproducible to better than its own size.
- **Baseline histories:** these are empty for all three. `SEC_USER_AGENT` is unset in this environment, so www.sec.gov answered 403 to the scripts. The searchers rebuilt the histories from daily bars.

This is a forecasting exercise over public information. It is not investment advice.

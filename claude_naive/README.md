# claude_naive

Arm A of the `backtest/` study, promoted to a live daily Routine.

## Why this one

Three research strategies were run over the same sealed, point-in-time corpus of 37
earnings events (`backtest/RESULTS.md`):

| | direction | return/trade (open) | return/trade (close) | magnitude error |
| --- | --- | --- | --- | --- |
| **A naive** | **72%** | **+0.90%** | +2.16% | 3.35pp |
| B plan-first | 71% | +0.45% | +2.24% | 3.09pp |
| C skill (production stage 2) | 55% | −1.16% | +0.11% | 3.09pp |

Floors on the same events: a free rule that repeats last quarter's reaction sign scored
**62%**; `always_down` returned **+0.25%** per trade; the base-rate proxy forecast
magnitude with **3.64pp** median error.

Arm A was given **no research method at all** — just the corpus and the instruction to
decide for itself what mattered. Arm C, which is the production `earnings-deep-dive`
skill with its nine research areas and calibration rules, came last on direction and lost
money.

## What is actually established, and what is not

**Established, or close to it:** all three arms beat the base-rate proxy on *magnitude*
(rank correlation 0.29–0.33 against 0.131), and each put 4 of the 8 biggest movers in its
own top 8 against a null of 1.7. Size is the answerable question.

**A lead, not a finding:** the direction ranking. 18 directional calls behind arm A's
72%, against a coin interval of 32–68%. The sample also skewed down, 18 of 40 up.

**Known bias:** all three arms under-scaled the large moves. Seven of the eight biggest
were forecast under, several by half — AAP moved 24.6% against 8.5–11.0 forecast, PWR
17.3% against 7.0–7.5. The live skill therefore emits **two** magnitude numbers, raw and
corrected, and `score_naive.py` scores both. If the correction is an artefact of 37
events, the ledger will show it.

## The transfer risk, stated plainly

The backtest ran arm A over a **sealed corpus** — SEC filings, date-fenced news,
StockTwits, and price anchors computed from bars. This Routine runs it over the **live
web**. The 72% does not transfer automatically, and the biggest reason is anchors: during
the study, rebuilding the base-rate table from EDGAR periodic reports *flipped a
directional call* on PWR (`backtest/FINDINGS.md` §31). Live anchors come from search and
will be noisier than the ones that produced the result.

There is also no fence live. The corpus could not contain post-print information; the web
can. Forecasts record the URLs actually used so this is at least auditable.

## Schedule

**19:30 CET, weekdays.** Thirty minutes before the 20:00 CET (14:00 ET) entry the
backtest priced, so the forecast always exists before the trade it describes.

## Layout

```
claude_naive/
  <YYYY-MM-DD>/
    forecasts.json      one object per ticker, the skill's output
    entry-prices.json   spot at forecast time, frozen
    scored.json         after the outcome exists
  LEDGER.md             rolling, every rate beside its floor
  scripts/
    entry_snapshot.py   freeze spot at forecast time
    score_naive.py      score against the realised move, append to the ledger
```

## Scoring

```bash
python3 claude_naive/scripts/score_naive.py --date 2026-09-07
```

Joins each forecast to the realised move under the backtest's own trading scheme, scores
both magnitude numbers, and appends a dated block to `LEDGER.md` with the floors beside
every rate.

## This is research, not advice

A forecasting exercise over public information. Not investment advice, and not to be
presented as such.

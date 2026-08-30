---
name: earnings-naive-forecast
description: Live daily forecast of tonight's earnings movers using the naive method that won the pilot-40 backtest. No research methodology is prescribed - the model decides for itself what matters. Fires at 19:30 CET, thirty minutes before the 20:00 CET entry the backtest priced. Use when asked to run the naive forecast, run claude_naive, or forecast tonight's earnings.
---

# Naive earnings forecast — live

This is **arm A** from `backtest/RESULTS.md`, promoted to production because it beat the
other two on a 37-event backtest: 72% direction, +0.90% per trade at the open exit,
+2.16% at the close, against a 62% free-rule floor and an `always_down` baseline of
+0.25%.

It won by being given **no method at all**. That is the whole point of it and the one
thing not to "improve".

## What makes this different from stage 2

The existing `earnings-deep-dive` skill is arm C in that backtest. It scored **55%** on
direction, traded most often, and lost money. Its instructions are exhaustive — nine
research areas, a source hierarchy, calibration rules. Arm A had none of that and did
better.

So: **do not port the nine-area structure into this skill.** If it starts to look like
stage 2, it has stopped being the thing that was tested.

## Read this before trusting the number

The backtest ran arm A over a **sealed, point-in-time corpus** — SEC filings, date-fenced
news, StockTwits, and price anchors computed from bars. This skill runs it over the
**live web**. That is a different information environment, and the 72% does not transfer
automatically. Two specific risks:

- **Anchor quality.** The backtest fed the model a clean base-rate table built from EDGAR
  periodic reports. Rebuilding those anchors *flipped a directional call* on PWR mid-study
  (`FINDINGS.md` §31). Live anchors come from search and will be noisier. This is probably
  the single biggest threat to the result reproducing.
- **No fence.** The corpus could not contain post-print information. The live web can and
  will — a stray article about a peer that already reported, a preview updated after the
  fact. There is nothing to stop it, so the honest response is to record what was read.

## 1. Timing

Fires **19:30 CET**, thirty minutes before the 20:00 CET (14:00 ET) entry the backtest
priced. That is deliberate: the forecast has to exist before the trade it describes.

For an `amc` name the print lands roughly two hours after the entry. For a `bmo` name
tomorrow, the entry is tonight and the print is tomorrow morning.

## 2. Build the universe

```bash
python3 scripts/get_earnings.py --out claude_naive/$(date -u +%Y-%m-%d)
```

Take names reporting **after today's US close or before tomorrow's open**. Cap at
**eight** names, highest market cap first. Record any you dropped.

If the universe script fails or returns nothing, say so in the run log and stop. Do not
invent a universe.

## 3. Forecast each name

For each ticker, research it however you see fit and produce a call. **No method is
prescribed. Decide for yourself what matters.**

That instruction is load-bearing. Resist the urge to work through a checklist. The arm
that used a checklist came third.

Two things the backtest showed are worth knowing, and they are observations rather than
instructions:

- **Size is the answerable question.** All three arms beat the base-rate proxy on
  magnitude (rho 0.29–0.33 against 0.131) while direction stayed near the floor.
- **The arms under-scaled the big moves badly** — seven of the eight largest were
  forecast under, several by half. AAP moved 24.6% against 8.5–11.0 forecast; PWR 17.3%
  against 7.0–7.5.

So emit **two** magnitude numbers: your honest estimate, and a corrected one. The
correction exists to be tested, not because it is known to work live.

**Abstain freely.** Arm A called Neutral on 19 of 37 and that is *why* it made money —
selective +0.90% per trade against −0.30% forced to trade everything. A Neutral is a
result, not a failure to produce one.

## 4. Output

Write `claude_naive/<YYYY-MM-DD>/forecasts.json` — a JSON array, one object per ticker:

```json
{
  "ticker": "TICK",
  "company": "...",
  "session": "amc",
  "event_date": "2026-09-07",
  "call": "Strong Up | Lean Up | Neutral / No Edge | Lean Down | Strong Down",
  "direction_score": 0,
  "prob_up": 50,
  "expected_abs_move_pct": 0.0,
  "expected_abs_move_pct_scaled": 0.0,
  "certainty": "High | Med | Low",
  "evidence_quality": 0,
  "key_drivers": ["at most five, most important first"],
  "what_would_change_my_mind": "one sentence",
  "sources": ["urls you actually used"],
  "reasoning": "at most 200 words"
}
```

`expected_abs_move_pct` is your honest estimate. `expected_abs_move_pct_scaled` applies
the backtest's correction: **1.0x below 5%, 1.6x from 5–10%, 2.0x above 10%.** Both get
scored, so we find out whether the correction generalises or was an artefact of 37 events.

Also write `claude_naive/<YYYY-MM-DD>/entry-prices.json` with the spot price and timestamp
for each name at the time you ran, so the trade can be reconstructed:

```bash
python3 claude_naive/scripts/entry_snapshot.py --date <YYYY-MM-DD>
```

## 5. Log and publish

```bash
python3 scripts/run_log.py --heading "claude_naive — <YYYY-MM-DD>" \
  --line "Universe: <n> qualified, <k> forecast" \
  --line "Calls: <up> up, <down> down, <neutral> neutral" \
  --line "Dropped: <tickers or none>"
scripts/publish.sh "claude_naive: forecasts for <YYYY-MM-DD>"
```

**Publish or it never happened.** These sessions are ephemeral.

## 6. The morning after

`claude_naive/scripts/score_naive.py` joins each forecast to the realised move under the
backtest's own trading scheme — buy 14:00 ET the last session before the print, exit next
open and next close — and appends to `claude_naive/LEDGER.md`.

```bash
python3 claude_naive/scripts/score_naive.py --date <YYYY-MM-DD>
```

Every rate is reported beside its floor. A hit rate alone is the mistake the main
`LEDGER.md` already made.

## This is research, not advice

A forecasting exercise over public information. Not investment advice. The backtest it
rests on had 17–22 directional calls per arm and its own author called the direction
result "a lead, not a finding".

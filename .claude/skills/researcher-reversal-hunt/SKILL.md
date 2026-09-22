---
name: researcher-reversal-hunt
description: The unpriced-information hunt, turned around and pointed at yesterday's biggest US losers. Seals what is already known about each fall, sends one hunter per name to work out what caused it and whether the reaction overshot, and sums their signed finding sizes into one number per company so the day's fallers can be ranked. Research only, no orders. Use when asked to run the reversal researcher, run stage R, rank yesterday's biggest losers, or work out whether a stock that fell will bounce or keep falling.
---

# Stage R — the reversal researcher

One signed number per company, so the names that fell hardest yesterday can be
**ranked** against each other. No call, no threshold, no direction label. Identical
output contract to stages E, J, EU and AU, and the identical scorer, which is the
point: a Japanese print and an American faller are then scored the same way and their
resolved numbers can be compared.

**This stage places no orders and reads no broker.** There is no `alpaca_trade.py` step
and there must not be one. Phase 0 says why in one line: at the horizon this stage
predicts, the gross edge is smaller than the estimated spread.

## The question is not the earnings question, and the difference decides everything

| | stage E (earnings) | stage R (reversal) |
| --- | --- | --- |
| The event | scheduled, binary, **not yet public** | already happened and already public |
| What the hunt looks for | a fact the market has not seen | whether the market's reaction to a fact it HAS seen is wrong |
| The anchor | option-implied move + 25d skew + prior prints | the fall decomposed, the volume, this name's own comparable falls, a chain where one exists |
| The window | close before the print → close after | close of the drop day → close of the next session |
| The free control | `-run_up_20d_pct`, ρ=0.335 on six days | **`atr14`, ρ=−0.126 on 749 sessions, family-wise p=0.0017** |
| Phantom events | 20 of 20 on one `time-not-supplied` day | none. The fall is observed |
| Hindsight risk | low: the outcome does not exist yet | **high: the outcome of the first move IS the input** |

That last row is the one to keep in mind all day. Stage E's hunters worked before the
outcome existed. Here the fall is handed to the hunter, and a model asked whether a 25%
fall was overdone will produce a fluent, confident rationalisation every time. The
defences are the `pre_lessons` freeze, the requirement that every finding name what
resolves it and by when, and the fact that the ranking is **within the day** — being
right that things which fall keep falling earns nothing, because every name in the day
fell.

## What phase 0 established, before any agent existed

`researcher_reversal/analysis/phase0-base-rates.json`, built by `rev_harvest.py` and
`rev_backtest.py` over **11,235 falls on 749 sessions**. Read
`researcher_reversal/README.md` for the whole table; the four lines that change how
you run the day:

1. **They continue, they do not rebound.** Median next session −1.00%, and the median
   is negative in every cut. At 21 sessions, −11.11% median and 34% of names up.
2. **Deeper falls continue harder.** Below −40% the next session averages −4.00%.
   Ranking by the size of the fall has the *wrong* sign for a rebound thesis.
3. **Volume separates the day.** Over 15× normal volume → −2.44% next session; under
   2× → +1.46%. It is the cheapest read on whether the fall carried information.
4. **One session is not tradeable.** Gross ±0.35% a day against a round-trip spread of
   about 1.06 points. The drift that survives cost is at ten and twenty-one sessions,
   on the short side, and it is not what this stage predicts.

So the note must never present a positive number as "the market over-reacted, expect a
bounce" without saying what it is fighting.

## Steps

Resolve paths with `python3 scripts/run_paths.py --json`. Re-read the clock with
`date -u`; do not trust the date you were told at startup. `<RUN>` below is
`research/<YYYY>/<MM>/<DATE>/reversal/`, where `<DATE>` is the **drop date**, the last
completed US session.

**0. Heartbeat, before you spend anything.**

```bash
python3 scripts/run_log.py --heading "Stage R — reversal researcher — STARTED" --line "<the plan>"
scripts/publish.sh "stage R: started for <YYYY-MM-DD>"
```

One cheap commit, and the only thing that distinguishes a Routine that never fired from
a session killed on its first subagent.

**1. Universe.** The worst fallers of the last completed session.

```bash
python3 researcher_reversal/scripts/rev_universe.py --k 15 -o <RUN>/universe.json
```

Read `counts` and `market_concentration` before going on. A day where one sector is more
than half the names is **one bet, not fifteen**, and the note has to say so — a sector
selling off is the most ordinary way for fifteen names to fall at once, and it is a
correlated exposure the scorer cannot see.

**2. Seal a baseline for every hunted name, before any hunter is spawned.**

```bash
mkdir -p <RUN>/baselines <RUN>/hunts
for T in $(python3 -c "import json,sys;print(' '.join(r['ticker'] for r in json.load(open('<RUN>/universe.json'))['hunted']))"); do
  python3 researcher_reversal/scripts/rev_priced_in.py --ticker "$T" --date <DROP_DATE> -o <RUN>/baselines/$T.json
done
```

Sealed means sealed: a baseline written after a hunter has run is not a baseline, it is
a summary of the hunt. If a name's baseline comes back `no_bars` or
`too_little_history`, drop the name and record it in the run log rather than hunting it
blind.

**3. One hunter per name, in parallel, with the `reversal-hunter` agent.**

Give each hunter its ticker, the drop date, the next session's date, the path to its
sealed baseline, and the output path `<RUN>/hunts/<TICKER>.json`. Nothing else — no
view of yours, no other name's findings, no sight of the sweep's opinion.

`cap` in `config/pipeline.yaml` equals K for a reason recorded there: choosing which of
the fifteen to hunt would be a second selection nothing downstream can see.

**4. Score, with the shared scorer, unchanged.**

```bash
python3 researcher_us/scripts/edge_score.py --run <RUN>
```

It is the US stage's script and it is not copied, forked or wrapped. It reads
`<RUN>/baselines/*.json` and `<RUN>/hunts/*.json`, and the reversal baseline supplies
`anchor_quality`, `priced_lean_pct`, `history.n` and `event_plausibility.verdict`, which
are the four keys it reads. Output is `<RUN>/edge-scores.json`, ranked on `impact_sum`.

**5. Resolve the PREVIOUS run, which is now scoreable.**

```bash
python3 researcher_reversal/scripts/rev_resolve.py --run <YESTERDAY'S RUN> -o <RUN>/../resolve.json
```

Read `lean_vs_free_control_rho` first. Near 1.0 means the baseline's lean IS the free
control and nothing built on it can beat the control; that is the stage J failure mode
and it would be a defect, not a result. Then read the hunt's ρ against
`neg_atr14` and `neg_ret_d`. **A run that does not beat the free controls has
established nothing**, and the note says so in those words.

**6. The note.** `<RUN>/reversal-note.md`. Answer first, then the table, then the
critical read.

It must carry, in this order:

- the day, the number of names, the sector concentration, and the day's SPY move
- the ranked table: ticker, fall, `impact_sum`, conviction, `priced_lean_pct`, the free
  controls, turnover, estimated half-spread, and the cause label the hunter returned
- for each name above the conviction floor, two sentences: what caused the fall, and
  what the hunt thinks the reaction got wrong
- **the base rate it is arguing against**, explicitly, for every positive number: the
  median faller does −1.00% the next session and this name's band does <x>
- what the day's ranking would cost to trade: the sum of the estimated half-spreads
  against the spread of the predictions. On most days this is the sentence that matters
- the disclaimer from `config/pipeline.yaml`

**7. Publish.**

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage R: reversal hunt for <YYYY-MM-DD>"
```

## Rules specific to this stage

**Never present a rebound thesis without its base rate.** Positive numbers here are
fighting 11,235 measured events. That does not make them wrong; it makes them
expensive, and the note has to price them.

**The cause classification is the hypothesis, and it is pre-registered.** Mechanical
falls revert, informational falls drift. It is written into
`config/pipeline.yaml:reversal_hunt.pre_registered_hypothesis` so it cannot be rewritten
after the answer arrives. `rev_resolve.py` reports `by_cause` and ranks
`mechanical_vs_informational` as its own column **whether or not it looks good**.

**Do not move a floor, a weight or a horizon on one day's result.** The repo has paid
for that lesson four times. A rule that changes with the data is not a hypothesis.

**No orders, ever.** If a future session finds an execution step in this stage, that is
a defect to remove, not a feature to configure.

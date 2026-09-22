---
name: researcher-reversal-hunt
description: The unpriced-information hunt, turned around and pointed at yesterday's biggest US losers. Seals what is already known and already scheduled for each fallen name, then sends one hunter per name to answer two questions about the very short term - did the fall misprice what is already known, and does anything land inside the window that the price does not hold - and sums their signed finding sizes into one number per company so the day's fallers can be ranked. Research only, no orders. Use when asked to run the reversal researcher, run stage R, rank yesterday's biggest losers, or work out whether a stock that fell has a second shoe coming.
---

# Stage R — the reversal researcher

One signed number per company, so the names that fell hardest yesterday can be
**ranked** against each other. No call, no threshold, no direction label. Identical
output contract to stages E, J, EU and AU, and the identical scorer, which is the
point: a Japanese print and an American faller are then scored the same way and their
resolved numbers can be compared.

## The question, in two legs, both bounded to one short window

**Leg 1 — repricing.** Did the fall misprice what is already known?
**Leg 2 — new information.** Does anything land inside the window that the price does not
hold, bad or good?

The window is the drop-day close to the next session's close, and it bounds both legs.
Nothing outside it counts, however real.

This is the third version and the first two were each half of it. **v1 asked only about
the overshoot**, which on its own is unfalsifiable inside a day: a mispricing with no
mechanism can sit there for months, and the fall is the hunter's own input, so a model
handed a 25% drop will argue either side fluently. **v2 asked only what comes next**,
which is checkable but throws away the case the stage was built for — a fall that was
simply too big.

**The short-horizon bound is what makes leg 1 answerable.** An overshoot earns nothing
unless it *corrects* inside the window, so a `repricing` finding must carry
`mechanism_in_window`: the named thing that closes the gap before the next close. A wider
overnight audience reading the primary document, a seller that is finished and dated, a
note landing before the open, a disclosed buyer, a checkable error in the wire copy, a
countable and spent supply. Without a mechanism it is an opinion, and the brief tells the
hunter to drop it or file it in `outside_window`.

Every finding carries `leg`. The shared scorer sums them into the one ranked number, and
`rev_resolve.py` ranks the two legs **separately** — which leg carries the result is the
most useful thing this stage can learn in its first month, and pooling them makes it
unanswerable.

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

The baseline's `forward` block is the point of this stage: `rev_forward.py` pulls the
issuer's whole filing history by form, full-text hits for the phrases that carry a
forward risk (ATM, covenant, going concern, minimum bid price, lock-up, reverse split,
non-reliance), dated short interest, insider activity, active trials and the bid-price
rule. Every source in it was probed on 2026-09-22 and answered. The hunter therefore
starts at a document rather than a search box, and two hunts on one name start from the
same documents.

**Two labels in there stop a reader over-trusting a number**, and the note must carry
them too: `next_earnings_estimated` is Zacks's cadence algorithm and not a company
announcement — the TRT failure — and short interest is published about eight business
days after settlement, so the position carried *into* the fall is not observable.

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
expensive, and the note has to price them. Read the drift the right way round, though:
it exists because bad news arrives in clusters, so it is evidence that the stage's
question is the right one, not a reason to mark everything down.

**A finding with no date is not a finding.** The window is the drop-day close to the next
session's close. A shelf that will be drawn "at some point", a trial reading out next
year, a hearing in March: real, sourceable, and worth nothing to this ranking. They go in
`outside_window`.

**Two hypotheses are pre-registered**, in
`config/pipeline.yaml:reversal_hunt.pre_registered_hypotheses`, so neither can be
rewritten after the answer arrives. Leg 2: a fall with an identified, dated, unfinished
pipeline of further bad news continues, and one whose cause is complete and dated does
not. Leg 1: an overshoot pays only where a named mechanism closes the gap inside the
window. `rev_resolve.py` ranks `news_flow_balance`, `seller_is_finished_pct`,
`overshoot_pct` and each leg's own sum at every horizon, and splits
`by_overshoot_mechanism` into a with-mechanism and a without-mechanism arm, **whether or
not they look good**.

**Nothing may rest on a source that was not measured to answer.** The hunter's brief
carries the probed table. Three things that do NOT answer from this container — Nasdaq's
Listing Center, FTSE Russell's index notices, Nasdaq's press-release API — so an index
deletion or a delisting notice is only assertable through the issuer's own 8-K.

**Do not move a floor, a weight or a horizon on one day's result.** The repo has paid
for that lesson four times. A rule that changes with the data is not a hypothesis.

**No orders, ever.** If a future session finds an execution step in this stage, that is
a defect to remove, not a feature to configure.

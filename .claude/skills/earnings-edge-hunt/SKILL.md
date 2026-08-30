---
name: earnings-edge-hunt
description: Establishes what the market has already priced into an imminent earnings print, then sends free-roaming hunters to find information that is not in that price, has an adversary attack every finding, and emits a direction call only where the evidence structurally earns one. Use when asked to run the edge hunt, hunt for unpriced information, run the Monday BMO test, or produce direction calls for a day's earnings.
---

# Edge hunt — call direction only where something unpriced was actually found

This stage answers a narrower question than the rest of the pipeline. Not "what
will this stock do" for every name, but **"is there anything here the market has
missed, and if so which way does it cut."** Most names get `abstain`, and that is
the design working rather than the design failing.

## Why it looks like this

Three things in this repository shaped every rule below, and they are worth
carrying in your head while you run it.

**Self-rated confidence does not work.** Across 33 scored arm calls in
`backtest/runs/pilot-40`, the model's own `evidence_quality` field split top-third
and bottom-third accuracy at exactly 50/50. Nothing a hunter says about how sure
it feels enters the score. Confidence is derived by `scripts/edge_confidence.py`
from counts and adversary outcomes, and there is no field for an agent to assert
it.

**The crux is "is it already priced", and there is no rule that settles it.** The
PWR event in `backtest/notes/disagreement-map.md` had two analyses holding the
same principle, reading the same corpus, disagreeing about which of two stories
was the widely-told one, and landing 14% apart. That question does not get solved
by methodology. It gets an adversary whose only job is to argue the other side.

**Averaging disagreement produces nothing.** Every panelled call in `LEDGER.md`
so far is `Neutral / No Edge` — three for three — while the cheap preliminary read
called direction correctly on all three. Nothing here averages a direction score.
Findings survive or die individually and the survivors vote.

## What is fixed and what is free

Fixed absolutely: the priced-in baseline, the six-field finding contract, the
sourcing rule, and the fact that every name in the universe gets scored and
logged. Free absolutely: where hunters look, what they look for, what counts as
interesting, and how they reason. Do not add a research checklist. The nine-area
program belongs to stage 2 and importing it here would rebuild the thing this
stage exists to replace.

## 1. Resolve the universe

```bash
python3 scripts/edge_universe.py --date <YYYY-MM-DD> --session <bmo|amc> \
  -o <RUN>/edge/universe.json
```

No market-cap floor. `--include-unknown` picks up rows Nasdaq left as
`time-not-supplied`; use it when the confirmed list is thin, and record that you
did.

Resolve the run directory with `python3 scripts/run_paths.py --json` and work
inside `<run>/edge/`. Never invent a path.

## 2. Snapshot what is already priced, before anything searches

```bash
python3 scripts/priced_in.py --tickers <T1,T2,...> --date <YYYY-MM-DD> \
  --session <bmo|amc> -o <RUN>/edge/baselines/
```

**Commit this before launching a single hunter.** The baseline is the thing the
hunt has to beat, and a baseline written after the finding exists is a baseline
the finding has already contaminated. Sealing it is one cheap commit and it is
what keeps `why_not_priced` from being unfalsifiable.

Read the output before going on. `baseline_quality.tier` is the number that
matters:

| tier | meaning | what to do |
| --- | --- | --- |
| `full` | usable option chain and 4+ prior reactions | two hunters |
| `partial` | one of the two | two hunters |
| `thin` | neither | one hunter, and it will be capped at 50% confidence |

A `thin` name has no defensible statement of what the market priced, so no finding
about it can be confidently called unpriced. That cap is applied in code and is
not yours to override.

## 3. Heartbeat before you spend anything

```bash
python3 scripts/run_log.py --heading "Edge hunt — <date> <session> — STARTED" \
  --line "<n> names, <k> full/partial, <m> thin; <h> hunters planned"
scripts/publish.sh "edge hunt: started for <YYYY-MM-DD>"
```

One commit, and it is the only thing distinguishing a stage that never fired from
one killed on its first subagent.

## 4. Hunt

Launch `unpriced-hunter` subagents. Two per `full`/`partial` name, one per `thin`
name, all in parallel within the wave size in `config/pipeline.yaml`.

Give each hunter exactly this and nothing more:

- ticker, company name, event date and session
- the absolute path to that name's `baselines/<TICKER>.json`
- the output path `<RUN>/edge/hunts/<TICKER>-h<N>.json`

**Hunters must not see each other.** Two hunts on the same name are two
independent samples, and their agreement is a scored component. Tell one what the
other found and you have destroyed the measurement while making the output look
better. For the same reason, do not pass them your own view, the other names, or
anything from stage 1 or 2.

Publish after each wave, not at the end of the fan-out. A wave that dies has cost
you one wave.

## 5. Adversary pass

For every finding in every hunt, launch `priced-in-adversary`. Give it the finding
object, the baseline path, and the ticker. Never give it the hunter's `direction`,
`conviction_note` or reasoning — it judges the claim, not the argument.

Write each verdict to `<RUN>/edge/adversary/<TICKER>-<hunterstem>-<i>.json`, and
add two fields the confidence script needs to join them up:

```json
{"ticker": "TICK", "finding_key": "<TICKER>-h1#0", "...": "the agent's verdict"}
```

`finding_key` is `<hunter file stem>#<index of the finding in its array>`.

If the finding count exceeds the adversary budget, judge the findings behind the
highest-conviction names first and let the rest score as `unjudged` — which is
weighted as partially priced, so skipping the pass costs confidence rather than
granting it free. Record in the run log how many went unjudged.

## 6. Score every name, then select by threshold

```bash
python3 scripts/edge_confidence.py --run <RUN>/edge --threshold 55
```

This writes `edge-calls.json` containing **every name in the universe**, called or
not, with its confidence and the components that produced it.

Do not filter this file. Do not report only the called names and drop the rest.
Selection happens by thresholding a complete table, which is what makes the
risk-coverage curve computable afterwards and what stops "I only call the ones I
am sure about" from being an unfalsifiable claim. A hunt that reports three
confident names and silently discards nine is indistinguishable from cherry
picking, including to you.

## 7. Write the note

`<RUN>/edge/edge-note.md`, answer first:

- the called names, each with its direction, confidence, the finding, and its URL
- for each call, one line on what the price says and why the finding cuts against it
- the abstentions, in a table with their confidence and why they were held back
- coverage: `n called / n scored`, stated as a fraction, never as a bare hit count
- the disclaimer from `config/pipeline.yaml`

Then publish:

```bash
python3 scripts/update_index.py
scripts/publish.sh "edge hunt: <n>/<m> called for <YYYY-MM-DD>"
```

## 8. Resolve, the day after the window closes

```bash
python3 scripts/edge_resolve.py --run <RUN>/edge
```

Prints the risk-coverage curve, which is the only number worth reading. Accuracy
should rise as the threshold rises and coverage falls. If it is flat, the
confidence signal is decorative and the components in `edge_confidence.py` need
changing — not the threshold.

Two things the resolver reports that are easy to look past. `no-direction` names
moved less than their own deadband and are neither hit nor miss; scoring them as
misses is what made BILL a recorded failure on a −0.65% day. `abstentions_that_moved`
is the cost of caution, and if that list is long the system is not being selective,
it is being blind.

## Honest limits, to state in every note

One day of names is not an accuracy test. Five called names at 60% is a coin, and
the curve needs many runs before its slope means anything. Say so in the note
rather than letting a good first day read as a result.

Coverage tracks market cap. A day of large caps will flatter the hunt relative to
the small, high-change-expectation names the pipeline normally shortlists.

Never fabricate a number. Every company-specific figure carries a source URL or is
marked `unavailable`. A missing anchor correctly lowers confidence downstream; an
invented one corrupts everything after it.

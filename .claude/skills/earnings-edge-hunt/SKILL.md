---
name: earnings-edge-hunt
description: Establishes what the market has already priced into each of the day's earnings prints, then sends free-roaming hunters to find information that is not in that price, has an adversary size how much of each finding is already in, and emits one signed number per company so the day's names can be ranked. Use when asked to run the edge hunt, rank the day's earnings names, hunt for unpriced information, or score companies reporting.
---

# Edge hunt — one signed number per company, so the day can be ranked

This stage produces, for every company reporting in the window, a single signed
score on −100…+100. Sort on it and you have the day ranked from most-likely-up to
most-likely-down.

There is no call, no threshold and no direction label anywhere in the output. That
is deliberate and it is the point: **the question being tested is whether these
companies can be ranked at all**, and that question is answerable at every cut
only if nothing has already been rounded into a bucket upstream.

## Why it looks like this

**Categories destroyed the first run.** On 2026-08-31 the adversary returned one
of three verdicts, baseline quality was one of three tiers, and hunters returned
up/down/abstain. Every judged finding landed in one of two verdict buckets and
twelve companies collapsed to one non-zero score and eleven zeros. There was
nothing to rank, and the bucketing did that rather than the evidence. Everything
that was a category is now a number.

**Self-rated confidence does not work.** Across 33 scored arm calls in
`backtest/runs/pilot-40`, the model's own `evidence_quality` split top-third and
bottom-third accuracy at exactly 50/50. No hunter's feeling about its own certainty
enters the score. `scripts/edge_score.py` derives everything from sizes, source
counts and adversary numbers.

**The crux is "is it already priced", and no rule settles it.** The PWR event in
`backtest/notes/disagreement-map.md` had two analyses holding the same principle,
reading the same corpus, disagreeing about which story was the widely-told one, and
landing 14% apart. That gets an adversary, not a heuristic.

## What is fixed and what is free

Fixed: the sealed baseline, the numeric output contracts, the sourcing rule, and
that every name in the universe is scored. Free: where hunters look, what they look
for, and how they reason. Do not add a research checklist — the nine-area program
belongs to stage 2 and importing it here rebuilds the thing this stage replaces.

## 1. Universe and sealed baseline

```bash
python3 scripts/run_paths.py <YYYY-MM-DD> --json          # never invent a path
python3 scripts/edge_universe.py --date <D> --session <bmo|amc> -o <RUN>/edge/universe.json
python3 scripts/priced_in.py --tickers <T,...> --date <D> --session <s> -o <RUN>/edge/baselines/
```

Drop `time-not-supplied` rows unless you are deliberately re-measuring the phantom
rate — on 2026-08-31 **eight of eight** of them had no earnings event at all.

**Commit the baselines before launching anything.** A baseline written after a
finding exists is one the finding has contaminated. Then heartbeat:

```bash
python3 scripts/run_log.py --date <D> --heading "Edge hunt — <D> <session> — STARTED" --line "<plan>"
scripts/publish.sh "edge hunt: started for <D>"
```

## 2. Sweep — one agent, all names

Launch **one** `edge-sweep` agent for the entire universe. It confirms which
companies are really reporting and gives each survivor a continuous
`hunt_priority` plus a note on where an unpriced finding might live.

This exists because the first run sent twelve names to twelve deep hunters and
eight of them burned a full Opus/high budget establishing that no event existed.
One cheap agent replaces those eight.

Write to `<RUN>/edge/sweep.json`. Publish it.

## 3. Hunt — parallel only where independence is measured

Launch `unpriced-hunter` on the confirmed names, ordered by `hunt_priority`:

- **two hunters** on the top names, in parallel, isolated from each other
- **one hunter** on the rest

Two hunters on one name is the one place agent count must not be economised. On
2026-08-31 the two SY hunters returned *opposite* numbers from the same sealed
baseline and the same disclosed cohort table, and that disagreement was the most
informative output of the run. It only exists because neither could see the other.

Give each hunter exactly: ticker, company, event date and session, the absolute
path to its `baselines/<TICKER>.json`, its output path, and its row from
`sweep.json`. Nothing else — not your view, not the other names, not the other
hunter.

Publish after each wave, not at the end of the fan-out.

## 4. Adversary — one agent per ticker, not per finding

Launch `priced-in-adversary` **once per company**, with all of that company's
findings in one brief. It returns `priced_in_pct` from 0 to 100 for each, plus its
own independent `size_check_pct`.

Batching here is free. The findings share a company, a baseline and a news record,
and they often rest on the same document or mirror each other — judging them
together costs less and sees the interaction. What must stay separate is the
adversary from the hunters, not the adversary from itself.

**Judge every finding, on both sides.** On the first run adversaries were launched
against the bullish findings only; since an unjudged finding defaults to
mostly-priced, that mechanically favoured whichever side went unattacked. Never
give the adversary the hunter's own numbers or reasoning.

Write to `<RUN>/edge/adversary/<TICKER>.json`.

## 5. Score and rank

```bash
python3 scripts/edge_score.py --run <RUN>/edge
```

Writes `edge-scores.json`: every name, with `edge_score` (−100…+100, the ranking
key), `edge_pct` (the residual in points of spot), `confidence`, `uncertainty_pct`
and the full component breakdown.

Names whose event was not confirmed carry `rankable: false` and sit out of the
ranking rather than sorting to the top on a 0.

Do not filter this file and do not apply a cutoff. Selection is the reader's, made
afterwards on a complete table, which is what keeps "can these be ranked" testable
at every k.

## 6. The note

`<RUN>/edge/edge-note.md`, answer first: the ranked table, then for each of the top
and bottom names the finding driving it, its URL, and what the price already says.
Then the names that could not be ranked and why. End with the disclaimer from
`config/pipeline.yaml`.

## 7. Resolve, once the window closes

```bash
python3 scripts/edge_resolve.py --run <RUN>/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'   # the real number
```

Reports Spearman rank correlation between `edge_score` and the realised move, both
raw and divided by the implied move, with a permutation p-value; plus the spread
from being long the top third and short the bottom third.

The normalised correlation is the skill measure. Sorting a 15%-implied biotech
above a 2%-implied utility is easy and means nothing.

**One day is an anecdote.** A single day of five to twelve names cannot produce a
meaningful correlation, and the pooled figure across many days is the result. Say
so in every note rather than letting a good first day read as a finding.

## Standing rules

Never fabricate a number. Every company-specific figure carries a source URL or is
marked unavailable — a missing anchor correctly lowers the score, an invented one
corrupts the ranking.

Coverage tracks market cap. `backtest/FINDINGS.md` §27 measured news coverage as a
near-monotonic function of size, so a day of large caps flatters the hunt relative
to the small, high-change-expectation names the pipeline normally shortlists.

If an agent type comes back "not found", the definitions were written this session
and are not registered yet. Launch `general-purpose` with the agent file's body
pasted into the prompt, add a line forbidding it to read anything else under
`edge/`, and record in the run log that the run used the inlined form.

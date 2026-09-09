---
name: earnings-edge-hunt
description: Establishes what the market has already priced into each of the day's earnings prints, then sends free-roaming hunters to find information that is not in that price, has an adversary size how much of each finding is already in, and emits one signed number per company so the day's names can be ranked. Use when asked to run the edge hunt, rank the day's earnings names, hunt for unpriced information, or score companies reporting.
---

# Edge hunt — one signed number per company, so the day can be ranked

This stage produces, for every company reporting in the window, a single signed
number in **points of spot**: `impact_sum`, the hunters' own per-finding sizes added
up. Sort on it and the day is ranked. Beside it travels `conviction` (its absolute
value), which is where the direction skill lives.

There is no call, no threshold and no direction label anywhere in the output. That
is deliberate and it is the point: **the question being tested is whether these
companies can be ranked at all**, and that question is answerable at every cut
only if nothing has already been rounded into a bucket upstream.

## What changed on 2026-09-09, and why the arithmetic got simpler

`docs/EDGE_ANALYSIS.md` decomposed six resolved runs — 43 names, 249 findings —
against the realised move, pooling within days. Every transformation the scorer
applied lowered the rank correlation:

| | ρ | p |
| --- | --- | --- |
| impact sum, as the hunters wrote it | **0.407** | **0.017** |
| × (1 − priced_in/100) | 0.376 | 0.027 |
| cluster-max | 0.284 | |
| ÷ √k | 0.279 | |
| × agreement discount × quality multiplier → the old `edge_score` | 0.243 | 0.156 |

A paired bootstrap over days puts the gap between the first row and the last at
+0.165, 95% CI [+0.082, +0.244], so this is not small-sample noise. The machinery is
still computed — into `diagnostics`, where `residual_sum` remains a genuinely open
question and `edge_score_legacy` keeps earlier runs comparable — but it decides
nothing.

**The direction lives in the large numbers only.** Over all 38 de-duplicated events
the sign of `impact_sum` is a coin flip: 53% to the next close. But the rank of
`conviction` predicts whether the sign was right at ρ=+0.514, permutation p=0.0015.
Above the median conviction the sign is right on 74% of events. `|impact_sum| ≥ 3`
gave 16/21 with +6.37% per trade. Run the same test on `|edge_score|` and it returns
−0.003 — the old machinery destroyed this too.

**The stage has still not beaten a free control.** `-run_up_20d_pct`, one number off
the sealed baseline before any subagent is spawned, ranked those six days at ρ=0.335
and was positive on 6 of 6 days when traded. `edge_resolve.py` now prints it beside
every result. Until the hunt beats it, the hunt has not been shown to add anything,
and the note must say so.

## Why it looks like this

**Categories destroyed the first run.** On the first run of 2026-08-31 the adversary
returned one of three verdicts, baseline quality was one of three tiers, and hunters
returned up/down/abstain. Every judged finding landed in one of two verdict buckets
and twelve companies collapsed to one non-zero score and eleven zeros. There was
nothing to rank, and the bucketing did that rather than the evidence. Everything
that was a category is now a number.

**Removing the categories worked, and revealed the next problem.** The second run of
2026-08-31 produced eight rankable names with eight distinct scores — a strict order,
which is what the rebuild was for. But the whole table spanned less than
two-thirds of a point of spot, because an adversary judging all 51 findings on both
sides left very little standing. The stage now reliably produces an *order*; whether
that order carries information is what `edge_resolve.py` pooled across many days is
for, and one day of eight names cannot answer it.

**Self-rated confidence does not work.** Across 33 scored arm calls in
`backtest/runs/pilot-40`, the model's own `evidence_quality` split top-third and
bottom-third accuracy at exactly 50/50. No hunter's feeling about its own certainty
enters the score. `scripts/edge_score.py` derives everything from sizes, source
counts and adversary numbers.

**The crux is "is it already priced", and no rule settles it.** The PWR event in
`backtest/notes/disagreement-map.md` had two analyses holding the same principle,
reading the same corpus, disagreeing about which story was the widely-told one, and
landing 14% apart. That gets an adversary, not a heuristic.

## If your Routine prompt disagrees with this file

**This file wins.** The prompt is a bootstrap: it knows the environment, the timing and
the agent counts, and it cannot know the output contract, which has changed once already
and will change again as days pool.

Concretely, if the prompt you were given says the output is "one signed number on
−100…+100", or asks you to report `edge_score` and `confidence`, you have the
pre-2026-09-09 prompt. Those fields are gone from the decision path. Do this:

1. Rank and report on `impact_sum` and `conviction`, as sections 5 and 6 specify.
2. `edge-scores.json` names its own `ranking_key` — quote that in your closing report so
   the disagreement is visible rather than silently resolved.
3. Record one line in the run log: the Routine prompt is stale and the replacement text
   is in `docs/routine-prompts/edge-hunt.md`, waiting to be pasted. A session cannot
   update that Routine itself — `update_trigger` refuses any Routine an agent did not
   create — so the note is the only way the fix gets requested.

Do not split the difference by emitting both. Two ranking keys in one note is worse than
either.

## What is fixed and what is free

Fixed: the sealed baseline, the numeric output contracts, the sourcing rule, and
that every name in the universe is scored. Free: where hunters look, what they look
for, and how they reason. Do not add a research checklist — the nine-area program
belongs to stage 2 and importing it here rebuilds the thing this stage replaces.

## 0. Is there already a run in this directory?

Before writing anything, look:

```bash
ls <RUN>/edge/ <RUN>/edge/hunts/ <RUN>/edge/adversary/ 2>/dev/null
```

If a previous edge hunt has written here, **archive it before you start** — do not
merge into it and do not delete it:

```bash
mkdir -p <RUN>/edge/_run1-<session>/{baselines,hunts,adversary}
git mv <RUN>/edge/hunts/*.json <RUN>/edge/_run1-<session>/hunts/
git mv <RUN>/edge/adversary/*.json <RUN>/edge/_run1-<session>/adversary/
# plus that run's baselines, edge-scores.json and edge-note.md
```

`edge_score.py` reads `baselines/`, `hunts/` and `adversary/` non-recursively, so a
subdirectory is enough to hide the old run from it while keeping every file.

This is not hypothetical. Two edge hunts ran on 2026-08-31 over **different
windows** — the first on that day's `bmo` with `--include-unknown`, the second on the
`amc` plus next-day `bmo` that `--window` resolves. Left in place, twelve names from
the first run would have been pooled into the second's ranking as one day. Worse,
their findings predated the continuous contract and carried `direction` rather than
`expected_impact_pct`, which the current scorer reads as `0.0` — so all twelve would
have entered the table as zeros and sorted **above every genuinely negative name**.
Write a README in the archive saying which window it covered and why it moved.

Two runs on one date is normal — a retry, a re-run against a corrected universe, or
a second window. Assume it has happened rather than assuming it has not.

## 1. Universe and sealed baseline

```bash
python3 scripts/run_paths.py <YYYY-MM-DD> --json          # never invent a path
python3 scripts/edge_universe.py --window -o <RUN>/edge/universe.json
python3 scripts/priced_in.py --tickers <T,...> --date <D> --session <s> -o <RUN>/edge/baselines/
```

`--window` resolves today's `amc` plus the next trading day's `bmo`, which is the
pipeline's real window and what a daily routine wants. `--date`/`--session` is for
re-measuring one specific slice. Names in the window can span two dates and two
sessions, so `priced_in.py` needs one call per `(date, session)` group.

Drop `time-not-supplied` rows unless you are deliberately re-measuring the phantom
rate — on the first 2026-08-31 run **eight of eight** of them had no earnings event
at all. Withholding `--include-unknown` on the second run took the phantom rate to
**zero of ten**.

If the universe is empty, log it and stop cheaply. A holiday or a thin day is a real
answer.

### The baseline can be wrong about whether the event exists

`priced_in.py` infers an earnings cadence from 6-K/8-K text matches, and for a
foreign private issuer it can catch monthly operational updates instead — bitcoin
production, vehicle deliveries. It now returns `unknown` with
`cadence_implausible: true` when the inferred cadence is under 70 days, because no
quarterly (~91) or semi-annual (~182) reporter has one. Before that guard existed,
one day produced four wrong verdicts: CANG at a 16-day "cadence" and NIO at 10, HMR
at 49 and PXS at 51.

That mattered because `edge_score.py` sets `rankable = false` on a `suspect` verdict
and multiplies `baseline_quality` by 0.05, so three companies whose dates were
confirmed by their own press releases were arithmetically incapable of ranking
anywhere.

If the sweep confirms a date from a company source and the baseline still disagrees,
amend it **before any hunter launches**, from company sources only:

```bash
python3 scripts/edge_baseline_amend.py --dir <RUN>/edge/baselines            # dry run
python3 scripts/edge_baseline_amend.py --dir <RUN>/edge/baselines --apply
```

This does not breach the sealing rule: `event_plausibility` is an event-existence
flag, not a priced-in estimate, and confirming or killing the event is the sweep's
stated job. The original verdict is kept in `amended_from`.

**Amend symmetrically or not at all.** The same pass that upgraded three names from
`suspect` also downgraded NIO from `fits_cadence` to `unknown`, because NIO's verdict
rested on the identical defect and its eight recorded "reactions" were reactions to
delivery reports. Correcting only the names that would score better is how a scorer
gets quietly tuned toward a result.

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

Where the sweep set `baseline_history_trustworthy: false`, or the baseline carries
`cadence_implausible`, tell that hunter so explicitly. Otherwise it will use a
reaction history built from monthly operational updates as an earnings base rate.

Publish after each wave, not at the end of the fan-out.

### Do the budget arithmetic before the first launch

```
1 sweep  +  (confirmed names + double_hunt_top_n) hunters  +  (tickers with findings) adversaries
```

At the `edge_hunt` cap of 20 that is about **eight hunted names**: 1 + 10 + 8 = 19.
Ten confirmed names needs 1 + 12 + 10 = 23 and does not fit, so plan the shed at the
start rather than discovering it when the adversaries are due.

Shed per `budget.edge_degrade_order`, which now sheds **names** before rigour:
unconfirmed names first, then lowest `hunt_priority`. Two things are never shed at
any budget — the two-hunter split, and adversary coverage of every finding.

Keeping a name but measuring it worse corrupts the ranking silently. Dropping one
puts it in the table as `rankable: false` with a stated reason, where the reader can
see it. Prefer the visible loss.

One judgement call worth stating: shed by `hunt_priority` but **keep the names with
a live option chain**, even if they rank low. On 2026-08-31 MDT (priority 26) and NIO
(37) both sat below the median and were kept deliberately, because they were the only
two names of ten with a usable chain and therefore the only ones where "what the
market priced" was measured rather than inferred from a historical median. A ranking
built entirely on names with no options is measuring something weaker. Record the
deviation in the run log.

**Concurrency is not the same limit as budget.** `max_concurrent_subagents` is about
load; the cap of 20 is about spend. An `amc` name reporting tonight must be judged
before its release, so serialising strictly can push its adversary past the event —
exceed the concurrency guideline for those and stay inside the total.

## 4. Adversary — one agent per ticker, not per finding

Build the briefs with the script, never by hand:

```bash
python3 scripts/edge_brief.py --run <RUN>/edge      # writes adversary-briefs/<TICKER>.json
```

It carries the claim, its source and its date, and nothing else — by whitelist, so a
new field on the hunter contract cannot leak a hunter's own size or its
`why_not_priced` into the brief and destroy the independence the whole pass depends
on. It also generates each `finding_key` with the same rule `edge_score.py` uses to
join on (`<hunt file stem>#<index>`).

Launch `priced-in-adversary` **once per company**, with that company's brief. It
returns `priced_in_pct` from 0 to 100 for each finding, plus its own independent
`size_check_pct`, and writes `<RUN>/edge/adversary/<TICKER>.json` itself.

Then verify the join before you score:

```bash
python3 scripts/edge_brief.py --run <RUN>/edge --check
```

A `finding_key` that does not match is dropped **silently** — the finding keeps no
`priced_in_pct`, defaults to "unjudged, mostly priced", and quietly costs that name
edge with nothing in the output to say so. `--check` names every unjudged finding,
orphan verdict, null number and duplicate. Run it; "8 of 8 adversary files exist" is
not the same statement as "every finding carries a number".

Batching here is free. The findings share a company, a baseline and a news record,
and they often rest on the same document or mirror each other — judging them
together costs less and sees the interaction. What must stay separate is the
adversary from the hunters, not the adversary from itself.

**Judge every finding, on both sides.** On the first run adversaries were launched
against the bullish findings only; since an unjudged finding defaults to
mostly-priced, that mechanically favoured whichever side went unattacked. Never
give the adversary the hunter's own numbers or reasoning.

**If an adversary returns its JSON in the message instead of writing a file**, its
definition is missing the `Write` tool — check
`.claude/agents/priced-in-adversary.md`'s frontmatter before launching the rest.
On 2026-08-31 all six adversaries hit this and the parent transcribed every verdict
by hand, which is slow and puts a silent-drop typo into every join key. The tool is
granted now; if it goes missing again, fix the definition rather than transcribing.

## 5. Score and rank

```bash
python3 scripts/edge_score.py --run <RUN>/edge
```

Writes `edge-scores.json`: every name with `impact_sum` (the ranking key, signed
points of spot), `conviction`, `priced_lean_pct` (the control), and a `diagnostics`
block. The script prints which names clear `conviction_floor` from
`config/pipeline.yaml`.

Names whose event was not confirmed carry `rankable: false` and sit out of the
ranking rather than sorting to the top on a 0.

Do not filter this file and do not apply a cutoff — not even the conviction floor.
The floor governs **emphasis in the note**, never the contents of the JSON, because
the ranking test needs the complete table at every k.

Nothing in `diagnostics` is a decision input. If you find yourself reaching for
`confidence` or `baseline_quality` to decide what to highlight, stop: they were
measured at −0.090 and +0.074 against the realised move, and on 2026-08-31 the
highest-confidence name was the uninformative one while the name carrying that day's
entire correlation had the lowest confidence in the run.

## 6. The note

`<RUN>/edge/edge-note.md`, answer first: the ranked table, then for each of the top
and bottom names the finding driving it, its URL, and what the price already says.
Then the names that could not be ranked and why. End with the disclaimer from
`config/pipeline.yaml`.

Four things the note must also do, each because a reader would otherwise draw a
wrong conclusion from a correct table:

**Separate the order from the sign.** Report the ranking for every name, and mark
which names clear the conviction floor. Say in the note that below the floor the sign
is a coin flip on the evidence so far (53% over 38 events) and that above it the rank
of conviction predicted sign-correctness at ρ=+0.514. A reader who treats a
`impact_sum` of −0.4 as a bearish view is reading the table wrong, and the note is
where that is prevented.

Also state that `impact_sum` is not a forecast of the move. The same fact often
appears in two findings from two sources and adding both double-counts it — which is
exactly what the cluster-max was built to stop, and the cluster-max is what the
measurement demoted. The number ranks; it does not size.

**Give the control its own line.** Print `-run_up_20d_pct` beside the ranking and say
whether the hunt's order differs from it. On the six resolved runs that free number
ranked at ρ=0.335 against the hunt's raw 0.407, a gap whose CI spans zero. A note
that reports the ranking without the control is claiming more than the evidence
carries.

**Report the sign balance.** Count how many hunts leaned each way and say so. Six of
eight leaned negative on 2026-08-31, which is more plausibly an artefact of asking
hunters to find what the market has missed into a print than a fact about those eight
companies. If it recurs across many days, the hunter prompt is generating pessimism
rather than detecting it — and that is only visible if each note records the count.

**Say what the adversary broke.** The pass is the most informative part of the stage
and its corrections belong in the note, not just in the JSON. Name the findings that
turned out to be factually wrong and how, and name the one that survived best with
its `priced_in_pct`. An adversary that conceded a fact but refused its sign is
reporting something different from one that refuted the fact; keep that distinction.

**Say how much of the baseline was measured rather than inferred.** Count the names
with a live option chain. Where there is none, `priced_lean_pct` falls back to
−0.05 × the 20-day run-up, and the "expected move" in the baseline is a historical
median rather than a priced expectation. Seven of ten names had no listed options on
2026-08-31, and 18 of the first 43 resolved names took the fallback. Nothing
multiplies by that lean any more, but `edge_resolve.py` still normalises by the
expected move, so a note that calls the normalised correlation an implied-move
measure is overstating it.

**Say what the day would have cost to trade.** Capacity is not in the scorer and not
in the budget. Report spot × 20-day average volume for the top and bottom names. On
2026-09-02 the single best-ranked name, DLTH, moved +23.20% on **$170k a day** of
turnover; six of the first 22 long/short positions traded under $1m a day. A ranking
whose extremes are untradeable is a research result, not a signal, and the note
should be the place a reader learns which one they are looking at.

## 7. Resolve, once the window closes

```bash
python3 scripts/edge_resolve.py --run <RUN>/edge
python3 scripts/edge_resolve.py --pool 'research/2026/*/*/edge'   # the real number
```

Reports, per day and pooled: the rank correlation between the key and the realised
move; **the conviction-versus-sign correlation**, which is the threshold-free form of
"is the direction real"; both free controls; the legacy key for continuity; and the
long/short spread.

The pooled figure pools **within** days — each day converted to within-day ranks and
centred — because concatenating raw pairs across days lets market-wide drift into the
rank structure and understates every ranker (0.189 against 0.243 on the same six
days).

Watch the conviction number as days accumulate. It needs no cut and no calibration,
which is what makes it the honest headline; the ranking correlation and the
long/short spread both depend on where you cut.

**One day is an anecdote.** A single day of five to twelve names cannot produce a
meaningful correlation, and the pooled figure across many days is the result. Say
so in every note rather than letting a good first day read as a finding.

## Standing rules

Never fabricate a number. Every company-specific figure carries a source URL or is
marked unavailable — a missing anchor correctly lowers the score, an invented one
corrupts the ranking.

Dates come off the URL path, not the search snippet. Search results relabel old
articles with the current year, and on 2026-08-31 three separate leads on one name
turned out to be August 2025 stories served as August 2026.

The sweep's `session_confirmed` is not `event_confirmed`. A confirmed date with an
unconfirmed hour does not say which session carries the reaction, and
`edge_resolve.py` measures the move over the session you record. Two names that day
were company-confirmed `bmo` while nearly all their prior prints were `amc`, and one
had a date with no sourceable hour.

Coverage tracks market cap. `backtest/FINDINGS.md` §27 measured news coverage as a
near-monotonic function of size, so a day of large caps flatters the hunt relative
to the small, high-change-expectation names the pipeline normally shortlists.

If an agent type comes back "not found", the definitions were written this session
and are not registered yet. Launch `general-purpose` with the agent file's body
pasted into the prompt, add a line forbidding it to read anything else under
`edge/`, and record in the run log that the run used the inlined form.

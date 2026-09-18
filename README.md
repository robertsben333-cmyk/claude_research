# Daily earnings research pipeline

> **Stages 1 to 4 were retired on 2026-09-18.** The triage, the deep-dive dossiers, the
> seven-persona panel and the calibration ledger are frozen under
> [`archive/`](archive/README.md), which records what they scored and why that was not
> enough. What still runs is **stage 0** (the day's earnings universe) and **stage E**
> (the edge hunt, which places real orders on a paper account). The section below
> describes the retired funnel and is kept as history.

An automated research pipeline over US companies reporting earnings between today's
close and tomorrow's open. It runs itself on a schedule, does the expensive work with
parallel Opus subagents, and archives every run in this repository.

The deliverable used to land each weekday around **19:30 CET** as `04-advice.md`, with a
call, an expected move, a probability and a certainty tier per name. Over 22 panels it
produced 21 calls of Neutral and one wrong directional call, which is what ended it.

> This is research, not financial advice. Earnings reactions are highly uncertain and
> can be driven by market positioning, guidance, macro conditions, and management
> commentary rather than reported results alone.

## The funnel

```
  ~60 companies reporting tonight/tomorrow morning        stage 0   07:12
        │  liquidity, options market, confirmed timing
  ~35 eligible
        │  scored on: how much could this move?
        │             can research actually say anything?
   10 shortlisted                                         stage 1   09:38
        │  one Opus/high deep researcher each, two batches
   10 full dossiers                                       stage 2   11:52 + 14:22
        │  ranked by conviction × evidence completeness
    3 panelled                                            stage 3   17:37
        │  7 independent personas each → synthesis → dossier
    the advice note                                       ~19:30
        │  what actually happened
    scored, next morning                                  stage 4   08:20
```

Two ideas do most of the work.

**Triage scores two things, not one.** A name has to be able to move *and* be
forecastable. A biotech binary readout scores 95 on the first and 15 on the second — it
will move enormously and nobody can call it, so it does not get a dossier. Being willing
to discard those is what keeps the ten slots useful.

**The panel is genuinely independent.** (It was, and it did not help: the seven personas
averaged 42% on direction while their consensus scored 27%, so the aggregation stacked
their shared bearish prior instead of cancelling it. Kept here as the design intent.) Seven personas research the same name through
different lenses in isolated subagents. They never see each other's verdicts, nor the
stage 2 dossier, nor the orchestrator's view — the persona agents are defined without
file-reading tools so they cannot. Their *disagreement* is the signal:
`scripts/synthesize.py` turns the spread of their scores into a disparity measure and
lowers certainty when they diverge. A panel that has been allowed to converge produces a
confident number that means nothing.

## Layout

```
.claude/agents/     9 subagent definitions — 1 deep researcher, 7 personas, 1 triage scout
.claude/skills/     5 stage skills, one per pipeline stage
config/             pipeline.yaml — every threshold, weight and budget cap
scripts/            fetch, path resolution, synthesis maths, validation, publishing
research/           the archive: research/<YYYY>/<MM>/<YYYY-MM-DD>/
docs/ROUTINES.md    the schedule, the cost table, and how to change either
INDEX.md            generated archive index
archive/            retired: the backtest, stage N, and stages 1-4 with their ledger
                    and PREDICTIONS.csv — see archive/README.md
CLAUDE.md           what a fresh Routine session needs to know
```

## Running it by hand

```bash
python3 scripts/smoke_test.py                # is the plumbing intact? (no model calls)
python3 scripts/get_earnings.py --probe      # can this environment reach a data source?
python3 scripts/get_earnings.py              # build today's universe
python3 scripts/run_paths.py --json          # where today's files go
```

`smoke_test.py` runs the whole chain against synthetic data in about a second: agent
definitions parse, path resolution works, every stage's file shape passes its validator,
and the conviction gate fires when it should. Run it after editing a skill, an agent, or
`synthesize.py` — a shape mismatch between two stages otherwise surfaces at 17:37 on a
Tuesday.

Then in a Claude session in this repo: *"Run stage 1 of the earnings pipeline for
today."* Stages are resumable and skip work already on disk, so re-running one is safe.

## Cost

31 Opus/high subagents per trading day, deliberately spread across four firings so no
single rolling usage window absorbs all of it. `docs/ROUTINES.md` has the cost table and
the knobs to turn — `panel.names` is the big one.

## Does it work?

`LEDGER.md` is the answer, and it is kept whether or not it flatters the pipeline. Stage
4 scores every call the morning after against the realised close-to-close move, and
tracks direction hit rate, magnitude error, band hit rate, and — the one that matters
most — whether High-certainty calls actually hit more often than Low-certainty ones. If
they do not, the certainty tiering is decorative and the synthesis needs fixing.

It also scores the ten deep dossiers' preliminary reads separately from the three panel
calls. That comparison is the evidence for whether the seven-persona panel earns its
cost over a single deep researcher. If it does not, stage 3 should be cut.

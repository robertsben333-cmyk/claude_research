# Stage H: the self-revising holistic researcher

Built 2026-11-05 on the operator's idea (thread "Build self-evolving holistic researcher
routine"). Research only: **no orders**. Writes `research/<date>/edge-holistic/`.

## The two hypotheses

1. **Turning evidence into points loses information.** Stage E-P has a searcher file
   findings and four blind judges size each one; the sum ranks the day. Stage H has ONE
   researcher per name that is searcher and judge at once: it keeps searching while it
   thinks, confirms what it doubts, reads web, grey and alternative sources, and returns
   one view (`p_up`, and a long or short recommendation only where it is confident the
   market has not priced the reaction).
2. **The best approach drifts with the market.** What works this week may not work next
   week, so the approach is a playbook the stage rewrites from its own resolved days,
   not a list of static lessons.

## How it runs (one fire, weekdays 14:15 New York)

1. **Names.** Stage E-P's sweep-confirmed names by `hunt_priority`, at most 12, with E-P's
   sealed baselines. Using E-P's sweep means every name also has an E-P panel score to
   compare against, and stage H does not spend a sweep of its own.
2. **Research.** One `holistic-researcher` (Opus 5.5) per name, following
   `playbook/current.md` (frozen into the run as `playbook-a.md`). On every name a second
   researcher follows the frozen control (`playbook-b.md` = hp.v1); until 2026-11-13 that
   was a date-seeded random third of the names. Each run records `control_design`
   (`random_share_0.34` or `all_names`), carried into every outcome row, and `evaluate`
   reports the paired comparison per design as well as pooled. Researchers do not know
   their arm.
3. **Collect** before 15:45 ET: `recommendations.json` and `note.md`, published before
   the 16:00 close.
4. **Learn**, on every fire: `holistic.py resolve` prices every closed window,
   `holistic.py evaluate` scores every version, and if the gate is open one
   `holistic-reflector` proposes up to three small edits, which `holistic.py revise`
   applies or rejects. Tomorrow's run uses the result.

**The window** (fixed, not in the playbook): entry at the run day's close (the research
finishes after E-P's 13:30 entry, so 13:30 would leak the afternoon's price into the
score); an amc name exits at the next opening print, a bmo name at 13:00 New York on its
report day, the same exits as stage E-P's scorebord. E-P's selected names are re-priced on
this window for the comparison, so both sit on one ruler.

## What may change and what may not

| changes (the playbook, `playbook/current.md`) | never changes (code and config) |
| --- | --- |
| what to look for, where, which sources, how to weigh grey material | the window and the 15:35 ET deadline |
| how to interpret a reaction, positioning, the line a stock trades on | the source and no-fabrication rules, public information only |
| how to spend time, when to stop | the output contract (`p_up`, recommendation, evidence) |
| calibration posture and **when to recommend** | the metrics: Brier on every name, return and hit rate of the recommendations, a fixed-cut view at 65 |
| anything else, including removing sections | the gates, and the frozen control `playbook/control.md` (sha256 pinned in config, smoke-tested) |

## Why this design: what the literature says, and what it does not cover

The loop is a small version of the reflective prompt-evolution designs of the last two
years:

- **Reflexion** (Shinn et al., 2023): an agent writes verbal reflections on its failures
  and reads them next time. Stage H's reflector is the same idea, run across days rather
  than within a task.
- **ACE, Agentic Context Engineering** (Zhang et al., 2025, arXiv 2510.04618): the context
  is an evolving playbook, with a generator, a reflector and a curator. Its central
  finding is that letting a model rewrite the whole context causes *context collapse*
  (each rewrite drops detail) and *brevity bias*, and that small itemised delta edits,
  merged by plain code rather than by the model, avoid it. Stage H copies that: the
  reflector proposes `edit`, `add`, `remove` on numbered sections, and `holistic.py`
  merges them deterministically.
- **GEPA** (Agrawal et al., 2025, arXiv 2507.19457): reflective prompt mutation with a
  Pareto archive of candidates, so a bad mutation does not erase a good ancestor. Stage H
  keeps every version in `playbook/versions/` and allows `revert_to`, and keeps hp.v1 as a
  permanent control.
- From model risk practice: **champion and challenger**, and **walk-forward** testing.
  Each version is judged only on names it predicted after it was written.

What those papers have and this stage does not: thousands of cheap, instantly scored
trials. Stage H gets about 12 names a day, each scored one or two days later, on a target
(the sign of an earnings reaction) that is close to a coin flip. That is the main risk,
and the gates exist for it.

## The risks, stated plainly

- **Chasing noise.** With 30 resolved names a hit rate has a standard error near 9
  points; five recommendations a week say almost nothing. A reflector that reads one
  week's winners and losers will always find a story. Guards: no revision below 30
  resolved names over 3 run days on the current version; at most 3 operations; each
  citing at least 3 resolved names; Brier over all names (not the few recommendations)
  is the headline; a revision must state its predicted effect and a revert condition,
  and the next reflection checks them.
- **Drift without a baseline.** A chain of small changes can wander away from anything
  that worked, and each version looks fine on its own small sample. Guards: the frozen
  control on the same names gives a paired comparison that does not move; a drift alarm
  (evolving Brier worse than the control over the last up to 60 pairs with t >= 2)
  allows only `revert_to`.
- **Overfitting to names.** "Short retailers after a 20% run-up" written after two
  retailers fell is a company fix in disguise. The script rejects any operation that
  names a ticker, and the reflector is told to write mechanisms.
- **Accretion.** A playbook that only grows becomes the static lesson list this stage was
  meant to avoid. The playbook is capped at 16,000 characters and the reflector is told
  to prefer edits and removals.
- **Small versions.** If the gate opens every three days, each version carries about 30
  to 40 names. That is enough to stop a bad version, not to prove a good one. The
  question the operator asked (does adapting beat not adapting) is answered by the
  **lineage** row, every evolving version against the control on the same names, which
  pools versions on purpose because it tests the process, not a version. Expect weeks
  before it says anything.
- **Holistic means less inspectable.** A single `p_up` per name loses the per-finding
  trail stage E-P has. The researcher records `questions_pursued`, `key_evidence` with
  its weight, and `self_critique`, so a post-mortem can still see what it relied on.
- **Self-modification through publish.** The Routine pushes the new playbook to `main`
  with the day's research, like `LESSONS.md`. Nothing reads it except this stage, and
  the control and the code are checked by the smoke test, but a bad edit goes live
  without review. `changes.jsonl` and `CHANGELOG.md` are the audit trail; the operator
  can revert any version by hand.

## Files

```
researcher_holistic/
  playbook/current.md          the evolving approach (data; changed only by holistic.py revise)
  playbook/control.md          hp.v1, frozen; sha256 pinned in config/pipeline.yaml
  playbook/versions/hp.vN.md   every version ever used
  playbook/changes.jsonl       every proposal: applied, rejected or kept, with reasons
  playbook/CHANGELOG.md        human-readable record of applied changes
  scripts/holistic.py          pick, brief, collect, resolve, evaluate, revise, status, selftest
  analysis/outcomes.json       one frozen row per resolved name and arm
  analysis/evaluation.json/.md per version, control, paired, E-P on the same names, the gate
  routine-prompts/holistic.md  the Routine's text and settings
.claude/agents/holistic-researcher.md   searcher and judge in one; fixed rules + contract
.claude/agents/holistic-reflector.md    reads outcomes, proposes delta edits
.claude/skills/earnings-holistic-research/SKILL.md
```

Versions: the researcher definition is `us-holistic.vN` (provenance, `--market US-H`), the
playbook `hp.vN` (in `pick.json`). Judge a (definition, playbook) pair only on its own
resolved names, never pooled with stage E-P, stage D or each other.

This is research, not investment advice.

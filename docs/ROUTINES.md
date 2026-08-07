# The Routines — schedule, cost, and setup

Five Routines run the pipeline. Each fires a **fresh session** in a cloud environment,
which clones this repo, reads `CLAUDE.md`, invokes one stage skill, and pushes its
output back before dying.

## Schedule

All wall-clock times are Europe/Amsterdam. Weekdays only — US markets are closed at the
weekend, and `scripts/get_earnings.py` handles NYSE holidays itself, so a holiday run
simply finds an empty universe and stops cheaply.

| Time | Stage | Skill | Subagents | Cost |
| --- | --- | --- | --- | --- |
| 07:12 | 0 · Universe | `earnings-universe` | 0 | negligible |
| 09:38 | 1 · Triage | `earnings-triage` | ≤6 Sonnet/medium | low |
| 11:52 | 2A · Deep dive, batch 1 | `earnings-deep-dive` | 5 Opus/high | **high** |
| 14:22 | 2B · Deep dive, batch 2 | `earnings-deep-dive` | 5 Opus/high | **high** |
| 17:37 | 3 · Panel & advice | `earnings-panel-advice` | 21 Opus/high | **highest** |
| 08:20 | 4 · Calibration | `earnings-calibration` | 0 | low |

Stage 3 starts at 17:37 to deliver the advice note by roughly **19:30**, which is
13:30 New York time — the US session is live, so positioning and implied-move data are
current, and after-close reporters have not printed yet.

### Cron expressions

Routines are scheduled in **UTC**, so they do not follow Dutch daylight saving. Use the
summer set from late March to late October and the winter set otherwise.

| Stage | Summer (CEST, UTC+2) | Winter (CET, UTC+1) |
| --- | --- | --- |
| 0 | `12 5 * * 1-5` | `12 6 * * 1-5` |
| 1 | `38 7 * * 1-5` | `38 8 * * 1-5` |
| 2A | `52 9 * * 1-5` | `52 10 * * 1-5` |
| 2B | `22 12 * * 1-5` | `22 13 * * 1-5` |
| 3 | `37 15 * * 1-5` | `37 16 * * 1-5` |
| 4 | `20 6 * * 1-5` | `20 7 * * 1-5` |

Switching over is one `update_trigger` call per Routine changing `cron_expression`.
Nothing else moves. Ignoring the switch is not fatal either — every stage runs an hour
later than intended and stage 3 lands near 20:30, which still works.

None of the times sit on `:00` or `:30`. Those minutes are where every scheduled job on
the platform piles up.

## How the day is spaced, and why

The spacing is the usage-limit design, not a convenience.

Usage is enforced over a **rolling five-hour window** plus a weekly cap. The pipeline's
expensive work is 31 Opus/high subagents; running them together would spike one window
badly. Spread as above, the five-hour window ending with stage 3 contains **stage 2B
(5 agents) and stage 3 (21 agents)** — stage 2A and stage 1 have already aged out.

That is why the deep dives are split into two batches at all. One firing of ten deep
researchers would be simpler to write and considerably worse to live with.

The other consequence of the spacing: **each stage's output is on disk and pushed before
the next stage starts.** A session that dies mid-stage costs one stage, not the day.

### If you hit limits anyway

Turn these knobs in `config/pipeline.yaml`, in this order:

1. `panel.names: 3` → `2` — removes 7 Opus/high agents, the single biggest saving.
2. `triage.shortlist_size: 10` → `8` — removes 2 deep researchers.
3. `deep_dive.batches: 2` → `3` — same total cost, spread across three windows.
   Requires a third stage-2 Routine.
4. `panel.personas` — leave this alone. Cutting personas does not save much and it
   directly degrades the disparity measure that the whole calibration rests on.

Stage 3 also sheds scope on its own when the run log shows earlier stages ran long, and
records what it dropped in `degradations_applied`.

## Before any of this works: attach the repository

**The six Routines are currently paused, and they must stay paused until this repository
is attached to each of them.** Their names carry a `[PAUSED — attach repo]` suffix as a
reminder.

A Routine fires a fresh session that only has the repositories configured as its
*sources*. A Routine created programmatically — via the `create_trigger` MCP tool —
has no way to set that field, so its sessions start with no repository at all. They
then do the research, find nothing to publish into, and the work is lost when the
container is reclaimed.

This was verified twice, not assumed. A stage 0 run with no repo attached burned roughly
four million tokens and pushed nothing. A second run, scoped to nothing but
`git clone` plus an empty commit, ran for ten minutes and also pushed nothing.

To fix it, for each of the six Routines in the claude.ai Routines UI:

1. Open the Routine.
2. Add `robertsben333-cmyk/claude_research` as its repository/source.
3. Set the output branch to `main`.
4. Re-enable it and drop the `[PAUSED — attach repo]` suffix from the name.

Then verify with one cheap firing of stage 0 before trusting the expensive stages: use
`fire_trigger` on the stage 0 Routine and confirm a `stage 0: universe for <date>`
commit appears on `main`. If that commit does not appear, nothing downstream will work
either — stop and fix it rather than letting stages 2 and 3 spend 31 Opus/high
subagents on output that cannot be saved.

## Environment

The Routines target the environment with **full network access**. This matters: the
default "trusted network access" environment blocks `api.nasdaq.com`, Yahoo Finance,
SEC EDGAR, and effectively every financial data source, for `WebFetch` and for `curl`
alike. `WebSearch` still works there, so the pipeline degrades to search snippets rather
than failing outright — but the dossiers are much weaker.

To check which environment a session is in:

```bash
python3 scripts/get_earnings.py --probe
```

`network_blocked` on every source means the Routines are pointed at the wrong
environment. Fix it by updating the Routines' `environment_id` rather than by working
around the proxy.

## Repointing, pausing, editing

```
list_triggers                      # trigger IDs, cron, next run
update_trigger  trigger_id=...     # change cron, prompt, or enabled state
fire_trigger    trigger_id=...     # run one stage now, outside its schedule
delete_trigger  trigger_id=...     # remove it
```

`fire_trigger` is the right way to test a stage or to catch up after a failure — the
stages are resumable and skip work that is already on disk.

To pause the pipeline for a week, set `enabled: false` on all five. To stop the cost
without losing the archive, pause stages 2A, 2B and 3 and leave 0, 1 and 4 running:
you keep the daily universe and shortlist for a rounding error in tokens.

## Running a stage by hand

In any session with this repo:

```
Run stage 2 batch 1 of the earnings pipeline for today.
```

The stage skills trigger on that phrasing. Or invoke one directly: `earnings-universe`,
`earnings-triage`, `earnings-deep-dive`, `earnings-panel-advice`,
`earnings-calibration`.

## What each Routine's prompt says

The prompts are stored in the Routines themselves, not in this repo, so changing one
means calling `update_trigger`. Each is self-contained — a fresh session has no memory
of the others — and follows the same shape: state which stage it is, name the skill,
point at `CLAUDE.md`, and require a push at the end.

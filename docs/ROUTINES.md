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

## Each Routine must have this repository attached

A Routine fires a fresh session that only has the repositories configured as its
*sources*. Attaching this repo to each of the six is what makes the pipeline work at
all — without it a session does the research, finds nothing to publish into, and loses
everything when the container is reclaimed.

This is not theoretical. Before the repo was attached, a stage 0 firing burned roughly
four million tokens and pushed nothing, and a second firing scoped to nothing but a
clone plus an empty commit ran ten minutes and also pushed nothing. After attaching it,
the same Routine published cleanly on the first try.

A Routine created programmatically through the `create_trigger` MCP tool has no field
for sources, so **any Routine added that way later must have its repository attached by
hand in the claude.ai Routines UI** before being enabled.

### The outcome branch is overridden on purpose

Each Routine is assigned an auto-generated outcome branch — `claude/funny-shannon`,
`claude/dreamy-turing`, and so on. Left alone, that would scatter the five stages across
five different branches, and stage 1 would never see what stage 0 wrote.

`scripts/publish.sh` checks out `main` explicitly and pushes there, which overrides the
assigned branch. Verified: the stage 0 test run started on
`claude/funny-shannon-rgagyj` and still published to `main`, leaving no stray branch
behind. Do not "fix" the checkout in `publish.sh` to use the current branch — the shared
`main` is what lets the stages hand files to each other.

### Verifying after any change

Fire stage 0 and confirm a `stage 0: universe for <date>` commit appears on `main`. It
is the cheapest stage and exercises the whole path: repo access, network, the fetch
script, the run log, the index, and the push. If that commit does not appear, nothing
downstream will work either — fix it before letting stages 2 and 3 spend 31 Opus/high
subagents on output that cannot be saved.

**Verified working 2026-08-08:** stage 0 fetched 48 companies from the Nasdaq feed,
qualified 27, correctly rolled the Saturday reference date to Monday's open (0 AMC,
48 BMO), and published to `main`. This environment has real network access — the feed
is not degraded to search snippets.

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

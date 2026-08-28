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
| 08:20 | 4 · Calibration (of yesterday) | `earnings-calibration` | 0 | low |
| 08:38 | 1 · Triage | `earnings-triage` | ≤3 Sonnet/medium | low |
| 10:22 | 2 · Deep dive (one group) | `earnings-deep-dive` | 3 Opus/high, in waves of 2 | **high** |
| ~~12:22~~ | ~~2B · Deep dive, batch 2~~ | *paused 2026-08-28* | — | — |
| 17:52 | 3 · Panel & advice | `earnings-panel-advice` | 7 Opus/high | **highest** |

Subagent counts were cut on 2026-08-13 (10 dossiers → 6, 3 panels → 2), and cut again on
2026-08-28 (6 dossiers → 3 in **one** firing, 2 panels → 1). The day is now **10
Opus/high agents**, down from 31. See "What actually went wrong, 2026-08-08 to 08-12"
and "Scaling back up" below before raising them.

**One research group.** Stage 2 is a single firing again. Splitting six names across two
firings was supposed to halve the spike; what it did was give the day two chances to be
killed, and batch 2 took both — killed mid-run on 08-26 (URBN lost) and again on 08-27
(IREN lost, no closing log). Three names in waves of two, in one firing, is sized so the
whole stage lands. The 2B Routine is **paused, not deleted**, so going back to two
batches is one `update_trigger` call plus `deep_dive.batches: 2`.

Stage 3 starts at 17:52 to deliver the advice note by roughly **19:30**, which is
11:52 New York time — the US session is live, so positioning and implied-move data are
current, and after-close reporters have not printed yet.

### Cron expressions

Routines are scheduled in **UTC**, so they do not follow Dutch daylight saving. Use the
summer set from late March to late October and the winter set otherwise.

| Stage | Summer (CEST, UTC+2) | Winter (CET, UTC+1) |
| --- | --- | --- |
| 0 | `12 5 * * 1-5` | `12 6 * * 1-5` |
| 4 | `20 6 * * 1-5` | `20 7 * * 1-5` |
| 1 | `38 6 * * 1-5` | `38 7 * * 1-5` |
| 2 | `22 8 * * 1-5` | `22 9 * * 1-5` |
| 2B *(paused)* | `22 10 * * 1-5` | `22 11 * * 1-5` |
| 3 | `52 15 * * 1-5` | `52 16 * * 1-5` |

Switching over is one `update_trigger` call per Routine changing `cron_expression`.
Nothing else moves. Ignoring the switch is not fatal either — every stage runs an hour
later than intended and stage 3 lands near 20:30, which still works.

None of the times sit on `:00` or `:30`. Those minutes are where every scheduled job on
the platform piles up.

## How the day is spaced, and why

The spacing is the usage-limit design, not a convenience. The pipeline's expensive work
is now 10 Opus/high subagents — 3 in the deep dive and 7 in the panel. The spacing below
was designed for the original 31-agent shape. It is kept unchanged because it costs
nothing to keep and it is what the schedule returns to as the sizes go back up; at the
current sizes every window has a great deal of slack.

Usage is enforced over a **five-hour window** plus a weekly cap
([docs](https://code.claude.com/docs/en/costs#claude-for-teams-and-enterprise): the
allowance "resets on a rolling five-hour window"). There are two accounts of how that
window is bounded, and they imply different schedules:

- **Anchored** — the window starts when you send the day's first message and runs five
  hours from there. The reset time moves with your behaviour.
- **Truly sliding** — usage from more than five hours ago ages out continuously, and
  what matters is the peak load in any five-hour span.

The schedule above is built to be correct under **both**, so it does not depend on
settling that question:

At the **current** sizes, with 2B paused:

| | Anchored (day anchored by stage 0 at 07:12) | Sliding (worst five-hour span) |
| --- | --- | --- |
| Window 1 | 07:12–12:12 — stages 0, 4, 1, 2 → **3 Opus** | 10:22–15:22 — stage 2 only → **3 Opus** |
| Window 2 | 12:12–17:12 — nothing | |
| Window 3 | 17:12–22:12 — stage 3 → **7 Opus, alone** | 12:52 onward — stage 3 only → **7 Opus** |

At the **original** sizes the same schedule gave:

| | Anchored (day anchored by stage 0 at 07:12) | Sliding (worst five-hour span) |
| --- | --- | --- |
| Window 1 | 07:12–12:12 — stages 0, 4, 1, 2A → **5 Opus** | 10:22–15:22 — 2A + 2B → **10 Opus** |
| Window 2 | 12:12–17:12 — stage 2B → **5 Opus** | |
| Window 3 | 17:12–22:12 — stage 3 → **21 Opus, alone** | 12:52–17:52 onward — stage 3 only → **21 Opus** |

Two properties do the work:

- **Stage 0 at 07:12 anchors the day.** Under the anchored model, that single cheap
  firing decides where every boundary falls. It places stage 3 twenty minutes into a
  fresh window with four and a half hours of headroom.
- **Stage 2B ends more than five hours before stage 3 begins** (12:22 → 17:52). Under
  the sliding model, batch 2's ten researchers have aged out before the panel starts.

That is also why the deep dives were split into two batches *at the original size*. One
firing of ten deep researchers would be simpler to write and considerably worse to live
with. Three in waves of two is a different matter, which is why the split is off for now
— see "One research group" above.

### Do not let another Routine anchor the day first

Under the anchored model, **any earlier activity on the account moves every boundary**,
including a Routine for an unrelated project, and including a deliberate "wake up" ping.
A 03:00 wake-up, for instance, puts the boundaries at 08:00 / 13:00 / 18:00 — which
lands stage 3 (17:52) eight minutes before a window closes, so the most expensive stage
of the day straddles the boundary and can be cut off mid-panel.

If you keep wake-up Routines for other projects, schedule them **after 07:12**, or move
them to 07:05–07:10 so they anchor where stage 0 would anyway. Do not leave one in the
small hours.

Two such Routines exist on this account — "Wake up" (`0 4 * * 1-5`) and "wake - up 2"
(`5 8 * * *`, seventeen minutes before stage 2). Both appear paused as of 2026-08-13:
their `next_run_at` is in the past and neither has fired since 08-07/08-08. Leave them
paused, or delete them. Re-enabling "Wake up" would anchor the day at 04:00 and put the
boundaries at 09:00 / 14:00 / 19:00, which drops stage 2's fan-out 38 minutes before a
window close — the exact shape of failure this schedule was built to avoid.

The other consequence of the spacing: **each stage's output is on disk and pushed before
the next stage starts.** A session that dies mid-stage costs one stage, not the day.

### The cost of moving the deep dives earlier

Stage 2 at 10:22 (and 2B at 12:22 when it runs) is 04:22 New York time — well before
the open, so their spot prices and implied moves come from the prior close. That is a
real loss of freshness, bought deliberately for the usage separation.

It is mitigated, not ignored: stage 3 re-sources spot and implied move before building
the persona anchor packet, so the panel always sizes its move against live data. The
dossiers' own anchors carry their original timestamps, so the staleness is visible
rather than silently inherited.

## What actually went wrong, 2026-08-08 to 08-12

Five scheduled days, zero advice notes. The Routines were never the problem: all six
existed, were enabled, had the repo attached, pointed at the full-network environment,
and fired on time — `last_fired_at` confirms every one. Stage 0 published all five days
and stage 1 published four of five. **Stage 2 published nothing on any of them.**

Three distinct faults, which is why it looked intermittent:

1. **The fan-out was all-or-nothing.** Stage 2 launched its whole batch of five
   Opus/high researchers in parallel. Nothing reaches disk until the first agent
   returns, so a session killed during the fan-out leaves *no dossier and no log line*.
   On 08-08 the account hit its monthly spend limit and batch 2 died after roughly 2M
   input tokens having published nothing; 08-11 and 08-12 show the identical signature —
   a valid 10-name shortlist sitting ready, the Routine fired, and not one commit.
   Fixed by `deep_dive.wave_size` (waves of 2, publish after each wave) plus a
   published heartbeat *before* any researcher is spawned.

2. **The day's budget was never survivable.** 31 Opus/high subagents across stage 2 and
   stage 3, on a plan that had already tripped a monthly ceiling. The documented
   `degrade_order` existed but nothing ever applied it, because the stage that was
   supposed to apply it was the stage that kept dying. Applied by hand instead:
   shortlist 10 → 6, panel names 3 → 2. That is 31 Opus/high agents down to 20.

3. **A failed day published nothing, so the archive recorded the outage only in prose.**
   `validate_stage.py advice` required a non-empty `ranked_names`, so on a day with no
   ranking the only way to publish was to invent rows — which CLAUDE.md forbids. Stage 3
   correctly refused, four days running, and wrote a run-log entry instead of a
   deliverable. Advice notes now carry a `status` of `ok` / `no_names` / `blocked`, and
   a blocked day publishes an empty note with a stated reason.

A fourth, smaller fault made all of this harder to see: **`CLAUDE.md`'s schedule table
was stale**, still showing the pre-08-08 times (11:08 / 14:22 / 16:22 / 18:07) after
commit `27cdf99` retimed everything. Every fresh session reads that table first. It led
a stage 2 session to conclude the platform clock was "running ahead of Europe/Amsterdam
wall time", and stage 3 sessions to report stage 2 as due at 14:22 and 16:22 when it had
actually fired at 10:22 and 12:22. Sessions also wrote local timestamps into the run log
that were an hour or two wrong; run-log entries are UTC now, via `scripts/run_log.py`.

### The fourth fault: the Routines stopped firing altogether (08-14 to 08-17)

Everything above is about a stage that fires and fails. On 2026-08-14 and again on
2026-08-17 a different thing happened: **nothing fired at all.** No universe, no
shortlist, no run log, no directory — on `main` or on any other branch. Every earnings
Routine sat at `enabled: true` with the right cron, the right environment and the repo
attached, and simply did not run. `last_fired_at` on all six stayed at 2026-08-13 while
`next_run_at` rolled forward to 2026-08-18, skipping two trading days.

This is invisible from inside the repo, because a Routine that never fires leaves
nothing behind — not even the heartbeat, which is the whole point of the heartbeat's
absence being meaningful. **The archive cannot tell you about this failure; only
`list_triggers` can.** So when a day is missing, check in this order:

```
list_triggers                      # last_fired_at vs next_run_at, per Routine
```

- `last_fired_at` older than the missing day → the Routine never fired. Nothing in the
  repo will explain it; the cause is account- or platform-level.
- `last_fired_at` on the missing day, no `— STARTED` in the run log → it fired and died
  before reaching the skill.
- `— STARTED` but no dossiers → it fired and was killed during research.

The likeliest cause of an outright stop, given this account tripped a monthly spend
limit on 08-08, is an account-level usage or billing pause: the Routines stay enabled
and stop being dispatched. That is a claude.ai settings question
([usage](https://claude.ai/settings/usage)), not something any change in this repo can
fix. Verify it before spending time on the pipeline — five days of work went into
diagnosing a stage that fires and fails, and none of it helps on a day nothing fires.

Recovery is `fire_trigger` per stage, oldest first, and it works: firing stage 0 by hand
on 08-17 updated `last_fired_at` immediately, which also proves dispatch is healthy and
points the finger at scheduling rather than execution.

One trap while diagnosing this. `next_run_at` is the *next* scheduled fire, so once a
slot is missed it rolls forward and the Routine looks normally scheduled — the evidence
of the miss is only in `last_fired_at` being older than the day you are asking about.
Compare the two, never read either alone. And give a manually fired stage its real
running time before calling it dead: stage 0 takes four to five minutes to publish, and
a session spanning several days makes it very easy to misjudge how long ago you fired it.

### The heartbeat is the diagnostic

Nothing in this environment exposes a failed Routine session's transcript, so "the
session died" had to be inferred from absence. It should not have to be. Stage 2 now
publishes a `— STARTED` section naming the tickers and the plan before it spends
anything, so from here on the archive distinguishes:

- no `— STARTED` section → the Routine did not fire, or died before reaching the skill
- `— STARTED` with no dossiers → it fired and was killed during research (usage limit)
- `— STARTED` plus a `— HALTED` section → it detected the failure and stopped cleanly

### If you hit limits anyway

Turn these knobs in `config/pipeline.yaml`, in this order. Everything above step 3 is
already applied — the remaining headroom is what is left:

1. ~~`panel.names: 3` → `2`~~ — **applied 2026-08-13**. Removes 7 Opus/high agents.
2. ~~`triage.shortlist_size: 10` → `6`~~ — **applied 2026-08-13**. Removes 4 deep
   researchers.
3. ~~`panel.names: 2` → `1`~~ — **applied 2026-08-28**. Removes another 7.
4. ~~`triage.shortlist_size: 6` → `3`, `deep_dive.batches: 2` → `1`~~ — **applied
   2026-08-28**. Removes 3 more researchers and one whole firing.
5. `deep_dive.wave_size: 2` → `1` — fully serial. Slowest, but the finest-grained
   recovery: a kill costs one dossier.
6. `triage.shortlist_size: 3` → `2`, then `1`. Below that stage 2 has no field to rank
   and the panel has no choice to make.
7. Pause stages 2 and 3 and keep 0, 1 and 4 running. You keep the daily universe,
   shortlist and ledger for a rounding error in tokens, and the archive stays
   continuous — which is what calibration needs.
8. `panel.personas` — leave this alone at any size. Cutting personas does not save much
   and it directly degrades the disparity measure that the whole calibration rests on.

Stage 3 also sheds scope on its own when the run log shows earlier stages ran long, and
records what it dropped in `degradations_applied`.

## Scaling back up

The current sizes are a floor chosen to guarantee a finished day, not a judgement that
three dossiers and one panel is the right amount of research. Widen **one step at a
time**, and only after **five consecutive weekdays complete cleanly** — every stage
published, `02-ranking.json` present, `04-advice.json` written, and no run-log section
carrying a `— HALTED` heading or a usage/spend limit. One good day is not evidence: the
pipeline had good days on 08-08 and 08-28 and failed everything in between.

| Step | Change in `config/pipeline.yaml` | Opus/high per day |
| --- | --- | --- |
| *(now)* | `shortlist_size: 3`, `batches: 1`, `panel.names: 1` | 10 |
| 1 | `panel.names: 1` → `2` | 17 |
| 2 | `shortlist_size: 3` → `4` | 18 |
| 3 | `shortlist_size: 4` → `6` **and** `batches: 1` → `2`, re-enabling the 2B Routine | 20 |
| 4 | `panel.names: 2` → `3` | 27 |
| 5 | `shortlist_size: 6` → `10` | 31 — the original shape |

Notes on the order:

- **Panel names before shortlist size.** A second panel adds far more to the deliverable
  than a fourth dossier does. The panel is what produces a call; extra dossiers only
  widen the ranked field behind it.
- **Re-split the deep dives at step 3, not before.** Above roughly five researchers a
  day, one firing is the failure mode the two-batch design exists to avoid. Setting
  `batches: 2` and re-enabling the paused 2B Routine go together — either one alone
  leaves half the shortlist unresearched, or six researchers in a single firing.
- **Raise `triage.skip_if_universe_at_or_below` with `shortlist_size`.** They are the
  same number for a reason: the skip path writes *every* eligible name to the shortlist,
  so leaving the threshold high while the shortlist is small hands stage 2 a list longer
  than its cap on any thin day.
- **When a step fails, go back one step and stay there for a week.** Record it in the
  run log so the next attempt does not rediscover it.

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
downstream will work either — fix it before letting stages 2 and 3 spend the day's
Opus/high subagents on output that cannot be saved.

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
without losing the archive, pause stages 2 and 3 and leave 0, 1 and 4 running:
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

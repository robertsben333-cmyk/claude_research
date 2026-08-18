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
| 08:38 | 1 · Triage | `earnings-triage` | ≤6 Sonnet/medium | low |
| 10:22 | 2A · Deep dive, batch 1 | `earnings-deep-dive` | 4 Opus/high (full dossiers) | **high** |
| 12:22 | 2B · Deep dive, batch 2 | `earnings-deep-dive` | 4 Opus/medium (focused dossiers) | moderate |
| 17:52 | 3 · Panel & advice | `earnings-panel-advice` | 14 Opus/high | **highest** |

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
| 2A | `22 8 * * 1-5` | `22 9 * * 1-5` |
| 2B | `22 10 * * 1-5` | `22 11 * * 1-5` |
| 3 | `52 15 * * 1-5` | `52 16 * * 1-5` |

Switching over is one `update_trigger` call per Routine changing `cron_expression`.
Nothing else moves. Ignoring the switch is not fatal either — every stage runs an hour
later than intended and stage 3 lands near 20:30, which still works.

None of the times sit on `:00` or `:30`. Those minutes are where every scheduled job on
the platform piles up.

## How the day is spaced, and why

The spacing is the usage-limit design, not a convenience. The pipeline's expensive work
is 22 Opus subagents, and 14 of them are stage 3 alone.

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

| | Anchored (day anchored by stage 0 at 07:12) | Sliding (worst five-hour span) |
| --- | --- | --- |
| Window 1 | 07:12–12:12 — stages 0, 4, 1, 2A → **4 Opus/high** | 10:22–15:22 — 2A + 2B → **4 high + 4 medium** |
| Window 2 | 12:12–17:12 — stage 2B → **4 Opus/medium** | |
| Window 3 | 17:12–22:12 — stage 3 → **14 Opus, alone** | 12:52–17:52 onward — stage 3 only → **14 Opus** |

Two properties do the work:

- **Stage 0 at 07:12 anchors the day.** Under the anchored model, that single cheap
  firing decides where every boundary falls. It places stage 3 twenty minutes into a
  fresh window with four and a half hours of headroom.
- **Stage 2B ends more than five hours before stage 3 begins** (12:22 → 17:52). Under
  the sliding model, batch 2's ten researchers have aged out before the panel starts.

That is also why the deep dives are split into two batches at all. One firing of eight
deep researchers would be simpler to write and considerably worse to live with.

### Do not let another Routine anchor the day first

Under the anchored model, **any earlier activity on the account moves every boundary**,
including a Routine for an unrelated project, and including a deliberate "wake up" ping.
A 03:00 wake-up, for instance, puts the boundaries at 08:00 / 13:00 / 18:00 — which
lands stage 3 (17:52) eight minutes before a window closes, so the most expensive stage
of the day straddles the boundary and can be cut off mid-panel.

If you keep wake-up Routines for other projects, schedule them **after 07:12**, or move
them to 07:05–07:10 so they anchor where stage 0 would anyway. Do not leave one in the
small hours.

The other consequence of the spacing: **each stage's output is on disk and pushed before
the next stage starts.** A session that dies mid-stage costs one stage, not the day.

### The cost of moving the deep dives earlier

Stage 2A at 10:22 and 2B at 12:22 are 04:22 and 06:22 New York time — both well before
the open, so their spot prices and implied moves come from the prior close. That is a
real loss of freshness, bought deliberately for the usage separation.

It is mitigated, not ignored: stage 3 re-sources spot and implied move before building
the persona anchor packet, so the panel always sizes its move against live data. The
dossiers' own anchors carry their original timestamps, so the staleness is visible
rather than silently inherited.

### If you hit limits anyway

The 2026-08 pass already spent the easy savings: shortlist 10 → 8, panel 3 names → 2,
batch 2 dropped from full to focused dossiers, and turn caps cut on every research and
persona agent (researcher 80 → 55, focused 40, personas 45 → 30). That took the day from
31 Opus/high subagents to 4 Opus/high + 4 Opus/medium + 14 Opus/high, and shortened what
each one writes. What is left, in order:

1. `panel.names: 2` → `1` — removes 7 Opus/high agents, still the single biggest saving,
   and still the one that costs the most output.
2. `triage.shortlist_size: 8` → `6` — removes one researcher from each batch.
3. `deep_dive.batch_depth: {1: focused, 2: focused}` — every dossier focused. Do this
   before cutting the shortlist further if you would rather keep breadth than depth.
4. `deep_dive.batches: 2` → `3` — same total cost, spread across three windows.
   Requires a third stage-2 Routine.
5. `panel.personas` — leave this alone. Cutting personas does not save much and it
   directly degrades the disparity measure that the whole calibration rests on.

Going the other way — if there is headroom — raise `panel.names` back to 3 before
restoring batch 2 to full depth. A third panelled name is worth more than a deeper
dossier on the shortlist's eighth-best name.

### What batch 2 gives up

The focused dossier covers the event, the anchors, the bar and the one metric,
positioning, and the reversal case. It skips full segment fundamentals, alt-data,
filing-language forensics and the macro/peer survey, and runs at `effort: medium` on the
same Opus model — research was never delegated to a cheaper model.

The bet is that the shortlist's bottom half rarely reaches the panel, and that when it
does, the panel works from Phase-0 anchors the focused dossier sources just as carefully.
`research_depth` is carried through `02-ranking.json`, `04-advice.json` and
`PREDICTIONS.csv` precisely so the bet is checkable: if focused names start showing
materially worse direction hit rates in `LEDGER.md`, that is the signal to put batch 2
back to full depth rather than to argue about it.

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
downstream will work either — fix it before letting stages 2 and 3 spend 22 Opus
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

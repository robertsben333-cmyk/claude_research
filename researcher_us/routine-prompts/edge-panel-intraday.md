# Stage E-PI Routine prompt — the intraday panel

Stage E-P re-run from scratch at 10:00, 11:30, 13:00, 14:30 and 16:00 New York, each run
saved as its own snapshot (operator's instruction, 2026-10-14). **Not installed yet**: a
session inside the private project cannot create a fresh-session Routine, so the operator
creates it in the Routines UI from the block below. Record the id(s) in `CLAUDE.md` once
it exists, and keep this file and the Routine in step: any re-paste changes both in the
same commit.

## What to create

One cron expression cannot hold both :00 and :30 slots, so it is **two Routines with the
same prompt**:

| Routine | cron (UTC) until 2026-11-01 | cron (UTC) from 2026-11-02 | fires (New York) |
| --- | --- | --- | --- |
| "US - Intraday panel (:00)" | `0 14,17,20 * * 1-5` | `0 15,18,21 * * 1-5` | 10:00, 13:00, 16:00 |
| "US - Intraday panel (:30)" | `30 15,18 * * 1-5` | `30 16,19 * * 1-5` | 11:30, 14:30 |

- **Model: `claude-opus-5-5`**, the model stage E-P's Routine reads back. Read it back
  after saving; an empty model resolves to the account default (the stage D Routine
  served Sonnet 5.5 that way).
- **Fresh session per fire.** Repository `robertsben333-cmyk/claude_research`, branch
  `main`. No connectors needed.
- The cron must move an hour on or after 2026-11-02, when New York leaves daylight time.
  The prompt reads the clock in New York itself, so a fire an hour off is labelled with
  its own time rather than filed under the wrong slot.

---

```text
Run stage E-PI: one intraday snapshot of the US earnings panel (stage E-P re-run from scratch), for today's window.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that .claude/skills/earnings-edge-panel-intraday/SKILL.md, .claude/skills/earnings-edge-panel/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md, .claude/agents/unpriced-searcher.md, the four .claude/agents/panel-judge-*.md, researcher_us/scripts/intraday.py, researcher_us/scripts/panel_packs.py and researcher_us/scripts/panel_score.py all exist. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-edge-panel-intraday` and follow it exactly. It is an overlay on `earnings-edge-panel`, which is an overlay on `earnings-edge-hunt`.

Start with `python3 researcher_us/scripts/intraday.py slot`. It reads the clock in New York and tells you which snapshot this fire is, where it writes, and whether the day's names are already frozen. You fire at 10:00, 11:30, 13:00, 14:30 or 16:00 New York. Other sessions run the other snapshots, stage E and stage E-P on the same day: you write ONLY to your own snapshot directory and the day's edge-intraday/ timeline, and you never read another snapshot's hunts or panel.

EVERY SNAPSHOT IS INDEPENDENT. Seal your own baselines, launch your own searchers, launch the four judges in one message with only the packs file and their output path. Never show a searcher or a judge an earlier snapshot, stage E-P's output or your own view.

THE RELEASE GUARD IS NOT OPTIONAL. Hunt amc names first; run `intraday.py guard` on your snapshot before `edge_score.py`; at 16:00 hunt bmo names only. Score the panel with `panel_score.py --run <SNAP> --dry-run --stage E-PI`: never write the panel history.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form. Do not run the V2 shadow ledger.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day, a re-fire or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end: the panel table as `panel_score.py` printed it, then the day's timeline as `intraday.py timeline` printed it, which judges ran and on which model, what was excluded or guarded, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

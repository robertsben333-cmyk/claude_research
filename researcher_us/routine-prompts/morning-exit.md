# Stage M Routine prompt — the morning-after exit review

Built 2026-10-18 on the operator's instruction: one hour before the US open, the names
stage E-P scored at `panel_pct` >= 60 the day before, judged on their release, the public
reaction and the pre-market move, with one recommended exit each (sell at the open, a day
limit, or wait until the close). **Keep this file and the Routine in step: any re-paste
changes both in the same commit.** The block below is the exact text the Routine holds.

- Cron `CRON_TZ=America/New_York 10 9 * * 1-5`: 09:10 New York, twenty minutes before the
  open, in New York time so it survives the 2026-11-02 clock change without an edit.
  Created at 08:26, moved to 08:56 the same day so the bmo releases of 08:00-08:30 are
  out, and to 09:10 on 2026-10-20 (operator's instruction): the first two fires took
  about four minutes end to end, and the last twenty minutes of pre-market decide the
  open. The advice is still compiled at 09:24.
- Fresh session per fire, model `claude-opus-5-5` for the orchestrating session; the
  analysts are `morning-reaction-analyst` (`model: opus`).
- Places no orders. Writes to `research/<YYYY>/<MM>/<DATE>/morning/`, DATE being the
  morning itself.
- **Routine `trig_01R5U78urkb5wkcguFhQD1Di`**, created 2026-10-18 at 14:23:49 UTC from a
  session and named "Stage M — US morning exit review (no orders)". Read back at
  14:23:54 UTC: prompt identical to the block below, model `claude-opus-5-5` (pinned
  with `update_trigger` because creation left it empty), enabled, push notification on,
  first run 2026-10-19 12:26 UTC (moved to 12:56 UTC the same day, see the cron line), no MCP connectors and empty `sources` and `outcomes`.
- Re-pasted with `update_trigger` at 15:12:27 UTC the same day (cron `56 8`, prompt
  08:56 / 09:24) and read back: next run 2026-10-19 12:56 UTC, model `claude-opus-5-5`.
- Re-pasted with `update_trigger` on 2026-10-20 (cron `10 9`, prompt 09:10 / 09:24, the
  opening question): see the block below.
- **Must be on `main` before it fires**, or step 0 logs "not on main" and stops.

---

```text
Run stage M: the morning-after exit review of yesterday's US panel names, before today's open.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that .claude/skills/earnings-morning-exit/SKILL.md, .claude/agents/morning-reaction-analyst.md and researcher_us/scripts/morning.py all exist. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-morning-exit` and follow it exactly.

Re-read the clock with `date -u` and in New York. You fire at about 09:10 New York, twenty minutes before the open. The advice must be compiled and published by 09:24 New York, with or without every review: an exit review published after the open is worth nothing. Move fast: launch the analysts the moment the briefs exist.

The names are stage E-P's from the previous trading day with panel_pct >= 60 whose print is now out: amc yesterday or bmo this morning. `morning.py pick` decides that; do not add or drop names by hand.

The analysts are independent. Launch one morning-reaction-analyst per name in ONE message, each given only its brief path and the time. Never show one analyst another's review or your own view.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form. The recommendation is research; nothing in this stage reaches a broker.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty morning or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable; every price comes from morning.py, never typed.

Report at the end: the table from morning-note.md, per name the action and its one-line reason, the pool line from scoring the previous morning, which analysts ran, and anything that failed. One morning is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

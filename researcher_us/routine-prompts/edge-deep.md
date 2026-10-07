# Stage D Routine prompt — three names a day, researched in depth

**NOT INSTALLED YET (merged to main 2026-10-07).** The operator asked for the Routine on
2026-10-07, and `create_trigger` refused to make a fresh-session Routine from a session
inside a private project ("create_new_session_on_fire is not supported for routines
created from a private project"), so it has to be created in the Routines UI. Create it as
a standalone Routine (a fresh session per fire, like stages J, EU, AU, CA, R and E-P), not
inside the project: a project Routine fires into one existing session, so every run would
share one growing context. Then record the trigger id, the read-back model and cron here
and in `CLAUDE.md`'s stage table, in the same commit.

- **Schedule: weekdays at 13:30 America/New_York.** In the UI pick that time zone, so it
  follows US daylight saving by itself. In a UTC cron it is `30 17 * * 1-5`, and **that
  must move to `30 18 * * 1-5` on or after 2026-11-02**, when 17:30 UTC becomes 12:30 ET.
- 13:30 New York is the operator's instruction (2026-10-07). Anchor on New York time,
  never on the cron string. That leaves two hours to the 15:30 ET research stop and 2.5 to the close: every
  name, amc tonight or bmo tomorrow, is researched and scored before today's 16:00 ET
  close. Today's six trial hunts took 10 to 30 minutes each; the universe, baselines and
  sweep come on top, so a slow sweep is the main risk to the deadline. The market is open,
  so the option chain the baseline reads is live. It fires after stage E (17:04 UTC) and
  E-P (17:06); the researchers never read their files.
- Pin the model to `claude-opus-5` (it reads back as `claude-opus-5-5`); an empty model
  resolves to the account default.
- Places no orders. Writes to `research/<YYYY>/<MM>/<DATE>/edge-deep/`.

---

```text
Run stage D: deep, one-by-one research on three US companies reporting in today's earnings window.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that .claude/skills/earnings-deep-research/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md, .claude/agents/deep-question-researcher.md, .claude/agents/edge-sweep.md, researcher_us/scripts/deep_pick.py and researcher_us/scripts/deep_compare.py all exist. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-deep-research` and follow it exactly. It is an overlay on `earnings-edge-hunt`: you run stage E's steps 0 to 2 into <RUN>/edge-deep/, draw three names with deep_pick.py, and launch one deep-question-researcher per name.

Re-read the clock with `date -u`. You fire at 13:30 New York (17:30 UTC in summer), after stage E (17:04 UTC) and E-P (17:06 UTC) have started. You write ONLY to <RUN>/edge-deep/ and you seal your own baselines. The researchers never see stage E's or E-P's files; you read those only at the very end, for the comparison table in the note, and only if they exist by then. Do not wait for them.

THE DRAW IS RANDOM AND IT STANDS. Never re-draw, never swap a name. Every researcher, amc and bmo alike, stops at 15:30 ET, and the run is scored before the 16:00 ET close. If you fire after 15:00 ET, publish that it was too late and stop.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status. Do not run the V2 shadow ledger.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end. FIRST, paste verbatim the output of `python3 scripts/score_report.py --run <RUN>/edge-deep --label "Stage D (deep)"`. Then, per name, the investment decision (action, conviction, reason, what would change it), the frozen key questions with our answer and confidence, p_up, abs_move_pct, impact_sum and the quick first read beside it, and the comparison with stage E and E-P where their files exist. Three names on one day are an anecdote. This is a forecasting exercise over public information, not investment advice.
```

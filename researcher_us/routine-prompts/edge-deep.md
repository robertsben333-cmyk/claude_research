# Stage D Routine prompt — three names a day, researched in depth

**NOT INSTALLED.** No Routine runs this yet; the operator decides when it goes live. When
it does, create it as a standalone Routine (a fresh session per fire, like stages J, EU,
AU, CA, R and E-P), not inside the project: a project Routine fires into one existing
session, so every run would share one growing context. Then record the trigger id, the
read-back model and cron here and in `CLAUDE.md`'s stage table, in the same commit.

- Proposed cron `0 14 * * 1-5` = 14:00 UTC = **10:00 New York**, half an hour into the
  session so the option chain the baseline reads is live. **Move it to `0 15 * * 1-5` on or
  after 2026-11-02**, when US daylight saving ends and 14:00 UTC becomes 09:00 ET, before
  the open. Earlier than stage E (17:04 UTC) on purpose: a deep hunt can take four hours
  and tonight's amc names must be finished before their 16:00 ET release. The realised
  move is scored from daily closes, so sealing the baseline earlier than stage E does not
  change what is measured.
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

Re-read the clock with `date -u`. You fire at 14:00 UTC, before stage E (17:04) and E-P (17:06). You write ONLY to <RUN>/edge-deep/ and you seal your own baselines. The researchers never see stage E's or E-P's files; you read those only at the very end, for the comparison table in the note, and only if they exist by then. Do not wait for them.

THE DRAW IS RANDOM AND IT STANDS. Never re-draw, never swap a name. An amc name's researcher stops at 15:45 ET.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status. Do not run the V2 shadow ledger.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end. FIRST, paste verbatim the output of `python3 scripts/score_report.py --run <RUN>/edge-deep --label "Stage D (deep)"`. Then, per name, the frozen key questions with our answer and confidence, p_up, abs_move_pct, impact_sum and the quick first read beside it, and the comparison with stage E and E-P where their files exist. Three names on one day are an anecdote. This is a forecasting exercise over public information, not investment advice.
```

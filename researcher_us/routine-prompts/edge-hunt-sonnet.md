# Stage E-S Routine prompt — stage E with Sonnet hunters

`trig_01QJzV84MhL3xnFwUjdzEvW7`, "Stage E-S — US edge hunt, Sonnet hunters (no orders)". Created 2026-10-01 at 10:59 UTC from a session, so `update_trigger` works on it. Model pinned and read back as `claude-opus-5-5`; it stores no MCP connectors and empty `sources`, like stages J, EU, AU and CA, so step 0 clones the repo itself. **Keep this file and
the Routine in step: any re-paste changes both in the same commit.** The block below is
the exact text the Routine holds.

- Cron `6 17 * * 1-5` = 17:06 UTC, two minutes after stage E's `4 17`, so both seal
  their baselines on the same afternoon quotes.
- Fresh session per fire. Routine model pinned to Opus (the orchestrator); the hunters
  it spawns are `unpriced-hunter-sonnet`, the sweep `edge-sweep` on Opus.
- Places no orders. Writes to `research/<YYYY>/<MM>/<DATE>/edge-sonnet/`.

---

```text
Run stage E-S: the US earnings edge hunt with Sonnet hunters, for today's window.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that .claude/skills/earnings-edge-hunt-sonnet/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md and .claude/agents/unpriced-hunter-sonnet.md all exist. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-edge-hunt-sonnet` and follow it exactly. It is an overlay on `earnings-edge-hunt`: you run stage E's skill step by step with the overrides it lists, and nothing else differs.

Re-read the clock with `date -u`. You fire at 17:06 UTC, 13:06 New York, two minutes after stage E. Stage E is running in another session at the same time and writes to <RUN>/edge/. You write ONLY to <RUN>/edge-sonnet/, you seal your own baselines, and you never read stage E's files except, at the very end, its edge-scores.json for the comparison line in the note.

THE ONLY VARIABLE IS THE HUNTER MODEL. Hunters are `unpriced-hunter-sonnet`. The sweep is `edge-sweep` on Opus. You, the orchestrator, are Opus. If you have to fall back to `general-purpose` for a hunter, pass model sonnet on the launch, or the run tests nothing.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status. Stage E trades the one paper account; a second book on it would stack exposure. Do not run the V2 shadow ledger either.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end: names in the window, how many the sweep confirmed, the ranked table with the key the scorer names, the overlap and Spearman rho against stage E's impact_sum if its file exists by then, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

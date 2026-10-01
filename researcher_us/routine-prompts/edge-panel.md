# Stage E-P Routine prompt — Opus 5.5 searchers and a four-model panel

`trig_01QJzV84MhL3xnFwUjdzEvW7`, the Routine that ran stage E-S, re-pointed to stage E-P.
Created 2026-10-01 at 10:59 UTC from a session, so `update_trigger` works on it. Model
pinned (reads back as `claude-opus-5-5`); no MCP connectors and empty `sources`, so step 0
clones the repo itself. **Keep this file and the Routine in step: any re-paste changes
both in the same commit.** The block below is the exact text the Routine holds.
`edge-hunt-sonnet.md` is the text it held before, kept as history.

- Cron `6 17 * * 1-5` = 17:06 UTC, two minutes after stage E, so both seal their baselines
  on the same afternoon quotes.
- Fresh session per fire. Searchers `unpriced-searcher` (Opus 5.5), sweep `edge-sweep`,
  judges `panel-judge-opus5/-opus55/-sonnet55/-fable51`, each pinned to a full model ID.
- Places no orders. Writes to `research/<YYYY>/<MM>/<DATE>/edge-panel/`.

---

```text
Run stage E-P: the US earnings edge hunt with Opus 5.5 searchers and a blind four-model judging panel, for today's window.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that .claude/skills/earnings-edge-panel/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md, .claude/agents/unpriced-searcher.md, the four .claude/agents/panel-judge-*.md, researcher_us/scripts/panel_packs.py and researcher_us/scripts/panel_score.py all exist. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-edge-panel` and follow it exactly. It is an overlay on `earnings-edge-hunt`: you run stage E's skill step by step with the overrides it lists, plus its step 5p, the panel.

Re-read the clock with `date -u`. You fire at 17:06 UTC, 13:06 New York, two minutes after stage E. Stage E is running in another session and writes to <RUN>/edge/. You write ONLY to <RUN>/edge-panel/, you seal your own baselines, and you never read stage E's files except, at the very end, its edge-scores.json for the comparison line in the note.

THE PANEL IS INDEPENDENT OR IT IS NOTHING. Launch the four judges in one message, give each only the packs file and its output path, and never show a judge the hunts, the searcher's scores, another judge's output or your own view. If a judge's pinned model is refused, use the fallback the skill names; Opus 5 has none, so run without it and say so.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status. Do not run the V2 shadow ledger either.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end: names in the window, how many the sweep confirmed, which judges ran and on which model, the panel table (selected names first), the overlap and Spearman rho against stage E's impact_sum if its file exists by then, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

# Stage E-P Routine prompt — Opus 5.5 searchers and a four-model panel

`trig_01QJzV84MhL3xnFwUjdzEvW7`, the Routine that ran stage E-S, re-pointed to stage E-P.
Created 2026-10-01 at 10:59 UTC from a session, so `update_trigger` works on it. Model
pinned (reads back as `claude-opus-5-5`); no MCP connectors and empty `sources`, so step 0
clones the repo itself. **Keep this file and the Routine in step: any re-paste changes
both in the same commit.** The block below is the exact text the Routine holds.
`edge-hunt-sonnet.md` is the text it held before, kept as history.

**Pasted 2026-10-01 at 20:10:11 UTC** (`updated_at`), renamed "Stage E-P — US edge hunt, Opus 5.5
searchers + four-model panel (no orders)". Read back: prompt identical to the block below,
model `claude-opus-5-5`, cron `6 17 * * 1-5`, enabled, next run 2026-10-02 17:06 UTC, a
populated repository source and an `outcomes` branch of `claude/upbeat-hopper` (which the
prompt's `EARNINGS_DATA_BRANCH=main` overrides for the data).

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

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status. Do not run the V2 shadow ledger either. DO run `edge_grounded_score.py --run <RUN>/edge-panel` before the first print: it only reads the ledger and writes V2 into your own directory.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end. FIRST, paste verbatim the output of `python3 scripts/score_report.py --run <RUN>/edge-panel --label "Stage E-P (searcher)"`, then the same command on <RUN>/edge with --label "Stage E" if stage E's files exist. Then the panel table as `panel_score.py` printed it (selected names first), which judges ran and on which model, names in the window, how many the sweep confirmed, the overlap and Spearman rho between stage E's impact_sum and the panel_score, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

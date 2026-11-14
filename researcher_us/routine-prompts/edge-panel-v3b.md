# Stage E-P v3b Routine prompt — the v3b searcher and judges, no orders

Created 2026-11-14 from a session on the operator's instruction ("create a routine like
E-P that doesn't trade, named ep v3b, and improve the searcher and judger based on this
analysis; the goal is to see if it predicts better than the current E-P"). The text is
stage E-PF's prompt with the skill, the searcher, the judges, the output directory and
the labels changed. Created by a session, so `update_trigger` works on it. **Keep this
file and the Routine in step: any re-paste changes both in the same commit.** The block
below is the exact text the Routine holds.

**Routine `trig_016YK3TQezvXuierckLwP9mj`**, created 2026-11-14 at 10:27:36 UTC and named
"Stage E-P v3b — US edge hunt, v3b searcher + v3b four-model panel (no orders)". Read back
at 10:27:40 UTC: prompt identical to the block below, model `claude-opus-5-5` (pinned with
`update_trigger` because creation left it empty), cron
`CRON_TZ=America/New_York 10 13 * * 1-5`, enabled, first run 2026-11-16 18:10 UTC, no MCP
connectors, empty `sources` and `outcomes`.

- Cron `CRON_TZ=America/New_York 10 13 * * 1-5` = 13:10 New York, four minutes after
  stage E-P (13:06) and two after stage E-PF (13:08), so all three seal their baselines
  on the same afternoon quotes.
- Fresh session per fire, model `claude-opus-5-5` for the orchestrating session, as
  stage E-P. Searchers `unpriced-searcher-v3b` (`claude-opus-5-5`), sweep `edge-sweep`,
  judges `panel-judge-v3b-opus5/-opus55/-sonnet55/-fable51`, each pinned to a full
  model ID. No MCP connectors; step 0 clones the repo.
- Places no orders. Writes to `research/<YYYY>/<MM>/<DATE>/edge-panel-v3b/`.
- **Must be on `main` before it fires**, or step 0 logs "not on main" and stops.

---

```text
Run stage E-P v3b: the US earnings edge hunt with the v3b searcher and the v3b blind four-model judging panel, for today's window. It places no orders.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that .claude/skills/earnings-edge-panel-v3b/SKILL.md, .claude/skills/earnings-edge-panel/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md, .claude/agents/unpriced-searcher-v3b.md, the four .claude/agents/panel-judge-v3b-*.md, config/panel-judge-v3b.md, researcher_us/analysis/panel-history-v3b.json, researcher_us/scripts/panel_packs.py and researcher_us/scripts/panel_score.py all exist. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-edge-panel-v3b` and follow it exactly. It is an overlay on `earnings-edge-panel`, which is itself an overlay on `earnings-edge-hunt`: you run stage E's skill step by step with stage E-P's overrides and its step 5p, the panel, and then the stage E-P v3b overrides on top.

Re-read the clock with `date -u`. You fire at 13:10 New York, four minutes after stage E-P and two after stage E-PF. Both are running in other sessions and write to <RUN>/edge-panel/ and <RUN>/edge-panel-fable/. You write ONLY to <RUN>/edge-panel-v3b/, you seal your own baselines, and you never read their files except, at the very end, stage E-P's score file for the comparison block in the note.

THE SEARCHER IS unpriced-searcher-v3b OR THIS STAGE DID NOT RUN. If it is not found, use the fallback the skill names, with the v3b body pasted in. Check every hunt for the expectations and next_guide blocks and an evidence_type on its items, as the skill says.

THE PANEL IS INDEPENDENT OR IT IS NOTHING. Launch the four panel-judge-v3b-* judges in one message, give each only the packs file and its output path, and never show a judge the hunts, the searcher's scores, another judge's output or your own view. If a judge's pinned model is refused, use the fallback the skill names; Opus 5 has none, so run without it and say so. Score the panel with the two panel_score.py calls in the skill: first --dry-run on stage E-P's scale into edge-scores-panel-epscale.json, then --history researcher_us/analysis/panel-history-v3b.json. Never write stage E-P's panel history.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status, not flatten. Do not run the V2 shadow ledger either. DO run `edge_grounded_score.py --run <RUN>/edge-panel-v3b` before the first print: it only reads the ledger and writes V2 into your own directory.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end. FIRST, paste verbatim the output of `python3 scripts/score_report.py --run <RUN>/edge-panel-v3b --label "Stage E-P v3b (searcher)"`, then the same command on <RUN>/edge-panel with --label "Stage E-P (searcher)" if stage E-P's files exist. Then the panel table as the second panel_score.py call printed it (selected names first), which judges ran and on which model, names in the window, how many the sweep confirmed, how many hunts carried the v3b fields, the overlap of the selected names with stage E-P's and the Spearman rho between the two panel_pct_signed columns, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

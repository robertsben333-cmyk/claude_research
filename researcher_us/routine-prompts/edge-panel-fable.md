# Stage E-PF Routine prompt — Fable 5.1 searchers and the four-model panel

Created 2026-10-14 from a session on the operator's instruction ("an exact copy from
US-panel, runs at approximately the same time, but uses Fable 5.1 as a searcher instead
of Opus"). The text is stage E-P's prompt (`edge-panel.md`) with the skill, the searcher,
the output directory and the labels changed, and nothing else. Created by a session, so
`update_trigger` works on it. **Keep this file and the Routine in step: any re-paste
changes both in the same commit.** The block below is the exact text the Routine holds.

**Routine `trig_018ZcJBitxYfubdnMET8wN8U`**, created 2026-10-14 at 11:36:55 UTC and named
"Stage E-PF — US edge hunt, Fable 5.1 searchers + four-model panel (no orders)". Read back
at 11:36:59 UTC: prompt identical to the block below, model `claude-opus-5-5` (pinned with
`update_trigger` because creation left it empty), cron `8 17 * * 1-5`, enabled, first run
2026-10-14 17:08 UTC, no MCP connectors, empty `sources` and `outcomes` (step 0 clones the
repo; the prompt's `EARNINGS_DATA_BRANCH=main` decides where the data lands).

- Cron `CRON_TZ=America/New_York 8 13 * * 1-5` since 2026-10-28 (was `8 17 * * 1-5` = 17:08 UTC), two minutes after stage E-P (`6 17`) and four after
  stage E, so all three seal their baselines on the same afternoon quotes.
- Fresh session per fire, model `claude-opus-5-5` for the orchestrating session, as
  stage E-P. Searchers `unpriced-searcher-fable` (`claude-fable-5-1`), sweep `edge-sweep`,
  judges `panel-judge-opus5/-opus55/-sonnet55/-fable51`, each pinned to a full model ID.
- Places no orders. Writes to `research/<YYYY>/<MM>/<DATE>/edge-panel-fable/`.

---

```text
Run stage E-PF: the US earnings edge hunt with Fable 5.1 searchers and the same blind four-model judging panel as stage E-P, for today's window.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that .claude/skills/earnings-edge-panel-fable/SKILL.md, .claude/skills/earnings-edge-panel/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md, .claude/agents/unpriced-searcher-fable.md, the four .claude/agents/panel-judge-*.md, researcher_us/scripts/panel_packs.py and researcher_us/scripts/panel_score.py all exist. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-edge-panel-fable` and follow it exactly. It is an overlay on `earnings-edge-panel`, which is itself an overlay on `earnings-edge-hunt`: you run stage E's skill step by step with stage E-P's overrides and its step 5p, the panel, and then the stage E-PF overrides on top.

Re-read the clock with `date -u`. You fire at 17:08 UTC, 13:08 New York, two minutes after stage E-P and four after stage E. Both are running in other sessions and write to <RUN>/edge-panel/ and <RUN>/edge/. You write ONLY to <RUN>/edge-panel-fable/, you seal your own baselines, and you never read their files except, at the very end, their score files for the comparison lines in the note.

THE SEARCHER IS FABLE 5.1 OR THIS STAGE DID NOT RUN. Launch `unpriced-searcher-fable`. If it is not found, use the fallback the skill names with model fable. Never substitute an Opus searcher; if Fable is refused, log it, publish and stop.

THE PANEL IS INDEPENDENT OR IT IS NOTHING. Launch the four judges in one message, give each only the packs file and its output path, and never show a judge the hunts, the searcher's scores, another judge's output or your own view. If a judge's pinned model is refused, use the fallback the skill names; Opus 5 has none, so run without it and say so. Score the panel with `panel_score.py --run <RUN>/edge-panel-fable --dry-run --stage E-PF`: never write stage E-P's panel history.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status. Do not run the V2 shadow ledger either. DO run `edge_grounded_score.py --run <RUN>/edge-panel-fable` before the first print: it only reads the ledger and writes V2 into your own directory.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end. FIRST, paste verbatim the output of `python3 scripts/score_report.py --run <RUN>/edge-panel-fable --label "Stage E-PF (Fable searcher)"`, then the same command on <RUN>/edge-panel with --label "Stage E-P (Opus searcher)" if stage E-P's files exist. Then the panel table as `panel_score.py` printed it (selected names first), which judges ran and on which model, which model the searchers ran on, names in the window, how many the sweep confirmed, the overlap of the selected names with stage E-P's and the Spearman rho between the two panel_pct_signed columns, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

# Stage E-P Routine prompt — Opus 5.5 searchers and a four-model panel

`trig_01QJzV84MhL3xnFwUjdzEvW7`, the Routine that ran stage E-S, re-pointed to stage E-P.
Created 2026-10-01 at 10:59 UTC from a session, so `update_trigger` works on it. Model
pinned (reads back as `claude-opus-5-5`); no MCP connectors and empty `sources`, so step 0
clones the repo itself. **Keep this file and the Routine in step: any re-paste changes
both in the same commit.** The block below is the exact text the Routine holds.
`edge-hunt-sonnet.md` is the text it held before, kept as history.

**Re-pasted 2026-10-19 at 19:42:24 UTC (`updated_at`, read back identical; operator's instruction): stage E-P now trades the Alpaca paper
account**, renamed "Stage E-P — US edge hunt, Opus 5.5 searchers + four-model panel
(trades Alpaca paper)". It sells whatever is held once the searchers finish (skill step 3s)
and buys the panel's book after the panel (step 6b, `execution.panel`). The keys are in
this Routine's environment only. Stage E's Routine is stopped, so this is the only stage
connected to the account.

**Pasted 2026-10-01 at 20:10:11 UTC** (`updated_at`), renamed "Stage E-P — US edge hunt, Opus 5.5
searchers + four-model panel (no orders)". Read back: prompt identical to the block below,
model `claude-opus-5-5`, cron `6 17 * * 1-5`, enabled, next run 2026-10-02 17:06 UTC, a
populated repository source and an `outcomes` branch of `claude/upbeat-hopper` (which the
prompt's `EARNINGS_DATA_BRANCH=main` overrides for the data).

- Cron `CRON_TZ=America/New_York 6 13 * * 1-5` since 2026-10-28 (was `6 17 * * 1-5` = 17:06 UTC), two minutes after stage E, so both seal their baselines
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
   Then verify that .claude/skills/earnings-edge-panel/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md, .claude/agents/unpriced-searcher.md, the four .claude/agents/panel-judge-*.md, researcher_us/scripts/panel_packs.py and researcher_us/scripts/panel_score.py all exist, and that `grep -q 'def select_panel' researcher_us/scripts/alpaca_trade.py` succeeds. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-edge-panel` and follow it exactly. It is an overlay on `earnings-edge-hunt`: you run stage E's skill step by step with the overrides it lists, plus its step 5p, the panel.

Re-read the clock with `date -u`. You fire at 17:06 UTC, 13:06 New York, two minutes after stage E. Stage E is running in another session and writes to <RUN>/edge/. You write ONLY to <RUN>/edge-panel/, you seal your own baselines, and you never read stage E's files except, at the very end, its edge-scores.json for the comparison line in the note.

THE PANEL IS INDEPENDENT OR IT IS NOTHING. Launch the four judges in one message, give each only the packs file and its output path, and never show a judge the hunts, the searcher's scores, another judge's output or your own view. If a judge's pinned model is refused, use the fallback the skill names; Opus 5 has none, so run without it and say so.

YOU TRADE THE ALPACA PAPER ACCOUNT, and only in the two steps the skill names. This replaces the "places no orders" rule this stage had until 2026-10-19; stage E's Routine is stopped, so you are the only stage connected to the account. (1) SELL, skill step 3s: as soon as every searcher has finished, before the panel packs, run `python3 researcher_us/scripts/alpaca_trade.py mode` and then `python3 researcher_us/scripts/alpaca_trade.py flatten --run <RUN>/edge-panel --submit`, which closes every position still held at market. (2) BUY, skill step 6b: after the note is published, run `python3 researcher_us/scripts/alpaca_trade.py plan --run <RUN>/edge-panel`, then `python3 researcher_us/scripts/alpaca_trade.py open --run <RUN>/edge-panel --submit --no-flatten`, then `status` on the same run. The book is panel_pct 80 or more with all four judges, weight panel_pct minus 60, at most 50% of equity a name; the script applies it, never size by hand. Write those commands exactly as given (python3 and the researcher_us/scripts/ path), never with --top, --min-pct or --allow-stale. The buy needs an open market: if the run reaches step 6b after 16:00 New York, `open` refuses; say so rather than forcing it. Never print a credential. Do not run the V2 shadow ledger. DO run `edge_grounded_score.py --run <RUN>/edge-panel` before the first print: it only reads the ledger and writes V2 into your own directory.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end. FIRST, paste verbatim the output of `python3 scripts/score_report.py --run <RUN>/edge-panel --label "Stage E-P (searcher)"`, then the same command on <RUN>/edge with --label "Stage E" if stage E's files exist. Then what step 3s sold and what step 6b bought (the plan table and the status output), then the panel table as `panel_score.py` printed it (selected names first), which judges ran and on which model, names in the window, how many the sweep confirmed, the overlap and Spearman rho between stage E's impact_sum and the panel_score, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

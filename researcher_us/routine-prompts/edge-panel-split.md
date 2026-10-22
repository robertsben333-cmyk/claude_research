# Stage E-PS Routine prompt — the split panel, one day's test

Four one-shot Routines created 2026-10-22 from a session on the operator's instruction
("ik wil even 4 test routines aanmaken, die ieder max 5 stocks beoordelen, en op de een of
andere manier communiceren onderling wie welk doet"). All four hold the SAME prompt, the
block below: none of them knows its shard until `panel_split.py claim` gives it one, so a
Routine that fails to fire costs a shard, never a wrong assignment.

- One-shot (`run_once_at`), 2026-10-22 at 18:00, 18:01, 18:02 and 18:03 UTC (14:00-14:03
  New York), fresh session per fire, model pinned to `claude-opus-5-5` for the
  orchestrator. They disable themselves after firing.
- `claim` holds each session until stage E-P has reached its buy (`alpaca-plan.json`) or
  14:30 ET, whichever is first, so the test cannot push the account into the usage limit
  before E-P's book is placed.
- Code and data on branch `claude/modest-davinci-mjddtu`, never `main`.
- Places no orders. Writes `research/<Y>/<M>/<DATE>/edge-split-<k>/` and `edge-split/`.

Created 2026-10-22 13:47-13:48 UTC and read back at 13:48 UTC: prompt identical to the
block below, model `claude-opus-5-5` (pinned with `update_trigger`, creation left it
empty), enabled, no MCP connectors, empty `sources` and `outcomes` (step 0 clones the
test branch).

| Routine | fires (UTC) |
| --- | --- |
| `trig_014cDcoeh22Q9HkB15RhakRT` "Stage E-PS test 1/4" | 2026-10-22 18:00 |
| `trig_01C8x9mEG9WDmMeSKtoYATKA` "Stage E-PS test 2/4" | 2026-10-22 18:01 |
| `trig_01QT81ouPyusTDRuB75g5uxL` "Stage E-PS test 3/4" | 2026-10-22 18:02 |
| `trig_01TFqFSPwXthRFeN3toYUyLs` "Stage E-PS test 4/4" | 2026-10-22 18:03 |

---

```text
Run stage E-PS, one shard of today's split-panel test: stage E-P's own names, at most five in this session, with Opus 5.5 searchers and the blind four-model panel. Three sibling sessions run the other shards at the same time; you agree with them who takes which names through `panel_split.py claim`, never by guessing.

0. GET THE TEST BRANCH. The code is on branch claude/modest-davinci-mjddtu, not on main.
   - If /home/user/claude_research/CLAUDE.md does not exist: add_repo with owner robertsben333-cmyk, repo claude_research, access push; then git clone --depth 1 -b claude/modest-davinci-mjddtu https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research; then register_repo_root on that directory.
   - If it exists: in /home/user/claude_research run git fetch origin claude/modest-davinci-mjddtu and git checkout -B claude/modest-davinci-mjddtu FETCH_HEAD.
   Then verify that .claude/skills/earnings-edge-panel-split/SKILL.md, .claude/skills/earnings-edge-panel/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md, .claude/agents/unpriced-searcher.md, the four .claude/agents/panel-judge-*.md, researcher_us/scripts/panel_split.py, researcher_us/scripts/panel_packs.py and researcher_us/scripts/panel_score.py all exist. If any is missing, say so in your reply and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-edge-panel-split` and follow it exactly; if the skill is not listed, read .claude/skills/earnings-edge-panel-split/SKILL.md and follow that. It is an overlay on `earnings-edge-panel`, which is an overlay on `earnings-edge-hunt`.

Re-read the clock with `date -u`. You fire around 18:00 UTC, 14:00 New York. Start with `python3 researcher_us/scripts/panel_split.py claim`, with the Bash timeout set to 600000 ms: it waits for stage E-P to reach its buy (or 14:30 New York), then gives you your shard, its names and its directory. Exit 3 means run it again; exit 2 or 4 means log one line with `panel_split.py log` and stop, as the skill says.

THIS IS A TEST ON A BRANCH. Never run scripts/publish.sh or scripts/run_log.py directly: use `python3 researcher_us/scripts/panel_split.py publish "<message>"` and `python3 researcher_us/scripts/panel_split.py log --shard <k> --heading "<h>" --line "<l>"`, which write to claude/modest-davinci-mjddtu. Never push to main.

USE STAGE E-P'S NAMES, SWEEP AND BASELINES, NOT YOUR OWN. Do not build a universe, seal baselines or run edge-sweep: `claim` copies them into your shard directory. Never open stage E-P's hunts, packs, judge files or scores; only `panel_split.py summary` reads them, at the end.

ALL YOUR SEARCHERS IN ONE MESSAGE: one unpriced-searcher per name, at most five, amc names first. Run `intraday.py guard --snap <SHARD>` before `edge_score.py`. Record every searcher that says its search budget ran out.

THE PANEL IS INDEPENDENT OR IT IS NOTHING. Launch the four judges in one message, give each only the packs file and its output path, and never show a judge the hunts, the searchers' scores, another judge's output, stage E-P's panel or your own view. If a judge's pinned model is refused, use the fallback the skill names; Opus 5 has none, so run without it and say so. Score with `panel_score.py --run <SHARD> --dry-run --stage E-PS`: never write the panel history.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status. Do not run the V2 shadow ledger, edge_grounded_score.py or edge_context.py.

Publish something on every fire, even a stop: a fire that publishes nothing looks exactly like a Routine that never fired. `panel_split.py log` is itself a published commit.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end: your shard and its names, the panel table as `panel_score.py` printed it, the comparison table as `panel_split.py summary` printed it, which judges ran and on which model, what the guard moved, any searcher that ran out of search budget, claim-to-done minutes, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

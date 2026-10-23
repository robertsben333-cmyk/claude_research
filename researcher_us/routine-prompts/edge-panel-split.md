# Stage E-PS Routine prompt — the split panel, beside stage E-P

Four Routines, created 2026-10-22 from a session on the operator's instruction ("ik wil
even 4 test routines aanmaken, die ieder max 5 stocks beoordelen, en op de een of andere
manier communiceren onderling wie welk doet"), first as one-shots for that day. **On
2026-10-23 they were made daily ("zet die routines voorlopig standaard op") and moved to
fire with stage E-P ("laat ze gelijktijdig met e-p lopen zodat ze goed te vergelijken
zijn").** All four hold the SAME prompt, the block below: none of them knows its shard until
`panel_split.py claim` gives it one, so a Routine that fails to fire costs a shard, never a
wrong assignment.

- Cron in UTC like stage E-P's own (`6 17 * * 1-5`), so the five move together when New
  York leaves daylight time on 2026-11-02: `7 17`, `8 17`, `9 17` and `10 17`, weekdays.
  Fresh session per fire, model pinned to `claude-opus-5-5` for the orchestrator.
- `claim` holds each session until stage E-P's `sweep.json` is on main (about fifteen
  minutes after E-P fires), so the shards search while E-P's searchers do. Without a sweep
  by 14:30 ET it stops and logs.
- The session clones **main** and lays only the three overlay files over it from
  `claude/modest-davinci-mjddtu`, so the searcher, the judges, the scripts and the panel
  history are E-P's own that day. Output lands on that branch only, never on `main`.
- Places no orders. Writes `research/<Y>/<M>/<DATE>/edge-split-<k>/` and `edge-split/`.

Updated 2026-10-23 and read back: see the table below and `CLAUDE.md`'s stage table.

| Routine | fires (UTC, weekdays) |
| --- | --- |
| `trig_014cDcoeh22Q9HkB15RhakRT` "Stage E-PS 1/4" | 17:07 |
| `trig_01C8x9mEG9WDmMeSKtoYATKA` "Stage E-PS 2/4" | 17:08 |
| `trig_01QT81ouPyusTDRuB75g5uxL` "Stage E-PS 3/4" | 17:09 |
| `trig_01TFqFSPwXthRFeN3toYUyLs` "Stage E-PS 4/4" | 17:10 |

---

```text
Run stage E-PS, one shard of today's split panel: stage E-P's own names, at most five in this session, searched and judged while stage E-P runs them, with Opus 5.5 searchers and the blind four-model panel. Three sibling sessions run the other shards; you agree with them who takes which names through `panel_split.py claim`, never by guessing.

0. GET MAIN, THEN LAY THIS STAGE'S FILES OVER IT. Stage E-P runs on main and so do you; only this stage's own three files come from branch claude/modest-davinci-mjddtu, so your searcher, judges, scripts and panel history are exactly stage E-P's today.
   - If /home/user/claude_research/CLAUDE.md does not exist: add_repo with owner robertsben333-cmyk, repo claude_research, access push; then git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research.
   - Then, in /home/user/claude_research, run exactly: git fetch -q --depth 1 origin claude/modest-davinci-mjddtu && for f in .claude/skills/earnings-edge-panel-split/SKILL.md researcher_us/scripts/panel_split.py config/edge-panel-split.yaml; do mkdir -p "$(dirname "$f")" && git show FETCH_HEAD:"$f" > "$f"; done
   - If you cloned in the first step, call register_repo_root on /home/user/claude_research.
   Then verify that those three files, .claude/skills/earnings-edge-panel/SKILL.md, .claude/skills/earnings-edge-hunt/SKILL.md, .claude/agents/unpriced-searcher.md, the four .claude/agents/panel-judge-*.md, researcher_us/scripts/panel_packs.py, researcher_us/scripts/panel_score.py and researcher_us/scripts/intraday.py all exist. If any is missing, say so in your reply and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-edge-panel-split` and follow it exactly; if the skill is not listed, read .claude/skills/earnings-edge-panel-split/SKILL.md and follow that. It is an overlay on `earnings-edge-panel`, which is an overlay on `earnings-edge-hunt`.

Re-read the clock with `date -u`. You fire at 17:07 to 17:10 UTC, one to four minutes after stage E-P (17:06 UTC). Start with `python3 researcher_us/scripts/panel_split.py claim`, with the Bash timeout set to 600000 ms: it waits until stage E-P's sweep is on main, then gives you your shard, its names and its directory. Exit 3 means run it again; exit 2 or 4 means log one line with `panel_split.py log` and stop, as the skill says.

YOUR CHECKOUT IS MAIN AND YOU NEVER COMMIT TO IT. Never run scripts/publish.sh or scripts/run_log.py: publish.sh would push your shard to main and run_log.py would write into stage E-P's day log. Use `python3 researcher_us/scripts/panel_split.py publish --shard <k> "<message>"`, `python3 researcher_us/scripts/panel_split.py log --shard <k> --heading "<h>" --line "<l>"` and `python3 researcher_us/scripts/panel_split.py stamp --shard <k> --orchestrator-model "<model>"`, which write to claude/modest-davinci-mjddtu only. Never git commit, never git push yourself.

USE STAGE E-P'S NAMES, SWEEP AND BASELINES, NOT YOUR OWN. Do not build a universe, seal baselines or run edge-sweep: `claim` copies them into your shard directory. Never open stage E-P's hunts, packs, judge files or scores; only `panel_split.py summary` reads them, at the end.

ALL YOUR SEARCHERS IN ONE MESSAGE: one unpriced-searcher per name, at most five, amc names first. Run `intraday.py guard --snap <SHARD>` before `edge_score.py`. Record every searcher that says its search budget ran out.

THE PANEL IS INDEPENDENT OR IT IS NOTHING. Launch the four judges in one message, give each only the packs file and its output path, and never show a judge the hunts, the searchers' scores, another judge's output, stage E-P's panel or your own view. If a judge's pinned model is refused, use the fallback the skill names; Opus 5 has none, so run without it and say so. Score with `panel_score.py --run <SHARD> --dry-run --stage E-PS`: never write the panel history.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form - not mode, not plan, not status. Do not run the V2 shadow ledger, edge_grounded_score.py or edge_context.py.

Publish something on every fire, even a stop: a fire that publishes nothing looks exactly like a Routine that never fired. `panel_split.py log` is itself a published commit.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end: your shard and its names, the panel table as `panel_score.py` printed it, the comparison table as `panel_split.py summary` printed it, which judges ran and on which model, what the guard moved, any searcher that ran out of search budget, claim-to-done minutes, and anything that failed. One day is an anecdote. This is a forecasting exercise over public information, not investment advice.
```

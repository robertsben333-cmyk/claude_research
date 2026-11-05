# Stage H Routine prompt: the self-revising holistic researcher

**NOT YET CREATED.** A session inside the private project cannot create a fresh-session
Routine (`create_trigger` refuses it), so the operator creates it in the Routines UI with
these settings, then a session reads it back and records the id here and in `CLAUDE.md`.

| setting | value |
| --- | --- |
| Name | Stage H — US holistic researcher, self-revising (no orders) |
| Schedule | weekdays 14:15 **America/New_York**; as a cron `CRON_TZ=America/New_York 15 14 * * 1-5` |
| Model | Opus 5.5 (`claude-opus-5-5`); read it back, an empty model resolves to the account default |
| Session | a fresh session per fire |
| Environment | "full env" (full network access), like every research Routine on this account |
| Repository | `robertsben333-cmyk/claude_research`, branch `main` (step 0 clones it if absent) |
| Connectors | none needed |

Why 14:15 New York: stage E-P fires at 13:06 and its panel was done between 13:51 and
14:04 ET on 2026-10-29 to 11-04, so stage H starts after it and their subagents do not
compete for the same session limits (the 2026-10-21 E-P run lost eight judges to HTTP 429
when too much ran at once). It leaves 80 minutes to the 15:35 ET research stop and the
recommendations land before the 16:00 close, which is the entry. Must be on `main` before
it fires, or step 0 logs "not on main" and stops.

---

```text
Run stage H: the self-revising holistic US earnings researcher, for today's window.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that .claude/skills/earnings-holistic-research/SKILL.md, .claude/agents/holistic-researcher.md, .claude/agents/holistic-reflector.md, researcher_holistic/scripts/holistic.py, researcher_holistic/playbook/current.md and researcher_holistic/playbook/control.md all exist, and that `python3 researcher_holistic/scripts/holistic.py status` runs. If any is missing, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Read CLAUDE.md, then invoke the skill `earnings-holistic-research` and follow it exactly.

Re-read the clock with `date -u`. You fire at 14:15 New York, after stage E-P (13:06 New York) has sealed its baselines, run its sweep and normally finished its panel. You use E-P's sweep and sealed baselines only to choose the names; you never read E-P's hunts, scores or panel until the very end, for the comparison table. If it is past 15:00 New York, do not research: run only the learning step (resolve, evaluate, and the reflector if the gate is open) and publish.

THE RESEARCHERS ARE BLIND. Give each holistic-researcher only the brief that `holistic.py brief` prints for it. Never tell a researcher which arm it is on, never show it another researcher's file, E-P's files or your own view. Launch each name's two arms in the same wave, at most eight launches per turn.

THE PLAYBOOK CHANGES ONLY THROUGH THE SCRIPT. Never edit anything under researcher_holistic/playbook/ by hand, never re-run the reflector to get a different answer, and never repair a proposal the script rejected. The frozen control never changes.

YOU PLACE NO ORDERS. Do not run alpaca_trade.py in any form. Do not run the V2 shadow ledger.

export EARNINGS_DATA_BRANCH=main before every scripts/publish.sh, and after the last one run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there. The recommendations must be published before 16:00 New York. Publish something on every fire, even an empty day or a failure: a fire that publishes nothing looks exactly like a Routine that never fired.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable.

Report at the end: the recommendations (ticker, action, confidence, reason, what would flip it), every name's p_up on one line, the comparison with E-P on the same names, and the learning step: the gate numbers, the reflector's decision and diagnosis, and the playbook version tomorrow's run will use. One day is an anecdote; judge a playbook version only on its own resolved names. This is a forecasting exercise over public information, not investment advice.
```

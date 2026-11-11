# Stage E-P amc exit Routine prompt: sell the amc legs at the open

Built 2026-11-10 on the operator's instruction ("onze alpaca trades die amc zijn bij
opening van de markt verkocht"). Until then stage E-P sold its amc legs only at its own
step 3s flatten, about 13:40 ET the day after entry (fills 2026-11-04 to 11-09), while
the scorebord prices them at the open. "Close AMC" on the other account fires every
morning but scans only `research/*/*/*/edge`, so it never saw an E-P leg.

**Keep this file and the Routine in step: any re-paste changes both in the same commit.**
The block below is the exact text the Routine holds.

- Cron `CRON_TZ=America/New_York 0 9 * * 1-5`: 09:00 New York, before the open. The
  amc leg goes in as a market DAY order, which Alpaca accepts in the pre-market and
  routes at the open (`opg` needs the Elite Smart Router and is refused 09:28-19:00 ET,
  which is also why the exit cannot be placed by E-P itself at entry). A fire that
  starts late, after 09:30, still works: the same order then fills at once.
- Fresh session per fire, model `claude-opus-5-5`, environment "with alpaca" (the Alpaca
  keys are there; "full env" has none). No subagents, a few minutes end to end.
- The bmo legs are NOT this Routine's: `close` defers a `market` placement while the
  market is closed, so they stay for E-P's own run.
- **Safety net:** E-P's step 3s flatten still sells everything held, so a missed fire
  costs the open and nothing more.
- Every `alpaca_trade.py` call is written exactly as
  `python3 researcher_us/scripts/alpaca_trade.py ...`, the form the allow rule in
  `.claude/settings.json` covers. Any other form (absolute path, `python`, an env-var
  prefix) is classified again and may be refused.
- **Routine: `trig_01EVjSnebMCTM29YxaYo4HER`**, created from a session on 2026-11-10 at
  20:59 UTC, model pinned and read back as `claude-opus-5-5`, prompt read back identical
  to the block below. It was created on "full env", which holds NO Alpaca keys (no
  environment variables at all); the keys are in "with alpaca"
  (`env_015eAPLAkj3rueawDnePMzAR`). A session cannot change a Routine's environment, so
  the operator moves it to "with alpaca" in the Routines UI.
- **Must be on `main` before it fires**, or step 0 logs "not on main" and stops.

---

```text
Sell stage E-P's amc positions at today's US open. You place orders on the Alpaca account; nothing else.

0. GET THE REPO. If /home/user/claude_research/CLAUDE.md does not exist:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that researcher_us/scripts/alpaca_trade.py and researcher_us/routine-prompts/edge-panel-amc-exit.md exist and that `python3 researcher_us/scripts/alpaca_trade.py close --help` lists --today-only. If not, the work is not on main yet: append one line saying so to today's run log, publish, and stop. Do not improvise a substitute.

Re-read the clock with `date -u` and in New York. You fire at about 09:00 New York, before the 09:30 open. Work in the repo directory and write every alpaca_trade.py call exactly as below: `python3 researcher_us/scripts/alpaca_trade.py ...`, no absolute path, no env-var prefix.

1. GUARD: `python3 researcher_us/scripts/alpaca_trade.py mode --require-exit-tif opg`
   It exits 0 only when execution is enabled and the amc exit is aimed at the open. "matched on placement, not on the literal tif" is expected. On a non-zero exit do nothing further: paste its output into the run log, publish, stop.

2. `python3 researcher_us/scripts/alpaca_trade.py verify --scan 'research/*/*/*/edge-panel' --fix --submit`
   Re-reads earlier exits; re-sends at market any leg still held behind a dead order. Name every UNFILLED leg and every rescue.

3. `python3 researcher_us/scripts/alpaca_trade.py close --scan 'research/*/*/*/edge-panel' --today-only --submit --no-verify`
   Sends each amc leg whose exit date is today as a market DAY order, queued for the open, sized to what Alpaca holds. It refuses the bmo legs with "market placement, and the market is closed": that is correct, they belong to stage E-P's own run. It never touches an older leg (--today-only). Never drop --today-only and never pass --all or --now.

4. Append to today's run log with `python3 scripts/run_log.py --heading "Stage E-P amc exit — <YYYY-MM-DD>" --line "<what was sent, with tif and order id, and every refusal with its reason>"`, then `python3 scripts/update_index.py` and `scripts/publish.sh "stage E-P amc exit: <what> for <YYYY-MM-DD>"`. Publish even when nothing was due or the account was unreachable: a fire that publishes nothing looks exactly like a Routine that never fired.

export EARNINGS_DATA_BRANCH=main before scripts/publish.sh, and after it run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there.

Report at the end in a few lines: the legs sent, the legs refused and why, anything UNFILLED. Do not wait for fills; the order fills at 09:30 and stage E-P's run reads it back.
```

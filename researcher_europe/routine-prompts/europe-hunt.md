# The Routine prompt for stage EU

**The Routine exists: `trig_018WGfdq2fUm1ZqJhCGQ1wde`, "Stage EU — Europe researcher (10
markets)", cron `30 13 * * 1-5`, enabled, created 2026-09-19 at 08:24 UTC, prompt
re-pasted from this file by a session at 13:25 UTC when the stage went from three markets
to ten.** Check it against `list_triggers` rather than against this line.

It was **created by a session**, so `update_trigger` works on it — the same as stage J's
Routine and unlike stage E's. That corrects what this file said until 2026-09-19
("`create_trigger` is refused to agent sessions"), which was true on 2026-09-10 and is
not true now. **So the text below and the pasted prompt must be changed together, in the
same commit**, and this file is still the only thing that can be kept in step with it.

## What it was created with, and the hand-fire that did not settle it

**CORRECTED 2026-09-19.** This file said `create_trigger` returned empty `sources`,
`outcomes` and `allowed_tools`. That was true at creation and is **no longer true of the
stored Routine**: the `update_trigger` response of 13:25 UTC returns a populated
`session_request.config` carrying a `git_repository` source for
`robertsben333-cmyk/claude_research`, a full `allowed_tools` preset, and an **`outcomes`
branch of `claude/pensive-sagan`**. Somebody attached them from the Routines UI between
08:24 and now.

Two things follow and neither is cosmetic. A fired session **does** get a checkout, so
step 0's clone is now belt-and-braces rather than the only path — it is kept because it
costs one `ls` and it distinguishes "no repo" from "branch not merged", which are
different faults. And the Routine's declared outcome branch is **not `main`**, while the
prompt tells the run to `scripts/publish.sh` (which pushes to `main` by default). Those
two are not the same destination; nobody has yet observed which one a fired run's work
ends up on. **Check that on the next fire before trusting either.**

It was hand-fired on 2026-09-19 at 08:24 UTC (session `cse_01GPAvkwHzwzxuWdsscSUPUN`) to
find out whether a fired session arrives with a checkout. **That run published nothing** —
no commit, no branch, no run directory, on any remote — and ended idle after ten minutes
having spent 165k tokens, so it did substantial work and then left no trace. Its
transcript is not readable from another session, so the question was not answered.

**The prompt was therefore made to not depend on the answer** (updated 08:39 UTC): step 0
clones the repo if `CLAUDE.md` is absent and distinguishes "no repo" from "branch not
merged", which are different faults with different fixes. It also now requires the run to
publish *something* on every fire, even an empty day or a failure, because a fire that
publishes nothing is indistinguishable from a Routine that never fired.

It stores no MCP connectors, so its sessions run without `mcp__*` tools. That is expected
to be harmless: this stage needs WebSearch, WebFetch and Bash, which are core.

**It served on `claude-sonnet-5`,** while `config/pipeline.yaml`'s `europe_hunt` block asks
for `model: opus`. The config governs the hunters the run spawns; the Routine's own model
governs the session that orchestrates them. Whether that mismatch matters is unmeasured.

## When it fires, and why that is not the obvious time

**Europe reports before the open.** 339 of 379 measured UK results announcements landed
before 08:00 London, so this stage cannot seal a baseline on the morning of the print —
by then the release is out and the entry price no longer exists. It runs the day before,
against the next trading day's calendar.

The obvious slot would be after the Paris (17:35), Frankfurt (17:30) and London (16:30
UK) closes, so that every name's `close(D-1)` is final. **The operator chose two hours
before the close instead**, on 2026-09-19: `30 13 * * 1-5` is 15:30 Amsterdam in summer
and 14:30 in winter, and the run therefore happens while the European markets are still
trading.

What that costs and does not cost:

- **It does not corrupt the measurement.** `eu_resolve.py` computes the realised move
  from daily bars, `close(D-1) -> close(D)`, and never from the sealed spot.
- **It does make the sealed spot an intraday price**, not a close, along with
  `run_up_20d_pct`. The free control is struck at the same instant as the hunt, so the
  two stay comparable to each other; neither is struck at the close. Do not describe the
  sealed spot as a close in a note.
- **The cron is UTC and the exchanges are not**, so the gap to the close is two hours
  during CEST and three after the October change. Stage J has the same drift.

The run's date and the event date differ. **Re-read the clock with `date -u` and pass
`--date` explicitly** rather than letting a default decide, and say in the run log which
date was sealed for. A stage-2 session in this repo once concluded the platform clock was
"running ahead" from a stale table; do not give a future session that problem.

---

## The prompt, as pasted

The text below is what `trig_018WGfdq2fUm1ZqJhCGQ1wde` carries as of **2026-09-19, re-pasted from this file by a session** when the stage went from three markets to ten. It is quoted verbatim, so keep the two in step; nothing else will.

> You are running **stage EU**, the European researcher, for the next European session.
>
> ## Step 0 — make sure you have the repository
>
> This Routine was created with an empty `sources` list, so **do not assume a checkout exists.** Run this first, from your home directory:
>
> ```bash
> date -u
> if [ ! -f /home/user/claude_research/CLAUDE.md ]; then
>   git clone https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
> fi
> cd /home/user/claude_research && git fetch origin && git checkout main && git pull --ff-only origin main
> ls researcher_europe/scripts/eu_universe.py researcher_europe/scripts/eu_priced_in.py researcher_europe/scripts/eu_resolve.py researcher_europe/scripts/eu_market.py
> python3 scripts/run_paths.py --json
> ```
>
> If the clone fails, **stop, say so, and exit non-zero.** If the clone succeeds but any `researcher_europe/` script is missing, that is a different fault: the branch holding this stage has not been merged, which has happened three times in this repo and cost live runs every time. Say which of the two it is. Do not improvise around either. A failure that reports is worth more than a tidy no-op.
>
> Then read `CLAUDE.md` in full before doing anything else.
>
> ## The clock, and why the event date is not today
>
> **Re-read the clock: `date -u`.** The date you were told at startup may be stale. You fire at 13:30 UTC, which is 15:30 Amsterdam in summer and 14:30 in winter, because the cron is UTC and the European exchanges are not. Either way you are firing **while the European markets are still open**, roughly two hours before the 17:30 CET close, on the operator's instruction of 2026-09-19.
>
> That is deliberate and it has one consequence you must not get wrong: **`close(D-1)` is NOT final when you seal.** The baseline's spot and its `run_up_20d_pct` are intraday prices, not closes. Do not wait for a close, do not assume one, and do not describe the sealed spot as a close in the note. This does not corrupt the measurement: `eu_resolve.py` computes the realised move from daily bars, `close(D-1) -> close(D)`, never from the sealed spot. The free control is struck at the same instant as the hunt, so the two stay comparable.
>
> **The event date is not today.** Europe reports before the open: 339 of 379 measured UK results announcements landed before 08:00 London. You are sealing for the **next trading day on which the European markets are open**. Pass that date explicitly everywhere rather than letting a default decide, and say in the run log which date you sealed for. The ten markets do not share a holiday calendar, so "open" is per market and `universe.json` carries `market_closed` for each.
>
> ## The run
>
> Invoke the skill `researcher-europe-hunt` and follow it exactly. Do not improvise a different workflow.
>
> Things this stage gets wrong if nobody says them:
>
> - **It places no orders and reads no broker.** There is no `alpaca_trade.py` step here and there must not be one. Alpaca carries none of these ten venues.
> - The ranking key is whatever `edge-scores.json` reports in its own `ranking_key` field. Read it; do not carry a remembered contract into the run.
> - **TEN MARKETS SINCE 2026-09-19**: uk, de, fr, se, dk, no, fi, it, es, pl. The cap is **20** names. Read `config/pipeline.yaml`'s `europe_hunt` block rather than this line.
> - **Spawn one isolated subagent per name**, dispatched on each baseline's `submarket` field. The mapping is `MARKETS[<submarket>]["hunter"]` in `researcher_europe/scripts/eu_market.py`, so read it rather than recalling it: `unpriced-hunter-uk`, `-de`, `-fr`, `-it`, `-es`, `-pl`, and **`unpriced-hunter-nordic` for se/dk/no/fi — that one agent covers four markets, so tell it which of the four it is hunting.** Give each only its own ticker, its own window and the path to its own baseline. Running several names in one context destroys both controls the stage exists to measure and leaves names unhunted.
> - **ONE BILINGUAL PASS PER HUNTER SINCE 2026-09-22.** Each hunter searches English and its own local language together in a single pass. It no longer freezes an English-only `pre_local` draft: that control was retired on the operator's instruction because sequencing the two halves stopped them informing each other. Do not ask a hunter for `pre_local` and do not add it back to the contract. What each one emits instead is `language_note` — prose, one line per thing the local sources carried that the English ones did not. Nothing ranks it; quote it in the note where it is interesting. The `pre_lessons` freeze still runs and is still load-bearing. `eu_resolve.py`'s language-pass section will report 0 names, and that is the honest report of a retired control, not a hunter that forgot to freeze.
> - A two-name day is a normal outcome for this stage, not a failure. Hunt the names there are. **Do not lower the turnover floor to fill a wave.** The floor is $200k a day, set by the operator on 2026-09-19 to match the US and Japanese stages.
> - **Never fabricate a number.** Every company-specific figure carries a source URL or is marked `unavailable`/`null`, and a non-English source gets its original string quoted beside the translation.
> - **Leave a heartbeat before you spend anything**, publish after every wave, and append to `_run-log.md` rather than rewriting it. A run that publishes nothing is indistinguishable from a Routine that never fired, and those have completely different fixes.
>
> Known limits, so you do not rediscover them at cost. **They now differ by market** — `eu_market.CAPABILITY` is the measured table and the code reads it:
>
> - **Yahoo's European daily closes lag** one session for `.L` and about two for `.PA` and `.DE`, so a run cannot be resolved the next morning. Rows carry `last_bar_date` and `move_pending`.
> - **`event_occurred: false` is unreachable for Germany, Spain and Poland.** EQS-News has no whole-day query, so a German phantom cannot be caught; Spain and Poland have no reachable day archive at all.
> - **For Sweden, Denmark and Finland it is reachable only for about a week.** The Nasdaq Nordic feed has NO date query — its `fromDate` is accepted and silently ignored, returning today's rows for any date you ask for — so the archive is paged back roughly twelve days and no further. **A Nordic run must be resolved within about a week** or its rows resolve `null` for ever.
> - **Spain and Poland have no short register either**, so those names carry NO positioning anchor: their `priced_lean_pct` falls back to the run-up, which is also the free control this stage is measured against, so they cannot beat the benchmark with anything that uses it. Say in the note how many of the day's names came from those two.
> - **Denmark's register publishes from 0.1%** where everyone else publishes from 0.5%, so a Danish short ratio is not on the same scale as a Swedish one.
> - **The draw is random and the calendar is seasonal, so a day can be almost entirely one market** — 15 of 20 names were Swedish on 2026-10-22, because October is Sweden's month. Report `selection.market_concentration` before making any pooled statement about the day.
> - **`history.basis` is an ESTIMATED cadence for eight of the ten markets.** Only UK names (`observed_rns`) and Norwegian ones (`observed_newsweb`) carry real dated announcement history. A cadence prior is a scale, never evidence that a print happened on a date — TRT was ranked, traded and never reported on exactly that mistake.
>
> ## Publishing — to `main`, and pin it rather than trusting a default
>
> **The day's research goes on `main`.** `scripts/publish.sh` pushes to
> `${EARNINGS_DATA_BRANCH:-main}`, so the default is already right — but this Routine's
> stored `outcomes` branch is NOT `main`, and it is not even a fixed value: it read
> `claude/pensive-sagan` on 2026-09-19 and `claude/clever-gates` on 2026-09-22, and the
> stage CA and AU Routines carry their own different ones. It is assigned outside this
> repo and it rotates, so no prompt can name it correctly for long. So do not rely on
> the default: **pin the variable, and say in the run log where you pushed.**
>
> ```bash
> export EARNINGS_DATA_BRANCH=main
> python3 scripts/update_index.py
> scripts/publish.sh "stage EU: Europe ranking for <EVENT-DATE>"
> git log --oneline -1 origin/main    # confirm the work is on main, and say so in the run log
> ```
>
> If that last command does not show your commit, **say so explicitly in your reply** —
> a publish that went somewhere else is the one failure mode that looks exactly like
> success from inside the session.
>
> **You must publish something even if the day is empty or the run fails** — a heartbeat, a run-log line saying what happened, or the finished ranking. Ending a fire with nothing pushed leaves no evidence the Routine ran at all.

---

## A resolver Routine, if one is ever wanted

`eu_resolve.py` should run **after the close of the event date**, and not the next morning:
Yahoo's European daily closes lag one session for `.L` and about two for `.PA` and `.DE`,
so a same-day-after resolve reads `move_pending` and scores nothing. Two sessions later is
the earliest honest slot.

The confirmation sources expire at different rates, which is why a late resolve costs more
here than in the US stage:

- The **UK** source (Investegate) is queryable by date back to 1999 and will keep.
- **France** is `info-financiere.gouv.fr`, the AMF's own regulated-information flux:
  536,868 records back to 2012, and — with the Nordic feed added in 2026-09 — one of the
  few carrying the issuer's own filing category. It will keep. This corrects what this file said until 2026-09-19
  ("France has no readable confirmation source at all"), which was measured against
  Euronext's SPA and never against the regulator.
- **Germany** is the EQS-News *search*, which paginates back years per issuer but has **no
  whole-day query**. So a German name can be confirmed but a German phantom cannot be
  caught: `event_occurred: false` is unreachable for Germany by construction.
- **Norway** is Oslo Børs NewsWeb — a true day query, ticker-keyed, and it will keep.
- **Italy** is eMarket STORAGE, which keeps, behind a WAF that answers about 7 of 8.
- **Sweden, Denmark and Finland are the ones that expire**, and this is the reason a
  late resolve now costs more than it used to. The Nasdaq Nordic feed has **no date
  query at all** — its `fromDate` is accepted and ignored — so the archive is paged back
  ~200 rows and about two days at a time, roughly twelve days before it stops being
  cheap. Past that, a Nordic row resolves `null` for ever. **Resolve within a week.**
- **Spain and Poland have no archive**, so their rows always resolve `null`.

A guard for any such Routine should be an **exit status, not a config key read by eye** —
the lesson `researcher_us/routine-prompts/edge-execute.md` paid for twice. There is no
execution here to guard, so the honest guard is the file check above: if the scripts are
not in the tree, exit non-zero and let the Routine report a failure rather than a tidy
no-op.

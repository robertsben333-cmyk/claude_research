# The Routine prompt for stage EU

**The Routine exists: `trig_018WGfdq2fUm1ZqJhCGQ1wde`, "Stage EU — Europe researcher
(UK/FR/DE)", cron `30 13 * * 1-5`, enabled, created 2026-09-19 at 08:24 UTC.** Check it
against `list_triggers` rather than against this line.

It was **created by a session**, so `update_trigger` works on it — the same as stage J's
Routine and unlike stage E's. That corrects what this file said until 2026-09-19
("`create_trigger` is refused to agent sessions"), which was true on 2026-09-10 and is
not true now. **So the text below and the pasted prompt must be changed together, in the
same commit**, and this file is still the only thing that can be kept in step with it.

## What it was created with, and the one thing that is unverified

`create_trigger` returned **empty `sources`, `outcomes` and `allowed_tools`**, exactly as
stage J's did, and `update_trigger` cannot set those three fields. Stage J survives this
because its prompt clones the repo at step 0. **This prompt does not**, so if a fired
session arrives without a checked-out repo, the file check below exits non-zero and the
Routine reports a clean failure every morning while never running. It was hand-fired on
2026-09-19 at 08:24 UTC (session `cse_01GPAvkwHzwzxuWdsscSUPUN`) to settle exactly that.
**If that run reported no repo, add a clone step to the prompt and re-paste it.**

It also stores no MCP connectors, so its sessions run without `mcp__*` tools. That is
expected to be harmless: this stage needs WebSearch, WebFetch and Bash, which are core.

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

> You are running **stage EU**, the European researcher, for the next European session.
> The repo is `robertsben333-cmyk/claude_research`. Read `CLAUDE.md` in full before doing
> anything.
>
> **Re-read the clock first: run `date -u`.** The date you were told at startup may be
> stale. You fire at 13:30 UTC, which is 15:30 Amsterdam in summer and 14:30 in winter,
> because the cron is UTC and the European exchanges are not. Either way you are firing
> **while the European markets are still open**, roughly two hours before the 17:30 CET
> close, on the operator's instruction of 2026-09-19.
>
> That is deliberate and it has one consequence you must not get wrong: **`close(D-1)` is
> NOT final when you seal.** The baseline's spot and its `run_up_20d_pct` are intraday
> prices, not closes. Do not wait for a close, do not assume one, and do not describe the
> sealed spot as a close in the note. This does not corrupt the measurement:
> `eu_resolve.py` computes the realised move from daily bars, `close(D-1) -> close(D)`,
> never from the sealed spot. The free control is struck at the same instant as the hunt,
> so the two stay comparable.
>
> **The event date is not today.** Europe reports before the open: 339 of 379 measured UK
> results announcements landed before 08:00 London. You are sealing for the **next
> trading day on which the European markets are open**. Pass that date explicitly
> everywhere rather than letting a default decide, and say in the run log which date you
> sealed for.
>
> Before anything else, verify the tree has what this stage needs:
>
> ```bash
> ls researcher_europe/scripts/eu_universe.py researcher_europe/scripts/eu_priced_in.py researcher_europe/scripts/eu_resolve.py
> python3 scripts/run_paths.py --json
> ```
>
> If any of those is missing, **stop and say so in the run log, and exit non-zero.** It
> means the branch holding this stage has not been merged, which has happened three times
> in this repo and cost live runs every time. Do not improvise around it. A failure that
> reports is worth more than a tidy no-op.
>
> Then invoke the skill `researcher-europe-hunt` and follow it exactly. Do not improvise a
> different workflow.
>
> Things this stage gets wrong if nobody says them:
>
> - **It places no orders and reads no broker.** There is no `alpaca_trade.py` step here
>   and there must not be one. Alpaca does not carry LSE, Euronext or XETRA.
> - The ranking key is whatever `edge-scores.json` reports in its own `ranking_key` field.
>   Read it; do not carry a remembered contract into the run.
> - **Spawn one isolated subagent per name**, matching each baseline's `submarket` field:
>   `unpriced-hunter-uk`, `unpriced-hunter-fr` or `unpriced-hunter-de`. Give each only its
>   own ticker, its own window and the path to its own baseline. Running several names in
>   one context destroys both controls the stage exists to measure and leaves names
>   unhunted.
> - Each hunter runs its **English pass first**, freezes it as `pre_local`, then runs the
>   local pass and revises. The ordering is load-bearing; reversing it tests a different
>   question.
> - A two-name day is a normal outcome for this stage, not a failure. Hunt the names there
>   are. **Do not lower the turnover floor to fill a wave.** The floor is $200k a day, set
>   by the operator on 2026-09-19 to match the US and Japanese stages.
> - **Never fabricate a number.** Every company-specific figure carries a source URL or is
>   marked `unavailable`/`null`, and a non-English source gets its original string quoted
>   beside the translation.
> - Heartbeat before you spend anything, publish after every wave, and append to
>   `_run-log.md` rather than rewriting it.
>
> Known limits, so you do not rediscover them at cost:
> - **Yahoo's European daily closes lag** one session for `.L` and about two for `.PA` and
>   `.DE`, so a run cannot be resolved the next morning. Rows carry `last_bar_date` and
>   `move_pending`.
> - **`event_occurred: false` is unreachable for Germany**: EQS-News has no whole-day
>   query, so a German phantom cannot be caught. French and UK names can be confirmed and
>   killed.
>
> Finish by publishing:
>
> ```bash
> python3 scripts/update_index.py
> scripts/publish.sh "stage EU: Europe ranking for <EVENT-DATE>"
> ```

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
  536,868 records back to 2012, and the only one of the three carrying the issuer's own
  filing category. It will keep. This corrects what this file said until 2026-09-19
  ("France has no readable confirmation source at all"), which was measured against
  Euronext's SPA and never against the regulator.
- **Germany** is the EQS-News *search*, which paginates back years per issuer but has **no
  whole-day query**. So a German name can be confirmed but a German phantom cannot be
  caught: `event_occurred: false` is unreachable for Germany by construction.

A guard for any such Routine should be an **exit status, not a config key read by eye** —
the lesson `researcher_us/routine-prompts/edge-execute.md` paid for twice. There is no
execution here to guard, so the honest guard is the file check above: if the scripts are
not in the tree, exit non-zero and let the Routine report a failure rather than a tidy
no-op.

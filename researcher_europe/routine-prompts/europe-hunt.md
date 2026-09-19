# The Routine prompt for stage EU

**The Routine exists: `trig_018WGfdq2fUm1ZqJhCGQ1wde`, "Stage EU — Europe researcher
(UK/FR/DE)", cron `30 13 * * 1-5`, enabled, created 2026-09-19 at 08:24 UTC.** Check it
against `list_triggers` rather than against this line.

It was **created by a session**, so `update_trigger` works on it — the same as stage J's
Routine and unlike stage E's. That corrects what this file said until 2026-09-19
("`create_trigger` is refused to agent sessions"), which was true on 2026-09-10 and is
not true now. **So the text below and the pasted prompt must be changed together, in the
same commit**, and this file is still the only thing that can be kept in step with it.

## What it was created with, and the hand-fire that did not settle it

`create_trigger` returned **empty `sources`, `outcomes` and `allowed_tools`**, exactly as
stage J's did, and `update_trigger` cannot set those three fields. Stage J survives this
because its prompt clones the repo at step 0.

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

The text below is what `trig_018WGfdq2fUm1ZqJhCGQ1wde` carries as of 2026-09-19 08:39 UTC.
Keep the two in step; nothing else will.

> You are running **stage EU**, the European researcher, for the next European session.
>
> ## Step 0 — make sure you have the repository
>
> This Routine was created with an empty `sources` list, so **do not assume a checkout
> exists.** Run this first, from your home directory:
>
> ```bash
> date -u
> if [ ! -f /home/user/claude_research/CLAUDE.md ]; then
>   git clone https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
> fi
> cd /home/user/claude_research && git fetch origin && git checkout main && git pull --ff-only origin main
> ls researcher_europe/scripts/eu_universe.py researcher_europe/scripts/eu_priced_in.py researcher_europe/scripts/eu_resolve.py
> python3 scripts/run_paths.py --json
> ```
>
> If the clone fails, **stop, say so, and exit non-zero.** If the clone succeeds but any
> `researcher_europe/` script is missing, that is a different fault: the branch holding
> this stage has not been merged, which has happened three times in this repo and cost
> live runs every time. Say which of the two it is. Do not improvise around either. A
> failure that reports is worth more than a tidy no-op.
>
> Then read `CLAUDE.md` in full before doing anything else.
>
> ## The clock, and why the event date is not today
>
> **Re-read the clock: `date -u`.** You fire at 13:30 UTC, 15:30 Amsterdam in summer and
> 14:30 in winter, **while the European markets are still open**, roughly two hours before
> the 17:30 CET close, on the operator's instruction of 2026-09-19.
>
> **`close(D-1)` is NOT final when you seal.** The baseline's spot and its
> `run_up_20d_pct` are intraday prices. Do not wait for a close, do not assume one, and do
> not call the sealed spot a close in the note. This does not corrupt the measurement:
> `eu_resolve.py` takes the realised move from daily bars, `close(D-1) -> close(D)`, never
> from the sealed spot, and the free control is struck at the same instant as the hunt.
>
> **The event date is not today.** Europe reports before the open. You are sealing for the
> next trading day the European markets are open. Pass it explicitly and record it.
>
> ## The run
>
> Invoke `researcher-europe-hunt` and follow it exactly.
>
> - **No orders, no broker.** Alpaca does not carry LSE, Euronext or XETRA.
> - The ranking key is whatever `edge-scores.json`'s own `ranking_key` says.
> - **One isolated subagent per name**, matching the baseline's `submarket`:
>   `unpriced-hunter-uk`, `-fr` or `-de`. Several names in one context destroys both
>   controls and leaves names unhunted.
> - **English pass first**, frozen as `pre_local`, then the local pass revises.
> - A two-name day is normal. **Do not lower the $200k turnover floor to fill a wave.**
> - **Never fabricate a number**; non-English sources get the original string quoted.
> - Heartbeat before spending, publish after every wave, append to `_run-log.md`.
>
> Known limits: Yahoo's European closes lag one session for `.L` and ~two for `.PA`/`.DE`,
> so a run cannot be resolved the next morning; and `event_occurred: false` is unreachable
> for Germany, since EQS-News has no whole-day query.
>
> ## Publishing
>
> ```bash
> python3 scripts/update_index.py
> scripts/publish.sh "stage EU: Europe ranking for <EVENT-DATE>"
> ```
>
> **Publish something on every fire**, even an empty day or a failure. A fire that
> publishes nothing is indistinguishable from a Routine that never fired.

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

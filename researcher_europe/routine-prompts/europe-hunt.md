# The Routine prompt for stage EU

**No Routine exists for this stage and this session did not create one** — `create_trigger`
is refused to agent sessions in this repo, confirmed on 2026-09-10. This file is the text
to paste if and when a person decides to schedule it, and it is kept here for the same
reason `edge/routine-prompts/edge-hunt.md` is: **a session cannot edit a Routine's prompt,
so the file in the tree is the only thing that can be kept in step with it, and nothing
else will do it for you.**

If a Routine is ever created from this, the pasted text and this file must be changed
together, in the same commit, and the table in `CLAUDE.md` must gain a row checked against
`list_triggers` rather than against anybody's memory.

---

## When it would have to fire, and why that is not obvious

**Europe reports before the open.** 339 of 379 measured UK results announcements landed
before 08:00 London. So unlike stage E and stage J, this stage cannot seal a baseline on
the morning of the print — by the time it runs, the release is already out and the entry
price no longer exists.

It has to run **the evening before**, against the next day's calendar. A sensible slot is
**18:00–20:00 CET**, which is after the Paris (17:35) and Frankfurt (17:30) closes and
after the London close (16:30 UK), so every name's `close(D−1)` is final and sealable.
`eu_universe.py --date` defaults to the next calendar day for exactly this reason.

That also means the run's own date and the event date are different. **Re-read the clock
with `date -u` and pass `--date` explicitly** rather than letting a default decide, and
say in the run log which date you sealed for. A stage-2 session in this repo once
concluded the platform clock was "running ahead" from a stale table; do not give a future
session that problem.

---

## The prompt

> You are running **stage EU**, the European researcher, for the next European session.
>
> Re-read the clock first: run `date -u`. The date you were told at startup may be stale.
> The **event date** you are sealing for is the next trading day on which the European
> markets are open — not today. Pass it explicitly everywhere.
>
> Before anything else, verify the tree has what this stage needs:
>
> ```bash
> ls researcher_europe/scripts/eu_universe.py researcher_europe/scripts/eu_priced_in.py
> python3 scripts/run_paths.py --json
> ```
>
> If either file is missing, **stop and say so in the run log**. It means the branch that
> holds this stage has not been merged, which has happened three times in this repo and
> cost live runs each time. Do not improvise around it.
>
> Then invoke the skill `researcher-europe-hunt` and follow it exactly. Do not improvise a
> different workflow.
>
> Things this stage gets wrong if nobody says them:
>
> - **It places no orders and reads no broker.** There is no `alpaca_trade.py` step here
>   and there must not be one. Alpaca does not carry LSE, Euronext or XETRA.
> - The ranking key is whatever `edge-scores.json` reports in `ranking_key`. Read it; do
>   not carry a remembered contract into the run.
> - Spawn the hunter that matches each baseline's `submarket` field: `unpriced-hunter-uk`,
>   `unpriced-hunter-fr` or `unpriced-hunter-de`. Give each one only its own ticker, its
>   own window and the path to its own baseline.
> - A two-name day is a normal outcome for this stage, not a failure. Hunt the names there
>   are. **Do not lower the turnover floor to fill a wave.**
> - Heartbeat before you spend anything, publish after every wave, and append to
>   `_run-log.md` rather than rewriting it.
>
> Finish by publishing:
>
> ```bash
> python3 scripts/update_index.py
> scripts/publish.sh "stage EU: Europe ranking for <EVENT-DATE>"
> ```

---

## A resolver Routine, if one is ever wanted

`eu_resolve.py` should run **after the close of the event date**, so roughly 18:00 CET the
following day. It matters more here than in the US stage because the confirmation sources
expire at different rates:

- The **UK** source (Investegate) is queryable by date back to 1999 and will keep.
- The **German** source (EQS-News) is a non-paginating snapshot of the live feed. It
  confirms today and yesterday and nothing older. **A German run resolved late loses its
  confirmation**, exactly as a Japanese run does after TDnet's ~31 days.
- **France** has no readable confirmation source at all, so French names resolve
  `event_occurred: null` and never `false`.

A guard for any such Routine should be an **exit status, not a config key read by eye** —
the lesson `edge/routine-prompts/edge-execute.md` paid for twice. There is no execution
here to guard, so the honest guard is the file check above: if the scripts are not in the
tree, exit non-zero and let the Routine report a failure rather than a tidy no-op.

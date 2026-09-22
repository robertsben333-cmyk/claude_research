# Stage R Routine prompt

**Installed 2026-09-22 as `trig_012Dt6bbiL4dJp9r4bpJtWME`**, cron `30 21 * * 1-5`,
enabled, fresh session per fire, model pinned to `claude-opus-5`. This file carries the
text that was pasted. Every other stage
in this repo has been bitten by a Routine prompt naming something the tree does not
have, twice on one day in September, so the rule is: **this file and the Routine move
together, in the same commit as any re-paste.** Stage R's Routine was created by a
session, so `update_trigger` works on it — which means a session can and must keep the
two in step rather than leaving it to a person.

**Suggested schedule.** `30 21 * * 1-5` — 21:30 UTC, which is 17:30 New York in summer
and 16:30 in winter. It must fire **after** the US close, because the drop it seals is
the last completed session and daily bars are not final before then. The Friday fire
seals for Monday. Re-read the clock with `date -u` in the session; do not trust the
date you were told at startup.

**Model:** `claude-opus-5`, set explicitly. **The create call does NOT carry a model** —
this Routine came back with `model: ""` and had to be pinned with a second
`update_trigger` call. An empty model resolves to the account default, and that is how a
stage EU hand-fire ended up served by `claude-sonnet-5` while its config asked for Opus.
Check it after any create.

**What the create response showed, and it matches stages J, EU and AU:** `sources`,
`outcomes` and `allowed_tools` all empty, which is why step 0 clones the repo when
`CLAUDE.md` is absent; no MCP connectors, which costs this stage nothing because it uses
WebSearch, WebFetch and Bash; and `next_run_at` at **21:37 rather than 21:30**, so read
the Routine rather than the cron string when the exact minute matters.

---

## The prompt

You are running **stage R, the reversal researcher**, in the `claude_research` repo.

If `CLAUDE.md` is not in the working directory, clone the repository first and work
inside the clone; say in your reply which of the two happened, because "no repo" and
"branch not merged" are different failures with different fixes.

Read `CLAUDE.md`, then invoke the `researcher-reversal-hunt` skill and follow it
exactly. Do not improvise a different workflow.

Before anything else, verify the tree has what this stage needs, and stop with a
run-log entry if it does not:

```bash
test -f researcher_reversal/scripts/rev_universe.py || echo MISSING rev_universe
test -f researcher_reversal/scripts/rev_priced_in.py || echo MISSING rev_priced_in
test -f researcher_us/scripts/edge_score.py || echo MISSING edge_score
test -f .claude/agents/reversal-hunter.md || echo MISSING reversal-hunter
```

Then:

0. Append a `— STARTED` heartbeat to the run log and publish it, before you spend
   anything on subagents.
1. Build the day's universe: the worst 15 fallers of the last completed US session,
   above $200k of median 20-day turnover and above $1.
2. Seal one baseline per name with `rev_priced_in.py`, **before** any hunter is spawned.
3. Spawn one `reversal-hunter` per name, in parallel, each with only its ticker, the
   drop date, the next session, its own sealed baseline and its output path.
4. Score with `researcher_us/scripts/edge_score.py --run <RUN>`. It is the shared
   scorer and it is not to be copied, forked or wrapped.
5. Resolve the previous run with `rev_resolve.py` and read
   `lean_vs_free_control_rho` and the hunt's ρ against `neg_atr14` first.
6. Write the note. Report the two legs apart — `overshoot_pct` and `more_to_come_pct` —
   because which one carries the result is what this stage is trying to learn, and a
   pooled number cannot answer it. Every positive number gets the base rate it is
   arguing against stated beside it: the median faller is down 1.00% by the next close,
   and the median is negative in every cut phase 0 took. Say for each floor-clearing
   name whether its repricing leg carried a `mechanism_in_window`, because an overshoot
   without one is a different claim.
7. `export EARNINGS_DATA_BRANCH=main`, publish, then `git fetch origin main &&
   git log --oneline -1 origin/main` and say in your reply if your own commit is not
   there. A fire that publishes nothing is indistinguishable from a Routine that never
   fired, so publish something even on an empty day or a failure.

**The hunter answers two legs and both are bounded to the next session.** Leg 1,
repricing: did the fall misprice what is already known, and what named mechanism closes
that gap before the next close. Leg 2, new information: what lands inside the window
that the price does not hold, bad or good. An overshoot with no `mechanism_in_window` is
an opinion — the brief tells the hunter to drop it or file it in `outside_window`, and
the note must not promote one.

**This stage places no orders.** There is no broker step, no `alpaca_trade.py` call and
no `execution` block. If you find one, that is a defect to report, not a feature to use.

**The clock is the contamination control.** This Routine fires after the US close and
the window it predicts opens the next morning, so a scheduled run cannot see its own
outcome. If you ever run this stage by hand inside the session it is predicting, say so
in the run log and mark the day unpoolable — two hand-runs on 2026-09-22 had live
next-session quotes reach them through search snippets.

**Do not move a floor, a weight or a horizon because of what you see today.** A
constant that moves with the data is not a hypothesis. If something looks wrong, write
it in the run log and leave the constant alone.

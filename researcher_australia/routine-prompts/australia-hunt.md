# The Routine prompt for stage AU

Cron `30 6 * * 0-4` — **06:30 UTC**, which is **16:30 Sydney on AEST and 17:30 on
AEDT**, after the 16:00 close either way.

## Why Sunday to Thursday, and not Monday to Friday

**This stage seals for the NEXT Sydney session, because Australia reports before the
open.** Measured 2026-09-22 against the ASX announcement record, 67 of 74 results
announcements (91%) landed before the 10:00 Sydney open. So the window is
`close(D−1) → close(D)`, `au_universe.py --date` defaults to the next session, and the
fire that seals for Monday has to happen on **Sunday**.

| fire | Sydney local | seals for | last close |
| --- | --- | --- | --- |
| Sun 06:30 UTC | Sun 16:30/17:30 | Monday | Friday |
| Mon 06:30 UTC | Mon 16:30/17:30 | Tuesday | Monday |
| … | | | |
| Thu 06:30 UTC | Thu 16:30/17:30 | Friday | Thursday |

A Monday-to-Friday cron would put the Monday seal on the **previous Friday**, two
sessions stale, and waste the Friday fire on a three-day-old spot. Sunday to Thursday
gives every session a seal struck at the immediately preceding close. The hunt then has
about fifteen hours before the first release, which land from roughly 07:30 Sydney.

**Do not "fix" the cron to `1-5`.** It looks like a typo and it is not.

## Why 06:30 UTC and not later

It is after the close on both AEST and AEDT (06:00 and 05:00 UTC respectively), so the
sealed spot is a real close year-round, and the daylight-saving change on 2026-10-04
does not move it across the close. It also collides with nothing: stage J fires at 01:04
UTC, stage EU at 13:30, stage E at 17:04.

## This Routine can be edited from a session

Like stage J's and stage EU's and unlike stage E's, it was created by a session, so
`update_trigger` works on it. **That means this file and the pasted prompt must change
in the same commit.** Nothing enforces it; stage E's prompt drift cost two live things
on 2026-09-15 and the tell was always the same — the Routine naming something the tree
does not have.

`update_trigger` takes only `name`, `cron_expression`, `enabled`, `model`, `prompt` and
`run_once_at`. It cannot set `sources`, `outcomes` or `allowed_tools`; those are the
Routines UI's, and stage EU's `outcomes` branch of `claude/pensive-sagan` is the
outstanding example of why that matters. The prompt below therefore **pins
`EARNINGS_DATA_BRANCH=main` explicitly and verifies its own commit landed**, the same
belt-and-braces stage EU adopted on 2026-09-21. That makes the destination deterministic
whatever the outcome field says, and makes a wrong destination visible instead of silent.

## What it was created with

`trig_01Qy7FjBpjY4dEGcZsYGnpt3`, created 2026-09-22 at 08:09 UTC by a session, enabled,
first scheduled fire 2026-09-23 06:36 UTC. Pinned to `claude-opus-5`, because both other
research Routines were moved to Opus on 2026-09-19 and an empty `model` resolves to the
account default — the stage EU hand-fire served Sonnet that way.

It came back with **empty `sources`, empty `outcomes` and empty `allowed_tools`**, and a
warning that it stores no MCP connectors, exactly as stage J's and stage EU's did.
`update_trigger` cannot set any of those three. So a fired session may arrive without
`add_repo` and `register_repo_root`, which is why step 0 below tries a **plain
`git clone` first** and treats the connector path as the fallback rather than the
default. Stage J's prompt still has that ordering the other way round and has never been
fired to find out.

**The code reached `main` on 2026-09-22**, fast-forwarded from
`claude/jolly-brown-3dm2xo`, so the first scheduled fire has a tree to work in. Step 0's
file check stays: the tell for the two live things stage E lost on 2026-09-15 was always
a Routine naming something the tree does not have, and a check that has never failed is
not the same as a check that is unnecessary.

## What to check on the first fire

1. Did it get a checkout, or did step 0's clone do the work? Both are fine; knowing
   which is not optional.
2. Did anything publish? **A fire that publishes nothing is indistinguishable from a
   Routine that never fired.** The prompt requires a publish on every fire, including an
   empty day and a failure.
3. Which branch did the commit land on?

---

```text
Run stage AU, the Australia researcher, for the next Sydney session.

0. GET THE REPO, ON THE RIGHT BRANCH. The sandbox may start empty and this repository's DEFAULT branch is a stale feature branch.
   - If /home/user/claude_research/CLAUDE.md IS present, you were given a checkout: run `git fetch origin main && git checkout main && git pull origin main`.
   - If it is absent, try the plain clone FIRST, because this Routine stores no MCP connectors and add_repo may not exist in your toolset: `git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research`
   - Only if that clone fails, and only if the tools exist, fall back to add_repo (owner robertsben333-cmyk, repo claude_research, access push) followed by the clone and register_repo_root.
   Say in your reply which of those three paths you took.
   Then verify that researcher_australia/scripts/au_universe.py, researcher_australia/scripts/au_positioning.py, researcher_us/scripts/edge_score.py and .claude/skills/researcher-australia-hunt/SKILL.md all exist. If any is missing you are on the wrong branch or a merge is outstanding: STOP, publish a run-log line saying exactly which file is missing, and say so in your reply. Do not improvise a substitute workflow and do not run another market's skills.

Now invoke the skill `researcher-australia-hunt` and follow it exactly. Read CLAUDE.md first.

Re-read the clock with `date -u` rather than trusting any date you were told at startup. You fire at 06:30 UTC, which is 16:30 or 17:30 in Sydney depending on daylight time, and the ASX closed at 16:00. YOU ARE SEALING FOR TOMORROW'S SESSION, not for today's. au_universe.py defaults to the next ASX session and that default is correct; do not override it with today's date.

THIS STAGE PLACES NO ORDERS. There is no broker step, no alpaca_trade.py call and no execution block. Alpaca does not carry the ASX. If you find yourself reaching for one, stop - that is the US stage and it is not this one.

WHAT THIS STAGE PRODUCES: one signed number per company, so the session's names can be RANKED. No call, no threshold, no direction label anywhere in the output. The question under test is whether these companies can be ranked at all, and it is only answerable at every cut if nothing has been rounded into a bucket upstream.

THE OUTPUT CONTRACT LIVES IN THE SKILL, NOT IN THIS PROMPT. Which field is the ranking key and what the note must report are stated in .claude/skills/researcher-australia-hunt/SKILL.md and in edge-scores.json's own `ranking_key` field. Read them in the tree you actually cloned and follow those.

ONE ENGLISH PASS PER HUNTER, AND THAT IS DELIBERATE. Stages EU and J freeze a `pre_local` draft and run a second local-language or domestic-source pass. Australia does not: there is no Australian-language press the wires do not read, and stage EU's UK hunter - the degenerate case it already carries - says in its own definition that a UK zero is not evidence about language. unpriced-hunter-au has no pre_local field. Do not ask a hunter for one and do not add it to the contract. The pre_lessons freeze still runs, and researcher_australia/LESSONS.md is deliberately empty until a run resolves, so "nothing changed" is the correct answer there and not a fault.

IF THE UNIVERSE IS EMPTY, READ THE REASON RATHER THAN GUESSING IT. universe.json carries `market_open` and `market_open_basis`, and they distinguish three cases that look identical in `scheduled_today: 0` and mean different things:
  - market_open false, basis "weekend" or "ASX holiday (...)" - the exchange is shut. Nothing to wait for.
  - market_open null - the ASX index tape could not be read, so trading days, windows and the register lag are all unreliable. This is a container or network fault. DO NOT HUNT on that file; publish it, say so, and stop.
  - market_open true with zero names - a genuinely thin Australian session. Normal outside the February and August reporting seasons, which carry 427 and most of the year's other events between them. Publish the empty universe and stop.
Publish the empty universe, say which of the three it is in one line, and stop. Do not go looking for names another way.

FIVE THINGS SPECIFIC TO THIS MARKET THAT BELONG IN THE NOTE EVERY TIME:

  - THE POSITIONING ANCHOR IS THE BEST IN THE REPO AND IT IS LAGGED. There is no ASX option chain (measured: AAPL 22 expiries, BHP.AX zero), so `options` is all null and this stage runs in the regime archive/backtest/FINDINGS.md section 33 priced at rho=+0.073, p=0.45 over 104 events. In its place the baseline carries ASIC's aggregated daily short position, which - unlike the FCA, JPX, Bundesanzeiger and AMF registers - is NOT truncated at a 0.5% disclosure threshold: 430 of 755 rows on 2026-09-16 were below 0.5%, minimum 0.000000%. So an absent product is a measured zero and there is no anchor_covered arm. What it costs is the lag: ASIC publishes about four business days in arrears. Report positioning.lag_sessions in the note and never treat it as zero - on a name that has already run, four sessions is the whole move.
  - THE LEAN'S WEIGHTS ARE TOKYO'S PRIORS, UNMEASURED HERE. Report lean_vs_free_control_rho from the last resolved run if there is one. On the 2026-08-27 validation run it read 0.80 over 20 names, which is HIGHER than stage J's healthy 0.446-0.59: the run-up term dominates the lean whenever short interest is small, so Australia's lean is more entangled with its own benchmark than Tokyo's is. That is a known weakness, it is the first thing a resolved run should fix, and it must not be fixed by editing a constant until measurement says which way.
  - HALF THE ASX LODGES A CASH-FLOW REPORT, NOT A PROFIT RESULT. history.filer_type is `results` (Appendix 4D/4E), `quarterly_report_only` (Appendix 4C/5B under Listing Rule 4.7B - cash burn against runway, a completely different bar) or `none_found`. Report the mix. `none_found` on an issuer whose three years of archive read cleanly is a reason to doubt the print exists at all.
  - THE VENDOR DATE WAS SHIFTED AND THE HISTORY IS OBSERVED. 85% of Australian vendor rows sit one Sydney day later than the vendor says, because the vendor stamps the UTC instant; au_market.sydney_event_date() converts the instant rather than adding a constant, and every row carries event_date_basis. And unlike stage J, `history` is REAL ASX lodgement dates with real timestamps, so its dates may be cited as facts.
  - THE UNIVERSE IS CUT AND THE CUT IS RANDOM. Turnover floor, then a date-seeded draw if more than the cap survive. Report selection.method, eligible and hunted. Do not substitute your own judgement for the draw, and do not re-run the universe step hoping for a different sample. Also report how many names carried session_unresolved.

Work on the `main` branch and pin the destination explicitly: `export EARNINGS_DATA_BRANCH=main` before you call scripts/publish.sh. Publish the STARTED heartbeat before you spawn a single hunter, publish after each wave, and finish with `python3 scripts/update_index.py` then `scripts/publish.sh "stage AU: Australia ranking for <date>"`. Then run `git fetch origin main && git log --oneline -3 origin/main` and say in your reply whether your own commit is there. This session is ephemeral; anything not pushed is lost.

EVERY FIRE PUBLISHES SOMETHING, including an empty day, a shut exchange and a failure. A fire that publishes nothing is indistinguishable from a Routine that never fired, and this repo has already spent days on that ambiguity.

Reply with the funnel in one line (scheduled / eligible / hunted), the ranked table, the finding and URL driving the top and bottom name, the filer-type mix and the register lag, and one line on what the day does NOT establish.
```

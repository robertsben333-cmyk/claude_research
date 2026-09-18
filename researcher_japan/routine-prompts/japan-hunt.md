# Stage J Routine prompt — the Japan researcher

Cron `4 1 * * 1-5` — **01:04 UTC = 10:04 JST = 03:04 Amsterdam.**

**Tokyo closes more often than you think, and the Routine fires anyway.** Next week is
the worked example: 2026-09-21, 09-22 and 09-23 are 敬老の日, a 国民の休日 and 秋分の日,
so three consecutive scheduled fires land on a shut exchange. `jp_universe.py` now reads
the Cabinet Office's own 国民の祝日 list and writes `market_closed` into the universe
file, because an empty calendar otherwise has two causes that look identical and mean
opposite things — the exchange is shut (nothing to wait for) or the fiscal cohort's
sheet is not up yet (wait).

Why that hour: Tokyo trades 09:00–11:30 and 12:30–15:00 JST, and Japanese results land
overwhelmingly after the 15:00 close (386 of 456 `決算短信` on 2026-08-14, all 24 on
09-01). Firing at 10:04 JST puts the run an hour into the session, with live prices for
the sealed baseline and just under five hours before the first release. The US stage E
fires at 17:04 UTC, so the two never overlap and neither can starve the other.

**THE PROMPT IS EDITABLE FROM A SESSION — confirmed 2026-09-18 at 17:38 UTC**, when
`update_trigger` rewrote it and the Routine's `updated_at` moved. That is the one thing
stage E cannot do, and it means this file and the Routine can be kept in step by a
session rather than by hand. Keep doing it anyway: nothing enforces it.

**WHAT IS STILL UNVERIFIED, AND IT IS THE THING MOST LIKELY TO MAKE THIS A SILENT
NO-OP.** The Routine was created from a session on 2026-09-18
(`trig_0192kQeqhumBKpNGzzyQrS1H`) and came back with **empty `sources`, empty `outcomes`
and empty `allowed_tools`**, plus a warning that it stores no MCP connectors. The five stage 0–4 Routines all carry a
populated `sources` (the git repository), an `outcomes` branch and an explicit tool
list; this one carries none. Step 0 is written to clone the repo itself, exactly as
stage E's prompt does, so an empty `sources` may not matter — **but that path needs
`add_repo` and `register_repo_root`, which are connector tools this Routine may not
have.** `update_trigger` cannot set any of those fields, so a session cannot repair it.

Before trusting the first scheduled fire, do one of these:

1. Fire it once by hand (`fire_trigger`) and read what the session actually did. A run
   that cannot clone will say so at step 0 rather than producing a wrong ranking, which
   is the failure mode this prompt was written to force.
2. Or recreate the Routine from the claude.ai Routines UI, where the repository source
   and the tool list can be attached, and delete `trig_0192kQeqhumBKpNGzzyQrS1H`.

Do not assume it works because it exists and is enabled. A Routine that fires, fails
step 0 and reports a tidy no-op every morning is precisely the fault this repo has
already paid for twice.

Unlike stage E, this Routine **was created by an agent session**, so a later session can
update it with `update_trigger` and does not have to ask for a hand-paste. Keep this file
in step with it anyway — that discipline is what stage E's prompt drift cost.

---

```text
Run stage J, the Japan researcher, for today's Tokyo window.

0. GET THE REPO, ON THE RIGHT BRANCH. The sandbox starts empty and this repository's DEFAULT branch is a stale feature branch. Do exactly this:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that researcher_japan/scripts/jp_universe.py, researcher_japan/scripts/jp_positioning.py, researcher_us/scripts/edge_score.py and .claude/skills/researcher-japan-hunt/SKILL.md all exist. If any is missing you are on the wrong branch or a merge is outstanding: stop and say so. Do not improvise a substitute workflow and do not run the US stage's skills.

Now invoke the skill `researcher-japan-hunt` and follow it exactly. Read CLAUDE.md first.

Re-read the clock with `date -u` rather than trusting any date you were told at startup. You fire at 01:04 UTC, which is 10:04 in Tokyo and 03:04 in Amsterdam. The Tokyo close is 15:00 JST, five hours out, and essentially every release lands after it. That is your deadline for the note, not for an order: THIS STAGE PLACES NO ORDERS. There is no broker step, no alpaca_trade.py call and no execution block. If you find yourself reaching for one, stop - that is the US stage and it is not this one.

WHAT THIS STAGE PRODUCES: one signed number per company, so today's names can be RANKED. No call, no threshold, no direction label anywhere in the output. The question under test is whether these companies can be ranked at all, and it is only answerable at every cut if nothing has been rounded into a bucket upstream.

THE OUTPUT CONTRACT LIVES IN THE SKILL, NOT IN THIS PROMPT. Which field is the ranking key and what the note must report are stated in .claude/skills/researcher-japan-hunt/SKILL.md and in edge-scores.json's own `ranking_key` field. Read them in the tree you actually cloned and follow those.

IF THE UNIVERSE IS EMPTY, READ THE REASON RATHER THAN GUESSING IT. `universe.json` carries `market_closed`. If it is set, Tokyo is shut - a weekend, a 国民の祝日, or the 31 Dec to 3 Jan exchange holiday - and there is nothing to wait for. If it is null and `scheduled_today` is 0, the relevant fiscal cohort's sheet is most likely not published yet; report `calendar_sheets` and `calendar_as_of`. These two look identical in the output and have opposite meanings. Publish the empty universe, say which case it is in one line, and stop. Do not go looking for names another way.

FOUR THINGS SPECIFIC TO THIS MARKET THAT BELONG IN THE NOTE EVERY TIME:

  - There is no option anchor, and since 2026-09-18 it is SUBSTITUTED rather than merely disclosed. Japan has no liquid single-stock options, so `options` is all null. In its place the baseline carries `positioning`: JPX's daily disclosed short register (level, and whether shorts are building or covering), and 信用倍率, the margin long/short ratio. The baseline supplies its own `priced_lean_pct` and `anchor_quality` from these. What it bought, measured on the 2026-09-11 universe: the lean's rank correlation against the free control fell from 1.0 BY CONSTRUCTION to 0.446-0.59, and baseline_quality rose from a hard ceiling of 0.40 to 0.725. Report `lean_vs_free_control_rho` from the last resolved run if there is one: if it has climbed back toward 1.0 the positioning sources stopped resolving and the lean is the run-up alone again, which is invisible in the ranking itself. The weights behind those components are PRIORS with no Japanese measurement behind them; jp_resolve.py ranks each separately so measurement can replace them.
  - The universe is cut and the cut is random. Microcaps go on turnover, then if more than the cap survive, a random draw seeded by the date picks them. Report selection.method, eligible and hunted. Do not substitute your own judgement for the draw, and do not re-run the universe step hoping for a different sample.
  - `history` is an estimated cadence, not a record of dates. It is a scale for how much the name moves. Never cite one of its dates as a fact.
  - Daily price limits truncate the tail, so a large finding may be right and still not get paid in full.

Work on the `main` branch. Publish the STARTED heartbeat before you spawn a single hunter, publish after each wave, and finish with `python3 scripts/update_index.py` then `scripts/publish.sh "stage J: Japan ranking for <date>"`. This session is ephemeral; anything not pushed is lost.

Reply with the funnel in one line (scheduled / eligible / hunted), the ranked table, the finding and URL driving the top and bottom name, and one line on what the day does NOT establish.
```

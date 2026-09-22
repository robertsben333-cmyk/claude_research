# Stage CA Routine prompt — the Canada researcher

Proposed cron `30 18 * * 1-5` — **18:30 UTC = 14:30 Toronto = 20:30 Amsterdam.**

**THE HOUR IS LOAD-BEARING AND IT IS NOT NEGOTIABLE THE WAY THE OTHER STAGES' ARE.**
Toronto trades 09:30–16:00 ET. Outside that window the Montreal Exchange's option chain
returns bid and ask of zero on every strike, so `ca_priced_in.py` refuses to compute an
implied move and **every name falls to the register arm**. That is not a degraded run,
it is a different experiment: the whole reason this stage exists is that Canada can run
the option-anchored and anchor-less regimes inside one day's names, and a run sealed at
06:00 ET runs only one of them. 14:30 ET puts the seal ninety minutes before the close,
with live two-sided quotes, and before the after-close releases that most Canadian
issuers use.

It also does not collide with anything. Stage E fires at 17:04 UTC and needs its entry
margin; stage EU at 13:30; stage J at 01:04.

**The Routine exists: `trig_01Qv4Yyo6K8K3nNyGbiESeAv`, cron `30 18 * * 1-5`, enabled,
model `claude-opus-5`, created from a session on 2026-09-22 at 08:35 UTC.** It was
created by a session, so `update_trigger` works on it and this file and the Routine must
move in the same commit.

**IT STORES NO MCP CONNECTORS, AND THE CREATE CALL SAID SO IN WRITING.** Its `sources`,
`outcomes` and `allowed_tools` all came back empty, exactly as stage J's and stage EU's
did. Step 0 below clones the repo itself so an empty `sources` is survivable — **but
that path needs `add_repo` and `register_repo_root`, which are connector tools a fired
session may not have.** `update_trigger` takes only name, cron, enabled, model, prompt
and run_once_at, so a session cannot repair any of those three fields; only the claude.ai
Routines UI can.

**The first fire is a free probe of exactly that, and it should not be read as a stage
run.** It falls at 2026-09-22T18:35 UTC, against `main`, which does not yet carry
`researcher_canada/`. Step 0 is written to detect that case and say "the branch carrying
this stage has not been merged" rather than improvising, so the fire answers the one
unverified question — can a fired session reach the repository at all — without
pretending to produce a ranking. Read its reply before merging anything on the strength
of it. Stage EU's first hand-fire (`cse_01GPAvkwHzwzxuWdsscSUPUN`) spent 165k tokens and
published nothing at all, which is indistinguishable from a Routine that never fired.

**Keep this file and the Routine in step in the same commit.** Nothing enforces it and
stage E's prompt drift is what cost two live things on 2026-09-15.

---

```text
Run stage CA, the Canada researcher, for today's Toronto window.

0. GET THE REPO, ON THE RIGHT BRANCH. The sandbox starts empty and this repository's DEFAULT branch may be a stale feature branch. Do exactly this:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   If CLAUDE.md is absent after that, you have no repository and must say so rather than improvising; if CLAUDE.md is present but researcher_canada/ is not, the branch carrying this stage has not been merged and you must say THAT rather than running a different stage. Then verify that researcher_canada/scripts/ca_universe.py, researcher_canada/scripts/ca_priced_in.py, researcher_canada/scripts/ca_sources.py, researcher_us/scripts/edge_score.py and .claude/skills/researcher-canada-hunt/SKILL.md all exist.

   export EARNINGS_DATA_BRANCH=main before you call scripts/publish.sh, and after publishing run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there.

Now invoke the skill `researcher-canada-hunt` and follow it exactly. Read CLAUDE.md first.

Re-read the clock with `date -u` rather than trusting any date you were told at startup. You fire at 18:30 UTC, which is 14:30 in Toronto. The Toronto close is 16:00 ET, ninety minutes out. THAT DEADLINE IS REAL AND IT IS ABOUT THE DATA, NOT ABOUT AN ORDER: THIS STAGE PLACES NO ORDERS. There is no broker step, no alpaca_trade.py call and no execution block. Seal the baselines BEFORE the close, because after it the Montreal Exchange chain stops quoting two-sided and every name loses its option anchor.

WHAT THIS STAGE PRODUCES: one signed number per company, so today's names can be RANKED. No call, no threshold, no direction label anywhere in the output.

THE OUTPUT CONTRACT LIVES IN THE SKILL, NOT IN THIS PROMPT. Which field is the ranking key and what the note must report are stated in .claude/skills/researcher-canada-hunt/SKILL.md and in edge-scores.json's own `ranking_key` field. Read them in the tree you actually cloned.

IF THE UNIVERSE IS EMPTY, READ THE REASON RATHER THAN GUESSING IT. `universe.json` carries `market_closed`: if it is set, the TSX is shut and there is nothing to wait for. If it is null and `scheduled_today` is 0, nobody is scheduled — which in Canada is a NORMAL weekday outcome outside the reporting peaks, not a fault. Late September ran one name a day; late October runs twelve. Publish the empty universe, say which case it is in one line, and stop.

FIVE THINGS SPECIFIC TO THIS MARKET THAT BELONG IN THE NOTE EVERY TIME:

  - TWO ANCHOR ARMS, AND THE SPLIT IS THE RESULT. Report how many names came back anchor_covered "options" and how many "register". If it is zero on the options arm during a weekday run, the seal happened outside 09:30-16:00 ET and the day is a register-arm run — say so, because it changes what the day can be compared against. ca_resolve.py ranks the two arms separately and that comparison is why this stage exists: the sealed backtest priced anchor-less hunting at rho=+0.073, p=0.45 over 104 events and could not tell the anchor from the market.
  - TWO CALENDARS THAT DISAGREE ON 172 OF 277 FORWARD DATES. Report the calendar_reconciliation split (confirmed / agreed / wsh_only / vendor_only / disputed) and moved_off_target_by_wsh. Disputed names are dropped unless the issuer itself announced the date. Do not override that with --hunt-disputed: hunting an unconfirmed date is exactly how TRT was ranked, traded at 33% of equity and never reported.
  - THE SHORT REGISTER HAS NO HISTORY. short_change_pct_pts is null until two runs have stored a snapshot in researcher_canada/analysis/short-register/. Report the register_business_date you sealed. Whether that feed refreshes daily or restamps CIRO's twice-monthly snapshot is still unknown and those files are what will answer it.
  - THERE IS NO CONSENSUS EPS IN THE BASELINE AT ALL. No Canadian source here carries one. The hunter has to source the bar itself and caps its sizes when it cannot. If a hunt comes back with `bar: unsourced` and large findings anyway, that is a defect and it belongs in the run log.
  - ONE BILINGUAL PASS PER HUNTER SINCE 2026-09-22. unpriced-hunter-ca searches English and, for a Quebec issuer, French together in a single pass. It no longer freezes an English-only `pre_local` draft: that control was retired on the operator's instruction because sequencing the two halves stopped them informing each other. Do not ask a hunter for pre_local and do not add it back to the contract. What each one emits instead is `language_note` - prose, one line per thing the French sources carried that the English ones did not, or "not a Quebec issuer, English sources only". Nothing ranks it; quote it in the note where it is interesting. The pre_lessons freeze still runs.
  - ABOUT A THIRD OF THE ELIGIBLE UNIVERSE REPORTS BY SEDAR+ FILING WITH NO PRESS RELEASE. Those issuers are screened out upstream as filing_only. Report how many were dropped that way; it is the single biggest cut this stage makes and nobody has yet measured what it costs.

EVERYTHING EXCEPT THE OPTION CHAIN COMES FROM ONE VENDOR STACK (TMX/QuoteMedia). If the register, the filings, the archive and the calendar all fail together, that is one outage and not four, and the run should say so rather than reporting four separate degradations.

Work on the `main` branch. Publish the STARTED heartbeat before you spawn a single hunter, publish after each wave, and finish with `python3 scripts/update_index.py` then `scripts/publish.sh "stage CA: Canada ranking for <date>"`. This session is ephemeral; anything not pushed is lost. Publish SOMETHING even on an empty day or a failure — a fire that publishes nothing cannot be told apart from a Routine that never fired.

Reply with the funnel in one line (scheduled / eligible / hunted), the anchor-arm split, the ranked table, the finding and URL driving the top and bottom name, and one line on what the day does NOT establish.
```

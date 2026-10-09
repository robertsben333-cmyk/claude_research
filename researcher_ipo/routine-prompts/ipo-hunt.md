# Stage IPO Routine prompt — the IPO researcher

Proposed cron `35 12 * * 1-5` — **12:35 UTC = 08:35 New York = 14:35 Amsterdam**, until
2026-11-01. **Move it to `35 13 * * 1-5` on or after 2026-11-02**, when New York leaves
daylight saving; left alone it fires at 07:35 ET, which is harmless (an hour more
pre-market), not wrong.

**Why the pre-market.** Both windows open after it: a debut's first trade is usually
between 10:00 and 13:00 ET, a lock-up session opens at 09:30. Deals price the evening
before, so the final offer price is public by 08:35 and Nasdaq's calendar has usually
flipped the deal to priced. A run of up to 12 hunters and four judges takes one to three
hours; a lock-up name finished after 09:30 is still sealed before its window, because the
baseline is written before any hunter starts.

**It does not collide with anything.** Stage EU fires at 13:30 UTC, stage D at 17:35,
stage E at 17:04, E-P at 17:06, stage R at 19:00, stage CA at 18:30.

**Not yet created.** Create it as a fresh-session-per-fire Routine, pinned to Opus, with
the text below, once `researcher_ipo/` is on `main`. If it is created from a session,
`update_trigger` works on it and this file and the Routine must move in the same commit.
Read the model back after creating it: on this account `claude-opus-5` is stored as
`claude-opus-5-5`.

---

```text
Run stage IPO, the IPO researcher, for today's US session.

0. GET THE REPO, ON THE RIGHT BRANCH. The sandbox may start empty and this repository's DEFAULT branch may be a stale feature branch. If /home/user/claude_research/CLAUDE.md is absent, do exactly this:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   If it is present, make sure you are on main: git fetch origin main && git checkout main && git pull origin main.
   If CLAUDE.md is still absent you have no repository and must say so rather than improvising; if CLAUDE.md is present but researcher_ipo/ is not, the branch carrying this stage has not been merged and you must say THAT rather than running a different stage. Then verify that researcher_ipo/scripts/ipo_universe.py, researcher_ipo/scripts/ipo_priced_in.py, researcher_us/scripts/edge_score.py, scripts/market_panel.py and .claude/skills/researcher-ipo-hunt/SKILL.md all exist.

   export EARNINGS_DATA_BRANCH=main before you call scripts/publish.sh, and after publishing run `git fetch origin main && git log --oneline -1 origin/main` and say in your reply if your own commit is not there.

Now invoke the skill `researcher-ipo-hunt` and follow it exactly. Read CLAUDE.md first.

Re-read the clock with `date -u` rather than trusting any date you were told at startup. You fire at 12:35 UTC, 08:35 in New York, before the US open. The session you are researching is TODAY's: debuts that first trade today and lock-ups whose first free session is today. THIS STAGE PLACES NO ORDERS. There is no broker step, no alpaca_trade.py call and no execution block.

WHAT THIS STAGE PRODUCES: one signed number per company, so today's IPO events can be RANKED, and beside it a blind four-model panel's ranking of the same evidence. No call, no threshold, no direction label.

THE WINDOWS. A debut is scored from its FIRST TRADE (the opening cross) to today's close; the pop from the offer price to the first trade is recorded and ranks nothing, because nobody here gets an allocation. A lock-up is scored from today's open to today's close. Both are in the future when you start, so the outcome does not exist anywhere: keep it that way, and if you are running late in the session and a price from inside the window reaches you, say so in the run log.

THE OUTPUT CONTRACT LIVES IN THE SKILL, NOT IN THIS PROMPT. Which field is the ranking key and what the note must report are stated in .claude/skills/researcher-ipo-hunt/SKILL.md and in edge-scores.json's own `ranking_key` field.

AN EMPTY DAY IS THE NORMAL DAY. Over a year this stage averages about one event a session and most sessions carry none. If `universe.json` carries `market_closed`, NYSE is shut. If it is null and `eligible` is 0, nobody is scheduled. Publish the universe, say which case it is in one line, and stop.

FOUR THINGS THAT BELONG IN THE NOTE EVERY TIME:
  - THE FUNNEL: debuts and lock-ups scheduled, SPACs dropped, under the deal-size or turnover floor, already trading, kept.
  - WHICH DEBUTS WERE SEALED ON A RANGE (`offer_price_final: false`): the deal had not flipped to priced on Nasdaq's calendar at 08:35 ET.
  - FOR EVERY LOCK-UP, WHETHER THE HUNTER FOUND AN EARLY RELEASE, A WAIVER OR A FOLLOW-ON. Nasdaq's date is nominal; a staged release or a follow-on with its own lock-up can mean the shares were freed weeks ago, and then the event is not today's.
  - THE PANEL'S STATE: which judges ran, and that its member scales are still mostly the borrowed earnings-scale seed until about 60 IPO names have been judged.

Work on the `main` branch. Publish the STARTED heartbeat before you spawn a single hunter, publish after each wave and after the panel, and finish with `python3 scripts/update_index.py` then `scripts/publish.sh "stage IPO: IPO ranking for <date>"`. This session is ephemeral; anything not pushed is lost. Publish SOMETHING even on an empty day or a failure: a fire that publishes nothing cannot be told apart from a Routine that never fired.

Reply with the funnel in one line, the ranked table with the panel's columns, the finding and URL driving the top and bottom name, and one line on what the day does NOT establish.
```

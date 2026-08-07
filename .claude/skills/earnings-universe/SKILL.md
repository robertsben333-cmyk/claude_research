---
name: earnings-universe
description: Stage 0 of the daily earnings pipeline. Builds the day's US earnings universe for the actionable window (after today's close plus before the next open), qualifies it for liquidity and confirmed timing, and commits it to the research archive. Use when asked to run stage 0, build the earnings universe, or fetch today's earnings calendar.
---

# Stage 0 — Earnings universe

Cheap, mechanical, and early. This stage answers one question: **which US companies
report between today's close and the next open?** It does no analysis. Everything
downstream depends on this list being complete and correctly dated, so accuracy here
matters more than insight.

Target: finish in a handful of tool calls. If you are running subagents in this stage,
you have misunderstood it.

## 1. Resolve paths

```bash
python3 scripts/run_paths.py --json
```

Use the returned `run_dir` for everything. Never invent a path.

## 2. Fetch

```bash
python3 scripts/get_earnings.py
```

The script handles the NYSE calendar itself, so a Friday run correctly rolls the
before-open side to Monday and holidays are skipped. It writes `00-universe.json` and
`00-universe.md`, and exits:

- **0** — data retrieved. Go to step 4.
- **2** — no data. Read `status_reason` in the JSON and go to step 3.

`status_reason: network_blocked` means the *environment's* egress policy blocked the
provider, not that the provider is down. Note it in the run log — it is a configuration
problem the user needs to fix, not something you can work around properly.

## 3. Fallback: rebuild the universe by hand

Only when step 2 returned no rows.

Use `WebSearch` (and `WebFetch` where the domain is reachable) against several
independent earnings calendars — Nasdaq, Earnings Whispers, TipRanks, Investing.com,
Seeking Alpha, Zacks. Cross-check at least two sources for the session (BMO/AMC) of
every name you keep.

This fallback is materially less reliable than the API. Be explicit about that:
set `"status": "partial"` and `"status_reason": "rebuilt_from_web_search"` in the JSON,
and list which sources you used in `source_attempts`. Downstream stages read those
fields and lower their confidence accordingly.

Write the same JSON shape the script produces — keep `schema_version`, `counts`,
`companies[]` with `symbol`, `name`, `session`, `event_date`, `market_cap_usd`,
`passes_market_cap_floor`. Regenerate `00-universe.md` to match.

## 4. Qualify

Read `config/pipeline.yaml` for the thresholds. Mark — do not delete — each company
that fails a qualification rule, adding `"excluded": "<reason>"`:

- Below the market-cap floor.
- No real listed-options market. Options are how the later stages get an implied move;
  a name without them cannot be scored properly.
- OTC, SPAC remnant, or too thinly traded to act on.
- **Conflicting or unconfirmed BMO/AMC timing across sources.** Drop these. A name
  researched for the wrong session is worse than a name not researched at all.

Keeping the excluded rows with their reason means tomorrow's run can see what was
dropped and why, and that a mistaken exclusion rule is visible rather than invisible.

Set `counts.eligible` to the number of companies with no `excluded` field.

## 5. Write the run log

Create `_run-log.md` in the run directory:

```markdown
# Run log — <YYYY-MM-DD>

## Stage 0 — universe (<HH:MM> CET)
- Window: <window_covered>
- Source: <nasdaq | fmp | finnhub | web-search fallback>
- Universe: <n> total (<a> AMC, <b> BMO); <e> eligible after qualification
- Excluded: <n> (<breakdown by reason>)
- Notes: <anything odd — feed gaps, holiday roll, conflicting timings>
```

Each later stage appends its own section. Never rewrite an earlier stage's section.

## 6. Publish

```bash
python3 scripts/update_index.py
scripts/publish.sh "stage 0: universe for <YYYY-MM-DD> (<e> eligible of <n>)"
```

The session is ephemeral. Anything not pushed is gone.

## 7. Report

Three or four lines: the window, the counts, the source used, and whether stage 1 will
trigger (it is skipped when eligible names are at or below
`triage.skip_if_universe_at_or_below`). If the universe is empty because of a market
holiday, say so plainly — that is a normal outcome, not a failure.

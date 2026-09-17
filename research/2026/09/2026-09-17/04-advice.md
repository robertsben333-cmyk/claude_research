# Earnings advice — 2026-09-17

**Status: NO NAMES — no calls today.** Window: after the US close on Thursday 17
September 2026 through before the US open on Friday 18 September 2026. 0 names
researched, 0 panelled.

## Why there is nothing to call

Stage 0's universe fetch for this window found exactly one candidate — **UPXI**
(Upexi, Inc.), an amc print, market cap $76.0M — and excluded it at the $500M
market-cap floor, leaving `universe_eligible: 0`. Stage 1 triage ran in skip mode
(`triage_mode: skipped_small_universe`) and published `shortlist: []`. Both stage 2
batches checked that against `00-universe.json`/`01-shortlist.json`, found nothing to
research, and published `02-ranking.json` with `names: []` and `top_n_for_panel: []`.

This is not a pipeline outage. Every upstream stage published a `STARTED` heartbeat
and a finished section today (`_run-log.md`), and `02-ranking.json` exists — it is
correctly empty because the day's actionable calendar was empty, not because a stage
died. Per the `earnings-panel-advice` skill, an empty-but-legitimate ranking is
reported as `status: no_names`, distinct from `blocked` (an upstream stage producing
nothing at all).

## Ranked field

No names cleared the universe's own market-cap floor, so there is no deep-dive ranking
to show and nothing panel-eligible.

| Ticker | Session | Market cap | Result |
| --- | --- | --- | --- |
| UPXI | amc | $76.0M | Excluded at stage 0 — below the $500M market-cap floor |

## What would change this

Nothing about this note is a market call to revisit. The next thing that changes it is
tomorrow's stage 0 finding a print that actually clears the $500M floor.

## Coverage and caveats

- **Upstream stages:** 0, 1 and 2 all ran and published on schedule for 2026-09-17;
  all three correctly found nothing to carry forward.
- **Panel:** not run — no eligible names, no subagents spent, no panel seats to fill.
- **Budget:** no degradation applied; nothing was shed, because there was nothing to
  shed against.

---

This is research, not financial advice. Earnings reactions are highly uncertain and
can be driven by market positioning, guidance, macro conditions, and management
commentary rather than reported results alone.

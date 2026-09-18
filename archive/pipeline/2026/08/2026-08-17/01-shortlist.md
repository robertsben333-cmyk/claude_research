# Stage 1 — Triage shortlist for 2026-08-17

Window covered: After the US close on Monday 17 August 2026 through before the US open on Tuesday 18 August 2026

## Funnel

22 universe → 11 eligible → 11 cleared floors → **6 shortlisted**

Mode: scouted (1 `earnings-triage-scout` subagent, sonnet/medium, 11 names in one batch —
under `triage.batch_size`). `triage.shortlist_size` is 6 as of the 2026-08-13 budget cut.

All 11 eligible names cleared both hard floors (`min_change_expectation: 35`,
`min_ai_edge: 30`); the cut to 6 is entirely a priority-score ranking, not a floor
rejection.

## Shortlist

| Ticker | Session | change_expectation | ai_edge | priority | Rationale |
| --- | --- | --- | --- | --- | --- |
| FN | amc | 78 | 65 | 72.15 | AI-capex optical pure-play; history of double-digit post-print moves; strong peer read-throughs (Coherent, Lumentum) |
| VNET | bmo | 60 | 52 | 56.40 | China AI-infrastructure data-center build-out; sharp historical reactions, thin but real synthesis opportunity |
| KLAR | bmo | 70 | 38 | 55.60 | Post-IPO BNPL/AI hype name; big expected move but ai_edge only narrowly clears the floor — thin history to underwrite conviction |
| PONY | bmo | 70 | 38 | 55.60 | Chinese robotaxi story; large expected move but ai_edge narrowly clears the floor — thin, unreliable forward estimates |
| BIDU | bmo | 55 | 55 | 55.00 | China AI-cloud/Apollo Go robotaxi monetization debate; well-balanced on both axes |
| AS | bmo | 55 | 50 | 52.75 | Arc'teryx/Salomon growth mix; guidance is a live question, moderate public channel-check data |

## Session mix warning for stage 2

**5 of 6 names are BMO (2026-08-18), only 1 is AMC (FN, 2026-08-17).** This is a real
tilt, not a tiebreak artifact — the top 6 by priority score simply skewed BMO-heavy
(XP and YALA, the next two AMC names, ranked #8 and #9 at 49.5 and 49.15, below AS at
#6 with 52.75). No manual swap was made to correct it; the ranking was left mechanical
and auditable. Stage 2 should note that tonight's after-close window (2026-08-17) is
only lightly covered by this shortlist.

## Notable drops (cleared floors, cut on rank)

| Ticker | Session | priority | Why dropped |
| --- | --- | --- | --- |
| IQ | bmo | 50.80 | Well-worn structural-decline story, already heavily covered — limited fresh edge despite real volatility |
| XP | amc | 49.50 | Brazil fintech macro story, decent edge, but change_expectation (45) is the lowest of the surviving-floor group |
| YALA | amc | 49.15 | MENA social/gaming name; sharp historical swings but thin public engagement data and light liquidity cap the edge |
| HD | bmo | 47.85 | Mega-cap grinds low-single-digit moves; change_expectation too low to compete despite decent ai_edge |
| RNW | bmo | 42.25 | Small-cap India renewable IPP; complex financing/regulatory story, thin US coverage, lower on both axes |

Evidence quality across the board is `thin` — the scout could not confirm implied-move
percentages for any name (`expected_move_hint: null` throughout), so no number was
fabricated. Stage 2 dossiers should prioritize sourcing real implied-move and options
data for the shortlist before leaning on the triage scores.

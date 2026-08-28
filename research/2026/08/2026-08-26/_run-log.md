# Run log — 2026-08-26

## Stage 0 — universe (07:22 CEST)
- Window: After the US close on Wednesday 26 August 2026 through before the US open on Thursday 27 August 2026
- Source: nasdaq (`scripts/get_earnings.py` exit 0, no fallback needed)
- Universe: 40 total (16 AMC, 24 BMO); 32 above the $500M market-cap floor; 32 eligible after qualification
- Excluded: 8, all `below_market_cap_floor` (BBW, TITN, GOTU, MTLS, LTRX, BZUN, CISS, PDCC)
- Qualification detail: checked each of the 32 above-floor names for listed-options market via
  WebSearch (nasdaq.com / broker option-chain pages) — all 32 confirmed optionable, none OTC or
  SPAC-remnant shells. LUCK (ex-Bowlero via ISOS Acquisition Corp) and CMBT (ex-Euronav) are
  post-merger operating companies, not shells, so kept.
- Notes: `sources_used` for both sides of the window was `nasdaq` only — no second calendar was
  cross-checked, so the "conflicting/unconfirmed BMO/AMC timing" exclusion rule could not be
  applied for real (nothing to conflict against). Session tags are taken as given from Nasdaq's
  earnings calendar, which is generally reliable for BMO/AMC. Flagging this as a standing
  limitation rather than a defect this run. Two empty leftover directories (`02-dossiers/`,
  `03-panel/`) existed in today's run folder before this stage started, with no files and no
  prior run log — stray scaffolding, not resumed state; left in place since stages 2/3 will use
  them anyway. 32 eligible names is well above `triage.skip_if_universe_at_or_below: 10`, so
  stage 1 will run today.

## Stage 1 — triage (09:12 CEST)
- Mode: scouted (32 eligible names, above the 10-name skip threshold)
- Funnel: 40 universe -> 32 eligible -> 22 cleared floors -> 6 shortlisted
- Scouts: 3 subagents (sonnet/medium), batches of 11/11/10
- Session mix: 5 AMC / 1 BMO — shortlist tilts to after-close reporters. CSIQ (65.0) and
  BURL (64.35) were the closest BMO alternatives but scored below the AMC names actually
  taken; not swapped in, noted as a tilt for stage 2/3 awareness of Thursday's BMO window.
- Dropped for floors (7): RY, TD, CM (mega-cap banks, Δ-exp 24-26, formulaic prints),
  HMY (AI edge 28 — pre-announced guidance, gold-price/rand driven), HRL (Δ-exp 32 —
  low-volatility packaged foods), PURR (AI edge 25 — GAAP dominated by unrealized HYPE
  mark-to-market, not an analyzable operating story), LUCK (Δ-exp 30 — low-volatility
  bowling roll-up).
- Dropped for timing/tradeability (3): DG — scout found a conflicting report-date source
  (28 Aug vs the 27 Aug used in the universe file); would have scored well enough to
  shortlist (Δ-exp 60 / AI edge 55) had timing been confirmed — worth re-checking before
  stage 2. P ("Everpure, Inc.") — likely a universe-stage data-quality error; the only
  filing findable under this ticker/cap belongs to Pure Storage, not an entity called
  "Everpure." LOT (Lotus Technology) — timing confirmed but flagged not tradeable, thin
  ADS liquidity.
- Shortlist: OKTA (68.8), STDN (68.75), URBN (67.9), DLTR (67.7), NTNX (66.4), CRWD (65.7)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-08-26 08:23 UTC
- Tickers: OKTA, STDN, URBN
- Plan: 2 waves (OKTA+STDN, then URBN) of opus/high researchers, publish after each dossier and after each wave

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-08-26 10:24 UTC
- Tickers: DLTR, NTNX, CRWD (shortlist positions 4-6)
- Batch 1 status: partial — OKTA and STDN dossiers exist, URBN (position 3) is missing and batch 1 has no closing run-log section (likely killed before its second wave). Not treated as 'batch 1 failed entirely' since 2/3 completed, so batch 2 sticks to its own assigned half per the cap; URBN gap flagged for stage 3 awareness.
- Plan: 2 waves of opus/high researchers (wave 1: DLTR+NTNX, wave 2: CRWD), publish after each dossier and after each wave
- This batch is the day's final batch: will also write 02-ranking.json from whatever dossiers exist (OKTA, STDN + this batch's).

## Stage 2 — deep dive, batch 2 — wave 1 complete
- Logged at 2026-08-26 10:44 UTC
- DLTR: published, implied move ±9.2%, direction -10, evidence completeness 84
- NTNX: published, implied move ±14.49%, direction -10, evidence completeness 84
- Starting wave 2: CRWD

## Stage 3 — panel & advice — STARTED
- Logged at 2026-08-26 15:56 UTC
- Stage 2 never wrote 02-ranking.json (batch 2 stalled after wave 1: DLTR, NTNX published, CRWD never researched; batch 1 also left URBN unpublished). Built 02-ranking.json myself from the 4 dossiers on disk (OKTA, STDN, DLTR, NTNX) using panel.rank_by.
- Panel eligibility: OKTA, DLTR, NTNX eligible; STDN excluded (no implied move, no historical move history — thin post-IPO trading record).
- Ranking (panel_priority): OKTA 49.1, DLTR 48.7, NTNX 47.9, STDN 44.45 (excluded).
- Not researched at all: URBN, CRWD — flagged for the ranked field and coverage section.
- config panel.names=2 (already at first budget.degrade_order step from 2026-08-13). Taking top 2 eligible: OKTA, DLTR. No further degradation applied — panel budget cap (14 = 2x7) matches this exactly.

## Stage 3 — panel & advice — OKTA complete
- Logged at 2026-08-26 16:07 UTC
- Panel: 7/7 seats filled, no retries needed
- Synthesis: consensus -1.4, call Neutral / No Edge, certainty High (80.6), reversal risk High (60.5 consensus / 62 red-team)
- Chair: no override; added early_prediction, red_team_survival_note, chair_independence_note

## Stage 3 — panel & advice — DLTR complete
- Logged at 2026-08-26 16:11 UTC
- Panel: 7/7 seats filled, no retries needed
- Synthesis: consensus +5.4, call Neutral / No Edge, certainty High (84.8), reversal risk Med (59.7 consensus / 60.0 red-team)
- Chair: no override; added early_prediction, red_team_survival_note, chair_independence_note

## Stage 3 — panel & advice — FINISHED
- Logged at 2026-08-26 16:13 UTC
- Panelled: OKTA, DLTR
- Calls: OKTA Neutral / No Edge (unsigned band 6.7-31.6%, certainty High, reversal High), DLTR Neutral / No Edge (unsigned band 4.9-23.3%, certainty High, reversal Med)
- Panel seats filled: 14/14 (7/7 both names), no retries needed
- Chair overrides: none (both syntheses accepted as computed; chair added early_prediction/red_team_survival_note/chair_independence_note only)
- Degradations: 02-ranking.json rebuilt by this stage from 4 dossiers (stage 2 stalled after wave 1 in both batches, URBN and CRWD never researched); panel.names held at config default of 2 rather than cut to 1, since both panels completed and published before this note was written -- see 04-advice.md Coverage for the full reasoning

## Stage 4 — calibration — DEFERRED
- Logged at 2026-08-27 (attempted on schedule)
- 04-advice.json exists (OKTA and DLTR panelled Neutral/No Edge; NTNX non-panelled with a
  preliminary read; STDN non-panelled and panel-ineligible). No 05-outcome.md.
- Cannot score yet: measurement convention is close-before-print to
  close-after-first-full-session-following. OKTA reported amc 2026-08-26, so its first full
  session is today's (2026-08-27) regular session; DLTR reports bmo 2026-08-27, so its first
  full session is also today's session. Both need the 2026-08-27 close.
- Confirmed via WebSearch this is the same gap logged on 2026-08-20: today (2026-08-27) is a
  normal trading day with no holiday, but DLTR's bmo print and reaction have not resolved yet
  (search results for DLTR still show pre-earnings expectations, not a reported outcome), and
  OKTA's Thursday close is not yet in — only Wednesday's after-hours move is known. Not
  fabricating an intraday or after-hours quote as a close.
- Deferring: the next stage-4 firing (2026-08-28 08:20 CEST) is the earliest time
  2026-08-27's close is known for both names, so it should pick this run up on the next
  attempt. Recorded here per the standing flag from 2026-08-20: stage 4's 08:20 "of
  yesterday" slot cannot generally close out a run whose window extends to a bmo print or a
  same-evening amc print, because both resolve on the *current* day's close — this is not a
  one-off, it is the second such deferral on record (2026-08-20, and now 2026-08-27), so the
  schedule itself likely needs an extra day of lag rather than each occurrence being treated
  as a fluke.
- No LEDGER.md change made; no 05-outcome.md written.

## Stage 4 — calibration — FINISHED
- Logged at 2026-08-28 (scheduled run)
- 2026-08-27's close is now known for both OKTA (amc 8/26) and DLTR (bmo 8/27); scored
  this run in full.
- OKTA: +28.63% (close $134.42 -> $172.91), a miss for the Neutral call under the
  below-expected-move convention (28.63% >> 13.4% expected) though inside its 6.7-31.6%
  band; broke the 13.0% implied move by >2x. Preliminary read (+10) called direction
  right; panel hedged to Neutral and had no view.
- DLTR: -3.92% (close $132.18 -> $127.00), a hit for the Neutral call (3.92% < 9.9%
  expected) but the move landed below the low end of its own 4.9-23.3% band. Gapped down
  ~9% at the open on weak Q3 guidance before recovering to close -3.92% -- the red-team's
  specific reversal mechanism (beat overshadowed by cautious guide) fired; only its -10%
  magnitude overshot. Preliminary read (-10) called direction right.
- NTNX (non-panelled, prelim -10): +6.81%, preliminary miss.
- STDN (non-panelled, panel-ineligible, prelim -15): +4.45%, preliminary miss.
- Third straight panelled run where the panel converged to Neutral / No Edge on every
  panelled name (WOLF 08-19, OKTA+DLTR 08-26) while the stage-2 preliminary read called
  direction correctly on all three -- flagged in 05-outcome.md as a pattern worth
  checking against `scripts/synthesize.py`'s Neutral threshold, not yet a fourth
  coincidence.
- Wrote 05-outcome.md / 05-outcome.json. Updated LEDGER.md, rebuilt PREDICTIONS.csv/json.
- 2026-08-27 run (ESTC, AFRM, S, MRVL, RBRK, all amc 2026-08-27) still cannot be scored:
  its first full session following is 2026-08-28's close, which has not happened yet at
  this firing. Left for the next stage-4 run once that close exists -- same schedule-lag
  issue flagged on 2026-08-20 and 2026-08-27, now a third occurrence. Recommend the
  routine schedule build in the extra day of lag rather than relying on stage 4 to defer
  and retry each time.

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

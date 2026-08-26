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

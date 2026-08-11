# Run log — 2026-08-11

## Stage 0 — universe (07:19 CEST)
- Window: After the US close on Tuesday 11 August 2026 through before the US open on Wednesday 12 August 2026
- Source: nasdaq (both after-close and before-open sides; single source, no network block)
- Universe: 112 total (67 AMC, 45 BMO); 53 above the $500,000,000 market-cap floor; 53 eligible after qualification
- Excluded: 59 total — 58 below_market_cap_floor (feed value), 1 unconfirmed_market_cap (`SPMC`, feed returned no market-cap figure at all)
- Notes: `python3 scripts/get_earnings.py` returned status `ok` on the first attempt — no
  network block. Qualification against `config/pipeline.yaml` used the nasdaq feed as the
  sole source, so there were no cross-source BMO/AMC timing conflicts to reconcile.
  13 recently-listed or otherwise unfamiliar above-floor names were spot-checked via
  WebSearch for a real, confirmed listed-options market rather than excluded by
  guesswork: `QNT` (Quantinuum, Nasdaq IPO Jun 2026), `FRVO` (Fervo Energy, Nasdaq IPO May
  2026), `BETA` (Beta Technologies, NYSE IPO Nov 2025 — specific option contract page
  found), `FLY` (Firefly Aerospace, Nasdaq IPO Aug 2025 — specific option contract page
  found), `AADX` (Applied Aerospace & Defense, NYSE), `EROC` (ERock, NYSE IPO Jun 2026 —
  new option listings confirmed added Jul 10), `TE` (T1 Energy, formerly FREYR Battery —
  option chain confirmed on Nasdaq.com), `ELE` (Elemental Royalty, Nasdaq since Nov 2025,
  also cross-listed TSX-V), `WYFI` (WhiteFiber, Nasdaq carve-out IPO of Bit Digital, Aug
  2025), `VINP` (Vinci Compass Investments, renamed Vinci Partners, Nasdaq-listed since
  2021), `FAC` (Factorial Energy, Nasdaq SPAC-merger completion Jun 2026 — options
  confirmed available on Robinhood/Webull despite recency), `MRX` (Marex Group, Nasdaq IPO
  2024 — options confirmed via Yahoo/Webull/TradingView), `BGSI` (Boyd Group Services,
  NYSE, 14 analysts). All 13 cleared and remain eligible; none excluded on
  options/OTC/SPAC-remnant/timing grounds.
  The remaining 40 above-floor names are established Nasdaq/NYSE-listed operating
  companies or ADRs with analyst coverage; options-market/OTC/SPAC-remnant/timing
  screening for those was done by inspection, consistent with the 2026-08-10 run's
  approach.
  `SPMC` (Sound Point Meridian Capital) returned `market_cap_usd: null` from the feed —
  excluded as `unconfirmed_market_cap` rather than guessed; it is a closed-end fund
  reporting on 2026-08-12 BMO, well below the kind of size that would plausibly clear the
  floor even if the feed had populated it, so no correction was chased.
  53 eligible names exceeds the stage-1 skip threshold (`triage.skip_if_universe_at_or_below: 10`),
  so stage 1 (triage) will run normally at 11:08 CEST.

## Stage 1 — triage (10:47 CEST)
- Mode: scouted (53 eligible > skip threshold of 10)
- Funnel: 112 universe -> 53 eligible -> 35 cleared floors -> 10 shortlisted
- Scouts: 4 subagents (sonnet/medium), batches of 14/14/14/11 tickers
- Session mix: 7 AMC / 3 BMO — tilted AMC; noted in 01-shortlist.md, not corrected
  beyond one tie-break (LQDA kept over BORR, tied at priority 62.75, to add a third
  BMO name)
- Dropped for timing/tradeability (11): QNT, FRVO, AADX, ELE, UAMY, EROC
  (not_tradeable — recent IPO/thin float/no real options market/implausible data);
  TGLS, IMOS, EVLV, WYFI, MLYS (timing_unconfirmed — stale/conflicting dates or
  session mismatch)
- Dropped below floors (7): ALT (chg 92, edge 20 — Phase 2b binary readout paired
  with the print, textbook high-move/no-edge case), FNV, AMCR, HRB, PFGC, BGSI, ITRN
  (formulaic, slow, well-covered prints)
- Note for stage 2 / auditability: stage 0's due-diligence pass confirmed a real
  listed-options market for QNT, FRVO, AADX, and ELE at the universe stage. The
  triage scouts still marked them `tradeable: false` here — their objection is thin
  float / recency / one-quarter-of-history making the *setup* hard to research and
  act on, not literal options-market absence. Flagging the discrepancy rather than
  silently reconciling it; if any of these move sharply tomorrow, this is where to
  look.
- No warnings triggered stage 2 scope reduction; budget (`triage.max_subagents: 6`)
  not exceeded (4 of 6 scouts used).

# Run log — 2026-09-22

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-21 13:39 UTC
- Fired 2026-09-21 13:30 UTC (session clock read 13:38 UTC). Sealing for the NEXT European trading day, **2026-09-22** (Tue). Europe reports before the open, so the window is close(2026-09-21) -> close(2026-09-22) for bmo names.
- Sealed spot is an INTRADAY price, not a close: the stage fires ~2h before the 17:30 CET close on the operator's instruction of 2026-09-19. eu_resolve.py takes the realised move from daily bars, never from the sealed spot.
- Plan: eu_universe.py --date 2026-09-22 over ten markets (uk de fr se dk no fi it es pl), $200k/day turnover floor, cap 20, seeded random draw; eu_priced_in.py seals baselines; one isolated hunter per name dispatched on submarket in waves of 5; edge_score.py (the US scorer, unchanged); europe-note.md; publish after every wave.
- Research only. No orders, no broker call. Publishing to main (EARNINGS_DATA_BRANCH pinned explicitly).

## Stage EU — universe and baselines sealed
- Logged at 2026-09-21 13:42 UTC
- Universe: 22 vendor rows scheduled for 2026-09-22, 13 dropped on the $200k/day floor, **9 eligible, 9 hunted** — at/under the cap of 20, so `selection.method` is 'all 9 eligible names' and no random draw was needed.
- by_market: uk 8, fr 1. `market_concentration.largest_market_share` = **0.889 uk**, 2 markets represented. Eight of the ten markets contributed nothing: de/se/dk/no/fi/it/es all had 0 scheduled rows, pl had 1 scheduled and 0 above the floor. No market was flagged `market_closed`. Late September is the UK's month, as SUBMARKET.md predicts.
- Registers: FCA (uk) read, 419 rows as of 2026-09-19; AMF (fr) read, 74 issuers as of 2026-09-17. **7 of 9 names carry `anchor_covered: true`**; FNX and ABCA are `register_read_no_position` (a truncated zero, not an anchor) and take `anchor_quality.direction` 0.15 instead of 0.45.
- Sessions: all 9 bmo. Three carry `session_unresolved: true` — PRTC, SAA, SMIN — defaulted to bmo on the 339/379 measured UK base rate.
- history.basis: 8 UK names `observed_rns` (real dated announcement history); ABCA (fr) is `estimated_from_cadence` — a scale, never evidence a print exists.

## Stage EU — wave 1 banked (5 of 9)
- Logged at 2026-09-21 18:32 UTC
- Hunted: ABCA (fr), KGF, SMIN, OXB, MAB1 (uk). All five wrote a complete hunt file and all five carry a real `pre_local` freeze, a `pre_lessons` freeze and `event_confirmed: true`.
- Finding sums before scoring: OXB +3.20, KGF +2.70, ABCA +2.30, MAB1 +1.40, SMIN −1.40.
- **All five subagents were killed by an account session rate limit (HTTP 429, reset 18:30 UTC) during their wrap-up turn, AFTER writing their JSON.** Nothing was lost: the contract check passes on all five. Only KGF's hand-back reached this session in prose; the other four are read from disk.
- **The run therefore spans a 4.5-hour gap**: baselines sealed 13:39 UTC, wave 1 hunted 13:50–14:00 UTC, wave 2 dispatched after the reset at 18:31 UTC. The baselines are unaffected — sealed once, before any hunter, and nothing downstream revises them. But wave 2's hunters can see the 2026-09-21 European close and wave 1's could not, which is an information asymmetry INSIDE one day's ranking. It is recorded here and in the note rather than smoothed over.
- KGF flagged that it could not reproduce the baseline's short figure: the live FCA aggregated CSV reads 9.31% at position date 2026-08-05 where the cached baseline reads 10.69% at 2026-09-16, and the FCA's own 'current' file is itself ~6 weeks stale. Direction unaffected. Recorded, not corrected — the baseline is sealed.

## Stage EU — wave 2 partial (FNX, SAA banked)
- Logged at 2026-09-21 18:45 UTC
- FNX: emitted −1.0, 3 findings summing −1.3, event confirmed twice from the issuer's own words (23 Jul RNS naming 22 September, plus today's 11:33 RNS setting a 22 Sep 09:00 BST question deadline). `anchor_covered: false` — the FCA register read and does not name Fonix, which is the 0.5% per-holder truncation floor and not a measurement, so its lean is close to the free control.
- SAA: emitted +2.4, 3 findings summing +3.1, event confirmed. Its locality control is the largest on the day — `pre_local` −2.0 flips to `pre_lessons` +2.4.
- Two 89-byte files (`prtcq.json`, `sptxq.json`) were left in the repo root by a hunter's curl — failed Yahoo chart calls returning `Invalid Crumb`. Deleted; they carried nothing. Worth noting that hunters can write scratch to the repo root.
- LUCE and PRTC still hunting.

## Stage EU — Europe researcher — COMPLETE (9 of 9 hunted, 9 of 9 rankable)
- Logged at 2026-09-21 19:07 UTC
- Sealed for **2026-09-22**. Ranking on `impact_sum`: OXB +3.20, SAA +3.10, KGF +2.70, ABCA +2.30, LUCE +1.40, MAB1 +1.40, PRTC −0.80, FNX −1.30, SMIN −1.40. **Two clear the conviction floor of 3.0** (OXB, SAA).
- **Both floor-clearers rest on an activist TR-1 filed within 24h of the print** — Irenic 5.41% in OXB (RNS 21 Sep 10:43) and Harwood/Rockwood/Oryx crossing 9% in SAA (TR-1 21 Sep 17:25). That is ONE correlated exposure the scorer cannot see, the same shape as the four IEEPA-tariff US names on 2026-09-10. Flagged at the top of the note.
- All nine `event_confirmed: true` from the issuer's own calendar or RNS, not the vendor. **All three `session_unresolved` names (PRTC, SAA, SMIN) were settled against a primary document**; PRTC's hunter also closed the ADR/after-hours risk via Form 25 and 15F-12B on EDGAR.
- Anchor: `options` null in all ten markets. FCA (419 rows, 2026-09-19) and AMF (74 issuers, 2026-09-17) both read; **7 of 9 `anchor_covered: true`**, ABCA and FNX truncated zeros whose lean is therefore the free control. Zero names from es/pl and zero from de, so the three markets that cannot reach `event_occurred: false` cost this day nothing.
- Controls: lessons freeze on 9 of 9, **8 moved** (largest LUCE +1.3; SMIN unmoved; ABCA and PRTC moved DOWN). Locality freeze on 9 of 9, **9 moved**, largest **SAA −2.0 → +2.4, a sign reversal**. Eight UK names against one French one, so there is nothing poolable here and `eu_resolve.py` will not pool a UK locality delta with a French language one anyway.
- **Two defects recorded, not smoothed.** (1) The run spans 4.5h across two account rate limits, so wave 2 saw the 09-21 London close and wave 1 did not — SAA's largest finding rests on a 17:25 TR-1 that did not exist when wave 1 ran, and SAA and OXB are ranked against each other on unequal information. (2) KGF's baseline short (10.69% @ 2026-09-16) is not reproducible from the live FCA file (9.31% @ 2026-08-05), whose every top row is ~6 weeks stale.
- Also noted: ABCA's `print_vs_bar_pct` is +25.0, an order-of-magnitude outlier struck against an H1 share of an unrevised FY consensus on 2 analysts. It does not affect the rank — `impact_sum` is the key — but it should not be quoted bare.
- Resolve: all nine are uk/fr, both of which have a dated day archive, so **this run does not expire** (no Nordic ~12-day window applies). Yahoo's `.L` closes lag one session and `.PA` about two, so it cannot be resolved on the morning of 09-23.
- Research only: no order placed, no broker contacted, no `alpaca_trade.py` step. Published to **main** with EARNINGS_DATA_BRANCH pinned explicitly.

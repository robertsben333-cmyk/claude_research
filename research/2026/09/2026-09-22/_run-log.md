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

## Stage J — Japan researcher — STARTED
- Logged at 2026-09-22 01:07 UTC
- Fired 01:04 UTC (10:04 JST) for the Tokyo window. Plan: jp_universe → seal baselines → one unpriced-hunter-jp per name in waves of 5 → edge_score → ranked note. NO orders. Note: 2026-09-22 is 敬老の日, expect market_closed.

## Stage J — Japan researcher — MARKET CLOSED
- Logged at 2026-09-22 01:08 UTC
- 2026-09-22 is 敬老の日 / 国民の休日; universe.json carries market_closed='public holiday: 休日'. Calendar WAS readable (680 rows across 2 JPX sheets, as_of 2026-09-03 & 2026-09-17), scheduled_today=0. This is the exchange-shut case, not an unpublished cohort sheet. No baselines sealed, no hunters spawned, no orders (stage J never places orders). Empty universe + note published. Tokyo reopens 2026-09-24.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-22 13:42 UTC
- Fired 2026-09-22 13:40 UTC (13:30 cron), European markets still OPEN — the sealed spot is an intraday price, NOT close(D-1). Sealing for the next European trading day, EVENT DATE 2026-09-23 (Europe reports before the open: 339/379 measured UK results RNS landed before 08:00 London).
- PRIOR RUN FOUND at research/2026/09/2026-09-23/europe/: built 2026-09-19T02:10Z over THREE markets (uk/de/fr) only, 9 eligible, 2 hunted (KWS SAAT, Quadient), 7 UK names shed because that session could not spawn subagents. Its baselines were sealed three sessions before close(D-1), so its spot and run_up_20d_pct are struck on the wrong day for the window eu_resolve.py will measure. It is preserved at europe/_run1-2026-09-19-seal/ (the same treatment the US stage gave 2026-08-31 run 1) and today's run is built fresh.
- Plan: ten-market universe (uk de fr se dk no fi it es pl), $200k/day turnover floor, cap 20, date-seeded random draw -> seal baselines -> one isolated hunter per name dispatched on submarket via MARKETS[submarket]['hunter'], English pass frozen as pre_local then local pass -> waves of 5, publish after each -> researcher_us/scripts/edge_score.py -> europe-note.md. RESEARCH ONLY: no broker, no orders, no alpaca_trade.py step.
- Publishing to main with EARNINGS_DATA_BRANCH pinned explicitly; the Routine's stored outcomes branch reads claude/pensive-sagan and has never been observed.

## Stage EU — universe and baselines sealed for 2026-09-23
- Logged at 2026-09-22 13:48 UTC
- Ten-market universe: 23 scheduled, 14 dropped, 9 eligible, 9 hunted (at/under the cap of 20, so NO random draw was needed — selection.method is 'all 9 eligible names'). by_market uk 6, de 1, fr 1, it 1; se/dk/no/fi/es/pl contributed ZERO. market_concentration: uk 66.7%, 4 of 10 markets represented.
- No market was closed — market_closed is null on all ten. Off-primary-exchange rows filtered: 231 Swedish (NGM) and 326 Polish (NewConnect), neither of which would take Yahoo's .ST/.WA tape.
- NONE of the day's names come from Spain or Poland, so no name in this run is anchor-less by construction. ONE name (KWS, de) sits in the market that can never reach event_occurred:false. Italy's PHIL is the first Italian name this stage has ever hunted — it arrives from the 2026-09-19 seven-market expansion and is the only one of the seven new markets to contribute today.
- Registers all read at seal time: FCA 419 rows as_of 2026-09-19, Bundesanzeiger 287 as_of 2026-09-21, AMF 74 as_of 2026-09-21, CONSOB 48 as_of 2026-09-21. anchor_covered is TRUE for only 3 of 9 (BOKU 0.27%, CWR 13.21%, JDG 1.67% — all UK); the other six are register_read_no_position, a truncated zero and not a disclosure, and their anchor_quality.direction is held to 0.15 rather than 0.45.
- options is null on all nine, all ten markets: Europe runs in the anchor-less regime that backtest/FINDINGS.md section 33 priced at rho=+0.073, p=0.45 over 104 events.
- session_unresolved on 3 of 9 (PHIL, BOKU, CWR) — vendor flag unknown, defaulted to bmo; eu_resolve.py measures BOTH windows for those rows. history.basis is observed_rns for the 6 UK names and estimated_from_cadence for KWS, QDT and PHIL — a scale, never evidence a print exists on a date.
- TIME (Time Finance) was in run 1's universe and is dropped today at $189,238/day against the $200,000 floor. The floor was NOT lowered to keep it.

## Stage EU — DEFECT: the cadence-estimated history understates event scale, measurably
- Logged at 2026-09-22 14:06 UTC
- Found by the KWS hunter and VERIFIED here against the sealed baselines rather than taken on trust. KWS's history.basis is estimated_from_cadence and carries eight dates: 2023-10-16, 2024-02-27, 2024-07-10, 2024-11-20, 2025-04-08, 2025-08-14, 2026-01-02, 2026-05-12. Exactly ONE of the eight (2026-05-12) is a real KWS print day. The hunter's independently sourced print dates are 2024-09-26, 2025-02-13, 2025-05-13, 2025-09-25, 2026-02-12, 2026-05-12.
- The consequence is a BIASED MAGNITUDE SCALE, and it is visible across this whole run. Median absolute move by basis, over today's nine sealed baselines: observed_rns (6 UK names) 2.61 / 3.16 / 3.80 / 4.76 / 6.06 / 10.50 with maxima of 15-32 pct; estimated_from_cadence (KWS de, QDT fr, PHIL it) 1.82 / 1.90 / 2.09 with maxima of 3.79, 4.65 and 17.82. A cadence estimator that lands on ordinary sessions samples ordinary-session volatility, so the eight markets without an observed history get an event scale roughly HALF the observed one.
- Why this matters beyond one name: history feeds the magnitude half of baseline_quality and it is the scale a hunter sizes against. Understating it pushes every hunter in those eight markets toward smaller numbers, and 'understatement is the hunters' systematic error' is already a LESSONS.md rule. Only uk (observed_rns) and no (observed_newsweb) are exempt.
- NOTHING WAS CHANGED. The baselines are sealed and stay sealed; no baseline was revised, and no hunter was re-run. The KWS hunter did the right thing — it sized against the real dated record it sourced itself and said in baseline_tension that it was doing so.
- This is one day and three estimated names, so it is a lead and not a measurement. The cheap way to settle it is to put the observed-vs-estimated split in eu_resolve.py's output and let it pool, the same way anchor_covered is already split.

## Stage EU — the cadence defect is corroborated INDEPENDENTLY, from a second market
- Logged at 2026-09-22 14:06 UTC
- The QDT (fr) hunter reached the same conclusion as the KWS (de) hunter with no knowledge of it — the two ran in isolated contexts and were never given each other's output, which is the whole point of one-hunter-per-name. QDT's sealed event_move_proxy_pct is 1.82%; the last two full-results prints in exactly this close-to-close window were -17.82% (2025-09-24) and -14.20% (2026-03-25), with +3.01% for the one guidance confirmation (2026-05-21). The hunter called it 'wrong by roughly 8x'.
- So the defect now has two independent instances in two markets on one day, plus the cross-sectional split measured here (observed_rns median |move| 2.61-10.50 against estimated_from_cadence 1.82-2.09). It is no longer a single hunter's complaint about a single name. It is still ONE DAY and THREE estimated names, so it is a lead to settle by pooling, not a measurement.
- TOOLING TRAP worth keeping, from the QDT hunt: on info-financiere.gouv.fr (the AMF flux) the working field names are identificationsociete_iso_cd_isi for the ISIN and uin_dat_amf for the timestamp. A where= clause on a field that does not exist returns total_count: null rather than an error — so a wrong field name reads exactly like a company that filed nothing. That is the same silent-failure shape as the Nasdaq Nordic feed's ignored fromDate and eMarket STORAGE's exclusive data_to, and it belongs beside them.
- Also measured: eu_pdftext.py read the three AMF franchissement-de-seuils PDFs cleanly (which is what turned Quadient's positioning finding from a search snippet into a quotable primary document) but returned only font and language tags on the Q1 2026 communique PDF from the same flux. Its success rate varies by filer/producer within one source, so a failed read is not evidence the document is unreachable.
- NOTE ON PROVENANCE: both of these are subagent claims. The cadence defect was verified directly against the sealed baselines before being recorded. The two tooling notes are NOT independently verified here and are recorded as hunter reports.

## Stage EU — DEFECT FIXED: Italy could have killed a name that DID report
- Logged at 2026-09-22 14:11 UTC
- Found by the PHIL hunter, VERIFIED here before anything was changed. eMarket STORAGE is Borsa Italiana's appointed storage mechanism but it is NOT the only authorised one and it does NOT carry every Italian issuer. PHILOGEN is absent from its azienda dropdown (which runs PHARMANUTRA -> PIAGGIO & C. -> PIERREL), and eu_archive.day('it', d) on three dates Philogen is known to have filed returned 33 rows (2025-09-23, its own prior-year half-year), 99 rows (2026-03-27, FY-2025) and 24 rows (2026-08-17) with NO Philogen row on any of the three. The archive read cleanly every time — it returned a populated list, never None.
- That is the TRT mistake INVERTED and it was live. Italy is not ticker-keyed, so eu_archive.confirm() joins on a normalised company name; an issuer the mechanism does not carry falls through to 'the source WAS read, carries the day, and this issuer is not in it at all' and returns False — a retrospective kill on a company that reported. Resolving today's run tomorrow would have written event_occurred: false on PHIL.
- THE FIX, in the shape confirm() already used for Germany: eu_archive.confirm() gets an 'it' branch returning None (not False) on absence, with the measurement and the two working substitutes in the note. eu_market.CAPABILITY['it'] carries a new 'universal': False, and false_reachable() now requires 'universal' as well as a day/paged archive. 'universal' DEFAULTS TO TRUE via capability(), so a market nobody has checked is not silently exempted from kills — only Italy, which was measured, is.
- Verified after patching: false_reachable is now uk/fr/se/dk/no/fi True, de/es/pl/it False, and every other market's archive kind is untouched. scripts/smoke_test.py passes.
- The smoke test's own assertion was WRONG and was rewritten rather than worked around. It asserted 'event_occurred: false is reachable where a day archive exists' over (uk, fr, no, it, se) — encoding the very belief this measurement refuted. It now asserts the universal-archive rule, pins Italy as the measured exception, and asserts every other market is universal, so a future market added without measurement fails loudly instead of quietly gaining the power to kill.
- TWO SUBSTITUTES the hunter reached first try, for whoever builds the Italian confirmation path properly: borsaitaliana.it/azioni/documenti/calendariobilancidividendi/CDA_today.pdf (forward board meetings, exchange-side, every Italian issuer) and the per-ISIN news list. Neither is wired in; confirm() names them in its return note so the human call is cheap.

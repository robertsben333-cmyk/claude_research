# Run log — 2026-09-01

## Stage 0 — universe (07:17 CEST)
- Logged at 2026-09-01 05:19 UTC
- Window: After the US close on Tuesday 01 September 2026 through before the US open on Wednesday 02 September 2026
- Source: nasdaq (both after-close and before-open legs)
- Universe: 16 total (6 AMC, 10 BMO); 13 above the $500M market-cap floor; 12 eligible after qualification
- Excluded: 4 — GASS/YSG/SPWH below_market_cap_floor; BF.A no_options_market (Class A voting shares carry no active listed-options chain; BF.B, the optionable class, is kept)
- Notes: single-source fetch (nasdaq) succeeded on both legs with no network issues; no conflicting BMO/AMC timing observed to adjudicate. Verified options-market status for the six sub-$2B eligible names (CXM, FCEL, GIII, REX, DAKT) plus the BF.A/BF.B split via WebSearch since the API does not report it; all confirmed via option-chain listings. 12 eligible is above triage.skip_if_universe_at_or_below (10), so stage 1 will trigger.

## Stage 1 — triage
- Logged at 2026-09-01 06:43 UTC
- Mode: scouted (1 scout, batch of 12 — universe fit within triage.batch_size of 15)
- Funnel: 16 universe -> 12 eligible -> 10 tradeable -> 9 cleared floors -> 6 shortlisted
- Scouts: 1 subagent (sonnet/medium)
- Session mix: 4 AMC / 2 BMO
- Notable drops: FCEL (ai_edge 25 < floor 30, high-beta but unforecastable), REX & DAKT (tradeable: false, thin options liquidity), PANW (tied 50.5 with GIII on priority_score, dropped for AMC/BMO balance), OLLI (47.25, below cut), BF.B (37.25, formulaic quarter)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-09-01 08:24 UTC
- Shortlist (6, cap=triage.shortlist_size=6, no names dropped for cap): CRDO, MDB, GTLB, DELL, CXM, GIII
- Batch 1 (top 3 by priority_score): CRDO (73.75), MDB (66.0), GTLB (57.5)
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (wave_size=2) — wave 1: CRDO+MDB, wave 2: GTLB — publish after each wave

## Stage 2 — deep dive, batch 1 — FINISHED (08:54 UTC)
- Logged at 2026-09-01 08:54 UTC
- Researched: CRDO, MDB, GTLB
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves of wave_size=2 (wave 1: CRDO+MDB; wave 2: GTLB)
- Median evidence completeness: 80/100 (CRDO 78, MDB 84, GTLB 80)
- Panel-eligible after this batch: not computed — final batch only (batch 2 covers DELL, CXM, GIII)

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-09-01 10:23 UTC
- Shortlist: 6 names (cap=triage.shortlist_size=6, no names dropped for cap); batch 1 already covered CRDO, MDB, GTLB
- This batch: DELL, CXM, GIII
- Already on disk, skipping: none
- Plan: waves of 2 opus/high researchers (wave_size=2) — wave 1: DELL+CXM, wave 2: GIII — publish after each wave

## Stage 2 — deep dive, batch 2 — FINISHED (11:03 UTC)
- Logged at 2026-09-01 11:10 UTC
- Researched: DELL, CXM, GIII
- Skipped (already done): none
- Failed: none
- Subagents: 3 opus/high, in 2 waves of wave_size=2 (wave 1: DELL+CXM; wave 2: GIII)
- Median evidence completeness (this batch): 84/100 (DELL 84, CXM 78, GIII 84)
- 02-ranking.json written from all 6 dossiers (CRDO, MDB, GTLB, DELL, CXM, GIII); panel_priority = 0.45*|preliminary_direction_score| + 0.35*evidence_completeness + 0.20*change_expectation
- Panel-eligible after this batch, rank order: DELL (50.0), CXM (49.55), GIII (49.4), GTLB (49.4, tiebreak loser vs GIII on evidence_completeness), MDB (48.9), CRDO (48.8) — all 6 pass event_confirmed/evidence_completeness>=50/has-anchor; none excluded
- Notes for stage 3: CXM and GIII have no options-market implied move (both effectively illiquid options chains) — sized only off historical realised-move history (and, for GIII, a derived IV-term-structure inference flagged as such, not a market price); DELL's options-positioning read is thin (no IV rank/skew/borrow-fee, vendor APIs returned 403/503)

## Edge hunt — 2026-09-01 amc + 2026-09-02 bmo — STARTED
- Logged at 2026-09-01 14:10 UTC
- Window: 16 calendar rows (6 on 09-01 amc, 10 on 09-02 bmo), --window, no --include-unknown. Baselines sealed and pushed BEFORE any agent launched (commit 4c29a4d). Option-chain coverage 7/16 usable (CRDO DELL FCEL GTLB MDB OLLI PANW); ATM spread frac of mid 0.033-0.50 vs 0.41 on the 08-31 weekend run, so the 14:04 UTC / 10:04 NY fire time delivered the tight two-sided quotes it was moved for. No cadence_implausible flags fired; GASS verdict=suspect and PANW/CXM=unknown (PANW because all 28 prior prints on its CIK were filed under a former name, not a cadence defect). BF.A/BF.B baselines FAILED (bars_failed HTTPError/KeyError, dotted-symbol resolution) after one retry - they will enter the table as rankable:false with a stated reason rather than be measured worse. Plan: 1 edge-sweep over all 16; then hunters on at most 8 confirmed names (cap 20 = 1 sweep + (8+2) hunters + 8 adversaries = 19), two isolated hunters on the top 2 by hunt_priority; adversary once per ticker over every finding both sides; edge_score.py; edge-note.md. Shed by budget.edge_degrade_order (unconfirmed first, then lowest hunt_priority) while preferentially KEEPING the 7 names with a live chain, since those are the only ones where what-is-priced is measured rather than inferred from a run-up.

## Edge hunt — 2026-09-01 — sweep result and the shed
- Logged at 2026-09-01 14:23 UTC
- SWEEP: 16 of 16 rows event-confirmed from a company-issued scheduling release. PHANTOM RATE ZERO (08-31 run 1 was 8 of 8 phantom on time-not-supplied rows; run 2 was 0 of 10). Session confirmed for all 16; four rows (BF.A/BF.B, FCEL, REX, DAKT) have an intraday CALL time with a pre-open RELEASE and are correctly bmo - reading the call hour would have mislabelled them. Sweep found three real baseline defects: (a) a SYSTEMATIC former-name filter bug in priced_in.py zeroed the reaction history of PANW (all 28 prints on CIK 0001327567, cutoff 2026-08-27) and CXM (all 21 on CIK 0001569345, cutoff 2026-08-19); neither company changed its name, and two registrants producing the identical artefact two weeks apart is a bug, not two records events. (b) GASS 'suspect' is a FALSE POSITIVE - the 6-K matcher counted StealthGas' own 2026-08-28 SCHEDULING RELEASE as an earnings print, giving an impossible 5-day gap against an 88-day cadence. (c) YSG history holds a literal duplicate (2026-03-02 twice, identical -8.99%) plus a non-earnings 6-K five days before the real print. AMENDED symmetrically before any hunter launched: PANW unknown->fits_cadence, CXM unknown->fits_cadence, GASS suspect->unknown (all three upgrades company-sourced), YSG fits_cadence->unknown (downgrade, same FPI defect). Symmetry here means one standard applied, not an equal count - the sweep found no other name whose fits_cadence rested on a defect, and inventing a downgrade for numerical balance would be its own distortion. Note the upgrades land on names I hunt and the downgrade on one I drop; each is independently justified by a named defect and a company URL. SHED: cap 20 = 1 sweep + (8+2) hunters + 8 adversaries = 19, so 8 hunted names from 15 distinct companies. KEPT: SPWH(79) CXM(73) CRDO(71) FCEL(68) GTLB(62) PANW(58) DELL(53) MDB(47). DROPPED: GIII(65) REX(63) DAKT(57) YSG(55) GASS(51) OLLI(43) BF.B(39), plus BF.A(11) as a DUPLICATE of BF.B - one company, one release, two share classes; scoring both would double-count one event and pollute Spearman with a near-duplicate observation. DEVIATION FROM STRICT hunt_priority, recorded as the skill requires: GIII(65) REX(63) DAKT(57) outrank DELL(53) and MDB(47) and were dropped anyway. Policy applied was - keep the top 2 by priority regardless of chain (they take the double hunt), then fill on BASELINE MEASUREMENT QUALITY. DELL and MDB carry the two tightest chains of the day (ATM spread 0.033 and 0.115 of mid, full tier, trustworthy history); taking them over GIII/REX/DAKT lifts measured-baseline coverage in the hunted set from 4 of 8 to 6 of 8. Where a chain is unusable, priced_lean_pct falls back to -0.05x the 20-day run-up and 'expected move' is a historical median, so the agreement discount fires against a lean that was inferred rather than measured. OLLI(43) is the one chain name dropped - lowest priority of the seven and the widest spread (0.50). BF.A/BF.B also carry NO baseline at all (bars_failed on the dotted symbol), so they could not have been measured even if kept. Both enter the table as rankable:false with a stated reason - the visible loss the skill prefers over a name kept and measured worse. ALSO FIXED THIS RUN: scripts/edge_baseline_amend.py carried the 2026-08-31 AMENDMENTS table, and a stale table prints only 'SKIP no baseline' lines then 'DRY RUN', which reads exactly like 'nothing to amend' - it now exits non-zero when no entry matches a baseline in the target dir. Its printed upgrade/downgrade label also called every non-suspect change a downgrade, mislabelling unknown->fits_cadence and hiding whether a pass was symmetric; it now ranks by the event_q multiplier edge_score.py actually applies (suspect 0.05 < unknown 0.6 < fits_cadence 1.0). smoke_test.py passes.

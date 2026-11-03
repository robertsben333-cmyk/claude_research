# Run log — 2026-11-04

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-03 14:37 UTC
- Fired 14:36 UTC Tue 2026-11-03 (15:36 Amsterdam, markets open; sealed spots are intraday). Sealing for event date 2026-11-04 (Wed).
- Plan: eu_universe (cap 20) -> baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> 4-judge intl panel -> note. Pushing to main.

## Stage EU — universe and baselines sealed
- Logged at 2026-11-03 14:48 UTC
- 102 scheduled, 64 eligible, 20 drawn (seed eu-2026-11-04): uk 5, de 4, no 4, it 3, dk 2, se 1, fi 1; largest market uk 25%, 7 markets. es+pl 0. anchor_covered 8/20. All registers read (de dk fi it no se uk).
- SHED: SOLAR_B — the 2026-11-03 run hunted Solar's Q3 for 3 Nov (issuer's 2026 calendar lists 3 Nov; hunt research/2026/11/2026-11-03/europe/hunts/SOLAR_B.json). Today's row comes from nasdaq_fincal alone, with no release time. Hunting it again for 4 Nov would either count one print twice or hunt after the print.
- 19 to hunt in waves of 5: W1 BMW BSL EVK FRA PNDORA; W2 SAMPO BPE TEN TIT AKER; W3 BOUV ODF SOFF CHEF BTRW; W4 BUR LRE SNWS TRN. provenance stamped (orchestrator model not recorded: get_session unavailable).

## Stage EU — wave 1 partial
- Logged at 2026-11-03 14:52 UTC
- EVK banked: event_confirmed false — Evonik published Q3 on 2026-11-03 pre-open (press release https://www.evonik.com/en/news/press-releases/2026/11/Q3-2026.html); vendor 11-04 date is stale. No findings, impact 0.

## Stage EU — wave 1 banked
- Logged at 2026-11-03 14:58 UTC
- BMW -0.35, BSL -0.8, EVK 0 (event_confirmed false: Evonik reported 2026-11-03), FRA -0.2, PNDORA +0.5. All search_complete true. Wave 2 launched: SAMPO BPE TEN TIT AKER.

## Stage EU — wave 2 partial
- Logged at 2026-11-03 15:00 UTC
- TIT: event_confirmed false — TIM moved its Q3 board to 2026-11-10 (Teleborsa/Borsa Italiana 2026-10-06); vendor date stale.
- TEN: event_confirmed false for the sealed bmo window — Tenaris releases after the close on 11-04 (ir.tenaris.com invitation), reaction 11-05. Baseline is sealed and not revised; the real print is outside this run's window and is in no sample.

## Stage EU — wave 2 partial
- Logged at 2026-11-03 15:03 UTC
- BPE: event_confirmed false — BPER board 11-04, release 11-05 ~07:00 CET (emarketstorage calendar 2026-08-06, call invite 2026-10-27). Not rankable; scorer drops event_confirmed false.

## Stage EU — wave 2 banked
- Logged at 2026-11-03 15:05 UTC
- SAMPO +0.45, AKER +0.55, BPE/TEN/TIT event_confirmed false (not rankable). All search_complete true. Wave 3 launched: BOUV ODF SOFF CHEF BTRW.

## Stage EU — wave 3 banked
- Logged at 2026-11-03 15:13 UTC
- BOUV +1.2, ODF +0.6, SOFF +1.3, CHEF -0.5, BTRW -1.2. All event_confirmed, all search_complete. Wave 4 launched: BUR LRE SNWS TRN.

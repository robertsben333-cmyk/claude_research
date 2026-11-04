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

## Stage EU — wave 4 partial
- Logged at 2026-11-03 15:20 UTC
- SNWS -1.4, TRN -1.9, BUR +1.3. BUR session corrected by hunter: release 4 Nov 13:00 GMT (RNS 26 Oct), inside the London session, so session_check opens bmo; sealed baseline said amc (close 11-04 -> 11-05). Baseline not revised; eu_resolve reads the hunter's session_check.

## Stage EU — panel STARTED
- Logged at 2026-11-03 15:20 UTC
- 19/19 hunts banked, all search_complete. LRE +0.1. 15 ranked, none above floor 2.8; top BUR/SOFF +1.30, bottom TRN -1.90. Not ranked: EVK BPE TEN TIT (no event in window), SOLAR_B (shed). 15 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-11-03 15:28 UTC
- Sealed for 2026-11-04 (Wed) at ~14:45 UTC Tue (intraday spots). 102 scheduled, 64 eligible, 20 drawn; SOLAR_B shed (duplicate of 11-03); 19 hunted, all search_complete; 15 ranked; EVK BPE TEN TIT not ranked (no release in window: stale/wrong vendor dates). Top BUR/SOFF +1.30, bottom TRN -1.90; none above floor 2.8.
- Panel: 4/4 members, 15/15 each, no fallback (sonnet55 reported it skipped the hunter definitions). Selected BUR long (4/4, pct 85) and BSL short (3/4, pct 85). BUR's session corrected to in-session (13:00 GMT) by its hunter; baseline sealed amc, not revised.
- anchor_covered 7/20 sealed (6/15 ranked) — corrects the '8/20' in the seal entry. es+pl 0. Resolve by ~2026-11-12 (Nordic window). Pushing to main (EARNINGS_DATA_BRANCH=main).

## Close AMC — 2026-11-04
- Logged at 2026-11-04 11:17 UTC
- Guard mode --require-exit-tif opg exit 0 (amc_open, exit as market DAY). verify: 14 legs, none UNFILLED, nothing held. close --submit: no legs due today, nothing sent, no refusals. Account reachable.

## Stage M — morning exit review — STARTED
- Logged at 2026-11-04 14:15 UTC
- source research/2026/11/2026-11-03/edge-panel, 09:15 ET, 9 picks (ALAB CRCT DUOL FRSH MQ SEDG TARS TREE XPEL); 8 analysts launched, XPEL waiting on concurrency limit (8)

## Stage M — scored 2026-11-03
- Logged at 2026-11-04 14:16 UTC
- pool: 60 names / 9 days; review mean -0.17% (t -0.12), static +0.43% (t 0.31), review_minus_static -0.60 (t -1.22)

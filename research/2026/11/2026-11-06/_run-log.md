# Run log — 2026-11-06

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-05 14:37 UTC
- Fired 14:36 UTC Thu 2026-11-05 (15:36 Amsterdam, markets open; sealed spots are intraday). Sealing for event date 2026-11-06 (Fri). Plan: universe (cap 20), seal, one hunter per name in waves of 5, score, four-judge intl panel, note. Publishing to main.

## Stage EU — progress
- Logged at 2026-11-05 14:41 UTC
- Universe: 66 scheduled, 27 eligible ($100k floor), 20 drawn (seed eu-2026-11-06): uk3 de1 se4 dk2 no3 fi1 it3 es3; largest se 20%. 20 baselines sealed ~14:40 UTC (intraday spots). Provenance stamped. Wave 1 launched: AMS ATT BMPS CLNX DTG.

## Stage EU — progress
- Logged at 2026-11-05 14:49 UTC
- Banked 5/20: BMPS +0.15 (Intesa exchange offer pins it), DTG -0.6, ATT +0.2, AMS -1.1, EGTX 0 (event_confirmed false: Q3 released early 2026-11-05 07:30 CET with ANI SEK 11.25 recommended cash bid — a release that moved OUT of the window, not a phantom). ATT hunter: one curl to a consensus widget refused by auto-mode permission check (not a budget limit). Running CLNX GUBRA HAYPP HEX IAG.

## Stage EU — progress
- Logged at 2026-11-05 14:58 UTC
- Banked 11/20: +CLNX -0.4 (releases amc 11-05, sealed window still correct), GUBRA -0.8, HEX +0.1, HAYPP -1.5, LOG +0.4, IAG +0.1. DEFECT: UK register join missed IAG ('INTERNATIONAL CONSOLIDATED AIRLINES GROUP, S.A.' 1.36% on FCA 02/11) — sealed as 0.0; likely an issuer-name join bug on ', S.A.' suffixes in eu_positioning.py. Baselines not revised. Running ORK OUT1V PIA REC SCHO.

## Stage EU — progress
- Logged at 2026-11-05 15:06 UTC
- Banked 16/20: +REC +0.1, PIA +0.05 (releases in-session ~12:35 CET), OUT1V -1.1, ORK +0.85, TRUE_B 0 (PHANTOM: vendor date wrong — Q3 released 2026-11-03, next print 2027-02-17; event_confirmed false). Running SCHO SEA1 TBCG TES.

## Stage EU — panel STARTED
- Logged at 2026-11-05 15:11 UTC
- 20/20 hunts banked, all search_complete. 18 ranked, 2 not ranked (EGTX release moved to 11-05 with ANI bid; TRUE_B phantom, printed 11-03). None above floor 2.8. Top ORK +0.85, bottom HAYPP -1.50. 18 packs, four -intl- judges.

## Stage EU — Europe ranking — DONE
- Logged at 2026-11-05 15:19 UTC
- Sealed for 2026-11-06 (Fri) at ~14:40 UTC Thu (intraday spots). 66 scheduled, 27 eligible, 20 drawn (se 4 largest, 20%), 20 hunted, all search_complete; 18 ranked, EGTX (release moved to 11-05 with ANI bid) and TRUE_B (phantom, printed 11-03) not ranked. Top ORK +0.85, bottom HAYPP -1.50; none above floor 2.8.
- Panel: 4/4 members, 18/18 each, no fallback (sonnet55 skipped hunter definitions). Selected TBCG, OUT1V, HAYPP — all short, 4/4 (pct 98/91/91).
- Defects: UK FCA join miss on IAG (', S.A.' name, 1.36% sealed as 0.0); one ATT curl refused by auto-mode permission check. anchor_covered 1/20; es 3, pl 0, de 1. Resolve by ~2026-11-13. Pushing to main (EARNINGS_DATA_BRANCH=main).

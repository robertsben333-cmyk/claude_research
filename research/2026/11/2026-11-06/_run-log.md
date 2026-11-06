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

## Stage M — morning exit review — STARTED
- Logged at 2026-11-06 14:20 UTC
- source research/2026/11/2026-11-05/edge-panel, 09:20 EST, 8 picks (AAOI ETON FNKO GRND HNST OMDA SOUN TMDX), fired 09:17 EST (7 min late)

## Stage M — morning exit review — done
- Logged at 2026-11-06 14:21 UTC
- 8 names, compiled 09:21 EST: exit_open ETON AAOI SOUN GRND; exit_1000 OMDA FNKO; exit_limit HNST 4.87, TMDX 80.00. Prev morning (2026-11-05) resolved; pool 76 names/11 days review_minus_static -0.551 (t -1.34).

## Edge hunt (panel) — 2026-11-06 amc + 2026-11-09 bmo — STARTED
- Logged at 2026-11-06 18:12 UTC
- fired 18:06 UTC (13:08 ET, session started late by ~2 min). Universe 65 names (2 amc 11-06, 63 bmo 11-09), 65 baselines sealed 18:13 UTC. Plan: 1 edge-sweep, up to 20 unpriced-searcher, 4 judges; step 3s flatten, step 6b buy.

## Edge hunt (panel) — wave 1
- Logged at 2026-11-06 18:21 UTC
- 18:22 UTC. Sweep: 65 checked, 48 confirmed, 15 unconfirmed (incl. HE amc, CEG AMG WTTR LDI SEAT DOLE BCAX OFIX TLS AIOT CTEV ADCT ISPR MDCX), 2 no event in window (VRTS printed 10-30, MUX ~11-09 amc). Cap 20: unconfirmed shed first, then lowest hunt_priority among confirmed: SBET(48) IONS CEVA SGC TH OPAL NESR KMDA UNIT RDNT KGS IMVT SGI SOHU FERG RBA ROIV NRG KSPI GCMG CNH CGEN B KKR GSL IX TKC WHF shed. Hunted (20): TOMZ (amc today) + FRVO SOC HRTX DCTH QTRX LFMD VFF TNXP HAIN VIA OCUL TPB PRAX MPAA MNDY NRXS EVGO TGTX LINC. MPAA release hour unsettled (call 13:00 ET Mon). Wave 1 (8): TOMZ FRVO SOC HRTX DCTH QTRX LFMD VFF.

## Edge hunt (panel) — waves 2-3
- Logged at 2026-11-06 18:33 UTC
- 18:34 UTC. All 20 searchers launched (LINC last). Returned, search_complete true per hand-backs: TOMZ (no event: company moved Q3 to 2026-11-12 in a 10:30 ET release today) DCTH VFF QTRX FRVO SOC LFMD HRTX HAIN TNXP VIA TPB. Running: OCUL PRAX MPAA MNDY NRXS EVGO TGTX LINC. One launch (MNDY) refused at the 8-concurrent cap and relaunched.

## Edge hunt (panel) — step 3s sell
- Logged at 2026-11-06 18:42 UTC
- 20/20 searchers returned by 18:42 UTC (unpriced-searcher, native, Opus 5.5). hunt_status check --apply: 0 unfinished of 20; none retried. mode: execution enabled, amc_open. flatten --submit at 18:42 UTC: 4 positions still held from 2026-11-05's book (ETON 87 +17.12%, FNKO 573 +2.30%, HNST 684 +8.03%, OMDA 220 -17.08% unrealised as printed), all closed; flatten reported 'closed'. These amc legs were dated to exit at today's open but were still held at 13:42 ET.

## Edge hunt (panel) — panel STARTED
- Logged at 2026-11-06 18:42 UTC
- edge_score and V2 grounded written 18:43 UTC, before the first print. 19 rankable (TOMZ no event). Packs built; four judges, one part. Account flat after 3s.

## Edge hunt (panel) — panel done
- Logged at 2026-11-06 18:49 UTC
- 18:48 UTC: all four judges on pinned agents, 19/19 each, one part, no fallback, no retry. panel_score: selected (panel_pct >= 80, 4 present) HAIN S 99, DCTH L 90, VFF L 90 (3-of-4 rule: HAIN DCTH; VFF 3 of 4 also). Next QTRX S 78. Note written; stage E edge/ absent.

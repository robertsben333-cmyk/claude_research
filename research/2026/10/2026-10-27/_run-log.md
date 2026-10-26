# Run log — 2026-10-27

## Stage EU — Europe researcher — STARTED
- Logged at 2026-10-26 13:47 UTC
- Fired 13:35 UTC 2026-10-26 (Routine trig_018WGfdq2fUm1ZqJhCGQ1wde), session start 13:45 UTC. Sealing for event date 2026-10-27 (Tue), next European session. Plan: eu_universe (cap 20, $100k floor) -> seal baselines -> provenance -> one hunter per name in waves of 5 -> edge_score -> four-model intl panel -> note. No orders. Local main was a shallow clone unrelated to the force-updated origin/main; working on a local branch cut from origin/main 840103925, publish.sh pushes HEAD:main.

## Stage EU — universe and baselines sealed
- Logged at 2026-10-26 13:50 UTC
- Event date 2026-10-27. 57 scheduled, 40 eligible (uk 2, de 3, fr 4, se 10, no 4, fi 8, it 2, es 2, pl 5), 20 drawn (random, seed eu-2026-10-27): fi 5, se 4, de 3, no 2, pl 2, uk/fr/it/es 1 each. Largest market fi 25%, 9 markets. Baselines sealed ~13:50-13:51 UTC at intraday spots (European markets still open). session_unresolved: BEI, VIB3, GOFORE, VRLA, YACHT, BDX, KRU. ENC sealed amc. Registers: es/pl none; all others read. Provenance stamped (orchestrator model not passed; get_session not available). Wave 1 launched: BEI P911 VIB3 ENC FIA1S.

## Stage EU — short-register cache
- Logged at 2026-10-26 13:50 UTC
- eu-short-cache.json refreshed by the seal; committed so tomorrow's Nordic/IT short change is computable.

## Stage EU — wave 1 mostly banked, wave 2 launched
- Logged at 2026-10-26 14:00 UTC
- Banked: VIB3 +0.6, FIA1S -0.5, BEI -1.4, ENC -0.9 (ENC confirmed amc by issuer filing: window 27 Oct close -> 28 Oct close). P911 still running. Wave 2 launched early (4/5 of wave 1 banked): GOFORE GRK TIETO TYRES VRLA.

## Stage EU — session corrections from hunters
- Logged at 2026-10-26 14:11 UTC
- VRLA: sealed bmo (session_unresolved), issuer calendar says 'communiqué de presse après bourse' 27 Oct -> amc, true window 27 Oct close -> 28 Oct close. ENC: sealed amc, confirmed amc. YACHT and TYRES release intraday (inside the sealed window). Baselines not revised (sealed); eu_resolve.py measures both windows for unresolved sessions.

## Stage EU — BDX session
- Logged at 2026-10-26 14:13 UTC
- BDX: sealed bmo (session_unresolved); hunter infers amc from the last two quarterly filings (18:18, 19:33 Warsaw) -> likely window 27 Oct close -> 28 Oct close. Inferred, not observed.

# Run log — 2026-11-25

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-24 14:38 UTC
- Fired 14:38 UTC 2026-11-24 (15:38 Amsterdam, markets open; sealed spots are intraday). Sealing for event date 2026-11-25. Plan: universe -> baselines -> hunters in waves of 5 -> score -> 4-model panel -> note -> IBKR handoff.

## Stage EU — IBKR
- Logged at 2026-11-24 14:38 UTC
- mode: broker=IB Gateway on the executor's server (auth tws); this session only hands over. Last line: would refuse: IBKR_ENVIRONMENT is None but execution_eu.environment is 'live' (expected in the cloud: no broker env here).

## Stage EU — universe and baselines
- Logged at 2026-11-24 14:47 UTC
- 39 scheduled, 25 eligible (>= $100k), 20 drawn (seed eu-2026-11-25): uk 5, no 5, se 3, es 2, pl 2, de 1, fr 1, dk 1. Concentration: UK 25%, 8 markets. 20 baselines sealed (intraday spots, ~15:00 UTC). Hunters in waves of 5.

## Stage EU — hunters launched
- Logged at 2026-11-24 14:48 UTC
- First 8 (concurrency limit): EZJ PETS (uk) AT1 (de) MPCC (no) SECT_B (se) GRE (es) LOUP (fr) TXT (pl). Queued: HLCL IPX NRR BWO JACK NORSE SOFTX ROCK_A BIOA_B CANTA HBX MUR.

## Stage EU — hunts banked (partial)
- Logged at 2026-11-24 14:53 UTC
- Returned so far: TXT (hunter settles session as amc from issuer IR notice: H1 after the WSE close on 25 Nov, so the sealed bmo window holds no release), AT1, EZJ. HLCL launched.

## Stage EU — hunts banked (2)
- Logged at 2026-11-24 14:56 UTC
- Back: TXT AT1 EZJ MPCC PETS SECT_B LOUP (+NORSE file). LOUP hunter settles session amc (AMF flux timestamps 17:45 Paris on the last two results), so like TXT its print is outside the sealed bmo window. EZJ: under a 715p Apollo cash offer, event_confirmed false. Running: GRE HLCL IPX NRR BWO NORSE BIOA_B ROCK_A. Queued: JACK SOFTX CANTA HBX MUR.

## Stage EU — hunts banked (3)
- Logged at 2026-11-24 14:59 UTC
- 12/20 back (+BWO GRE NRR HLCL NORSE). NORSE: issuer moved Q3 to 2026-11-30 (NewsWeb 687104, 2026-11-20), event_confirmed false. All 20 launched; running IPX ROCK_A BIOA_B JACK SOFTX CANTA HBX MUR.

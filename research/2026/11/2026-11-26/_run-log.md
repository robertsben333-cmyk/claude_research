# Run log — 2026-11-26

## Stage EU — Europe researcher — STARTED
- Logged at 2026-11-25 14:38 UTC
- Fired 14:37 UTC 2026-11-25 (15:37 Amsterdam, markets open; sealed spots are intraday). Sealing for event date 2026-11-26 (Thu). Plan: universe -> baselines -> hunters in waves of 5 -> score -> 4-model panel -> note -> IBKR handoff. Local main had diverged from a rewritten origin/main (no merge base); working on a fresh branch at origin/main 2250fb921 and publishing to main.

## Stage EU — universe and baselines
- Logged at 2026-11-25 14:42 UTC
- 49 scheduled, 20 eligible (>= $100k), all 20 hunted (at the cap, no draw needed): uk 10, pl 6, no 2, se 1, dk 1. Concentration: UK 50%, 5 markets. 20 baselines sealed (intraday spots, ~14:45 UTC). Provenance stamped.
- IBKR mode: auth tws, executor server trades; cloud has no broker env (expected).
- Hunters: first 8 launched (concurrency limit 8): ACP CIG DIA ENT MDG VOX (pl) DFENS HUNT (no). Queued: PARKEN SANION CBOX CMCX FSG HFD IGP LTHM MAB PCIP SAFE SREI.

## Stage EU — hunts banked (1)
- Logged at 2026-11-25 14:47 UTC
- Back: HUNT (phantom: Q3 out 11-20, event_confirmed false), DFENS, ACP (hunter settles amc), CIG, DIA (amc), ENT (amc), VOX (date moved to 11-25 after close: window-equivalent bmo), MDG (amc likely), CBOX (released 11-25 07:00, a day before the vendor date; event_confirmed false). Running: PARKEN SANION CMCX FSG HFD IGP LTHM MAB. Queued: PCIP SAFE SREI.

## Stage EU — hunts
- Logged at 2026-11-25 14:54 UTC
- 20/20 hunted. 4 not ranked (no event in window): CBOX, IGP, PCIP (results released 24-25 Nov; 26 Nov is only an Investor Meet presentation), HUNT (Q3 out 20 Nov). Hunters settle ACP, DIA, ENT, MDG as amc (window close(11-26)->close(11-27)); VOX moved to 11-25 after close (window unchanged). 16 ranked, none above the 2.8 floor; top CMCX +1.20, bottom FSG -1.40.

## Stage EU — panel STARTED
- Logged at 2026-11-25 14:54 UTC
- 16 packs, four judges

## Stage EU — panel
- Logged at 2026-11-25 14:59 UTC
- 4/4 judges, no fallback. Selected (3 of 4 in own top 20%): CMCX 98 long (4/4), FSG 80 short (3/4). DIA 74 short (2/4).

## Stage EU — IBKR handoff
- Logged at 2026-11-25 14:59 UTC
- handoff written (before the note): 3 names, offline plan at sealed spots on EUR 10,000: BUY CMCX 50.0%, SELL FSG 29.2%, SELL DIA 20.8%. Not taken (< 70): ACP 68.0, DFENS 67.2, VOX 60.1. Caveat for the operator: DIA's hunter settles its release as amc on 26 Nov (after the Warsaw close), so a position held only to the 15:35 Amsterdam flatten on 26 Nov exits before the print.

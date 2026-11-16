# Run log — 2026-11-16

## Close AMC — exit Routine
- Logged at 2026-11-16 11:17 UTC
- Fired 11:10 UTC (06:10 ET). Guard `mode --require-exit-tif opg`: exit 0 (amc_open, amc -> open as market DAY).
- verify over 12 stage E runs / 14 exit legs: all ok, nothing still held, no UNFILLED legs.
- close --submit: no leg due today, so NO orders were placed and nothing was refused. Stage E's Routine is stopped since 2026-10-19; stage E-P's amc legs belong to E-PX, not this Routine.
- status: no open stage E positions; last legs (TRT, MANU, WOR) closed in September.

## Stage E-P amc exit — 2026-11-16
- Logged at 2026-11-16 14:10 UTC
- Fired 14:09 UTC (09:09 ET). Guards: live exit 0, paper exit 0 (amc -> open as market DAY, matched on placement). verify --fix: live 1 run / 0 exit legs; paper 20 runs / 2 exit legs, CURI amc ok 4303/4303 and CTVA amc ok 839/839, nothing UNFILLED, no rescues. close --today-only: live and paper sent NOTHING and refused nothing — no amc leg due today, because the 2026-11-13 E-P book had 0 positions on both accounts (alpaca-orders.json / alpaca-orders-live.json entries: []).

## Edge hunt (panel) — 2026-11-16 amc + 2026-11-17 bmo — STARTED
- Logged at 2026-11-16 18:15 UTC
- Fired 18:07 UTC (13:07 ET), an hour late against the 13:06 ET cron. Universe 70 names (43 amc 11-16, 27 bmo 11-17), 70 baselines sealed by 18:15 UTC. Plan: one edge-sweep, up to 20 unpriced-searchers (amc first, <=8 per turn), step 3s flatten live then paper, four judges, step 6b buy live then paper before 16:00 ET.

## Edge hunt (panel) — sweep and waves
- Logged at 2026-11-16 18:22 UTC
- Correction to the STARTED line: 18:07 UTC is 13:07 ET (EST), on time, not an hour late. Sweep: 70 names, 34 company-confirmed, 7 phantoms (RSSS WKHS CEPL SUPV GLBS SMWB GFUZ), 29 unconfirmed; short interest and trades_on left unknown by the sweep. Hunted 20 by budget.edge_degrade_order (unconfirmed shed first, then lowest hunt_priority): INFQ RCAT DUOT NXB OMER STEM TMS POCI OPRA WRAP POWL IMDX FTLF KLAR ELTK API AYTU YALA XBP GLAS (17 amc, 3 bmo). Shed confirmed on priority: MNSO BRFH AS HUYA ENR TME ESLT WB VIK JD DIS OCSL HD SR (several with option chains; no option-chain swap made, POWL RCAT KLAR in the hunt carry one). Wave 1 (8, 18:25 UTC): INFQ RCAT DUOT NXB OMER STEM TMS POCI.

## Edge hunt (panel) — waves 2+
- Logged at 2026-11-16 18:29 UTC
- 18:40-18:58 UTC: INFQ NXB POCI OMER STEM RCAT TMS returned, all search_complete true. Launched WRAP POWL IMDX FTLF API AYTU YALA as slots freed (8-concurrent limit hit once on AYTU, relaunched). Baseline amend: STEM suspect -> unknown (company rescheduled Q3 to Nov 16; matcher missed the 08-12 Q2 print); only hunted 'suspect' name; cadence_implausible names left at unknown.

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

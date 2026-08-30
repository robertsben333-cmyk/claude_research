# Run log — 2026-08-31

## Edge hunt — 2026-08-31 bmo — STARTED
- Logged at 2026-08-30 09:05 UTC
- First live run of stage E. Universe: 12 names from the Nasdaq calendar for 2026-08-31 session bmo, with --include-unknown because only 4 rows carry a confirmed pre-market time (SAIC, SY, LX, BLRX); the other 8 are time-not-supplied and may not be in the window at all.
- Baseline tiers: 1 full (SAIC), 4 partial (AIV, CHRN, FRGT, SY), 7 thin. Only SAIC has both a usable option chain and a reaction history: 9.39% event-implied move, +6.86 vol points of 25-delta skew, 23:1 put/call OI, 2.3% off its 52w high after a +7.5% 20-day run.
- Seven names are thin because they are foreign private issuers filing 6-K, which carries no item codes and no usable document description, so no reaction history is recoverable from EDGAR. Recorded unavailable rather than guessed; confidence on those names is capped at 50% in code.
- Budget: full fan-out would be 17 hunters against a 26-agent stage cap. Shedding via budget.edge_degrade_order step 1 (one_hunter_on_partial_names), except SY which keeps 2 as the only other name with a live option chain. Planned: 14 hunters, up to 12 adversaries.

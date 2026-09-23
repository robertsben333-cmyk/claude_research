# Run log — 2026-09-24

## Stage AU — Australia researcher — STARTED
- Logged at 2026-09-23 06:37 UTC
- Fired 06:37 UTC 2026-09-23 (16:37 Sydney). Sealing for the next ASX session, expected 2026-09-24.
- Plan: au_universe -> au_priced_in seal -> unpriced-hunter-au in waves of 5, one per name -> edge_score -> note. No orders.

## Stage AU — Australia researcher — DONE
- Logged at 2026-09-23 06:53 UTC
- 34 scheduled / 12 eligible / 12 hunted (no draw, under cap 20) / 4 rankable. session_unresolved 0. No name above floor 3.0. Ranked: AAR 0, SOL 0, PMV -0.5, PEN -1.0.
- 8 names not ranked (event unconfirmed): BCM CHN CXO GLN PNR RML VMM WIA. All map to the June-FY statutory annual report (due 30/09), which the vendor dates as a print. Late-September calendar defect: 8 of 12 hunts spent on it.
- AAR hunter set event_confirmed true on cadence alone (TRT pattern); check at resolve.
- Defect: au_priced_in history classifier misses 'Annual Report to Shareholders'/'Half-year Report' (CXO) and counts 'Quarterly Results Presentation' as results (PNR). Not fixed in this run; baselines are sealed.
- Defect: ASX announcement PDFs are RC4-encrypted with an empty password; eu_pdftext.py and WebFetch cannot read them. Hunters used ad-hoc scratch decryptors not in the repo.
- ASIC register 2026-09-17, lag 3 sessions. No resolved AU run, so lean_vs_free_control_rho unavailable (validation 0.80).

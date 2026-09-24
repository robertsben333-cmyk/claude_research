# Run log — 2026-09-25

## Stage AU — Australia researcher — STARTED
- Logged at 2026-09-24 06:41 UTC
- Fired 06:41 UTC 2026-09-24. Sealing for the next ASX session, expected 2026-09-25.
- Plan: au_universe -> au_priced_in seal -> unpriced-hunter-au in waves, one per name -> edge_score -> note. No orders.

## Stage AU — Australia researcher — DONE
- Logged at 2026-09-24 06:53 UTC
- 27 scheduled / 6 eligible / 6 hunted (no draw, under cap 20) / 0 rankable. session_unresolved 0. All 6 quarterly_report_only; all 6 hunters: event not confirmed, 0 findings.
- Defect (2nd day): late-Sept vendor rows for June-FY 5B filers are the statutory annual report (due 30/09), not a print. 6 of 6 hunts spent on it today, 8 of 12 on 09-24. A pre-hunt filter is warranted; not changed in this run.
- Register lag 3 sessions (ASIC 2026-09-18). ASX PDFs encrypted, eu_pdftext.py fails; hunters' scratch decryptors collided in shared /tmp.

## Stage EU — Europe researcher — STARTED
- Logged at 2026-09-24 13:39 UTC
- Fired 13:38 UTC 2026-09-24 (markets still open; sealed spot is intraday, not a close). Sealing for event date 2026-09-25 (Fri).
- Plan: eu_universe -> eu_priced_in seal -> one bilingual hunter per name by submarket, waves of 5, publish per wave -> edge_score -> note. No orders.
- Checkout: local main had diverged from origin/main (forced update, no ff); worked from a branch equal to origin/main b643b708, publishing with EARNINGS_DATA_BRANCH=main.

## Stage EU — universe and seal
- Logged at 2026-09-24 13:40 UTC
- 21 scheduled (uk 8, de 2, fr 2, it 4, pl 5; se/dk/no/fi/es 0), 2 eligible above $200k, 2 hunted, no draw. CHG (de) and VGO (pl); both session_unresolved (defaulted bmo), both history estimated_from_cadence, anchor_covered 0 of 2 (DE register read as of 09-23, CHG not named; PL has no register).

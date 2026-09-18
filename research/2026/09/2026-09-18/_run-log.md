# Run log — 2026-09-18

## Stage 0 — universe (05:13 UTC)
- Logged at 2026-09-18 05:15 UTC
- Window: After the US close on Friday 18 September 2026 through before the US open on Monday 21 September 2026
- Source: nasdaq
- Universe: 0 total (0 AMC, 0 BMO); 0 eligible after qualification
- Excluded: 0 (companies[] empty — nothing reached the eligibility check)
- Notes: Nasdaq returned rows (7 for 09-18, 8 for 09-21) but all but one carried time-not-supplied/unknown session; the one confirmed row (ABVX, amc on 09-21) does not fill the before-open slot. Per the qualification rule, unconfirmed-session rows are dropped rather than kept. Same pattern as 2026-09-17 (session_resolve.py may recover a real name from these later in stage E).

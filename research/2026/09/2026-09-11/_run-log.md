# Run log — 2026-09-11

## Stage 0 — universe (06:40 UTC / 08:40 CEST)
- Logged at 2026-09-11 06:41 UTC
- Window: After the US close on Friday 11 September 2026 through before the US open on Monday 14 September 2026
- Source: nasdaq
- Universe: 4 total (0 AMC, 4 BMO); 1 eligible after qualification
- Excluded: 3 (below_market_cap_floor: CODA, RFIL, HAIN)
- Notes: Weekend roll — Friday close side empty (0 AMC), before-open side rolled correctly to Monday 2026-09-14. CSHR ($0.70B) is the only name above the $500M floor; verified via WebSearch as Nasdaq-listed common (de-SPAC'd 2026-04-01, not a SPAC remnant), with an active listed-options market since 2026-04-16, and BMO timing confirmed by CoinShares' own IR release.

## Stage 1 — triage (06:52 UTC / 08:52 CEST)
- Logged at 2026-09-11 06:42 UTC
- Mode: skipped (universe <= threshold)
- Funnel: 4 universe -> 1 eligible -> 1 cleared floors -> 1 shortlisted
- Scouts: 0 subagents (skip mode)
- Session mix: 0 AMC / 1 BMO
- Notable drops: CODA (below_market_cap_floor), RFIL (below_market_cap_floor), HAIN (below_market_cap_floor) -- all dropped at stage 0, none reached triage

## Close AMC — 2026-09-11
- Logged at 2026-09-11 11:49 UTC
- Config change (operator instruction): orders.exit_mode uniform -> auction_split, flatten_before_entry true -> false in config/pipeline.yaml. Replication risk explicitly acknowledged and accepted by the operator; requirement is amc legs always exit at the opening auction.
- mode --require auction_split: PASS (exit 0) after the config change.
- close --scan 'research/*/*/*/edge' --submit: HOFT (bmo) not sent -- cls unavailable, market closed at 07:49:33 ET (correct, will go in at stage E's own run today). FEIM (amc) SENT opg 5cad5a24-b3f4-401e-8c68-f71b3ab6ca0a. ORCL (amc) SENT opg 58792a00-ceef-4810-8b21-c2ac9dc9c79a. RH (amc) SENT opg d53747ca-36bb-416b-9ea2-5f1323bc3ea8.
- status: all 3 opg exits queued (new, unfilled -- auction has not run yet). No refusals other than the expected HOFT/cls deferral.

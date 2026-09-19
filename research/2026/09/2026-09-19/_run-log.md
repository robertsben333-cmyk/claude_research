# Run log — 2026-09-19

## Stage EU — floor, France, day archives — RESTARTED
- Logged at 2026-09-19 01:22 UTC
- The 2026-09-18 attempt above died on a session rate limit before its first read, having written only its heartbeat. Nothing was built and nothing is half-done: the floor is still 1000000, there is no France register work and no DE/FR day archive. Restarted 2026-09-19 01:22 UTC against the same four tasks.

## Stage EU — tasks 1-3 done
- Logged at 2026-09-19 02:10 UTC
- 1. Turnover floor $1m -> $200k (config comment rewritten, not deleted). Measured forward over 10 sessions 2026-09-21..10-02: pooled median 2.5 -> 6.5 names/day, mean 2.8 -> 6.1, 28 -> 61 names; France median 0 -> 1/day. Cost carried in data: anchor_covered sealed per baseline, anchor_quality.direction pays a truncated zero 0.15 vs 0.45, eu_resolve reports by_anchor_covered. UK register names 80% of names >=$1m and 32% of the $200k-$1m band.
- 2. FRANCE SOLVED. www.data.gouv.fr is intermittent (~1 request in 3), not blocked; Phase 1 concluded blocked on four tries. Two retried hops -> object-api.infra.data.gouv.fr. 40,696 per-holder rows since 2012, 74 issuers with an open position, publication END dates so the change is reconstructed as of a past date and is backtestable.
- 3. DAY ARCHIVES for DE and FR (eu_archive.py). France = info-financiere.gouv.fr (AMF flux, 536,868 records, issuer's own filing category). Germany = EQS-News SEARCH, paginated, back years (the front page is what Phase 1 measured). Phantom: UK 2/90, FR 1/17, DE not measurable. Stream vs vendor: UK 1.7x, FR 3.6x, DE 0.78x in its August peak -- the UK undercount generalises to France and not to Germany.
- Also measured: Yahoo's European daily closes lag (.PA/.DE two sessions, .L one), so a European run cannot be resolved the morning after; rows now carry last_bar_date and move_pending.

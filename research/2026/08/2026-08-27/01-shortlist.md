# Stage 1 — Shortlist for 2026-08-27

Window: After the US close on Thursday 27 August 2026 through before the US open on
Friday 28 August 2026.

## Funnel

21 universe → 18 eligible → 18 cleared floors (min change_expectation 35, min ai_edge
30 — nothing dropped) → **6 shortlisted** (ranked cut at `shortlist_size: 6`).

Mode: scouted (2 `earnings-triage-scout` subagents, sonnet/medium, 9 tickers each).

## Shortlist

| Ticker | Session | change_expectation | ai_edge | priority | Rationale |
| --- | --- | --- | --- | --- | --- |
| AFRM | amc | 80 | 65 | 73.25 | BNPL fintech, history of violent post-earnings swings on GMV/credit-loss guidance; partner data (Shopify, Amazon) gives real edge |
| S | amc | 78 | 65 | 72.15 | IV >60%, up 42% YTD; cybersecurity peer read-throughs (CRWD, PANW) give synthesis real work to do |
| MRVL | amc | 75 | 62 | 69.15 | AI/custom-silicon narrative (AWS Trainium, hyperscaler concentration); supply-chain/customer-mix synthesis still pays despite heavy coverage |
| RBRK | amc | 78 | 55 | 67.65 | Cybersecurity/data-resilience name, track record of large post-print gaps on ARR/net-retention; consensus still forming |
| ESTC | amc | 75 | 55 | 66.00 | Small/mid-cap growth SaaS, history of sharp double-digit moves on billings/cloud-growth surprises |
| IREN | amc | 85 | 38 | 63.85 | Bitcoin-mining-to-AI-datacenter pivot, extreme volatility; ai_edge only just clears the floor — print is dominated by crypto price action research can't cleanly disambiguate |

## Warning for stage 2: session mix is 6/6 AMC

Every shortlisted name reports after Thursday's close. The four BMO names in the
eligible universe (FRO, HAFN, BWLP, MNSO — all reporting before Friday's open) all
scored below the cutoff, so Friday morning's open-window is unexamined by this
shortlist. The best of them (FRO 57.25, HAFN 57.25) were not close enough to the #6 cut
(IREN 63.85) to swap in without displacing a stronger AMC name, so the ranking was left
as scored rather than padded for balance.

## Notable drops (ranked out, not floor-failed)

All 18 eligible names cleared both floors — nothing was dropped for `timing_confirmed`,
`tradeable`, or the hard floors. These missed the top-6 cut on priority score alone:

| Ticker | Session | priority | Why it's a real loss |
| --- | --- | --- | --- |
| GAP | amc | 63.25 | Options imply ~11.5% move vs ~8.5% historical avg; tariff/margin guidance is a live, researchable question — narrowly missed the cut |
| ULTA | amc | 60.50 | Comp-sales/guidance reaction risk amid Sephora/Amazon competition; foot-traffic proxies offer real synthesis edge |
| PD | amc | 58.85 | Sub-$1B SaaS name prone to sharp NRR/ARR-guidance reactions; SaaS peer benchmarking (DDOG, NOW) adds signal |
| FRO | bmo | 57.25 | Tanker rates cyclical but trackable via Baltic index/spot-rate data — best BMO candidate, still 6.6pts below the cut |
| HAFN | bmo | 57.25 | Product tanker rates, alt-data-style edge via charter data and peer shipowner reports already out |

Low-edge names correctly screened out despite big expected moves: none — every name
that cleared the change_expectation floor also cleared the ai_edge floor this cycle
(closest case was IREN at ai_edge 38, kept in).

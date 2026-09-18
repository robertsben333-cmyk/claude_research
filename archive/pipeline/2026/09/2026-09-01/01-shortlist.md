# Stage 1 — Shortlist for 2026-09-01

**Window:** After the US close on Tuesday 01 September 2026 through before the US open
on Wednesday 02 September 2026.

**Funnel:** 16 universe → 12 eligible → 1 scout (batch of 12, no split needed since
`triage.batch_size` is 15) → 2 dropped as not tradeable (thin/no options liquidity) → 1
dropped below floors → 9 cleared both floors → **6 shortlisted**.

## Shortlist

| Ticker | Session | Event date | Change | AI edge | Priority | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| CRDO | amc | 2026-09-01 | 85 | 60 | 73.75 | AI-networking optics, history of 20-30%+ swings; hyperscaler capex + Marvell/Astera read-through gives real edge. |
| MDB | amc | 2026-09-01 | 75 | 55 | 66.0 | Violent (15-20%+) post-print history; open debate on Atlas growth durability vs. Postgres/vector-DB competition. |
| GTLB | amc | 2026-09-01 | 62 | 52 | 57.5 | Sizable (10-15%) historical swings; underexplored AI-coding-tool displacement debate rewards synthesis. |
| DELL | amc | 2026-09-01 | 58 | 55 | 56.65 | AI server backlog/margin trajectory is live and high-stakes; peer capex/GPU-supply read-throughs give edge. |
| CXM | bmo | 2026-09-02 | 55 | 55 | 55.0 | Thinly-covered small-cap SaaS; light sell-side attention leaves room for genuine NRR/customer-count edge. |
| GIII | bmo | 2026-09-02 | 55 | 45 | 50.5 | Meaningful historical swings on wholesale/tariff commentary; thin coverage still rewards read-through work. |

Session mix: 4 AMC / 2 BMO — tilts AMC-heavy but keeps tomorrow morning's window represented.

## Notable drops

- **PANW** (priority 50.5, tied exactly with GIII) — mega-cap security name; dense
  sell-side coverage leaves little unpriced and it historically grinds 4-8%, not double
  digits. Dropped for the shortlist's 6th slot in favor of GIII specifically to avoid an
  all-AMC top six (the top 5 by score were already all AMC reporters).
- **OLLI** (priority 47.25) — cleared both floors (change 45 / ai_edge 50) but ranked
  below the cut. Off-price retailer with a real edge angle (TJX/Burlington read-through)
  but a more moderate expected move than the six selected.
- **BF.B** (priority 37.25) — cleared floors narrowly (change 35, exactly at the floor;
  ai_edge 40) but the tariff/destocking narrative is already well covered and the print
  reads as formulaic; ranked last among the nine that cleared floors.
- **FCEL** (change 70, ai_edge 25) — dropped on the `min_ai_edge` floor (30). Violent,
  high-beta prints, but driven by cash-burn/contract-timing surprises and retail flow
  that public research can't reliably forecast — exactly the "moves a lot, nobody can
  call it" case this stage exists to filter out.
- **REX** and **DAKT** — dropped as `tradeable: false`. Both are small-cap names the
  scout flagged as likely having thin-to-no options liquidity, which stage 2/3 need to
  act on a call.

## Notes for stage 2

- All scores carry `evidence: "thin"` — the scout sourced earnings-date confirmations
  and qualitative catalysts but no implied-move, IV-rank, or short-interest figures for
  any of the 12 names (no `expected_move_hint` was returned). Stage 2's deep dives
  should not assume Phase-0 anchors (spot, implied move, historical realised moves) are
  already in hand; source them fresh.
- Single scout covered all 12 eligible names in one batch (`triage.batch_size` is 15,
  so 12 names needs no split) rather than the usual multi-scout fan-out.

# Stage 1 — Triage shortlist for 2026-08-18

Window: After the US close on Tuesday 18 August 2026 through before the US open on
Wednesday 19 August 2026.

## Funnel

29 universe → 21 eligible → 14 cleared floors → **6 shortlisted**

Scouted with 2 `earnings-triage-scout` subagents (Sonnet, medium effort), batches of
15 and 6. Floors: `change_expectation >= 35`, `ai_edge >= 30`, `timing_confirmed`,
`tradeable`.

## Shortlist

| Ticker | Session | Event date | Change | AI edge | Priority | Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| OPRA | bmo | 2026-08-19 | 65 | 68 | 66.4 | Under-covered multi-segment browser/ad/gaming name, sharp post-print move history |
| MRCY | amc | 2026-08-18 | 62 | 60 | 61.1 | Defense-electronics turnaround; contract/backlog data supports synthesis |
| VIK | bmo | 2026-08-19 | 58 | 58 | 58.0 | Booking-curve/capacity debate not fully priced in |
| TOL | amc | 2026-08-18 | 55 | 55 | 55.0 | Rate-sensitive homebuilder order/cancellation debate |
| WB | bmo | 2026-08-19 | 50 | 60 | 54.5 | China ad-spend proxy, peer (Baidu/Tencent/Alibaba) read-through already out |
| FLNG | bmo | 2026-08-19 | 45 | 62 | 52.65 | LNG charter-rate/dividend story, public spot TCE data sharpens the estimate |

Session mix: 4 BMO / 2 AMC. The tilt runs toward tomorrow's before-open window, not
away from it, so the morning window is not left unexamined.

## Notable drops

- **TGT** (68/62, priority 65.5) — highest-scoring name in the batch, dropped because
  the scout could not independently confirm event timing this run. Worth re-checking
  for stage 2 if a later pass confirms 2026-08-19 BMO.
- **ZIM** (70/45) — largest raw change_expectation in the universe (container-shipping
  rate volatility), dropped for the same unconfirmed-timing reason.
- **EL** (65/55) — Estee Lauder's China/travel-retail turnaround story scored well on
  both axes but timing was not reconfirmed.
- **LOW** (45/50) — timing not reconfirmed.
- **KC** — Kingsoft Cloud scored high on change_expectation (60) but flagged
  not tradeable (weak options liquidity) and ai_edge (25) below the floor — thin
  disclosure from a Chinese ADR caps what research can add.
- **LU** — Lufax has a large potential move (60) but conflicting event-date sources and
  opaque loan-book disclosure (ai_edge 30) put it right at the drop line on timing.
- **JKHY** — Jack Henry is a slow, predictable core-banking-tech name; both change
  expectation (25) and ai_edge (30) were the weakest in the batch.

## Warning for stage 2

Four of the six shortlisted names carry `evidence: "thin"` from the scout pass (OPRA,
WB, FLNG, and — on the retail side — none of the top 3, but note ADI/TJX/SQM also came
back thin and were not selected). The deep-dive researchers should expect to do real
sourcing legwork on OPRA, WB, and FLNG rather than relying on scout citations. Also
flag: TGT and ZIM were the two largest raw movers in the entire universe and were
dropped purely on unconfirmed timing, not on merit — worth a timing recheck before
next quarter's run if this keeps happening for mega-cap retail names.

# Earnings advice — 2026-08-19

Window: after the US close on Wednesday 19 August 2026 through before the US open on
Thursday 20 August 2026. 4 names deep-researched (of a 6-name shortlist — see Coverage),
1 panelled.

## The calls

**WOLF — Wolfspeed, Inc.** — **Neutral / No Edge** · unsigned band **7.7% … 24.6%**
(event-implied ≈15.5%) · P(down) 52% · certainty **Med** · reversal risk **High** (68.9)
Reason: panel splits narrowly negative (consensus −6.4) but no persona scored beyond
|18| — deteriorating fundamentals (3rd straight revenue decline, negative gross margin,
no FY27 frame yet) are fully offset by an ~80%-of-float short base that already squeezed
this identical setup upward once in May, on a worse print.
Caveat: reversal risk is High precisely because that squeeze-vs-fundamentals tension is
symmetric — it could break the print either way.
→ [full dossier](03-panel/WOLF-dossier.md)

## Ranked field

All names deep-researched today, ranked by `panel_priority` (rebuilt this stage — see
Coverage). "Prelim." is the stage-2 dossier's own preliminary direction score, shown
before the panel ever saw the name.

| Ticker | Company | Implied move | Prelim. score | Evidence | Panel priority | Panelled |
| --- | --- | --- | --- | --- | --- | --- |
| WOLF | Wolfspeed, Inc. | ≈15.5% (refreshed) | −20 | 84/100 | 56.8 | **Yes — Neutral / No Edge** |
| BILL | BILL Holdings, Inc. | ≈12.0% | +10 | 82/100 | 48.8 | No |
| BABA | Alibaba Group Holding Ltd | ≈6.6% | +10 | 82/100 | 48.2 | No |
| HOV | Hovnanian Enterprises Inc | unavailable | −15 | 72/100 | 45.95 | No |
| COTY | Coty Inc. | — | — | — | — | Not researched (see Coverage) |
| FUTU | Futu Holdings Limited | — | — | — | — | Not researched (see Coverage) |

BILL (AMC today) and BABA (BMO tomorrow) both have solid stage-2 evidence and a mild
positive preliminary lean; neither was panelled today under the budget degradation
below. HOV's dossier was itself thin (`evidence: "thin"` at triage) and carries no
implied-move anchor.

## What would change these calls

Cutting across the ranked field, the same two forces recur: (1) **short-base mechanics
overwhelming fundamentals** — WOLF's ~80%-of-float short position already did this once
in May; any near-term-relief print plus a credible forward frame likely forces covering
regardless of the headline numbers. (2) **FY2027 guidance, not the Q4 print, is the real
catalyst** for WOLF specifically — a credible non-GAAP gross-margin path and AI-datacenter
revenue framing flips the bull case; a still-negative-margin outlook or a fresh
equity/ATM raise flips the bear case. Neither direction was strong enough today for the
panel to commit to it.

## Coverage and caveats

- **Stage 2 shed scope.** The 6-name shortlist (WOLF, BABA, BILL, HOV, COTY, FUTU) only
  produced 4 dossiers. Batch 2's run log shows a plan to research BILL, HOV, COTY, FUTU
  in two waves, but only wave 1 (BILL, HOV) completed — no FINISHED or HALTED closing
  entry exists for batch 2, and no `02-ranking.json` was ever written. COTY and FUTU were
  never researched today.
- **Stage 3 rebuilt the ranking.** Per the panel-advice skill's explicit fallback for
  this exact failure mode, this stage built `02-ranking.json` itself from the 4 existing
  dossiers using `panel.rank_by` from `config/pipeline.yaml`, rather than blocking.
- **Panel size degraded from 2 to 1.** `config/pipeline.yaml` already runs `panel.names:
  2` (the first step of `budget.degrade_order`, applied structurally since 2026-08-13).
  Because stage 2 additionally shed scope today and left no closing log entry — the
  pipeline's established signature of a session running out of budget mid-stage — this
  stage applied the next step in the same order and panelled only the top-ranked name,
  WOLF, rather than risk a two-name panel getting cut off mid-run.
- **WOLF's spot anchor moved materially intraday.** Stage 2's anchor ($31.46, prior
  close) was ~12% stale by print time; a same-day WebSearch refresh by the chair could
  not resolve a clean figure, but two of the seven independent personas separately found
  and cited a fresher, sourced quote ($27.91, −11.3% intraday, 11:57 ET, stockanalysis.com)
  — used in the final anchor packet and dossier.
- **Shared secondary sourcing on short interest.** Six of seven WOLF personas
  independently cited the same aggregator (optionstradingreport.com) for the
  ~47%-of-shares-out / ~932%-borrow-fee figures, which are themselves unreconciled
  against a materially lower live-feed borrow estimate (~2–4.6%, ChartExchange/IBKR).
  Directional conclusions from that shared fact diverged across personas (both signs
  appear), so it was not treated as inflated agreement, but the underlying number
  should be read with caution — see the dossier's independence note.
- **HOV's evidence was thin at triage** (`evidence: "thin"`) and carries no implied-move
  anchor; treat its ranking as lower-confidence than the others even before any panel.

This is research, not financial advice. Earnings reactions are highly uncertain and
can be driven by market positioning, guidance, macro conditions, and management
commentary rather than reported results alone.

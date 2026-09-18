# Earnings advice — 2026-08-26

Window: after the US close on Wednesday 26 August 2026 through before the US open on
Thursday 27 August 2026. 4 names deep-researched (of a 6-name shortlist — see Coverage),
2 panelled.

## The calls

**OKTA — Okta, Inc.** — **Neutral / No Edge** · unsigned band **6.7% … 31.6%**
(event-implied ≈13.0%, refreshed) · P(down) 50% · certainty **High** · reversal risk
**High** (60.5)
Reason: panel genuinely splits — Fundamental and Options & Positioning independently
score −18 on cRPO-deceleration/valuation risk while Sentiment, Base-Rates and
Macro/Peers score +8 to +12 on de-risked positioning and Okta's habit of beating its
own conservative guides.
Caveat: reversal risk is High because OKTA has printed both a +30% squeeze and two
−16%/−18% "good quarter, conservative guide" reactions within its last eight prints.
→ [full dossier](03-panel/OKTA-dossier.md)

**DLTR — Dollar Tree, Inc.** — **Neutral / No Edge** · unsigned band **4.9% … 23.3%**
(event-implied ≈10.51%, refreshed) · P(up) 51.8% · certainty **High** · reversal risk
**Med** (59.7)
Reason: no persona scored beyond |18| — Fundamental and Options & Positioning lean on a
genuine traffic-led comp inflection while Sentiment and Base-Rates lean on an implied
move that is rich versus DLTR's own realised history and an already-de-risked setup.
Caveat: Dollar General reports the same morning, and DLTR's worst historical prints
have all been guidance resets.
→ [full dossier](03-panel/DLTR-dossier.md)

## Ranked field

All names deep-researched today, ranked by `panel_priority` (rebuilt this stage — see
Coverage). "Prelim." is the stage-2 dossier's own preliminary direction score, shown
before the panel ever saw the name.

| Ticker | Company | Implied move | Prelim. score | Evidence | Panel priority | Panelled |
| --- | --- | --- | --- | --- | --- | --- |
| OKTA | Okta, Inc. | ≈13.0% (refreshed) | +10 | 84/100 | 49.1 | **Yes — Neutral / No Edge** |
| DLTR | Dollar Tree, Inc. | ≈10.51% (refreshed) | −10 | 84/100 | 48.7 | **Yes — Neutral / No Edge** |
| NTNX | Nutanix, Inc. | ≈14.49% | −10 | 84/100 | 47.9 | No |
| STDN | Standard Nuclear, Inc. | unavailable | −15 | 62/100 | 44.45 | No — excluded (see Coverage) |
| URBN | Urban Outfitters, Inc. | — | — | — | — | Not researched (see Coverage) |
| CRWD | CrowdStrike Holdings, Inc. | — | — | — | — | Not researched (see Coverage) |

NTNX (AMC today) has solid stage-2 evidence and a mild negative preliminary lean but
was not panelled today under the panel-size cap. STDN was researched but is excluded
from panel eligibility entirely — it IPO'd in July and has neither an implied-move
anchor nor enough trading history to size a move against.

## What would change these calls

Both calls turn on the same underlying question: **is the print's headline strength
real demand or something the market already expects and has priced?** For OKTA, the
question is whether the Q3 cRPO guide accelerates past the 11% level guided for Q2 —
an acceleration validates the bull case regardless of the rich ~33x forward multiple; a
guide held flat at ~11% is the exact setup behind OKTA's two worst historical prints.
For DLTR, the question is whether the comp beat is traffic-led (rewarded this earnings
season, as Ross was) or tariff-refund-flattered with a decelerating core comp (punished,
as Walmart was) — a large excluded tariff refund could flatter the headline while the
underlying comp merely meets guidance. Both names also carry elevated reversal risk
because both have a history of "good quarter, conservative guide" selloffs that a
merely in-line print could repeat.

## Coverage and caveats

- **Stage 2 shed scope in both batches.** The 6-name shortlist (OKTA, STDN, URBN, DLTR,
  NTNX, CRWD) produced only 4 dossiers. Batch 1's run log shows a plan for OKTA, STDN,
  URBN, but URBN was never published and batch 1 has no FINISHED/HALTED closing entry.
  Batch 2 planned DLTR, NTNX, CRWD but CRWD was never published after wave 1 (DLTR,
  NTNX) completed, and batch 2 also has no closing entry.
- **Stage 3 rebuilt the ranking.** Per the panel-advice skill's explicit fallback for
  this exact failure mode, this stage built `02-ranking.json` itself from the 4 existing
  dossiers using `panel.rank_by` from `config/pipeline.yaml`, rather than blocking.
- **Panel size held at the config default of 2, not cut further to 1.** Stage 2's
  missing closing log entries match the exact signature that triggered a further
  panel.names cut (2 → 1) on 2026-08-19. That cut was not applied here: this stage's
  own panel budget (14 subagents = panel.names 2 × 7 personas) held, and both
  seven-persona panels (OKTA, DLTR) completed and were published in full before this
  note was written. Discarding either after the fact would have wasted validated work
  for no budget benefit.
- **Both spot prices and implied moves were refreshed today**, ~20 hours after stage 2's
  pre-market anchors. OKTA: spot $130.61 → $128.95, implied move 12.99% → 13.0%. DLTR:
  spot $134.48 → $133.21, implied move 9.2% → 10.51%. Both refreshed reads came from
  aggregated WebSearch snippets (`snippet_only`) rather than a direct exchange/vendor
  fetch — treat the exact decimal as indicative, not tick-precise.
- **STDN was researched but excluded from panel eligibility** — no implied-move anchor
  and no usable historical-move history (thin trading record since its July IPO), so
  there was nothing to size a move against.
- **NTNX was ranked but not panelled** purely on the panel-size cap, not on any evidence
  concern — its dossier evidence_completeness (84/100) matches OKTA's and DLTR's.

This is research, not financial advice. Earnings reactions are highly uncertain and
can be driven by market positioning, guidance, macro conditions, and management
commentary rather than reported results alone.

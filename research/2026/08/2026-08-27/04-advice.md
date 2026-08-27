# Earnings advice — 2026-08-27

Window: after the US close on Thursday 27 August 2026 through before the US open on
Friday 28 August 2026. 5 names deep-researched (of a 6-name shortlist; IREN was never
researched — see Coverage below), 2 panelled.

## The calls

### ESTC — Elastic N.V.
**Neutral / No Edge**  ·  unsigned band 6.7%–27.8% (event-implied ≈ ±12.9%)  ·  P(down) 57.1%  ·  certainty High
An unusually aligned seven-persona panel (disparity 8.7/100) leans mildly bearish but
falls just short of a directional call — spot ($84.66) already sits at/above the
sell-side mean target after a same-day +6.8% pop on top of a three-month +55% run, so a
beat looks largely priced.
Caveat: Elastic has a specific, well-documented pattern of beating and still falling on
guidance optics (most recently -26.49% in Aug-2024). Reversal risk High (64.1).
→ `03-panel/ESTC-dossier.md`

### AFRM — Affirm Holdings, Inc.
**Neutral / No Edge**  ·  unsigned band 5.4%–22.9% (event-implied ≈ ±10.55%)  ·  P(down) 49.8%  ·  certainty Med
A genuinely split panel (4 personas up, 3 down, disparity 28.0/100) nets to a coin-flip
consensus — the FQ4 headline beat is near-certain, but direction hinges entirely on
Affirm's first FY2027 GMV/margin/credit guide, which no anchor can price in advance.
Caveat: the exact precedent exists — Affirm beat cleanly and raised guidance in Feb-2026
and still fell 14.47% on a credit-provision jump. Reversal risk High (60.6).
→ `03-panel/AFRM-dossier.md`

## Ranked field

All five names that completed deep-dive research today, ranked by panel priority
(0.45×|preliminary direction score| + 0.35×evidence completeness + 0.20×change
expectation, per `config/pipeline.yaml`). See "Coverage" below for why this ranking was
built by stage 3 rather than stage 2.

| Ticker | Company | Implied move | Preliminary read | Evidence completeness | Panelled |
| --- | --- | --- | --- | --- | --- |
| ESTC | Elastic N.V. | ±12.9% | -20 (Med conviction) | 84/100 | Yes |
| AFRM | Affirm Holdings | ±10.55% | -18 (Med conviction) | 82/100 | Yes |
| S | SentinelOne, Inc. | ±11.36% | -15 (Low conviction) | 84/100 | No |
| MRVL | Marvell Technology | ±10.28% | -15 (Med-Low conviction) | 85/100 | No |
| RBRK | Rubrik, Inc. | ±12.9% | -10 (Low conviction) | 85/100 | No |

S, MRVL and RBRK were fully deep-dived (dossiers at `02-dossiers/<TICKER>.md/.json`) but
ranked below the panel cutoff (panel.names=2). Their preliminary reads are stage-2's own
single-analyst read, not panel-verified, and carry no independence guarantee — treat them
as leads for further reading, not calls.

## What would change these calls

- **ESTC:** A CRPO growth print at or above ~20% paired with an FY27 revenue raise
  toward $2.03B+ and no margin walk-down from the Deductive AI deal would flip this
  toward Lean Up; a guide that merely restates the current ~14.6% growth framework
  (the base case several personas expect) keeps it at best flat-to-down, consistent with
  Elastic's last two prints.
- **AFRM:** An FY2027 guide that holds the medium-term framework intact (>25% GMV
  growth, RLTC and margin broadly in line) with delinquencies flat-to-down YoY would tip
  this up; a guide below that framework, or a visible step-up in credit-loss
  provisioning echoing the Feb-2026 pattern, tips it down. Sector read-through (Klarna,
  Sezzle both fell on guidance this month despite beating) argues the market is primed
  to punish caution.
- Across both names, the same mechanism dominates: **the print is not the event, the
  guide is** — both companies are giving forward-year or forward-framework guidance for
  the first time in a while, and every persona that built a bear case built it on
  guidance optics, not on the quarter itself.

## Coverage and caveats

- **Stage 2 did not close.** Batch 2 was logged as STARTED (RBRK, ESTC, IREN planned)
  but no FINISHED or HALTED entry was ever written, and IREN's dossier does not exist.
  Stage 3 rebuilt `02-ranking.json` from the five dossiers that do exist, using the
  configured `panel.rank_by` formula — this is the same recovery pattern used on
  2026-08-26, when stage 2 also failed to close its ranking step.
- **ESTC's implied move could not be refreshed intraday.** It carries the stage-2
  derivation (two-expiry variance decomposition, as of 2026-08-26T15:59:59 ET) because
  ESTC has no weekly options and the decomposition could not be safely re-run today; a
  fresh raw monthly straddle read (17.54%) is directionally consistent (vol still
  elevated) but is not a like-for-like substitute.
- **Historical move data is order-suspect on both names.** Multiple independent
  personas — without seeing each other's work — flagged that the `historical_moves_pct`
  list handed to them did not reconcile with what they found in independent research
  (e.g. ESTC's May-2026 reaction looks like roughly -9% to -15%, not the list's
  labelled-most-recent -26.49%; AFRM's list appears ordered oldest-first). The panel was
  told to treat the anchors as given per the no-fabrication rule; this is flagged here
  rather than silently corrected, since the underlying stage-2 sourcing should be
  checked before the next run reuses it.
- **Panel seats:** 14/14 filled on the first attempt, no retries needed, no chair
  overrides on either name.
- **Budget:** panel.names stayed at its configured default of 2; no further degradation
  from `budget.degrade_order` was needed today.

---

This is research, not financial advice. Earnings reactions are highly uncertain and
can be driven by market positioning, guidance, macro conditions, and management
commentary rather than reported results alone.

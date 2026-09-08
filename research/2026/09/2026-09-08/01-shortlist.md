# Stage 1 — Triage shortlist — 2026-09-08

**Window:** After the US close on Tuesday 08 September 2026 through before the US open
on Wednesday 09 September 2026

**Funnel:** 24 universe → 15 eligible → 15 cleared floors → 6 shortlisted

**Mode:** scouted (1 `earnings-triage-scout` subagent, sonnet/medium, batch of 15 — one
batch covers the whole eligible universe since 15 ≤ `triage.batch_size` of 15)

**Floors:** `min_change_expectation` 35 · `min_ai_edge` 30 — nothing was dropped for
floors today; all 15 eligible names cleared both. The cut to 6 was entirely on
`priority_score` rank (`priority = 0.55 × change_expectation + 0.45 × ai_edge`).

**Session mix:** 3 AMC (BRZE, CASY, AVO) / 3 BMO (SAIL, CHWY, ODD) — balanced, no tilt.

## Shortlist

| Ticker | Session | Change Exp. | AI Edge | Priority | Evidence | Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| SAIL | bmo | 72 | 63 | 67.95 | thin | Re-IPO'd identity-security SaaS with a live guidance debate and ARR-trajectory questions; peer data (CyberArk, Okta) supports differentiated synthesis. |
| BRZE | amc | 70 | 62 | 66.40 | thin | Narrow guided revenue band ($219.5-220.5M); peer CDP data (Klaviyo, Iterable) gives a differentiated read on net retention. |
| CHWY | bmo | 72 | 58 | 65.70 | good | ~10% implied move against a tight guided revenue band; autoship/active-customer data offers real, heavily-picked-over edge. |
| CASY | amc | 74 | 55 | 65.45 | good | ~6.9% implied move but realized moves run hotter on fuel-margin surprises, which public wholesale fuel pricing can partially triangulate. |
| AVO | amc | 68 | 55 | 62.15 | good | Commodity-margin story (avocado costs); public Mexican/Peruvian pricing data gives real edge on the margin question that has burned this stock before. |
| ODD | bmo | 65 | 58 | 61.85 | thin | Small-cap DTC beauty-tech, history of sharp swings and past short-seller scrutiny; app/e-commerce trend data offers a differentiated growth-quality read. |

Half the shortlist (SAIL, BRZE, ODD) is flagged `evidence: thin` by the scout — worth a
harder push for primary sources (filings, transcripts, peer comps) early in the stage 2
dossier rather than leaning on secondary summaries.

## Notable drops (cleared floors, cut on rank)

- **TTAN** (ServiceTitan) — priority 59.15, 7th place, missed by ~2.7 points. Young
  vertical-SaaS IPO with only a few quarters of public history and mixed past reactions;
  thin track record capped `ai_edge` at 52.
- **ASO** (Academy Sports) — priority 58.00, 8th. Genuine consumer-spending/tariff
  read-through but scored a notch below the cut on both axes.
- **SIG** (Signet Jewelers) — priority 56.35, 9th. Guidance was already raised ahead of
  this quarter, narrowing surprise room versus the shortlisted names.
- **JMKE** (Jersey Mike's Subs) — priority 55.65, 10th. Highest raw `change_expectation`
  in the batch (75) — barely six weeks public — but `ai_edge` of 32 sits just above the
  floor: there is almost no track record to research against.

No name was dropped by the hard floors today; the screen did all its work on rank.

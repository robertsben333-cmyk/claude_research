# Stage 1 — Triage shortlist for 2026-08-13

**Window:** After the US close on Thursday 13 August 2026 through before the US open on
Friday 14 August 2026.

**Mode:** Scouted (universe eligible = 23, above the skip threshold of 10).

## Funnel

| Stage | Count |
| --- | --- |
| Universe (total fetched) | 114 |
| Eligible (passed stage-0 liquidity/timing/cap filters) | 23 |
| Screened by triage scouts | 23 (2 batches, 15 + 8) |
| Dropped — unconfirmed timing / untradeable / below floors | 6 |
| Cleared both floors (`change_expectation ≥ 35`, `ai_edge ≥ 30`) | 17 |
| Shortlisted (top 10 by priority score) | 10 |

`priority_score = 0.55 × change_expectation + 0.45 × ai_edge`

## Shortlist

| Ticker | Session | Change Exp. | AI Edge | Priority | Rationale |
| --- | --- | --- | --- | --- | --- |
| GLOB | amc | 75 | 68 | 71.85 | GenAI-disruption-to-demand narrative, peers already reported, history of violent guidance gaps. |
| DLO | amc | 72 | 66 | 69.30 | LatAm cross-border payments; violent history on take-rate/FX; complex flow-through rewards synthesis. |
| STNE | amc | 70 | 62 | 66.40 | Brazilian fintech; sharp historical moves on take-rate/credit trends; macro + competitive complexity. |
| AMAT | amc | 62 | 68 | 64.70 | Semicap swings hard on China export controls and AI capex commentary; deep, liquid options market. |
| HAWK | amc | 68 | 60 | 64.40 | Small-cap RF-geolocation/space-intel; contract cadence and backlog under-analyzed but piece-able. |
| SGML | bmo | 65 | 55 | 60.50 | Lithium producer, pre-announced production beat; move hinges on trackable pricing/cost trajectory. |
| GLAS | amc | 65 | 55 | 60.50 | Cannabis cultivator sensitive to wholesale flower pricing and rescheduling headlines. |
| NMAX | amc | 80 | 35 | 59.75 | Meme-like historical swings; large expected move but ai_edge only just clears the floor. |
| ETON | amc | 60 | 55 | 57.75 | Specialty pharma with recent launches; script/formulary data allow real launch-curve triangulation. |
| NKTR | amc | 75 | 30 | 54.75 | Large expected move but ai_edge sits exactly at the floor — reaction hinges on unknowable trial data. |

**Session mix: 9 AMC / 1 BMO.** The shortlist is heavily AMC-tilted — not by design, it's
simply how the top-10 priority scores fell. The next-best BMO names (USAS 49.9, TMS 44.65,
RLX 43.75) were materially lower-scored than the AMC names they'd have displaced, so no
swap was made. Stage 2/3 should note the next US pre-open window (Fri 14 Aug) is thin in
this batch.

## Notable drops

| Ticker | Change Exp. | AI Edge | Reason dropped |
| --- | --- | --- | --- |
| BLTE | 80 | 25 | Failed `ai_edge` floor — clinical-stage ophthalmology biotech, print is a formality, real driver is an unknowable trial/regulatory binary. |
| TMC | 80 | 25 | Failed timing — sources conflict on report date (Aug 13 vs Aug 17); also would have failed the `ai_edge` floor (deep-sea-mining political catalyst, unforecastable). |
| SPRY | 60 | 55 | Failed timing — session conflict across sources (bmo vs amc); would otherwise have cleared both floors comfortably. Re-check timing before stage 2 if this recurs. |
| SIND | 55 | 20 | Untradeable — thinly documented recent listing, no real public track record found, options liquidity unconfirmed. |
| MFP | 45 | 22 | Untradeable — obscure recent-listing food processor, minimal public coverage. |
| RMIX | 50 | 22 | Untradeable — recently-listed concrete/construction name, thin history, uncertain options liquidity. |

Also outside the top 10 but cleared both floors: RLX (43.75, bmo — opaque PRC regulatory
risk caps `ai_edge` at 30), TMS (44.65, bmo), HTFL (47.4, amc), BAP (48.1, amc), KLC
(49.1, amc), USAS (49.9, bmo), JCAP (52.75, amc).

## Warning for stage 2

Every scout returned `evidence: "thin"` and `expected_move_hint: null` across all 23
names — no implied-move, IV-rank, or short-interest figures were sourced at this cheap
pass. This is expected at triage depth, but stage 2 dossiers should not assume any
Phase-0 anchors are already populated; they still need to source spot price, implied
move, and historical realised moves from scratch. Two shortlisted names sit exactly at
the `ai_edge` floor (NMAX 35, NKTR 30) — worth extra scrutiny in the deep dive on whether
they're worth the dossier slot, and TMC's earnings-date conflict is worth re-checking
before tomorrow's stage 0 run in case it reports on a different day than assumed.

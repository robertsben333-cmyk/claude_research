# Stage 1 — Shortlist for 2026-09-08

Window: after the US close on Tuesday 08 September 2026 through before the US open on
Wednesday 09 September 2026.

Run by hand inside the stage 2 batch 1 session, because stage 1's own Routine had not
published by 08:23 UTC (10:23 CEST) — nearly two hours past its 08:38 CEST slot — and
the deep-dive skill directs a stage 2 session to run triage itself rather than lose the
day when the shortlist is merely late. See `_run-log.md`.

**Funnel:** 24 universe -> 15 eligible -> 11 cleared floors -> 6 shortlisted.

- Scouts: 1 subagent (sonnet/medium), single batch of all 15 eligible names
- Floors: `min_change_expectation` 35, `min_ai_edge` 30
- Session mix: 2 AMC (TTAN, BRZE) / 4 BMO (CHWY, SAIL, ASO, SIG) — tilts BMO, consistent
  with the day's underlying 5 AMC / 10 BMO eligible split rather than a triage artifact

## Shortlist

| Ticker | Session | Change Exp. | AI Edge | Priority | Evidence | Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| TTAN | amc | 70 | 55 | 63.25 | thin | Recent high-growth IPO trading unprofitably, elevated growth-stock volatility on guidance; limited historical print data caps synthesis. |
| BRZE | amc | 65 | 60 | 62.75 | thin | Unprofitable growth SaaS with decelerating revenue growth as a live guidance question; 7 analysts give enough dispersion for billings/NRR synthesis. |
| CHWY | bmo | 60 | 55 | 57.75 | good | History of sharp post-earnings moves on active-customer/margin trends; alt-data (app usage, autoship) synthesis can add value despite heavy coverage. |
| SAIL | bmo | 55 | 60 | 57.25 | thin | Recently re-IPO'd identity-security SaaS; ARR/NRR trajectory under-modeled, peer read-throughs (CyberArk, Okta) add signal. |
| ASO | bmo | 55 | 55 | 55.00 | thin | Mid-cap sporting-goods retailer, comp-sales/guidance sensitivity, thin coverage (4 analysts), consumer-spending read-throughs from peers already reported. |
| SIG | bmo | 55 | 50 | 52.75 | thin | Discretionary jewelry retailer with a history of large post-print moves; moderate coverage leaves room for bridal/engagement-trend synthesis. |

## Dropped for shortlist_size (cleared floors, not selected)

| Ticker | Priority | Note |
| --- | --- | --- |
| CNM | 46.75 | Water/wastewater distributor, thin coverage (2 analysts) — solid ai_edge but lower change_expectation. |
| SUNB | 46.50 | First print since March 2026 IPO, only 1 analyst — thin track record capped ai_edge. |
| AVO | 45.00 | Avocado pricing/crop-timing swings; commodity data gives some edge but moderate change_expectation. |
| INNV | 43.25 | Small-cap PACE healthcare provider — regulatory/reimbursement risk hard to pre-empt. |
| CASY | 39.50 | Mega-cap convenience grinder; well-covered, little edge left on the table. |

## Dropped for floors / tradeability

| Ticker | Reason |
| --- | --- |
| JMKE | `ai_edge` 25 < 30 floor — brand-new IPO, one analyst, essentially no historical reaction data to model against. |
| KFY | `change_expectation` 30 < 35 floor — slow-moving consulting/staffing name that typically grinds on a print. |
| ODD | `tradeable: false` — sub-$1B beauty-tech ADR, one analyst; scout raised doubt about listed-options depth that the universe stage had not independently verified for this name. |
| CGNT | `tradeable: false` — sub-$700M Israeli security-analytics ADR, one analyst; same options-depth concern, unverified at the universe stage. |

Disclaimer: this is research, not financial advice. Earnings reactions are highly
uncertain and can be driven by market positioning, guidance, macro conditions, and
management commentary rather than reported results alone.

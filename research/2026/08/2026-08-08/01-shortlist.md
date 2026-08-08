# Stage 1 — Shortlist for 2026-08-08

**Window covered:** After the US close on Saturday 08 August 2026 through before the US
open on Monday 10 August 2026. Every eligible name in this window reports **BMO on
Monday 10 August 2026** — stage 0 found zero AMC candidates for tonight (`after_close`
count was 0), so this shortlist is 100% BMO. That's a fact about tonight's calendar,
not a triage artifact; there was no AMC/BMO tradeoff to make.

**Funnel:** 48 universe → 27 eligible → 23 cleared floors → **10 shortlisted**

- Triage mode: scouted (universe eligible 27 > skip threshold 10)
- Scouts: 2 subagents (`earnings-triage-scout`, sonnet/medium), batches of 15 and 12
- Floors: `min_change_expectation` 35, `min_ai_edge` 30
- Dropped for floors/tradeability: 4 (B, FERG, GCMG — change_expectation too low;
  KSPI — untradeable, thin ADR options market)
- Session mix: 10 BMO / 0 AMC (matches tonight's universe — see above)

## Shortlist

| Ticker | Session | Δ-exp | AI-edge | Priority | Evidence | Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| BW | bmo | 82 | 55 | 69.85 | thin | Short-seller report (Wolfpack) disputes the structure of its $2.4B power contract — a contested, filings-dense situation careful synthesis can add to. |
| AXSM | bmo | 72 | 60 | 66.6 | good | Three launched CNS drugs; revenue trajectory trackable via prescription data; heavy bull skew (20/21 buys) raises miss-reaction risk. |
| CEVA | bmo | 78 | 48 | 64.5 | thin | Small-cap IP licensor, surged 14% on last beat; lumpy deal-timing revenue but design-win/royalty trends are trackable. |
| MNDY | bmo | 68 | 60 | 64.4 | good | Live analyst debate: SMB softness vs. enterprise strength (dispersed EPS estimates); rich public KPI/cohort data to adjudicate it. |
| SGRY | bmo | 60 | 68 | 63.6 | thin | Staffing-cost pressure vs. swing-to-profitability debate ($0.06 consensus EPS); dense public disclosure on case volume/margins. |
| LINC | bmo | 60 | 65 | 62.25 | thin | Already jumped 9-12% multiple times this year on guidance raises; guided student-start growth (10-14%) is a trackable KPI. |
| BTDR | bmo | 75 | 45 | 61.5 | good | Bitcoin miner pivoting to AI cloud (ARR ~$76M); mining side de-risked by monthly updates, AI-cloud monetization is the real swing factor. |
| KEEL | bmo | 82 | 35 | 60.85 | thin | 52-week range $1.17-$7.37, projected 55% YoY revenue decline; value driver is largely crypto/hashrate sentiment — edge here is thinner than the score suggests. |
| AIOT | bmo | 65 | 50 | 58.25 | thin | Post-merger IoT/fleet name, +45% YoY revenue last print; thin coverage and integration noise cap forecastability. |
| CAMT | bmo | 60 | 55 | 57.75 | good | HBM/advanced-packaging demand, disclosed $260M+ backlog; peer read-throughs (KLAC, ASML) give genuine synthesis edge. |

*Δ-exp = `change_expectation`, both scores 0-100. All `expected_move_hint` values are
`null` — neither scout could source an options-implied move within its time budget, and
per the no-fabrication rule that is left null rather than estimated.*

## Notable drops

**Failed the hard floors:**
- **B** (Barrick Mining) — change_expectation 30: mega-cap gold miner, moves track
  bullion price, not usually a violent earnings mover.
- **FERG** (Ferguson) — change_expectation 25: large-cap distributor, low binary
  catalyst, print is usually confirmatory of already-known trends.
- **GCMG** (GCM Grosvenor) — change_expectation 25: steady AUM-fee revenue, typically
  low-vol print.
- **KSPI** (Kaspi.kz) — tradeable: false: real growth catalysts but a thin ADR options
  market and weak US coverage make it untradeable for this pipeline's purposes.

**Cleared the floors but didn't make the cut (priority score, for the record):**
SNDA 55.4, NYAX 55.0, MPT 55.0, INSW 52.75, NABL 52.6, SBET 52.0, TH 51.75, RDNT 49.5,
SDRL 45.0, DOLE 44.0, CRC 42.25, CECO 41.1, NESR 37.25.

Two worth flagging specifically: **SBET** (SharpLink) — ai_edge sits right at the floor
(30); it's effectively an ETH-holdings NAV vehicle that already trades off spot crypto
price, so the print itself adds little new information. **MPT** (Medical Properties
Trust) — a distressed hospital-REIT turnaround with real complexity (tenant coverage,
lease amendments) that just missed the top 10 on priority score; worth a second look if
any shortlisted name falls through in stage 2.

## Warning for stage 2

Two shortlisted names cleared the floors mechanically but carry real forecastability
caveats the scouts flagged explicitly: **KEEL** (crypto/hashrate-sentiment-driven, not
really an earnings-print story) and, to a lesser extent, **BW** (short-seller dispute
whose resolution partly hinges on facts not yet public). Both are legitimately high on
`change_expectation`, but the deep-dive dossiers for these two should be honest about
how much of the move is genuinely forecastable vs. externally driven.

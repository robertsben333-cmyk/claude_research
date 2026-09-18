# Stage 1 — Shortlist for 2026-08-11

**Window:** After the US close on Tuesday 11 August 2026 through before the US open on
Wednesday 12 August 2026

**Mode:** scouted (universe well above the skip threshold of 10)

## Funnel

| Stage | Count |
| --- | --- |
| Universe (total) | 112 |
| Eligible (passes market-cap floor) | 53 |
| Dropped — timing unconfirmed or not tradeable | 11 |
| Dropped — below `change_expectation`/`ai_edge` floors | 7 |
| Cleared both floors | 35 |
| **Shortlisted** | **10** |

Floors: `min_change_expectation = 35`, `min_ai_edge = 30`. Weights: 0.55 change / 0.45
edge. 4 triage-scout subagents (sonnet/medium), ~13-14 tickers each.

## Shortlist

| Ticker | Session | Change | Edge | Priority | Rationale |
| --- | --- | --- | --- | --- | --- |
| CRWV | amc | 88 | 55 | 73.2 | Options price a 15.5% straddle; GPU-capex/backlog narrative, thin coverage caps synthesis edge |
| NBIS | bmo | 82 | 58 | 71.2 | Up 161% YTD on AI-cloud narrative, only 1 covering analyst |
| SMCI | amc | 72 | 66 | 69.3 | Preliminary update flagged revenue near low end of guide with record backlog — live credibility question |
| CAVA | amc | 75 | 60 | 68.3 | Easiest year-ago comp lap after a blowout Q1; alt-data can inform the traffic debate |
| FLY | amc | 75 | 55 | 66.0 | Recent launch/lunar IPO that missed last quarter; peer read-throughs (Rocket Lab, Intuitive Machines) add edge |
| JMIA | bmo | 75 | 55 | 66.0 | Turnaround-narrative African e-commerce ADR, history of violent post-print swings |
| LITE | amc | 68 | 62 | 65.3 | AI-datacenter transceiver pure-play; hyperscaler capex read-throughs add synthesis value |
| NRGV | amc | 75 | 50 | 63.8 | Distressed-ish energy storage name; backlog conversion and liquidity are live questions |
| ATRO | amc | 62 | 65 | 63.4 | Aerospace connectivity supplier with a history of large earnings-day moves; OEM production-rate checks add edge |
| LQDA | bmo | 65 | 60 | 62.75 | Yutrepia launch trajectory is a trackable commercial-uptake question, not a binary readout |

**Session mix: 7 AMC / 3 BMO** — tilted toward after-close reporters. LQDA was kept over
a tied AMC name (BORR, also 62.75) specifically to pull in a third BMO name; the
imbalance persists because most of the day's highest-priority setups happen to report
after today's close.

## Notable drops

**Timing unconfirmed:**
- **TGLS** — multiple sources show it already reported Q2 2026 results on Aug 6; the
  universe's Aug 11 date looks stale.
- **IMOS** — Taiwan OSAT ADR that reports pre-market ~3am ET; the universe's "amc"
  session tag looks mismatched with actual reporting time.
- **EVLV** — sources conflict on the exact date (Aug 11 vs 12 vs 13).
- **WYFI** — conflicting reported dates (Aug 9/12/13) for a recent AI-datacenter spinoff.
- **MLYS** — could not confirm the exact Q2 report date in the scout's search budget;
  real catalyst here is a Dec-2026 PDUFA date anyway, not this print.

**Not tradeable (thin float / no real options market / too little history):**
- **QNT**, **FRVO**, **AADX** — all recent IPOs (weeks to ~2 months old) with a single
  analyst and no meaningful public track record.
- **ELE**, **UAMY** — foreign-issuer/NYSE-American microcaps likely without real listed
  options liquidity.
- **EROC** — sourced financials look implausible (double-digit per-share losses),
  suggesting unreliable data on a thin, illiquid name.

**Cleared for tradeability but dropped on floors:**
- **ALT** (change 92, edge 20) — the print is paired with a Phase 2b clinical readout,
  a classic binary trial outcome nobody outside the company can forecast. Textbook case
  of "will move a lot, but AI research adds nothing."
- **FNV**, **AMCR**, **HRB**, **PFGC**, **BGSI**, **ITRN** — slow, well-covered,
  formulaic prints that clear neither floor by a comfortable margin.

Watch **ALT** in particular after the print — a 92 change-expectation name that the
pipeline correctly declined to research is exactly the kind of drop the archive should
catch if it moves big and the floor logic needs revisiting.

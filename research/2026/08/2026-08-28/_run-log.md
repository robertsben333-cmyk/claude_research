# Run log — 2026-08-28

## Stage 0 — universe (07:19 CEST)
- Window: After the US close on Friday 28 August 2026 through before the US open on Monday 31 August 2026
- Source: nasdaq (both after-close and before-open sides)
- Universe: 4 total (0 AMC, 4 BMO); 1 eligible after qualification
- Excluded: 3 (below_market_cap_floor: SY, LX, BLRX)
- Notes: Friday run correctly rolled the before-open side to Monday 2026-08-31 (weekend skip).
  Only SAIC cleared the $500M market-cap floor. Cross-checked SAIC's BMO timing against a second,
  independent source (SAIC's own GlobeNewswire IR release, issued 2026-08-13) beyond the Nasdaq
  calendar — both agree on before-market-open, 2026-08-31, so timing is confirmed, not just
  single-sourced. SAIC has an active listed-options market. Eligible universe of 1 is well below
  `triage.skip_if_universe_at_or_below: 10`, so stage 1 (triage) will be skipped — the single
  eligible name goes straight to stage 2.

## Stage 1 — triage (11:08 CEST)
- Mode: skipped (universe <= threshold — 1 eligible <= 10)
- Funnel: 4 universe -> 1 eligible -> 1 cleared floors (screen skipped) -> 1 shortlisted
- Scouts: 0 subagents (screen skipped)
- Session mix: 0 AMC / 1 BMO
- Notable drops: none by triage (SY, LX, BLRX already excluded at stage 0 for below_market_cap_floor)

## Stage 2 — deep dive, batch 1 — STARTED
- Logged at 2026-08-28 08:23 UTC
- Tickers: SAIC (Science Applications International Corporation, bmo, 2026-08-31)
- Batch split: shortlist has 1 name; N = ceil(1/2) = 1, so batch 1 takes SAIC and batch 2 will have nothing to do
- Plan: 1 wave of 1 opus/high researcher, publish after the wave completes

### Stage 2 — SAIC dossier written
- Logged at 2026-08-28 (deep-dive researcher, opus/high)
- Files: `02-dossiers/SAIC.md`, `02-dossiers/SAIC.json`
- `event_confirmed: true` — company press release 2026-08-13 confirms results before market open
  Monday 2026-08-31 with a 10:00 a.m. EDT webcast-only call (Q2 FY2027, quarter ended ~2026-07-31).
- Anchors: spot $128.96 (2026-08-27 close), market cap $5.45B, event-implied move **8.9%**
  (front ATM straddle 9.15% of spot; 8.87% from a two-expiry event-vol decomposition using Cboe
  delayed quotes — SAIC lists no weeklies, so the 22-dte 18 Sep straddle overstates the one-day move).
- Historical: 12 quarterly BMO prints reconstructed from EDGAR Item 2.02 8-K dates + daily closes.
  Last 6 mean |move| 9.21%, median 8.79%, max 16.29%, 4 up / 2 down. Also flagged the non-quarterly
  2026-02-11 pre-announcement (-16.03%).
- Preliminary read: direction +8, prob_up 54, reversal_risk 68, conviction Low.
- Evidence completeness 80.
- **Network notes:** globenewswire.com and investors.saic.com returned 503; benzinga.com, fintel.io,
  marketchameleon.com returned 403; alphaquery.com 503; zacks.com bot-blocked; wsj.com blocked by
  tooling; nasdaq.com earnings and short-interest modules returned "data not available"; stooq.com
  hit a proxy JS challenge. **SEC EDGAR (data.sec.gov + Archives), cdn.cboe.com and
  stockanalysis.com were fully reachable**, so all filing-based facts, the whole option chain and
  all price history are primary-sourced rather than snippet-sourced. IR press releases were routed
  through a GlobeNewswire mirror.
- Biggest gap: **IV rank / percentile is null** — no historical IV series obtainable. Substituted the
  46.4% front vs 37.4% three-month term-structure inversion and IV30 41.9% vs 20d realised 21.5%.
  Second gap: no 30/60/90-day estimate-revision table (Zacks blocked; two search snippets conflict).

## Stage 2 — deep dive, batch 1 (08:42 CEST)
- Logged at 2026-08-28 08:43 UTC
- Researched: SAIC
- Skipped (already done): none
- Failed: none
- Subagents: 1 opus/high (1 wave of 1 — shortlist had only 1 name total)
- Median evidence completeness: 80/100
- Note: batch 2 will have nothing left to research (shortlist length 1, N=ceil(1/2)=1 already covers it all in batch 1); batch 2 should still run the ranking step since it is the final batch

## Stage 2 — deep dive, batch 2 — STARTED
- Logged at 2026-08-28 10:23 UTC
- Tickers: none — shortlist has 1 name total (SAIC); N = ceil(1/2) = 1, so batch 1 already covered the entire shortlist
- Plan: no researchers to spawn; verify SAIC.md + SAIC.json exist, then run the final-batch ranking step (02-ranking.json)

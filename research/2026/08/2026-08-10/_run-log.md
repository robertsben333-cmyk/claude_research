# Run log — 2026-08-10

## Stage 0 — universe (07:12 CEST)
- Window: After the US close on Monday 10 August 2026 through before the US open on Tuesday 11 August 2026
- Source: nasdaq (both after-close and before-open sides; single source, no network block)
- Universe: 144 total (99 AMC, 45 BMO); 76 above the $500,000,000 market-cap floor; 75 eligible after qualification
- Excluded: 69 total — 68 below_market_cap_floor (feed value), 1 additional (`PPHC`, feed market-cap data error)
- Notes: `python3 scripts/get_earnings.py` returned status `ok` on the first attempt — no
  network block. Qualification against `config/pipeline.yaml` used the nasdaq feed as the
  sole source, so there were no cross-source BMO/AMC timing conflicts to reconcile.
  `PPHC` (Public Policy Holding Company) was caught by inspection: the feed reported a
  $28.52B market cap, which is implausible for a small government-affairs firm and off by
  roughly two orders of magnitude. Cross-checked via WebSearch (TipRanks, Morningstar,
  Yahoo Finance — consistently ~$271-390M / ~29-30M shares outstanding as of Jun-Jul 2026)
  and corrected to $305.53M (Morningstar, 2026-06-02), which puts it below the floor; it is
  now excluded and the corrected figure plus feed figure are both recorded on the company
  row (`market_cap_usd_feed` / `market_cap_usd_source_note`). Worth watching whether the
  nasdaq feed produces similar bad market-cap values again on a future run.
  A handful of unfamiliar or recently-listed names were spot-checked via WebSearch for a
  real listed-options market and confirmed exchange/session rather than excluded by
  guesswork: `EROK` (NYSE, 2025 IPO, options tradeable via major brokers), `CDNL` (Nasdaq,
  renamed from Civil Infrastructure Group Sep 2025, options chain confirmed via Finviz),
  `DPC` (NYSE, confirmed BMO earnings 2026-08-11 matching the feed), `RUM` (Nasdaq,
  formerly Rumble Inc., option chain confirmed via Nasdaq), `IMSR` (Nasdaq, de-SPAC
  completed Oct 2025 with HCM II Acquisition Corp, option chain confirmed via Yahoo
  Finance/OptionCharts). All five cleared and remain eligible. The remaining above-floor
  names are established Nasdaq/NYSE-listed operating companies or ADRs with analyst
  coverage; options-market/OTC/SPAC-remnant/timing screening for those was done by
  inspection, consistent with the 2026-08-08 run's approach.
  75 eligible names exceeds the stage-1 skip threshold (`triage.skip_if_universe_at_or_below: 10`),
  so stage 1 (triage) will run normally at 11:08 CEST.

## Stage 1 — triage (11:08 CEST)
- Mode: scouted (75 eligible names exceeds the skip threshold of 10)
- Funnel: 144 universe -> 75 eligible -> 68 timing/tradeable-confirmed -> 53 cleared floors -> 10 shortlisted
- Scouts: 5 subagents (sonnet/medium), batches of 15, run in parallel
- Session mix: 6 AMC / 4 BMO
- Shortlist (priority_score desc): SE (77.5), RKLB (73.8), HIMS (73.0), UPWK (68.8), DSP (67.8),
  ONON (67.8), LIF (66.4), LEGN (65.7), VSTS (64.6), HROW (64.4)
- Dropped for unconfirmed timing/no tradeable options market (7): AMTM, CIB, EROK, IHRT, SMC
  (conflicting date/session across sources — flag if they resurface in a future universe run),
  ALMR, IMSR (no real options market per scout). Note: stage 0 had spot-checked EROK and IMSR as
  tradeable via WebSearch; the stage-1 scouts flagged EROK on timing (not tradeability) and
  reversed the IMSR tradeability call. Worth a second look before trusting either verdict blindly.
- Dropped for failing a hard floor (15): mostly two clusters — (a) mega-cap/BDC/REIT formality
  prints with change_expectation <35 (ACM, MIDD, ARMK, CAH, ALC, SPG, BCSF, NHI, KBDC, PFLT) and
  (b) hyped small-caps with ai_edge <30 (USAR, QUBT, IAUX, BCAX, HUYA) — big potential moves but
  no researchable public thesis (meme/lottery-ticket profile or binary biotech readouts).
- Evidence quality: only SE and HIMS carry a sourced options-implied move (`evidence: good`); the
  other 8 shortlisted names are `evidence: thin` — stage 2 should independently source implied
  move and consensus estimates rather than trusting the scout read.

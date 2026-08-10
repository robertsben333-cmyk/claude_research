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

## Stage 2 — deep dive, batch 1 (attempted 10:25 CEST) — BLOCKED
- `01-shortlist.json` / `01-shortlist.md` do not exist yet for 2026-08-10 — only
  `00-universe.*` has been published. Stage 1 (triage) fires at 11:08 CEST; this firing
  landed at ~10:25 CEST, ~45 minutes before stage 1 is due to produce the shortlist.
- No deep-dive work was done. Per CLAUDE.md ("never fabricate a number") and the
  `earnings-deep-dive` skill (which reads `01-shortlist.json` as its required input),
  there is nothing to spawn researchers against — inventing a shortlist to unblock this
  firing would corrupt every downstream stage.
- Checked `02-dossiers/`: empty, consistent with stage 1 not having run.
- No action taken beyond this log entry. Flagging the ordering: either this Routine's
  fire time needs to move later than 11:08+buffer CEST, or stage 1 needs to run before
  this firing is dispatched. Recommend re-running stage 2 batch 1 after stage 1 publishes
  `01-shortlist.json` for 2026-08-10.

## Stage 2 — deep dive, batch 2 (attempted 12:24 CEST) — BLOCKED
- `01-shortlist.json` / `01-shortlist.md` still do not exist for 2026-08-10. Stage 1
  (triage, due 11:08 CEST) has not published — confirmed via `git log` on `main`: the
  only commits for today are stage 0 (universe, 07:12 CEST) and the stage 2 batch 1
  blocked-entry. No shortlist commit landed in between.
- Checked `02-dossiers/`: empty, consistent with stage 1 not having run and batch 1
  having done no work.
- Per the `earnings-deep-dive` skill, batch 2 should cover both halves if batch 1 failed
  entirely — but that only applies once a shortlist exists to split into halves. With no
  shortlist at all, there are zero tickers to assign to either batch; there is nothing to
  resume or restart, and inventing a shortlist would violate CLAUDE.md's "never fabricate
  a number" rule at the worst possible point in the pipeline (it would corrupt every
  downstream stage: dossiers, ranking, panel, advice, calibration).
- No research subagents were spawned. No action taken beyond this log entry.
- Recommend: check why stage 1's 11:08 CEST Routine firing did not publish (Routine
  misconfiguration, session failure, or timing skew — batch 1's own firing landed at
  10:25 CEST, well before stage 1 was due, which suggests this account's Routine clock
  may be running ahead of Europe/Amsterdam wall time). If stage 1 has genuinely not run
  by the time stage 3 (panel, 18:07 CEST) fires, stage 3 will also have nothing to work
  from — worth fixing before then rather than discovering it a third time downstream.

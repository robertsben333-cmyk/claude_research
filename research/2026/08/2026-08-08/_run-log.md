# Run log — 2026-08-08

## Stage 0 — universe (11:36 CET)
- Window: After the US close on Saturday 08 August 2026 through before the US open on Monday 10 August 2026
- Source: nasdaq (both after-close and before-open sides; single source, no network block)
- Universe: 48 total (0 AMC, 48 BMO); 27 eligible after qualification
- Excluded: 21 (below_market_cap_floor: 21)
- Notes: Reference date (2026-08-08, Saturday) is not a trading day; `get_earnings.py`
  correctly rolled the window to the next open (Monday 2026-08-10) and reported empty
  after-close as expected for a weekend. Qualification against `config/pipeline.yaml`
  used the nasdaq feed as the sole source (no cross-source timing conflicts to check);
  options-market/OTC/SPAC-remnant screening was done by inspection — all 27 above-floor
  names are established Nasdaq/NYSE operating companies with analyst coverage. One
  unfamiliar name, `KEEL` (Keel Infrastructure Corp.), was spot-checked via WebSearch
  and confirmed Nasdaq-listed (XNAS) with a live options market. No exclusions applied
  beyond the market-cap floor. 27 eligible names exceeds the stage-1 skip threshold
  (`triage.skip_if_universe_at_or_below: 10`), so stage 1 (triage) will run normally.

## Stage 1 — triage (11:57 CEST)
- Mode: scouted (27 eligible > skip threshold of 10)
- Funnel: 48 universe -> 27 eligible -> 23 cleared floors -> 10 shortlisted
- Scouts: 2 subagents (sonnet/medium), batches of 15 and 12
- Session mix: 10 BMO / 0 AMC — tonight's entire eligible universe is BMO (stage 0
  found 0 AMC candidates), so no session tilt was introduced by triage
- Dropped for floors/tradeability (4): B, FERG, GCMG (change_expectation below 35),
  KSPI (untradeable — thin ADR options market, ai_edge 25)
- Notable drops among names that cleared floors but missed the top 10: SBET
  (ai_edge sits exactly at the 30 floor — effectively an ETH-NAV vehicle, print adds
  little new info), MPT (distressed hospital-REIT turnaround, priority 55.0, just
  missed the cut)
- Flag for stage 2: KEEL and BW cleared floors mechanically but scouts flagged real
  forecastability caveats — KEEL's move is largely crypto/hashrate-sentiment driven,
  BW's short-seller dispute partly hinges on facts not yet public. Dossiers for these
  two should be explicit about how much of the move is genuinely forecastable.
- No fabricated data: all `expected_move_hint` fields are null (no options-implied
  move sourced by either scout within its time budget)

## Stage 2 — deep dive (halted, 16:50 CEST)

**This run stopped early: the account hit its monthly spend limit.** The failing
session reported `You've hit your org's monthly spend limit`. This is a billing
ceiling, not a pipeline fault — see claude.ai/settings/usage.

Completed and published (4 of 10): AXSM, CEVA, MNDY, SGRY.

Not researched (6 of 10): BW, LINC, BTDR, KEEL, AIOT, CAMT.

- Batch 1 first attempt researched five names but published only three before the
  session ended mid-batch; AXSM was left with a `.md` and no `.json`, and BW was
  never written. A follow-up run completed AXSM.
- Two separate attempts at BW returned without publishing. The second returned in
  three and a half minutes on ~180k tokens, which in hindsight was the spend limit
  already biting rather than a research failure.
- Batch 2 (LINC, BTDR, KEEL, AIOT, CAMT) failed outright on the spend limit after
  roughly 2M input tokens, publishing nothing.

No `02-ranking.json` was produced, so **stage 3 has no ranking to read and should not
run for this date.** Four dossiers is too thin a field to pick a top three from
honestly, and the six missing names include the two the triage flagged as most
questionable (BW, KEEL) — their absence biases what is left.

A defect found and fixed during this run: `scripts/publish.sh` destroyed a stage's
work whenever the remote branch moved mid-run. Three stacked causes, all fixed in
commit `bf8e2a6`, with a regression test in `scripts/smoke_test.py` that reproduces
the scenario against a throwaway remote. Stage 2 now publishes after each dossier
rather than per batch, which is why three of the five first-attempt dossiers survived.

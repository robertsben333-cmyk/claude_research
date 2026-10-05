# Source-value study: status (heartbeat)

Run started 2026-10-05 (UTC) as an autonomous session on branch `claude/source-value-study`,
following `PROMPT.md`. Nobody is watching; every choice the prompt leaves open is taken
conservatively and recorded in the "Decisions" list below.

## Plan and outcome (run finished 2026-10-05)

| phase | state |
|---|---|
| 0 Sample | done in full: A 158 prints / 2,141 items, A2 empty (no resolved E-P hunt), B 30 dossiers / 1,908 claims, C 89 prints / 913 items, D excluded |
| 1 Codebook | done in full: mechanical layer, Opus design (70 subtypes), two Sonnet runs over 4,962 items, agreement 92.6%, 17 subtypes merged |
| 2 Metrics | done in full, frozen in METHODS.md before the join; amendment 1 made on fake outcomes before the join |
| 3 Ledger | done: 445 questions in 13 batches, each registered before it ran |
| 4 Statistics | done in full (permutation, batch family-wise, ledger BH, leave-one-day-out, power, shrinkage) |
| 5 Large-cap case study | done in full: hits described and rules frozen before the misses were opened; forward test pending (no forward days) |
| 6 Registry | done: v1 frozen; forward scripts written and run (0 forward prints) |
| 7 Report | done: README, index row, Dutch summary in the final reply |
| Ablation | 31 codes, $75 of the $120 cap; stopped by choice once every code in at least ~15 packs, every group and the six largest search-note types were covered |

Stop condition met: 445 answered questions and the last two batches (b13, b14) added no
"works" or "misleads" verdict; every registry cell has a verdict.

## Budget

$250 total, at most $120 on the ablation arm. Final spend: **$115.70** (labels $38.62,
ablation $75.03, codebook design $1.65, pilot $0.40, setup $0.005). Every call in
`ledger/calls.jsonl`.

## Decisions (conservative defaults where the prompt leaves a choice)

1. Stratum A cut-off: the dashboard ledger as committed on this branch
   (`generated_utc` 2026-10-05T06:47Z). The 2026-10-02 US runs have no hunts, so the last
   resolved entry is 2026-10-01 (NKE). Main's later rebuilds change no resolved US name.
2. Stratum A2 is empty: no stage E-P searcher hunt has resolved (the first E-P fire was
   2026-10-02 and its directory holds no hunts). Reported as empty, not dropped silently.
3. Stratum B is limited to dossiers with an outcome in `PREDICTIONS.csv` (36 rows, 30 prints with extractable
   cited claims); no new prices were fetched for the other 45 dossiers. B's outcome is close-to-close (the only
   one recorded). Its items are extracted mechanically (no model), so both labelling runs see identical items.
4. Stratum C priced move = the baseline's median past reaction (no option anchor anywhere outside the US);
   `event_occurred*` fields, amended after the outcome, are stripped from C packs.
5. `dated_in_window` is defined as "dated after the company's previous quarterly results and on or before the
   seal" (the prompt does not define the window).
6. Primary DV/DV* use move/priced Winsorised at +-4 (one print would otherwise decide a cell); raw beside it.
7. The registry's estimates are stratum A only; B and C are replication columns, never pooled into the verdict.
8. Ablation: the intact arm is run twice (noise yardstick); an ablated arm re-judges only packs that contain
   the code, unchanged packs reuse the intact mean. This makes ~$2-6 per code instead of ~$15.
9. The four-model re-judge exists only for stratum A; MgV (observational) is A only.
10. Ablation codes were ordered: all search notes as one group first (individually the most
    prevalent codes but they carry no direction), then the non-search codes by prevalence, then
    the eight groups, then the six most prevalent search-note types. The paired per-pack
    statistic (change in sgn(impact) x move/priced) was added to the ablation score beside the
    pre-registered rho / hit / top-20% deltas, because those three move by noise-sized amounts on
    the few packs a code touches.
11. Question b12-C-G:researcher_own and b13-C-G:researcher_own are the same cell asked twice (the
    generator's two families overlapped); both stay in the ledger and both count in the BH q.
12. b14-22 could not exclude the derivation prints through the filter language; the leave-out
    version of that rule test is `casestudy/rules-test.json`.
13. A `pkill` used to stop stuck wait loops also ended one shell; nothing was lost (the ablation
    runs had already finished and were re-scored).

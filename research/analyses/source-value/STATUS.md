# Source-value study: status (heartbeat)

Run started 2026-10-05 (UTC) as an autonomous session on branch `claude/source-value-study`,
following `PROMPT.md`. Nobody is watching; every choice the prompt leaves open is taken
conservatively and recorded in the "Decisions" list below.

## Plan

| phase | what | state |
|---|---|---|
| 0 | **done**. Sample: stratum A (163 US hunts / 158 prints, ledger cut-off 2026-10-05T06:47Z, entries to 2026-10-01), A2 (stage E-P searcher hunts: none resolved yet), B (retired stage-2 dossiers with an outcome in PREDICTIONS.csv), C (Europe, Japan, Australia resolved runs). D (sealed corpus) excluded: `INCLUDE_CORPUS` not set. Result: A 163 hunts / 158 prints / 2,141 items; B 30 dossiers / 1,908 cited claims (mechanical extraction); C 89 prints / 913 items (Europe 56, Japan 17, Australia 16) | done |
| 1 | Codebook: mechanical layer (done: 676 SEC citations resolved via EDGAR accession), design call (done: 70 subtypes, $1.65, frozen as v1) (SEC form/items from URL + EDGAR index), one Opus design call on a 15% pack sample (no outcomes), two Sonnet labelling runs (running), agreement table, merges below 80% | in progress |
| 2 | Metrics DV, DV*, MV, MgV, prevalence and the size bands, frozen in `METHODS.md` with the codebook | done (committed before labels) |
| 3 | Question ledger, batches of 20-40, committed before running | pending |
| 4 | Statistics (permutation within day, EB shrinkage, three-level multiplicity, leave-one-day-out, power) in `METHODS.md` | pending |
| 5 | Large-cap case study | pending |
| 6 | Registry v1, forward scripts | pending |
| 7 | README, index row, Dutch summary | pending |

## Budget

$250 total, at most $120 on the ablation arm. Running total in `ledger/budget.json`.
Spend so far: ~$27 (labels ~$13 of an expected ~$35; ablation intact arm ~$12 of ~$14).

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

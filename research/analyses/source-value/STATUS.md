# Source-value study: status (heartbeat)

Run started 2026-10-05 (UTC) as an autonomous session on branch `claude/source-value-study`,
following `PROMPT.md`. Nobody is watching; every choice the prompt leaves open is taken
conservatively and recorded in the "Decisions" list below.

## Plan

| phase | what | state |
|---|---|---|
| 0 | Sample: stratum A (163 US hunts / 158 prints, ledger cut-off 2026-10-05T06:47Z, entries to 2026-10-01), A2 (stage E-P searcher hunts: none resolved yet), B (retired stage-2 dossiers with an outcome in PREDICTIONS.csv), C (Europe, Japan, Australia resolved runs). D (sealed corpus) excluded: `INCLUDE_CORPUS` not set | in progress |
| 1 | Codebook: mechanical layer (SEC form/items from URL + EDGAR index), one Opus design call on a 15% pack sample (no outcomes), two Sonnet labelling runs, agreement table, merges below 80% | pending |
| 2 | Metrics DV, DV*, MV, MgV, prevalence and the size bands, frozen in `METHODS.md` with the codebook | pending |
| 3 | Question ledger, batches of 20-40, committed before running | pending |
| 4 | Statistics (permutation within day, EB shrinkage, three-level multiplicity, leave-one-day-out, power) in `METHODS.md` | pending |
| 5 | Large-cap case study | pending |
| 6 | Registry v1, forward scripts | pending |
| 7 | README, index row, Dutch summary | pending |

## Budget

$250 total, at most $120 on the ablation arm. Running total in `ledger/budget.json`.
Spend so far: $0.00.

## Decisions (conservative defaults where the prompt leaves a choice)

1. Stratum A cut-off: the dashboard ledger as committed on this branch
   (`generated_utc` 2026-10-05T06:47Z). The 2026-10-02 US runs have no hunts, so the last
   resolved entry is 2026-10-01 (NKE). Main's later rebuilds change no resolved US name.
2. Stratum A2 is empty: no stage E-P searcher hunt has resolved (the first E-P fire was
   2026-10-02 and its directory holds no hunts). Reported as empty, not dropped silently.

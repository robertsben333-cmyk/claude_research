# Opus 5.5 under the two-measurement core, on the Opus 5 days

**Question.** Since 2026-10-01 (evening, `us.v9` and siblings) every hunter sizes each
finding on its own again (version 2: their sum is `impact_sum`, the key) and, separately,
gives `abs_move_pct` and `p_up` (version 3: `impact_scaled`). Does Opus 5.5 under that
prompt get back to the scale and the signal the live Opus 5 hunts had on the days the
3.0 floor and the conviction result were measured on?

**Sample.** Every name from `../rejudge-four-models/` whose live hunt ran on Opus 5: day
before 2026-09-23 (the `opus` alias moved to Opus 5.5 at 18:56-19:09 UTC on 09-22, after
every 09-22 run had sealed). 128 names: 119 US (25 of them anonymised) and 9 Europe.
`manifest.json` pins the git blob of every file the judges read.

**Method.** Blinded re-judge, exactly as in `../rejudge-four-models/`: the evidence the
live hunter collected, its sizes and verdicts removed. One Opus 5.5 judge per pack
(`packs-NN.json`, 13 names), Read only, following `brief.md`. Outputs `out-NN.json`.
`score.py` scores five arms on one sample: live (Opus 5, v2), the Opus 5 and Opus 5.5
re-judges under the morning's v3 core, and this run's `impact_sum` and `impact_scaled`.
Gross of all costs.

**What it cannot show.** It tests judgement, not search: the judges see only what the
Opus 5 hunters found, so a model that searches differently is not measured. Every judge
loads CLAUDE.md, which quotes outcomes from these days; the anonymised names and the
`us_clean` group are the guard. 119 US names over 15 days is the same sample every
earlier analysis was chosen on.

## Result

(written by the session that ran it)

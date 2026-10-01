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

Run 2026-10-01 by one session: ten Opus 5.5 judges (`general-purpose`, model `opus`),
five at a time. `unpriced-hunter.md` was at blob `83d939cf...` as pinned. All ten outputs
validated first time (128 of 128 names, `impact_sum` equal to its findings everywhere,
`score.py` reports 0 problems), so nothing was re-launched. Full numbers in `scores.json`.
US gross, `short all` +0.36% per name on this sample.

**(a) Scale: about halfway back, not back.** Per US name (n 119):

| arm | median \|x\| | zeros | share >= 3 | findings per name |
|---|---|---|---|---|
| live (Opus 5, v2) | 3.00 | 3 | 50% | 4.13 filed by the first hunter(s) |
| opus5_v3 (re-judge) | 1.95 | 2 | 26% | not recorded |
| opus55_v3 (re-judge) | 1.28 | 4 | 12% | 1.12 |
| **opus55_v2 (this run)** | **1.70** | 5 | **18%** | **3.75** |
| opus55_scaled (this run) | 1.10 | 12 | 7% | - |

Per-finding sizing fixed the FILING: 3.75 findings per name against 1.12 under the
morning's core, close to the 4.13 the live hunts filed (which still carries double-hunt
duplicates the judges merged). It did not fix the SIZE: the median is 57% of live and
the share at or above 3 is 18% against 50%. Each finding is now sized smaller, so the sum
lands between the v3 collapse and the live scale. Part of the gap is the re-judge format
itself, since Opus 5 judging the same evidence also came in below live (1.95), but
opus55_v2 is below that too.

**The 3.0 floor does not mean what it meant.** Live, 3.0 bought half of the nonzero
tradable US names; on this scale it buys 17 of 119, about a third as many. The cut that
selects the same 50% share is 1.8. On that matched share the two books are the same
book in size and return: live 30/50 +3.43% (t 1.91), opus55_v2 28/50 +3.01% (t 1.97).
Do not move the floor to 1.8 on this: it was found on the days every earlier analysis
was chosen on.

**(b) Signal: the tail, not the ranking, and the same as live.**

| group | arm | within-day rho (p) | >= 3 book | family-wise p | leave-one-day-out |
|---|---|---|---|---|---|
| us | live | +0.119 (0.21) | 30/50 +3.43% t 1.91 | 0.10 | 17 names +5.54% |
| us | opus55_v2 | +0.087 (0.35) | 12/17 +3.76% t 1.66 | 0.00 | 8 names +10.59% |
| us | opus55_scaled | +0.148 (0.12) | 4/5 +10.67% t 3.37 | 0.04 | 22 names +4.14% |
| us_clean | live | -0.024 (0.84) | 21/32 +4.14% t 2.06 | 0.02 | 10 names +6.57% |
| us_clean | opus55_v2 | +0.016 (0.89) | 8/9 +5.65% t 2.24 | 0.13 | 10 names +4.21% |
| us_clean | opus55_scaled | +0.037 (0.74) | 2/2 +12.74% t 3.16 | 0.07 | 14 names +6.15% |

No arm ranks the whole day: every rho is inside noise, and on the 94 named US names
every arm is at zero. What survives is the tail, as in `../rejudge-four-models/`. The
US family-wise p of 0.00 for opus55_v2 is real but narrow: its best threshold sits at
3.5-4.0 (the thresholds leave-one-day-out picks), it rests on eight to ten names, and on
`us_clean` it falls to 0.13. So the anonymised names carry part of it, which is the
opposite of what leakage would predict but is still a small-sample result.
Nonzero names traded on sign alone return +0.53% (98 names), so the conviction cut is
again the whole finding.

**(c) impact_sum against impact_scaled: one measurement twice.** Sign agreement 97% and
rho +0.94 on the US names, despite the brief forbidding the judges to fit one to the
other. The scaled number is smaller (median 1.10, 12 zeros, because p_up 50 is a common
answer) and ranks marginally better (+0.148 against +0.087, neither significant). The
tradable tail sits in `impact_sum`: at 3.0 the scaled key buys only 5 US names, and at
the matched 50% share it returns +2.32% (t 1.24) against +3.01% (t 1.97) for the sum.
The scaled key's +10.67% on 5 names is not a book.

**(d) What it cannot show.** It tests judgement, not search: the judges saw only what
the Opus 5 hunters found, so whether Opus 5.5 under `us.v9` SEARCHES enough to fill
3.75 findings per name live is untested; the forward runs settle that. Every judge loads
CLAUDE.md, which quotes outcomes from these days; `us_clean` is the guard and it is
weaker than `us` on the family-wise test. One judge (pack 07) reported that
`unpriced-hunter-fr.md` names a real French company in a worked example with its
realised move, so the blinding on `anon/europe/027` is weaker than on the other
anonymised names. One judge (pack 10) used Edit once on its own output file to remove a
0.0 non-finding; outside the brief's tool list, no effect on any number. 119 US names
over 15 days is the sample every earlier analysis was chosen on, and every return here
is gross of costs, spread and borrow. Europe (9 names) says nothing.

**Answer.** Opus 5.5 under the two-measurement core files like Opus 5 again but sizes at
roughly 57% of its scale, so the 3.0 floor selects about a third as many names as it did
live. Matched on share, it carries the same tail signal live did, and no ranking.
Read the first forward `us.v9` days on share-matched cuts, not on 3.0.

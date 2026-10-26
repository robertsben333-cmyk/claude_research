# Split panels, busy days and agreement between runs (2026-10-26)

**Questions (Xavier, 2026-10-26).**

1. Do the 4x5 split panels (stage E-PS: four sessions of at most five names) score the high scorers better than the full E-P panel?
2. Is there any sign that on busy days we should be stricter and only take the top?
3. Now that several names were scored more than once on the same day (intraday snapshots, a Fable searcher, the split re-run), how much does agreement between those runs matter? And inside one panel, how much does agreement between the four judges matter?

**Short answers.**

1. No evidence either way. Two resolved days, 31 names. Both arms lost on their selected names (E-P 1 of 5 right, mean −3.7%; split 2 of 5, mean −1.1%). The more useful finding is that the two runs barely reproduce each other: ρ +0.49 between their scores, opposite sides on 10 of 31 names, and only 2 of the 8 selected names were picked by both.
2. Busy days did much worse, but taking only the top would not have helped. On the four days with 19 or more names, the ≥80 calls went 4 of 16, mean −6.2% (t −2.56, p 0.02), against 6 of 6 and +11.2% on days with 10 names or fewer. The top-1 per busy day went 0 of 4 and ≥90 went 1 of 5. So the problem was the days, not the threshold. All four busy days fall in one week (19 to 22 Oct), so a market regime explains this just as well as day size, and the August-September backtest showed no day-size effect.
3. Disagreement is a warning sign, agreement is not a buy signal. Names where another run took the other side did worse (−2.1% against −0.5%, n 31 and 60, difference t 1.44, p 0.15). Averaging the runs ranked no better than E-P alone. Inside one panel, a 2-2 split between judges was the worst group (4 of 16 right, −3.4%), but those names never reach 80 anyway. Nothing here clears a multiple-testing correction.

## Data and window

`collect.py` reads every US panel run in October and prices each name on the scorebord window: entry 13:30 ET on the run day, amc names out at the next open, bmo names out at 13:00 ET on the report day. Gross, equal weight. A move already frozen in `dashboard/data/scorebord-frozen.json` is reused so the numbers match the scorebord. Every arm is priced on the E-P window, so differences come from the scores, not the timing.

| arm | days resolved | names | prompt / stage |
|---|---|---|---|
| E-P live | 15 (10-05 to 10-23) | 173 | us-panel v1/v2 (same searcher file, see the 10-21 post-mortem) |
| E-PS split, 4 shards of ≤5 | 2 (10-22, 10-23) | 31 | us-panel-split.v1, branch `claude/modest-davinci-mjddtu` |
| E-PI 10:00 snapshot | 2 (10-14, 10-19) | 29 matched | us-panel-intraday.v1 |
| E-PI 12:00 snapshot | 5 (10-14 to 10-21) | 51 matched | us-panel-intraday.v1 |
| E-PF Fable searcher | 2 (10-14, 10-16) | 11 | us-panel-fable.v1 |

Runs before 10-14 carry no `panel_pct`; it is recomputed the way the scorebord does (each judge against its own live range from earlier runs, mean of the signed percentiles). The 10-26 split run (20 names) is not resolved yet and is left out. "Selected" means panel_pct ≥ 80 with all four judges, the live rule.

The arms are compared name by name and never pooled into one sample. Each arm's own result is reported on its own runs.

## 1. Split panels against the full panel

Same 31 names on 10-22 and 10-23, each arm with its own Opus 5.5 searchers and its own four judges.

| | E-P (one session) | E-PS (four sessions of ≤5) |
|---|---|---|
| within-day ρ against the move | −0.12 (p 0.51) | +0.08 (p 0.69) |
| selected (≥80) | 5: 1 right, −3.7% (t −1.78) | 5: 2 right, −1.1% (t −0.51) |
| panel_pct ≥ 70 | 7: 2 right, −1.5% | 7: 2 right, −1.6% |
| top 3 per day | 6: 2 right, −2.4% | 6: 2 right, −1.6% |
| findings per name | 7.3 | 7.5 |

Selected by E-P: WRLD, DECK, BE, FIX, MED. Selected by the split: WRLD, BE, FPH, MXL, CX. Both: WRLD and BE.

**Reading.** On these two days the split is not better on the high scorers in any way that can be told from noise; five names against five, two of them shared. What the comparison does show is how much a full re-run moves the score: ρ +0.49 between the two arms' signed panel_pct, opposite sides on 10 of 31 names. DECK was 90 long in E-P and 7 short in the split; MXL was 31 short in E-P and 94 long in the split. That is run-to-run noise in the searcher's evidence, and it is as large as most of the effects we try to measure. A fair answer to question 1 needs a few weeks of split days; 10-26 adds 20 names tomorrow.

## 2. Busy days

| day size | days | names | share ≥80 | selected | within-day ρ |
|---|---|---|---|---|---|
| ≤ 10 names | 8 | 45 | 13% | 6: 6 right, **+11.2%** (t 4.26, p 0.008) | +0.44 (p 0.007) |
| 11 to 16 | 3 | 40 | 10% | 4: 1 right, −1.3% | −0.39 (p 0.014) |
| ≥ 19 | 4 | 88 | 18% | 16: 4 right, **−6.2%** (t −2.56, p 0.02) | −0.10 (p 0.39) |

Day-level test, mean of each day's selected names: thin days +17.4, +9.4, +5.5, +16.1; busy days −4.4, +2.2, −9.0, −5.7. Difference +16.4 points, Welch t 4.44, p 0.005, on 4 against 4 days.

**Would "only the top" have helped on busy days? No.**

| busy days (≥19 names) | n | right | mean |
|---|---|---|---|
| top 1 per day | 4 | 0 | −6.5% |
| top 2 per day | 8 | 2 | −6.9% |
| rank 3 and lower among ≥80 | 8 | 2 | −5.5% |
| panel_pct ≥ 90 | 5 | 1 | −6.3% |
| top 10% of the day by rank | 9 | 2 | −7.5% |

A stricter cut keeps the losers. What did separate on busy days:

* **Lower-priority names.** Selected names ranked 11th or lower by `hunt_priority` lost −8.9% (n 9, t −2.34) against −2.8% for the first ten (n 7). These are the names the higher caps added. Both groups lost.
* **Longs.** Busy-day longs went 2 of 12, −7.6% (t −2.73); shorts 2 of 4, −2.0%. This is the buy-the-dip pattern from the 21 October post-mortem.
* **bmo.** Busy-day bmo calls 1 of 7, −10.7%; amc 3 of 9, −2.7%.
* Without 21 October the busy days still read 2 of 8, −3.4% (t −1.87).

On busy days more names also clear 80 (18% against 13%), because each judge is read against its own history, not against the day: a day full of large expected moves lifts everyone's percentile. That makes the bar effectively lower exactly when there are more names.

**Why this is not yet a rule.** All four busy days fall in one week (19 to 22 October), peak earnings season, and all the thin days with calls are 5 to 7 and 16 October. Day size and calendar week cannot be separated with this data. The August-September blind backtest (115 names, 15 days, median 8 names a day, studied in `/mnt/project-files/panel-day-dependent/`) found no day-size effect; its busiest day never had more than three names above 80. If day size is the cause, the 10-26 run (20 names) and the next busy days should keep losing on their top calls. If it was the week, the busy days of next week should look normal.

## 3. Agreement

### Between runs on the same day

91 names were scored by E-P and at least one other run (intraday snapshot, Fable searcher or split), on 7 days from 10-14 to 10-23.

| | E-P vs other run: n | ρ between scores | same side | selected by either / both |
|---|---|---|---|---|
| E-PI 10:00 (3.5 h earlier, re-searched) | 29 | +0.36 | 17 of 29 | 4 / 2 |
| E-PI 12:00 (1.5 h earlier, re-searched) | 51 | +0.70 | 40 of 51 | 14 / 4 |
| E-PF (Fable searcher) | 11 | +0.59 | 7 of 11 | 2 / 2 |
| E-PS (split, same time) | 31 | +0.49 | 21 of 31 | 8 / 2 |

Does agreement predict the outcome? E-P's side, by whether every other run took the same side:

| E-P panel_pct | all runs agree | at least one run disagrees | difference (Welch) |
|---|---|---|---|
| any | n 60, 28 right, −0.5% | n 31, 12 right, −2.1% | +1.7 pt, t 1.44, p 0.15 |
| ≥ 60 | n 24, 12 right, −0.4% | n 7, 2 right, −5.1% | +4.7 pt, t 1.65, p 0.12 |
| ≥ 70 | n 18, 9 right, −1.0% | n 6, 1 right, −6.3% | +5.3 pt, t 1.63, p 0.13 |
| ≥ 80 | n 13, 4 right, −2.9% | n 3, 1 right, −4.0% | |

Combining runs did not rank better: within-day ρ against the move was −0.17 (p 0.12) for E-P alone, −0.03 for the mean of all runs, −0.05 for the weakest link. A name selected by two or more runs went 2 of 8, −2.0%. More runs agreeing did not turn a losing week into a winning one; disagreement only marked the worst names.

### Inside one panel (four judges)

E-P live, all 173 names:

| | n | right | mean |
|---|---|---|---|
| all four judges on one side | 128 | 66 | +0.0% |
| 3 of 4 | 29 | 19 | +0.1% |
| 2 against 2 | 16 | 4 | −3.4% (t −2.92, p 0.01) |

Above 60 almost every name has all four judges on one side (58 of 59), so sign agreement cannot separate the high scorers. The spread can a little: among the ≥80 names, those with a spread below the median (3.6) returned +1.7% (n 14) against −5.1% above it (n 12), difference +6.9 pt, t 1.63, p 0.12. The `panel-mean-pct` study found the same direction on the backtest, nowhere at 2 standard errors.

## What it does not show

* About thirty comparisons were run here. At that count, one or two p values below 0.05 are expected by chance. Only the busy-day result is strong on its own (day-level p 0.005), and it is confounded with the calendar.
* Two split days and 31 names cannot rank the split against the full panel.
* All multi-run names fall in 14 to 23 October, a period in which E-P's calls lost overall, so the agreement tables describe which names lost less, not which won.
* Gross of costs; the busy-day extra names are the thinner ones, so costs would widen the gap.

## Suggested next steps

* Keep the split running; judge it after about ten resolved days, pooled, against E-P on the same names.
* Treat "another run on the same day took the other side" as a reason to drop or halve a ≥70 name. This costs nothing to record and can be tested forward. Do not use agreement as a reason to add a name.
* Do not tighten the threshold on busy days on this evidence. If anything, test the opposite lever: on days with more than 19 names, look only at the first 10 by `hunt_priority`, and watch whether busy-day longs keep losing.

## Rerunning

```bash
git worktree add /tmp/split origin/claude/modest-davinci-mjddtu
python3 collect.py --split-root /tmp/split   # writes rows.json, prices from Yahoo where not frozen
python3 analyse.py    # question 1
python3 analyse2.py   # question 2
python3 analyse2b.py  # question 2, the follow-up cuts
python3 analyse3.py   # question 3
```

This is research, not investment advice.

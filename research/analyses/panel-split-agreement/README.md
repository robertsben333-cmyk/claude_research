# Split panels, busy days and agreement between runs (2026-10-26, updated 2026-10-27)

**Questions (Xavier, 2026-10-26).**

1. Do the 4x5 split panels (stage E-PS: four sessions of at most five names) score the high scorers better than the full E-P panel?
2. Is there any sign that on busy days we should be stricter and only take the top?
3. Now that several names were scored more than once on the same day (intraday snapshots, a Fable searcher, the split re-run), how much does agreement between those runs matter? And inside one panel, how much does agreement between the four judges matter?

**Short answers.**

1. No evidence either way. Two resolved days, 31 names. Both arms lost on their selected names (E-P 1 of 5 right, mean −3.7%; split 2 of 5, mean −1.1%). The more useful finding is that the two runs barely reproduce each other: ρ +0.49 between their scores, opposite sides on 10 of 31 names, and only 2 of the 8 selected names were picked by both.
2. Busy days did much worse, but taking only the top would not have helped. On the four days with 19 or more names, the ≥80 calls went 4 of 16, mean −6.2% (t −2.56, p 0.02), against 6 of 6 and +11.2% on days with 10 names or fewer. The top-1 per busy day went 0 of 4 and ≥90 went 1 of 5. So the problem was the days, not the threshold. All four busy days fall in one week (19 to 22 Oct), so a market regime explains this just as well as day size, and the August-September backtest showed no day-size effect.
3. Disagreement is a warning sign, agreement is not a buy signal. Names where another run took the other side did worse (−2.1% against −0.5%, n 31 and 60, difference t 1.44, p 0.15). Averaging the runs ranked no better than E-P alone. Inside one panel, a 2-2 split between judges was the worst group (4 of 16 right, −3.4%), but those names never reach 80 anyway. Nothing here clears a multiple-testing correction.

## Update 2026-10-27: 10-26 resolved, 10-27 scored

The short answers above and the tables in sections 2 and 3 are the 2026-10-26 version; section 1 is rewritten on the new data. What changed elsewhere is listed here.

The 10-26 split run (20 names) has resolved and is now in every table below. The 10-27 run (20 names) is scored but none of it has resolved yet: its amc names exit at tomorrow's open and its bmo names at 13:00 ET on the 28th.

* **Split against full, three days, 51 names.** Still no difference. Selected names: E-P 4 of 10 right, +2.0% (t 0.64); split 5 of 10, +3.2% (t 1.10). 10-26 was a good day for both arms (E-P +7.8% on 5, split +7.4% on 5), and they picked four of the same five.
* **Agreement between the two arms helps less than it seemed.** Names both arms selected on the same side: 2 of 6 right, +3.2%. E-P only: 2 of 4, +0.3%. Split only: 3 of 4, +3.2%. These samples are tiny.
* **Reproducibility varies a lot by day.** ρ between the two arms' scores was +0.36 on 10-22, +0.72 on 10-23, +0.78 on 10-26 and +0.49 on 10-27. On 10-27 the arms selected 6 and 5 names with only 3 in common (KIDS, LUNG, RBBN). BOOM was 96 long in E-P and 68 short in the split; OI was 94 short in E-P and flat in the split.
* **The busy-day result weakened.** 10-26 was a busy day (20 names) and its calls paid, so busy days now read 7 of 21, −2.9% (t −1.14, p 0.27), against 6 of 6, +11.2% on thin days. The direction holds; the significance is gone.
* **Disagreement between runs as a warning got a little stronger.** A name where another same-day run took the other side: −1.7% (n 37) against +0.3% (n 74), difference t 1.76, p 0.08; at panel_pct ≥ 70, +6.5 points, t 2.05, p 0.06 (n 28 and 7). Still one of about thirty tests.

## Data and window

`collect.py` reads every US panel run in October and prices each name on the scorebord window: entry 13:30 ET on the run day, amc names out at the next open, bmo names out at 13:00 ET on the report day. Gross, equal weight. A move already frozen in `dashboard/data/scorebord-frozen.json` is reused so the numbers match the scorebord. Every arm is priced on the E-P window, so differences come from the scores, not the timing.

| arm | days resolved | names | prompt / stage |
|---|---|---|---|
| E-P live | 15 (10-05 to 10-23) | 173 | us-panel v1/v2 (same searcher file, see the 10-21 post-mortem) |
| E-PS split, 4 shards of ≤5 | 3 (10-22, 10-23, 10-26), plus 10-27 scored | 51 | us-panel-split.v1, branch `claude/modest-davinci-mjddtu` |
| E-PI 10:00 snapshot | 2 (10-14, 10-19) | 29 matched | us-panel-intraday.v1 |
| E-PI 12:00 snapshot | 5 (10-14 to 10-21) | 51 matched | us-panel-intraday.v1 |
| E-PF Fable searcher | 2 (10-14, 10-16) | 11 | us-panel-fable.v1 |

Runs before 10-14 carry no `panel_pct`; it is recomputed the way the scorebord does (each judge against its own live range from earlier runs, mean of the signed percentiles). "Selected" means panel_pct ≥ 80 with all four judges, the live rule.

The arms are compared name by name and never pooled into one sample. Each arm's own result is reported on its own runs.

## 1. Split panels against the full panel

Same 51 names on 10-22, 10-23 and 10-26, each arm with its own Opus 5.5 searchers and its own four judges. (The first version of this report had 31 names on two days.)

| | E-P (one session) | E-PS (four sessions of ≤5) |
|---|---|---|
| within-day ρ against the move | −0.01 (p 0.97) | +0.11 (p 0.47) |
| selected (≥80) | 10: 4 right, +2.0% (t 0.64, p 0.54) | 10: 5 right, +3.2% (t 1.10, p 0.30) |
| panel_pct ≥ 60 | 26: 14 right, +2.3% (t 1.36) | 21: 10 right, +2.3% (t 1.37) |
| panel_pct ≥ 70 | 18: 10 right, +3.0% (t 1.26) | 14: 7 right, +3.0% (t 1.36) |
| top 3 per day | 9: 4 right, +1.8% | 9: 3 right, +1.3% |
| findings per name | 7.6 | 7.5 |

| day | names | ρ between arms | same side | E-P selected | split selected | both |
|---|---|---|---|---|---|---|
| 10-22 | 20 | +0.36 | 12 | BE, DECK, FIX, WRLD (−5.7%) | BE, FPH, MXL, WRLD (−1.9%) | BE, WRLD |
| 10-23 | 12 | +0.72 | 10 | MED (+4.3%) | CX (+2.1%) | none |
| 10-26 | 20 | +0.78 | 14 | AEYE, CLS, CVLT, GLXY, KNSA (+7.8%) | CLS, CVLT, DQ, GLXY, KNSA (+7.4%) | CLS, CVLT, GLXY, KNSA |
| 10-27 | 20 | +0.49 | 14 | BOOM, ENPH, KIDS, LUNG, OI, RBBN (open) | AMRN, KIDS, LUNG, RBBN, SEVN (open) | KIDS, LUNG, RBBN |

Selected by both arms on the same side: 6 names, 2 right, +3.2%. E-P only: 4, 2 right, +0.3%. Split only: 4, 3 right, +3.2%.

**Reading.** Over three resolved days the split is not better on the high scorers in any way that can be told from noise: ten names against ten, six of them shared. What the comparison does show is how much a full re-run moves the score. Over the four days the two arms' signed panel_pct correlate at ρ +0.36 to +0.78, and on 10-22 and 10-27 a third or more of the selected names were picked by one arm only. DECK on 10-22 was 90 long in E-P and 7 short in the split; BOOM on 10-27 was 96 long and 68 short. That is run-to-run noise in the searcher's evidence, and it is as large as most of the effects we try to measure. A fair answer to question 1 needs about ten resolved split days.

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

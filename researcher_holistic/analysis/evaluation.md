# Stage H evaluation

Generated 2026-11-11T19:40:11+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 35 names / 3 days; Brier 0.2492 (skill 0.003); direction 16/32 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 11/20 right, 3.376% on the lean's side (t 0.91, p 0.824); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 12 pairs, Brier diff -0.004 (t -0.45)

- **control (frozen hp.v1)**: 12 names / 3 days; Brier 0.2416 (skill 0.034); direction 5/10 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 4/4 right, 17.875% on the lean's side (t 1.47, p 0.125)

## The process: every evolving version against the frozen control, same names

12 pairs, mean Brier difference -0.004 (t -0.45, p 0.659). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

6 selected calls, 5 right, mean 8.169% (t 1.91). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 35 names / 3 days; Brier 0.2492 (skill 0.003); direction 16/32 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 11/20 right, 3.376% on the lean's side (t 0.91, p 0.824); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0)
- control: 12 names / 3 days; Brier 0.2416 (skill 0.034); direction 5/10 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 4/4 right, 17.875% on the lean's side (t 1.47, p 0.125)

## Gate

Current version hp.v2: 0 resolved names over 0 run days (needs 30 over 3). Gate closed. Drift alarm: no (12 recent pairs, diff -0.004, t -0.45).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

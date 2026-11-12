# Stage H evaluation

Generated 2026-11-12T19:30:04+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)

- **control (frozen hp.v1)**: 16 names / 4 days; Brier 0.2509 (skill -0.004); direction 5/13 (p 0.5810546875); 0 recs; leaning views: |p_up-50| >=5: 4/6 right, 8.978% on the lean's side (t 0.94, p 0.688); |p_up-50| >=7: 2/2 right, 1.993% on the lean's side (t 9.45, p 0.5)

## The process: every evolving version against the frozen control, same names

16 pairs, mean Brier difference -0.012 (t -1.53, p 0.148). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

7 selected calls, 5 right, mean 4.832% (t 0.98). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0)
- control: 16 names / 4 days; Brier 0.2509 (skill -0.004); direction 5/13 (p 0.5810546875); 0 recs; leaning views: |p_up-50| >=5: 4/6 right, 8.978% on the lean's side (t 0.94, p 0.688); |p_up-50| >=7: 2/2 right, 1.993% on the lean's side (t 9.45, p 0.5)

## Gate

Current version hp.v2: 0 resolved names over 0 run days (needs 30 over 3). Gate closed. Drift alarm: no (16 recent pairs, diff -0.012, t -1.53).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

# Stage H evaluation

Generated 2026-11-13T19:38:11+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 12 names / 1 days; Brier 0.2302 (skill 0.079); direction 8/11 (p 0.2265625); 0 recs; leaning views: |p_up-50| >=5: 4/5 right, 11.11% on the lean's side (t 2.17, p 0.375); |p_up-50| >=7: 1/1 right, 13.964% on the lean's side (t None, p 1.0); vs control on the same names: 4 pairs, Brier diff -0.016 (t -0.83)

- **control (frozen hp.v1)**: 20 names / 5 days; Brier 0.2462 (skill 0.015); direction 8/17 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 6/9 right, 9.415% on the lean's side (t 1.41, p 0.508); |p_up-50| >=7: 2/2 right, 1.993% on the lean's side (t 9.45, p 0.5)

- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

20 pairs, mean Brier difference -0.013 (t -1.79, p 0.089). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

10 selected calls, 8 right, mean 6.919% (t 1.72). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 59 names / 5 days; Brier 0.2462 (skill 0.015); direction 29/54 (p 0.6834892282353375); 0 recs; leaning views: |p_up-50| >=5: 17/29 right, 3.878% on the lean's side (t 1.35, p 0.458); |p_up-50| >=7: 8/10 right, 7.415% on the lean's side (t 2.31, p 0.109); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0)
- control: 20 names / 5 days; Brier 0.2462 (skill 0.015); direction 8/17 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 6/9 right, 9.415% on the lean's side (t 1.41, p 0.508); |p_up-50| >=7: 2/2 right, 1.993% on the lean's side (t 9.45, p 0.5)

## Gate

Current version hp.v2: 12 resolved names over 1 run days (needs 30 over 3). Gate closed. Drift alarm: no (20 recent pairs, diff -0.013, t -1.79).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

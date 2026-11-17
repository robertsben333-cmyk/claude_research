# Stage H evaluation

Generated 2026-11-17T19:41:13+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 36 names / 3 days; Brier 0.2257 (skill 0.097); direction 25/35 (p 0.01667384780012071); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 15/20 right, 8.912% on the lean's side (t 3.07, p 0.041); |p_up-50| >=7: 9/12 right, 10.227% on the lean's side (t 2.44, p 0.146); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375); vs control on the same names: 28 pairs, Brier diff -0.001 (t -0.07)

- **control (frozen hp.v1)**: 44 names / 7 days; Brier 0.2327 (skill 0.069); direction 25/40 (p 0.1538599441628321); 0 recs; leaning views: |p_up-50| >=5: 19/26 right, 9.502% on the lean's side (t 3.08, p 0.029); |p_up-50| >=7: 9/11 right, 9.106% on the lean's side (t 2.07, p 0.065); |p_up-50| >=10: 4/4 right, 16.245% on the lean's side (t 1.93, p 0.125)

- pairs with control design **all_names**: 24, Brier diff 0.002 (t 0.22)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

44 pairs, mean Brier difference -0.005 (t -0.8, p 0.428). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

19 selected calls, 15 right, mean 9.938% (t 2.96). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 60 names / 5 days; Brier 0.2362 (skill 0.055); direction 35/57 (p 0.11116111910399348); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 20/30 right, 6.164% on the lean's side (t 2.67, p 0.099); |p_up-50| >=7: 11/14 right, 10.268% on the lean's side (t 2.81, p 0.057); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375)
- control: 36 names / 5 days; Brier 0.2317 (skill 0.073); direction 21/32 (p 0.11018416518345475); 0 recs; leaning views: |p_up-50| >=5: 15/22 right, 7.979% on the lean's side (t 2.69, p 0.134); |p_up-50| >=7: 7/9 right, 10.687% on the lean's side (t 2.03, p 0.18); |p_up-50| >=10: 4/4 right, 16.245% on the lean's side (t 1.93, p 0.125)

## Gate

Current version hp.v2: 36 resolved names over 3 run days (needs 30 over 3). Gate OPEN. Drift alarm: no (44 recent pairs, diff -0.005, t -0.8).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

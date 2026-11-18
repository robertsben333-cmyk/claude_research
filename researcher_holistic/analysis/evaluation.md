# Stage H evaluation

Generated 2026-11-18T19:17:28+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 47 names / 4 days; Brier 0.2371 (skill 0.052); direction 27/46 (p 0.3019956131896606); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 16/24 right, 4.881% on the lean's side (t 1.45, p 0.152); |p_up-50| >=7: 9/12 right, 10.227% on the lean's side (t 2.44, p 0.146); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375); vs control on the same names: 39 pairs, Brier diff 0.002 (t 0.25)

- **control (frozen hp.v1)**: 55 names / 8 days; Brier 0.2396 (skill 0.042); direction 28/51 (p 0.5758493477318467); 0 recs; leaning views: |p_up-50| >=5: 21/31 right, 7.84% on the lean's side (t 2.53, p 0.071); |p_up-50| >=7: 10/13 right, 7.428% on the lean's side (t 1.92, p 0.092); |p_up-50| >=10: 4/4 right, 16.245% on the lean's side (t 1.93, p 0.125)

- pairs with control design **all_names**: 35, Brier diff 0.004 (t 0.51)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

55 pairs, mean Brier difference -0.002 (t -0.42, p 0.674). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

21 selected calls, 16 right, mean 10.135% (t 3.03). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 59 names / 5 days; Brier 0.2404 (skill 0.038); direction 32/57 (p 0.4270428565032551); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 18/28 right, 3.805% on the lean's side (t 1.25, p 0.185); |p_up-50| >=7: 9/12 right, 10.227% on the lean's side (t 2.44, p 0.146); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375)
- control: 43 names / 5 days; Brier 0.239 (skill 0.044); direction 23/41 (p 0.5327092552361137); 0 recs; leaning views: |p_up-50| >=5: 17/27 right, 6.353% on the lean's side (t 2.05, p 0.248); |p_up-50| >=7: 8/11 right, 8.416% on the lean's side (t 1.86, p 0.227); |p_up-50| >=10: 4/4 right, 16.245% on the lean's side (t 1.93, p 0.125)

## Gate

Current version hp.v3: 0 resolved names over 0 run days (needs 30 over 3). Gate closed. Drift alarm: no (55 recent pairs, diff -0.002, t -0.42).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

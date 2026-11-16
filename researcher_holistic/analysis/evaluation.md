# Stage H evaluation

Generated 2026-11-16T19:17:19+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 24 names / 2 days; Brier 0.2167 (skill 0.133); direction 18/23 (p 0.010622024536132812); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 10/12 right, 12.566% on the lean's side (t 3.52, p 0.039); |p_up-50| >=7: 6/7 right, 13.97% on the lean's side (t 2.69, p 0.125); |p_up-50| >=10: 3/3 right, 17.844% on the lean's side (t 2.11, p 0.25); vs control on the same names: 16 pairs, Brier diff -0.015 (t -1.7)

- **control (frozen hp.v1)**: 32 names / 6 days; Brier 0.2357 (skill 0.057); direction 16/28 (p 0.5715881884098053); 0 recs; leaning views: |p_up-50| >=5: 12/16 right, 11.783% on the lean's side (t 2.75, p 0.077); |p_up-50| >=7: 5/5 right, 10.243% on the lean's side (t 1.75, p 0.062); |p_up-50| >=10: 2/2 right, 17.905% on the lean's side (t 1.22, p 0.5)

- pairs with control design **all_names**: 12, Brier diff -0.015 (t -1.42)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

32 pairs, mean Brier difference -0.014 (t -2.32, p 0.027). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

13 selected calls, 11 right, mean 10.312% (t 2.59). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 59 names / 5 days; Brier 0.2342 (skill 0.063); direction 34/56 (p 0.14089542359848078); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 20/29 right, 5.793% on the lean's side (t 2.69, p 0.061); |p_up-50| >=7: 11/12 right, 11.159% on the lean's side (t 3.35, p 0.006); |p_up-50| >=10: 4/4 right, 13.828% on the lean's side (t 1.92, p 0.125)
- control: 28 names / 5 days; Brier 0.2356 (skill 0.058); direction 14/24 (p 0.5412561893463135); 0 recs; leaning views: |p_up-50| >=5: 10/14 right, 8.644% on the lean's side (t 2.32, p 0.18); |p_up-50| >=7: 5/5 right, 10.243% on the lean's side (t 1.75, p 0.062); |p_up-50| >=10: 2/2 right, 17.905% on the lean's side (t 1.22, p 0.5)

## Gate

Current version hp.v2: 24 resolved names over 2 run days (needs 30 over 3). Gate closed. Drift alarm: no (32 recent pairs, diff -0.014, t -2.32).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

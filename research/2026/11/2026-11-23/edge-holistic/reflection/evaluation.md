# Stage H evaluation

Generated 2026-11-23T19:38:31+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 48 names / 4 days; Brier 0.236 (skill 0.056); direction 28/47 (p 0.24296021728332562); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 17/25 right, 4.989% on the lean's side (t 1.54, p 0.108); |p_up-50| >=7: 10/13 right, 10.024% on the lean's side (t 2.6, p 0.092); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375); vs control on the same names: 40 pairs, Brier diff 0.001 (t 0.18)
- **hp.v3**: 26 names / 3 days; Brier 0.2391 (skill 0.044); direction 14/26 (p 0.8450189828872681); 0 recs; leaning views: |p_up-50| >=5: 10/14 right, 4.145% on the lean's side (t 2.19, p 0.18); |p_up-50| >=7: 4/5 right, 8.11% on the lean's side (t 1.94, p 0.375); |p_up-50| >=10: 3/3 right, 5.511% on the lean's side (t 5.49, p 0.25); vs control on the same names: 26 pairs, Brier diff -0.002 (t -0.21)

- **control (frozen hp.v1)**: 82 names / 11 days; Brier 0.2396 (skill 0.042); direction 44/77 (p 0.2543046661477); 0 recs; leaning views: |p_up-50| >=5: 30/45 right, 4.936% on the lean's side (t 2.14, p 0.036); |p_up-50| >=7: 13/17 right, 5.467% on the lean's side (t 1.75, p 0.049); |p_up-50| >=10: 5/5 right, 13.199% on the lean's side (t 1.83, p 0.062)

- pairs with control design **all_names**: 62, Brier diff 0.001 (t 0.16)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

82 pairs, mean Brier difference -0.002 (t -0.5, p 0.616). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

24 selected calls, 18 right, mean 9.554% (t 3.03). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 50 names / 5 days; Brier 0.2468 (skill 0.013); direction 24/50 (p 0.887724827340783); 0 recs; leaning views: |p_up-50| >=5: 17/27 right, 1.184% on the lean's side (t 0.48, p 0.248); |p_up-50| >=7: 8/11 right, 6.643% on the lean's side (t 1.92, p 0.227); |p_up-50| >=10: 4/5 right, 6.189% on the lean's side (t 0.96, p 0.375)
- control: 50 names / 5 days; Brier 0.2421 (skill 0.032); direction 28/49 (p 0.3916029105474905); 0 recs; leaning views: |p_up-50| >=5: 18/29 right, 1.158% on the lean's side (t 0.47, p 0.265); |p_up-50| >=7: 8/12 right, 3.476% on the lean's side (t 0.94, p 0.388); |p_up-50| >=10: 3/3 right, 10.062% on the lean's side (t 1.07, p 0.25)

## Gate

Current version hp.v3: 26 resolved names over 3 run days (needs 30 over 3). Gate closed. Drift alarm: no (60 recent pairs, diff 0.001, t 0.08).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

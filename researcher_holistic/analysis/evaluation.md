# Stage H evaluation

Generated 2026-11-24T19:32:22+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 48 names / 4 days; Brier 0.236 (skill 0.056); direction 28/47 (p 0.24296021728332562); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 17/25 right, 4.989% on the lean's side (t 1.54, p 0.108); |p_up-50| >=7: 10/13 right, 10.024% on the lean's side (t 2.6, p 0.092); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375); vs control on the same names: 40 pairs, Brier diff 0.001 (t 0.18)
- **hp.v3**: 38 names / 4 days; Brier 0.2397 (skill 0.041); direction 20/37 (p 0.7428293587290682); 0 recs; leaning views: |p_up-50| >=5: 15/22 right, 3.074% on the lean's side (t 1.51, p 0.134); |p_up-50| >=7: 8/9 right, 9.729% on the lean's side (t 3.75, p 0.039); |p_up-50| >=10: 3/3 right, 5.511% on the lean's side (t 5.49, p 0.25); vs control on the same names: 38 pairs, Brier diff 0.001 (t 0.09)

- **control (frozen hp.v1)**: 94 names / 12 days; Brier 0.239 (skill 0.044); direction 51/89 (p 0.20311681873649562); 0 recs; leaning views: |p_up-50| >=5: 34/50 right, 5.141% on the lean's side (t 2.41, p 0.015); |p_up-50| >=7: 15/20 right, 5.337% on the lean's side (t 1.88, p 0.041); |p_up-50| >=10: 6/6 right, 12.958% on the lean's side (t 2.2, p 0.031)

- pairs with control design **all_names**: 74, Brier diff 0.002 (t 0.37)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

94 pairs, mean Brier difference -0.001 (t -0.3, p 0.769). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

24 selected calls, 18 right, mean 9.554% (t 3.03). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 50 names / 5 days; Brier 0.2463 (skill 0.015); direction 23/49 (p 0.7754496546815659); 0 recs; leaning views: |p_up-50| >=5: 17/27 right, 0.523% on the lean's side (t 0.21, p 0.248); |p_up-50| >=7: 9/10 right, 9.515% on the lean's side (t 4.08, p 0.021); |p_up-50| >=10: 3/3 right, 5.511% on the lean's side (t 5.49, p 0.25)
- control: 50 names / 5 days; Brier 0.2445 (skill 0.022); direction 26/49 (p 0.7754496546815659); 0 recs; leaning views: |p_up-50| >=5: 15/24 right, 0.417% on the lean's side (t 0.16, p 0.307); |p_up-50| >=7: 6/9 right, 0.73% on the lean's side (t 0.25, p 0.508); |p_up-50| >=10: 2/2 right, 6.383% on the lean's side (t 1.19, p 0.5)

## Gate

Current version hp.v3: 38 resolved names over 4 run days (needs 30 over 3). Gate OPEN. Drift alarm: no (60 recent pairs, diff 0.006, t 1.0).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

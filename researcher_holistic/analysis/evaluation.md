# Stage H evaluation

Generated 2026-11-20T19:25:59+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 48 names / 4 days; Brier 0.236 (skill 0.056); direction 28/47 (p 0.24296021728332562); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 17/25 right, 4.989% on the lean's side (t 1.54, p 0.108); |p_up-50| >=7: 10/13 right, 10.024% on the lean's side (t 2.6, p 0.092); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375); vs control on the same names: 40 pairs, Brier diff 0.001 (t 0.18)
- **hp.v3**: 23 names / 2 days; Brier 0.2369 (skill 0.052); direction 13/23 (p 0.6776394844055176); 0 recs; leaning views: |p_up-50| >=5: 9/13 right, 4.36% on the lean's side (t 2.15, p 0.267); |p_up-50| >=7: 4/5 right, 8.11% on the lean's side (t 1.94, p 0.375); |p_up-50| >=10: 3/3 right, 5.511% on the lean's side (t 5.49, p 0.25); vs control on the same names: 23 pairs, Brier diff -0.002 (t -0.2)

- **control (frozen hp.v1)**: 79 names / 10 days; Brier 0.239 (skill 0.044); direction 43/74 (p 0.20067820312938572); 0 recs; leaning views: |p_up-50| >=5: 29/43 right, 5.555% on the lean's side (t 2.36, p 0.032); |p_up-50| >=7: 12/16 right, 5.724% on the lean's side (t 1.73, p 0.077); |p_up-50| >=10: 5/5 right, 13.199% on the lean's side (t 1.83, p 0.062)

- pairs with control design **all_names**: 59, Brier diff 0.001 (t 0.16)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

79 pairs, mean Brier difference -0.002 (t -0.5, p 0.62). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

24 selected calls, 18 right, mean 9.554% (t 3.03). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 59 names / 5 days; Brier 0.2375 (skill 0.05); direction 33/59 (p 0.4349928051221533); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 22/33 right, 3.814% on the lean's side (t 1.58, p 0.08); |p_up-50| >=7: 13/17 right, 9.229% on the lean's side (t 2.95, p 0.049); |p_up-50| >=10: 7/8 right, 10.559% on the lean's side (t 2.03, p 0.07)
- control: 59 names / 5 days; Brier 0.2365 (skill 0.054); direction 35/57 (p 0.11116111910399348); 0 recs; leaning views: |p_up-50| >=5: 23/34 right, 4.533% on the lean's side (t 1.87, p 0.058); |p_up-50| >=7: 10/14 right, 6.257% on the lean's side (t 1.66, p 0.18); |p_up-50| >=10: 5/5 right, 13.199% on the lean's side (t 1.83, p 0.062)

## Gate

Current version hp.v3: 23 resolved names over 2 run days (needs 30 over 3). Gate closed. Drift alarm: no (60 recent pairs, diff 0.001, t 0.16).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

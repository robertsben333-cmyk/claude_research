# Stage H evaluation

Generated 2026-11-19T19:31:15+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 48 names / 4 days; Brier 0.236 (skill 0.056); direction 28/47 (p 0.24296021728332562); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 17/25 right, 4.989% on the lean's side (t 1.54, p 0.108); |p_up-50| >=7: 10/13 right, 10.024% on the lean's side (t 2.6, p 0.092); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375); vs control on the same names: 40 pairs, Brier diff 0.001 (t 0.18)
- **hp.v3**: 12 names / 1 days; Brier 0.2285 (skill 0.086); direction 8/12 (p 0.3876953125); 0 recs; leaning views: |p_up-50| >=5: 5/5 right, 5.305% on the lean's side (t 3.01, p 0.062); |p_up-50| >=7: 1/1 right, 6.187% on the lean's side (t None, p 1.0); |p_up-50| >=10: 1/1 right, 6.187% on the lean's side (t None, p 1.0); vs control on the same names: 12 pairs, Brier diff -0.01 (t -0.7)

- **control (frozen hp.v1)**: 68 names / 9 days; Brier 0.2389 (skill 0.044); direction 36/63 (p 0.3135030532964529); 0 recs; leaning views: |p_up-50| >=5: 27/40 right, 5.93% on the lean's side (t 2.37, p 0.038); |p_up-50| >=7: 11/15 right, 5.87% on the lean's side (t 1.66, p 0.118); |p_up-50| >=10: 5/5 right, 13.199% on the lean's side (t 1.83, p 0.062)

- pairs with control design **all_names**: 48, Brier diff -0.0 (t -0.04)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

68 pairs, mean Brier difference -0.004 (t -0.78, p 0.438). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

23 selected calls, 17 right, mean 8.921% (t 2.77). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 60 names / 5 days; Brier 0.2345 (skill 0.062); direction 36/59 (p 0.11747735024505848); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 22/30 right, 5.042% on the lean's side (t 1.86, p 0.016); |p_up-50| >=7: 11/14 right, 9.75% on the lean's side (t 2.72, p 0.057); |p_up-50| >=10: 5/6 right, 12.354% on the lean's side (t 1.79, p 0.219)
- control: 52 names / 5 days; Brier 0.2352 (skill 0.059); direction 31/50 (p 0.11892045255943628); 0 recs; leaning views: |p_up-50| >=5: 23/34 right, 5.392% on the lean's side (t 2.17, p 0.058); |p_up-50| >=7: 9/13 right, 6.466% on the lean's side (t 1.59, p 0.267); |p_up-50| >=10: 5/5 right, 13.199% on the lean's side (t 1.83, p 0.062)

## Gate

Current version hp.v3: 12 resolved names over 1 run days (needs 30 over 3). Gate closed. Drift alarm: no (60 recent pairs, diff -0.004, t -0.68).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

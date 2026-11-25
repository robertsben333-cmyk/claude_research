# Stage H evaluation

Generated 2026-11-25T19:24:42+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 48 names / 4 days; Brier 0.236 (skill 0.056); direction 28/47 (p 0.24296021728332562); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 17/25 right, 4.989% on the lean's side (t 1.54, p 0.108); |p_up-50| >=7: 10/13 right, 10.024% on the lean's side (t 2.6, p 0.092); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375); vs control on the same names: 40 pairs, Brier diff 0.001 (t 0.18)
- **hp.v3**: 49 names / 5 days; Brier 0.2439 (skill 0.024); direction 25/48 (p 0.8854334972865132); 0 recs; leaning views: |p_up-50| >=5: 18/28 right, 3.046% on the lean's side (t 1.54, p 0.185); |p_up-50| >=7: 9/12 right, 7.374% on the lean's side (t 2.12, p 0.146); |p_up-50| >=10: 3/3 right, 5.511% on the lean's side (t 5.49, p 0.25); vs control on the same names: 49 pairs, Brier diff 0.002 (t 0.26)

- **control (frozen hp.v1)**: 105 names / 13 days; Brier 0.2405 (skill 0.038); direction 55/99 (p 0.3148798910376222); 0 recs; leaning views: |p_up-50| >=5: 36/54 right, 5.133% on the lean's side (t 2.52, p 0.02); |p_up-50| >=7: 16/21 right, 6.241% on the lean's side (t 2.19, p 0.027); |p_up-50| >=10: 6/6 right, 12.958% on the lean's side (t 2.2, p 0.031)

- pairs with control design **all_names**: 85, Brier diff 0.002 (t 0.49)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

105 pairs, mean Brier difference -0.001 (t -0.15, p 0.882). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

26 selected calls, 20 right, mean 10.055% (t 3.4). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 49 names / 5 days; Brier 0.2439 (skill 0.024); direction 25/48 (p 0.8854334972865132); 0 recs; leaning views: |p_up-50| >=5: 18/28 right, 3.046% on the lean's side (t 1.54, p 0.185); |p_up-50| >=7: 9/12 right, 7.374% on the lean's side (t 2.12, p 0.146); |p_up-50| >=10: 3/3 right, 5.511% on the lean's side (t 5.49, p 0.25)
- control: 49 names / 5 days; Brier 0.2423 (skill 0.031); direction 26/47 (p 0.5600646295802107); 0 recs; leaning views: |p_up-50| >=5: 14/22 right, 1.207% on the lean's side (t 0.54, p 0.286); |p_up-50| >=7: 6/8 right, 4.312% on the lean's side (t 1.0, p 0.289); |p_up-50| >=10: 2/2 right, 6.383% on the lean's side (t 1.19, p 0.5)

## Gate

Current version hp.v4: 0 resolved names over 0 run days (needs 30 over 3). Gate closed. Drift alarm: no (60 recent pairs, diff 0.002, t 0.4).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

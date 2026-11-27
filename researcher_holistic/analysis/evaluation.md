# Stage H evaluation

Generated 2026-11-27T19:19:12+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

Read the leaning views first: the claim under test is that some events can be called with some certainty, so a version is judged on the views it leans on and on its recommendations, not on its average Brier alone.

## Per playbook version (evolving arm)

- **hp.v1**: 47 names / 4 days; Brier 0.2502 (skill -0.001); direction 21/43 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 13/24 right, 2.372% on the lean's side (t 0.72, p 0.839); |p_up-50| >=7: 7/9 right, 6.688% on the lean's side (t 1.92, p 0.18); |p_up-50| >=10: 1/3 right, -1.572% on the lean's side (t -0.72, p 1.0); vs control on the same names: 16 pairs, Brier diff -0.012 (t -1.53)
- **hp.v2**: 48 names / 4 days; Brier 0.236 (skill 0.056); direction 28/47 (p 0.24296021728332562); 1 recs, 1 right, mean 3.254% (t None, p None); leaning views: |p_up-50| >=5: 17/25 right, 4.989% on the lean's side (t 1.54, p 0.108); |p_up-50| >=7: 10/13 right, 10.024% on the lean's side (t 2.6, p 0.092); |p_up-50| >=10: 4/5 right, 13.588% on the lean's side (t 1.63, p 0.375); vs control on the same names: 40 pairs, Brier diff 0.001 (t 0.18)
- **hp.v3**: 49 names / 5 days; Brier 0.2439 (skill 0.024); direction 25/48 (p 0.8854334972865132); 0 recs; leaning views: |p_up-50| >=5: 18/28 right, 3.046% on the lean's side (t 1.54, p 0.185); |p_up-50| >=7: 9/12 right, 7.374% on the lean's side (t 2.12, p 0.146); |p_up-50| >=10: 3/3 right, 5.511% on the lean's side (t 5.49, p 0.25); vs control on the same names: 49 pairs, Brier diff 0.002 (t 0.26)
- **hp.v4**: 3 names / 1 days; Brier 0.287 (skill -0.148); direction 1/3 (p 1.0); 0 recs; leaning views: |p_up-50| >=5: 1/3 right, -5.778% on the lean's side (t -1.23, p 1.0); |p_up-50| >=7: 1/3 right, -5.778% on the lean's side (t -1.23, p 1.0); vs control on the same names: 3 pairs, Brier diff 0.036 (t 0.93)

- **control (frozen hp.v1)**: 108 names / 14 days; Brier 0.2408 (skill 0.037); direction 56/101 (p 0.3197273207002655); 0 recs; leaning views: |p_up-50| >=5: 36/54 right, 5.133% on the lean's side (t 2.52, p 0.02); |p_up-50| >=7: 16/21 right, 6.241% on the lean's side (t 2.19, p 0.027); |p_up-50| >=10: 6/6 right, 12.958% on the lean's side (t 2.2, p 0.031)

- pairs with control design **all_names**: 88, Brier diff 0.003 (t 0.73)
- pairs with control design **random_share_0.34**: 20, Brier diff -0.013 (t -1.79)

## The process: every evolving version against the frozen control, same names

108 pairs, mean Brier difference 0.0 (t 0.1, p 0.917). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

26 selected calls, 20 right, mean 10.055% (t 3.4). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 40 names / 5 days; Brier 0.2518 (skill -0.007); direction 18/39 (p 0.7492586247608415); 0 recs; leaning views: |p_up-50| >=5: 14/26 right, 1.593% on the lean's side (t 0.72, p 0.845); |p_up-50| >=7: 9/14 right, 4.64% on the lean's side (t 1.35, p 0.424); |p_up-50| >=10: 2/2 right, 5.173% on the lean's side (t 3.16, p 0.5)
- control: 40 names / 5 days; Brier 0.2441 (skill 0.024); direction 20/38 (p 0.8714146793645341); 0 recs; leaning views: |p_up-50| >=5: 9/14 right, 2.858% on the lean's side (t 0.87, p 0.424); |p_up-50| >=7: 5/6 right, 7.169% on the lean's side (t 1.41, p 0.219); |p_up-50| >=10: 1/1 right, 11.751% on the lean's side (t None, p 1.0)

## Gate

Current version hp.v4: 3 resolved names over 1 run days (needs 30 over 3). Gate closed. Drift alarm: no (60 recent pairs, diff 0.004, t 0.69).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

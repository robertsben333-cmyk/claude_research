# Stage H evaluation

Generated 2026-11-10T19:34:43+00:00. Window: entry run-day close; amc exit next open; bmo exit 13:00 ET report day.

Below about 30 names a version's numbers are noise; below 20 recommendations a hit rate tells almost nothing.

## Per playbook version (evolving arm)

- **hp.v1**: 11 names / 1 days; Brier 0.2337 (skill 0.065); direction 6/11 (p 1.0); 0 recs; vs control on the same names: 4 pairs, Brier diff -0.013 (t -0.75)

- **control (frozen hp.v1)**: 4 names / 1 days; Brier 0.2374 (skill 0.05); direction 2/4 (p 1.0); 0 recs

## The process: every evolving version against the frozen control, same names

4 pairs, mean Brier difference -0.013 (t -0.75, p 0.506). The lineage row pools every evolving version on purpose: it tests the PROCESS (does self-revision beat a frozen approach on the same names), not any one version. Judge a version only on its own row.

## Stage E-P on the same names

3 selected calls, 3 right, mean 6.416% (t 2.64). stage E-P's selected calls (panel_pct >= 80) on the names stage H also researched, priced on stage H's window.

## Last five run days

- evolving: 11 names / 1 days; Brier 0.2337 (skill 0.065); direction 6/11 (p 1.0); 0 recs
- control: 4 names / 1 days; Brier 0.2374 (skill 0.05); direction 2/4 (p 1.0); 0 recs

## Gate

Current version hp.v1: 11 resolved names over 1 run days (needs 30 over 3). Gate closed. Drift alarm: no (4 recent pairs, diff -0.013, t -0.75).

revise only with >= 30 resolved names over >= 3 run days on the current version; at most 3 ops, each citing >= 3 resolved names; on a drift alarm only revert_to

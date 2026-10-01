# Re-judge, 2026-10-01: Opus 5 against Opus 5.5 on the same evidence

Question: would Opus 5, judging the evidence the Opus 5.5 hunters collected on
2026-09-23..09-29, have produced a better ranking or a better book?

Setup. `packs.json` holds, for each of the 32 resolved names, the sealed baseline and
every item the live Opus 5.5 hunter surfaced: filed findings, outside-window items and
'searched and found nothing' entries, with its sizes, verdicts and final numbers
removed. Two fresh cloud sessions, one on `claude-opus-5` and one on `claude-opus-5-5`
(served models confirmed), read only `brief.md` and `packs.json`. Neither made a web
search or a fetch. Each judged every item under the hunter definition and LESSONS.md.

Results (`score.py`, strategy exit, within-day Spearman, $0.2m turnover floor):

| arm | zeros | median abs | rho vs move | book at abs>=3 | book at abs>=1.5 | every nonzero name by sign |
|---|---|---|---|---|---|---|
| live Opus 5.5 hunt | 12 | 0.25 | -0.23 (p 0.26) | 0 names | 1 name, +16.4% | -2.63% on 20 |
| Opus 5 re-judge | 11 | 0.65 | -0.30 (p 0.13) | 0 names | 4 names, 2/4, +2.28% | -2.83% on 21 |
| Opus 5.5 re-judge | 14 | 0.30 | -0.27 (p 0.18) | 0 names | 0 names | -3.43% on 18 |
| Sonnet 5.5 re-judge | 5 | 1.00 | -0.18 (p 0.37) | 3 names, 3/3, +7.26% | 9 names, 4/9, -2.13% | -2.36% on 27 |

Opus 5 sizes the same evidence 1.77x larger and agrees on sign on 18 of 18 names where
both are nonzero. Its ranking is no better. The only name it puts past the 3.0 floor,
UXIN at -3.5, fails the turnover floor and rose 22.5%.

Sonnet 5.5 (`out-sonnet-5-5.json`, served model confirmed, no web requests) is the least
strict of the three: five zeros against 11-14, a median size of 1.0, and the least
negative ranking. Its three floor names (NEOV, GNS, BB) went 3 of 3, which is three
names and proves nothing.

Five days and 32 names; nothing here is significant.

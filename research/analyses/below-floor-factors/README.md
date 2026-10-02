# Below the floor: do the three "reliability" factors rescue weak scores?

**Question (2026-10-02).** The dashboard's hypothesis register shows three variables under
which the hunt's book does better: `retail_tilt` (H3), agreement with the sealed price lean
(H5) and a quiet Google search spike (H9). For names with **1 <= |impact_sum| < 2.8**, below
the conviction floor, does the hunt's sign become usable when those factors are favourable?

**Method.** `band.py` reads `dashboard/data/ledger.json` (141 resolved, de-duplicated US
names, 22 run days), uses the factor definitions frozen in `dashboard/scripts/weighting.py`
and scores the signed return at the strategy exit and at the close.

**Result: no.** In the band (44 names, 18 days; 40 of them Opus 5) the hunt's sign is a coin
flip (52.3%, -2.00% per name at the strategy exit). Each factor narrows the loss by under
1pp and none turns it positive. Names with every measurable factor favourable do worst
(14 names, 35.7%, -4.29%). Shorting every name in the band earns +3.27% (t 2.26). Same
picture at the close.

Above the floor the factors do separate (lean agrees 70.0% / +6.31% against 50.0% / -0.59%;
retail 71.8% against 39.1% hit rate). So they behave as amplifiers of a strong score, not
substitutes for one.

**A side result worth carrying.** Where lean and hunt disagree the two predictions are
exact opposites, so the lean "factor" is a contest between them. Over the 62 names above
the floor, trading the lean's sign alone returns +3.36% against +2.75% for the hunt's.

**What this does not show.** 44 names, no correction for the cuts tried, a band defined on
Opus 5's size scale (2.8 is about p50 there and p80 on Opus 5.5's), and the search factor
is measured for only 16 names in the band. With a per-name sd near 10%, a gap under about
6pp between two halves of the band is invisible.

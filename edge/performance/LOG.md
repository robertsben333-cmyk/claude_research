# Performance log

Append-only. One dated section per update, written by the `edge-performance` skill.
Three things in every entry: what closed and what resolved, the pooled ranking figure
beside its free control, and one sentence of critical read.

## 2026-09-17 — first build

Thirteen runs, 107 names priced, 102 in the ranking sample over 11 days (five names
are duplicate events: the 09-04 run re-hunted names the 09-07 run hunted again for
the same 09-08 prints, and the run closest to the print is the one kept). Eleven
positions at the broker, nine closed.

Closed so far, in entry order: HOFT +7.1%, ORCL −6.2%, FEIM −29.1%, RH −1.1%,
CODA −6.2%, FPS +15.6%, VRA +41.8%, RLGT +17.2%, LUXE +25.4%. Six of the nine were
closed by hand, not by stage E — three `opg`/`cls` orders filled, and HOFT and CODA
sat 95 hours before someone sold them. Open: ALMU and LEN, both entered 09-16.

Pooled over all 11 days: **ρ = −0.145** for `impact_sum` against the realised move,
against **−0.137** for the free control `-run_up_20d_pct`. The conviction test
(does the rank of |impact_sum| predict whether its sign was right) is +0.185, and
the sign was right on 59 of 101 names. Per day the picture splits cleanly: the five
days `edge/EDGE_ANALYSIS.md` was written on (08-31 … 09-07) pool at ρ ≈ +0.38 and
the conviction test at +0.44, in line with the +0.453 and +0.514 recorded there;
every day from 09-08 onward is at or below zero — 09-08 −0.333, 09-09 −0.290,
09-10 −0.200, 09-11 −0.316 — with 09-14 (+0.828) and 09-15 (+0.800) on four and
nine names pulling back the other way.

Account: $10,000 → $11,729, +17.3% over eight sessions, max drawdown −6.9%. Mean
per closed position +7.18% with a 95% interval of −6.4% to +20.8%.

**Read.** Nothing here is established and two things are worth watching. The
ranking has not beaten its free control on any pooled cut, and since 09-08 neither
of them sorts the day at all — which is the same window in which the sample stopped
being the one `EDGE_ANALYSIS.md` was written on. The account's +17% is one leg: six
longs at +17.7% against three shorts at −13.9%, in a week when shorting everything
paid −1.7% a name. Nine positions cannot separate a strategy from a market. The
number to watch over the next ten days is the conviction test on new days only,
because that is the one finding the repo rests its trading rule on.

*(This build re-prices every run from the raw `edge-scores.json` and Yahoo bars
rather than reading `edge/analysis/edge-rows.json`, so its figures for the first
six days sit a few hundredths from the frozen ones in `EDGE_ANALYSIS.md` — same
method, freshly computed, and the duplicate-event rule is derived rather than
hard-coded to a date.)*

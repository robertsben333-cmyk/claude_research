# Edge hunt — 2026-09-15 amc + 2026-09-16 bmo

**Ranking key: `impact_sum`** — the hunters' signed per-finding sizes added up, in points
of spot. Signed, unbounded, no call and no threshold. `edge-scores.json` names
`"ranking_key": "impact_sum"` and that is what is reported here.

Four names in the window. The sweep confirmed **4 of 4** from company sources, with
**zero phantom calendar rows** and zero unsettled sessions. 12 findings across 4 hunters,
one hunter per name.

## The ranking

| # | ticker | session | event | `impact_sum` | floor (≥3.0) | tradable | control `-run_up_20d_pct` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | LUXE | bmo | 2026-09-16 | **+3.00** | yes | yes — $0.78m/day | +6.96% |
| 2 | EPM | amc | 2026-09-15 | +2.50 | – | yes — $2.70m/day | +0.92% |
| 3 | TCOM | amc | 2026-09-15 | +0.50 | – | yes — $125.06m/day | +11.85% |
| 4 | ISPR | bmo | 2026-09-16 | **−5.10** | yes | **no — $0.03m/day, below the $0.2m floor** | +9.55% |

Two of four clear the conviction floor of 3.0: LUXE and ISPR.

## The finding driving the top name

**LUXE, +3.00.** The fiscal Q4 being reported is the quarter ended 30 June 2026 — the
window in which Richemont reported group sales +20% at constant rates with online retail
+18%, Kering posted its first positive comparable quarter in three years, and LVMH's
Fashion & Leather Goods returned to organic growth for the first time in seven quarters.
LuxExperience's own Q3 (to March) was flat ex-FX with management blaming "geopolitical
headwinds in March", so the demand comparison inverts *inside* the reported quarter.
Sized +1.8.
<https://www.richemont.com/news-media/press-releases-news/richemont-posts-strong-start-to-the-year-with-sales-up-by-20-at-constant-rates-for-its-first-quarter-ended-30-june-2026/>

**What the price already says:** the ADR is at $7.155, within 4% of its 52-week low and
−6.96% over 20 days, while Richemont and Kering re-rated; sell-side cut targets into the
print (TD Cowen $12→$8, JPMorgan $10→$9). The tape is treating LUXE as an idiosyncratic
restructuring rather than a luxury-sector name. The hunter's own stated counterweight is
that the **FY27 guide is the actual event**, it is being given for the first time, and it
had no evidence about it — which is why the number is +3.0 and not larger.

## The finding driving the bottom name

**ISPR, −5.10 — and it is the most interesting finding of the day.** Charlie's Holdings'
shareholder letter of 2026-09-09, seven days before Ispire's print, says the age-gated
launch is still only a "pilot test … this fall" and that shipping waits on Ispire's side.
Ispire's CEO told the 2026-02-06 call that Charlie's would launch "in the next two to
three months" at "between 2 million chips a month and 3 million chips a month" and that
"we should start seeing results in the next quarter" — i.e. exactly the Apr–Jun fiscal Q4
now being reported. Sized −2.5.
<https://www.globenewswire.com/news-release/2026/09/09/3358727/0/en/charlie-s-holdings-otcqb-chuc-issues-letter-to-shareholders.html>

Corroborated by two documents that are not the letter: Charlie's 10-Q for the quarter
ended 2026-06-30 contains **no mention of IKE, Ispire or age-gating anywhere in the
filing**, and Charlie's own Q1 release had already pushed the launch to "Q3 2026".

**What the price already says:** −9.55% over 20 days and −61% from the 52-week high, so
the hunter is adding to a direction the tape already leans. Its own stated tension is
exactly that. What is genuinely new is the partner-side evidence that the ramp did not
happen in the reported quarter.

**Nothing checked either finding.** See the caveats below.

## Names that could not be ranked

None. All four were rankable. But see the capacity section — "rankable" and "tradable"
are different questions and they disagree on the most convicted name in the run.

## What this table does not say

**The order is not the sign.** Below the conviction floor the sign of `impact_sum` is a
coin flip on the evidence so far — 53% over 38 resolved events. Above it, the rank of
conviction predicted sign-correctness at ρ=+0.514 (permutation p=0.0015), and above the
median conviction the sign was right on 74% of events. So EPM at +2.50 and TCOM at +0.50
are **not** bullish views; they are two names the hunt found little on. A reader treating
TCOM's +0.50 as a directional call is reading the table wrong. Note also that the
forward regime is one hunter per name, and on single-hunted names the conviction
correlation is **+0.361, not +0.514** — the higher figure was inflated by a double hunt
that no longer runs.

**`impact_sum` is not a forecast of the move.** It ranks; it does not size. The same fact
often appears in two findings from two sources and adding both double-counts it — which
is what the cluster-max was built to stop, and the cluster-max is what measurement
demoted. Regression slope against the realised move is 0.72–0.76, median absolute error
6–7 points against a realised standard deviation near 11. Both LUXE's and ISPR's hunters
flagged shared-document clusters in their own findings and trimmed for them by hand;
nothing downstream does.

**The control disagrees with the hunt today, strongly.** `-run_up_20d_pct` — one number
off the sealed baseline, available before a single subagent was spawned — ranks the day
TCOM (+11.85) > ISPR (+9.55) > LUXE (+6.96) > EPM (+0.92). Against the hunt's order that
is **Spearman ρ = −0.60**: near-inversion. On four names this is arithmetic, not evidence,
but it is worth stating plainly that **the hunt has still not been shown to beat that free
control** — over six resolved runs it ranked at ρ=0.335 against the hunt's raw 0.407, a
gap whose confidence interval spans zero, and when traded the control was positive on 6 of
6 days. TCOM's own hunter noted unprompted that its mildly positive read *agrees* with the
control and so may add nothing over it.

**Sign balance.** Three of four names leaned positive, one negative. At the finding level
it is exactly even: 6 positive, 6 negative of 12. That is a departure from the usual
pattern — six of eight leaned negative on 2026-08-31 — and worth recording, because the
standing worry is that asking hunters to find what the market has missed into a print
generates pessimism rather than detecting it. One day does not settle it either way.

**Nothing checked these findings.** There is no adversary pass and no second hunter, so a
factually wrong finding entered the key at full size and nothing in this run would have
caught it. That is the accepted cost of the one-hunter-per-name budget. It is not
hypothetical: the adversary, while it ran, caught a covenant amendment misread by a year
and a short-interest claim contradicted by its own source. Two specific soft spots in
today's run, both self-declared by the hunters: LUXE's 17.19m float figure is
uncorroborated and comes from the same vendor page as its short-interest number, and the
Q1+Q2 standalone GMVs sum to €1,273.8m against a reported H1 of €1,230.6m — a €43m
inconsistency the hunter could not resolve.

**The key is not reproducible to better than its own size.** When the stage still
double-hunted, twelve paired names came back with a median gap of 2.40 points and **four
of the twelve had opposite signs**, on a key whose typical magnitude is about 5. Nothing
re-measures that now. On today's table that caveat is larger than the gap between LUXE
(+3.00) and EPM (+2.50), and comparable to the whole spread from LUXE to TCOM.

**How much of the baseline was measured rather than inferred.** Two of four names have a
listed option chain, but only **one is usable**. TCOM's is liquid — 35,441 contracts of
open interest, a 6.89% straddle and a 6.54% event-implied move with balanced skew. LUXE's
carries 714 contracts total with an ATM bid-ask at 67% of mid, so its ~11% implied move is
indicative only and is not evidence of what the market expects. EPM (381 contracts, no
two-sided ATM legs) and ISPR have no usable chain at all, so their "expected move" is a
historical median, not a priced expectation. Any normalised correlation computed over this
day is therefore an implied-move measure for one name of four.

**Three of four baselines carry an unusable reaction history**, and the hunters were told
so explicitly. TCOM and LUXE are foreign private issuers whose 6-K text-matched "history"
is not earnings reactions — TCOM's most recent recorded "print" is the scheduling
announcement for this very event, and LUXE's list repeats 2025-11-19 three times. ISPR's
two recorded events are both over sixteen months old because four recent prints are
missing from the 8-K item 2.02 path. **EPM is the only name whose baseline history is a
real earnings base rate.** No baseline was amended: no name carried `suspect` (the only
verdict that blocks rankability), and upgrading the two `cadence_implausible` names would
have forgiven a history defect and handed each a 1.0 event multiplier neither has earned.

## What the day would cost to trade

This is the finding that matters most for anyone reading the table as a signal.

| ticker | turnover (spot × 20d avg volume) | reachable |
| --- | --- | --- |
| TCOM | $125.06m/day | yes, easily |
| EPM | $2.70m/day | yes |
| LUXE | $0.78m/day | yes, but thin |
| ISPR | **$0.03m/day** | **no** |

**The most convicted name in the run is untradeable, and it is the only negative.** ISPR
at −5.10 is the largest `|impact_sum|` of the day and turns over roughly $26,000 a day —
two-thirds of an order of magnitude below the $200k floor. So the traded book is
**one name, long, LUXE** — the smaller of the two floor-clearing convictions, on $780k a
day of turnover.

That means today, like 2026-09-14, **tests only the long half of the ranking**. On
2026-09-14 all four floor-clearing negatives were untradeable; today the single
floor-clearing negative is. Two days running, the short side of this ranking has been
unreachable, and a book that is structurally long-only is not a test of a signed ranking.
It is worth watching whether that is a recurring property of where this hunt finds
conviction — small, illiquid, heavily-shorted names — rather than a coincidence.

## One day is an anecdote

Four names cannot produce a meaningful rank correlation, and nothing in this note should
be read as a result. The pooled figure across many days is the result; `edge_resolve.py`
computes it, pooling within days. Four names is at the very bottom of the range this stage
has run on, and a day this thin contributes almost nothing to the pooled number either.

The standing position of the stage is unchanged: over six resolved runs the shipped
ranking has **not** been shown to beat `-run_up_20d_pct`, a free number available before
any subagent is spawned; and scored on 104 sealed backtest events the hunt found no rank
signal at all (ρ=+0.073, p=0.45). Read `edge/EDGE_ANALYSIS.md` and `backtest/FINDINGS.md`
§33 before weighing today's table.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.

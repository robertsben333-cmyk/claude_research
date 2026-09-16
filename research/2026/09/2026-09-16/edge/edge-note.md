# Edge hunt — 2026-09-16 amc + 2026-09-17 bmo

**Ranking key: `impact_sum`** — the hunters' signed per-finding sizes added up, in points
of spot. Signed, unbounded, no call and no threshold. `edge-scores.json` names
`"ranking_key": "impact_sum"` and that is what is reported here.

Four names in the window. The sweep confirmed **4 of 4** from company sources, with
**zero phantom calendar rows** and zero unsettled sessions. 11 findings across 4 hunters,
one hunter per name.

## The ranking

| # | ticker | session | event | `impact_sum` | floor (≥3.0) | tradable | control `-run_up_20d_pct` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | LEN.B | amc | 2026-09-16 | **+0.00** | – | yes — $6.59m/day | +6.01% |
| 2 | IPHA | bmo | 2026-09-17 | −2.20 | – | **no — $0.05m/day, below the $0.2m floor** | +6.28% |
| 3 | LEN | amc | 2026-09-16 | **−3.00** | yes | yes — $235.88m/day, borrow available | +5.86% |
| 4 | ALMU | amc | 2026-09-16 | **−5.00** | yes | yes — $6.17m/day, borrow available | +16.77% |

Two of four clear the conviction floor of 3.0: LEN and ALMU. Both are negative, and both
are tradable.

**Read the top row carefully.** LEN.B ranks first on a `+0.00` that is a *researched zero*,
not an absent hunt: its hunter measured the Class A/B discount over 30 sessions, checked
the buyback by class, the Section 16 trail, the index calendar and the dual-class
proposal, found nothing class-specific the market had missed, and returned an empty
findings list — which is the correct and complete answer its instructions ask for. A zero
sorts above every negative name by construction. On this day that is a four-name table
where the top row means "nothing found", not "most positive". The scorer cannot express
that difference and the note is where it has to be said.

## The finding driving the top name

There is no finding driving the top name. LEN.B returned zero findings.

What its hunter produced instead is worth recording, because it is a correction to two of
this run's own inputs:

- **The sweep row's central premise was wrong.** It told the hunter "the A/B discount is
  wide and mean-reverting". Measured daily from closes 2026-08-05 to 2026-09-16 it is
  neither: 1.54%–2.20%, mean 1.791%, 30-day sd about 0.18pp, no trend. Today's is
  ~1.57–1.85%, dead centre. The "wide discount" framing traces to a 2018 arbitrage piece
  that is the top search hit and is eight years stale.
  <https://stockanalysis.com/stocks/len.b/history/>
- **LEN.B's own sealed baseline understates this print.** Its `expected_move_pct` of 3.69%
  and `deadband_pct` of 1.84% come from seven prints in which B cushioned A's move by
  0.4–1.25pp — a cushion that existed only while the discount compressed from ~4.7% to
  ~1.8%. That compression finished: the last two prints show a cushion of 0.13pp
  (Mar-2026 +2.49 vs +2.62, Jun-2026 −4.77 vs −4.90). LEN.B should now move about 1.0×
  LEN, so its true expected absolute move tonight is nearer LEN's 6.33% than 3.69%.
  That is a correction to our baseline, not a market mispricing, which is why it is here
  and not in the findings — and it carries no sign, which is the other reason it cannot
  produce a non-zero key.

## The finding driving the bottom name

**ALMU, −5.00 — and it is the most interesting finding of the day.** Aeluma's own narrowed
FY26 guide of $4.2–4.6m, set against nine-month revenue of $3.879m, arithmetically implies
a Q4 of $321–721k. The fiscal-year sequence is then $1.4m → $1.3m → $1.2m → ~$0.59m, a 58%
decline across the year; FY26 revenue will be the company's first-ever annual *decline*
($4.2–4.6m against FY25's $4.7m); and the FY2027 guidance the company must issue tonight
has to be anchored to an exit run-rate annualising to about $2.3m against a ~$245m market
cap. Sized −4.0.
<https://www.aeluma.com/investors/news-events/press-releases/detail/105/aeluma-announces-third-quarter-fiscal-2026-financial-results>

The hunter is explicit that the Q4 revenue number itself is priced — four analysts carry
$586.5k, squarely inside the implied band. What it claims is unpriced is the second half
of tonight's event: the initial FY27 guide, and the fact that the exit rate it must be
built from is a 58%-decayed quarter. Its stated tail is that the company may decline to
guide FY27 at all, and a withheld guide reads as a cut.

Second leg, −2.5: the Sumitomo Chemical Advanced Technologies agreement announced
**2026-09-15, one trading day before the print**, is a *procurement* agreement — SCAT
supplies epiwafers **to** Aeluma from SCAT's own Phoenix tools — with no disclosed terms,
volumes or exclusivity, and the relationship was already public in April. The stock took
+4.70% on it ($12.54 → $13.13). The hunter's claim is that the market paid up for a cost
line read as a revenue line, and that this is the most reversible part of the current
price. <https://www.semiconductor-today.com/news_items/2026/sep/aeluma-scat-150926.shtml>

Offsetting leg, +1.5, and the hunter filed it against its own thesis: the $50m ATM opened
in March is essentially undrawn. Shares outstanding were 18,305,335 on 2026-08-26 (a field
on an unrelated Form 144) against 18,002,949 on the March 424B5 cover — +1.7% across five
months, consistent with equity compensation alone, where a meaningfully used $50m
programme would have issued roughly 3.5m shares. That closes the dilution tail, which is
why the net is −5.0 rather than larger.
<https://www.sec.gov/Archives/edgar/data/1828805/000162828026059045/xsl144X01/primary_doc.xml>

**What the price already says:** ALMU is −16.8% over 20 days and −57.5% from its 52-week
high, so the hunter is adding to a direction the tape already leans — and it says so. But
it cuts hard against the option skew, which at −11.04 vol points has upside being paid
for, and against this repo's own free control, which ranks ALMU as the day's **best** name.
Note the chain is close to unreadable: ATM spread is 56% of mid on 3,305 total OI, so the
13.05% "implied move" in the baseline is indicative, not a market statement.

**Nothing checked either finding.** See the caveats below.

## The other two names

**LEN, −3.00**, clears the floor. Three negative legs — a record Q4 embedded in the
company's own 82,000–83,000 full-year target (Q1 16,863 + Q2 20,519 + Q3 guided
20,500–21,500 leaves a Q4 of 23,118–25,118, i.e. +0.4% to +9.0% year over year); two
consecutive quarters landing at or below the bottom of its own guided ranges; and a Q4
order quarter that opened with the MBA 30-year contract rate at 6.97% after a fifth
straight monthly fall in new-home applications — against one +1.5 offset for a crowded
short base (~8.5% of free float, borrow 0.37%) at a 52-week low with a call-rich skew.
<https://www.sec.gov/Archives/edgar/data/0000920760/000162828026042551/ex991-2026531x8kq1.htm>

Its hunter raises one thing that bears on everything downstream: **the 6.33% event-implied
move is overstated as an earnings anchor**, because the 2026-09-18 straddle it was struck
from also spans today's 14:00 ET FOMC decision and dot plot and the 08:30 ET August
housing starts release on 09-17. Three events sit in one option. Any normalisation of
LEN's realised move by that number will understate the reaction.

**IPHA, −2.20**, does not clear the floor and cannot be traded at $0.05m a day. Its hunter's
main conclusion is a negative one worth keeping: the line the sweep called "the single most
repriceable" — cash runway — was **already published on 2026-08-14** as "through Q1 2028",
so this print carries less information than a semi-annual biotech print normally does. What
is left is a 30 June balance-sheet date that predates both of the company's cash events
(the Sobi $75m upfront announced 10 Aug, the €30m placement priced 14 Aug), an unconfirmed
antitrust closing condition on that $75m which neither issuer has announced as completed 37
days on, and a first-ever "early 2027" first-patient date for TELLOMAK-3 given at a
conference two days ago against prior guidance of H1-then-H2 2026 — partly offset by
PACIFIC-9, whose registry primary-completion date is 13 days after this print.

Two things its hunter caught that belong in the record. It **nearly filed a false finding**
and stopped: a history table rendered today's row as "Close $2.19, +17.74%", which was an
artefact of an unclosed session; the live quote at 13:08 ET was $1.97, +5.91%. And the
sealed baseline's `spot: 1.94` is a **mid-session snapshot** taken at 17:06 UTC, not a
close, although `last_close_date` reads 2026-09-16 — anything downstream treating it as an
entry close is using an intraday price. IPHA was also moving on ~3× normal volume into the
print with no sourceable cause.

## Names that could not be ranked

None. All four were rankable — `event_plausibility` was `fits_cadence` for LEN, LEN.B and
ALMU, and `unknown` for IPHA, which still ranks (only `suspect` blocks). See the note on
IPHA's history below.

## What this table does not say

**The order is not the sign.** Below the conviction floor the sign of `impact_sum` is a
coin flip on the evidence so far — 53% over 38 resolved events. Above it, the rank of
conviction predicted whether the sign was right at ρ=+0.514 (permutation p=0.0015) to the
next close. So LEN and ALMU are the two rows where the sign carries information; reading
IPHA's −2.20 as a bearish view, or LEN.B's +0.00 as a bullish one, is reading the table
wrong.

**`impact_sum` is not a forecast of the move.** It ranks; it does not size. Regression slope
0.72–0.76, median absolute error 6–7 points against a realised standard deviation near 11.
It also double-counts: the same fact appearing in two findings from two sources enters
twice, which is exactly what the cluster-max was built to stop and exactly what measurement
demoted. Both hunters that filed multiple findings disclosed partial overlap themselves —
ALMU's legs 1 and 2 share a thesis on different documents, IPHA's legs 1 and 2 share the
14 Aug runway release read two ways.

**The control beats nothing here, and it disagrees with the hunt almost completely.**
`-run_up_20d_pct` — one number off the sealed baseline, available before a single subagent
was spawned — ranks the day ALMU, IPHA, LEN.B, LEN. The hunt ranks it LEN.B, IPHA, LEN,
ALMU. Spearman between the two orders is **−0.40**: they are close to opposed, and the
name they disagree about hardest is the hunt's most convicted one. Over the six resolved
runs that free number ranked at ρ=0.335 against the hunt's raw 0.407, a gap whose CI spans
zero, and it was positive on 6 of 6 days when traded. **The hunt has not been shown to beat
it.** On this day they cannot both be right about ALMU.

**The sign balance is 3 negative, 1 zero, 0 positive.** That is the pattern to watch, not a
fact about these four companies: hunters asked to find what the market has missed into a
print have leaned negative before (six of eight on 2026-08-31). Individual hunters here
argued against themselves — ALMU filed a +1.5 leg that cuts its own thesis, LEN a +1.5
short-squeeze offset, IPHA a +1.5 PACIFIC-9 leg — but no name netted positive. If this
recurs across many days the hunter prompt is generating pessimism rather than detecting it,
and it is only visible because each note records the count.

**Nothing checked these findings.** There is no adversary pass and no second hunter, so a
factually wrong finding enters the key at full size and nothing in this run would have
caught it. That is the accepted cost of the one-hunter-per-name contract, and it is not
hypothetical: on 2026-09-09 the adversary caught a covenant amendment misread by a year and
a short-interest claim contradicted by its own source. Today the only such catches were the
hunters' own — IPHA's near-miss on a bogus +17.74% price row, LEN.B's refutation of the
sweep row it was handed.

**The key is not reproducible to better than its own size.** When the stage still
double-hunted, twelve paired names came back with a median gap of 2.40 points and **four of
the twelve had opposite signs**, on a key whose typical magnitude is about 5. Nothing
re-measures that now. On a table whose whole span is 5 points, the gap between LEN.B's
+0.00 and LEN's −3.00 is inside that noise.

**Two of four baselines were measured; two were inferred.** LEN has a real chain (ATM
spread 7.8% of mid, 47,283 OI, skew −0.77). ALMU's chain exists but is 56% of mid on 3,305
OI and should be read as a warning rather than a price. LEN.B and IPHA have **no options
market at all**, so their `expected_move_pct` is a historical median, and `priced_lean_pct`
falls back to −0.05 × the 20-day run-up. `edge_resolve.py` still normalises by the expected
move, so any normalised correlation for this day is not an implied-move measure. And LEN's
own 6.33% is contaminated by the FOMC and housing starts sharing its expiry, as above.

**IPHA's reaction history is not an earnings history.** `priced_in.py` inferred an 8-day
cadence from eight 6-K text matches; a semi-annual French reporter cannot print eight times
in three months. The sweep set `baseline_history_trustworthy: false` and the hunter was told
so explicitly before it opened the file. Its median_abs_move of 2.97%, its 3-up-of-8 base
rate and the 2026-08-10 +28.3% move are press and operational releases, not results
reactions. `edge_baseline_amend.py` proposed no change — correctly, because the cadence is
genuinely unrecoverable from those filings rather than wrong — so the baseline stands as
sealed with `verdict: unknown`.

**What the day would cost to trade.** Three of four names clear the $200k turnover floor;
IPHA at $48.5k a day does not, and it is not a marginal miss — it is a quarter of the floor,
on a name with no option chain, where the hunter noted any measured "move" is fragile.
Both floor-clearing names are tradable and both are shortable, so unlike 2026-09-14 the
extremes of this ranking are reachable. But the reachable extreme is only one end: the
table's positive end is a zero, so **the book this ranking implies is short-only** and tests
the short half of the hunt and nothing else. LEN at $236m a day is the only genuinely liquid
name in the window; ALMU and LEN.B are both around $6.5m, which is fine at this account size
and would not be at a larger one.

**LEN and LEN.B are one event, not two.** Two share classes of one issuer releasing one set
of Q3 FY2026 results after tonight's close. They appear as two rows because the room for an
unpriced finding genuinely differs — and the hunt found that room to be empty on the B side
— but they are **not two independent observations**, and any pooled statistic that counts
them as two is double-counting this print. `edge_resolve.py` will do exactly that unless
told otherwise; treat this day as three independent events, not four.

**One day is an anecdote.** Four names — three of them one company and a half-year report —
cannot produce a meaningful rank correlation. The pooled figure across many days is the
result, and today's contribution to it is small.

---

This is research, not financial advice. Earnings reactions are highly uncertain and can be
driven by market positioning, guidance, macro conditions, and management commentary rather
than reported results alone.

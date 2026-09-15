# Edge hunt — 2026-09-14 amc + 2026-09-15 bmo

**The ranking key is `impact_sum`** — the hunters' own signed per-finding sizes, added
up, in points of spot. `edge-scores.json` names it in its own `ranking_key` field. There
is no call, no threshold and no direction label anywhere below. Cut the table wherever
you like; that is the point of not bucketing it upstream.

9 names in the window, **9 of 9 confirmed by the sweep, 0 phantom rows**, 9 hunters,
**32 findings**, 6 names clear the conviction floor of 3.0.

## The ranking

| # | ticker | session | `impact_sum` | floor | tradable | control `-run_up_20d` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | VRA | **bmo** 09-15 | **+7.20** | yes | **yes** — long, $288k/d | +9.48 (5th) |
| 2 | FPS | **bmo** 09-15 | **+3.00** | yes | **yes** — long, $154.9m/d | +26.70 (8th) |
| 3 | RLGT | **amc** 09-14 | **+3.00** | yes | **yes** — long, $1.08m/d | +4.59 (3rd) |
| 4 | KMTS | **amc** 09-14 | +2.70 | – | yes — long, $5.90m/d | +15.94 (6th) |
| 5 | PLAY | **amc** 09-14 | +2.00 | – | yes — long, $12.9m/d | +18.35 (7th) |
| 6 | HITI | **amc** 09-14 | −1.60 | – | yes — borrow ok, $1.36m/d | −9.36 (1st) |
| 7 | COE | **bmo** 09-15 | **−3.00** | yes | **no** — not shortable | +43.67 (9th) |
| 8 | BIOX | **amc** 09-14 † | **−5.00** | yes | **no** — not shortable | +4.05 (2nd) |
| 9 | HYFT | **amc** 09-14 | **−7.00** | yes | **no** — $138k/d, under the $200k floor | +6.03 (4th) |

† BIOX's session is **unsettled** — the date is company-confirmed, the release hour is
not. Recorded as 09-14 amc on precedent only; see below.

**`floor` and `tradable` are different questions and the table keeps them apart.** The
floor is a selection decision about whether the sign means anything. Tradable is a fact
about the name — turnover against the $200k floor, and for a negative row whether
Alpaca will lend it. A name can be below the floor and perfectly tradable (KMTS, PLAY,
HITI) or top-of-table and barely reachable (VRA at $288k/day).

**Read down the tradable column and the day's real result appears: all four
floor-clearing NEGATIVES were untradeable.** COE and BIOX could not be borrowed and
HYFT — the single strongest conviction in the run at −7.00 — turns over $138k a day
against a $200k floor. So the book that actually went on was long-only and tested the
long half of this ranking only. The ranking itself is nine names; the tradable
expression of it was three.

Borrow is as the run recorded it at 2026-09-14 17:35 UTC, not as it reads now — Alpaca
re-checks shortability daily and **COE already reads borrowable this morning**. The
column is deliberately the run's own answer, because that is what the book was refused
on. Regenerate with `alpaca_trade.py assets --run <RUN>/edge` (`--live` for today's
borrow); HITI's borrow is a live lookup because the plan never checked it, being below
the floor.

`edge-scores.json` is the complete table, unfiltered and uncut — the ranking test needs
every name at every k. `alpaca-assets.json` carries the two columns above per name.

## The order is not the sign

Report the order; do not read the sign off a small number. Over the 38 de-duplicated
events resolved so far the sign of `impact_sum` is a **coin flip — 53%**. What carries
direction is `conviction` (the absolute value): its rank predicted whether the sign was
right at ρ=+0.514, permutation p=0.0015, and above the median conviction the sign was
right on 74% of events against 53% below it.

So the six floor-clearers above are where the sign means anything, and **KMTS at +2.70,
PLAY at +2.00 and HITI at −1.60 are ordering information only**. A reader treating
HITI's −1.60 as a bearish view is reading the table wrong.

One correction to the headline number, which applies to this run and every future one:
the +0.514 was measured while the day's top two names got two hunters each and the key
is a sum, so those names carried the largest conviction by construction. Rebuilt from a
single hunter per name it falls to **+0.361 (p=0.045)**. This run is one hunter per name,
so **+0.361 is the number to expect here, not +0.514.**

`impact_sum` is **not a forecast of the move**. The same fact often reaches two findings
from two sources and the key adds both — the cluster-max existed to stop exactly that and
was demoted because it lowered the correlation. Regression slope against the realised
move is 0.72–0.76 and median absolute error is 6–7 points against a realised standard
deviation near 11. The number ranks. It does not size.

## The free control, and the day's sharpest disagreement

`-run_up_20d_pct` — one number off the sealed baseline, available before a single
subagent was spawned — ranked the six resolved runs at **ρ=0.335** against the hunt's
raw 0.407, a gap whose confidence interval spans zero. **The hunt has not been shown to
beat it.** Today it is priced at 6 of 6 days positive when traded (+10.97pp), which is
the strongest sign-test result anything in this repo has.

Today the two orders **disagree substantially: Spearman between them is 0.209.** The
disagreement is concentrated in one name and it is worth stating plainly:

**COE is the control's best long and the hunt's third-worst name.** The control sees a
−43.67% 20-day slide — the largest drawdown in the window — and ranks it first. The
hunter's central finding is that the slide is not information: CEO Jack Jiajia Huang
bought COE ADSs on the open market under a 10b5-1 plan almost weekly from April through
2026-08-13, and has filed nothing since 2026-08-21 — 17 sessions and a 46% decline with
zero purchases, on a plan that demonstrably is not suspended by an earnings blackout
(it bought on 06-05 and filed 06-10, two days before the 06-12 Q1 release). If that read
is right, the run-up the control is ranking on is the withdrawal of a price-insensitive
bid rather than priced-in disappointment, and there is nothing to relieve.
[EDGAR Form 4 index](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001659494&type=4&dateb=&owner=include&count=100)

That is a genuine test of whether the hunt adds anything to the free number. It resolves
tomorrow; it is not evidence today.

## What drives the top and bottom

**Top — VRA, +7.20.** Vera Bradley's Q1 10-Q says it has filed IEEPA tariff refund
claims and will "recognize any related refunds and interest when cash is received", and
CBP's own refund machinery (CAPE Phase I opened 2026-04-20, 60–90 days from acceptance)
puts that cash inside the quarter that ended 2026-08-01. Size is anchored on management's
own number — the CFO said tariffs added ~$4.2m to year-end inventory value — which on
28.4m shares is roughly $0.10–0.18 a share against a single −$0.08 estimate.
[10-Q](https://www.sec.gov/Archives/edgar/data/1495320/000162828026042444/vra-20260502.htm) ·
[CBP](https://www.cbp.gov/trade/programs-administration/trade-remedies/ieepa-duty-refunds)
What the price says: nothing specific. The 25-delta skew is null, there is one estimate,
and the stock is −11.64% over five sessions into the print.

**A correlated-exposure warning on that name.** The IEEPA tariff-refund file also ranked
four of seventeen names on the 2026-09-10 run. It is one regulatory event, and a day (or
a pooled sample) that ranks several names on it is not carrying as many independent bets
as the row count suggests. The scorer cannot see this and does not adjust for it.

**Bottom — HYFT, −7.00.** Two things stack. The hunter discarded the baseline's reaction
history entirely — correctly, see below — and rebuilt it from the four 6-Ks it could
confirm were real earnings releases by EDGAR acceptance time: −20.4%, +1.1%, +2.3%,
−18.1%, mean signed −8.8% and median absolute 10.2%, against the baseline's 3.73% and a
tidy 4-up/4-down split. On top of that, at 08:46 ET **this morning**, hours before its own
amc print, MindWalk announced a "binding commitment" for a US$30m senior unsecured
revolver from "Sanabil (Cayman)" at 7.00% fixed with no covenants, no warrants, no
pledge, no MAC condition and a definitive agreement still to be negotiated — and the tape
paid +0.37% on about a fifth of normal volume.
[8-K exhibit](https://www.sec.gov/Archives/edgar/data/1715925/000119312526389966/hyft-ex99_1.htm)
The hunter also flagged that the CEO's "without issuing a single share" line is
contradicted by the 20-F's own disclosure of 357,760 ATM shares sold May–July 2026, inside
the quarter being reported tonight. What the price says: nothing usable — no option chain,
and the baseline's own anchors are both broken.

## Sign balance

**5 positive, 4 negative.** That is the most balanced any run has come back, and it is
worth recording as such: on 2026-08-31 six of eight leaned negative, which is more
plausibly an artefact of asking hunters to find what the market has missed into a print
than a fact about those companies. One balanced day is not evidence the prompt is neutral,
but the count is only visible if each note records it.

## What nothing checked

**No finding in this run was checked for being factually wrong.** There is no adversary
pass (removed 2026-09-09, both its numbers measured as subtractive over 215 findings) and
no second hunter. A factually wrong finding enters the key at full size and nothing here
would have caught it. The adversary was the only thing that ever did — on 2026-09-09 it
caught a covenant amendment misread by a year and a short-interest claim contradicted by
its own source. That is the accepted cost of nine names on nine hunters, and the reader
should not have to open the config to learn it.

**The key is not reproducible to better than its own size.** When the stage still
double-hunted, twelve paired names came back with a median gap of 2.40 points and **four
of the twelve had opposite signs**, on a key whose typical magnitude is about 5. Nothing
measures that any more. Read the table as an ordering with that much noise in it, not as
a set of estimates.

## How much of the baseline was measured rather than inferred

**3 of 9 names have a live option chain** — PLAY (15.84% event-implied), FPS (17.11%
straddle, 25-delta skew −22.46 vol points, i.e. upside paid) and VRA (21.11%). For the
other six, `priced_lean_pct` falls back to −0.05 × the 20-day run-up and the "expected
move" is a historical median rather than a priced expectation. So for two thirds of the
day, "what the market priced" is inferred, not measured, and `edge_resolve.py`'s
normalised correlation should not be described as an implied-move measure.

**3 of 9 baselines carried `cadence_implausible: true`** — BIOX, HITI and HYFT, all
foreign private issuers whose earnings cadence was inferred by 6-K text matching that
latched onto operational updates instead. The sweep independently set
`baseline_history_trustworthy: false` on the same three, and each of those hunters was
told so explicitly before it started, so none used an operational-update reaction history
as an earnings base rate. HYFT's hunter rebuilt the base rate from confirmed prints; the
gap between the baseline's 3.73% and its rebuilt 10.2% median absolute is a measure of
how wrong that anchor was.

**BIOX's session is unsettled.** The company confirmed a 2026-09-15 08:30 ET call saying
only that a release will be issued "prior to the call". It is recorded as 09-14 amc on
precedent (the fiscal Q3 release went out 2026-05-11 for a 2026-05-12 08:30 ET call), not
on a sourceable hour. `edge_resolve.py` measures the move over the session recorded, so
if the release is actually pre-open 09-15 this row is scored over the wrong window.

## What the day would have cost to trade

Capacity is in neither the scorer nor the budget, and the extremes of this ranking are
the thin end of it:

- **The top and bottom names are both near-untradeable.** VRA at #1 turns over $288k a
  day; HYFT at #9 turns over **$138k a day, below the $200k execution floor**, and BIOX
  at #8 is $202k — at the floor to within a rounding error.
- **Only 3 of 9 names trade above $5m a day**: FPS ($154.9m), PLAY ($12.9m), KMTS
  ($5.90m). Of those, only FPS clears the conviction floor.
- This matters because it has bitten before: on 2026-09-02 the single best-ranked name,
  DLTH, moved +23.20% on $170k a day, and six of the first 22 long/short positions traded
  under $1m a day. A ranking whose extremes cannot be traded is a research result, not a
  signal.

## One day is an anecdote

Nine names cannot produce a meaningful rank correlation, and nothing in this note should
be read as one. The result is the pooled figure across many days — and there, as of the
last decomposition, the shipped scorer ranks at ρ=0.243 (p=0.156, not significant), its
own raw inputs at ρ=0.407, and the free control at ρ=0.335 with a gap to the hunt whose
CI spans zero. Scored on the sealed 104-event backtest corpus the hunt found **no rank
signal at all** (ρ=+0.073, p=0.45). Read this table as one more day added to that sample,
not as a finding.

---

*This is research, not financial advice. Earnings reactions are highly uncertain and can
be driven by market positioning, guidance, macro conditions, and management commentary
rather than reported results alone.*

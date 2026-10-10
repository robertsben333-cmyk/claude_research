# Options on the most confident US names (2026-10-10)

Question (Xavier): for the names the US stages were most confident about, would an
options strategy have worked better than the stock, for instance an up/down bet?

## Short answer

No, not on what is on disk. Before costs a directional option on the Opus 5 confident
book looks better than the stock, but it is not significant, and the quoted spreads on
these names take it away. Long straddles lose on every cut, because the market's
event-implied move is larger than what these names actually do. And the hunt's edge sits
mostly in names that have no usable option chain at all. The Opus 5.5 October sample is
two to four names per stage, which is far too small to tell anything.

## Method

`options_overlay.py`, read-only, no orders. For every resolved name whose sealed baseline
holds a two-sided option quote (`options.status: ok`), it prices four ways to express the
call against the strategy exit the stock book uses (amc at the next open, bmo 20:00 CET):

| strategy | what it is |
|---|---|
| stock | sign of the call times the realised move, gross |
| option | ATM call if the call is up, ATM put if down |
| binary | a cash-or-nothing digital on the predicted side: the up/down bet |
| straddle | a long ATM straddle; with `abs_move_pct`, also long if the judge's move beats the event-implied move and short if not |

**Every option price is an estimate.** The baseline stored one quote (front expiry, ATM
IV, straddle mid, the worst leg's spread as a share of mid), never a chain at entry or
exit. Entry: Black-Scholes at the entry close with the sealed event variance kept. Exit:
Black-Scholes at the exit spot with implied vol fully crushed to 20-day realised vol.
Costs: half the quoted spread paid on each side (crossing the spread, as stage E's market
orders do). Quotes with a spread of 100% of mid or more are treated as untradeable. No
commissions, no skew. Returns are per dollar of premium.

Selections, each judged on its own (no pooling across versions or models; September
Opus 5.5 hunts out): stage E per prompt version at its own floor (3.0 Opus 5, 2.8 Opus
5.5) and, for `us.v9`, the book key `impact_scaled >= 1.76`; stage E-P's panel-selected
names; the four-model blind re-judge (`rejudge-four-models/`), labelled in-sample because
the panel rule was chosen on those names. Stage D had no confident name (largest
`impact_sum` 0.75) and stage R's names have no option chains, so both are left out.

## Results (net of crossing the spread)

| selection | n | stock | option | binary | long straddle |
|---|---|---|---|---|---|
| E `us.v4` Opus 5, \|impact_sum\| >= 3.0 | 21 | +2.3% (t 0.63, p 0.54) | +7.9% (p 0.81), median -85% | -18.7% (p 0.26) | -19.6% (p 0.14) |
| same, at mid (no spread) | 21 | | +41.0% (p 0.31) | +10.0% (p 0.61) | +14.9% (p 0.37) |
| same, filled halfway inside the spread | 21 | | +22.3% (p 0.53) | -6.2% (p 0.72) | -4.7% (p 0.74) |
| E `us.v9` Opus 5.5, \|impact_sum\| >= 2.8 | 2 | +2.7% | -43.9% | +12.4% | -59.0% |
| E `us.v9`, `impact_scaled` >= 1.76 | 1 | +0.6% | -69.3% | -9.9% | -73.2% |
| E-P panel-selected (Opus 5.5 October) | 3 | +3.6% (3 of 3) | -30.4% | +19.6% (2 of 3) | -54.3% |
| Re-judge, 3 of 4 models in own top 20% (in-sample) | 4 | +9.7% | +24.9% | +23.5% | -38.3% |
| Re-judge, Opus 5.5 own top 20% (in-sample) | 7 | +2.2% | | | |

p is a two-sided sign-flip test on the per-name mean. Rows with n under 5 are anecdotes.
The binary gated on the judge's own `p_up` beating the price paid: `us.v9` 7 names +8.0%
(p 0.69), E-P 3 names +19.6%. Too few to read.

**Three things that hold whatever the version:**

1. **The edge is where the options are not.** `us.v4` confident names with a usable chain
   returned +2.3% on the stock (n 21, 52% right, p 0.54); those without one +4.3% (n 24,
   67% right, t 2.36, p 0.029). The gap between the two is not itself significant, but the
   half you could trade with options carries no measurable edge on the stock either, and
   an option cannot create one.
2. **The market overprices the event move on these names.** Realised move over the
   event-implied move: median 0.65 over 76 names, only 25% moved more than implied. A long
   straddle on every name lost 36% of premium net (n 78, t -6.9, p < 0.001). A short
   straddle earned +10.5% at mid (71% right, p 0.11) but -32% after spreads, with single
   names losing 2-4x the premium (LUXE, FEIM, SIG, VRA). This pools every version on
   purpose: it describes the options market, not a prompt.
3. **Spreads are the cost that decides it.** The median quoted spread is 23% of mid and the
   top quarter is 59% or wider. The stock book's names are thin, and their options are
   thinner.

## What would change the answer

The binary on panel-selected names is the only arm that leans positive on every sample,
and it rests on 3 to 4 names. To test it properly the seal would have to store the ATM
and next strikes' bid and ask at entry, and the run would have to re-quote them at exit,
so a vertical spread (the tradeable form of an up/down bet) can be priced from real
quotes. About 30 panel-selected names with chains would be needed to see a 60% hit rate
against a coin; at one or two a day that is weeks.

## Rerun

`python3 options_overlay.py` writes `results.json` (every row, every group, the
sensitivity variants) and prints the tables. Reads `dashboard/data/ledger.json`, the
baselines and scaled/panel score files under `research/`, and
`../rejudge-four-models/`.

Research, not investment advice.

# Is the US $200k turnover floor in the right place, given earnings-day liquidity?

**Question (operator, 2026-10-09).** `execution.benchmark.min_dollar_volume_usd` drops any
name whose 20-day average dollar turnover is under $200k. Liquidity on an earnings date is
probably much higher than that average. Does that make the floor too strict?

**Method.** Every de-duplicated US name in `dashboard/data/ledger.json` (181 of 184 with
bars). Yahoo daily bars per name (`measure.py`, which writes `event-liquidity.json`; the
6 MB bar cache is not checked in). Turnover is defined as `alpaca_trade.py` defines it:
the mean volume over the 20 sessions before the entry day times the last close. Against
that: the entry day (the day stage E buys, about 13:30 ET, before the print), the reaction
day (the first session that trades the print) and the session after it. Spread is a
Corwin-Schultz half-spread over the same 20 pre-event days, which is a floor. Tables:
`python3 report.py`.

## Result

**The volume premise is right.** Reaction-day turnover is a median **3.5×** the 20-day
average (p25–p75 about 2.5–5.5×), and the thinner the name the larger the multiple: 5.6×
below $200k against 2.9× above $25m. The entry day is up too, about 2× (amc 2.3×, where the
entry day is the print day itself; bmo 1.7×).

| 20d turnover | n | reaction day × | entry day × | CS half-spread | median \|move\| |
|---|---|---|---|---|---|
| < $200k | 27 | 5.6 | 2.4 | 0.47% | 9.5% |
| $200k–1m | 23 | 4.2 | 1.9 | 0.52% | 6.9% |
| $1–5m | 22 | 3.7 | 2.1 | 0.31% | 8.3% |
| $5–25m | 36 | 3.6 | 1.6 | 0.32% | 7.3% |
| > $25m | 73 | 2.9 | 1.9 | 0.08% | 4.1% |

**It does not follow that the floor should move, for four reasons.**

1. **The floor guards the entry, and the entry is before the print.** The 3.5× is the
   exit day. Stage E buys around 13:30 ET on a day that runs at about 2×, with half of it
   gone. Below the floor a $3.7k position (33% of $11.2k equity) is a median 3.3% of the
   volume traded by then, at most 45%; at a 50% cap it is 5% and at most 68%. For a market
   order that is impact, not a rounding error. Only 14 of the 27 below-floor names cleared
   $200k even on the entry day.
2. **The extra volume arrives with the move.** The reaction multiple correlates +0.56 with
   the size of the move. The liquidity is there because the price is gapping, which is the
   moment a thin book's spread widens. Volume is not cost. For amc names the exit is a market
   order queued for the open, and the opening print is a fraction of the day's volume.
3. **The event multiple is close to a constant, so redefining the measure is the same as
   lowering the number.** Log 20-day turnover predicts log reaction-day turnover at
   r = 0.93. A floor of $200k on expected event-day volume is a floor of about $57k on the
   20-day average. The question is only ever "which number", not "which volume".
4. **The 1%-of-ADV position cap binds before the floor does.** `max_position_pct_of_adv: 1.0`
   caps a name at $2,000 at the floor, and binds below $370k (33% cap) or $560k (50% cap).
   A name at $100k gets a $1,000 position. Lowering the floor without touching that cap adds
   small positions, not exposure. If the event-volume argument is to be used anywhere, the
   cap is the place: 1% of expected event-day volume is about 3.5% of the 20-day average.

**What the floor costs is small.** 27 of 181 hunted names (15%) sit under it. A $100k floor
would add 10 names, $50k would add 18: well under one name a day over these runs.

**The research is no better or worse below the floor.** Above |impact_sum| 2.8: 5 of 11
right below the floor (mean +2.59%, median −2.94%) against 26 of 53 above it (+1.20%,
−0.28%). No band has a t above 0.8. Nothing here can rank the bands. The older 38-event
sample (`edge_turnover_floor.py`) had a higher floor helping monotonically, and was the
first sample, too.

**The spread is the deciding number and it is not measured.** Corwin-Schultz shows no cliff
at $200k (0.47% under, 0.52% at $200k–1m), but it is a floor estimate that misses gap days.
The quotes stage E records are the paper/IEX feed and are not usable: WOR, $22m a day,
logged a 29.8% quoted spread. One fill does stand out: VRA ($0.28m a day) filled 8.3% above
the recorded mid.

## What it does not show

- Paper fills are simulated, so nothing here measures real impact.
- Daily bars only: no intraday volume curve, so "half the day by 13:30" is an assumption.
- The below-floor tail holds meme spikes (KNDI 1,560×, SANG 976×, AENT 530×) that no one
  could have known in advance; the medians are the numbers to read.

## What would settle it

Record a SIP-grade bid and ask for every ranked name, not only the traded ones, at the
entry time and at each exit time, for a few weeks. That gives the spread by turnover band
on the days that matter, which is the one input this question turns on.

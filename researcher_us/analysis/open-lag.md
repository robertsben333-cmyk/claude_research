# Does the open miss the pre-market move? (2026-10-20)

Asked by the operator after AERO on 2026-10-20: the pre-market held the reaction
(15.00 against a 15.89 close, -5.6%), the stock opened at 15.28 (-3.8%), traded to
15.67 in the first minute, and was at 14.78 by 09:31. An exit "at the open" gives back
part of a gain the position already had. The operator also asked for the reverse: if
we are on the wrong side, a stale open is a better exit than what follows.

`researcher_us/scripts/open_lag.py` measures it on every US earnings event in the
repo's universe files (stages E, E-P, E-PF, E-PI, E-S, D), Yahoo 5m bars with pre- and
post-market, 2026-08-31 to 2026-10-20: 335 events, 322 measured, **231 with a
pre-market gap of at least 2%**. Output: `open-lag.json`, rows in `open-lag-rows.json`.
Everything is capture: the share of the pre-market move a price holds (1 = the
pre-market level, 0 = the old close).

## What it says

| | n | AERO pattern (open < 50%, back to >= 80% within 15 min) | Pre-market was wrong (open < 50%, still < 50% at 10:00) | Median capture at the open |
|---|---|---|---|---|
| All | 231 | 14 (6%) | 17 (7%) | 0.98 |
| amc | 109 | 6 (6%) | 7 (6%) | 1.00 |
| bmo | 122 | 8 (7%) | 10 (8%) | 0.97 |

**The open usually holds the whole pre-market move, and when it does not, the
pre-market is as often the wrong price as the open.** WOR on 2026-09-23 is the worked
counter-example: the open lagged back toward the old close and the stock kept going
past it.

**The systematic effect points the other way: after the open, earnings gaps fade.**
For a position on the side of the pre-market move, return relative to selling at the
official open:

| Exit | All 231 | Fresh pre-market 199 | Stale pre-market 32 |
|---|---|---|---|
| 09:35 | -0.75 (t -3.1) | -1.00 (t -3.8) | +0.89 (t 1.9) |
| 10:00 | -1.03 (t -2.8) | -1.44 (t -3.5) | +1.59 (t 2.4) |
| Day limit at the PM price | -0.59 (t -3.3) | -0.74 | +0.39 |
| Close | -1.03 (t -1.8) | -1.38 | +1.15 |

*Stale* means the last pre-market print came 31 or more minutes before the open, or
there were fewer than 6 five-minute pre-market bars. That is 14% of big-gap events,
and AERO is one of them (last print 08:32, 4 bars). The fresh-PM fade holds when you
cluster by day (32 days, mean of day means -1.27, t -2.4, 21 days negative) and holds
in both halves of the sample (-1.55 to 09-30, -1.12 from 10-01). It is larger for gaps
of 8% or more (-2.0 at 10:00).

Because the measurement is symmetric, the reverse falls out of it directly:

- **Fresh pre-market (86%).** A winning position should sell at the open, because
  waiting costs about 1 to 1.5 points. A losing position should wait until about 10:00,
  which gains the same amount on average. This is how the "use it when we're wrong"
  idea actually pays, although the mechanism is the post-open fade rather than the
  stale open.
- **Stale pre-market (14%).** The open lags (median capture 0.67), and for the winning
  side waiting to about 10:00 pays +1.6. The losing side should take the stale open.
  This is the AERO case. But the group holds 5 lag events against 9 fades, so it is
  n=32 and a lead, not a rule.

An adaptive rule using only what is visible at 09:25 (pre-market winning or losing,
fresh or stale) beats "always sell at the open" by about +0.2 points on the winning
side and +1.2 on the losing side. It was chosen on these same events.

## Follow-up checks (same day)

**Stale is not just illiquid.** Stale names are mostly thin: median 20-day turnover is
$2.7m, against $22.8m for fresh names. But the correlation with the turnover rank is
only -0.23. Among names under $5m a day, fresh ones fade like everything else (10:00
minus open -1.68) and stale ones go the other way (+2.56, t 3.1). In an OLS of
10:00-minus-open on stale and log turnover, turnover carries nothing (t 0.4) and stale
carries +3.1 (t 2.8). Adding log|gap| shrinks stale to +2.2 (t 1.9), because stale
pre-markets come with smaller gaps, and a bigger gap fades harder (t -2.5).

**The last pre-market print is a fragile reference.** On EFX, 2026-10-20, one 09:10
print sat exactly at the old close between 166-170 prints. Re-run with the median of
the last five pre-market bars as the reference (the reference moves by more than 1% on
88 of 231 events): the fresh-PM fade holds (-1.39, t -3.4, n 204). The stale effect
weakens to +0.99 (t 1.45, n 27), with 2 lag events against 6 fades. **The AERO-type
signal does not survive a better reference; the post-open fade does.**

**Stage M's own estimate, two mornings, six names.** Stage M's `expected_open_pct` sat
closer to the actual open than the last pre-market print on 3 of 6 names (EFX, AERO,
NOC), and further away on 3 (CLF, VICR, HAS). It loses where the price moved after its
09:00 snapshot: HAS read +0.1% at 08:56 and +4.0% at 09:25. Six names is an anecdote.

## What it does not establish

- **The live book does not exit at the open.** Since 2026-10-19 stage E-P sells
  everything at market in its skill step 3s, around 14:00 ET on the exit date. "Close
  AMC" scans only `research/*/*/*/edge`, so it never touches E-P's legs. AERO itself
  was never a position. The open matters today for stage M's advice, its control, the
  scorebord's static exit and the dashboard's `mv_open`. It would matter for money only
  if an at-open exit were restored, and that needs a person to change a Routine.
- **Yahoo's open is not our fill.** Alpaca paper fills a queued market order against
  the NBBO; the two recorded cases filled about 90 seconds after 09:30. Score any
  policy on the tape, never on paper fills.
- **Extended-hours bars carry no volume** from this source. "Stale" is measured as
  print count and recency. Imbalance feeds would be the real predictor, and we do not
  have them.
- **One sample, rules read off it.** The stale cut combines two bucket edges after
  seeing them, and 10:00 was picked from five horizons. Run it forward in stage M
  before anything trades on it.
- **Stage M fires at 08:56 ET**, but staleness is a 09:25 quantity. Its 5m feed also
  missed AERO's 08:32 print at 08:58.

    python3 researcher_us/scripts/open_lag.py --cache <dir> \
        --out researcher_us/analysis/open-lag.json \
        --rows-out researcher_us/analysis/open-lag-rows.json

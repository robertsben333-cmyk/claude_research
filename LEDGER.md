# Forecast accuracy ledger

Maintained by stage 4 (`earnings-calibration`), the morning after each run. Every call
is scored against the realised move, whether or not the result is flattering.

Measurement convention, applied identically every day: **close before the print → close
after the first full session following it.**

## Summary

_No runs scored yet._

| Metric | Panelled calls | Deep-dive preliminary reads |
| --- | --- | --- |
| Calls scored | — | — |
| Direction hit rate | — | — |
| Mean absolute magnitude error | — | — |
| Median absolute magnitude error | — | — |
| Band hit rate | — | n/a |
| Implied move broken | — | — |
| Red-team reversal fired | — | n/a |

### Calibration by certainty tier

The question this table exists to answer: **do High-certainty calls actually hit more
often than Low-certainty ones?** If they do not, the tiering is decorative and
`scripts/synthesize.py` needs fixing.

| Certainty | Calls | Direction hit rate |
| --- | --- | --- |
| High | — | — |
| Med | — | — |
| Low | — | — |
| Neutral / No Edge | — | — |

A `Neutral / No Edge` call is scored as a hit when the realised absolute move came in
below the expected move, and a miss when the stock moved hard and the panel had no view.

## Runs

| Date | Names | Panelled | Direction hits | Mean abs error | Notes |
| --- | --- | --- | --- | --- | --- |
| _(none yet)_ | | | | | |

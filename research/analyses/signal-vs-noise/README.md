# Signal against noise: why is the hunt right more often in volatile names?

**Question (2026-10-02).** `attention-proxies/` found that retail tilt is largely
volatility and that volatility alone splits the book's hit rate. The proposed
explanation was signal against noise: in a name that barely moves, the sign of the move
is mostly chance. Is that the mechanism, which indicators capture it best, and what would
it mean for the scripts?

**Method.** `analyse.py` tests five predictions written before any result was read
(listed in its docstring) on two samples: the live ledger (141 resolved US names, 22
days, strategy exit and close) and the sealed backtest corpus (52 usable events on 7
days, close to close, contaminated captures out), which is independent of the live days.
Every move is also adjusted for the market (beta x SPY) and the sector (beta x the SPDR
sector ETF) over exactly the ledger's window, using 5-minute bars for the 14:00 ET exit.
Twelve ex-ante indicators: realised vol 20d, daily sd 60d, idiosyncratic sd, the median
past earnings reaction, the option-implied move, the baseline expected move,
event-to-noise, implied-to-noise, market and sector R^2, |impact_sum| and |impact_sum| /
expected move.

## The noise mechanism is refuted

| prediction | result |
|---|---|
| P1 hit rate rises with the realised \|move\| | **No.** All names: 55 / 53 / 49% by tercile (strategy), 61 / 57 / 46% (close). Inside the deadband 53-60% against 52% outside. Corpus flat too. Small moves are not coin flips more than large ones |
| P2 event size and event-to-noise beat raw vol | **No.** Past reaction, implied move, expected move and event-to-noise are zero or negative. Only RECENT realised volatility predicts the hit rate (book rho +0.29 strategy, +0.20 close; corpus book +0.41) |
| P3 market adjustment closes the gap | **Barely.** The market explains a median 5-12% of a move. Book low/high vol 50/65% becomes 55/58% at the strategy exit; at the close 52/72% stays 57/70% |
| P4 equal return per unit of risk | **Live: the hit gap does not reach the money.** Book low-vol +4.2% against +1.9% high-vol (strategy), +2.4% / +2.7% (close). Corpus: it does, -5.1% against +4.1%, on 7 and 14 names |
| P5 conviction is a volatility selector | **Partly.** \|impact_sum\| correlates +0.25 with vol and +0.32 with the implied move: the hunter sizes larger where moves are larger. But the floor separates inside both volatility halves (low vol 50% / +4.2% above against 40% / -3.3% below) |

Within the book the effect sits in the top volatility third (rv20 at or above about 58%
annualised): 82% right against 50% and 45% for the lower two thirds at the strategy
exit, 77% against 55% and 60% at the close, with returns of +4.3%, +3.7% and -0.1%.

## Reading

The hunt is right more often in names that have been **moving a lot lately**, not in
names whose **earnings usually move them a lot**. That is the opposite of what a
signal-against-noise mechanism predicts, so that explanation (from the previous
analysis) is withdrawn. What recent volatility captures is open: a name in play with news
already flowing, a retail-held small cap, or continuation. Nothing here separates them.

In the live sample the higher hit rate does not buy a higher return per name, because
low-volatility book names win less often but larger. The corpus shows it in both. Two
samples pointing the same way on hit rate and opposite ways on return is not a basis for
a rule.

**What this does not show.** 62 live book names, 21 in the corpus, twelve indicators by
three outcomes by two populations: several nominal p < 0.05 are expected by chance and
none is corrected. The tercile cut at rv20 58 was read off these days.

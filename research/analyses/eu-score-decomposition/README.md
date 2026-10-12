# Why are European scores lower? (2026-10-12)

Question (operator, after `../country-thresholds/`): are European scores lower because the
hunters file fewer findings, or because each finding is sized smaller?

`python3 decompose.py > output.txt`. One unit is one hunt file; validation runs (synthetic
findings) and non-events are left out. |impact_sum| is split into findings per hunt x size
per finding x coherence (|sum f| / sum |f|: 1 when every finding points one way, near 0 when
they cancel). The judges' |impact| is split into `abs_move_pct` x certainty
(|2 p_up / 100 - 1|). Sizes are also read against each name's own reaction history, the
baseline's `history.median_abs_move_pct`.

## Result

**Neither, in relative terms. European stocks move less around results, and hunters and
judges both scale their sizes to each stock's own history.**

Hunters, October (shared core), per hunt:

| | hunts | findings | median size | mean size | coherence | mean \|sum\| | history move | size / history |
|---|---|---|---|---|---|---|---|---|
| US | 36 | 4.94 | 0.3 | 0.44 | 0.40 | 0.87 | 5.96% | 0.06 |
| EU | 16 | 4.19 | 0.3 | 0.32 | 0.47 | 0.57 | 4.09% | 0.07 |
| JP | 77 | 3.74 | 0.3 | 0.44 | 0.44 | 0.74 | 2.95% | 0.11 |

The US sums are 1.44x the European ones: findings 1.11x, size 1.36x, coherence 0.96x. The
history move is 1.46x. The median finding is the same size; the US mean is larger because
of a few large findings in the tail. Against its own history a European finding is if
anything slightly larger (0.07 against 0.06).

In September (Opus 5.5 before the core) the gap ran the other way, 0.60x: the US hunters
collapsed to 1.1 findings with 34% empty hunts while the European ones kept 2.0.

Judges: `abs_move_pct` is about 1.5x the name's history in every region (US 1.47-1.54,
Europe 1.17-1.52, Japan 1.15-1.24), so they scale the move to the stock. Certainty is
where Europe differed in the re-judge (0.08-0.12 against 0.10-0.16, mostly
September-era evidence); in the live October panels it does not (Europe 0.11-0.16, US
0.09-0.14). Live European judge sizes are 70-90% of the US ones, which is the volatility
difference and nothing else. Australia's re-judge certainty is near zero (0.02-0.04)
because 62% of those September hunts filed no finding.

## What it means for the thresholds

The low European scores are a rational response to smaller moves, not a weaker hunt.
A line set on the US scale therefore filters on volatility, not on conviction. That
supports scaling each market's panel seed by its move ratio, as stage IPO already does.

## What it does not show

October Europe is 16 hunts, ten of them UK; Opus 5-era Europe 9. Per country only the UK
has more than five hunts in any era. Whether the sizes are RIGHT, given the outcome, is
not tested here.

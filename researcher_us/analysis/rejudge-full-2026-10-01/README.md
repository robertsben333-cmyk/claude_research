# Full blinded re-judge, 2026-10-01: four models on every resolved run

Question: judging the evidence each live hunt collected, under the shared hunter core
(`config/hunter-core.md`), would Opus 5, Opus 5.5, Sonnet 5.5 or Fable 5.1 rank the day
better or run a better book than the live hunt did? And how does the |impact_sum|
threshold move the return per trade?

## Sample

`build_packs.py` writes `key.json` and the packs. 231 names: US 154, Europe 48, Japan
13, Australia 16 (Canada has no resolved run; stage R and the sealed backtest corpus are
left out on the operator's instruction). That is every resolved, rankable hunted name on
disk; foreign names drop out only where the event did not occur or the scorer marked
them unrankable.

- First pass (`packs-us1..us3`, `packs-eu`, `packs-apac`): 174 names.
- Second pass (`packs-x1`, `packs-x2`): 15 US hunts saved under suffixed names
  (`-a`, `-1`) that the first glob missed, and the 42 names whose ticker or company
  appears in CLAUDE.md, an agent definition or a LESSONS file. Those 42 are anonymised:
  ticker, company name and every URL replaced by placeholders. Product and executive
  names in the evidence text are not removed, so recognition is reduced, not ruled out.
  `packs-x2` also carries 9 corpus names; the scorer ignores them.

28 cloud sessions, one per pack per model, read only `brief.md`, their pack, the hunter
definition and LESSONS file. Every session ran on its configured model
(`claude-opus-5`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-fable-5-1`) and made
zero web searches and zero fetches. Outputs are `out-<pack>-<model>.json`; on every row
impact_sum = (2 x p_up / 100 - 1) x abs_move_pct.

## Method

`score_full.py` writes `scores.json`; `chart.py` draws `threshold-chart.html`. Return per
trade = sign(impact_sum) x realised move, **gross: no cost is assumed**. US names use the
strategy exit and the $200k turnover floor; other regions their resolver window.
Spearman is within day with a within-day permutation p. Three additions:

- **family-wise p**: the best t over 25 thresholds (at least 8 trades), tested against
  the same maximum with moves shuffled within each day;
- **floor re-derived by share**: per arm, the cut that selects the same share of nonzero
  tradable names as 3.0 did for the live hunt on its Opus 5 days (50%);
- **leave-one-day-out**: pick the threshold on the other days, trade the held-out day.

## Result

| group | n | short all | arm | rho (p) | >=3 | fw p (best t) | LOO |
|---|---|---|---|---|---|---|---|
| US, no anonymised | 128 | +2.09% | live | -0.05 (0.63) | +4.14% on 32 | 0.02 (3.71) | +6.6% on 10 |
| | | | Opus 5 | -0.06 (0.54) | +7.25% on 13 | 0.01 (5.08) | +10.6% on 10 |
| | | | Opus 5.5 | -0.08 (0.41) | +4.30% on 4 | 0.19 (1.79) | +5.7% on 14 |
| | | | Sonnet 5.5 | +0.01 (0.96) | 1 name | 0.00 (6.30) | +11.8% on 12 |
| | | | Fable 5.1 | -0.03 (0.81) | +7.51% on 6 | 0.19 (1.88) | +6.3% on 13 |
| Europe | 48 | -1.19% | live | +0.21 (0.18) | 5 names | | |
| | | | Opus 5.5 | +0.33 (0.03) | | | |
| | | | Fable 5.1 | +0.34 (0.02) | | | |
| Japan + Australia | 29 | -0.30% | all arms | -0.25 to -0.31 | | | |

No arm ranks the US day: rho is near zero for all five. What survives is the tail. The
largest calls carry the sign, and for the live hunt, Opus 5 and Sonnet 5.5 that survives
the correction for having picked the best of 25 thresholds. The re-judges' tails are
mostly the same names as the live hunt's largest (SWBI, YQ, RZLV, NNOX, SPWH); what they
add is dropping some of its large misses (MAMA, LOVE, VNCE, NX). Opus 5.5 is the weakest
re-judge in the US. In Europe the re-judges rank better than the live hunt, and Opus 5.5
and Fable reach p < 0.05 on 48 names. Japan and Australia are negative for every arm.

The tail sits almost entirely in the US runs up to 09-22. On the 35 US names from 09-23
on, every arm is negative at every cut with enough names. The anonymised names rank best
of all (live rho +0.42), which is what recognition would look like, so they are reported
apart and the clean rows above leave them out.

## Without the size: ranking on p_up - 50

`scores.json` carries a second key, `keys.pup`: each re-judge ranked on p_up - 50 alone,
in points, without multiplying by abs_move_pct. The live hunts before the shared core
carry no p_up, so this key has no live arm. The chart switches between the two keys.

| US, no anonymised (128) | rho impact / p_up | fw p impact / p_up | best t impact / p_up |
|---|---|---|---|
| Opus 5 | -0.06 / -0.09 | 0.01 / 0.24 | 5.08 / 2.18 |
| Opus 5.5 | -0.08 / -0.06 | 0.19 / 0.12 | 1.79 / 2.28 |
| Sonnet 5.5 | +0.01 / -0.02 | 0.00 / 0.01 | 6.30 / 3.98 |
| Fable 5.1 | -0.03 / -0.03 | 0.19 / 0.24 | 1.88 / 1.93 |

Dropping the size costs the US tail for the two re-judges that had one: Opus 5 loses it,
Sonnet 5.5 keeps a weaker one. In Europe direction alone ranks slightly better
(rho +0.29 to +0.37 against +0.27 to +0.34). So the expected size carries information
in the US, mostly by putting the names that move most at the top, and adds little
elsewhere.

## Caveats

Gross of every cost. Five arms and several groups were looked at, so the best family-wise
p here is itself a selection. The tail results rest on 10 to 30 trades, several of them
under $1m of daily turnover. The re-judges see only what the live hunter found; they test
judgement, not search.

## Which sample is the headline (operator's decision, 2026-10-01)

The full 231 names, anonymised ones included, are the headline sample, and the portfolio
calculator defaults to it. Leaving them out would drop the most informative cases,
the big convictions and trades this repo wrote about. The leakage check found no
sign that the judges used CLAUDE.md's quoted outcomes: on the anonymised names the
re-judges get the sign right 51-55% of the time against 50% for the live hunt, and
change the live sign on one or two names each. What the group does carry is selection:
larger live scores (median 3.00 against 1.10) and larger moves (6.5% against 4.6%).

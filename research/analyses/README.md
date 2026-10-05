# Analyses: one folder per question

The day-by-day research output lives in `research/<YYYY>/<MM>/<date>/`. This folder holds
the analyses run **over** those days: one folder per question, each with its own README
that states the question, the method, the result and what it does not show. Nothing here
is read by a live stage; the daily pipeline skips this folder because its names are not
dates.

## The analyses in this folder (October 2026)

| folder | question | headline |
|---|---|---|
| [`prompt-trial-opus55/`](prompt-trial-opus55/) | Why do Opus 5.5 hunters return near-zero sums since 09-23, and does a prompt change move them? | Neither era ranks measurably (Opus 5 ρ +0.14, p 0.18; Opus 5.5 −0.10, p 0.60). On three trial names, a brief where lessons resize instead of veto raised findings per name from 0.33 to 2-2.7. Three names: anecdote. |
| [`rejudge-opus5-vs-opus55/`](rejudge-opus5-vs-opus55/) | Same evidence, 32 names (09-23..09-29): would Opus 5 or Sonnet 5.5 have judged better than Opus 5.5? | Opus 5 sizes 1.77x larger with the same sign, but does not rank better. Five days; nothing is significant. |
| [`rejudge-four-models/`](rejudge-four-models/) | Every resolved name (231), judged blind by Opus 5, Opus 5.5, Sonnet 5.5 and Fable 5.1 from the live hunters' evidence. | No model ranks the whole US day. What survives is the tail: the largest calls carry the sign, and that holds against a correction for picking the best threshold. |
| [`portfolio-simulator/`](portfolio-simulator/) | Those calls traded as a compounding day-by-day book (model, key, cut, cap, weighting). | An interactive page (`portfolio.html`), gross of costs. |
| [`judge-lab/`](judge-lab/) | Which way of scoring the findings picks the right names in the **top 10-20%**: rules, fitted models, and agent judges written as skills (rubric, casebook, learned). | Fixed day split, sealed test set, three folds. The agent judges that learned from outcomes did worst. Plain re-judges on another model (Sonnet 5.5, Opus 5) did best in the top 15%: 20/25 and 18/25 against 15/25 for live. Seven arms on one sample: run forward before believing it. Then `ensemble.py` and `APPROACH.md`: the literature on AI forecasting, and an ensemble of the four re-judges gated on unanimity, which matches the best single model in every region (20/25 +6.6% all, 8/8 ex-US) without having to know which model that is. Learned aggregation overfits. |
| [`skillopt-judge/`](skillopt-judge/) | Can Microsoft's SkillOpt train the US panel judge's skill on resolved names (Sonnet 5.5 judge, Opus 5.5 optimizer, judge-lab split, margin gate)? | No. Both runs raised the gate score by abstaining (views 42 to 17, then 41 to 6) and did worse on the 25 unseen readout names (top 20% -0.3% and -2.2% against +4.0 to +8.9% for the seed). The slow update wrote five training tickers and a follow-the-lean rule into the skill. The harness works; the reward and the sample do not. |
| [`rejudge-opus55-v2-sizing/`](rejudge-opus55-v2-sizing/) | The 128 Opus 5-era names re-judged blind by Opus 5.5 under the two-measurement core (`us.v9`): does per-finding sizing bring back the Opus 5 scale and signal? | Filing comes back (3.75 findings per name against 1.12), size only halfway (median 1.70 against 3.00 live), so 3.0 buys 18% of US names against 50%. At a matched share the tail book equals live (+3.01% against +3.43%); no arm ranks the day. `impact_scaled` agrees with the sum (rho 0.94). Judgement only, not search. |
| [`below-floor-factors/`](below-floor-factors/) | Do retail tilt, lean agreement and a quiet search spike make the hunt's sign usable for 1 <= \|impact_sum\| < 2.8? | No. 44 names, 52% right, -2.0% per name; no factor or combination turns it positive, all-favourable is worst (36%, -4.3%). The factors separate only above the floor. |
| [`attention-proxies/`](attention-proxies/) | Are there better attention proxies than retail tilt and the search spike (analysts, size, options, Wikipedia, StockTwits, abnormal volume, 52-week high), and do they predict where the hunt is right? | No. Sixteen proxies and two composites, none survives the family-wise correction, leaders change with the exit. Retail tilt stays the strongest and is largely volatility (rank corr 0.74); volatility alone splits the book 81% / 39% right. |
| [`signal-vs-noise/`](signal-vs-noise/) | Is the hunt right more often in volatile names because tiny moves are coin flips (signal against noise), and which indicator captures it? Twelve ex-ante indicators, market and sector adjusted, live ledger plus the sealed corpus. | The noise mechanism is refuted: the hit rate does not rise with the realised move, and event size, implied move and event-to-noise predict nothing. Only RECENT realised volatility does (top third 82% right on the live book, corpus +0.41). Live it does not reach the return per name; in the corpus it does. |

Read them in this order. The prompt trial and the 32-name re-judge raised the question,
the four-model re-judge answered it on every name, and the simulator and the judge lab
build on its `key.json` and outputs.

## Rerunning

| folder | command | reads |
|---|---|---|
| `rejudge-four-models/` | `python3 build_packs.py` (packs), then `score_full.py`, `chart.py` | `research/`, `dashboard/data/ledger.json` |
| `portfolio-simulator/` | `python3 portfolio.py` | `../rejudge-four-models/` |
| `judge-lab/` | `python3 judge_lab.py score` / `compare` / `prepare` | `../rejudge-four-models/key.json` and packs, hunts in `research/` |

The re-judge outputs (`out-*.json`) and the judge outputs (`judges/*/out/`) come from
model sessions and cannot be rebuilt by a script. Each README says how they were made.

## Analyses kept elsewhere, and why

These stay where they are, because a live stage, the dashboard or a script reads their
paths. Moving them would break the thing that reads them.

| where | what |
|---|---|
| `researcher_us/EDGE_ANALYSIS.md` and `researcher_us/analysis/edge-*.json` / `.html` | Stage E's own analyses: decomposition, conviction floor, exit horizons (`edge-exit-hourly.html`), entry clock, run-up, search volume, hunter control, trading tables |
| `researcher_us/analysis/shadow/`, `shadow-ledger.json` | Stage E V2: the blind 8-K scorer and the κ fit |
| `researcher_us/EXECUTION.md` | What the Alpaca execution path does and does not do |
| `dashboard/` (`dashboard.html`, README) | The standing performance record: names, trades, account, and the hypothesis register |
| `archive/backtest/` (`FINDINGS.md`, `RESULTS.md`) | The sealed backtest, arms A/B/C and the edge corpus |
| `archive/claude_naive/` | Stage N, the naive forecast |
| `researcher_reversal/README.md`, `researcher_reversal/analysis/` | Phase 0 of stage R: 11,235 falls of 5% or more |
| `researcher_europe/SUBMARKET.md`, `researcher_australia/SUBMARKET.md`, `researcher_canada/SOURCES.md` | Why each foreign market is built the way it is, with the counts |

A new cross-cutting analysis goes in a new folder here, with a README and a row in the
first table.

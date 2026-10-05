# Which sources help predict the earnings reaction? A source-value registry (2026-10-05)

Question (the operator's, `PROMPT.md`): **which sources of evidence actually help predict how a
US stock reacts to its earnings, which do not, and does that differ between small and large
companies?** The end product is a registry with, per recognisable source type and size band,
an estimate of its usefulness, an interval and a verdict.

**This is a diagnostic. No scorer, no book and no hunter reads anything in this folder.**
Nothing live was edited.

## Answer in five lines

1. **Almost no source type carries the sign beyond drift on this sample.** Of 315 registry
   cells, 314 are "no evidence either way" and one is "probably works". 445 questions were
   tested; 22 reached p < 0.05, which is what chance alone gives (4.9%), and the smallest
   ledger-wide q is 0.22. Nothing is "works" or "misleads".
2. **The one "probably works" cell: the company's own disclosures in small caps** ($300m–2bn):
   55 voting items, 67% right, shrunk DV\* +0.17 [0.00, 0.33], same sign on 83% of held-out
   days. It does not replicate in the dossiers (only 2 small caps there) or clearly in
   Europe/Japan/Australia (turnover $1–25m: +0.40, p 0.06; under $1m: 0.0).
3. **Two leads held on a second, independent stratum** (the retired dossiers): items citing
   ownership filings (Form 4, 144, 13D/G) point the WRONG way (US hunts −0.43, p 0.015;
   dossiers −0.37, p 0.008), and items about the company itself beat items about others
   (hunts +0.41, p 0.03; dossiers +0.38, p 0.046). Neither held in the ex-US stratum.
4. **Large caps: the right calls do not generalise.** 6 of 26 large caps with a view were
   right with a real move. Their common feature, other companies reporting the same period
   (peers, customers, wholesale partners), fired on 6 other large caps and was wrong on all
   6; in the dossiers, peer read-across into large caps also points the wrong way
   (−0.20, p 0.028). The same rules work better in micro and small caps than in large ones.
5. **The strongest single result did not replicate.** In US hunts, fresh sources (≤ 30 days)
   point the wrong way and old ones (> 90 days) the right way (contrast z −3.7, p 0.0005,
   batch family-wise 0.002). In Europe/Japan/Australia the same contrast is zero (z −0.2).

What it means for the operator: on 158 US prints there is not enough data to rank source types
by usefulness, and the large-cap successes look like the hunt being right for case-specific
reasons, not for a reusable kind of source. Section "What would change this" says what would.

## Data and strata (Phase 0, `scripts/build.py`)

| stratum | what | prints | items | outcome |
|---|---|---|---|---|
| A | US edge hunts (stage E), ledger cut-off 2026-10-05T06:47Z, entries to 2026-10-01 | 158 (163 hunts) | 2,141 | strategy exit (amc open, bmo 20:00 CET) |
| A2 | stage E-P searcher hunts | 0 (none resolved) | 0 | |
| B | retired stage-2 dossiers with a scored outcome in `PREDICTIONS.csv` | 30 | 1,908 cited claims (mechanical extraction) | close to close |
| C | Europe (56), Japan (17), Australia (16) resolved hunts | 89 | 913 | each market's resolver window |
| D | sealed backtest corpus | excluded (`INCLUDE_CORPUS` not set) | | |

Size bands in A (prints): micro 57, small 37, mid 35, large 29. B is 14 large, 14 mid, 2 small.
C has no market cap and is banded by turnover. Every outcome is the move over the move the
baseline priced (option-implied, else expected, else median past reaction), Winsorised at ±4.

## Codebook (Phase 1, `codebook/`)

- **Mechanical layer** (`scripts/mechanical.py`): SEC form and 8-K items for 676 citations
  through the EDGAR accession (data.sec.gov, 207 filers), the rest by regex; newswire and
  whether the release is the company's own; domain class; source age.
- **Design**: one Opus 5.5 call on every item of a seeded 15% of packs (41 packs, 674 items),
  no outcomes: 70 subtypes in 8 groups with decision rules and precedence ($1.65).
  `codebook/codebook.md`. Frozen as v1 before any outcome was joined.
- **Labels**: Sonnet 5.5, isolated (`claude -p`, no tools, no MCP, no setting sources, temp
  cwd, the CLAUDE.md variables removed), twice, all 4,962 items ($38.6). Packs anonymised where
  the context names the company (A 33, B 5, C 17).
- **Agreement** (`codebook/agreement-v1.md`): subtype 92.3% exact; direction 96.9% (89.5%
  where either run gave a direction, 3 opposite signs); flags 93–99%. **17 subtypes below
  80% agreement were merged into their group** before any outcome was joined, among them the
  retail-finance portal, major press and trade press (all now `G:media`) and the
  pre-announcement/interim update (now `G:company_own`). The seed question on retail portals
  is therefore asked of the merged media code and of the retail-finance domain.

## Metrics and statistics (Phases 2 and 4, `METHODS.md`)

DV (vote × move/priced), **DV\*** (the same net of what a vote with no source earns in that
name: band mean and 20-day run-up, fitted leaving the day out), MV (presence → move larger than
priced), MgV (observational against the four-model median; ablation), prevalence. Permutation
p with 2,000 within-day shuffles keeping each print's items together; family-wise max-|z| per
batch; Benjamini–Hochberg q over the whole ledger; leave-one-day-out sign share; power per
question. Empirical-Bayes shrinkage cell → subtype → group → overall with one τ² per level.
**Amendment 1** (made on fake outcomes, before the real join): a directional verdict also
needs the cell's own raw 80% interval to exclude 0 on at least 10 voting items, because with τ²
near 0 every cell otherwise inherits its parent's verdict.

## The ledger (Phase 3, `ledger/questions.jsonl`)

445 questions in 13 batches, each committed before it was run. 325 on stratum A, 79 on B, 41 on
C. **Every question is under-powered** for a 10-point hit-rate gap at 80% power (that needs
about 196 independent prints for a one-sample test and 392 per arm for a contrast, more with
several items per print); their p is reported and not read as evidence of absence.

| verdict | questions |
|---|---|
| lead (p < 0.05, sign as predicted, not ledger-corrected) | 20 |
| opposite sign (p < 0.05) | 2 |
| no evidence (all flagged under-powered) | 417 |
| not computable (no voting items) | 6 |
| ledger q < 0.10 | 0 |

The leads, with what happened when they were tested elsewhere (batch b14):

| lead (stratum A unless said) | A | tested on | result |
|---|---|---|---|
| fresh (≤ 30 d) against old sources | −0.41, p 0.0005 | C | −0.06, p 0.86: **did not replicate** |
| items claiming a large move → bigger move than priced (MV) | +0.25, p 0.004 | B, C | +0.39 / +0.13, p 0.48 / 0.58: same sign, not significant |
| votes agreeing with the sealed price lean | +0.52, p 0.021 | C | +0.01: did not replicate |
| items about the company against items about others | +0.41, p 0.03 | B, C | **B +0.38, p 0.046**; C −0.04 |
| ownership filings (Form 4, 144, 13D/G) point the wrong way | −0.43, p 0.015 | B, C | **B −0.37, p 0.008**; C −0.35, p 0.45 |
| commodity / FX price items point the wrong way | −0.87, p 0.03 | B, C | B −1.08, p 0.048 (10 items); C one item |
| researcher-own items → bigger moves (MV) | +0.16, p 0.014 | B, C | no |
| company-own items better in high-volatility names | +0.44, p 0.03 | C | no |
| market data worse in amc than bmo | −1.16, p 0.025 | B | −0.22, p 0.27 |

Six of the 20 leads are single subtype-by-band cells with fewer than 15 voting items; they are
in `ledger/questions.jsonl` and not repeated here.

## The registry (Phase 6, `registry/REGISTRY.md`, `registry/registry-v1.json`)

315 rows: 55 codes (48 subtypes and 7 merged group codes) and 8 group rows, each overall and per
cap band, on stratum A, with B and C as replication columns. Shrinkage is heavy because the data
cannot tell the source types apart: the between-group variance τ² is 0, between subtypes 0.007,
between bands 0.027, against a typical cell standard error of 0.23–0.38 (interquartile, cells with at least 10 votes).

| | small companies (micro + small) | large companies (mid + large) |
|---|---|---|
| works | none | none |
| probably works | company's own disclosures, small caps (`company_own`, +0.17 [0.00, 0.33]) | none |
| no evidence either way | every other cell | every cell |
| probably misleads / misleads | none | none |

Raw (unshrunk) directions worth knowing, none of them a verdict: peer earnings results
−0.42 (35 votes, 41% right; also negative in B), commodity/FX prices −0.87 (12 votes; also
negative in B), the company's own results releases +0.43 (20 votes, 61%), history patterns
+0.84 (10 votes, 76%), the company's own periodic reports +0.11 (52 votes).

**Marginal value, observational**: the four judges are not right more often where a group's
net vote agrees with them (company-own +0.10, p 0.33; every other group negative and
insignificant). **Ablation** (`results/ablation.json`): see the table below.

ABLATION_TABLE

## Where the hunt gets large caps right (Phase 5, `casestudy/`)

Written in the order the prompt asks: the hits first (`casestudy/HITS.md`, committed before
the misses were opened), then rules (`casestudy/rules.json`), then the test
(`casestudy/rules-test.json`). **6 of the 26 large caps with a view were hits** (sign right
and a move above half the priced move): DELL, PANW, LULU, SUNB, AZO, NKE. Anecdotes, labelled
as such:

- **DELL (up, +8.7%)**: two direct server-assembler peers had reported the overlapping
  quarter with margin upside, and IDC data covered two of its three months.
- **PANW (down, −4.4%)**: a one-day +12.8% run-up on an M&A rumour, and the company's own
  release implied a share count that mechanically lowers the first FY27 EPS guide.
- **LULU (down, −19.4%)**: the guide was set on 4 June; a viral brand crisis in China came
  11–13 days later.
- **AZO (up, +5.6%)**: peer prints whose measuring periods ended before AZO's quarter, and a
  LIFO detail in its own 10-Q.
- **NKE (down, −7.4%)**: wholesale partners reporting sell-through weakness after Nike last
  spoke, and consensus at the ceiling of Nike's own framework.
- **SUNB (up, +7.3%)**: a near-zero view; not a reasoned call.

Six rules were derived from them and scored on prints they were not derived from:

| rule | other large caps | mid caps | micro + small |
|---|---|---|---|
| R1 same-period read-across (peers, customers, industry data, quantified, in window) | **0 of 6 right** | 6 of 13 | 10 of 26 |
| R2 the same with two or more items | never fired | 1 of 2 | 1 of 1 |
| R3 unread detail in the company's own filing | 1 of 4 | 5 of 9 | 20 of 33 |
| R4 fresh, not widely reported, not company-own | 2 of 9 | 7 of 20 | 31 of 63 |
| R5 R1 or R3 | 0 of 7 | 9 of 17 | 25 of 49 |
| R6 large claims, quantified, not widely reported | **0 of 5** | 7 of 11 | **36 of 56** |

**The large-cap rules do not generalise inside large caps**: every rule is at or below a coin
flip on the other large caps, and the read-across rule is wrong every time it fires. R1
fired on CRDO, COO, ADBE, KR, CPRT and JBL, with the same kind of evidence as the hits, and
pointed the wrong way each time. In the dossiers, peer read-across into large caps is also
negative (−0.20, p 0.028). The rules derived from large caps do better in micro and small caps
(R6 64%, R3 61%), but as ledger questions on those rows (b14-17, b14-20) they are not
significant (p 0.19, 0.39) and they do not hold in B or C.

So the operator's observation is right in the narrow sense (the hunt has some striking large-cap
calls) and the explanation offered by the data is that they are case-specific: the same kind of
evidence, read the same way, was wrong as often or more on the other large caps.

## What this does NOT show

- **That sources are useless.** 158 US prints with about 520 directional items, spread over
  55 codes and four bands, cannot detect a 10-point hit-rate edge for almost any cell. "No
  evidence" means the interval spans zero, not that the value is zero.
- **Anything about the hunter's sizes as a ranking.** The registry is about the labeller's
  per-item direction. The labeller follows the hunter's own sign almost always (487 of 490
  filed items where both give a sign agree), so "a source type's vote" is close to "the hunter's reading of that
  source".
- **Causal value.** DV\* is observational. The ablation arm is the closest thing, and it
  measures one judge (Sonnet 5.5) on one brief.
- **Anything about the stage E-P searcher** (no resolved hunt) or the sealed corpus (excluded).
- Stratum B's outcome is close-to-close and its items are cited claims, not findings; C has no
  option anchor anywhere and two-thirds of its rows are thin names.

## What would change this

1. **Forward days.** `scripts/label_forward.py` + `scripts/update_registry.py` label every newly
   resolved US hunt with the frozen v1 codebook and add a forward column; a verdict is
   CONFIRMED only when the forward data agree. At about 6 US prints a day, the small-cap
   company-own cell needs a few hundred more prints to settle.
2. **The two leads that held in B** (ownership filings wrong way; company-own beats
   other-company) are the first to watch forward; they are the only results here that held on
   an independent stratum.
3. **A stratum disagreeing**: C contradicts the fresh-vs-old lead; if forward US days also
   show nothing, it was noise in A.
4. **More ablation.** It is cheap (about $1–5 per code because only packs holding the code are
   re-judged) and could run on every code; it says what a judge loses, not whether the source
   is right.

## Rerun

```bash
python3 scripts/build.py && python3 scripts/mechanical.py          # sample + mechanical fields
python3 scripts/codebook_design.py && python3 scripts/freeze_codebook.py   # (v1 is frozen; do not rerun)
python3 scripts/label.py --strata A,B,C --runs 2 && python3 scripts/agreement.py
python3 scripts/gen_batches.py b01 b02 bx b07 b08 b09 b10 b11 b12 b13
python3 scripts/questions.py register ledger/batches/<b>.json && python3 scripts/questions.py run <b>
python3 scripts/registry.py                                        # registry/registry-v1.json, REGISTRY.md
python3 scripts/ablation.py intact | ablate <codes> | score
python3 scripts/casestudy.py hits | test
python3 scripts/label_forward.py && python3 scripts/update_registry.py   # forward refresh, never over v1
```

`SV_FAKE=1` replaces every move with seeded noise, for testing code without reading an outcome.
Budget and every model call: `ledger/budget.json`, `ledger/calls.jsonl`. Status trail:
`STATUS.md`.

## Files

| file | what |
|---|---|
| `PROMPT.md` | the run's instructions |
| `STATUS.md` | heartbeat and every conservative choice made |
| `METHODS.md` | metrics, bands, statistics, verdict rules, amendment 1 |
| `data/` | events, items, packs per stratum, mechanical fields, sample counts |
| `codebook/` | design input and raw call, codebook v1, labeller prompt, agreement, merges |
| `labels/v1/run{0,1}/` | the two labelling runs |
| `ledger/` | the question ledger, batch files, budget, call log |
| `registry/` | registry v1 (JSON and readable) |
| `casestudy/` | large-cap hits, rules, rule test |
| `results/` | batch run log, ablation judgements and scores |
| `scripts/` | everything above |

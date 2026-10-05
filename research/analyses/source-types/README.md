# Which kinds of evidence carry the sign? (2026-10-05)

Question (the operator's, after `../skillopt-judge/`'s rating test): the judge rated
packs with low reliability and low sufficiency, and those names seemed to do best. Is
there a TYPE of source, unreliable or thin, that scores, and what is it?

**Answer: no unreliable source type scores, and the low-sufficiency edge is a property
of the name, not of the source.** Over all 158 US prints:

- Items the labeler rates least reliable point the WRONG way more often than not
  (44.8% right, mean −0.35× the priced move). Unreliable and obscure is worst (39.6%).
  This held on the sealed test days.
- What carries the sign, weakly, is the company's own disclosure in names the option
  market does not price: press releases (65% right) and the issuer's own filings,
  read with middling, not top, reliability. Macro, peer read-across and positioning
  items point the wrong way. The focal-disclosure result held on the sealed days.
- "Low sufficiency" is a thin, small, option-less name without a consensus bar. The
  judges get the sign right more often there (68% against ~50%), but on the sealed
  test days that contrast reversed (C1) or went flat (C2), so it is not established.
  Much of it is drift: 58% of these names fell, and the judges mostly called them down.
- Nothing survives a family-wise correction: 132 cells tested, best family-wise p 0.51
  on the full sample.

## Data (`build.py`)

Every resolved US hunt on disk: the dashboard ledger's 163 hunts, **158 prints** (the 154
of `../rejudge-four-models/` including the 33 anonymised packs, the five 09-04 hunts of
09-08 prints counted once with their 09-07 twins, and MKC, AYI, ACN and NKE resolved
since). **2,141 evidence items**: 567 filed findings with the live hunter's signed size,
61 placed outside the window, 3 rejected candidates, 1,510 "searched, found nothing"
notes. Outcome: the strategy exit (amc at the open, bmo 20:00 CET), as a multiple of the
move the baseline priced (option-implied, else the expected move, else the median past
reaction).

Item order matches the re-judge packs, so every item joins to the four-model re-judges
(`opus5`, `opus` = Opus 5.5, `sonnet`, `fable`, and `median4`), the live hunt, and the
rated Sonnet judge of `../skillopt-judge/`.

## Labels

- **Source class by domain** (`data/domain_classes_llm.json`): 408 cited domains into 14
  classes by one Opus 5.5 call, audited on the 40 largest domains (all correct).
  sec.gov is 47% of findings.
- **Blind item labels** (`labeler.md`, `label.py`): Sonnet 5.5, isolated (no tools, no
  MCP, no CLAUDE.md, anonymised packs where the context names the company, opaque pack
  ids), never shown an outcome. Per item: claim type (11 classes), whether it is about
  the company itself, reliability, specificity, novelty, obscurity, relevance,
  direction, strength. Per pack: reliability, sufficiency, coverage, a forced direction.
  **Two full runs; they agree**: Spearman 0.90–0.97 on every scale, claim type 94%,
  direction 97%. About $16.

## Method (`analyze.py`)

A cell is a set of (print, sign) votes: items of one kind, or one judge's calls inside
one group of names. Statistic: mean of sign × move/priced. Significance: permutation,
shuffling realised moves across prints **within each day**, 1,000–2,000 times, keeping
a print's items together. A family-wise p reads each |z| against the permutation maximum
over all cells; Benjamini–Hochberg q beside it. Discovery used every day except the
judge-lab TEST days; the four contrasts in `CONFIRM-PREREG.md` were committed (`1174eb1`)
before those 20 names were opened (`confirm.py`, logged in `../judge-lab/TEST-LOG.md`).
Every table below is the full 158 after unsealing unless marked.

## 1. Source reliability: an inverted U, not "unreliable wins"

Item level, labeler direction, quintiles of reliability (`results/deep-unsealed.json`):

| reliability | items | right | mean signed move/priced |
|---|---|---|---|
| Q1 (< 62.5) | 124 | 46% | −0.44 |
| Q2 | 123 | 47% | −0.13 |
| **Q3 (70–76.5)** | **162** | **63%** | **+0.37** |
| Q4 | 105 | 52% | +0.15 |
| Q5 (> 80) | 170 | 51% | +0.01 |

The middle beats both tails (55% against 49%, p 0.17 as one pre-specifiable contrast).
A reading that fits: the most reliable items are mostly primary filings everybody reads,
so they are priced; the least reliable are mostly wrong. Obscurity has the same shape and
its top quintile is the worst cell of all (41% right). The user's hypothesis in its item
form ("unreliable and new/obscure scores") fails everywhere:

| cell | items | right | mean | z |
|---|---|---|---|---|
| low reliability | 223 | 44.8% | −0.35 | −1.53 |
| low reliability and high novelty | 104 | 42.3% | −0.42 | −1.41 |
| low reliability and high obscurity | 96 | 39.6% | −0.59 | −1.81 |
| low reliability, not about the company | 17 | 41% | −1.38 | −2.60 (discovery) |
| mid reliability | 218 | 61.0% | +0.32 | +2.18 |
| mid reliability and mid novelty | 75 | 62.7% | +0.48 | +2.70 (best of 132; family-wise p 0.51) |

## 2. Source type: the company's own word, in names nobody prices

| claim type / source | items | right | mean | z |
|---|---|---|---|---|
| newswire (company press releases) | 66 | 65.2% | +0.49 | +1.83 |
| the company's own disclosure | 149 | 53.7% | +0.30 | +1.82 |
| retail-finance portals | 82 | 57.3% | +0.24 | +1.08 |
| SEC filings (any filer) | 252 | 53.2% | +0.01 | 0.00 |
| positioning or price | 35 | 48.6% | −0.22 | −1.47 |
| macro or industry | 43 | 48.8% | −0.81 | −1.47 |

Split by whether an option chain priced the move (`results/items_by_anchor.json`,
discovery): **in option-priced names no evidence type carries the sign** (every cell
|z| < 1). In names without an option anchor the company's own disclosure is right 63%
(+0.52), mid-reliability items 65% (+0.54, z 2.52), while positioning (36%, z −2.03),
macro (z −2.41) and not-about-the-company items (z −1.77) point the wrong way. On the
sealed test days the focal-disclosure cell held (9 items, +0.97) and low reliability
stayed negative (27 items, −0.43).

Per-name votes of one kind of evidence (`D_votes`) rank nothing significantly: the best
are the company's-own-disclosure vote (z 1.67) and the newswire vote (62% right, z 1.60).

## 3. "Low sufficiency" is a kind of name

Pack sufficiency tracks the name, not the sources (Spearman): turnover +0.59, thinly
covered −0.51, a consensus bar in the pack +0.41, implied move −0.30. The source mix
barely differs between quadrants (SEC 42–46% in three of four). The exception is the
worst quadrant, **sufficient but unreliable**: big names (median turnover $51m) whose
evidence leans on retail-finance portals (24% of items against 13–15%) and trade press.
The judges together got 41% of signs there.

| group (all 158) | judges right, median4 | move / priced |
|---|---|---|
| no option anchor, low sufficiency | 34/50 (68%) | 1.99 |
| no option anchor, high sufficiency | 9/17 | 1.53 |
| option anchor, low sufficiency | 9/19 | 0.81 |
| option anchor, high sufficiency | 30/58 (52%) | 0.78 |

**Each judge's top-20% book inside the low-sufficiency half beats the one inside the
high half, for all seven judges** (net of judge-lab's cost table): median4 9/11 +8.8%
against +1.2%, Sonnet 10/11 +9.4% against +3.7%, Opus 5 +8.2% against +2.8%, Opus 5.5
+8.6% against −2.7%, Fable +5.1% against +1.6%, live +3.4% against +0.9%. Dropping any
one day keeps the median4 figure between +6.2% and +10.4% (discovery).

**Why not to believe it yet:**

- **The sealed days reversed it.** C1 (low-sufficiency names right more often) flipped:
  4/7 against 8/11. C2 (no anchor right more often) was flat: 6/9 against 6/9.
- **Seven judges are not seven tests.** They judge the same evidence; the agreement
  shows the effect is not one model's quirk, not that it is real.
- **It is mostly drift.** 58% of anchor-less names fell (shorting all of them is right
  42/72). The judges call them down 61–71% of the time. When they call against the
  majority they are right 14/24.
- **Capacity.** Low-sufficiency names have median turnover $0.71m; 22 of 74 sit under
  the $200k floor, 24 clear $5m, 19 have an option chain.
- **Significance.** One-sided permutation p for the median4 book gap: 0.075; for the
  hit-rate gaps 0.13–0.22 (rated judge 0.036). Chosen after the operator's observation,
  so these are exploratory.

## What to do with it

1. **Do not add a reliability or sufficiency filter to the panel.** Neither confirmed,
   and "low reliability" points the wrong way.
2. **Worth carrying forward as a hypothesis, not a rule:** in names without an option
   chain, weight the company's own disclosures (press releases, its filings) and
   discount macro, peer read-across and positioning items. That is two held sign
   checks on few items, so log it forward, alongside the anchor flag the baseline
   already carries.
3. **Measure judges by anchor group.** In option-priced names the judges are at or below
   a coin flip on every slice here. If that holds forward, the panel's effort there is
   cost without return.
4. **The labeler is cheap and stable** ($16, agreement 0.90+), so its item labels can be
   added to every forward run as a diagnostic beside the key, the same way
   `edge_context.py` labels names, never read by the scorer or the book.

## Files

| file | what |
|---|---|
| `build.py` | the dataset: `data/events.json`, `data/items.json`, `data/packs.json` |
| `data/domain_classes_llm.json` | domain to source class |
| `labeler.md`, `label.py`, `labels/run0/`, `labels/run1/` | the blind labeler and its two runs |
| `analyze.py` | families A–G: quadrants per judge, name types, item cells, votes, books, robustness |
| `deep.py` | what sufficiency tracks, strata, quadrant mix, dose-response, judges together |
| `mechanism.py` | turnover terciles, option anchor, move vs priced, books per half, capacity |
| `checks.py` | drift, permutation contrasts, by hunter model, leave-one-day-out |
| `CONFIRM-PREREG.md`, `confirm.py` | the four contrasts and the one unseal |
| `results/` | every output; `*-unsealed.json` is the full 158 |

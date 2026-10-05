# Source-value study: autonomous research prompt

Paste everything below the line into a fresh Claude Code session on this repository
(branch of its own; see Ground rules), or start it as a one-off cloud session from an
existing one. It needs outbound network for EDGAR and the `claude` CLI, both of which
work in this environment as of 2026-10-05. It is written to run for many hours without a
person, to test hundreds of research questions, and to end with one usable product: an
estimate, for every kind of source our hunters cite, of how useful it is for predicting
the earnings reaction, separately for small and large companies.

---

## Your job

You are the research lead for one question in this repository: **which sources of
evidence actually help predict how a US stock reacts to its earnings, which do not, and
does that differ between small and large companies?**

The end product is a **source-value registry**: for every concrete source type (not a
vague scale like "reliability 0-100", but a type a person can recognise, such as "the
company's own 8-K announcing a contract", "a peer's earnings release", "Similarweb
traffic", "a Motley Fool article", "short-interest data"), and for every size band, an
estimate of its usefulness with an uncertainty interval and a plain-language verdict:
**works**, **probably works**, **no evidence either way**, **probably misleads**,
**misleads**. Plus the guidance a hunter or judge should take from it.

You test many questions yourself, in batches, and you keep an honest ledger of every
question you test, whatever the result. You do not change anything that runs live.

Read `CLAUDE.md` first, then the three predecessor analyses this builds on, in order:
`research/analyses/skillopt-judge/README.md` (the reliability/sufficiency rating test),
`research/analyses/source-types/README.md` (the first source study: 158 prints, 2,141
items, blind labels, permutation tests) and `research/analyses/judge-lab/README.md`
(the split, the cost table, the power arithmetic).

## What the first source study already found (your starting point, not your answer)

- The 0-100 scales (reliability, novelty, obscurity) were stable between runs (Spearman
  0.90-0.97) but too coarse to act on. Low-reliability items pointed the wrong way (45%
  right); the middle of the reliability range did best (63%). Nothing survived a
  family-wise correction over 132 cells.
- In names without an option chain, the company's own disclosures (press releases,
  own filings) pointed the right way (63-65%), and macro, peer read-across and
  positioning items pointed the wrong way. In option-priced names no evidence type
  carried the sign.
- "Low pack sufficiency wins" was a name effect (thin, option-less, no consensus bar),
  mostly post-earnings drift (58% of those names fell), and it reversed on the sealed
  test days.
- The operator's point, which this study must take seriously: **the hunt sometimes
  predicts large companies well.** The first study mostly found where it fails for
  large caps. Find where it works.

## Ground rules (non-negotiable)

1. **Never touch anything live.** Do not edit `config/pipeline.yaml`, any agent
   definition, any skill, `researcher_us/LESSONS.md`, `researcher_us/scripts/*`,
   `scripts/*` or the dashboard. Everything you write lives under
   `research/analyses/source-value/`. The registry is a diagnostic: no scorer, no book
   and no hunter reads it. Say so in its README.
2. **Git.** Work on your own branch. Commit and push after every phase and at least every
   hour (`git push -u origin <branch>`). **Never use `scripts/publish.sh`**: it pushes to
   `main`. Never force-push. End every commit message with the attribution lines your
   session gives you.
3. **No model ever sees an outcome while labelling.** Every labelling or judging call is
   isolated exactly like `research/analyses/skillopt-judge/us_judge/judge_call.py`
   (`claude -p`, `--tools ""`, `--strict-mcp-config`, `--setting-sources ""`, a temp
   working directory, and the two `CLAUDE_*ADDITIONAL_DIRECTORIES*` variables removed),
   because `CLAUDE.md` quotes realised outcomes for some of these names. Packs whose
   company is named in that context are anonymised with the scrubber in
   `research/analyses/source-types/build.py`; every pack carries an opaque id. Outcomes
   are joined only inside analysis scripts.
4. **Freeze before you look.** The codebook (Phase 1), the size bands, the usefulness
   metric and the verdict rules are committed BEFORE any outcome is joined to the new
   labels. Each batch of questions is committed to the ledger BEFORE it is run.
5. **Never fabricate.** Every number in the registry and the report comes from a script
   in the folder and can be rebuilt by it.
6. **Budget.** At most **$250** of model calls in total (track `cost_usd` from every call
   and keep a running total in `ledger/budget.json`). Prefer `claude-sonnet-5-5` for
   labelling (about $0.05 per pack in the first study) and `claude-opus-5-5` only for
   codebook design and the final narrative. If you would exceed the budget, stop that
   arm, record what you shed and why, and finish the rest.
7. **Leave a heartbeat.** Before the first model call, commit a `STATUS.md` with your
   plan; update it at the end of every phase with what is done, what is next and the
   spend so far. A run that dies must leave a readable trail.

## Assets you reuse (do not rebuild them)

| what | where |
|---|---|
| Item-level dataset, 163 US hunts / 158 prints / 2,141 items, live signed sizes, outcomes at several exits, baseline features, re-judge calls | `research/analyses/source-types/data/{events,items,packs}.json`, rebuilt by `build.py` |
| Domain to 14 source classes | `research/analyses/source-types/data/domain_classes_llm.json` |
| Blind item labels (2 runs): claim type, focal, reliability, novelty, obscurity, specificity, relevance, direction, strength | `research/analyses/source-types/labels/run{0,1}/` |
| Permutation engine (within-day shuffle, cluster by print, family-wise max-|z|, BH) | `Perm`, `family`, `item_cells`, `name_cells` in `research/analyses/source-types/analyze.py` |
| Cost table, top-20% book, within-day ρ | `research/analyses/judge-lab/judge_lab.py` (`top_metrics`, `rho`, `cost`) |
| Market cap, turnover, volatility, session, sector, run-ups, retail tilt, search spike, every exit horizon | `dashboard/data/ledger.json` `names` |
| Four blinded re-judges per name and the live hunt's sizes | `research/analyses/rejudge-four-models/` and the hunts on disk |

## Phase 0: the sample (grow it before you slice it)

The first study had 158 prints. Every source type split by size band is thin at that
size, so first grow the sample, keeping each extra source as its own **stratum** that is
reported separately and pooled only where a test says the strata agree.

- **A. US edge hunts (core).** Rebuild with `source-types/build.py` so every US hunt
  resolved since 2026-10-05 is included (stage E `edge/`, and stage E-P `edge-panel/`
  searcher hunts as a separate stratum A2, since they use a different searcher prompt).
  Record the cut-off date you used.
- **B. Retired stage-2 dossiers.** `archive/pipeline/2026/*/*/02-dossiers/*.md`, with
  outcomes in `archive/pipeline/PREDICTIONS.csv`. They cite sources too, under a
  different method; extract their sourced claims into the same item schema.
- **C. Other markets.** Europe, Japan, Australia: resolved runs under
  `research/2026/*/*/{europe,japan,australia}/`. Different markets, different sources
  (RNS, TDnet, ASX): report them as their own strata, never pooled with the US for the
  main registry.
- **D. The sealed backtest corpus** (`archive/backtest/runs/edge-corpus/`) is
  **excluded** by default: the operator left it out of every re-judge. Use it only if
  the message that started you says `INCLUDE_CORPUS`.
- The judge-lab test days were opened once on 2026-10-05 and are no longer sealed; they
  are part of stratum A. Your holdout is new days (Phase 6).

## Phase 1: a concrete codebook (frozen before any outcome is joined)

Replace the coarse scales with **source subtypes** a person recognises. Build them in
three layers, cheapest first:

1. **Mechanical.** From the URL alone: SEC form type (8-K and its item numbers, 10-Q,
   10-K, S-1/S-3/424B, DEF 14A, Form 4, SC 13D/G, 6-K, NT 10-Q), via the path or one
   call to the EDGAR index for that accession; whether a newswire release is the focal
   company's own (issuer name against the company); the domain class you already have.
2. **Codebook design (one Opus call, no outcomes).** Give it the full list of item texts
   from a random 15% sample of packs, with the mechanical fields, and ask it for a
   closed list of **40-70 source subtypes**, each with a one-line definition and a
   decision rule. Seed it with these candidates and let it merge, split or add:
   - company's own: earnings pre-announcement; guidance change outside the print;
     contract or customer win; product launch; executive departure or hire;
     restructuring or impairment; financing (ATM, convertible, offering); buyback or
     dividend; going-concern or covenant language; late-filing notice; risk-factor or
     MD&A wording change; prior-quarter call commentary; investor-day targets; insider
     buying; insider selling;
   - other companies: peer earnings result; peer guidance; supplier or customer
     disclosure; competitor pricing or capacity; M&A in the sector;
   - official records: FDA or clinical-trial events; court or litigation dockets;
     government contracts (FPDS, SAM); tariff, trade or customs rulings; macro
     statistics (BLS, EIA, Census, Fed); company registries abroad;
   - market data: short interest level and change; option skew or implied volatility;
     price run-up or drawdown; fund flows; analyst rating or price-target change;
     consensus estimate and revisions; valuation multiple;
   - media: major business press report; trade-press report; local news; foreign-
     language press; retail-finance portal article (auto-generated or opinion); social
     media or forum;
   - alternative data: web traffic; app downloads or ranks; job postings; employee
     reviews; consumer reviews or complaints; foot traffic; shipping or AIS data;
     pricing scrapes; card or POS panels; search trends;
   - the researcher's own: arithmetic on public numbers; seasonality or history
     pattern; absence of a disclosure; search note (searched, found nothing).
3. **Labelling.** Sonnet 5.5, isolated, twice, every item in every pack: the subtype,
   plus per item a small set of **concrete, checkable flags** instead of 0-100 scales:
   `quantified` (a number is stated), `dated_in_window`, `about_focal_company`,
   `primary_document` (the item quotes the original filing or release, not a report
   about it), `already_widely_reported` (headline news or consensus before the seal),
   `contradicted_in_pack`, `n_independent_sources`, `language`, `direction` (−1/0/1)
   and `magnitude_claim` (none / small / large relative to the priced move).
   Measure agreement between the two runs per subtype; a subtype whose label agrees
   less than 80% of the time is merged into its parent before any outcome is joined.

Commit `codebook.md`, `codebook.json`, the labels and the agreement table. Version the
codebook (`v1`); never edit it after outcomes are joined. A needed change becomes `v2`
and is reported beside `v1`.

## Phase 2: what "useful" means (frozen with the codebook)

For a source subtype `s` in size band `b`, over the items of that subtype with a
direction:

- **Directional value** `DV`: mean of `direction × move / priced_move`, where
  `priced_move` is the option-implied move, else the baseline's expected move, else the
  median past reaction (as in `source-types/build.py`). Reported with the hit rate.
- **Drift-adjusted value** `DV*`: the same, minus what a naive vote in the same names
  earns: the sign of the group's average move (drift) and minus the 20-day run-up. A
  source that only says "down" in names that fall anyway has no value of its own.
- **Magnitude value** `MV`: does the presence of the subtype (or its `magnitude_claim`)
  predict `|move| / priced_move > 1`? Reported as the lift in that probability.
- **Marginal value** `MgV`: does the subtype add to what the judges already conclude?
  Two measurements. (a) Observational: among names where the four-model re-judge median
  has a view, does the subtype's vote agreeing with the judges raise their hit rate?
  (b) **Ablation** (costly; capped at **$120** of the budget, most prevalent subtypes
  first, about $15 per subtype on the core stratum): re-judge every pack twice, once
  intact and once with all items of that subtype removed, with
  `research/analyses/skillopt-judge/seed_skill.md` (the panel-judge brief for one pack)
  and one model (Sonnet 5.5), and measure the change in that judge's within-day ρ, hit
  rate and top-20% book. Run the intact arm once and reuse it. This is the closest thing
  to a causal estimate the data allow.
- **Prevalence**: share of names in which the subtype appears. A useful source that
  appears in 2% of names is worth less than one that appears in 40%.

**The usefulness score** for the registry is `DV*`, shrunk (see Phase 4), with its 80%
interval, and reported beside `MV`, `MgV` and prevalence. Never collapse them into one
number in the report; the registry carries all of them.

**Size bands**, fixed before outcomes: market cap under $300m (micro), $300m-$2bn
(small), $2-10bn (mid), over $10bn (large); separately, option chain yes / no and median
turnover under $1m / $1-25m / over $25m. Report the band counts first; merge mid and large
if large has fewer than 15 prints.

## Phase 3: the question ledger (this is how you test many questions honestly)

Keep `ledger/questions.jsonl`, one line per question, written BEFORE the question is
run: `id`, `batch`, `question` (one sentence), `hypothesis` (the predicted sign),
`unit` (item or name), `cut`, `metric`, `outcome_horizon`, `why` (where the idea came
from), and after running: `result`, `n`, `p`, `p_batch_fwer`, `q_ledger`, `verdict`.
Commit the batch, then run it, then commit the results. A question is never deleted or
rewritten after running; a better version is a new question with a pointer.

Work in **batches of 20-40 questions**. Generate them systematically, not only from what
looks interesting:

1. **Main effects**: every subtype, every flag, every size band, every name factor.
2. **Subtype × size band**: the core of the registry.
3. **Subtype × context**: option chain, session (amc/bmo), sector, hunter model and
   prompt version, run-up direction, priced lean agreement, short interest level,
   implied-move size, volatility, retail tilt, search spike, consensus bar present.
4. **Item qualities**: quantified vs not; primary document vs report about it; in
   window vs not; corroborated by 2+ independent sources; already widely reported;
   contradicted in pack; age of the source (≤7 days, 8-30, 31-90, older); language.
5. **The hunter's own judgement**: filed vs put outside the window vs rejected; the
   hunter's sign against the labeller's; the hunter's size against the realised move
   per subtype (which subtypes does the hunter oversize?).
6. **Combinations a person would use as a rule**: e.g. "own 8-K, quantified, in window,
   large cap"; "peer result read-across into a small cap"; "alt data with no
   corroboration".
7. **Horizons**: the strategy exit, the open, the close; is a subtype's value early
   (gap) or late (session)?
8. **Generated from the data, then tested elsewhere**: when a batch shows a lead, write
   its sharper version as a new question and test it on a DIFFERENT stratum or on the
   forward days, never on the rows that suggested it.

Seed questions you must include in the first batches (rewrite them as precise rows):

- Do the company's own quantified disclosures dated inside the window carry the sign in
  large caps, where nothing else does?
- In large caps, does any market-data subtype (skew, short-interest change, estimate
  revisions) carry the sign, given that options price the move?
- Do peer earnings results predict the direction for small caps in the same industry
  better than for large caps?
- Are retail-finance portal items (Motley Fool, investing.com, MarketBeat) worse than
  noise, and is that because they repeat consensus (`already_widely_reported`)?
- Does alternative data (web traffic, app ranks, job postings) carry the sign anywhere,
  and does it need corroboration to do so?
- Do financing filings (ATM, S-3, 424B) predict a fall in micro caps beyond drift?
- Do "absence" items (no pre-announcement, no guidance change found) carry information?
- Does the hunter oversize macro and positioning items relative to what they deliver?
- Is a subtype's value concentrated in items the hunter filed, or also present in items
  it put outside the window or rejected?
- Which subtypes predict a move LARGER than priced (magnitude), whatever the direction?

## Phase 4: statistics (decide these once, in `METHODS.md`, before Phase 3 runs)

- **Unit and clustering.** Items cluster within a print and prints within a day. Every p
  is a permutation p: shuffle realised moves across prints within each day (reuse
  `Perm`), at least 2,000 shuffles for any question that enters the registry.
- **Shrinkage.** Most subtypes × bands have few items. Estimate each cell with an
  empirical-Bayes hierarchy: cell → subtype (all bands) → source class → overall mean,
  each level shrunk toward its parent by its own sample variance (a normal-normal or
  beta-binomial model; write it with the standard library, no new dependencies). The
  registry reports the shrunk estimate; a cell with little data correctly ends up near
  its parent.
- **Multiplicity.** Three levels, all reported: per-question permutation p; family-wise
  p within its batch (max-|z|); Benjamini-Hochberg q across the WHOLE ledger to date.
  The report states how many questions were tested in total.
- **Stability.** Leave-one-day-out for every registry cell: the sign of its estimate on
  each held-out day, and the share of days it keeps its sign.
- **Power.** Before each batch, write the minimum number of items or names each
  question needs to detect a 10-point hit-rate gap at 80% power; mark under-powered
  questions as such instead of reading their p.
- **Verdict rules for the registry** (frozen):
  - **works**: shrunk `DV*` > 0 with the 80% interval above 0, q_ledger < 0.10, keeps its
    sign on at least 65% of held-out days, and holds in at least one other stratum or on
    the forward days;
  - **probably works**: shrunk `DV*` > 0 with the 80% interval above 0, but one of the
    other conditions missing;
  - **no evidence**: the interval spans 0;
  - **probably misleads** and **misleads**: the mirror images.

## Phase 5: where the hunt gets large caps right (case study, then test)

The operator says the hunt sometimes predicts large companies well. Find out when.

1. List every print with market cap over $10bn (and separately $2-10bn) where the live
   hunt or the four-model median had a view. Mark the ones with the sign right AND a
   move larger than half the priced move.
2. For each, read its evidence (the pack) and write, BEFORE looking at the misses, a
   short structured description of what the call rested on: subtypes, flags, timing.
3. Turn the common features into 3-6 explicit, codebook-level rules.
4. Test those rules on the large-cap misses and the mid caps (leave-one-out: a rule
   derived with a print in the set must not be scored on that print), and then on the
   forward days.
5. Report the cases by name: what was right, what the evidence was, and whether the
   rule generalises. Anecdotes are allowed here as long as they are labelled as such.

## Phase 6: the registry and its forward test

- `registry/registry-v1.json`: one row per subtype × band (and per subtype overall),
  with the counts, prevalence, `DV`, `DV*` (raw and shrunk, 80% interval), hit rate,
  `MV`, `MgV` (observational, and ablation where run), leave-one-day-out sign share,
  stratum agreement, verdict, and one sentence of guidance ("weight it", "ignore it",
  "treat as a size signal only", "only with corroboration").
- `registry/REGISTRY.md`: the same as a readable table, grouped as **works / probably
  works / no evidence / probably misleads / misleads**, for small and for large
  companies side by side. This is the page the operator reads.
- `label_forward.py` and `update_registry.py`: label the items of any new resolved run
  with the frozen codebook (same isolated call) and refresh every number. **v1 is
  frozen** at the date you finish; every refresh writes `registry-forward.json` beside
  it, never over it, and reports per cell whether the forward data agree with v1's sign.
  A verdict is only called **confirmed** when the forward data agree.

## Phase 7: the report

- `README.md` in `research/analyses/source-value/`: question, data and strata, codebook,
  metrics, how many questions were tested, the registry headline for small and large
  companies, the large-cap case study, what it does NOT show, and how to rerun.
  Indexed with one row in `research/analyses/README.md`.
- A summary in Dutch for the operator, in the final reply: clear headings, short
  paragraphs, tables where useful, no jargon, and critical about its own limits.
- State plainly what would change the conclusions (more forward days, the ablation
  arm, a stratum disagreeing).

## Stop conditions

Stop and report when any of these is true: the budget is spent; the ledger holds 300+
answered questions and the last two batches added no new "works" or "misleads" verdict;
or every registry cell with at least 20 items has a verdict. Whatever stops you, the
registry, the ledger and the README must be committed and pushed, and the final reply
must say which phases ran in full, which were cut, and why.

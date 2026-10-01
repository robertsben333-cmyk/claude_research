# A judging approach built on the forecasting literature (2026-10-01)

The question stays narrow: given the evidence a hunter collected, which names belong in
the **top ~15%** we would trade, and on which side. This note sets out what the research
on AI forecasting says about that, what our own data already shows, and the approach that
follows from both.

## 1. What the literature says

| finding | source | what it means here |
|---|---|---|
| A retrieval + reasoning system nears the human crowd **only after aggregating** many forecasts (trimmed mean); single runs are worse | [Halawi et al. 2024, NeurIPS](https://arxiv.org/abs/2402.18563) | Do not trust one judge's run; aggregate |
| A median of **12 different LLMs** matches a crowd of 925 human forecasters; single models do not | [Schoenegger et al. 2024, Science Advances](https://www.science.org/doi/10.1126/sciadv.adp1528) | Model diversity is the cheap source of accuracy |
| Learned aggregators beat the mean, but their weights track **error diversity**, not individual accuracy; contamination reorders model rankings (ρ 0.53) | [Wisdom of LLM Crowds, 2026](https://arxiv.org/html/2607.18269) | Pick members for different errors; learned weights need far more data than we have |
| Multi-agent **debate adds nothing over majority voting**; the gain is the ensemble, not the argument | [Debate or Vote, NeurIPS 2025](https://arxiv.org/abs/2508.17536) | Skip debate/adversary designs; vote |
| Correlated pretraining makes majorities suppress a correct minority in ~1 in 4 split cases | [Minority Sentinel, 2026](https://arxiv.org/pdf/2606.29270) | Unanimity is a stronger gate than majority when members share evidence |
| **Stated confidence is overconfident**; agreement across samples predicts errors better (AUROC 0.78–0.86 vs 0.42–0.76) | [Xiong et al. 2023](https://arxiv.org/abs/2306.13063), [survey 2025](https://arxiv.org/html/2510.20460v1) | Take certainty from agreement, never from the judge's own number |
| **Pairwise** ranking beats pointwise scoring by >10% for LLM rankers | [Qin et al. 2024, PRP](https://aclanthology.org/2024.findings-naacl.97/) | If a day has more candidates than slots, compare them in pairs |
| Aggregated probabilities should be **extremized** when forecasters hold different information | [Baron et al. 2014](https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2015---two-reasons-to-make-aggregated-probability-forecasts_1.pdf), [Satopää et al. 2014](https://arxiv.org/html/1406.2148v5) | Only matters for sizing, not for which names make the top |
| Structured CoT over anonymised statements predicts earnings direction at ~60%, above analysts | [Kim, Muhn, Nikolaev 2024](https://arxiv.org/abs/2407.17866) | Realistic hit rates are ~60%, not 80% |
| LLM news scores predict the **initial** reaction very well (non-tradable) and the drift weakly, mostly in small caps; returns decay as adoption rises | [Lopez-Lira & Tang 2023](https://arxiv.org/abs/2304.07619) | Expect a small, fading edge, strongest in thin names |
| Base rates plus a competence gate beat either source alone | [Competence-gated pooling, 2026](https://arxiv.org/pdf/2609.12101) | Default to "no bet"; let the model override only where it has earned it |
| Backtests leak (dates, logic, retrieval) and overstate skill | [Paleka et al. 2025](https://openreview.net/forum?id=z85kARAoyD) | Our in-sample numbers are an upper bound; forward is the test |

## 2. What our data already shows (`ensemble.py`, no model cost)

187 development names, top 15% pooled within bucket, net of assumed cost:

| arm | all | US | ex-US |
|---|---|---|---|
| live `impact_sum` | 15/25 +1.6% | 10/17 +1.8% | 5/8 +1.1% |
| best single model, chosen afterwards (Sonnet 5.5) | 20/25 +6.9% | 13/17 +7.3% | 7/8 +6.0% |
| worst single model (Fable 5.1 US / Opus 5.5) | 17/25 +2.3% | 9/17 +0.5% | 7/8 +5.5% |
| **unanimous four, weakest size** | **20/25 +6.6%** | **12/17 +6.3%** | **8/8 +7.3%** |
| mean of four (scaled) | 19/25 +5.2% | 11/17 +4.5% | 8/8 +6.7% |
| learned logistic stack (leave-one-day-out) | 15/25 +0.7% | 9/17 +0.7% | 6/8 +0.9% |
| agent judges that learned from outcomes | 16–19/25 +0.9 to +2.8% | | |

Three things in that table match the literature exactly:

- **The ensemble matches the best single model without having to know which one it is.**
  Every single model is good in one region and mediocre in the other (Fable 5.1 is the
  best ex-US and the worst in the US); unanimity is near the top in both.
- **Learned aggregation and learned rules overfit** at this size: the stacked logit and
  the learned skill are the two worst arms. The literature's learned aggregators had
  thousands of questions.
- **Adding the live hunt to the ensemble makes it worse** (unanimous five: 17/25 +3.3%).
  The member that searched and sized under one prompt is the weakest judge of its own
  evidence.

## 3. The approach

**Separate search from judgement (already the design), and make the judgement an
ensemble with an agreement gate.**

1. **Hunt** as now: one hunter per name collects and files evidence.
2. **Judge** each name blind, from the pack, with **four different models**
   (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) under the shared hunter core. No debate, no
   adversary, no learned rules.
3. **Gate on unanimity.** A name is a candidate only if all four give the same nonzero
   sign. Its strength is the **weakest** of the four scaled sizes, so one enthusiastic
   judge cannot carry a name.
4. **Cut with one number.** In live use the top 15% is not available (it is a pooled,
   after-the-fact share), so the cut becomes a threshold `c` on that weakest size, set
   once on the development folds to give ~15% coverage. One parameter, not a model.
5. **Only if a day has more candidates than capital:** rank them with a pairwise judge
   ("which of these two is the surer trade, and why"), per the PRP result.
6. **Size** as now; extremizing would only matter if the four were turned into a
   probability for sizing, which is not the question here.

What it deliberately does not do: learn weights or rules from outcomes, ask a model how
sure it is, or let one model dominate.

## 4. How to test it without fooling ourselves

1. **Pre-register** the rule above (members, unanimity, weakest size, `c` from the
   development folds) in this file before anything forward is read.
2. **Run it forward**: every new US hunt pack goes to the four judges the evening it is
   sealed. About 4 × 20 names a day at ~4k tokens a pack. Nothing is traded on it.
3. **Two cheap development experiments first**, each one question:
   - *Framing diversity*: the same four models under a second framing (outside view
     first: the name's own reaction history and base rates, then the evidence). Does an
     8-member ensemble beat 4? The literature says diversity of error is what pays.
   - *Self-consistency*: Sonnet 5.5 three times on the same packs. Does within-model
     agreement add anything beyond cross-model agreement?
4. **Open the sealed test set once**, for unanimous-four and the live hunt only.

## 5. What this cannot fix

- All four judges read the **same evidence**; their errors are correlated through it.
  Unanimity measures agreement about the evidence, not independent information.
- Every subagent loads `CLAUDE.md`, which quotes results from these days. That favours
  no arm in particular but flatters all absolute levels.
- 25 picks per arm. A 5-point gap between two arms is about one standard error. The
  ensemble's advantage is **robustness across regions**, which is a structural argument
  the literature supports, more than its level, which is not established.
- Realistic expectations from the literature are ~60% direction, not 80%.

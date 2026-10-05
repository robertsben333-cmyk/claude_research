# SkillOpt on the US panel judge (2026-10-05)

Question: can Microsoft's [SkillOpt](https://github.com/microsoft/SkillOpt) (commit
`fa4ca18`, v0.2.0) improve the stage E-P judging skill if it is trained on resolved US
names? SkillOpt treats a skill document as the trainable state of a frozen model: the
model judges, an optimizer model reads the scored trajectories and proposes a few
bounded edits, and an edit stays only if a held-out gate set scores higher.

**Answer on this sample: no.** Two runs, two reward designs. Both runs ended on a skill
that scores higher on the gate set and **worse on the 25 names neither the optimizer nor
the gate ever saw**. Both found the same shortcut: stop giving a view. The second run's
end-of-epoch update also wrote five tickers from the training days into the skill and a
rule to follow the price lean. Nothing here goes near `config/panel-judge.md`.

## Set-up

| | |
|---|---|
| Target (the judge) | `claude-sonnet-5-5` through `claude -p`, **no tools, no MCP, no setting sources, no CLAUDE.md** (this repo's CLAUDE.md quotes outcomes for some of these names). Served model checked on every call |
| Optimizer | `claude-opus-5-5` through SkillOpt's `claude_chat` backend, effort high, the same two CLAUDE.md variables removed |
| Trainable skill | `seed_skill.md`: `config/panel-judge.md` rewritten for one pack per call. The hunter definition (with the shared core) and `researcher_us/LESSONS.md` are appended to every call as fixed reference and are not editable |
| Evidence | the blinded packs of `../rejudge-four-models/`, US only |
| Train (optimizer reads outcomes) | 60 names: the judge-lab TRAIN days LESSONS.md was written from (09-08 to 09-14) |
| Gate (only its mean score is used) | 49 names: every other judge-lab TRAIN day |
| Readout | 25 names: the judge-lab VALIDATION days |
| Sealed | the judge-lab TEST days (20 US names) are not written to `data/` at all and were not opened |
| Schedule | 2 epochs × 3 steps, batch 20, at most 3 edits a step (cosine to 1), slow update and meta skill on, slow update gated |
| Gate | SkillOpt's gate needs the candidate to be strictly higher. `run.py` adds a **margin**: 1.645 × the standard error of the gap between two runs of the SAME skill on the gate set (`evaluate.py --runs 2`) |

The reward per name is `r = (impact_sum / E) × (move / E)`, with `E` the move the baseline
priced. `soft = 0.5 + 0.5·tanh(r)`, and the gate compares mean soft (`us_judge/reward.py`).
That is the per-name version of what the panel earns: a large number with the right sign
on a name that moves more than was priced.

## Noise first

Two runs of the unchanged seed skill on the 49 gate names: mean soft 0.4640 and 0.4645,
the standard error of the gap is 0.0040, so the margin is **0.0066**. The same two runs
put the top-20% book at **−2.9% and +1.7%** per pick, with nothing changed. 88% of signs
agree between the runs; the sizes do not.

## Run 1: raw reward

| step | action | gate soft | names with a view (of 49) | ρ within day | top 20% net |
|---|---|---|---|---|---|
| seed (in-run) | | 0.4561 | 42 | −0.01 | −2.3% (3/8) |
| 1 | accept | 0.4635 | 41 | −0.08 | −2.1% |
| 2 | reject | 0.4684 | 36 | −0.04 | +4.6% |
| 3 | **accept, best** | 0.4920 | **17** | +0.04 | −0.1% |
| 4–6, slow update | reject | | | | |

Step 1 cleared the margin with a score below the seed's own two re-runs (0.4640 and
0.4645), so the margin did not stop the first noise acceptance. Re-scored at the end of
the run, the chosen skill's gate score was **0.4752**, not 0.4920: the winner's curse.

The accepted rules (`results/run1-raw-reward/best_skill.md`) read well and name no
company: keep the sign tied to the item's own mechanism, treat one-offs, amplifiers and
absences as size and not direction, give second-hand inference a quarter of the weight of
a company disclosure, and when nothing primary is left answer 50 and 0. What they did is
the last clause. On these gate days the seed was right on fewer than half its views
(17 of 42), so its average r is negative, and a name scored 0 earns exactly 0.5. Silence
pays, and the gate cannot tell silence from skill.

## Run 2: normalised reward

To close that, `USJUDGE_REWARD=normalised` divides each impact/priced by its RMS over the
whole evaluated set, so fewer views carry the same total weight. Margin from the same
seed runs: **0.0093**. Steps 1 to 5 were all rejected; step 6 was accepted at 0.4746 (one
rule: positioning is never proof that something is unpriced). Then the slow update was
accepted at 0.5089 **with a view on 6 of 49 names, 3 of them right**. The tanh bounds
each name's loss, so dropping the names a judge gets wrong still pays even after the
normalisation. The fix was not enough.

The slow update is a different SkillOpt prompt from the analyst prompts that carry
`us_judge/prompts/domain_rules.md`, so it never saw "no names, no direction". It wrote
**"These items called the sign wrong on FLWS, COO, NAVN, AENT and WLTH"** into the skill
and a rule that items against `priced_direction_lean` are zeroed. That is a list of
training outcomes and a direction rule learned from a few days, exactly the overfit the
judge lab's `learned` arm showed in round 1.

## Readout: the 25 names neither loop saw

| skill | names with a view | signs right | ρ within day | top 20% net (picks) | top-20% \|move\| / priced |
|---|---|---|---|---|---|
| seed, run A | 19 | 13 | +0.30 | **+8.9%** (4/4) | 1.56 |
| seed, run B | 19 | 12 | +0.30 | +8.9% (4/4) | 1.89 |
| seed, inside run 1 | 19 | 12 | +0.31 | +4.0% (3/4) | 1.45 |
| seed, inside run 2 | 20 | 13 | +0.35 | +8.9% (4/4) | 1.45 |
| run 1 best (step 3) | 8 | 6 | +0.23 | −0.3% (2/4) | 2.08 |
| run 1 last | 11 | 9 | +0.44 | −0.9% (2/4) | 2.10 |
| run 2 best = last | **4** | 2 | −0.06 | −2.2% (1/3) | 1.58 |

Four picks per row is noise, and so is the ρ on 25 names. The direction is what matters:
neither trained skill is better on the book the panel trades, and both have thrown away
most of the names the panel ranks. Run 1's last skill holds its sign on 9 of 11 views
and its top names move about twice what was priced. That is the only thing here worth
watching, and on eleven names it is an anecdote.

## What this says, and what it does not

- **SkillOpt runs on this repository and the plumbing is reusable.** `us_judge/` is a
  working SkillOpt environment. `evaluate.py` scores any skill the way judge-lab does,
  and `run.py` adds the margin gate without patching SkillOpt.
- **The method needs a reward that cannot be met by abstaining, and a gate set large
  enough to rank.** A per-name reward on a ranking task is either gameable (run 1) or,
  once bounded, still gameable (run 2). A gate on a set-level rank metric (within-day ρ or
  the top-20% book) would close it. On 49 names that metric is the noise shown above,
  so it would accept or reject at random.
- **Every SkillOpt prompt needs the domain rules, not only the analyst prompts.** The
  slow update and meta skill have their own prompts. A run that keeps the slow update
  must override those too, or turn it off.
- **The loop is cheap; the evidence is not.** About $59 of judge calls over 1,426 calls,
  plus the optimizer (about 175k completion tokens on Opus; SkillOpt's tracker does not
  report prompt tokens for this backend). The bottleneck is the same as in judge-lab:
  about 150 resolved US names, where telling a +3-point edge from zero takes about 77 top
  picks.
- **What would make a re-run worth doing**: several hundred resolved US names under one
  prompt version, a gate on top-20% net with a significance margin, the slow update off
  or given the domain rules, and the judge-lab test set opened once at the end.

Not shown: anything about Opus 5, Opus 5.5 or Fable as the target, other regions, or the
live panel. The readout days are the judge-lab validation days, which other judge-lab
arms have been scored on, so they are clean for this loop but not virgin.

## Files

| file | what |
|---|---|
| `prepare.py` | builds `data/{train,val,test}/items.json` from judge-lab's frozen split (gitignored; rebuild with this) |
| `seed_skill.md` | the starting skill |
| `us_judge/` | the SkillOpt environment: `adapter.py`, `judge_call.py` (isolated `claude -p`), `reward.py`, `prompts/domain_rules.md` |
| `config.yaml`, `run.py` | the training config and the runner (margin gate, env registration) |
| `evaluate.py` | runs a skill n times over a split and scores it; `--runs 2` gives the noise margin |
| `archive_run.py` | copies a SkillOpt output dir into `results/` without packs or transcripts |
| `results/seed-{val,test}.json` | the seed's noise and readout runs |
| `results/run1-raw-reward/`, `results/run2-normalised-reward/` | every skill version, step records, patches, and every judgement with its reward |

Rerun: `pip install -e "<SkillOpt checkout>[claude]"` in a venv, then
`python3 prepare.py`, `python3 evaluate.py --skillopt-dir <checkout> --skill seed_skill.md --split val --runs 2 --tag seed`,
and `python3 run.py --skillopt-dir <checkout> --out <dir> --margin <from the noise run>`
(prefix `USJUDGE_REWARD=normalised` for run 2).

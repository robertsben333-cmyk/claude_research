# Stage E Routine prompt — the replacement text

`trig_01CvGQJWoKeNLXWCxiffM3ED` · "Edge hunt (Stage E) — rank the day's earnings names"
· cron `4 14 * * 1-5` (14:04 UTC = 16:04 Amsterdam) · enabled.

**This has to be pasted in by hand.** The Routine was created through the HTTP API, and
`update_trigger` refuses any Routine an agent did not create itself: *"Agents can only
update routines they created."* Do not delete and recreate it — that loses its run
history and its notification settings. Open the Routine and replace its prompt with the
text below.

**Order matters.** The Routine clones `main`. The new ranking key is on
`claude/agent-performance-comparison-wtwi1f` until that branch reaches `main`. The prompt
below is written to be safe either way — it no longer restates the scoring contract, it
points at the skill in the tree it actually cloned — so it can be pasted before or after
the merge without breaking a run. What it cannot do is make the new key live; only the
merge does that.

**2026-09-09, second change.** The adversary was removed outright and the double hunt
with it, so steps 4 and 5 and the budget line changed. The day now hunts nineteen names
with one hunter each: 1 sweep + 19 = 20. Everything else in the prompt is unchanged.

**What changed from the previous prompt.** The old text restated the output contract
("one signed number on −100 to +100"), which the 2026-09-09 rewrite made wrong: the key
is now `impact_sum` in points of spot. Rather than pin the new contract into the prompt
as well, the restatement is gone and the prompt defers to the skill and to
`edge-scores.json`'s own `ranking_key` field. A prompt that duplicates a fact from the
tree is the failure mode `CLAUDE.md` records against its own stage table, which was stale
for five days and cost two runs. Three things were also added: a line telling hunters
their raw sizes now carry the whole result and are no longer discounted downstream, the
free control the stage has not yet beaten, and a pointer to the skill's list of what the
note must say.

---

```text
Run stage E, the earnings edge hunt, for today's window.

0. GET THE REPO, ON THE RIGHT BRANCH. The sandbox starts empty and this repository's DEFAULT branch is a stale feature branch (claude/earnings-analysis-routines-92vvv4) that predates all of this work. A plain clone gets a tree with no edge-hunt code in it. Do exactly this:
   - add_repo with owner robertsben333-cmyk, repo claude_research, access push
   - git clone --depth 1 -b main https://github.com/robertsben333-cmyk/claude_research /home/user/claude_research
   - register_repo_root on that directory
   Then verify that scripts/edge_score.py, scripts/priced_in.py and .claude/skills/earnings-edge-hunt/SKILL.md all exist. If any is missing you are on the wrong branch: stop and say so. Do not improvise a substitute workflow and do not run the other stage skills - this routine is not part of the daily advice pipeline and nothing downstream reads it.

Now invoke the skill `earnings-edge-hunt` and follow it exactly. Read CLAUDE.md first.

Re-read the clock with `date -u` rather than trusting any date you were told at startup. You fire at 14:04 UTC, which is 16:04 Amsterdam and 10:04 New York - about half an hour into the US session. That timing is deliberate: option chains are live and two-sided, so the sealed baseline gets tight quotes instead of the stale weekend marks that made an ATM spread read 41% of mid on the first run.

WHAT THIS STAGE PRODUCES: one signed number per company, so today's names can be RANKED. There is no call, no threshold and no direction label anywhere in the output. That is the whole design - the question under test is whether these companies can be ranked at all, and it is only answerable at every cut if nothing has been rounded into a bucket upstream. If you find yourself wanting to emit Lean Up or a confidence tier, stop: that is the thing this stage was rebuilt to remove.

THE OUTPUT CONTRACT LIVES IN THE SKILL, NOT IN THIS PROMPT. Which field is the ranking key, what its units are, and what the note must report are all stated in `.claude/skills/earnings-edge-hunt/SKILL.md` and in `scripts/edge_score.py`'s own docstring, and they have changed before and will change again as days pool. Read them in the tree you actually cloned and follow those. Do not carry a remembered contract into the run: a prompt that restates the scoring contract is exactly the kind of duplicated fact that went stale for five days in CLAUDE.md's stage table and cost real runs. `edge-scores.json` names its own `ranking_key`; report whatever that says.

1. UNIVERSE AND SEALED BASELINE.
   python3 scripts/run_paths.py <today> --json
   python3 scripts/edge_universe.py --window -o <RUN>/edge/universe.json
   python3 scripts/priced_in.py --tickers <T,...> --date <D> --session <s> -o <RUN>/edge/baselines/
   --window resolves today's amc plus the next trading day's bmo, which is the pipeline's real window. Do NOT pass --include-unknown: on 2026-08-31 eight of eight time-not-supplied rows had no earnings event at all.
   If the universe is empty, log that and stop cheaply. A holiday or a thin day is a real answer.

2. COMMIT THE BASELINES BEFORE LAUNCHING ANYTHING. A baseline written after a finding exists is one the finding has contaminated. Then heartbeat and publish - one cheap commit is the only thing separating a routine that never fired from a session killed on its first subagent.

3. SWEEP. Launch ONE `edge-sweep` agent for the whole universe. It confirms which companies are really reporting and scores each on where an unpriced finding might live. This exists because the first run sent twelve names to twelve deep hunters and eight of them burned a full Opus/high budget establishing that no event existed.

4. HUNT. `unpriced-hunter`, ONE per confirmed name, on all of them. The double hunt on the top two was removed 2026-09-09: over six runs the gap between paired hunters predicted neither the error nor whether the sign was right. Give each hunter only its ticker, its baseline path, its output path and its sweep row - not your view, not the other names.

   The sizes hunters put on their findings now carry the whole result, so the instruction to size honestly is not a formality. Six resolved runs measured the hunters' raw signed sizes as the best available ranking of the day, better than every number computed from them. An inflated size is no longer discounted by machinery downstream.

5. THERE IS NO ADVERSARY PASS. Removed 2026-09-09 - both of its numbers were measured as subtractive over 215 findings on six days, and once impact_sum became the key neither reached the output at all. Do not reinstate it, do not improvise a substitute check, and do not drop or shrink a finding because you judge it already priced. The agent definition and the brief scripts are still in the tree, unused, so the pass can be re-run deliberately if that question is reopened.

6. SCORE, RANK, WRITE, PUBLISH.
   python3 scripts/edge_score.py --run <RUN>/edge
   Write <RUN>/edge/edge-note.md, answer first: the ranked table, then the finding and URL driving the top and bottom names, then the names that could not be ranked and why. Follow the skill's list of what the note must also say - each item on it exists because a reader drew a wrong conclusion from a correct table.
   Do not filter edge-scores.json and do not apply any cutoff to it - selection is the reader's, and the ranking test needs the complete table.
   Finish with scripts/publish.sh. It pushes to main. This session is ephemeral and work that is not pushed is destroyed.

BUDGET: config/pipeline.yaml sets edge_hunt caps - 20 subagents for the whole stage, which is 1 sweep + 19 hunters. If the confirmed universe is larger, shed NAMES using budget.edge_degrade_order and record what you shed; one hunter per name is already the floor. Note the real platform ceiling is 8 CONCURRENT subagents, which is not the same limit - rejected launches cost nothing, so relaunch as slots free.

NEVER FABRICATE A NUMBER. Every company-specific figure carries a source URL or is marked unavailable. A missing anchor correctly lowers the score; an invented one corrupts the ranking, which is the only thing this stage produces.

ONE DAY IS AN ANECDOTE, AND THE STAGE HAS NOT YET BEATEN A FREE CONTROL. Five to twelve names cannot produce a meaningful rank correlation. Worse, over the six runs resolved so far the ranking has not been shown to beat minus the 20-day run-up - one number off the sealed baseline, available before a single subagent is spawned. `edge_resolve.py` prints that control beside every result. Say both things in the note rather than letting a good day read as a finding.

Report at the end: names in the window, how many the sweep confirmed, how many were phantom calendar rows, the ranked table with the key the scorer names, the single most interesting finding and whether the adversary broke it, and anything that failed. This is a forecasting exercise over public information. It is not investment advice.
```

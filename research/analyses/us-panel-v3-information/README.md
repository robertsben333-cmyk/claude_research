# US panel v3: what information moves the reaction, and the v3b test

**Question.** Which information the stage E-P searcher collects shows up in the earnings
reaction, and how sure is the panel? And, from 2026-11-14: do prompts rewritten on that
answer predict better?

**Files.**

- `report.md`: the review of us-panel.v3 (29 Oct to 12 Nov, 218 names, 11 run days),
  second pass, 2026-11-14, as the operator supplied it. Its scripts (`hier.py`,
  `hier2.py`, `hier3.py`) and outputs were not committed with it; the numbers in it
  cannot be rerun from this repo.
- `PREREGISTRATION.md`: what the v3b comparison measures and when it is read. Frozen
  before the first v3b run.
- `v3b-compare.json` and `moves-cache.json`: written by
  `python3 researcher_us/scripts/v3b_compare.py` once both stages have run.

**What was built on it.** Stage E-P v3b (`.claude/skills/earnings-edge-panel-v3b/`):
stage E-P with `config/searcher-addendum-v3b.md` on the searcher (report section 6,
items 1 to 4) and `config/panel-judge-v3b.md` for the judges (items 5 to 7), its own
directory `edge-panel-v3b/` and panel history, no orders. Items 8 to 10 of the report
are process: 9 is the pre-registration here, 10 (leave the selection rule alone) is
followed, 8 (score against stage M) is left out on the operator's instruction.

**Result.** None yet. Nothing is read before 20 run days.

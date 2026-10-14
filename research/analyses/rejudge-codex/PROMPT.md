# One Codex task per model: the whole blind re-judge in one run

Open a Codex task on this repository (branch `main`, or the branch this folder is on),
pick the model, keep internet access OFF, and paste the block below. Change only the
first line: `MODEL: sol61` for GPT-6.1 Sol, `MODEL: astra` for GPT-6 Astra. A second
model is a second task with its own label. If a task stops before the end, start a new
task with the same block: it picks up where the last one stopped.

```text
MODEL: sol61

You are judging earnings research that was collected before the outcome existed. This is
an experiment and nothing you write is traded. Four other models judged the same evidence
independently; you never see their verdicts and must not guess them.

=== WHAT YOU MAY OPEN, AND NOTHING ELSE ===
The base folder is research/analyses/rejudge-codex/ (call it B). You may:
- read B/PROMPT.md, B/AGENTS.md and anything under B/input/;
- run exactly one command: python3 B/check_outputs.py --model <MODEL>;
- create and write files under B/out/<MODEL>/ only.
Everything else in this repository is off limits, because it holds the outcomes of these
companies: no CLAUDE.md, no dashboard/, no research/ outside B/input/, no other folder in
research/analyses/, no researcher_*/, no archive/, no scripts/, no config/ and no .claude/
at the repository root (B/input/ carries its own copies of the definitions you need, in
the versions that apply), and nothing under B/out/ except your own <MODEL> folder. No
git commands (the history quotes outcomes), no grep, rg, find or ls over the repository,
no web search, no network, no package installs. Do not use anything you may know about
what happened to a company, its stock or its results after its baseline's seal time
(baseline.as_of_utc). Some packs are anonymised (id starts with anon/; name, ticker and
URLs replaced by placeholders): judge them like any other and do not try to identify them.

=== THE WORK ===
1. Run python3 B/check_outputs.py --model <MODEL>. It lists the 13 packs files in the
   order to do them (part A-backtest first, then B-oktober) and which are done. Skip a
   pack marked done. Fix a pack marked partial or bad (judge only what is missing or
   wrong, keep the rest).
2. For each pack still to do, in that order:
   a. PART is A-backtest or B-oktober, from the check's output. The pack file is
      B/input/<PART>/packs/<name>.json. Every path inside a pack (hunter_definition,
      lessons_file) and config/hunter-core.md are relative to B/input/<PART>/, so
      _claude/agents/unpriced-hunter.md means B/input/<PART>/_claude/agents/unpriced-hunter.md.
   b. Read the hunter definition(s), lessons file(s) and config/hunter-core.md of that
      PART before the first pack of the PART. The two parts carry DIFFERENT versions of
      these files; when you move to B-oktober, read its own copies.
   c. Judge each company in the pack (rules below), from that pack alone. Do not carry
      a view from an earlier pack or company into the next.
   d. Write B/out/<MODEL>/<PART>-<name>.json, rewriting it after every ten companies so a
      stopped run leaves its work, then run the check again before the next pack.
3. When the check shows every pack done, write B/out/<MODEL>/meta.json (below), run the
   check once more until it prints ALL DONE, and finish.

=== JUDGING ONE COMPANY ===
You are the hunter described in the pack's hunter_definition, with one difference: the
searching is done. Ignore everything in that definition about searching, tools, web
access, budgets, the pre_lessons freeze and the files a hunter writes. Each pack gives
the sealed baseline (what the market had priced at the seal: implied move, past
reactions, run-ups, positioning), context the first hunter wrote (the bar, positioning),
and a numbered list of evidence items, each tagged with how the first hunter classified
it (filed_by_first_hunter, put_outside_window_by_first_hunter, rejected_by_first_hunter,
listed_as_searched_and_found_nothing). The tag is its opinion, not a fact. Judge every
item yourself, applying the definition, its lessons file and the shared core exactly as
a live hunter would:
1. decide which items are findings (only the core's four drop reasons may drop one);
2. set abs_move_pct, the size of the move you expect over the event window, never
   shrunk for uncertainty;
3. set p_up, 0-100, where all the uncertainty goes; 50 means no view;
4. give the findings shares (expected_impact_pct, signed, in points of spot) that add up
   to (2 x p_up / 100 - 1) x abs_move_pct.
A company where nothing qualifies is p_up 50 and impact_sum 0.
For B-oktober only: size honestly at both ends. A name with a strong, sourced,
in-window case that the baseline does not hold deserves a large number; a name with
nothing deserves zero. Each judge's number is read against that judge's OWN range, so a
judge that sizes every name alike adds nothing.

=== OUTPUT, PER PACK ===
One JSON array, one object per company, in pack order, nothing else in the file:
[{"id": "us/2026-09-23/ABC", "abs_move_pct": 8.0, "p_up": 62, "impact_sum": 1.92,
  "findings": [{"i": 0, "expected_impact_pct": 1.42}, {"i": 3, "expected_impact_pct": 0.5}],
  "note": "one sentence: the item(s) the number rests on"}]
Use each pack's id exactly. "i" is the evidence item's index in that pack. impact_sum is
the sum of the findings and equals (2 x p_up / 100 - 1) x abs_move_pct to two decimals.

=== meta.json ===
{"model_label": "<MODEL>",
 "model": "<the model name exactly as shown for this task>",
 "reasoning_effort": "<as set for this task, or unknown>",
 "training_cutoff": "<your training data cutoff, as you understand it>",
 "files_read": ["<every file you opened in this task, repository-relative>"],
 "commands_run": ["<every shell command you ran>"],
 "packs_done_in_this_task": ["<PART>-<name>", "..."]}
If an earlier task already wrote meta.json, keep its content and append this task's
files_read, commands_run and packs under a new key "continuation_<n>".

Finish with one line per pack: the output path and how many companies it holds.
```

## Afterwards

- Open the task's log and scan the commands. Any read outside `research/analyses/rejudge-codex/`
  (`CLAUDE.md`, `dashboard/`, a `git log`, a repository-wide `rg`) voids the run: discard
  its `out/<MODEL>/` and run it again in a new task.
- Merge or push the `out/<MODEL>/` files to the branch; the scoring is built on them.

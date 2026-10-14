# Task prompt: paste this into one Codex task per packs file per model

Replace the three values in the first lines. Run each packs file as its own task (a fresh
task, not a follow-up), once with GPT-6 Astra and once with GPT-5.6 Sol.

```text
PART:  A-backtest            (or B-oktober)
PACKS: A-backtest/packs/us1.json
MODEL: astra                 (or sol)

Read AGENTS.md first and follow it exactly. Then judge every company in PACKS.

Each pack gives the sealed baseline (what the market had priced at the seal: implied
move, past reactions, run-ups, positioning), context the first hunter wrote (the bar,
positioning), and a numbered list of evidence items, each tagged with how the first
hunter classified it (filed_by_first_hunter, put_outside_window_by_first_hunter,
rejected_by_first_hunter, listed_as_searched_and_found_nothing). That tag is its
opinion, not a fact. Judge every item yourself.

Per company, apply the hunter definition, its lessons file and the shared core exactly
as a live hunter would:
1. decide which items are findings (only the core's four drop reasons may drop one);
2. set abs_move_pct, the size of the move you expect over the event window, never
   shrunk for uncertainty;
3. set p_up, 0-100, where all the uncertainty goes; 50 means no view;
4. give the findings shares (expected_impact_pct, signed, in points of spot) that add
   up to (2 x p_up / 100 - 1) x abs_move_pct.
A company where nothing qualifies is p_up 50 and impact_sum 0.

Only if PART is B-oktober, also apply this: size honestly at both ends. A name with a
strong, sourced, in-window case that the baseline does not hold deserves a large number;
a name with nothing deserves zero. The panel reads each judge's number against that
judge's OWN range, so a judge that sizes every name alike adds nothing.

Write ONE JSON array to out/<PART>-<packs file name without .json>-<MODEL>.json, for
example out/A-backtest-us1-astra.json: one object per company in PACKS, in PACKS order,
nothing else in the file:

[{"id": "us/2026-09-23/ABC", "abs_move_pct": 8.0, "p_up": 62, "impact_sum": 1.92,
  "findings": [{"i": 0, "expected_impact_pct": 1.42}, {"i": 3, "expected_impact_pct": 0.5}],
  "note": "one sentence: the item(s) the number rests on"}]

Use each pack's id exactly as given. impact_sum is the sum of the findings'
expected_impact_pct and must equal (2 x p_up / 100 - 1) x abs_move_pct to two decimals.
Cover every company. Write the file as you go (rewrite it after every ten companies) so
a cut-off task leaves its work behind; the final file must be one valid JSON array.

Then write out/<same name>.meta.json:
{"model": "<the model name exactly as the model picker shows it>",
 "reasoning_effort": "<as set for this task>",
 "training_cutoff": "<your training data cutoff, as you understand it>",
 "companies_in_packs": <n>, "companies_written": <n>,
 "files_read": ["<every file you opened>"]}

Then reply with one line: the output path and how many companies you wrote.
```

## Checks after each task

- `companies_written` equals `companies_in_packs`.
- `files_read` lists only AGENTS.md, PROMPT.md, the packs file and that part's
  definition files. Any other file, or any web access, voids the task: delete its two
  output files and run it again in a fresh task.

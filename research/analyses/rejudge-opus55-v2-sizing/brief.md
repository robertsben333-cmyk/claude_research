# Blinded re-judge: Opus 5.5 under the two-measurement core, on the Opus 5 days

You are judging earnings research that has already been collected. This is an
experiment and nothing you write is traded.

## What you may read, and nothing else

Use only the Read tool, and only on: this brief; the one packs file named in your
prompt; each `hunter_definition` file and each `lessons_file` named inside that pack;
and `config/hunter-core.md`. **No web search, no web fetch, no Bash, no Grep or Glob, no
other file.** The repository holds the realised outcomes for these companies elsewhere,
and opening anything else ruins the experiment. Do not use anything you may know about
what happened to a company after its baseline's seal time. CLAUDE.md is in your context
and quotes some outcomes; ignore every outcome it mentions.

## The task, per company

You are the hunter named in the pack's `hunter_definition`, with one difference: the
searching is done. An earlier hunter searched and recorded what it found; its sizes,
verdicts and final numbers are removed. Each pack gives the sealed baseline, some
context the first hunter wrote (the bar, positioning), and a numbered list of evidence
items, each tagged with how the first hunter classified it. That tag is its opinion,
not a fact. Judge every item yourself.

Apply the hunter definition and its lessons file exactly as a live hunter would,
**including the shared core at the top of the definition, as it reads today**. Its
step 3 asks for TWO measurements that are never fitted to each other:

1. **Each finding on its own.** Decide which items are findings (the core's four drop
   reasons). Size every finding at what THAT finding alone would move the stock over
   the window, signed, in points of spot. Do not divide a total among them and do not
   shrink them so their sum matches anything. `impact_sum` is the sum of these sizes.
2. **The print as a whole.** `abs_move_pct` (never shrunk for sign uncertainty) and
   `p_up` (0-100, where all the uncertainty of this measurement goes).

Do NOT make the findings add up to (2 x p_up / 100 - 1) x abs_move_pct. A company where
nothing qualifies has no findings, `impact_sum` 0, and `p_up` 50. Skip the pre_lessons
freeze.

## Output

Write ONE file, the path given in your prompt, containing only a JSON array with one
object per company in your pack:

[{"id":"us/2026-09-08/ABC","impact_sum":2.4,"abs_move_pct":8.0,"p_up":58,"findings":[{"i":0,"expected_impact_pct":1.8},{"i":3,"expected_impact_pct":0.6}],"note":"one short sentence"}]

`id` exactly as given in the pack (anonymised ids start `anon/`; judge those from the
evidence alone and do not try to work out the company). `impact_sum` must equal the sum
of your findings' `expected_impact_pct`. Cover every company in the pack.

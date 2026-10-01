# Blinded re-judge, full set (2026-10-01)

You are judging earnings research that has already been collected. This is an
experiment and nothing you write is traded.

## What you may read, and nothing else

Use only the Read tool, and only on: this brief; the one packs file named in your
session prompt; each `hunter_definition` file and each `lessons_file` named inside
those packs; and `config/hunter-core.md`. **No web search, no web fetch, no Bash, no
Grep or Glob, no other file.** The repository holds the realised outcomes for these
companies elsewhere; opening anything else ruins the experiment. Do not use anything
you may know about what happened to a company after its baseline's seal time.

## The task, per company

You are the hunter named in the pack's `hunter_definition`, with one difference: the
searching is done. An earlier hunter searched and recorded what it found; its sizes,
verdicts and final numbers are removed. Each pack gives the sealed baseline, some
context the first hunter wrote (the bar, positioning), and a numbered list of
evidence items, each tagged with how the first hunter classified it. That tag is its
opinion, not a fact. Judge every item yourself.

Apply the hunter definition and its lessons file exactly as a live hunter would,
**including the shared core at the top of the definition**: decide which items are
findings (the core's four drop reasons), set `abs_move_pct`, set `p_up`, and give the
findings shares that add up to (2 x p_up / 100 - 1) x abs_move_pct. A company where
nothing qualifies is `p_up` 50 and `impact_sum` 0. Skip the pre_lessons freeze.

## Output

Reply with ONLY one JSON array, one object per company in the packs file, nothing
else:

[{"id":"us/2026-09-23/SFIX","abs_move_pct":8.0,"p_up":55,"impact_sum":0.8,"findings":[{"i":0,"expected_impact_pct":0.8}],"note":"one short sentence"}]

`impact_sum` is the sum of your findings' `expected_impact_pct`. Cover every company.

## Second pass (packs-x1 to packs-x4)

Some packs are anonymised: their id starts with `anon/`, and the company's name, ticker
and every URL are replaced by placeholders. Judge them like any other company, from the
evidence alone. Do not try to work out which company it is, and use the pack's `id`
exactly as given in your output.

# Contract every judge in the judge lab follows

You are one judge in an experiment. Nothing you write is traded.

## Isolation (breaking it ruins the experiment)

Read only the files your task names: your SKILL.md, this contract, your packs file, and
(if your skill says so) one casebook or one learned skill. **No web search, no web
fetch, no Bash, no Grep, no Glob, and no other file.** The repository holds the outcomes
for the companies you are judging elsewhere (`research/`, `dashboard/`, `key.json`,
`*resolved*`, `archive/`, ledgers, analysis folders). Do not open any of them. Do not use
anything you may know about what happened to a company after its baseline's seal time.
Some packs are anonymised (`anon/...` ids); judge them from the evidence and do not try
to identify the company.

## What a pack holds

The sealed baseline (what the market priced: implied move, past reactions, run-ups,
positioning), some context the first hunter wrote (the bar, positioning), and a numbered
list of evidence items it surfaced, each tagged with how it classified the item. The
tag is the first hunter's opinion. Its sizes and verdicts are removed.

## The question

Not "which way will each stock go". **Which of these names would you put money on, and
how sure are you.** The book trades only the top ~15% of names by your certainty, on
your direction. A name you leave at low certainty costs nothing. A name you put high
that goes the wrong way costs real money. Most names should NOT be high.

## Output

Write ONE JSON array to the output path your task gives, one object per company in your
packs file, nothing else in the file:

```json
[{"id": "us/2026-09-23/SFIX", "direction": 1, "certainty": 35, "expected_move_pct": 6.0,
  "impact_sum": 1.5, "basis": "one sentence: the item(s) this rests on, by index",
  "against": "one sentence: the strongest reason it is wrong"}]
```

- `direction`: 1 (up), -1 (down), 0 (no view).
- `certainty`: 0 to 100, how sure you are that the direction is right AND the move is
  big enough to be worth trading. Use the whole range. Across a typical set, about one
  name in six or seven should sit at 60 or above.
- `impact_sum`: your signed size in points of spot, as the hunter definition would set it.
- Use each pack's `id` exactly. Cover every company. Then reply with one line: the
  output path and how many companies you wrote.

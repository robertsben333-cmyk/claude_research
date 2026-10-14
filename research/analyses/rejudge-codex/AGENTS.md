# Blind panel re-judge: rules for every task in this folder

This folder is an experiment in judging earnings research that has already been
collected. Nothing you write is traded. Four other models have judged the same packs
independently; you never see their verdicts and must not guess them.

## What you may read, and nothing else

- `AGENTS.md` and `PROMPT.md` in this folder;
- the ONE packs file named in your task;
- inside the same part folder (`A-backtest/` or `B-oktober/`): each `hunter_definition`
  and `lessons_file` named in that packs file, and `config/hunter-core.md`. Paths in the
  packs are relative to the part folder, so `.claude/agents/unpriced-hunter.md` in a
  pack under `A-backtest/` means `A-backtest/.claude/agents/unpriced-hunter.md`.

**No web search, no web fetch, no network, no other file in this folder**, in particular
no other packs file and nothing under `out/` except the file you write. Use the shell
only to read those files and to write your output. Do not install anything.

Do not use anything you may know about what happened to a company, its stock or its
results after the baseline's seal time (`baseline.as_of_utc`). Judge from the pack.
Some packs are anonymised: their id starts with `anon/` and the name, ticker and URLs are
placeholders. Judge them like any other company and do not try to work out which company
it is.

## Who you are in this task

You are the hunter described in the pack's `hunter_definition`, with one difference: the
searching is done. Ignore everything in that definition about searching, tools, web
access, budgets, the pre_lessons freeze, and the files a hunter writes: the only output
here is the one described in `PROMPT.md`. Apply its judging and sizing rules, its lessons
file and the shared core (`config/hunter-core.md`) exactly as a live hunter would.

## Output files

Write only to `out/`, only the two files your task names, and never edit any other file.

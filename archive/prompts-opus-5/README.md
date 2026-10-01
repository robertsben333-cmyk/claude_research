# Hunter prompts as they stood under Opus 5 (reference, not live)

Every hunter definition and LESSONS file exactly as they were on `main` at `813c5a5`
(2026-10-01 06:47 UTC), before the 2026-10-01 rewrite for Opus 5.5. These are the
instructions every run up to 2026-09-22 used (served on Opus 5), and every run from
09-23 to 10-01 (served on Opus 5.5, which read them too strictly).

The files carry a `.txt` suffix and sit outside `.claude/agents/` on purpose, so the
harness never loads them as agents. To re-run the old prompt deliberately, copy a file
back into `.claude/agents/` under a new `name:`.

What changed and why: CLAUDE.md, "The hunters moved to Opus 5.5 on 2026-09-22", and
`config/hunter-core.md`, which is now the first section of every live hunter.

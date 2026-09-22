# Right baseline, stale brief — the harness snapshot, observed a second time

These two hunts ran on 2026-09-22 against the NEW baselines (with the `forward` block)
but were served the OLD `reversal-hunter` definition: the harness registers
`.claude/agents/` once and keeps that snapshot for the life of a session, so the file on
disk had already been rewritten while the spawnable agent had not.

The tell is in the output, not in any error. Both files carry `drop_explained_pct` and
`cause.mechanical_vs_informational` — v1 fields — and neither carries
`more_to_come_pct`, `cause.seller_is_finished_pct` or `pipeline.news_flow_balance`, which
v2 requires. Nothing failed; the wrong contract simply came back looking correct.

They are kept because they are not worthless: they used the forward block and their
findings are dated, sourced supply mechanisms (an effective resale S-3, a $33.21 crossover
block, a cash runway against a planned Phase 2b/3). What they are not is a validation of
the v2 contract.

This is the third time in this repo that a running process and the tree have disagreed
and the tree was the thing that moved — see CLAUDE.md on the 2026-09-15 merges. The rule
is the same: check what the process was actually served before blaming the definition.

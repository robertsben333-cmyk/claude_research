# Hunter model trial

Question (Xavier, 2026-10-14): what does the hunter's model do to the number of findings and to the panel scores?

Design: one US name (CMC, Commercial Metals, FQ4 bmo 2026-10-15), one sealed baseline copied into every arm, so only the searcher's model differs. The searcher is stage E-P's `unpriced-searcher` definition. The four E-P judges (`panel-judge-*`, pinned) judge each arm blind and separately. `panel_score.py --dry-run`: percentiles against each judge's live E-P range, nothing written to the panel history. One run per model. **n = 1 name. Nothing here is evidence; it is never pooled with live runs.**

| arm | how it ran | tool calls / minutes | findings | rejected | sources | searcher impact_sum, abs_move, p_up | panel_pct, side | judges' own percentile (opus5 / opus55 / sonnet55 / fable51) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Opus 5.5 | `unpriced-searcher` (pinned) | 58 / 11 | 10 | 4 | 24 | -0.1, 5.0, 45 | 37 short | 23 / 32 / 54 / 39 |
| Sonnet 5.5 | `general-purpose`, model sonnet, definition read in | 9 / 1 | 0 | 2 | 6 | 0.0, 4.0, 50 | 0 | 0 / 0 / 0 / 0 |
| Fable 5.1 | `general-purpose`, model fable, definition read in (substitute arm) | 101 / 13 | 10 | 9 | 31 | +0.8, 5.5, 53 | 42 long | 23 / 52 / 54 / 39 |
| Opus 5 | not run: no alias reaches it from a session; prompt for a UI one-shot Routine in `/mnt/project-files/hunter-model-trial/opus5-routine-prompt.txt` | | | | | | | |

Caveats: the Sonnet and Fable arms did not get the definition's frontmatter (`effort: high`, `maxTurns: 90`), so model and effort are confounded there; Sonnet's 9 tool calls may be effort, not model. The option chain was unusable at the 07:10 ET seal, so no arm had an implied move.

Files: `2026-10-14-CMC/<arm>/hunts/CMC.json` (searcher), `panel/<judge>.json`, `edge-scores-panel.json`.

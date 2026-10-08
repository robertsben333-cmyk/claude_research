# Step 4p — the four-model panel, for stages EU, J, AU and CA

Since 2026-10-08 (operator's instruction) every non-US researcher stage runs stage E-P's
judging method after its own scoring step: the day's hunter evidence goes into blind
packs, four judges on four different models size it independently, and
`panel_score.py` combines them with stage E-P's frozen rules. The stage's own hunters,
its `impact_sum` key and everything before scoring are unchanged. The US stages are not
touched by any of this. Background and rationale: `scripts/market_panel.py`'s docstring
and the `market_panel` block in `config/pipeline.yaml`.

`<M>` is the stage's market code (`EU`, `JP`, `AU`, `CA`), `<RUN>` its run directory and
`<STAGE>` the run-log prefix the skill already uses (`Stage EU`, `Stage J`, `Stage AU`,
`Stage CA`). Run this AFTER `edge_score.py --run <RUN>` has written `edge-scores.json`,
so the packs hold exactly the names the stage ranks, and BEFORE the note.

1. **Packs.**
   ```bash
   python3 scripts/market_panel.py packs --market <M> --run <RUN>
   ```
   It writes `<RUN>/panel/packs.json`: per rankable hunted name, the sealed baseline, the
   context the hunter wrote and every evidence item, with every size, verdict and final
   number removed, plus the hunter definition and lessons file the judges apply. If it
   reports 0 packs there is nothing to judge: say so in the note and go to the note.

2. **Heartbeat, then publish, before spending anything:**
   ```bash
   python3 scripts/run_log.py --heading "<STAGE> — panel STARTED" --line "<n> packs, four judges"
   scripts/publish.sh "<stage prefix>: panel started for <DATE>"
   ```

3. **Four judges, in ONE message, in parallel**, one per model, each with this prompt and
   nothing else (fill in the two paths):

   > Follow your definition. Your packs file is `<RUN>/panel/packs.json`. Write your JSON
   > array to `<RUN>/panel/<member>.json`. Use only Read and Write.

   | member | agent | fallback if the agent or its model is refused |
   | --- | --- | --- |
   | `opus5` | `panel-judge-intl-opus5` (`claude-opus-5`) | **none**: no alias reaches Opus 5. Run without it and record it missing |
   | `opus55` | `panel-judge-intl-opus55` (`claude-opus-5-5`) | `general-purpose`, `model: opus`, body of `config/panel-judge-intl.md` pasted in |
   | `sonnet55` | `panel-judge-intl-sonnet55` (`claude-sonnet-5-5`) | `general-purpose`, `model: sonnet`, same |
   | `fable51` | `panel-judge-intl-fable51` (`claude-fable-5-1`) | `general-purpose`, `model: fable`, same |

   **Use the `-intl-` judges, never stage E-P's `panel-judge-*`**: those may only open the
   US hunter definition, and these packs name the market's own. **Never give a judge
   anything beyond the packs file**: not the hunts, not `edge-scores.json`, not another
   judge's output, not your own view. Their independence is the whole point of the panel.

4. **Check coverage.**
   ```bash
   python3 scripts/market_panel.py check --market <M> --run <RUN>
   ```
   Exit 0 means every pack id is in every member's file. Otherwise re-launch a member
   once for the ids it missed (output `<RUN>/panel/<member>-retry.json`, merged by hand
   into `<member>.json` before scoring). A member that fails twice is missing for the day:
   delete its partial file so the scorer does not read half a member.

5. **Combine.**
   ```bash
   python3 scripts/market_panel.py score --market <M> --run <RUN>
   ```
   Add `--fallback <member>=general-purpose:<alias>` for each member that ran through a
   fallback. It reads each member against that member's own history for THIS market
   (`researcher_<market>/analysis/panel-history.json`), writes
   `<RUN>/edge-scores-panel.json`, appends the day's sizes to that history, and writes the
   `panel` block into `<RUN>/provenance.json`. Fewer than four members is allowed: the
   selection becomes all of three, and the note must say which model was missing.

6. **Publish** the packs, the four member files and the panel scores:
   `scripts/publish.sh "<stage prefix>: panel for <DATE>"`.

## In the note

Put a panel section directly under the ranked table:

- one line: **four blind judges (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) re-sized the
  hunters' evidence; the panel ranks beside `impact_sum` and replaces nothing**; which
  members ran, and any fallback;
- the panel table as `score` printed it: rank, ticker, `selected`, `consensus_k`, sign
  agreement, `panel_score`, each member's z (`*` where in its own top 20%), and the
  hunter's own `impact_sum` beside it;
- one paragraph per **selected** name: the evidence items the members' notes name, and the
  strongest case against;
- where the panel and the hunter's `impact_sum` disagree most (opposite sign, or a name
  above the conviction floor the panel did not select), one line each;
- what the numbers are not: `panel_score` ranks and does not forecast; there is no
  `expected_edge_pct` off the US; certainty (`p_up`) is recorded and decides nothing; the
  member scales are still mostly the frozen E-P seed until this market has about 200
  panel names of its own; and in the four-model re-judge the judges ranked Europe better
  than the live hunt but Japan and Australia worse, so nothing about this market's panel
  is established.

Paste the panel table from `score` into the closing chat reply, directly after the
`score_report.py` output the skill already asks for.

## Resolving

After the market's own resolver has written its `*-resolved.json`:

```bash
python3 scripts/market_panel.py resolve --market <M> --run <RUN>
```

It writes `<RUN>/panel-resolved.json`: ρ for `panel_score` and for `impact_sum` on the
same names (withheld below five), and the selected names against the hunter's
above-floor book, gross, in the resolver's own window. One day is an anecdote; read it
pooled:

```bash
python3 scripts/market_panel.py pool --market <M>
```

This is research, not investment advice. Nothing here places an order.

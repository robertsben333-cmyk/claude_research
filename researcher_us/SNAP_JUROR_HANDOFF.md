# Handoff: SubQ Snap as a fifth, non-Anthropic juror on stage E-P

Written 2026-10-14 by a session that could not hold the API key. Pick this up in a new
session whose environment carries `SUBQ_API_KEY` and allows `api.subq.ai`. Everything a
decision was needed for is decided below; build it as written and change a decision only
for a measured reason, recorded here.

## Why

The E-P panel counts "3 of 4 members agree" as independent confirmation, but all four
members (Opus 5, Opus 5.5, Sonnet 5.5, Fable 5.1) are Anthropic models and their errors
are probably correlated. SubQ Snap (Subquadratic, public preview since 2026-10-12) is a
decision model from another lab on another architecture: it answers declared questions
over declared answers and returns a probability for every answer. It is the first juror
whose mistakes could plausibly be uncorrelated with the panel's.

**It is a shadow column, not a member.** It ranks beside the panel in `edge_resolve.py`
and nothing that selects, sizes or trades reads it. Promotion into `panel_score.py` is a
separate decision for after it has pooled, and it needs the operator.

## The API (from docs.subq.ai, read 2026-10-14)

- `POST https://api.subq.ai/v1/systemone`, header `Authorization: Bearer $SUBQ_API_KEY`,
  `Content-Type: application/json`.
- Body: `model` = `subq-snap-preview` (the only id), `state` (text, object or array),
  `questions` = 1-16 named questions. Optional `images`, not used here.
- Question types: `noul` (yes/no; answer `noul` = P(yes)); `choice` (`criteria` = 2-255
  named options, each a description or null; answer `choice`, `probabilities`,
  `confidence`); `score` (`criteria` = 2-10 ordered level strings; answer `score`
  (fractional), `legend`, `probabilities`, `confidence`).
- Response: `model`, `answers` keyed by question name, `usage.input_tokens`
  (`output_tokens` is always 0). Price $0.05 per M input tokens.
- Limits: 384K context (a request at or near it fails 400), question names <= 100 chars.
- Errors: `detail.error_type` + `detail.message`; 400 too long or rejected, 401 key,
  402 credits, 403 key cannot use model, 422 invalid request, 429 rate limit, 503 down.
- No published rate limits and no published calibration data. All benchmarks are the
  vendor's own.

## First thing in the new session

1. `echo ${SUBQ_API_KEY:+set}` must print `set`. Never print the key itself.
2. One smoke call with a trivial `noul` question. A 403 with an HTML body is the
   network policy (the host is not allowed); a 403 with a JSON `detail` is the key not
   having access to the model. They have different fixes; report which.
3. Only then build.

## What to build

Work on your session's own branch and bring this file across from
`claude/vibrant-newton-lsndrf` if it is not on `main` yet. Do not use
`scripts/publish.sh` while building; it pushes to `main`. Do not merge to `main` without
the operator: the E-P Routine runs whatever `main` holds.

### 1. `researcher_us/scripts/snap_juror.py --run <RUN>/edge-panel [--dry-run]`

- Reads `<RUN>/edge-panel/panel/packs.json` (built by `panel_packs.py`; a list of packs
  with `id`, `hunter_definition`, `lessons_file`, `baseline`, `first_hunter_context`,
  `evidence`). A pack is about 4-5k tokens, so one pack per request is far under the
  limit.
- `state` = the pack minus `hunter_definition` and `lessons_file` (Snap cannot open
  files), plus a short fixed preamble naming the window: entry at the regular close
  before the print, exit at the regular close after the first full session, moves in
  percent of spot. The preamble is a constant in the script and is versioned with it.
- HTTP with `urllib.request`, as `alpaca_trade.py` does. No SDK, no pip install: a
  Routine must not need one. Timeout 30 s, at most two retries with backoff on 429/5xx,
  none on 4xx.
- Three questions per pack:
  - `move` (choice): where the move over the window lands. Bins with edges
    `-inf,-20,-15,-12,-10,-8,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,8,10,12,15,20,+inf`
    (24 options), each described in words ("falls between 3% and 4%"). Representative
    values: bin midpoints, tails at -25 / +25. Derived per name:
    `snap_impact` = E[move], `snap_p_up` = 100 x P(move > 0), `snap_abs` = E[|move|].
    `snap_impact` is the ranked number; it is on the same footing as a judge's
    `impact_sum`, which is (2 p_up/100 - 1) x abs_move_pct.
  - `up` (noul): will the stock close the window above the entry price. Kept as a cross
    check on the `move` distribution; its disagreement with `snap_p_up` is logged, not
    used.
  - `vs_implied` (score): `|move|` against the sealed implied move, five levels from
    "well under half" to "well over 1.5x". Logged, not ranked.
- Writes `<RUN>/edge-panel/panel/snap.json` (raw response per pack, plus the request
  hash, the `model` string the API returned, the script version and the UTC time) and
  `<RUN>/edge-panel/edge-scores-snap.json` with `ranking_by_ticker`:
  `{ticker, snap_impact, snap_p_up, snap_abs, snap_vs_implied, confidence_move,
  p_up_noul}`.
- Never fatal. No key, host denied, 4xx, a pack over the limit: write the file with
  `status` and `reason` per name and exit 0, so the stage run carries on.
- On the first live day only, call each pack twice and record whether the two answers
  were identical (`repeat_identical`). Determinism is unverified and it matters for
  whether one call per name is enough.

### 2. `edge_resolve.py`

Add `score_snap` from `edge-scores-snap.json` exactly the way `score_panel` is read from
`edge-scores-panel.json` (around line 280), and `spearman_snap` everywhere
`spearman_panel` appears (the two ranking tuples and the two print blocks).

### 3. `config/pipeline.yaml`

A `snap_juror` block: `enabled: true`, `model: subq-snap-preview`, `host:
api.subq.ai`, the bin edges, timeout, retries, `places_orders: false`,
`reads_into_selection: false`. The script reads the bins from here, not a literal.

### 4. The E-P skill

In `.claude/skills/earnings-edge-panel/SKILL.md`, a step 5p.7 after the panel is
recorded: run `snap_juror.py`, then add a `snap` entry to the `panel` block of
`provenance.json` (model string as returned, script version, status). The note gets one
line under the panel: Snap's top and bottom name, or why it did not run. Snap's numbers
never enter the panel table, the selection or the reply's `score_report.py` table.

### 5. `scripts/smoke_test.py`

- `alpaca_trade.py`, `edge_score.py` and `panel_score.py` must not contain `snap`
  (same pattern as the `edge-context` check near line 1830).
- An offline test with a canned response: the expected value, P(up) and E|move| from a
  known distribution, and the never-fatal path when `SUBQ_API_KEY` is unset. No network
  in the smoke test.

### 6. Allow rule

Auto mode drops the broad Bash rule; see the 2026-10-08 note in `CLAUDE.md`. Add
`Bash(python3 researcher_us/scripts/snap_juror.py:*)` to `.claude/settings.json` the
way the `alpaca_trade.py` rules were added. An auto-mode session refuses to write that
file itself, so this may need the operator.

## Rules that are already decided

- **Forward only, with one exception.** No backfill of runs sealed before 2026-10-12,
  the model's release: its training may contain those outcomes. Runs sealed on or after
  2026-10-12 (`2026-10-12/edge-panel`, `2026-10-13/edge-panel`) may be scored now,
  flagged `basis: retro_post_release`, because their outcomes did not exist when the
  model was built.
- **Version.** `subq-snap-preview` is a preview alias and can change underneath us, as
  `opus` did on 2026-09-22. Record the returned `model` string on every call; if it
  changes, that is a new version and the two are never pooled. Register it in
  `config/prompt-versions.json` via `scripts/provenance.py registry` like a hunter.
- **One primary number.** `spearman_snap` on `snap_impact` is the pre-registered test.
  `up`, `vs_implied` and confidence are logged and are not candidates; adding arms is the
  multiple-comparison problem this repo already has.
- **Judge it pooled, and against the panel on the same names**, not alone. About 200
  names before a difference in rho means anything.
- **Data retention.** Set the shortest retention in console.subq.ai. Everything sent is
  public information, but there is no reason to keep it there.
- Never put the key in a file, a log, a commit or a reply.

## Not in scope here (ideas for later, in order)

1. The same juror on the non-US panels (`scripts/market_panel.py`). English-first
   caveat: check how much non-English text the packs carry.
2. Classification gates (event confirmation, headline classifiers, the file/drop call
   over `rejected_candidates`), tested against the labelled rows of 2026-08-31 and the
   20 phantoms of 2026-09-17. Date comparisons stay in code.
3. A whole-day call: all packs in one `state`, one `move_<ticker>` question per name
   (16 per request). Interesting because the stage is judged on rank within a day; do
   it only after the per-name arm has pooled.

## Built 2026-10-14 (branch `claude/gallant-bohr-hzsesq`), and what changed on the way

**The first-thing checks, as found.** `SUBQ_API_KEY` was NOT set in the building
session. `api.subq.ai` was reachable (JSON answers, not an HTML proxy 403), so the egress
policy allows the host. A request without an auth header got `401 authentication_error:
Missing API key`, so the environment's "SubQ" network secret did not put a key on a bare
request. Nothing live has been called; no number from Snap exists yet.

**Measured, not in the docs above:** every question needs an `instructions` field (422
`must have required property 'instructions'` without it). The API validates the body
before it checks the key, which is how this was learned without one.

**Decisions changed, each for a stated reason:**

- *The smoke check matches the juror's own names, not `snap`.* `alpaca_trade.py` has
  carried `quote_snapshot()` since 2026-09-10, so "must not contain `snap`" fails on
  day one. It checks `snap_juror`, `edge-scores-snap`, `snap_impact` and `subq`.
- *`basis` is set by WHEN Snap is asked, not by a fixed date.* `forward` = asked no later
  than the run's seal day; `retro_post_release` = asked later, on a run sealed on or
  after `release_date`; `refused_pre_release` = sealed before it, nothing sent.
- *No key, no call.* The script sends nothing without `SUBQ_API_KEY` (status `no_key`);
  a 401 with a key is `bad_key`. The first `no_key`/`bad_key`/402/JSON-403/egress-403
  stops the remaining calls.
- *The registry keeps jurors apart.* `config/prompt-versions.json` gained a `jurors`
  section (`snap-juror`, ids `us-snap.vN`, from the script's blob), so the dashboard's
  hunter versions do not pick it up. `provenance.py check` fails on an unregistered
  juror the same way it does on a hunter.
- *The `repeat_identical` day* is the first `forward` day on which no earlier E-P run
  holds a Snap file with an answered name; `--repeat` / `--no-repeat` override it.
- The allow rule in `.claude/settings.json` was written by the building session itself
  (it was not refused).

**Plumbing run** on `2026-10-13/edge-panel`, outputs in the session scratchpad only:
9 packs, 18-24 KB per request body, `--dry-run` and the no-key path both exit 0 and
write both files plus the `provenance.json` `snap` entry; `edge_resolve.py` reads the
file and skips it while no name is answered. `smoke_test.py` passes.

## First live test 2026-10-14

A session with `SUBQ_API_KEY` in its environment, `snap.v1` unchanged. Outputs stayed in
that session's scratchpad; nothing was written to `research/`.

**What the API returned.** Every call answered first time (`attempts: 1`), no 4xx, no
retry. The returned `model` was `subq-snap-preview` on every call, the same string as
requested, so the alias does not reveal a dated build: a silent change underneath it
would not show in that field. The shape matches what the script already parsed, so
nothing had to change:

- `move` (choice): `type`, `choice` (the modal bin), `probabilities` **keyed by bin
  name**, all 24 present, summing to 1.0000, and `confidence` (0.08-0.35 here).
- `up` (noul): `type` and `noul`, a float in 0-1. The field really is called `noul`.
- `vs_implied` (score): `type`, `score` (fractional, 1.35-1.93 here), `legend` and
  `probabilities` both keyed by the level's INDEX as a string (`"0"`-`"4"`), not by its
  text, and `confidence`. The script reads only `score`, so this is harmless, but anything
  that later reads these probabilities must key on the index.
- `usage.input_tokens` 6,632-8,622 per pack, `output_tokens` 0.

`snap_impact`, `snap_p_up`, `snap_abs` and `p_up_noul` were filled for 18 of 18 names,
no NaN. `snap_impact` ran from -2.80 to +1.61, `snap_abs` 3.0-5.2. The `up` answer agrees
in rank with `snap_p_up` (Spearman 0.90 and 0.97 per day) and is more extreme (FAST 8.7
against 23.9, BLK 90.1 against 75.6); logged, not used.

**Cost.** 2026-10-13: 66,421 input tokens, $0.0033 for nine names. 2026-10-12: 68,537,
$0.0034. About $0.0004 a name; the whole test, every call included, was under $0.02.

**Repeatability: deterministic, but not invariant to formatting.** The same request
sent three times (one `--no-repeat` run, then `--repeat`, which calls twice) returned
byte-identical answers on 9 of 9 names: `repeat_identical: true`, every probability equal
to the last digit. So a second call of the same request adds nothing. But a request that
is the SAME CONTENT with the pack's keys and the three questions in reverse order (an
extra probe, scratchpad only) moved `snap_impact` by a median 0.22 points and at most
1.02 (PGR -2.68 to -1.66, BLK +1.61 to +0.99), and flipped AZZ from -0.39 to +0.18,
against a cross-name spread of 1.6. The day's ranking held (Spearman 0.967 between the
two). Read: the number is a deterministic function of the exact request bytes, so
**the request layout is part of the version**. Any change to `PREAMBLE`, the question
text or order, or to the pack layout `panel_packs.py` builds is a new version and must
not be pooled with the old, even with `SCRIPT_VERSION` unchanged on the Snap side; the
`request_sha256` on every call is what makes that checkable.

**Basis.** 2026-10-12 and 2026-10-13 both came back `retro_post_release`. 2026-10-09 was
refused (`refused_pre_release`, 0 tokens, nothing sent).

**Beside the panel, descriptive only.** The two sealed panel files predate the
mean-percentile rule, so `panel_pct` was recomputed with `panel_score.py --dry-run` on a
scratchpad copy (point-in-time: its reference uses runs dated before each day; the
history file was not touched). No name was selected on either day, under either rule.
Spearman `snap_impact` against `panel_pct`: +0.35 on 10-12, +0.70 on 10-13; against the
searcher's `impact_sum`: +0.08 and +0.63. Resolved on 10-12 only (the 10-13 names close
their window on 10-14): `spearman_snap` **+0.083** against `spearman_panel` +0.833 and
`spearman_panel_pct` +0.75, n = 9. Snap's top name, FBK +0.55, fell 4.21%; its bottom,
ACI -1.87, rose 1.44%. Nine names is an anecdote; nothing is judged before about 200.

**Script changes: none.** The parser already handled the real shape.

## snap.v2 and the full backtest, 2026-10-14

**The question changed, on the operator's instruction: Snap is now asked what the four
judges are asked.** `config/snap-judge.md` is the task section of `config/panel-judge.md`
word for word, with only the reading and output rules changed (Snap cannot open files or
write JSON). The script inlines it with the window, the pack's hunter definition (which
opens with the shared core) and its lessons file, the same texts the judges read; none of
the three has changed since 2026-10-01, so October's judges and Snap read identical text.
Two questions replace v1's three: `abs_move_pct` (choice over |move| bins
`abs_bin_edges`, open tail at `abs_tail_value`) and `p_up` (noul).
`snap_impact` = (2 x p_up/100 - 1) x E|move|, the judges' own `impact_sum`, stays the one
pre-registered number. `SCRIPT_VERSION` is `snap.v2`; v1's bins left the config.
`edge_resolve.py` is unchanged (it reads `snap_impact`). A request is now about 19k input
tokens, $0.001 a name.

Versioning: the brief is registered as a second juror entry, `snap-judge-brief`, so an
edit to it is a new version like an edit to the script. The registry derives ids from
main's history and neither file has been on main, so both read `.v1*` (pending merge)
while the script calls itself `snap.v2`; the script string is the one recorded per call.
Each call also records `docs_sha256` over the inlined texts.

**The backtest: no demonstrable added value.** `research/analyses/snap-juror-backtest/`,
154 US names over 21 days (the 119 Opus 5-era re-judge names and 35 October panel names,
the same sample and returns as `research/analyses/panel-mean-pct/`), 437 calls, all `ok`,
model `subq-snap-preview` throughout, $0.19. Pooled, strategy exit entered 19:30 CET:
Snap v2 within-day ρ +0.159 (p 0.066) against +0.271 for the four-judge mean and +0.177
to +0.286 for each judge; Snap's own top 20% +4.1% against +7.3%. The five-member mean
(judges + Snap) against the four: top 20% +6.8% against +7.3%, top 10% +11.5% on 8 names
against +9.9% on 11; at equal numbers of names it wins at k=10 and 20 and loses at 15 and
30, with 80-100% of the names the same. Inside the panel's top 20% Snap agreed on the
sign 25 times of 25, so it cannot act as a veto either. Its percentiles are less
correlated with the judges (0.84-0.87) than the judges are with each other (0.91-0.95),
but where it departs from them it ranks worse. v2 beats v1 in the tail (top 20% +4.1%
against +1.3%), not in rank (ρ +0.159 against +0.195).

**Leakage is not ruled out, and it does not change the answer.** 145 of the 154 names
were sealed before Snap's release. A control arm with only ticker, name, date and session
ranks the 94 named backtest names at ρ +0.170 (p 0.11), where v2 reaches -0.023 on the
same names; in October the control is +0.04. Leakage could only favour Snap, so a
negative result here stands, while a positive one would not have. The forward-only rule
in the live script is untouched: this backtest ran from the analysis folder on the
operator's instruction, and the live script still refuses a run sealed before
2026-10-12.

**What it would take to change the verdict:** a forward sample, post-release, where
Snap's ρ approaches the panel's, or where the five-member book beats the four at equal
names by more than its standard error (about 3 points per name in the top 20%). At about
9 names a day that is months, for about $0.01 a day.

## Decision, 2026-10-14: Snap does not become a panel member

The operator's call, after the backtest above. Snap is not promoted into `panel_score.py`
and does not run as a shadow column either: the wiring (`snap_juror.py`, the E-P skill's
step 5p.7, the `snap_juror` config block, the edge_resolve column, the allow rule) stays on
branch `claude/gallant-bohr-hzsesq` and is NOT merged, so the E-P Routine is unchanged.
Only the analysis (`research/analyses/snap-juror-backtest/`) and this file went to `main`,
as the record. Reopening it needs a new reason, not a re-run of this sample.

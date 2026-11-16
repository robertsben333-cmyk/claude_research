## Stage E-P v3b: search for the reaction, not only the quarter

This block is added for stage E-P v3b only, after the stage E-P searcher block above,
which still applies in full. It comes from the review of us-panel.v3 (29 Oct to 12 Nov,
218 names; `research/analyses/us-panel-v3-information/`). That review found that the
panel researches the quarter against consensus, which the market treats as the base
case (about two thirds of releases beat), and barely researches what decides the rest
of the move: the bar the market really holds, statements made inside the quarter, and
the next guide. Four changes follow. None of them replaces a search the core asks for.

### 1. Tag every item with its evidence type

Every finding, every `outside_window` item and every `rejected_candidates` item carries
`evidence_type`, exactly one of:

`consensus_bar` (the quarter against the street's estimate), `expectations` (what the
market already expects: price path, run-up, price against targets, whisper or buy-side
bar, last quarter's beat and reaction, short-interest trend), `mid_quarter_statement`,
`next_guide`, `guidance_mgmt` (other guidance and management commentary),
`counterparty`, `peer`, `positioning`, `capital`, `own_figures`, `regulatory`,
`insider`, `macro`, `analyst_action`, `alt_data`, `one_off`, `reaction_history`,
`other`.

`lands_on` stays as the core defines it. The tag says what kind of evidence the item is;
`lands_on` says which line it moves. The tag is used to measure which evidence carries
the reaction, so pick the honest one, not the flattering one.

### 2. Fill the expectations block, and file what it finds as findings

Write a top-level `expectations` object on every name:

```json
"expectations": {
  "price_path": "5-day and 20-day return into the print, against the sector ETF over the same days, with the source; the baseline's run-up fields are the starting point",
  "vs_targets": "spot against the mean and high analyst price target, with source and date, or 'not found'",
  "whisper_or_buyside_bar": "any reported whisper number, buy-side bar or 'the street needs X' commentary, with source, or 'not found'",
  "last_print": "last quarter's beat or miss on the line this stock trades on, and the stock's reaction to it, with source",
  "short_interest_trend": "the last two short-interest settlements and days to cover, with source and dates, or 'not found'",
  "real_bar": "one sentence: what the release must show for the stock to rise, in the market's terms, not consensus's",
  "real_bar_vs_consensus": "above | at | below | unknown"
}
```

Every field carries a source or says `not found`. The question the block answers is
**what does the market already expect, and is this release likely to clear THAT?** A
consensus beat on a name that ran 25% into the print against a flat sector is not the
same setup as the same beat on a name sold down 15%.

Whatever in the block bears on the reaction is ALSO filed as a finding with
`evidence_type: expectations`, sized like any finding (the core's step 3), with
`lands_on` `positioning` or the line it lands on. The block is context for the judges;
the findings are what gets sized. The review measured this evidence as carrying the most
move per judged point, and it was the evidence filed least.

### 3. Search for what management said inside the quarter

Before you stop, search explicitly for statements dated after the company's last
earnings call: conference and investor-day remarks, reaffirmation 8-Ks, pre-releases,
"on track" comments in interviews, updated targets. File each with `evidence_type:
mid_quarter_statement` and the date it was made. If you find none, write
`"mid-quarter statements: none found after <date of last call>"` in
`searched_and_found_nothing`, so the absence is a recorded result.

### 4. The next guide is a finding of its own

Write a top-level `next_guide` object:

```json
"next_guide": {
  "likely_direction": "raise | maintain | cut | initiate | withdraw | no_guide | unknown",
  "street_next_quarter": "the street's next-quarter figure on the line this stock trades on, with source, or 'not found'",
  "street_full_year": "the street's full-year figure, with source, or 'not found'",
  "company_current_guide": "the company's current guide for those periods, with source, or 'none'",
  "basis": "one sentence: why that direction, from which sourced items"
}
```

and file the evidence for the direction as a finding (or findings) with `evidence_type:
next_guide` and `lands_on: guidance`. A stock that beats and guides below the street
falls; the analysis found shorts on an expected guide cut that became a beat and raise,
and longs whose beat was sold on the guide. Ask the next-guide question on every name.

### 5. Counterparties before peers, and a peer needs a link

Search customers, suppliers and distributors that have reported on the SAME quarter
before generic peers, and tag them `counterparty`. Every `counterparty` and `peer`
finding carries a `link` field naming what ties the two companies, with a figure where
one exists (shared customers, the same product, the same channel, the share of revenue
in the same end market). Where you cannot state a link, still file the item (the core's
drop reasons are unchanged) and write `"link": "none stated"`. The judges are told to
size an unlinked peer small.

### 6. One-offs

An item below operating income (a refund, a settlement, an impairment, a gain) is tagged
`one_off` unless you can source its path into the guide or the multiple, in which case
it is `guidance_mgmt` or `next_guide` and the source for that path is in the finding.

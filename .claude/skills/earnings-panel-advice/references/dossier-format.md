# Dossier format — answer first

The dossier surfaces the prediction before the rationale. A reader who sees only the
first screen must come away with the call, the direction, the size, the probability, the
certainty, and the main caveat. Everything below that is justification.

Write one per panelled name at `03-panel/<TICKER>-dossier.md`.

## Header

The file opens with this block, verbatim in structure:

```text
=== EARNINGS FORECAST: <TICKER> (<Company>) ===
Window covered: <plain language>   |   Event: <BMO/AMC, date>   |   Spot: $<x>
ESTIMATED MOVE   <signed % or unsigned band only>   (band <lo>% … <hi>%;  event-implied ≈ ±<M>%)
CERTAINTY        <High/Med/Low>  ·  P(<up|down>) <p>%  ·  panel <aligned/mixed/split> (disparity <d>/100)
CALL             <Strong/Lean Up · Neutral / No Edge · Lean/Strong Down>   score <s>   reversal risk <r> (<tier>)
```

Immediately after, one line:

```text
Prediction first: <plain-English call and likely direction>; expected post-event move
<signed point or unsigned band>; main reason <driver>; main caveat <reversal risk or
missing anchor>.
```

Use the synthesis packet's `early_prediction` to sharpen this line, but keep the call,
probability, certainty, and move identical to the packet. If the two disagree, the
packet wins.

**If the conviction gate forced `Neutral / No Edge`:** show no signed directional point
estimate anywhere. Show the unsigned expected-move band and state plainly that the
directional evidence was insufficient, naming which gate condition fired.

## The eleven sections

In this order, as concise prose. Length is not the goal — a section with one grounded
sentence beats a paragraph of hedging.

1. **Why this name** — where it came from: universe size, triage scores, deep-dive
   ranking, evidence completeness, and the Phase-0 anchors.
2. **What the market cares about** — the single key metric or management signal this
   print trades on, and what is expected for it.
3. **Expected move size** — implied versus historical anchors, the right-skewed band,
   and whether the event looks fairly priced, rich, or cheap. State that the implied
   move is roughly one standard deviation, not a cap.
4. **Directional consensus** — consensus score, P(direction), reversal risk, disparity,
   and the seven-persona agreement pattern. If the panel is split, say so here in plain
   words, not only as a number.
5. **Thesis** — bull case, bear case, base case. One short paragraph each.
6. **What flips it** — the most credible reversal drivers, tied explicitly to the
   red-team verdict and the reversal-risk evidence.
7. **Positioning & sentiment** — one line each for options/skew, short interest or
   crowding, run-up/momentum, and social/retail tone.
8. **Insider / communication / alt-data findings** — what the forensics persona found,
   and whether it corroborates or contradicts the traditional read. "Nothing unusual" is
   a real finding; report it as one.
9. **Analyst & revisions read** — consensus, revisions, guidance setup, caveats.
10. **Panel table** — markdown, columns: Persona · Score · P(up) · Reversal risk ·
    Confidence · Top driver.
11. **Sources** — grouped by what they support. Every company-specific claim in the
    dossier traces to one of them.

## Final line

End every dossier with this sentence exactly:

> This is research, not financial advice. Earnings reactions are highly uncertain and
> can be driven by market positioning, guidance, macro conditions, and management
> commentary rather than reported results alone.

## Checks before you save

- The window matches after-close-today plus next-before-open, with weekends and holidays
  correctly rolled.
- The event timing is confirmed and cited.
- Spot, implied move, and historical anchors are grounded, cited, and dated.
- Seven personas are present, or the missing seats are named explicitly.
- Every persona cites at least two evidence points where evidence exists.
- Bullish verdicts name what sinks the stock; bearish verdicts name what squeezes it.
- Reversal risk is presented separately from direction, nowhere blended into it.
- The estimated move is a signed point plus a right-skewed band — or an unsigned band
  only, if the gate fired.
- Header, `Prediction first` line, and synthesis packet agree on every number.
- No company-specific number appears without a source.

That last one is the one to actually verify rather than assume. Scan the finished
dossier for digits and confirm each traces to a citation.

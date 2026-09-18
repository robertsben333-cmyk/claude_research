# researcher_europe/LESSONS.md

What counts as a finding in these three markets, and how to size one. Read **after** you
have sized the day twice — once in English, once locally — and frozen both drafts. It
does not tell you where to look.

**Nothing in this file has been paid for by a resolved European run yet, because there
has not been one.** Every rule below is either (a) carried over from a resolved US or
Japanese run and marked as such, or (b) a defect this stage's own Phase 1 measurement
found in Europe specifically. When European runs resolve, `eu_resolve.py` and the
post-mortem replace these with measurement. A rule that costs rank correlation gets cut,
not argued for. That is the point of freezing `pre_lessons`: the file is scored.

---

## Europe-specific, measured in this stage's Phase 1

**The session is the single most load-bearing field and it is often a guess.** 339 of 379
UK results announcements landed before 08:00 London, so the default is `bmo` and the
window is one session. But the vendor calls the session unknown for 150 of 318 German and
238 of 346 French rows. Windowing an unknown row as pre-market **roughly halves the move**:
on the 2026-09-16 validation run Barratt Redrow moved +11.72% over the bmo window and
+1.78% over the amc one. If your baseline says `session_unresolved`, spend one search
settling it before you size anything. It is worth more than any finding you will make.

**`positioning.covered: false` is not a zero.** It means the register could not be read.
For France it is the normal case. A hunter that writes "no disclosed short position" into
`positioning_check` on a French name has invented a fact. Say "register not readable for
this market" and size your negative findings knowing you cannot see the crowding.

**Read the headline loosely and the URL strictly.** UK issuers headline results in
marketing language often enough to defeat a keyword filter — Trustpilot's 2026 interims
went out as "AI, Enterprise and US momentum fuel strong growth". Six of the eight apparent
calendar misses in Phase 1 were this, not the calendar. Conversely, search results relabel
old articles with today's year: read the date out of the URL path or the document.

**Four sources are shut and retrying them wastes calls.** Les Echos, Investir,
Boursier.com, Zonebourse and actusnews return 403 to both `curl` and `WebFetch`;
Sharecast, Proactive and the Investors' Chronicle return 403 to both; `www.data.gouv.fr`
resets the connection. Note them once in `searched_and_found_nothing` and route around.
The Japanese rule that `curl` beats `WebFetch` **does not hold on this path** — the two
mostly agree here — but trying the other tool once when one fails costs a single call and
occasionally works.

**The tail is intact, so do not size as if it were not.** None of these markets has a
daily price limit. Measured maxima were 42% (UK), 27% (Germany) and 52% (France), and the
median realised move was 2.81% / 3.12% / 4.19%. Tokyo's 値幅制限 truncates exactly the
events a hunt most wants credit for; here a large correct call can be paid in full.

**A German ad-hoc filed before the print may have pre-released the number.** MAR Article
17 is a continuous, timestamped channel separate from the results calendar, and a
`Prognoseanpassung` in the days before a print means most of the news is already out.
Porsche SE, Villeroy & Boch and Enapter all filed exactly that in one sampled week. Check
before sizing anything on the quarter. The French analogue is `information privilégiée`;
the UK's is an RNS trading update, which is where most of the UK's price-sensitive
information actually lands given the 217-day median gap between scheduled releases.

**Coverage tells you which regime you are in.** `consensus.analyst_band` is in your
baseline. At `>13` you are competing with sixteen to nineteen analysts and an English
search returns their preview. At `3-7` — the $1–5m turnover band — nobody is positioned
for a confirmed fact, which is the setup for a large move. This is the stage's thesis and
it is being tested, not assumed: do not let it change what you search for, only how you
size what you find.

---

## Carried over from resolved US and Japanese runs

These are marked because they were paid for elsewhere and have not been re-measured here.

**A verified fact is not a predicted reaction.** The most common failure is a right fact
and a wrong reaction: the print confirms the finding in every particular and the stock
moves the other way on the guide, on the quality of the beat, or on positioning. On one US
day three of the four largest longs had their thesis confirmed and lost double digits.
That is why `print_vs_bar_pct` and `expected_move_pct` are separate fields and are allowed
to disagree.

**Name the line a finding lands on.** Four US names on two days carried the same
tariff-refund thesis; the refund landed in all four; two rose double digits and two fell
double digits, split entirely by the direction of guidance. A `one_off` with no stated
path to the guide or the multiple is sized at a fraction of the same money as operating
profit.

**The hunter's own caveat has to reach the number.** One hunter wrote "an honest zero is a
very plausible result" and emitted +1.40. Another wrote that the negatives were items the
holders had demonstrably looked through and sized them −3.5 net. If `baseline_tension`
says the evidence cuts against the lean, `expected_move_pct` must be visibly smaller than
the sum of your findings and the note says by how much.

**Financing is a question, not a verdict.** A revolver, a term loan or a placing ahead of
the print was twice read as distress and sized as a large negative; one company was
funding a ramp that printed +70% revenue and a record backlog, the other posted record
revenue with 600 basis points of margin. Ask what the money buys and whether backlog,
bookings, inventory or hiring corroborate a ramp.

**A narrow proxy loses to a broad series.** A company-level number in a primary document
beats an industry proxy; a proxy that contradicts a broader public series loses to that
series; macro-to-company transmission is a hypothesis until the company or a direct
counterparty has said it. "The drawdown has no cause in the filings" is worth 0 — in a
small cap the filing record is not the information set.

**Keep findings inside the exit window.** A lock-up expiry, an exchange deadline or a
capital-markets day dated after the exit is real, sourceable and worth nothing to this
ranking. Once a US day carried 3.5 points of an 8-point spread on events the trade would
never see. Here the window is **one session** for a `bmo` name, which is shorter than
either other stage's — so this bites harder.

**Positioning is the thing to beat, not the thing to agree with.** A negative finding that
merely restates a crowded, building short is already in the price. A crowded short is
fuel: the US run watched two names with 18% and 23% of float short both squeeze more than
20%.

**Understatement is the hunters' systematic error.** On the best day in the US record,
eight of nine realised moves were larger than the hunter's number. Size on the name's own
reaction distribution, not on how certain you are of the fact.

**Net of the rest of the company.** A hunter was once correctly bearish on 44% of revenue
and silent on the 56% that grew 68%; total revenue cleared the bar it had called
unreachable.

**Two findings resting on one document are one finding.** And two findings that cannot
both be true are resolved by you, now — the key is a sum and nothing downstream detects a
contradiction.

---

## How this file grows

Only from a resolved run. `eu_resolve.py` gives the per-finding outcome and the
per-market, per-band breakdown; a rule earns a place here when a named run shows the error
it prevents, and loses it when `impact_sum_pre_lessons` out-ranks the published key over
several pooled days. Do not add a plausible rule. A file nobody can score accumulates
plausible rules forever.

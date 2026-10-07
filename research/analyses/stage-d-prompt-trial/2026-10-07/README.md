# Stage D prompt trial, 2026-10-07: the same three names under two versions

v1 is the morning run (`v1-run/`, moved here from `research/2026/10/2026-10-07/edge-deep/` so the live Routine starts with a clean day; its v2 re-run is `v2-hunts/`). v2 re-ran the same
names, blind to v1, after two changes: "priced" must be shown with a number and each
question names the bias that could keep the price behind; and, sent mid-run, at least one
non-analyst route per question (`approaches_tried`).

| name | v1 sum | v1 p_up | v1 decision | v2 sum | v2 p_up | v2 decision | v2 priced_shown |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PEP | -0.7 | 45 | no trade, medium | +0.3 | 52 | no trade, low | 3 of 4 |
| RGP | -0.8 | 48 | no trade, low | -1.3 | 44 | short, low | 2 of 4 |
| TLRY | -0.4 | 46 | no trade, low | -0.4 | 49 | no trade, low | 2 of 5 |

What it shows, before any print:

- **v2 was less certain the market had it.** 7 of 13 questions could not show the priced
  answer with a number, and each named a bias. RGP became the stage's first trade call.
- **The two versions disagree about as much as the change would move them.** The quick
  first reads, frozen before any research and so untouched by most of the change, differ
  too: PEP +0.3 against -0.6, RGP -2.0 against -1.0, TLRY +0.2 against -0.5. RGP's central
  FQ2 guide estimate was $100-104m in v1 and $94-98m in v2. Run-to-run noise is as large as
  the method effect, so three names cannot separate them.
- **A factual error.** v2 PEP took Brent at "$87-92 after the guide" from an August article.
  FRED: 76.50 on 2026-07-08, 130.80 on 2026-09-15, 113.96 on 2026-09-29. Sizing on the
  stale level is part of why v2 PEP turned positive. The addendum now says to read any
  series yourself to its latest point.
- v2 ran 10 to 15 minutes per name against 25 to 29 for v1.
- RGP v2 wrote its question-freeze time by hand (11:25 UTC) after its `date -u` pre_lessons
  stamp (11:19:45), so the label is wrong; the order of the freezes in its file is intact.

Both versions are scored after the prints (RGP tonight, PEP and TLRY tomorrow morning).
Never pool the two versions to judge either one.

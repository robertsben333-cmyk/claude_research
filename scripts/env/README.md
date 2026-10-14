# The Routines' cloud environment

Every research Routine on Xavier's account fires into the cloud environment **"full
env"** (`env_01HBKyy2ZpubuvsBDUY2onkn`), read back from the sessions of stages J, EU and
D on 2026-10-13/14. **A Routine created by hand in the Routines UI must be given "full env"
too** (for example the two stage E-PI Routines, "US - Intraday panel (:00)" and "(:30)");
they need nothing beyond what the setup script installs. Stage E and "Close AMC" live on another account, so their
environment is configured there and cannot be seen from here.

Three files keep that environment right:

| File | What it does |
| --- | --- |
| `scripts/env/setup.sh` | The text to paste into the environment's **Setup script**. Runs as root before the session, cached with the container. Self-contained: it does not read the repo. |
| `.claude/hooks/session-start.sh` | SessionStart hook, registered in `.claude/settings.json`. A fast import check that installs `requirements.txt` only on a miss, so a session is right even if the setup script was never pasted. Never fails the session. |
| `scripts/env/check.py` | Prints what is present (package versions, tools, env var NAMES, never values). `--strict` exits 1 on a missing requirement. The smoke test fails if `setup.sh` and `requirements.txt` drift apart. |

## Why it exists

`researcher_japan/scripts/jp_positioning.py` reads JPX's daily short register, an `.xls`
file, with `xlrd`. No container had `xlrd`, `parse()` raised, the loader swallowed the
error and served the last cached file, so all nine stage J runs from 2026-10-01 to 2026-10-14
sealed on the **2026-09-29** register without anything failing. With `xlrd` installed
the 2026-10-14 file parses (597 codes).

Several hunter definitions still say `pdftotext` is absent and `pypdf` dies on a broken
`cryptography` module. In "full env" on 2026-10-14 both work. Those lines were left
alone on purpose: editing a hunter definition is a new prompt version.

## Settings to enter by hand

Project settings → Cloud environment → gear beside **full env**:

- **Setup script:** the contents of `scripts/env/setup.sh`.
- **Network access:** keep the current level (full). The stages fetch from many hosts
  (Yahoo, Nasdaq, SEC EDGAR, JPX, TDnet, ASX, ASIC, TMX, m-x.ca, FCA, AMF, EQS,
  Nasdaq Nordic, Oslo Børs, Borsa Italiana, Google Trends, plus open WebFetch by the
  hunters), so an allow-list would silently cut sources.
- **Environment variables:** none are needed on this account; nothing here places
  orders. On stage E's account: `ALPACA_API_KEY_ID`, `ALPACA_API_SECRET_KEY` (and
  optionally `ALPACA_BASE_URL`). `FMP_API_KEY` / `FINNHUB_API_KEY` are optional
  fallbacks for `scripts/get_earnings.py`.

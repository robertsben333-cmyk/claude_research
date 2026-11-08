# Stage EU executor (the operator's server)

IBKR gives OAuth to institutional clients only, so an individual account reaches the
API through a logged-in IB Gateway. This folder is what runs on the operator's own
always-on Ubuntu server next to that gateway. See `../EXECUTION.md` for the whole route.

| file | what |
| --- | --- |
| `install.sh` | one-off install: Java (Azul Zulu 17 FX on ARM), IB Gateway stable, IBC, a checkout of this repo, a Python venv with `ib_async`, `/etc/eu-executor.env`, the `ibgateway` service and two weekday timers |
| `eu_executor.py` | `flatten` (15:35 Amsterdam), `open` (from 16:00, waits for today's `<RUN>/ibkr-handoff.json` on main, gives up 17:30), `check`, `status`; logs in `~/eu-executor/logs/`, optionally pushed to branch `eu-ibkr-log` |
| `INSTALL_PROMPT.md` | a prompt for a Claude session on the operator's computer that walks through the install |

## Install, in short

1. A dedicated IBKR account with its **own username**, its paper account (`DU...`), and
   IBKR Mobile on the phone for the login confirmation.
2. An Ubuntu 22.04/24.04 server, 1 GB of memory or more (Oracle Cloud Always Free ARM,
   4 cores / 24 GB, region Amsterdam or Frankfurt; upgrade the account to Pay As You Go
   so an idle free server is not reclaimed).
3. A GitHub fine-grained token for `robertsben333-cmyk/claude_research` only: Contents
   read, or read and write to push the daily log to `eu-ibkr-log`.
4. On the server:
   ```bash
   curl -fsSL -H "Authorization: Bearer <TOKEN>" \
     https://raw.githubusercontent.com/robertsben333-cmyk/claude_research/main/researcher_europe/executor/install.sh -o install.sh
   bash install.sh
   ```
   It asks for the IBKR username and password (typed on the server, stored only in
   `~/ibc/config.ini`, mode 600), paper or live, the account number and the token.
5. Approve the login on the phone, then
   `~/eu-executor/venv/bin/python ~/eu-executor/claude_research/researcher_europe/executor/eu_executor.py check`.

## Day to day

- `systemctl list-timers 'eu-*'`: the next flatten and open.
- `journalctl -u ibgateway -f`, `~/ibc/logs/`: the gateway and IBC.
- `~/eu-executor/logs/<date>.log`: what the executor did.
- About once a week (Sunday) IBKR sends a login confirmation to the phone; until it is
  approved the gateway is logged out and the next run's `check` fails and nothing trades.
- To stop trading: `enabled: false` on main, or
  `sudo systemctl disable --now eu-flatten.timer eu-open.timer`.

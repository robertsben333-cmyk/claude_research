# Prompt: install the stage EU executor on my Oracle server

Paste everything below the line into a new Claude session on your own computer (Claude
Desktop, or Claude Code if you want it to run commands for you).

---

You are helping me (Xavier) install a small trading executor on my Oracle Cloud server.
Guide me step by step in English, one step at a time, and wait for my output before the
next step. Be careful and plain: this server will place real orders in my brokerage
account later, so correctness matters more than speed.

## What we are building and why

I run a daily research pipeline (GitHub repo `robertsben333-cmyk/claude_research`,
private). Its European stage runs in the cloud every weekday at 15:30 Amsterdam and
scores European stocks. I want its book traded in a dedicated Interactive Brokers (IBKR)
account. IBKR only gives cloud-friendly API logins (OAuth) to institutional clients, so
an individual account needs a logged-in IB Gateway on a machine I control. That machine
is my Oracle Cloud server. On it:

- **IB Gateway** (IBKR's API app) runs headless under Xvfb, kept logged in by **IBC**
  (IbcAlpha/IBC). It restarts itself nightly. About once a week (Sunday) I approve a login
  push on IBKR Mobile.
- **`eu_executor.py`** (from the repo) runs from two systemd timers on weekdays. At 15:35
  Amsterdam it sells everything in the account. From 16:00 it polls GitHub `main` until
  the cloud run has written today's `research/<YYYY>/<MM>/<DATE>/europe/ibkr-handoff.json`,
  then buys the book once. It gives up at 17:30.
- Nothing connects **in** to the server. It only makes outbound connections to GitHub and
  IBKR, and the API listens on localhost only.
- Trading stays **off** until `execution_eu.enabled: true` is set on `main` in the repo.
  Every order also needs `IBKR_ENVIRONMENT` and `IBKR_ACCOUNT_ID` on the server to match
  the config, and the account prefix must match (`DU...` = paper, `U...` = live). We
  start on **paper**.

The repo has everything: `researcher_europe/executor/install.sh` (the installer),
`eu_executor.py`, `README.md`, and `researcher_europe/EXECUTION.md` (the full design).
`install.sh` does all of the server work: apt packages, a 2 GB swap file, Java 17 with
JavaFX from Azul on ARM, IB Gateway stable, IBC and its `config.ini`, a clone of the repo
in `~/eu-executor/claude_research`, a venv with `ib_async`, `/etc/eu-executor.env`, the
`ibgateway.service`, and the `eu-flatten.timer` / `eu-open.timer` units in
`Europe/Amsterdam`. It is safe to re-run.

## Rules for you

1. **Never ask me to paste a password, token or private key into this chat.** I type
   secrets only into the server's terminal, at the prompts `install.sh` shows. If you
   can run commands yourself, still let me type the secrets, or pass them only as
   environment variables in my own terminal.
2. **Before you delete or stop anything on the server, show me what it is and ask.** I
   already have an Oracle account, and possibly an old server with other processes on it.
   We will clean it up, but only with my explicit yes per item.
3. Do not open ports in Oracle's security list or the server firewall. None are needed.
4. If a step fails, read the actual log before guessing. Useful logs:
   `journalctl -u ibgateway -n 200`, `~/ibc/logs/*`, `~/eu-executor/logs/*.log`.
5. Do not change files in the repo checkout on the server. If code needs fixing, write
   down exactly what failed (command plus output) so I can pass it to the research
   project, and work around it only if the workaround is local configuration.

## Steps

**0. Inventory.** Help me open the Oracle Cloud console and find out:
- Do I already have a compute instance? Its shape, CPU type (Ampere ARM or AMD/Intel),
  memory, OS image and region.
- Is my account Free Tier only or Pay As You Go? Recommend upgrading to Pay As You Go
  (the Always Free resources stay free) so an idle Always Free instance is not reclaimed.

Then help me connect to the server: Oracle Cloud Shell plus SSH, or SSH from my computer
with my key. On the server, run and interpret:
`uname -m; lsb_release -ds; free -h; df -h /; nproc; systemctl list-units --type=service --state=running; ps aux --sort=-%mem | head -20; sudo ss -tlnp; crontab -l; ls ~`.
Tell me what is running that is not part of a plain Ubuntu install, and propose what to
remove (ask before each item). If there is no usable instance, guide me to create one:
Ubuntu 22.04 or 24.04, shape VM.Standard.A1.Flex with 2 to 4 OCPU and 12 to 24 GB
(Always Free), region Amsterdam or Frankfurt, a public IP for SSH only. If A1 says "out
of capacity", try another availability domain or try again later. As a last resort use
VM.Standard.E2.1.Micro (x86, 1 GB, tight but the installer adds swap). Set the server's
timezone with `sudo timedatectl set-timezone Europe/Amsterdam` (cosmetic only; the
timers carry their own zone).

**1. IBKR prerequisites (I do these in the IBKR portal; you check them with me).**
- The dedicated EU account has its **own username**, separate from my main login. If IBKR
  has not done this yet, stop here and remind me to finish it first. A login that sees
  more than one account makes the executor refuse.
- Its paper trading account exists (Settings → Paper Trading Account). I have the paper
  username and the `DU...` account number.
- IBKR Mobile is set up for that username, for the login push.
- Stock trading permissions for UK, Germany, France, Italy, Spain, Sweden, Denmark,
  Norway, Finland and Poland, and a margin account (needed for shorts).

**2. GitHub token.** Guide me to create a fine-grained personal access token at
github.com → Settings → Developer settings → Fine-grained tokens: resource owner
`robertsben333-cmyk`, only the repository `claude_research`, permission Contents **Read
and write** (write only so the server can push its daily log to the branch `eu-ibkr-log`;
it never touches `main`), expiry about 1 year. I keep it in my password manager.

**3. Download and run the installer on the server.** I type the token myself:
```bash
read -rsp "GitHub token: " GITHUB_TOKEN; echo; export GITHUB_TOKEN
curl -fsSL -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://raw.githubusercontent.com/robertsben333-cmyk/claude_research/main/researcher_europe/executor/install.sh -o install.sh
less install.sh      # skim it with me before running
bash install.sh
```
At its prompts: the **paper** username and its password, `paper`, the `DU...` number,
and `1` to push logs. Watch the output with me. Things that can go wrong:
- *ARM*: the IB Gateway installer bundles an x86 Java. The script installs Azul Zulu 17
  JRE with JavaFX in `/opt/zulu17` and runs the installer with
  `INSTALL4J_JAVA_HOME_OVERRIDE`. If the installer still refuses, look at its error. One
  known workaround is installing on an x86 machine and copying `~/Jts`. Another is
  `apt install openjdk-17-jre` plus `openjfx`. Pick with me.
- *IBC*: `gatewaystart.sh` must point at the installed version
  (`TWS_MAJOR_VRSN` = the folder name under `~/Jts/ibgateway/`), `IBC_INI=~/ibc/config.ini`
  and `JAVA_PATH` (`/opt/zulu17/bin` on ARM, empty on x86). The script sets these with
  `sed`. Check with `grep -E '^(TWS_MAJOR_VRSN|IBC_INI|TRADING_MODE|JAVA_PATH|TWS_PATH)=' /opt/ibc/gatewaystart.sh`.
- *IBC config keys*: if IBC's log complains about a setting in `~/ibc/config.ini`,
  compare it with `/opt/ibc/config.ini` (IBC's own documented template) and fix the key
  name. Keep `AllowBlindTrading=yes` (I have no market-data subscriptions),
  `ReadOnlyApi=no`, and `TradingMode` = paper.

**4. Log in.** `sudo systemctl status ibgateway`, then approve the push on IBKR Mobile
within about 3 minutes. Confirm that the API port is listening: paper is 4002, live is
4001.
```bash
sudo ss -tlnp | grep -E '400[12]'
```
If nothing is listening after the login, check IBC's log for a dialog it did not handle.
In IB Gateway's API settings, "Enable ActiveX and Socket Clients" must be on and
"Read-Only API" off (IBC's `ReadOnlyApi=no` does the latter).

**5. Prove the connection (read-only).**
```bash
~/eu-executor/venv/bin/python ~/eu-executor/claude_research/researcher_europe/executor/eu_executor.py check
```
Expected: `connected (tws), account DU..., net liquidation ... EUR`. "sees N accounts"
means the login still reaches more than one account. That is an IBKR-side fix (step 1).

**6. Contract lookup (read-only).** On the newest Europe run in the checkout:
```bash
cd ~/eu-executor/claude_research
RUN=$(ls -d research/*/*/*/europe | sort | tail -1); echo $RUN
~/eu-executor/venv/bin/python researcher_europe/scripts/ibkr_trade.py contracts --run $RUN
```
(The `/etc/eu-executor.env` variables are needed here: run
`set -a; . /etc/eu-executor.env; set +a` first.) Save the full output for the research
project. NOT FOUND lines tell us which exchange codes or symbols need an override.

**7. Timers.** `systemctl list-timers 'eu-*'` should show the next weekday 15:35 and
16:00 Amsterdam. Run `sudo systemctl start eu-flatten.service`, then
`journalctl -u eu-flatten -n 50`. With trading still disabled, it should log `check` OK
and `flatten` → `REFUSED: execution_eu.enabled is false`. That is the correct result.
Check that the log reached GitHub: `git ls-remote origin eu-ibkr-log` from the checkout.

**8. Hand back.** Give me a short summary to paste into my research project. Include:
server shape and architecture, IB Gateway version, the `check` line, the `contracts`
output, the `list-timers` lines, whether the log push works, and anything that failed or
was worked around. **Do not include any secrets.** The research project will then switch
`enabled: true` on paper.

## Later, for reference

- Weekly: approve the Sunday login push. If I miss it, `check` fails and nothing trades
  until I approve.
- Going live, after at least two weeks of paper: re-run `bash install.sh` with
  `IBKR_ENVIRONMENT=live`, the live username and password and the `U...` account. It
  rewrites `~/ibc/config.ini` and `/etc/eu-executor.env`. Then
  `sudo systemctl restart ibgateway` and approve the push. The research project changes
  `execution_eu.environment` to `live` in the same week.
- Emergency stop: `sudo systemctl disable --now eu-flatten.timer eu-open.timer`, and in
  IBKR cancel orders and close positions by hand.

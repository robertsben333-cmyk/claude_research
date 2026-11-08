# Stage EU at Interactive Brokers

Since 2026-11-08 (operator's instruction) the EU Routine can trade its own panel book in a
dedicated IBKR account: **sell everything at the start of the run** (skill step 0s),
**buy the panel's names at the end** (step 6b). One script does both,
`researcher_europe/scripts/ibkr_trade.py`, on top of `ibkr_client.py`. It is committed
switched off (`execution_eu.enabled: false`, `environment: paper`).

**The EU panel has no measured edge yet.** The 2026-10-21 study put it at rho +0.22,
p 0.19 over 45 live names on 7 days, with four names at or above 70. Trading it is a way
to find out, with money at risk, not the use of a finding.

## The day

| CET | step | what happens |
| --- | --- | --- |
| 15:30 | fire | Routine starts, heartbeat |
| ~15:35 | 0s `flatten` | cancel working orders, sell/cover every position (collared DAY limits), wait 2 min, log what is still held |
| 15:35-16:20 | 1-6 | universe, baselines, hunters, panel, note, publish (measured: 40-45 min on 2026-11-03 to 11-06) |
| ~16:20 | 6b `open` | buy/short names with `panel_pct` >= 70 and four judges, collared DAY limits |
| 16:25-17:35 | | markets close; Oslo at 16:25 local, so Oslo names are usually skipped |

So a position is held from about an hour before the close of D-1 to about two hours
before the close of D. The scored window is close(D-1) to close(D); the trade carries the
morning reaction and misses the last hour or two of each day. A Friday book is held over
the weekend.

## The rule (`execution_eu` in `config/pipeline.yaml`)

- **Entry**: `panel_pct` >= 70 with all four judges; side from the panel; turnover at
  least $200k a day; market open for more than 10 more minutes.
- **Weight**: `panel_pct` - 60, linear, at most 50% of equity a name; what a capped name
  cannot take goes to the others (`alpaca_trade.allocate`, the same code as stage E-P).
- **Budget**: 100% of net liquidation minus anything still held.
- **Hard limits**, checked again right before each order: `max_gross_base` 10,000,
  `max_name_base` 5,000 (account base currency), `max_names` 6, `max_orders_per_run` 20,
  and a name is dropped when IBKR's price is more than 20% from the sealed spot (that
  means the contract lookup is wrong).
- **Orders**: DAY limits 1% through the price for entries, 2% for exits. An unfilled
  remainder works until that market's close and expires.

## Four switches, all needed to send an order

1. `execution_eu.enabled: true` in the config (a PR to `main`).
2. `--submit` on the command (the skill passes it).
3. `IBKR_ENVIRONMENT` in the Routine's environment equal to `execution_eu.environment`.
4. `IBKR_ACCOUNT_ID` naming an account the login can see, `DU...` on paper and `U...`
   on live, and the login seeing no other account.

Turning trading off is one line: `enabled: false`. Removing the variables also stops it.

## Why OAuth and not a gateway

IBKR's usual API needs TWS, IB Gateway or the Client Portal Gateway running and logged
in, with two-factor login at least weekly. A Routine is a fresh cloud container every
day, so it cannot hold a login. The options, plainly:

| route | what it takes | risk |
| --- | --- | --- |
| **First-party OAuth 1.0a (chosen)** | one-off key registration in IBKR's self-service portal; six secrets in the Routine's environment | the signing is ours and tested only against a simulated server until the first paper `check`; IBKR says individual accounts need IBKR Pro and a funded live account even for paper |
| Self-hosted gateway | a small always-on server running IB Gateway/IBC or the Client Portal Gateway behind TLS and a token, weekly 2FA re-login | an internet-facing login to a real-money account; a second system to keep alive |
| Another broker with plain API keys | Trading 212 has key-based API access but no short selling; Saxo has OAuth with refresh tokens | a different account, and the long/short book would lose its shorts or need new code |

`ibkr_client.py` supports the gateway too (`execution_eu.auth: gateway`,
`IBKR_GATEWAY_URL`), so the second route needs no new trading code if OAuth fails.

`api.ibkr.com` answered from the cloud on 2026-11-08 (HTTP 401 without credentials, as
it should).

## Setup, step by step

1. **The account.** Open the new account as IBKR Pro, margin (shorts need margin), base
   currency EUR, with its **own username**. Do not link it into your existing login: if
   one login can see two accounts, `ibkr_trade.py` refuses to run. Turn on stock trading
   permissions for the UK, Germany, France, Italy, Spain, Sweden, Denmark, Norway,
   Finland and Poland. Fund it.
2. **The paper account.** In that account's portal, Settings, Paper Trading Account:
   create it and note the paper username and the `DU...` account number.
3. **Keys, on your own computer** (never in the chat, never in the repo):
   ```bash
   openssl genrsa -out private_signature.pem 2048
   openssl rsa -in private_signature.pem -pubout -out public_signature.pem
   openssl genrsa -out private_encryption.pem 2048
   openssl rsa -in private_encryption.pem -pubout -out public_encryption.pem
   openssl dhparam -out dhparam.pem 2048
   ```
4. **Register.** Log in to IBKR's OAuth self-service portal **with the paper username**
   (search "IBKR OAuth self-service portal"; the community guides use
   `ndcdyn.interactivebrokers.com/sso/Login?action=OAUTH&RL=1&ip2loc=US`). Choose a
   nine-character consumer key, upload `public_signature.pem`, `public_encryption.pem`
   and `dhparam.pem`, and generate the access token and access token secret. **The keys
   only start working after IBKR's next overnight maintenance**, so test the day after.
5. **A separate cloud environment for the EU Routine.** Copy "full env" to a new
   environment (for example "EU trading env") so no other Routine sees these secrets.
   Add:

   | variable | value |
   | --- | --- |
   | `IBKR_OAUTH_CONSUMER_KEY` | the nine characters |
   | `IBKR_OAUTH_ACCESS_TOKEN` | from the portal |
   | `IBKR_OAUTH_ACCESS_TOKEN_SECRET` | from the portal |
   | `IBKR_OAUTH_SIGNATURE_KEY` | `base64` of `private_signature.pem` |
   | `IBKR_OAUTH_ENCRYPTION_KEY` | `base64` of `private_encryption.pem` |
   | `IBKR_OAUTH_DH_PARAM` | `base64` of `dhparam.pem` |
   | `IBKR_ACCOUNT_ID` | `DU...` |
   | `IBKR_ENVIRONMENT` | `paper` |

   `base64 -w0 file.pem` on Linux, `base64 -i file.pem | tr -d '\n'` on a Mac. Then point
   the EU Routine at the new environment in the Routines page.
6. **Allow the script in auto mode.** Add
   `"Bash(python3 researcher_europe/scripts/ibkr_trade.py:*)"` to `permissions.allow` in
   `.claude/settings.json` on `main`. A session in auto mode is not allowed to write that
   file itself, and without it the classifier can refuse the broker calls (stage E lost
   ten days of orders to exactly that, 2026-09-28 to 10-07).
7. **First proof, still switched off.** The next EU fire runs `check` at step 0s, which
   only reads: it logs in, finds the account and prints equity and positions into the
   run log. `flatten` and `open` refuse because `enabled` is false.
8. **Paper trading.** When `check` works, set `enabled: true` (environment stays
   `paper`). Run at least two weeks; compare the fills in `<RUN>/ibkr-orders.json` with
   the scorebord.
9. **Live.** Register again in the portal **with the live username** (new keys), replace
   the secrets, set `IBKR_ACCOUNT_ID=U...` and `IBKR_ENVIRONMENT=live`, and change
   `execution_eu.environment` to `live` in a PR. Raise `max_gross_base` only on purpose.

## Costs that a paper account hides

- UK stamp duty 0.5% on every UK purchase (not on a short); French FTT 0.4% and Spanish
  FTT 0.2% on purchases of large caps; Italian FTT 0.2% on positions held overnight. On a
  long that is held one day these are the same size as the expected edge.
- IBKR commissions in Europe are about 0.05% with a minimum per order (roughly EUR 1.25
  to 3 depending on the market), so a EUR 500 position pays a large share in minimums.
- Holding GBP, SEK, DKK, NOK and PLN positions from a EUR account creates negative
  currency balances (interest) and leaves positive ones after the sell. Convert now and
  then, or ask for this to be automated.
- Paper fills are simulated against quotes and are kinder than real fills in thin names.

## What is not verified yet

- The OAuth signing against IBKR's real server (only the simulated exchange in
  `smoke_test.py`). `check` on paper settles it.
- IBKR's exchange codes for Copenhagen and Helsinki (`DEFAULT_EXCHANGES`); `contracts
  --run <RUN>` lists every resolution and `execution_eu.exchanges` / `conid_overrides`
  correct it.
- Whether IBKR quotes London in pence or pounds through this API; the code detects it
  from the ratio to the sealed spot and refuses a London name when it cannot tell.
- Whether IBKR's snapshot returns prices without European market-data subscriptions;
  without one the code falls back to Yahoo (about 15 minutes delayed) for non-UK names.

This is research, not investment advice.

# Earnings universe — 2026-08-25

**Window:** After the US close on Tuesday 25 August 2026 through before the US open on Wednesday 26 August 2026
**Generated:** 2026-08-25T05:18:41+00:00 UTC
**Status:** `ok`
**Source:** after-close `nasdaq` · before-open `nasdaq`

**Counts:** 14 after-close + 19 before-open = **33** total; 26 above the $500,000,000 market-cap floor; **23 eligible** after qualification.

Session timing came from a single source (nasdaq) for both sides of the window; no
second-source cross-check was run given the size of the eligible set, so timing
confidence here is single-sourced rather than cross-verified — no conflicts were
surfaced during the manual options-market checks below. Options-market qualification
for smaller-cap/foreign-ADR/fund names was verified via WebSearch rather than assumed:
JOYY, TRMD, SFL, TIGR, QFIN, JKS all confirmed to have active listed-options chains
across Nasdaq/Yahoo/Barchart/Investing.com/OptionCharts; FSCO (a closed-end BDC fund)
and HDL (Super Hi International, Dec-2024 IPO) had no confirmed live options chain on
any platform checked and are excluded as `no_options_market`. `HEI.A` is Heico's
Class A share class reporting the same earnings event already captured by `HEI` and is
excluded as a duplicate to avoid double-counting one event downstream.

## Eligible

| Ticker | Company | Session | Event date | Market cap | EPS est. | Quarter |
| --- | --- | --- | --- | ---: | ---: | --- |
| `INTU` | Intuit Inc. | AMC | 2026-08-25 | $100.39B | $2.12 | Jul/2026 |
| `HEI` | Heico Corporation | AMC | 2026-08-25 | $49.61B | $1.51 | Jul/2026 |
| `ZM` | Zoom Communications, Inc. | AMC | 2026-08-25 | $31.50B | $1.01 | Jul/2026 |
| `WSM` | Williams-Sonoma, Inc. | BMO | 2026-08-26 | $27.97B | $2.05 | Jul/2026 |
| `SJM` | The J.M. Smucker Company | BMO | 2026-08-26 | $13.29B | $2.21 | Jul/2026 |
| `LI` | Li Auto Inc. | BMO | 2026-08-26 | $11.86B | ($0.01) | Jun/2026 |
| `DY` | Dycom Industries, Inc. | BMO | 2026-08-26 | $11.80B | $4.36 | Jul/2026 |
| `SMTC` | Semtech Corporation | AMC | 2026-08-25 | $11.56B | $0.41 | Jul/2026 |
| `DCI` | Donaldson Company, Inc. | BMO | 2026-08-26 | $10.81B | $1.12 | Jul/2026 |
| `ANF` | Abercrombie & Fitch Company | BMO | 2026-08-26 | $4.84B | $1.95 | Jul/2026 |
| `BOX` | Box, Inc. | AMC | 2026-08-25 | $4.56B | $0.09 | Jul/2026 |
| `BBWI` | Bath & Body Works, Inc. | BMO | 2026-08-26 | $3.92B | $0.24 | Jul/2026 |
| `JOYY` | JOYY Inc. | AMC | 2026-08-25 | $3.81B | $0.85 | Jun/2026 |
| `TRMD` | TORM plc | BMO | 2026-08-26 | $3.22B | n/a | Jun/2026 |
| `NCNO` | nCino, Inc. | AMC | 2026-08-25 | $2.26B | $0.11 | Jul/2026 |
| `KSS` | Kohl's Corporation | BMO | 2026-08-26 | $2.00B | $0.55 | Jul/2026 |
| `PLAB` | Photronics, Inc. | BMO | 2026-08-26 | $1.80B | $0.40 | Jul/2026 |
| `SFL` | SFL Corporation Ltd | BMO | 2026-08-26 | $1.65B | n/a | Jun/2026 |
| `QFIN` | Qfin Holdings, Inc. | AMC | 2026-08-25 | $1.41B | $0.96 | Jun/2026 |
| `TIGR` | UP Fintech Holding Limited | BMO | 2026-08-26 | $0.95B | n/a | Jun/2026 |
| `JKS` | JinkoSolar Holding Company Limited | BMO | 2026-08-26 | $0.83B | ($0.75) | Jun/2026 |
| `MOV` | Movado Group Inc. | BMO | 2026-08-26 | $0.77B | $0.36 | Jul/2026 |
| `NOAH` | Noah Holdings Ltd. | AMC | 2026-08-25 | $0.59B | n/a | Jun/2026 |

## Excluded

| Ticker | Company | Session | Event date | Market cap | Reason |
| --- | --- | --- | --- | ---: | --- |
| `HEI.A` | Heico Corporation | AMC | 2026-08-25 | $49.61B | duplicate_share_class (same earnings event as HEI) |
| `FSCO` | FS Credit Opportunities Corp. | AMC | 2026-08-25 | $1.03B | no_options_market |
| `HDL` | SUPER HI INTERNATIONAL HOLDING LTD. | BMO | 2026-08-26 | $0.91B | no_options_market |
| `DSC` | DSC Holdings Ltd. | BMO | 2026-08-26 | $0.43B | below_market_cap_floor |
| `STRT` | Strattec Security Corporation | AMC | 2026-08-25 | $0.34B | below_market_cap_floor |
| `ELMD` | Electromed, Inc. | AMC | 2026-08-25 | $0.33B | below_market_cap_floor |
| `ZH` | Zhihu Inc. | BMO | 2026-08-26 | $0.29B | below_market_cap_floor |
| `QMLS` | QumulusAI, Inc. | AMC | 2026-08-25 | $0.19B | below_market_cap_floor |
| `LANV` | Lanvin Group Holdings Limited | BMO | 2026-08-26 | $0.13B | below_market_cap_floor |
| `LITB` | LightInTheBox Holding Co., Ltd. | BMO | 2026-08-26 | $0.06B | below_market_cap_floor |

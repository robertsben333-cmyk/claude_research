"""EU panel study 2 (2026-11-05): one row per panel-scored live name, 2026-10-12 ..
2026-11-05, with panel numbers, baseline attributes, a Corwin-Schultz spread estimate
and prices at a grid of entry and exit times. Read-only on every live run.

Panel numbers: the live edge-scores-panel.json, except 10-12..10-14 whose live files
predate panel_pct and are taken from the dry-run rescore of the first study (PR #42).
Kills and sessions: resolved/<day>.json, stage EU's own resolver with the Nordic fix.
Prices: Yahoo 1d (6mo) and 5m (60d), cached in cache/ (not committed).
"""
import json, subprocess, time, glob, math
from datetime import datetime, date, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

S = Path(__file__).resolve().parent
REPO = S.parents[2]
CACHE = S / 'cache'; CACHE.mkdir(exist_ok=True)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0'
UTC = timezone.utc
NOW = datetime.now(UTC)


def fetch(sym, interval, rng):
    f = CACHE / f'{sym}_{interval}_{rng}.json'
    if f.exists():
        return json.loads(f.read_text())
    url = (f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}'
           f'&interval={interval}&includePrePost=false')
    for i in range(4):
        out = subprocess.run(['curl', '-sS', '--max-time', '40', '-H', f'User-Agent: {UA}', url],
                             capture_output=True, text=True).stdout
        try:
            r = json.loads(out)['chart']['result'][0]
            f.write_text(json.dumps(r))
            return r
        except Exception:
            time.sleep(2 * (i + 1))
    return None


def bars(r):
    if not r or 'timestamp' not in r:
        return []
    tz = ZoneInfo(r['meta'].get('exchangeTimezoneName') or 'UTC')
    q = r['indicators']['quote'][0]
    out = []
    for i, t in enumerate(r['timestamp']):
        o, c = q['open'][i], q['close'][i]
        if c is None:
            continue
        h, l = q['high'][i], q['low'][i]
        out.append({'t': datetime.fromtimestamp(t, UTC), 'loc': datetime.fromtimestamp(t, tz),
                    'o': o if o is not None else c, 'c': c, 'h': h if h is not None else c,
                    'l': l if l is not None else c, 'v': q['volume'][i] or 0})
    return out


def corwin_schultz(daily):
    """Mean Corwin-Schultz full spread (percent of price) over consecutive day pairs,
    negatives set to zero. A floor-ish estimate from highs and lows, not a quote."""
    k = 3 - 2 * math.sqrt(2)
    out = []
    for a, b in zip(daily, daily[1:]):
        if min(a['l'], b['l']) <= 0:
            continue
        beta = math.log(a['h'] / a['l']) ** 2 + math.log(b['h'] / b['l']) ** 2
        g = math.log(max(a['h'], b['h']) / min(a['l'], b['l'])) ** 2
        alpha = (math.sqrt(2 * beta) - math.sqrt(beta)) / k - math.sqrt(g / k)
        s = 2 * (math.exp(alpha) - 1) / (1 + math.exp(alpha))
        out.append(max(s, 0.0))
    return round(100 * sum(out) / len(out), 3) if out else None


def session_open_local(t0):
    z = str(t0.tzinfo)
    hh = 8 if 'London' in z else 9
    return t0.replace(hour=hh, minute=0, second=0, microsecond=0)


def prices(sym, entry_utc, d_event, session):
    daily_all = bars(fetch(sym, '1d', '6mo'))
    # A daily bar for today is only final after the close; treat today as incomplete
    # unless the 5m tape shows the session ended.
    m5 = bars(fetch(sym, '5m', '60d'))
    today = NOW.date()
    daily = [b for b in daily_all if b['loc'].date() < today or NOW.hour >= 17]
    if not daily:
        return None
    days = [b['loc'].date() for b in daily]
    try:
        iD = next(i for i, d in enumerate(days) if d >= d_event)
    except StopIteration:
        return {'pending': True}
    if days[iD] != d_event:
        return {'no_bar_on_event_day': str(days[iD])}
    iR = iD + (1 if session == 'amc' else 0)
    if iR >= len(daily):
        return {'pending': True}
    R = days[iR]
    p = {'R': str(R), 'close_Rm1': daily[iR - 1]['c'], 'close_R': daily[iR]['c'],
         'open_R_daily': daily[iR]['o'], 'high_R': daily[iR]['h'], 'low_R': daily[iR]['l']}
    for k in (1, 2, 5):
        p[f'close_Rp{k}'] = daily[iR + k]['c'] if iR + k < len(daily) else None
    pre = daily[max(0, iR - 21):iR - 1]
    p['cs_spread_pct'] = corwin_schultz(pre)
    if not m5:
        return p
    tz = m5[0]['loc'].tzinfo
    eday = entry_utc.astimezone(tz).date()
    p['entry_day'] = str(eday)
    dd = [b for b in daily if b['loc'].date() == eday]
    p['close_entry_day'] = dd[0]['c'] if dd else None
    eb = [b for b in m5 if b['loc'].date() == eday]
    pre = [b for b in eb if b['t'] + timedelta(minutes=5) <= entry_utc + timedelta(minutes=5) and b['t'] <= entry_utc]
    p['entry_panel'] = pre[-1]['c'] if pre else None
    p['entry_panel_bar'] = pre[-1]['loc'].isoformat() if pre else None
    if eb:
        so = session_open_local(eb[0]['loc'])
        for lab, mins in (('entry_last60', -60), ('entry_last30', -30)):
            # minutes before the official close: 16:30 London, 17:30 continent
            close_loc = so.replace(hour=16 if 'London' in str(tz) else 17, minute=30)
            cut = close_loc + timedelta(minutes=mins)
            bb = [b for b in eb if b['loc'] + timedelta(minutes=5) <= cut]
            p[lab] = bb[-1]['c'] if bb else None
    rb = [b for b in m5 if b['loc'].date() == R]
    p['n5m_R'] = len(rb)
    if rb:
        p['open_R'] = rb[0]['o']
        p['first_bar_R'] = rb[0]['loc'].isoformat()
        so = session_open_local(rb[0]['loc'])
        for lab, mins in (('R_15m', 15), ('R_30m', 30), ('R_60m', 60), ('R_120m', 120),
                          ('R_240m', 240), ('R_360m', 360)):
            cut = so + timedelta(minutes=mins)
            bb = [b for b in rb if b['loc'] + timedelta(minutes=5) <= cut]
            p[lab] = bb[-1]['c'] if bb else None
        # volume share of the first 30 minutes, a liquidity read
        v = sum(b['v'] for b in rb)
        p['vol_share_first30'] = (sum(b['v'] for b in rb if b['loc'] < so + timedelta(minutes=30)) / v) if v else None
    return p


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    rows = []
    bench = {}
    for run in sorted(glob.glob(str(REPO / 'research/2026/1*/*/europe'))):
        day = run.split('/')[-2]
        pf = Path(run, 'edge-scores-panel.json')
        if not pf.exists():
            continue
        alt = S / 'rescore' / day / 'edge-scores-panel.json'
        pan = json.loads((alt if alt.exists() else pf).read_text())
        prov = json.loads(Path(run, 'provenance.json').read_text())
        pstamp = datetime.fromisoformat(prov['panel']['stamped_utc'])
        hv = sorted({h.get('prompt_version') for h in prov['hunters'].values()})
        res = {}
        rf = S / 'resolved' / f'{day}.json'
        if rf.exists():
            res = {r['ticker']: r for r in json.loads(rf.read_text())['rows']}
        hs = {x['ticker']: x for x in json.loads(Path(run, 'edge-scores.json').read_text()).get('ranking', [])}
        for r in pan['ranking']:
            tk = r['ticker']
            bl = json.loads(Path(run, 'baselines', f'{tk}.json').read_text())
            rr = res.get(tk, {})
            sess = rr.get('session') or bl.get('session') or 'bmo'
            tape = bl.get('tape') or {}
            cons = bl.get('consensus') or {}
            x = {'day': day, 'ticker': tk, 'company': bl.get('company'),
                 'submarket': bl.get('submarket'), 'industry': bl.get('industry'),
                 'session': sess, 'session_source': rr.get('session_source'),
                 'turnover_usd': tape.get('median_turnover_usd_20d'),
                 'analyst_count': cons.get('analyst_count'), 'analyst_band': cons.get('analyst_band'),
                 'anchor_covered': bl.get('anchor_covered'),
                 'history_basis': (bl.get('history') or {}).get('basis'),
                 'vol20': tape.get('realised_vol_20d_pct'), 'run_up_20d': tape.get('run_up_20d_pct'),
                 'run_up_5d': tape.get('run_up_5d_pct'),
                 'exp_move': (bl.get('expected_move') or {}).get('event_move_proxy_pct'),
                 'yahoo': bl.get('yahoo_symbol'), 'panel_utc': pstamp.isoformat(),
                 'hunter_versions': hv,
                 'event_occurred': rr.get('event_occurred'), 'confirmation_note': rr.get('confirmation_note'),
                 'hunter_impact_sum': (hs.get(tk) or {}).get('impact_sum'),
                 'hunter_rankable': (hs.get(tk) or {}).get('rankable')}
            for k in ('panel_pct', 'panel_pct_signed', 'panel_pct_sd', 'side', 'sign_agree',
                      'consensus_k', 'selected_consensus', 'n_members'):
                x[k] = r.get(k)
            x['members'] = {m: {'pct_signed': v.get('pct_signed'), 'impact_sum': v.get('impact_sum'),
                                'p_up': v.get('p_up'), 'abs_move_pct': v.get('abs_move_pct')}
                            for m, v in (r.get('members') or {}).items()}
            x['px'] = prices(bl['yahoo_symbol'], pstamp, date.fromisoformat(bl['event_date']), sess) \
                if bl.get('yahoo_symbol') else None
            rows.append(x)
    # STOXX 600 as a market control, daily
    sb = [b for b in bars(fetch('^STOXX', '1d', '6mo'))]
    bench = {str(b['loc'].date()): b['c'] for b in sb}
    (S / 'dataset.json').write_text(json.dumps({'rows': rows, 'stoxx': bench}, indent=1, default=str))
    print(len(rows), 'rows;', sum(1 for r in rows if r['px'] and 'close_R' in r['px']), 'priced')


if __name__ == '__main__':
    main()

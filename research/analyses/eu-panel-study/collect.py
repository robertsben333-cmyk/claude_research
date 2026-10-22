"""Collect the EU panel study dataset: one row per panel-scored name with its panel
numbers, baseline attributes and prices at a grid of entry and exit times.

Live set: the EU panel days 2026-10-12 .. 2026-10-20 (rescored --dry-run in scratch so
every day carries panel_pct). Backtest set: the four-model re-judge of 2026-10-01 on
the clean (non-September-Opus-5.5) EU hunts, 2026-09-22 and 09-23.
"""
import json, subprocess, sys, time
from datetime import datetime, date, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path('/home/user/claude_research')
S = Path(__file__).resolve().parent  # rescore/<day>/: dry-run panel + resolver output; cache/ (prices) is not committed
CACHE = S / 'cache'; CACHE.mkdir(exist_ok=True)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0'
UTC = timezone.utc
TODAY = date(2026, 10, 21)  # today's session is incomplete: never a close


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
            d = json.loads(out)
            r = d['chart']['result'][0]
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
        out.append({'t': datetime.fromtimestamp(t, UTC), 'loc': datetime.fromtimestamp(t, tz),
                    'o': o if o is not None else c, 'c': c, 'v': q['volume'][i] or 0})
    return out


def prices(sym, entry_utc, d_event, session):
    """Grid of prices. R is the reaction session: D for bmo, the next session for amc."""
    daily = [b for b in bars(fetch(sym, '1d', '6mo')) if b['loc'].date() < TODAY]
    m5 = bars(fetch(sym, '5m', '60d'))
    days = [b['loc'].date() for b in daily]
    if not daily:
        return None
    # reaction session index
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
         'open_R_daily': daily[iR]['o'], 'last_daily': str(days[-1])}
    for k in (1, 2, 5):
        p[f'close_Rp{k}'] = daily[iR + k]['c'] if iR + k < len(daily) else None
    # entry at the seal / panel time on its own day (5m bar closed at or before)
    pre = [b for b in m5 if b['t'] <= entry_utc and b['loc'].date() == entry_utc.astimezone(m5[0]['loc'].tzinfo).date()] if m5 else []
    p['entry_seal'] = pre[-1]['c'] if pre else None
    p['entry_seal_bar'] = pre[-1]['loc'].isoformat() if pre else None
    # close of the day the panel ran (D-1 calendar session of entry)
    eday = entry_utc.astimezone(m5[0]['loc'].tzinfo).date() if m5 else None
    p['entry_day'] = str(eday)
    dd = [b for b in daily if b['loc'].date() == eday]
    p['close_entry_day'] = dd[0]['c'] if dd else None
    rb = [b for b in m5 if b['loc'].date() == R]
    p['n5m_R'] = len(rb)
    if rb:
        t0 = rb[0]['loc']
        p['open_R'] = rb[0]['o']
        p['first_trade_R'] = t0.isoformat()
        sess_open = t0.replace(hour=8 if 'London' in str(t0.tzinfo) else 9, minute=0, second=0)
        for lab, mins in (('R_30m', 30), ('R_60m', 60), ('R_120m', 120), ('R_240m', 240)):
            cut = sess_open + timedelta(minutes=mins)
            bb = [b for b in rb if b['loc'] + timedelta(minutes=5) <= cut]
            p[lab] = bb[-1]['c'] if bb else None
        p['R_vol_first30m_share'] = None
    else:
        p['open_R'] = None
    return p


def live_rows():
    out = []
    for dd in ('12', '13', '14', '15', '16', '19', '20'):
        run = S / 'rescore' / f'2026-10-{dd}'
        live_run = REPO / 'research/2026/10' / f'2026-10-{dd}' / 'europe'
        pan = json.loads((run / 'edge-scores-panel.json').read_text())
        prov = json.loads((live_run / 'provenance.json').read_text())
        pstamp = datetime.fromisoformat(prov['panel']['stamped_utc'])
        res = {}
        rf = run / 'eu-resolved.json'
        if rf.exists():
            for r in json.loads(rf.read_text()).get('rows', []):
                res[r['ticker']] = r
        hs = {x['ticker']: x.get('impact_sum') for x in json.loads((live_run / 'edge-scores.json').read_text()).get('ranking', [])}
        for r in pan['ranking']:
            r = dict(r, hunter_impact_sum=hs.get(r['ticker']))
            out.append(row('live', live_run, r, pstamp, res.get(r['ticker'], {})))
    return out


def row(src, run, r, entry_utc, res):
    bl = json.loads((run / 'baselines' / f"{r['ticker']}.json").read_text())
    sess = res.get('session') or bl.get('session') or 'bmo'
    x = {'src': src, 'day': bl['event_date'], 'ticker': r['ticker'], 'company': bl.get('company'),
         'submarket': bl.get('submarket'), 'industry': bl.get('industry'), 'session': sess,
         'session_baseline': bl.get('session'),
         'turnover_usd': (bl.get('tape') or {}).get('median_turnover_usd_20d'),
         'analyst_band': (bl.get('consensus') or {}).get('analyst_band'),
         'analyst_count': (bl.get('consensus') or {}).get('analyst_count'),
         'anchor_covered': bl.get('anchor_covered'),
         'history_basis': (bl.get('history') or {}).get('basis'),
         'vol20': (bl.get('tape') or {}).get('realised_vol_20d_pct'),
         'run_up_20d': (bl.get('tape') or {}).get('run_up_20d_pct'),
         'exp_move': (bl.get('expected_move') or {}).get('event_move_proxy_pct'),
         'sealed_spot': (bl.get('tape') or {}).get('spot'), 'sealed_utc': bl.get('sealed_utc'),
         'entry_utc': entry_utc.isoformat(), 'yahoo': bl.get('yahoo_symbol'),
         'event_occurred_res': res.get('event_occurred'), 'move_res': res.get('realised_move_pct'), 'move_pending_res': res.get('move_pending'), 'rankable_res': res.get('rankable'),
         'res_keys': sorted(res)[:0]}
    x.update({k: r.get(k) for k in ('panel_pct', 'panel_pct_signed', 'panel_pct_sd', 'side',
                                    'sign_agree', 'consensus_k', 'selected_consensus',
                                    'selected_mean_pct', 'panel_mean_z', 'n_members')})
    x['members'] = {m: {'impact_sum': v.get('impact_sum'), 'pct_signed': v.get('pct_signed'),
                        'p_up': v.get('p_up'), 'abs_move_pct': v.get('abs_move_pct')}
                    for m, v in (r.get('members') or {}).items()}
    x['hunter_impact_sum'] = r.get('hunter_impact_sum')
    d_event = date.fromisoformat(bl['event_date'])
    x['px'] = prices(bl['yahoo_symbol'], entry_utc, d_event, sess) if bl.get('yahoo_symbol') else None
    return x


def backtest_rows():
    key = [k for k in json.loads((REPO / 'research/analyses/rejudge-four-models/key.json').read_text())
           if k['region'] == 'europe' and k['day'] in ('2026-09-22', '2026-09-23')]
    rj = REPO / 'research/analyses/rejudge-four-models'
    sizes = {}
    for pack in ('eu', 'x1', 'x2'):
        for mm, name in (('opus5', 'opus5'), ('opus', 'opus55'), ('sonnet', 'sonnet55'), ('fable', 'fable51')):
            f = rj / f'out-{pack}-{mm}.json'
            if f.exists():
                for o in json.loads(f.read_text()):
                    sizes.setdefault(o['id'], {})[name] = o
    out = []
    for k in key:
        run = REPO / k['run']
        res = {}
        rf = run / 'eu-resolved.json'
        if rf.exists():
            res = next((r for r in json.loads(rf.read_text()).get('rows', []) if r['ticker'] == k['ticker']), {})
        bl = json.loads((REPO / k['baseline']).read_text())
        r = {'ticker': k['ticker'], 'members': {m: {'impact_sum': v['impact_sum'], 'p_up': v.get('p_up'),
                                                       'abs_move_pct': v.get('abs_move_pct')}
                                                   for m, v in sizes.get(k.get('pid') or k['id'], {}).items()},
             'hunter_impact_sum': k.get('live')}
        x = row('backtest', run, r, datetime.fromisoformat(bl['sealed_utc']), res)
        x['move_key'] = k.get('move')
        x['anon'] = bool(k.get('anon'))
        out.append(x)
    return out


if __name__ == '__main__':
    rows = live_rows() + backtest_rows()
    (S / 'dataset.json').write_text(json.dumps(rows, indent=1, default=str))
    print(len(rows), 'rows;', sum(1 for r in rows if r['px'] and 'close_R' in r['px']), 'priced')

"""Alpaca SIP bars for the priced-in study. Per reaction day, multi-symbol requests:
1-min from the previous session's 16:00 ET to the reaction day's 16:00 ET (covers amc after-hours,
overnight pre-market, regular session), and 15-min 04:00-20:00 over the 21 sessions before.
Usage: fetch.py ev.json cache_dir. Keys from env, never printed."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error, collections
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York'); UTC = dt.timezone.utc
H = {'APCA-API-KEY-ID': os.environ['ALPACA_API_KEY_ID'], 'APCA-API-SECRET-KEY': os.environ['ALPACA_API_SECRET_KEY']}
EV, C = sys.argv[1], sys.argv[2]; os.makedirs(C, exist_ok=True)
def iso(day, hh, mm):
    return dt.datetime.combine(dt.date.fromisoformat(day), dt.time(hh, mm), NY).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def et(t):
    x = dt.datetime.fromisoformat(t.replace('Z', '+00:00')).astimezone(NY); return x.date().isoformat(), x.hour * 60 + x.minute
def multi(syms, tf, start, end):
    out = collections.defaultdict(list); tok = None
    while True:
        q = dict(symbols=','.join(syms), timeframe=tf, start=start, end=end, feed='sip', adjustment='split', limit=10000)
        if tok: q['page_token'] = tok
        url = 'https://data.alpaca.markets/v2/stocks/bars?' + urllib.parse.urlencode(q)
        for a in range(8):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=90) as r: d = json.load(r); break
            except urllib.error.HTTPError as e:
                if e.code == 429: time.sleep(min(30, 2 ** a)); continue
                print('HTTP', e.code, e.read()[:200], flush=True); time.sleep(2 ** a)
            except Exception: time.sleep(2 ** a)
        else: raise RuntimeError('retries')
        for s, bars in (d.get('bars') or {}).items(): out[s] += bars
        tok = d.get('next_page_token')
        if not tok: return out
cal_p = f'{C}/_cal.json'
if not os.path.exists(cal_p):
    sp = multi(['SPY'], '1Day', iso('2026-06-01', 0, 0), iso('2026-11-07', 0, 0))['SPY']
    json.dump([et(b['t'])[0] for b in sp], open(cal_p, 'w'))
CAL = json.load(open(cal_p))
E = json.load(open(EV))
need = collections.defaultdict(list)
for e in E:
    d = e['event_date']
    if e['session'] == 'bmo': rd = d if d in CAL else None
    else:
        nx = [x for x in CAL if x > d]; rd = nx[0] if nx else None
    e['react_day'] = rd
    if not rd or rd > '2026-11-06' or rd < '2026-08-31': continue
    key = f"{e['ticker']}_{e['event_date']}"
    if os.path.exists(f'{C}/{key}.json'): continue
    need[rd].append((e['ticker'].replace('-', '.'), key))
json.dump(E, open(EV, 'w'))
print(sum(len(v) for v in need.values()), 'events over', len(need), 'days', flush=True)
for day in sorted(need):
    i = CAL.index(day); prev = CAL[i - 1]; h0, h1 = CAL[i - 22], CAL[i - 1]
    syms = sorted({s for s, _ in need[day]}); m, q = {}, {}
    for j in range(0, len(syms), 40):
        m.update(multi(syms[j:j + 40], '1Min', iso(prev, 16, 0), iso(day, 16, 0)))
        q.update(multi(syms[j:j + 40], '15Min', iso(h0, 4, 0), iso(h1, 20, 0)))
    for s, key in need[day]:
        m1 = [[*et(x['t']), x['o'], x['h'], x['l'], x['c'], x['v'], x.get('vw')] for x in m.get(s, [])]
        q15 = [[*et(x['t']), x['c'], x['v']] for x in q.get(s, [])]
        json.dump(dict(day=day, prev=prev, m1=m1, q15=q15), open(f'{C}/{key}.json', 'w'))
    print(day, len(need[day]), flush=True)
print('done')

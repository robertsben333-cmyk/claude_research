"""Faster fetch with Alpaca multi-symbol requests (same cache format as fetch.py):
per reaction day one 1-min request for all symbols, daily bars for all symbols in batches."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error, collections
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York'); UTC = dt.timezone.utc
H = {'APCA-API-KEY-ID': os.environ['ALPACA_API_KEY_ID'], 'APCA-API-SECRET-KEY': os.environ['ALPACA_API_SECRET_KEY']}
EV, CACHE = sys.argv[1], sys.argv[2]
CAL = json.load(open(f'{CACHE}/_cal.json'))
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
                with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60) as r: d = json.load(r); break
            except urllib.error.HTTPError as e:
                if e.code == 429: time.sleep(min(30, 2 ** a)); continue
                print('HTTP', e.code, e.read()[:200], flush=True); time.sleep(2 ** a)
            except Exception as ex: time.sleep(2 ** a)
        else: raise RuntimeError('retries')
        for s, bars in (d.get('bars') or {}).items(): out[s] += bars
        tok = d.get('next_page_token')
        if not tok: return out
E = json.load(open(EV))
need = collections.defaultdict(list)   # day -> [(sym, key)]
for e in E:
    r = e.get('react_day')
    if not r or r > '2026-11-06': continue
    key = f"{e['ticker']}_{e['event_date']}"
    if os.path.exists(f'{CACHE}/{key}.json'): continue
    need[r].append((e['ticker'].replace('-', '.'), key))
for day in need: need[day].append(('SPY', f'SPY_{day}'))
allsyms = sorted({s for v in need.values() for s, _ in v})
print(sum(len(v) for v in need.values()), 'to fetch over', len(need), 'days,', len(allsyms), 'symbols', flush=True)
daily = collections.defaultdict(list)
for i in range(0, len(allsyms), 100):
    b = multi(allsyms[i:i + 100], '1Day', iso('2026-06-20', 0, 0), iso('2026-11-07', 0, 0))
    for s, bars in b.items(): daily[s] = [[et(x['t'])[0], x['o'], x['h'], x['l'], x['c'], x['v']] for x in bars]
print('daily done', flush=True)
for day in sorted(need):
    syms = sorted({s for s, _ in need[day]})
    m = {}
    for i in range(0, len(syms), 50):
        m.update(multi(syms[i:i + 50], '1Min', iso(day, 4, 0), iso(day, 16, 0)))
    i0 = CAL.index(day); d0 = CAL[max(0, i0 - 46)]
    for s, key in need[day]:
        m1 = [[et(x['t'])[1], x['o'], x['h'], x['l'], x['c'], x['v']] for x in m.get(s, [])]
        dd = [x for x in daily.get(s, []) if d0 <= x[0] < day]
        json.dump(dict(day=day, m1=m1, d=dd), open(f'{CACHE}/{key}.json', 'w'))
    print(day, len(need[day]), flush=True)
print('done')

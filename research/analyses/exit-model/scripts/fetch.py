"""Alpaca SIP bars per event: 1-min 04:00-16:00 ET on the reaction day, daily bars for ~45 sessions
before. Reaction day from SPY's trading calendar. Keys from env, never printed."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York'); UTC = dt.timezone.utc
H = {'APCA-API-KEY-ID': os.environ['ALPACA_API_KEY_ID'], 'APCA-API-SECRET-KEY': os.environ['ALPACA_API_SECRET_KEY']}
EV, CACHE = sys.argv[1], sys.argv[2]; os.makedirs(CACHE, exist_ok=True)
def iso(day, hh, mm):
    return dt.datetime.combine(dt.date.fromisoformat(day), dt.time(hh, mm), NY).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def get(sym, tf, start, end):
    out, tok = [], None
    while True:
        q = dict(timeframe=tf, start=start, end=end, feed='sip', adjustment='split', limit=10000)
        if tok: q['page_token'] = tok
        url = f"https://data.alpaca.markets/v2/stocks/{urllib.parse.quote(sym)}/bars?" + urllib.parse.urlencode(q)
        for a in range(7):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40) as r: d = json.load(r); break
            except urllib.error.HTTPError as e:
                if e.code == 429: time.sleep(2 ** a); continue
                if e.code in (400, 404, 422): return out
                time.sleep(2 ** a)
            except Exception: time.sleep(2 ** a)
        else: raise RuntimeError('retries')
        out += d.get('bars') or []; tok = d.get('next_page_token')
        if not tok: return out
def et(t):
    x = dt.datetime.fromisoformat(t.replace('Z', '+00:00')).astimezone(NY); return x.date().isoformat(), x.hour * 60 + x.minute
# trading calendar
cal_p = f'{CACHE}/_cal.json'
if not os.path.exists(cal_p):
    sp = get('SPY', '1Day', iso('2026-06-01', 0, 0), iso('2026-11-07', 0, 0))
    json.dump([et(b['t'])[0] for b in sp], open(cal_p, 'w'))
CAL = json.load(open(cal_p))
def react_day(e):
    d = e['event_date']
    if e['session'] == 'bmo': return d if d in CAL else None
    nxt = [x for x in CAL if x > d]; return nxt[0] if nxt else None
def one(sym, day, key):
    p = f"{CACHE}/{key}.json"
    if os.path.exists(p): return
    try:
        m1 = get(sym, '1Min', iso(day, 4, 0), iso(day, 16, 0))
        i = CAL.index(day); d0 = CAL[max(0, i - 46)]
        dd = get(sym, '1Day', iso(d0, 0, 0), iso(day, 0, 0))
        out = dict(day=day, m1=[[et(b['t'])[1], b['o'], b['h'], b['l'], b['c'], b['v']] for b in m1],
                   d=[[et(b['t'])[0], b['o'], b['h'], b['l'], b['c'], b['v']] for b in dd])
    except Exception as ex:
        out = dict(error=f'{type(ex).__name__}: {ex}')
    json.dump(out, open(p, 'w'))
E = json.load(open(EV)); jobs = []
for e in E:
    r = react_day(e)
    if not r or r > '2026-11-06': continue
    e['react_day'] = r
    jobs.append((e['ticker'].replace('-', '.'), r, f"{e['ticker']}_{e['event_date']}"))
for day in sorted({j[1] for j in jobs}): jobs.append(('SPY', day, f'SPY_{day}'))
json.dump(E, open(EV, 'w'))
print(len(jobs), 'jobs', flush=True)
with ThreadPoolExecutor(6) as ex: list(ex.map(lambda j: one(*j), jobs))
print('done')

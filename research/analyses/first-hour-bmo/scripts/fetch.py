"""Alpaca SIP bars per bmo event: 1-min bars of the report day (09:30-16:00 ET) and 30-min
bars of the previous ~40 calendar days (first-hour volume, prior close). Keys from env, never printed."""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo
NY = ZoneInfo('America/New_York'); UTC = dt.timezone.utc
H = {'APCA-API-KEY-ID': os.environ['ALPACA_API_KEY_ID'], 'APCA-API-SECRET-KEY': os.environ['ALPACA_API_SECRET_KEY']}
CACHE = sys.argv[2]; os.makedirs(CACHE, exist_ok=True)
def iso(day, hh, mm):
    return dt.datetime.combine(dt.date.fromisoformat(day), dt.time(hh, mm), NY).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def get(sym, tf, start, end):
    out, tok = [], None
    while True:
        q = dict(timeframe=tf, start=start, end=end, feed='sip', adjustment='split', limit=10000)
        if tok: q['page_token'] = tok
        url = f"https://data.alpaca.markets/v2/stocks/{urllib.parse.quote(sym)}/bars?" + urllib.parse.urlencode(q)
        for a in range(6):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=30) as r: d = json.load(r); break
            except urllib.error.HTTPError as e:
                if e.code == 429: time.sleep(2 ** a); continue
                raise
            except Exception: time.sleep(2 ** a)
        else: raise RuntimeError('retries')
        out += d.get('bars') or []; tok = d.get('next_page_token')
        if not tok: return out
def et(t):
    x = dt.datetime.fromisoformat(t.replace('Z', '+00:00')).astimezone(NY); return x.date().isoformat(), x.hour * 60 + x.minute
def one(e):
    p = f"{CACHE}/{e['ticker']}_{e['event_date']}.json"
    if os.path.exists(p): return
    sym = e['ticker'].replace('-', '.'); d = e['event_date']
    try:
        m1 = get(sym, '1Min', iso(d, 9, 30), iso(d, 16, 0))
        d0 = (dt.date.fromisoformat(d) - dt.timedelta(days=42)).isoformat()
        m30 = get(sym, '30Min', iso(d0, 9, 30), iso(d, 4, 0))
        out = dict(m1=[[et(b['t'])[1], b['o'], b['h'], b['l'], b['c'], b['v'], b.get('vw')] for b in m1],
                   m30=[[*et(b['t']), b['c'], b['v']] for b in m30])
    except Exception as ex:
        out = dict(error=f'{type(ex).__name__}: {ex}')
    json.dump(out, open(p, 'w'))
E = json.load(open(sys.argv[1]))
with ThreadPoolExecutor(4) as ex: list(ex.map(one, E))
print('done')

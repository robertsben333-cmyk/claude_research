#!/usr/bin/env python3
"""Phase 1, layer 1: mechanical source fields, no model.

  python3 scripts/mechanical.py        # writes data/mechanical.json (and caches EDGAR in data/edgar-cache/)

Per item:
  sec_form        the SEC form the item cites: from the EDGAR accession in a sec.gov URL
                  (data.sec.gov submissions, one call per CIK, cached), else from the
                  text/source by regex. Normalised: 8-K, 10-Q, 10-K, S-1, S-3, 424B,
                  DEF 14A, 4, SC 13D, SC 13G, 6-K, NT 10-Q/10-K, 8-A, 144, other.
  sec_items       8-K item numbers (EDGAR's own field when the accession resolves,
                  else 'Item x.xx' found in the text).
  sec_filer_is_focal  the accession's CIK is the focal company's CIK (when resolvable).
  newswire        the domain is a newswire (globenewswire, prnewswire, businesswire,
                  accesswire, newsfile, ...); `newswire_own` when the release names the
                  focal company in its headline/text (the pack text, before scrubbing).
  domain_class    the 14-class domain map of ../source-types.
  age_bucket      days from the source date to the entry: <=7, 8-30, 31-90, >90, unknown.

Nothing here reads an outcome.
"""
import json, os, re, sys, time, urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.dirname(HERE)
R = os.path.abspath(os.path.join(SV, '..', '..', '..'))
CACHE = f'{SV}/data/edgar-cache'
UA = 'claude_research source-value study robertsben333@gmail.com'
URLS = re.compile(r'https?://[^\s)\]>"\',;]+')
ACC = re.compile(r'/Archives/edgar/data/(\d+)/(\d{18})')
ACC2 = re.compile(r'(\d{10})-(\d{2})-(\d{6})')
NEWSWIRES = ('globenewswire', 'prnewswire', 'businesswire', 'accesswire', 'newsfilecorp', 'einpresswire', 'stocktitan',
             'investorsobserver', 'newswire.ca', 'marketwired', 'globalnewswire')
FORM_RX = [
    ('NT 10-Q', r'\bNT\s*10-?[QK]\b|notification of late filing|\b12b-25\b'),
    ('424B', r'\b424B\d?\b|prospectus supplement'),
    ('S-3', r'\bS-3(ASR)?\b|shelf registration'),
    ('S-1', r'\bS-1\b'),
    ('DEF 14A', r'\bDEF\s*14A\b|proxy statement'),
    ('SC 13D', r'\b(SC\s*)?13D\b'),
    ('SC 13G', r'\b(SC\s*)?13G\b'),
    ('4', r'\bForm\s*4\b|\bForm 4s\b|\bSection 16\b'),
    ('144', r'\bForm\s*144\b'),
    ('6-K', r'\b6-K\b'),
    ('20-F', r'\b20-F\b'),
    ('10-K', r'\b10-K\b'),
    ('10-Q', r'\b10-Q\b'),
    ('8-K', r'\b8-K\b|\bItem\s+[1-9]\.\d\d\b'),
]
ITEM_RX = re.compile(r'\bItem\s+([1-9]\.\d\d)\b', re.I)


def norm_form(f):
    if not f:
        return None
    f = f.upper().replace('/A', '')
    if f.startswith('424B'):
        return '424B'
    for k in ('8-K', '10-Q', '10-K', 'S-1', 'S-3', 'DEF 14A', '6-K', '20-F', 'SC 13D', 'SC 13G', '144', '8-A12B'):
        if f.startswith(k):
            return k
    if f in ('4', '3', '5'):
        return '4'
    if f.startswith('NT 10'):
        return 'NT 10-Q'
    if f.startswith('SCHEDULE 13D'):
        return 'SC 13D'
    if f.startswith('SCHEDULE 13G'):
        return 'SC 13G'
    return 'other'


def fetch_submissions(cik):
    os.makedirs(CACHE, exist_ok=True)
    p = f'{CACHE}/{int(cik)}.json'
    if os.path.exists(p):
        return json.load(open(p))
    url = f'https://data.sec.gov/submissions/CIK{int(cik):010d}.json'
    out = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Encoding': 'identity'})
            d = json.load(urllib.request.urlopen(req, timeout=30))
            rec = d.get('filings', {}).get('recent', {})
            out = {'cik': int(cik), 'name': d.get('name'), 'tickers': d.get('tickers'),
                   'acc': {a.replace('-', ''): {'form': f, 'items': it, 'date': dt} for a, f, it, dt in
                           zip(rec.get('accessionNumber', []), rec.get('form', []), rec.get('items', []), rec.get('filingDate', []))}}
            break
        except Exception as e:  # noqa: BLE001
            out = {'cik': int(cik), 'error': str(e)[:200], 'acc': {}}
            time.sleep(1 + attempt)
    json.dump(out, open(p, 'w'))
    time.sleep(0.15)  # SEC fair-access: well under 10 requests a second
    return out


def item_urls(it):
    us = set(URLS.findall(it.get('text') or ''))
    if (it.get('source') or '').startswith('http'):
        us.add(it['source'])
    for u in URLS.findall(json.dumps(it.get('cited_titles') or '')):
        us.add(u)
    return sorted(us)


def main():
    I = json.load(open(f'{SV}/data/items.json'))
    E = {e['id']: e for e in json.load(open(f'{SV}/data/events.json'))}
    DOMCLS = json.load(open(f'{SV}/../source-types/data/domain_classes_llm.json'))
    # focal CIKs: from the ticker map EDGAR publishes
    tmap = {}
    tp = f'{CACHE}/company_tickers.json'
    os.makedirs(CACHE, exist_ok=True)
    if not os.path.exists(tp):
        try:
            req = urllib.request.Request('https://www.sec.gov/files/company_tickers.json', headers={'User-Agent': UA})
            json.dump(json.load(urllib.request.urlopen(req, timeout=30)), open(tp, 'w'))
        except Exception as e:  # noqa: BLE001
            json.dump({}, open(tp, 'w'))
            print('ticker map failed', e)
    for v in json.load(open(tp)).values():
        tmap[v['ticker'].upper()] = int(v['cik_str'])
    ciks = set()
    for it in I:
        for u in item_urls(it):
            m = ACC.search(u)
            if m:
                ciks.add(int(m.group(1)))
            m = re.search(r'CIK=?0*(\d+)', u, re.I) or re.search(r'/CIK0*(\d+)\.json', u)
            if m:
                ciks.add(int(m.group(1)))
    for e in E.values():
        if e['market'] == 'us' and e['ticker'].upper() in tmap:
            ciks.add(tmap[e['ticker'].upper()])
    subs = {c: fetch_submissions(c) for c in sorted(ciks)}
    acc_index = {}
    for c, s in subs.items():
        for a, v in (s.get('acc') or {}).items():
            acc_index[a] = dict(v, cik=c)
    out = {}
    for it in I:
        ev = E[it['event']]
        us = item_urls(it)
        text = (it.get('text') or '') + ' ' + (it.get('source') or '')
        form, items, filer, how = None, [], None, None
        for u in us:
            m = ACC.search(u)
            a = m.group(2) if m else None
            if not a:
                m2 = ACC2.search(u)
                a = ''.join(m2.groups()) if m2 else None
            if a and a in acc_index:
                v = acc_index[a]
                form, items, filer, how = norm_form(v['form']), [x for x in (v.get('items') or '').split(',') if x], v['cik'], 'edgar_accession'
                break
        if form is None:
            for f, rx in FORM_RX:
                if re.search(rx, text, re.I):
                    form, how = f, 'regex'
                    break
            if form == '8-K' or (form is None and any('sec.gov' in u for u in us)):
                items = sorted(set(ITEM_RX.findall(text)))
                if form is None and any('sec.gov' in u for u in us):
                    form, how = 'sec_other', 'url'
        focal_cik = tmap.get(ev['ticker'].upper()) if ev['market'] == 'us' else None
        doms = sorted({(re.sub(r'^www\.', '', u.split('/')[2].lower())) for u in us if u.count('/') >= 2})
        dom = it.get('domain') or (doms[0] if doms else None)
        nw = any(any(w in d for w in NEWSWIRES) for d in doms + ([dom] if dom else []))
        comp = (ev.get('company') or '').split(',')[0].split(' Inc')[0].strip()
        own = bool(nw and comp and len(comp) >= 3 and (comp.lower() in text.lower() or '[the company]' in text.lower()))
        age = it.get('age_days')
        ab = 'unknown' if age is None else ('<=7' if age <= 7 else '8-30' if age <= 30 else '31-90' if age <= 90 else '>90')
        out[f"{it['pack_id']}#{it['i']}"] = {
            'sec_form': form, 'sec_form_basis': how, 'sec_items': items,
            'sec_filer_is_focal': (filer == focal_cik) if (filer and focal_cik) else None,
            'newswire': nw, 'newswire_own': own, 'domain': dom,
            'domain_class': DOMCLS.get(dom) if dom else 'no_source', 'n_domains': len(doms), 'age_bucket': ab}
    json.dump(out, open(f'{SV}/data/mechanical.json', 'w'), indent=0)
    print('items', len(out), 'ciks', len(subs), 'edgar errors', sum(1 for s in subs.values() if s.get('error')))
    print('forms', Counter(v['sec_form'] for v in out.values()).most_common())
    print('basis', Counter(v['sec_form_basis'] for v in out.values()))
    print('8-K items', Counter(x for v in out.values() for x in v['sec_items']).most_common(15))
    print('newswire', Counter((v['newswire'], v['newswire_own']) for v in out.values()))
    print('domain_class', Counter(v['domain_class'] for v in out.values()).most_common())


if __name__ == '__main__':
    main()

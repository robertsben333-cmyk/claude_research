import re, zlib, sys
data = open(sys.argv[1], 'rb').read()
# collect all streams, decompress
streams = []
for m in re.finditer(rb'stream\r?\n', data):
    start = m.end()
    end = data.find(b'endstream', start)
    if end < 0: continue
    raw = data[start:end]
    try:
        dec = zlib.decompress(raw)
    except Exception:
        try:
            dec = zlib.decompressobj().decompress(raw)
        except Exception:
            dec = None
    if dec: streams.append(dec)
# expand object streams: they contain objects which may include ToUnicode CMaps etc.
cmaps = []
for s in streams:
    if b'beginbfchar' in s or b'beginbfrange' in s:
        cmaps.append(s)
print('streams', len(streams), 'cmaps', len(cmaps), file=sys.stderr)
# build a merged cmap per stream index (fallback: merge all; risky but try)
def parse_cmap(s):
    mp = {}
    for blk in re.findall(rb'beginbfchar(.*?)endbfchar', s, re.S):
        for a, b in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            try: mp[a.decode().upper()] = bytes.fromhex(b.decode()).decode('utf-16-be', 'ignore')
            except Exception: pass
    for blk in re.findall(rb'beginbfrange(.*?)endbfrange', s, re.S):
        for a, b, c in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            lo, hi, st = int(a, 16), int(b, 16), int(c, 16)
            w = len(a)
            for i in range(hi - lo + 1):
                try: mp[('%0*X' % (w, lo + i))] = chr(st + i)
                except Exception: pass
    return mp
cm_list = [parse_cmap(c) for c in cmaps]
out = []
for s in streams:
    if b'BT' not in s or (b'Tj' not in s and b'TJ' not in s): continue
    text = []
    for tok in re.finditer(rb'\[(.*?)\]\s*TJ|<([0-9A-Fa-f]+)>\s*Tj|\((.*?)(?<!\\)\)\s*Tj|(T\*|Td|TD|ET)', s, re.S):
        if tok.group(1) is not None:
            inner = tok.group(1)
            parts = re.findall(rb'<([0-9A-Fa-f]+)>|\((.*?)(?<!\\)\)|(-?\d+\.?\d*)', inner, re.S)
            for h, lit, num in parts:
                if h:
                    text.append(('H', h.decode().upper()))
                elif lit:
                    text.append(('L', lit))
                elif num:
                    try:
                        if float(num) < -200: text.append(('S', ' '))
                    except: pass
        elif tok.group(2) is not None:
            text.append(('H', tok.group(2).decode().upper()))
        elif tok.group(3) is not None:
            text.append(('L', tok.group(3)))
        else:
            text.append(('S', '\n' if tok.group(4) in (b'T*', b'ET') else ' '))
    out.append(text)
# try each cmap and choose the one decoding most hex codes
def decode(text, mp):
    res = []
    for kind, v in text:
        if kind == 'H':
            # try 4-hex units then 2-hex
            step = 4 if len(v) % 4 == 0 and any(len(k) == 4 for k in mp) else 2
            for i in range(0, len(v), step):
                res.append(mp.get(v[i:i+step], ''))
        elif kind == 'L':
            res.append(v.decode('latin-1'))
        else:
            res.append(v)
    return ''.join(res)
allmp = {}
for mp in cm_list:
    allmp.update(mp)
for text in out:
    sys.stdout.write(decode(text, allmp))
    sys.stdout.write('\n')

import zipfile,re,sys,xml.etree.ElementTree as ET
ns={'a':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def rows(path):
    z=zipfile.ZipFile(path)
    ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        t=ET.fromstring(z.read('xl/sharedStrings.xml'))
        for si in t.findall('a:si',ns):
            ss.append(''.join(x.text or '' for x in si.iter('{%s}t'%ns['a'])))
    sh=[n for n in z.namelist() if n.startswith('xl/worksheets/sheet')]
    t=ET.fromstring(z.read(sorted(sh)[0]))
    out=[]
    for r in t.iter('{%s}row'%ns['a']):
        vals=[]
        for c in r.findall('a:c',ns):
            v=c.find('a:v',ns); s=v.text if v is not None else ''
            if c.get('t')=='s' and s: s=ss[int(s)]
            vals.append(s)
        out.append(vals)
    return out
for p in sys.argv[1:]:
    R=rows(p)
    if 'hdr' in sys.argv[0:1]: pass
    print('==',p)
    for r in R[:12]: print(r[:6])
    for r in R:
        j='|'.join(r)
        if re.search(r'STONEX|O.?BRIEN|MAREX|INTERACTIVE',j,re.I): print(r)

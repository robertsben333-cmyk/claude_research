import zipfile,re,sys,xml.etree.ElementTree as ET
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def rows(p):
    z=zipfile.ZipFile(p)
    ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns):
            ss.append(''.join(t.text or '' for t in si.iter('{%s}t'%ns['m'])))
    sheets=[n for n in z.namelist() if n.startswith('xl/worksheets/sheet')]
    out=[]
    for s in sheets:
        for r in ET.fromstring(z.read(s)).iter('{%s}row'%ns['m']):
            vals=[]
            for c in r.findall('m:c',ns):
                v=c.find('m:v',ns); t=c.get('t')
                if v is None:
                    is_=c.find('m:is',ns); vals.append(''.join(x.text or '' for x in is_.iter('{%s}t'%ns['m'])) if is_ is not None else ''); continue
                vals.append(ss[int(v.text)] if t=='s' else v.text)
            out.append((s,vals))
    return out
for p in sys.argv[1:]:
    R=rows(p)
    if p==sys.argv[1]:
        for s,v in R[:8]: print('HDR',v)
    for s,v in R:
        j=' '.join(v).upper()
        if 'STONEX' in j or "O'BRIEN" in j or 'OBRIEN' in j or 'MAREX' in j:
            print(p.split('/')[-1],v)

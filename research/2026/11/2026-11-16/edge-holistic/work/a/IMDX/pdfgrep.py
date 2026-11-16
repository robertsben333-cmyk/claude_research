import re,zlib,sys
data=open(sys.argv[1],'rb').read()
out=[]
for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream',data,re.S):
    try: s=zlib.decompress(m.group(1))
    except Exception: continue
    # extract literal strings in TJ/Tj
    txt=[]
    for t in re.finditer(rb'\[(.*?)\]\s*TJ|\((.*?)\)\s*Tj',s,re.S):
        seg=t.group(1) if t.group(1) is not None else b'('+t.group(2)+b')'
        parts=re.findall(rb'\(((?:\\.|[^\\)])*)\)',seg)
        txt.append(b''.join(parts))
    if txt: out.append(b' '.join(txt).decode('latin1'))
open(sys.argv[2],'w').write('\n'.join(out))
print(len(out))

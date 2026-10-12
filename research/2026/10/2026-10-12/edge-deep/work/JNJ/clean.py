import sys,re
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
out=[]
for line in t.split('\n'):
    if not line.strip(): continue
    good=sum(ch.isascii() and (ch.isalnum() or ch in " .,$%()-&/:'\"?!;") for ch in line)
    if good/len(line)>0.93 and len(line)>30:
        out.append(line)
s='\n'.join(out)
s=re.sub(r'LSEG STREETEVENTS \| www\.lseg\.com.*?affiliated companies\.','',s)
print(s)

import sys,re,html
s=sys.stdin.read()
s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S)
t=html.unescape(re.sub('<[^>]+>',' ',s));t=re.sub(r'\s+',' ',t)
key=sys.argv[1]
idx=[m.start() for m in re.finditer(key,t)]
i=idx[1] if len(idx)>1 else (idx[0] if idx else 0)
print(t[i:i+1400])

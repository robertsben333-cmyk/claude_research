import re,html,sys
n=sys.argv[1]
t=open(n+'.htm',errors='ignore').read();t=re.sub(r'<[^>]+>',' ',t);t=html.unescape(t);t=re.sub(r'\s+',' ',t);open(n+'.txt','w').write(t)
for pat in [r'Revenue reached US\$[0-9.]+ million.{0,200}', r'Adjusted EBITDA Margin [0-9.]+%.{0,60}', r'We expect our revenue.{0,250}', r'estimate our Adjusted EBITDA margin.{0,120}', r'These estimates assume.{0,120}']:
  m=re.search(pat,t); print(n,'|',m.group(0) if m else None)

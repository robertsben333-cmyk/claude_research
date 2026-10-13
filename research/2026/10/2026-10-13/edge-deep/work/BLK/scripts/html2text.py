import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip+=1
        if tag in ('p','div','tr','br','li','h1','h2','h3','h4','table'): self.out.append('\n')
        if tag in ('td','th'): self.out.append(' | ')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)
src=open(sys.argv[1],encoding='utf-8',errors='replace').read()
src=re.sub(r'<img[^>]*>','',src)
p=P(); p.feed(src)
t=''.join(p.out)
t=re.sub(r'[ \t\xa0]+',' ',t)
t=re.sub(r'\n\s*\n+','\n',t)
open(sys.argv[2],'w').write(t)
print(len(t))

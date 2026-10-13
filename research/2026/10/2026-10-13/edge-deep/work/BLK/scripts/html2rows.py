import sys, re
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.lines=[]; self.cur=[]; self.cell=[]; self.skip=0; self.intable=0
    def flushcell(self):
        c=''.join(self.cell).strip()
        c=re.sub(r'\s+',' ',c)
        if c: self.cur.append(c)
        self.cell=[]
    def flushline(self):
        self.flushcell()
        if self.cur: self.lines.append(' '.join(self.cur))
        self.cur=[]
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style'): self.skip+=1
        if tag=='tr' or tag in ('p','br','li','h1','h2','h3','h4') and not self.intable: self.flushline()
        if tag=='table': self.flushline(); self.intable+=1
        if tag in ('td','th'): self.flushcell()
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1
        if tag=='tr': self.flushline()
        if tag=='table': self.flushline(); self.intable-=1
        if tag in ('td','th'): self.flushcell()
        if tag in ('p','div') and not self.intable: self.flushline()
    def handle_data(self, d):
        if not self.skip: self.cell.append(d)
src=open(sys.argv[1],encoding='utf-8',errors='replace').read()
src=re.sub(r'<img[^>]*>','',src)
p=P(); p.feed(src); p.flushline()
out='\n'.join(l.replace('\xa0',' ') for l in p.lines)
out=re.sub(r'\$ ','$',out); out=re.sub(r'\( ','(',out); out=re.sub(r' \)',')',out); out=re.sub(r' %','%',out)
open(sys.argv[2],'w').write(out)
print(len(out))

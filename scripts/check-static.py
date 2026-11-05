from pathlib import Path
from html.parser import HTMLParser
import re
ROOT=Path(__file__).resolve().parents[1]/'site'
class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.assets=[];self.summaries=0;self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag in ('script','img','source'):self.assets.append(a.get('src',''))
        if tag=='link':self.assets.append(a.get('href',''))
        if tag=='summary':self.summaries+=1
        if tag=='h1':self.h1+=1
        assert 'autoplay' not in a
p=Parser();s=(ROOT/'index.html').read_text();p.feed(s)
assert p.h1==1 and p.summaries==3
assert len(p.ids)==len(set(p.ids))
for x in p.links+p.assets:
    assert x and x!='#'
    if x.startswith('#'):assert x[1:] in p.ids,x
    elif not re.match(r'https://|mailto:',x):assert (ROOT/x).is_file(),x
assert not re.search(r'010[- ]?\d{4}',s)
assert '세계 최초' not in s and 'MACLab' not in s
assert 'EDITOR_NOTES' not in s

def luminance(h):
    values=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    values=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(v*w for v,w in zip(values,[.2126,.7152,.0722]))
for fg,bg in [('262626','ffffff'),('606060','ffffff'),('245b8a','ffffff')]:
    a,b=sorted([luminance(fg),luminance(bg)])
    ratio=(b+.05)/(a+.05);assert ratio>=4.5
    print(f'Contrast #{fg} / #{bg}: {ratio:.2f}:1')
print('PASS: heading, anchors, local assets, media policy, privacy, contrast')

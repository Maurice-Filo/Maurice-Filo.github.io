"""Check generated page links and content records with standard Python 3."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  for key in ['href','src']:
   if a.get(key):self.refs.append(a[key])
errors=[];missing=set();pages=list(ROOT.glob('*.html'))
for path in pages:
 p=Page();p.feed(path.read_text())
 if p.h1!=1:errors.append(f'{path.name}: expected one primary heading')
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or not u.path:continue
  name=unquote(u.path);target=ROOT/name
  if not target.exists():
   if target.suffix in ['.html','.css','.js','.svg','.webp','.jpg']:errors.append(f'{path.name}: missing {name}')
   else:missing.add(name)
records=json.loads((ROOT/'content/publications.json').read_text());ids=[p['id'] for p in records]
if len(ids)!=len(set(ids)):errors.append('Publication IDs must be unique')
topics=json.loads((ROOT/'content/navigation.json').read_text())['topics']
for paper in records:
 for topic in paper['topics']:
  if topic not in topics:errors.append(f'Unknown topic {topic} in {paper["id"]}')
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages and {len(records)} publication records. {len(missing)} omitted resource paths remain to be restored.')

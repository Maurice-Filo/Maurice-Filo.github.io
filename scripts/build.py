"""Build static GitHub Pages HTML from content sources. Python 3, no dependencies."""
from pathlib import Path
import json,re,html
from datetime import date as calendar_date
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
def read_json(name):
 return json.loads((ROOT/'content'/name).read_text())
D=read_json('navigation.json')
D['profile']=read_json('profile.json')
D['publications']=read_json('publications.json')
D['news']=read_json('news.json')
D['talks']=read_json('talks.json')
D['pages']={name:{**entry,'html':(ROOT/'content'/entry['file']).read_text()} for name,entry in read_json('pages.json').items() if name!='Talks'}
D['publication_appendix']=(ROOT/'content/pages/publication-appendix.html').read_text()
D['publications'].sort(key=lambda p: -int(p.get('year',0)))
esc=html.escape
def url(name):return quote(name+'.html')
def link(name,label=None):return f'<a href="{url(name)}">{esc(label or name)}</a>'
def cards(names):
 items=[]
 images=D.get('topic_images',{})
 for i,name in enumerate(names):
  art=f'<img class="topic-image" src="{esc(images[name])}" alt="" width="480" height="240" loading="lazy">' if name in images else ''
  items.append(f'<a class="topic-card{ " illustrated" if art else ""}" href="{url(name)}">{art}<div class="topic-card-copy"><span class="eyebrow">{i+1:02d}</span><h3>{esc(name)}</h3><span class="arrow" aria-hidden="true">↗</span></div></a>')
 return '<div class="cards">'+''.join(items)+'</div>'
def paper(p):
 thumbnail=f'<img class="paper-illustration" src="{esc(p["image"],quote=True)}" alt="" loading="lazy">' if p.get('image') else ''
 tags=' '.join(f'<span class="tag">{esc(t)}</span>' for t in p['topics'])
 links=' '.join(f'<a href="{esc(l["url"],quote=True)}">{esc(l["label"])}</a>' for l in p['links'])
 return f'<article class="paper" data-year="{p["year"]}" data-topics="{esc("|".join(p["topics"]),quote=True)}"><div class="paper-year">{p["year"] or "—"}</div><div>{thumbnail}<div class="tags">{tags}</div><h3><a href="{esc(p["url"],quote=True)}">{esc(p["title"])}</a></h3><p class="authors">{esc(p["authors"])}</p><p class="venue">{esc(p["venue"])}</p><div class="paper-links">{links}</div></div></article>'
def papers(items):return '<div class="paper-list">'+''.join(paper(p) for p in items)+'</div>'
lookup={p['id']:p for p in D['publications']}
def content(name):
 raw=D['pages'][name]['html']
 for key,value in D['profile'].items():
  if isinstance(value,str):raw=raw.replace('{{'+key+'}}',esc(value,quote=True))
 raw=re.sub(r'<div data-paper="([^"]+)"></div>',lambda m:paper(lookup[m[1]]),raw)
 return raw
nav=[('index','Home'),('Research','Research'),('Publications','Publications'),('Talks','Talks'),('Teaching','Teaching'),('Software','Software'),('Biography','About'),('Contact','Contact')]
def render(name,title,body,group=None):
 active=group or name
 n=''.join(f'<a href="{url(k)}"'+(' aria-current="page"' if active==k else '')+f'>{v}</a>' for k,v in nav)
 profile=D['profile']
 values={
  'title':esc(title), 'name':esc(profile['name']),
  'description':esc(f"{profile['name']}, {profile['role']} at {profile['institution']}, {profile['department']}. {profile['focus']}."),
  'canonical':'https://maurice-filo.github.io/'+('' if name=='index' else url(name)),
  'institution':esc(profile['institution']), 'navigation':n, 'body':body,
  'focus':esc(profile['focus']), 'scholar':esc(profile['scholar']), 'cv':esc(profile['cv'])}
 page=(ROOT/'templates/base.html').read_text()
 for key,value in values.items():page=page.replace('{{'+key+'}}',value)

 (ROOT/(name+'.html')).write_text(page)
def heading(title,subtitle='',label='Explore'):
 return f'<section class="page-heading"><p class="eyebrow">{label}</p><h1>{esc(title)}</h1>'+ (f'<p class="lead">{esc(subtitle)}</p>' if subtitle else '')+'</section>'
def talk_date(value):
 """Accept YYYY, YYYY-MM, or YYYY-MM-DD without inventing missing precision."""
 if not isinstance(value,str) or not re.fullmatch(r'\d{4}(?:-\d{2})?(?:-\d{2})?',value):
  raise ValueError(f'Invalid talk date {value!r}; use YYYY, YYYY-MM, or YYYY-MM-DD')
 parts=[int(x) for x in value.split('-')]
 day=calendar_date(parts[0],parts[1] if len(parts)>1 else 1,parts[2] if len(parts)>2 else 1)
 label=str(day.year) if len(parts)==1 else day.strftime('%B %Y') if len(parts)==2 else f'{day.day} {day.strftime("%B %Y")}'
 return day,label

talk_ids=set()
for talk in D['talks']:
 for field in ['id','title','date','venue']:
  if not isinstance(talk.get(field),str) or not talk[field].strip():raise ValueError(f'Talk requires a nonempty {field}: {talk}')
 if not re.fullmatch(r'[a-zA-Z0-9_-]+',talk['id']):raise ValueError('Talk IDs must use letters, numbers, hyphens or underscores')
 if talk['id'] in talk_ids:raise ValueError(f'Duplicate talk ID: {talk["id"]}')
 if not isinstance(talk.get('show_in_news',False),bool):raise ValueError('show_in_news must be true or false, without quotation marks')
 talk_ids.add(talk['id']);talk_date(talk['date'])
D['talks'].sort(key=lambda t:talk_date(t['date'])[0],reverse=True)

def talk_card(talk):
 _,label=talk_date(talk['date'])
 thumb=f'<img class="paper-illustration" src="{esc(talk["image"],quote=True)}" alt="" loading="lazy">' if talk.get('image') else ''
 title=esc(talk['title'])
 if talk.get('slides_url'):title=f'<a href="{esc(talk["slides_url"],quote=True)}">{title}</a>'
 venue=esc(talk['venue'])
 if talk.get('venue_url'):venue=f'<a href="{esc(talk["venue_url"],quote=True)}">{venue}</a>'
 when=esc(talk.get('location',''))+(' · ' if talk.get('location') else '')+f'<time datetime="{esc(talk["date"])}">{esc(label)}</time>'
 resources=[{'label':label,'url':talk[key]} for key,label in [('slides_url','Slides'),('paper_url','Paper'),('video_url','Video')] if talk.get(key)]
 resources+=talk.get('links',[])
 links=' '.join(f'<a href="{esc(item["url"],quote=True)}">{esc(item["label"])}</a>' for item in resources)
 notes=f'<p>{talk["notes_html"]}</p>' if talk.get('notes_html') else ''
 return f'<article class="paper" id="{esc(talk["id"])}"><div class="paper-year">{esc(talk["date"][:4])}</div><div>{thumb}<h3>{title}</h3><p>{venue}</p><p class="venue">{when}</p>{notes}<div class="paper-links">{links}</div></div></article>'

def talks_body():
 groups={}
 for talk in D['talks']:groups.setdefault(talk.get('group','Conference & Invited Talks'),[]).append(talk)
 return ''.join(f'<section><h2>{esc(group)}</h2>'+''.join(talk_card(t) for t in talks)+'</section>' for group,talks in groups.items()) or '<p>No talks listed yet.</p>'

def news_sort_date(item):
 value=item.get('datetime','')
 if value:
  try:return talk_date(value)[0]
  except ValueError:pass
 value=item.get('date','')
 for fmt in ['%Y %b','%Y %B','%d %b %Y','%d %B %Y','%Y']:
  try:
   from datetime import datetime
   return datetime.strptime(value,fmt).date()
  except ValueError:pass
 return calendar_date.min

def all_news():
 """Merge opted-in talks with manual news; do not duplicate announcements."""
 featured=[t for t in D['talks'] if t.get('show_in_news',False)]
 items=[]
 for item in D['news']:
  duplicate=False
  for talk in featured:
   same_month=news_sort_date(item).strftime('%Y-%m')==talk['date'][:7]
   if item.get('talk_id')==talk['id'] or (talk.get('slides_url') and talk['slides_url'] in item.get('html','')) or (same_month and talk.get('venue_url') and talk['venue_url'] in item.get('html','')):
    duplicate=True;break
  if not duplicate:items.append(item)
 for talk in featured:
  _,label=talk_date(talk['date'])
  target='Talks.html#'+talk['id']
  detail=f'<a href="{esc(target,quote=True)}">{esc(talk["title"])}</a> — {esc(talk["venue"])}'
  if talk.get('location'):detail+=f', {esc(talk["location"])}'
  items.append({'date':label,'datetime':talk['date'],'headline':talk.get('news_headline') or 'Talk: '+talk['title'],'html':detail+'.'})
 return sorted(items,key=news_sort_date,reverse=True)

profile=D['profile']
hero=f'''<section class="hero-artwork"><img class="hero-science" src="{esc(profile['hero_image'])}" alt="Conceptual illustration emphasizing feedback-control systems, dynamic trajectories, and AI neural networks, with a subtle molecular motif" width="1600" height="594" fetchpriority="high"><div class="hero-caption"><div><p class="eyebrow">{esc(profile['role'])} · {esc(profile['institution'])}</p><h1>{esc(profile['name'])}</h1><p class="lead">{esc(profile['intro'])}</p><p class="affiliation"><a href="{esc(profile['department_url'])}">{esc(profile['department'])}</a> · <a href="{esc(profile['division_url'])}">{esc(profile['division'])}</a><br><a href="{esc(profile['group_url'])}">{esc(profile['group'])}</a> · Fellow of <a href="{esc(profile['college_url'])}">{esc(profile['college'])}</a></p><div class="actions"><a class="button" href="Research.html">Explore my research ↗</a><a class="button secondary" href="{esc(profile['cv'])}">View CV</a></div></div><img class="profile-portrait" src="{esc(profile['portrait'])}" alt="{esc(profile['name'])}" width="160" height="190"></div></section>'''

recent=[p for p in D['publications'] if p['featured']][:4]
def news_entry(item):
 date_attr=f' datetime="{esc(item["datetime"])}"' if item.get('datetime') else ''
 return f'<li><time{date_attr}>{esc(item["date"])}</time><div><h3>{esc(item["headline"])}</h3><p>{item["html"]}</p></div></li>'
news_entries=[news_entry(item) for item in all_news()]

home=hero+'<section><div class="section-title"><div><p class="eyebrow">Areas of inquiry</p><h2>Research</h2></div>'+link('Research','All research ↗')+'</div>'+cards(D['topics'])+'</section><section><div class="section-title"><div><p class="eyebrow">Selected work</p><h2>Recent publications</h2></div>'+link('Publications','All publications ↗')+'</div>'+papers(recent)+'</section><section class="news"><div class="section-title"><div><p class="eyebrow">Updates & milestones</p><h2>News</h2></div></div><ol>'+''.join(news_entries[:5])+'</ol><details><summary>Earlier updates</summary><ol>'+''.join(news_entries[5:])+'</ol></details></section>'
render('index','Home',home)
render('Research','Research',heading('Research','Control, dynamics, biology, and AI: mathematical ideas connected to real systems.')+cards(D['topics']))
render('Talks','Talks',heading('Talks','Conference presentations, invited seminars, and research talks.')+'<div class="prose">'+talks_body()+'</div>')
render('Teaching','Teaching',heading('Teaching','Courses, lecture notes, and practical resources.')+cards(D['courses']))
render('Software','Software',heading('Software','Tools for exploring, simulating, and designing dynamical systems.')+cards(D['software']))
filters='<div class="filters"><label>Search publications<input id="paper-search" type="search" placeholder="Title, author, or venue"></label><label>Research area<select id="topic-filter"><option value="">All research areas</option>'+''.join(f'<option>{esc(t)}</option>' for t in D['topics'])+'</select></label><label>Year<select id="year-filter"><option value="">All years</option>'+''.join(f'<option>{y}</option>' for y in sorted({p['year'] for p in D['publications'] if p['year']},reverse=True))+'</select></label></div><p id="result-count" role="status" aria-live="polite"></p>'
render('Publications','Publications',heading('Publications','Browse papers and preprints by research area, year, or keyword.')+filters+papers(D['publications'])+'<p class="empty" hidden>No publications match these filters.</p><p class="note">* These authors contributed equally to this work.</p><div class="prose">'+D['publication_appendix']+'</div>')
for name in D['pages']:
 if name=='Publications':continue
 group='Research' if name in D['topics'] or name=='Talks' else 'Teaching' if name in D['courses'] else 'Software' if name in D['software'] else name
 extra='<div class="subnav">'+''.join(link(n) for n in D['topics']+['Talks'])+'</div>' if group=='Research' else ''
 body=heading(name,label=group)+extra+'<div class="prose">'+content(name)+'</div>'
 if name in D['topics']:
  # New tagged publications are appended even if no legacy placement exists.
  placed=re.findall('data-paper="([^"]+)"',D['pages'][name]['html'])
  additional=[p for p in D['publications'] if name in p['topics'] and p['id'] not in placed]
  if additional:body+='<section><h2>Related publications</h2>'+papers(additional)+'</section>'
 render(name,name,body,group)
urls=list(dict.fromkeys(['index','Research','Publications','Talks','Teaching','Software']+list(D['pages'])))
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://maurice-filo.github.io/'+('' if n=='index' else url(n))+'</loc></url>' for n in urls)+'</urlset>')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://maurice-filo.github.io/sitemap.xml\n')
print(f'Built {len(urls)} pages from content sources')

"""Build the interactive career reading layer from the public story sources."""
from pathlib import Path
import json,html,re
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'content/profile.json').read_text());d=json.loads((R/'content/story-details.json').read_text());E=html.escape

def actions(st):
 return '<ol class="action-list">'+''.join('<li><h4>'+E(t)+'</h4><p>'+E(copy)+'</p></li>' for t,copy in d[st['id']]['actions'])+'</ol>'
def narrative(st):
 s=d[st['id']]
 return f'<p class="eyebrow">{E(st["company"])} · {E(st["tag"])}</p><h2>{E(st["title"])}</h2><p class="reader-framing">{E(s["framing"])}</p><p class="reader-outcome">{E(st["outcome"])}</p><section><h3>What made this hard</h3><p>{E(s["context"])}</p></section><section><h3>The choice I made</h3><p>{E(s["choice"])}</p></section><section><h3>What I did</h3>{actions(st)}</section><section><h3>What I took from it</h3><p>{E(s["lesson"])}</p></section><div class="story-skills" aria-label="Strengths demonstrated">'+''.join(f'<span>{E(k)}</span>' for k in s['skills'])+f'</div><a class="text-link" href="../stories/{st["id"]}.html">Open full story ↗</a>'

# The journey presents each achievement once, linked straight to its full story.
company_notes={
 'Cake by VPBank': {'role':'Senior Technical Product Manager (L5)', 'stories':[
  ('cake-ai','Drove AI banking roadmaps and transfer parsing; AI workflows cut PM preparation effort ~50%.'),
  ('cake-investment','Launched investment products contributing an estimated $100K in annual revenue.'),
  ('cake-risk','Built configurable risk controls, cutting deployment from days to ~1 hour.'),
  ('cake-travel','Launched an embeddable travel mini-app generating $45K in its first six months.')
 ]},
 'Fundiin': {'role':'Principal / Senior Product Manager', 'stories':[
  ('fundiin-lenders','Built a multi-lender platform, expanding monthly funding capacity 10× ($2M → $20M).'),
  ('fundiin-qr','QR Pay-Later reached 20K first-month users and 50% of loan volume in eight months.'),
  ('fundiin-core','Redesigned the core for 4× loan-volume growth and 30% lower operating costs.'),
  ('fundiin-ml-risk','ML risk screening halved manual review across a $2M monthly portfolio.')
 ]},
 'ZaloPay · VNG': {'role':'Product Manager / Associate PM', 'stories':[
  ('zalo-apis','Grew ride-hailing transactions 50%, payout volume 40%, and acquired 100K users through enterprise integrations.'),
  ('zalo-remittance','Launched cross-border remittance in six months, leading a 20-person team.'),
  ('zalo-payment-conversion','Improved payment conversion 20% through customer interviews, funnel analysis, and 10 A/B-tested experiments.')
 ]}
}
index=(R/'index.html').read_text()
logos={'Cake by VPBank':'cake','Fundiin':'fundiin','ZaloPay · VNG':'zalopay'}
company_html=''
highlights={'cake-ai':'AI banking','cake-investment':'$100K','cake-risk':'~1 hour','cake-travel':'$45K','fundiin-lenders':'10×','fundiin-qr':'50%','fundiin-core':'4×','fundiin-ml-risk':'halved manual review','zalo-apis':'100K users','zalo-remittance':'six months','zalo-payment-conversion':'20%'}
def achievement_text(sid,copy):
 return E(copy).replace(E(highlights[sid]),'<strong>'+E(highlights[sid])+'</strong>',1)
for exp in p['experience']:
 name=exp['organization'];note=company_notes[name]
 links=''.join(f'<li><a id="{sid}" href="stories/{sid}.html"><span>{achievement_text(sid,copy)}</span><span class="journey-arrow" aria-hidden="true">↗</span></a></li>' for sid,copy in note['stories'])
 company_html+=f'<article class="journey-step"><div class="journey-logo"><img src="assets/organizations/{logos[name]}.png" alt="" width="32" height="32"></div><header class="journey-company"><h3>{E(name)}</h3><p>{E(note["role"])}</p><span>{E(exp["period"])}</span></header><ul class="journey-achievements">{links}</ul></article>'
education_html=''
for i,x in enumerate(p['education']):
 school='Berkeley Haas' if i==0 else 'National Economics University'
 education_html+=f'<article class="journey-school"><div class="journey-school-name"><img src="assets/organizations/{"berkeley" if i==0 else "neu"}.png" alt="" width="28" height="28"><h3>{school}</h3></div><p class="journey-degree">{E(x["degree"])} · {E(x["graduation"])}</p><p class="journey-school-focus">{E(x["focus"])}</p></article>'
icon='<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="18" height="14" rx="3"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12c5 3 13 3 18 0M12 12v4"/></svg>'
home=f'<section id="experience" class="section journey-section" aria-labelledby="journey-heading"><header class="journey-heading"><h2 id="journey-heading">{icon}Professional journey</h2><a class="text-link" href="resume/">Interactive resume ↗</a></header><div class="journey-track">{company_html}</div><div class="journey-education"><p class="eyebrow">EDUCATION</p><div class="journey-schools">{education_html}</div></div></section>'
index=re.sub(r'<section id="experience".*?</section>(?=<section id="beyond")',lambda _:home,index,flags=re.S)
index=re.sub(r'<link rel="stylesheet" href="styles/career-stories\.css[^"]*">','',index)
index=re.sub(r'<link rel="stylesheet" href="styles/journey\.css[^"]*">','',index)
index=index.replace('</head>','<link rel="stylesheet" href="styles/journey.css"></head>')
(R/'index.html').write_text(index)

# Add concrete action sections to the standalone pages without repeating the old delivery paragraph.
for st in p['career_stories']:
 f=R/st['detail_page'];s=f.read_text()
 s=re.sub(r'<section class="detail-section" id="delivery">.*?</section>',lambda _: '<section class="detail-section" id="delivery"><h2>What I did</h2>'+actions(st)+'</section>',s,flags=re.S)
 s=s.replace('<nav class="case-jump"','<p class="story-reader-back"><a class="text-link" href="../resume/#'+st['id']+'">Read alongside my career overview ↗</a></p><nav class="case-jump"')
 f.write_text(s)

# A full HTML reading experience: native disclosure works before JavaScript enhances desktop selection.
groups=''
for exp in p['experience']:
 name=exp['organization'];stories=[st for st in p['career_stories'] if st['company']==name]
 logo={'Cake by VPBank':'cake','Fundiin':'fundiin','ZaloPay · VNG':'zalopay'}[name]
 groups+=f'<section class="resume-company"><header><img src="../assets/organizations/{logo}.png" alt="" width="30" height="30"><div><h2>{E(name)}</h2><p>{E(exp["role"])} · {E(exp["period"])}</p></div></header><ul class="resume-bullets">'
 for st in stories:
  groups+=f'<li><details class="resume-story" id="{st["id"]}"><summary><span>{E(d[st["id"]]["bullet"])}</span><span class="read-story-label">Story <span aria-hidden="true">↗</span></span></summary><div class="resume-inline">{narrative(st)}</div></details></li>'
 groups+=''.join('<li class="resume-plain-bullet">'+E(b)+'</li>' for b in exp.get('additional_bullets',[]))
 groups+='</ul></section>'
education=''.join(f'<article><h3>{E(x["school"])}</h3><p>{E(x["degree"])} · {E(x["graduation"])}</p><p>{E(x["focus"])}</p></article>' for x in p['education'])
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Interactive resume — Hieu Nguyen</title><meta name="description" content="The decisions behind my work in AI products, platforms, and new ventures. Explore the context, actions, and results behind each career bullet."><link rel="icon" href="../assets/favicon.svg"><link rel="stylesheet" href="../styles/main.css"><link rel="stylesheet" href="../styles/career-stories.css"><script src="../scripts/career-stories.js" defer></script></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="wordmark" href="../index.html" aria-label="Hieu Nguyen home">hieu<span class="wordmark-dot">.</span></a><nav aria-label="Main navigation"><a href="../index.html">← Personal website</a><a href="../index.html#work">Independent projects</a><a href="https://www.linkedin.com/in/hieu-ng-trung/">LinkedIn ↗</a></nav></header><main id="main" class="resume-main"><header class="resume-heading"><p class="eyebrow">INTERACTIVE RESUME</p><h1>Hieu Nguyen.</h1><p>AI products, platforms, and new ventures. The decisions behind the results—choose a career bullet to explore the problem, my actions, and the impact.</p></header><div class="resume-layout"><div class="resume-overview"><p class="resume-instruction"><span aria-hidden="true">●</span> Each blue marker opens the story behind a result.</p>{groups}<section class="resume-education"><h2>Education</h2>{education}</section></div><aside class="story-reader" aria-label="Story behind the selected career bullet"><div class="reader-toolbar"><p class="eyebrow">BEHIND THE BULLET</p><button type="button" id="close-story" hidden>Close ×</button></div><div id="reader-content"><div class="reader-empty"><span class="reader-symbol" aria-hidden="true">↗</span><h2>A result tells you what changed.<br>The story shows how I work.</h2><p>Start with a decision that interests you.</p><div class="reader-starters">'''+''.join(f'<button type="button" data-story="{sid}">{E(label)} <span aria-hidden="true">→</span></button>' for sid,label in [('fundiin-lenders','Removing a funding ceiling'),('fundiin-ml-risk','Making ML work for Risk'),('zalo-payment-conversion','Changing a hypothesis with research'),('cake-travel','Building a new revenue line')])+'''</div></div></div><p class="reader-status" role="status" aria-live="polite"></p></aside></div></main><footer><a class="wordmark" href="../index.html">hieu<span class="wordmark-dot">.</span></a><p>Product judgment, in context.</p><a href="../llms.txt">llms.txt ↗</a></footer></body></html>'''
(R/'resume').mkdir(exist_ok=True);(R/'resume/index.html').write_text(page)
# Shared action typography also styles the full career pages.
for f in list((R/'stories').glob('*.html')):
 s=f.read_text()
 if 'styles/career-stories.css' not in s:
  prefix='' if f.name=='index.html' else '../'
  s=s.replace('</head>',f'<link rel="stylesheet" href="{prefix}styles/career-stories.css"></head>')
 f.write_text(s)
print('Built interactive career overview, homepage contributions, and detailed action narratives.')

# Give changed spacing styles a fresh URL so existing visitors receive the update.
import hashlib
style_version=hashlib.sha256((R/'styles/career-stories.css').read_bytes()).hexdigest()[:10]
for file in [R/'resume/index.html', *list((R/'stories').glob('*.html'))]:
 text=file.read_text()
 text=re.sub(r'(styles/career-stories\.css)(?:\?v=[a-f0-9]+)?',lambda m:m[1]+'?v='+style_version,text)
 file.write_text(text)

journey_version=hashlib.sha256((R/'styles/journey.css').read_bytes()).hexdigest()[:10]
f=R/'index.html';text=f.read_text();text=text.replace('styles/journey.css"','styles/journey.css?v='+journey_version+'"');f.write_text(text)

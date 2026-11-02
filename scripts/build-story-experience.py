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

company_notes={
'Cake by VPBank':('AI banking, new revenue lines, and the platforms behind them.', ['~80% correct transfer prefilling','$45K travel revenue / six months','Days → ~1 hour for risk controls'], [('Selected the opportunity','Shaped stock trading and travel around a commercial case, then sequenced the first releases.'),('Designed the operating model','Connected customer journeys with partner responsibilities, platform boundaries, and internal workflows.'),('Made AI useful in practice','Shipped transfer parsing and enabled PMs to prototype and prepare product work with AI.')]),
'Fundiin':('New credit experiences backed by scalable lending infrastructure.', ['$2M → $20M funding capacity','50% loan share / QR Pay-Later','50% less manual risk review'], [('Removed the funding ceiling','Designed the multi-lender product model and partner integrations, including fund flows and reconciliation.'),('Validated before rebuilding','Launched QR Pay-Later on the existing core to test demand, then led a phased platform redesign.'),('Connected ML to operations','Aligned evaluation, thresholds, shadow testing, and human review with Risk and Data Science.')]),
'ZaloPay · VNG':('Enterprise payment growth through partner products and customer evidence.', ['+50% ride-hailing transactions','Six-month remittance launch','+20% payment conversion'], [('Turned partnerships into capabilities','Led collection, payout, and pre-authorization integrations across enterprise use cases.'),('Aligned a regulated launch','Connected overseas partners to domestic fund flows and led cross-functional remittance delivery.'),('Changed course with evidence','Combined funnel analysis and interviews to prioritize reliability before experimenting on the interface.')])}
index=(R/'index.html').read_text()
def improve_company(m):
 card=m[0];name=html.unescape(re.search('<h3>(.*?)</h3>',card)[1]);note,chips,work=company_notes[name]
 card=re.sub(r'<div class="company-highlights">.*?</div><details class="contribution-preview">.*?</details>','',card,flags=re.S)
 card=re.sub(r'<p class="experience-summary">.*?</p>',lambda _:f'<p class="experience-summary">{E(note)}</p>',card,flags=re.S)
 extra='<div class="company-highlights">'+''.join('<span>'+E(x)+'</span>' for x in chips)+'</div><details class="contribution-preview"><summary>What I did <span aria-hidden="true">+</span></summary><ul>'+''.join('<li><strong>'+E(t)+'.</strong> '+E(copy)+'</li>' for t,copy in work)+'</ul></details>'
 card=card.replace('<details class="story-collection">',extra+'<details class="story-collection">')
 return card
index=re.sub(r'<article class="company-card">.*?</article>',improve_company,index,flags=re.S)
index=re.sub(r'<p class="career-reader-link">.*?</p>','',index,flags=re.S)
index=index.replace('<div class="history-layout">','<p class="career-reader-link"><a class="text-link" href="resume/">Read the story behind each career bullet ↗</a></p><div class="history-layout">')
index=index.replace('<a href="index.html#experience">Experience</a>', '<a href="index.html#experience">Experience</a><a href="resume/">Résumé</a>') if '<a href="resume/">Résumé</a>' not in index else index
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
 groups+='</ul></section>'
education=''.join(f'<article><h3>{E(x["school"])}</h3><p>{E(x["degree"])} · {E(x["graduation"])}</p><p>{E(x["focus"])}</p></article>' for x in p['education'])
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Career stories — Hieu Nguyen</title><meta name="description" content="The decisions behind my work in AI products, platforms, and new ventures. Explore the context, actions, and results behind each career bullet."><link rel="icon" href="../assets/favicon.svg"><link rel="stylesheet" href="../styles/main.css"><link rel="stylesheet" href="../styles/career-stories.css"><script src="../scripts/career-stories.js" defer></script></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="wordmark" href="../index.html" aria-label="Hieu Nguyen home">hieu<span class="wordmark-dot">.</span></a><nav aria-label="Main navigation"><a href="../index.html">← Personal website</a><a href="../index.html#work">Independent projects</a><a href="https://www.linkedin.com/in/hieu-ng-trung/">LinkedIn ↗</a></nav></header><main id="main" class="resume-main"><header class="resume-heading"><p class="eyebrow">INTERACTIVE RÉSUMÉ</p><h1>Hieu Nguyen.</h1><p>AI products, platforms, and new ventures. The decisions behind the results—choose a career bullet to explore the problem, my actions, and the impact.</p></header><div class="resume-layout"><div class="resume-overview"><p class="resume-instruction"><span aria-hidden="true">●</span> Each blue marker opens the story behind a result.</p>{groups}<section class="resume-education"><h2>Education</h2>{education}</section></div><aside class="story-reader" aria-label="Story behind the selected career bullet"><div class="reader-toolbar"><p class="eyebrow">BEHIND THE BULLET</p><button type="button" id="close-story" hidden>Close ×</button></div><div id="reader-content"><div class="reader-empty"><span class="reader-symbol" aria-hidden="true">↗</span><h2>A result tells you what changed.<br>The story shows how I work.</h2><p>Start with a decision that interests you.</p><div class="reader-starters">'''+''.join(f'<button type="button" data-story="{sid}">{E(label)} <span aria-hidden="true">→</span></button>' for sid,label in [('fundiin-lenders','Removing a funding ceiling'),('fundiin-ml-risk','Making ML work for Risk'),('zalo-payment-conversion','Changing a hypothesis with research'),('cake-travel','Building a new revenue line')])+'''</div></div></div><p class="reader-status" role="status" aria-live="polite"></p></aside></div></main><footer><a class="wordmark" href="../index.html">hieu<span class="wordmark-dot">.</span></a><p>Product judgment, in context.</p><a href="../llms.txt">llms.txt ↗</a></footer></body></html>'''
(R/'resume').mkdir(exist_ok=True);(R/'resume/index.html').write_text(page)
# Shared action typography also styles the full career pages.
for f in [R/'index.html',*list((R/'stories').glob('*.html'))]:
 s=f.read_text()
 if 'styles/career-stories.css' not in s:
  prefix='' if f.name=='index.html' else '../'
  s=s.replace('</head>',f'<link rel="stylesheet" href="{prefix}styles/career-stories.css"></head>')
 f.write_text(s)
print('Built interactive career overview, homepage contributions, and detailed action narratives.')

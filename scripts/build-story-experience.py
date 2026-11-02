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
 'Cake by VPBank': {
  'focus':'AI-first banking, platforms, and commercial new ventures.',
  'role':'Senior Technical Product Manager (L5)',
  'outcomes':[('AI-first banking','LLM roadmaps, a shipped transfer experience, and 10+ PMs enabled.'),('New revenue','$100K estimated annual investment revenue; $45K from travel in six months.'),('Operating leverage','Risk-control deployment cut from days to about one hour.')]
 },
 'Fundiin': {
  'focus':'0-to-1 credit products and the lending infrastructure to scale them.',
  'role':'Principal / Senior Product Manager',
  'outcomes':[('10× funding capacity','$2M → $20M through a scalable multi-lender platform.'),('0-to-1 growth','QR Pay-Later reached 50% of loan volume within eight months.'),('Core transformation','4× loan-volume growth and 30% lower operating costs.')]
 },
 'ZaloPay · VNG': {
  'focus':'Enterprise payments, new markets, and customer-led growth.',
  'role':'Product Manager / Associate Product Manager',
  'outcomes':[('Enterprise growth','+50% ride-hailing transactions, +40% payout volume, and 100K users acquired.'),('Market entry','Cross-border remittance launched in six months with a 20-person team.'),('Customer evidence','+20% payment conversion through research and experiments.')]
 }
}
index=(R/'index.html').read_text()
logos={'Cake by VPBank':'cake','Fundiin':'fundiin','ZaloPay · VNG':'zalopay'}
company_html=''
for exp in p['experience']:
 name=exp['organization'];note=company_notes[name];selected=[x for x in p['career_stories'] if x['company']==name]
 previews=''
 for st in selected:
  previews+=f'<details class="career-story" id="{st["id"]}"><summary><span><small>{E(st["tag"])}</small>{E(st["title"])}</span><b aria-hidden="true">+</b></summary><div class="story-body"><p>{E(st["problem"])}</p><h4>My contribution</h4><p>{E(st["decision"])}</p><h4>Impact</h4><p>{E(st["outcome"])}</p><a class="text-link" href="resume/#{st["id"]}">Explore this story in my resume ↗</a><a class="text-link full-page-link" href="{st["detail_page"]}">Open full page ↗</a></div></details>'
 company_html+=f'<article class="company-card"><div class="company-top"><span class="organization-logo"><img src="assets/organizations/{logos[name]}.png" alt="" width="32" height="32"></span><div><h3>{E(name)}</h3><p class="entry-meta">{E(note["role"])}</p><p class="entry-period">{E(exp["period"])}</p></div></div><p class="experience-summary">{E(note["focus"])}</p><ul class="company-outcomes">'+''.join(f'<li><p><span>{E(title)}.</span> {E(copy)}</p></li>' for title,copy in note['outcomes'])+f'</ul><details class="story-collection"><summary>Explore {len(selected)} work stories <span aria-hidden="true">+</span></summary><div class="company-stories">{previews}</div></details></article>'
education_html=''
for i,x in enumerate(p['education']):
 school='Berkeley Haas' if i==0 else 'National Economics University'
 education_html+=f'<article class="education-entry"><div class="education-top"><img src="assets/organizations/{"berkeley" if i==0 else "neu"}.png" alt="" width="32" height="32"><div><h3>{school}</h3><p class="entry-meta">{E(x["degree"])} · {E(x["graduation"])}</p></div></div><p class="education-summary">{E(x["focus"])}</p></article>'
home=f'<section id="experience" class="section background-section"><div class="history-heading"><div><p class="eyebrow">EXPERIENCE & EDUCATION</p><h2>Product leadership, in practice.</h2></div><a class="text-link" href="resume/">Explore my interactive resume ↗</a></div><div class="career-history">{company_html}</div><div class="history-education"><h3 class="column-label">Education</h3><div class="education-grid">{education_html}</div></div></section>'
index=re.sub(r'<section id="experience".*?</section>(?=<section id="beyond")',lambda _:home,index,flags=re.S)
index=index.replace('<a href="index.html#experience">Experience</a>', '<a href="index.html#experience">Experience</a><a href="resume/">Resume</a>') if '<a href="resume/">Resume</a>' not in index and '<a href="resume/">Resume</a>' not in index else index
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
for f in [R/'index.html',*list((R/'stories').glob('*.html'))]:
 s=f.read_text()
 if 'styles/career-stories.css' not in s:
  prefix='' if f.name=='index.html' else '../'
  s=s.replace('</head>',f'<link rel="stylesheet" href="{prefix}styles/career-stories.css"></head>')
 f.write_text(s)
print('Built interactive career overview, homepage contributions, and detailed action narratives.')

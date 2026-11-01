from pathlib import Path
import json,html,re
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'content/profile.json').read_text());details=json.loads((R/'content/project-details.json').read_text());stories=json.loads((R/'content/story-details.json').read_text())
E=html.escape
roles={'human':'Human','ai':'AI / LLM','code':'Code & rules','tools':'Tools & data','method':'Method'}
def head(title,description):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} — Hieu Nguyen</title><meta name="description" content="{E(description,quote=True)}"><meta name="theme-color" content="#f7f8fc"><meta property="og:title" content="{E(title,quote=True)} — Hieu Nguyen"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:type" content="article"><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../styles/main.css"><link rel="alternate" type="text/markdown" href="../profile.md" title="Text profile"></head><body><a class="skip-link" href="#main">Skip to content</a>'''
def nav():
 return '''<header class="site-header"><a class="wordmark" href="../index.html" aria-label="Hieu Nguyen home">hieu<span class="wordmark-dot">.</span></a><nav aria-label="Main navigation"><a href="../index.html#top">Profile</a><a href="../index.html#work">Projects</a><a href="../index.html#experience">Experience</a><a href="https://substack.com/@hieutnguyen">Blog ↗</a><a href="../index.html#contact">Connect ↗</a></nav></header>'''
def footer():
 return '''<footer><a class="wordmark" href="../index.html">hieu<span class="wordmark-dot">.</span></a><p>Curiosity, craft, and a wider perspective.</p><a href="../llms.txt">llms.txt ↗</a></footer></body></html>'''
def flow(d):
 steps=''
 for i,(owners,title,body,tools) in enumerate(d['steps'],1):
  badges=''.join(f'<span class="owner owner-{owner}">{roles[owner]}</span>' for owner in owners)
  steps+=f'<li><div class="flow-step-top"><span class="flow-number">{i:02}</span><div class="flow-owners">{badges}</div></div><h3>{E(title)}</h3><p>{E(body)}</p><small>{E(tools)}</small></li>'
 return f'<section class="flow-panel" id="system-flow" aria-labelledby="flow-heading"><p class="eyebrow">SYSTEM FLOW</p><h2 id="flow-heading">{E(d["flow_title"])}</h2><p class="flow-intro">{E(d["flow_note"])}</p><ol class="system-flow">{steps}</ol></section>'
for i,x in enumerate(p['projects']):
 d=details[x['slug']];tags=''.join(f'<span>{E(t)}</span>' for t in x['stack'])
 body=f'''<main id="main" class="detail-main"><a class="text-link" href="../index.html#work">← All selected work</a><header class="detail-heading"><p class="eyebrow">{E(x['category'])} / INDEPENDENT PROJECT</p><h1>{E(x['title'])}</h1><p class="detail-lede">{E(d['lede'])}</p><div class="tech-tags" aria-label="Technology stack">{tags}</div><nav class="case-jump" aria-label="On this page"><a href="#problem">Problem</a><a href="#system-flow">System flow</a><a href="#decisions">Decisions</a><a href="#outcome">Outcome</a></nav></header><div class="project-intro-grid"><section id="problem"><h2>{'The personal starting point' if i==0 else 'The product problem'}</h2><p>{E(d['problem'])}</p></section><figure class="detail-preview"><a href="../{x['image']}" aria-label="Open full-size {E(x['title'],quote=True)} image"><img src="../{x['image']}" alt="{E(x['title'],quote=True)} — {E(x['image_note'],quote=True)}"></a><figcaption>{E(x['image_note'])} · click to enlarge</figcaption></figure></div><section class="detail-section"><h2>The approach</h2><p>{E(d['approach'])}</p></section>{flow(d)}<section class="detail-section" id="decisions"><p class="eyebrow">PRODUCT & SYSTEM DECISIONS</p><div class="decision-grid">'''
 body+=''.join(f'<article><h3>{E(title)}</h3><p>{E(copy)}</p></article>' for title,copy in d['decisions'])
 body+=f'''</div></section><section class="detail-section outcome-section" id="outcome"><h2>{'Where it stands' if i==0 else 'What the work shows'}</h2><p>{E(d['outcome'])}</p><p class="detail-takeaway">{E(d['lesson'])}</p></section><div class="case-actions">'''
 if x.get('demo'):body+=f'<a class="button primary" href="{x["demo"]}">Open the dashboard ↗</a>'
 body+=f'<a class="text-link" href="{x["repo"]}">Explore the repository ↗</a></div><section class="source-links" aria-label="Project sources"><span>Go deeper:</span>'+''.join(f'<a href="{url}">{E(label)} ↗</a>' for label,url in d['sources'])+'</section>'
 other=p['projects'][(i+1)%len(p['projects'])]
 body+=f'<a class="next-project text-link" href="{other["slug"]}.html">Next: {E(other["title"])} →</a></main>'
 (R/f'projects/{x["slug"]}.html').write_text(head(x['title'],d['lede'])+nav()+body+footer())
 # Keep public summaries and machine-readable status current.
 x['problem']=d['problem'];x['approach']=d['approach'];x['detail_page']='projects/'+x['slug']+'.html'
 if i==0:x['evidence']='The repository includes the implementation, product decisions, and walkthroughs using synthetic data. Live deployment is on the way.'

index=(R/'index.html').read_text()
def refresh_company(match):
 card=match[0]
 name=html.unescape(re.search(r'<h3>(.*?)</h3>',card,re.S)[1])
 company=next(x for x in p['experience'] if x['organization']==name)
 card=re.sub(r'<p class="experience-summary">.*?</p>',lambda _: '<p class="experience-summary">'+E(company['summary'])+'</p>',card,flags=re.S)
 selected=[x for x in p['career_stories'] if x['company']==name]
 previews=''
 for st in selected:
  previews+=f'<details class="career-story" id="{st["id"]}"><summary><span><small>{E(st["tag"])}</small>{E(st["title"])}</span><b aria-hidden="true">+</b></summary><div class="story-body"><div class="story-result"><strong>{E(st["metric"])}</strong><span>{E(st["metric_label"])}</span></div><div><h4>The challenge</h4><p>{E(st["problem"])}</p><h4>My decision & contribution</h4><p>{E(st["decision"])}</p><h4>The result</h4><p>{E(st["outcome"])}</p></div></div></details>'
 prefix=card[:card.index('<details class="story-collection">')]
 return prefix+f'<details class="story-collection"><summary>Explore {len(selected)} product stories <span aria-hidden="true">+</span></summary><div class="company-stories">'+previews+'</div></details></article>'
index=re.sub(r'<article class="company-card">.*?</article>',refresh_company,index,flags=re.S)
for i,st in enumerate(p['career_stories']):
 d=stories[st['id']];path='stories/'+st['id']+'.html';st['detail_page']=path
 # Preserve native expansions; add a page link after the preview narrative.
 pattern=r'(<details class="career-story" id="'+re.escape(st['id'])+r'">)(.*?)(</details>)'
 def attach(m):
  content=re.sub(r'<p class="full-story-link">.*?</p>','',m[2],flags=re.S)
  return m[1]+content+f'<p class="full-story-link"><a class="text-link" href="{path}">Read the full story →</a></p>'+m[3]
 index=re.sub(pattern,attach,index,flags=re.S)
 body=f'''<main id="main" class="detail-main story-page"><a class="text-link" href="../index.html#experience">← Experience & education</a><header class="detail-heading"><p class="eyebrow">{E(st['company'])} / {E(st['tag'])}</p><h1>{E(st['title'])}</h1><p class="detail-lede">{E(d['framing'])}</p><p class="story-outcome">{E(st['outcome'])}</p><nav class="case-jump" aria-label="On this page"><a href="#context">Context</a><a href="#decision">Decision</a><a href="#delivery">Execution</a><a href="#result">Result</a></nav></header><section class="detail-section" id="context"><h2>The constraint</h2><p>{E(d['context'])}</p></section><section class="detail-section" id="decision"><h2>The decision I made</h2><p>{E(d['choice'])}</p></section><section class="decision-flow" aria-label="Conceptual product flow"><p class="eyebrow">THE PRODUCT LOGIC</p><ol>'''+''.join(f'<li><span>{n+1:02}</span>{E(step)}</li>' for n,step in enumerate(d['flow']))+f'''</ol></section><section class="detail-section" id="delivery"><h2>How I drove it forward</h2><p>{E(d['delivery'])}</p></section><section class="detail-section outcome-section" id="result"><h2>What changed</h2><p>{E(st['outcome'])}</p><p class="detail-takeaway">{E(d['lesson'])}</p></section><a class="text-link" href="../index.html#{st['id']}">Return to the concise story ↗</a>'''
 nxt=p['career_stories'][(i+1)%len(p['career_stories'])]
 body+=f'<a class="next-project text-link" href="{nxt["id"]}.html">Next story: {E(nxt["title"])} →</a></main>'
 (R/path).write_text(head(st['title'],d['framing'])+nav()+body+footer())

# Machine-readable summaries link to the full, crawlable pages.
md=f'# Hieu Nguyen\n\n{p["headline"]}\n\n{p["introduction"]}\n\n{p["about"]}\n\n## Professional background\n\n'
for x in p['experience']:md+=f'### {x["organization"]}\n\n{x["role"]} | {x["period"]}\n\n{x["summary"]}\n\n'
md+='## Education\n\n'
for x in p['education']:md+=f'### {x["school"]}\n\n{x["degree"]} | {x["graduation"]}\n\n{x["focus"]}\n\n'
md+='## Independent projects\n\n'
for x in p['projects']:md+=f'### {x["title"]}\n\n{x["summary"]}\n\n{x["problem"]}\n\n{x["approach"]}\n\nStack: {", ".join(x["stack"])}.\n\nStatus: {x["status"]}. {x["evidence"]}\n\n[Full case study]({x["detail_page"]}) · [Repository]({x["repo"]})\n\n'
md+='## Selected professional stories\n\n'
for x in p['career_stories']:md+=f'### {x["company"]} — {x["title"]}\n\nChallenge: {x["problem"]}\n\nMy contribution: {x["decision"]}\n\nResult: {x["outcome"]}\n\n[Full decision story]({x["detail_page"]})\n\n'
md+='## Interests\n\n'+', '.join(p['interests'])+'\n\n## Links\n\n'+'\n'.join(f'- {k.title()}: {v}' for k,v in p['links'].items())+'\n\n'+p['content_note']+'\n'
(R/'profile.md').write_text(md);(R/'content/profile.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
index=re.sub(r'(<pre id="profile-text"[^>]*>).*?(</pre>)',lambda m:m[1]+E(md)+m[2],index,flags=re.S)
(R/'index.html').write_text(index)
(R/'llms.txt').write_text('# Hieu Nguyen\n\nProduct leader working across AI products, platforms, and new ventures. Berkeley Haas MBA, May 2028.\n\n## Profiles\n\n- [Text profile](profile.md)\n- [Structured profile](content/profile.json)\n\n## Independent project case studies\n\n'+''.join(f'- [{x["title"]}]({x["detail_page"]}): problem, tools, human/AI/code roles, system flow, decisions, and outcome.\n' for x in p['projects'])+'\n## Professional decision stories\n\n'+''.join(f'- [{x["company"]}: {x["title"]}]({x["detail_page"]})\n' for x in p['career_stories'])+'\nUse repository links for detailed implementation evidence. Distinguish professional work from independent projects and aspirations from achieved outcomes.\n')
print(f'Built {len(p["projects"])} project case studies and {len(p["career_stories"])} career stories; linked expansions and synchronized profile sources.')

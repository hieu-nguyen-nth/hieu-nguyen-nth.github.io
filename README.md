# Hieu Nguyen — personal website

Personal website: https://hieu-nguyen-nth.github.io/

A static HTML/CSS/JavaScript site hosted with GitHub Pages from the root of the `main` branch. For local preview, start from this folder with `python3 -m http.server 4173 --bind 127.0.0.1`.

## Files

- `index.html`: personal introduction, independent projects, experience and education, interests, contact, and Machine view.
- `projects/`: independent project detail pages.
- `styles/main.css`: a single stylesheet with responsive typography, spacing, and accessibility states.
- `scripts/main.js`: Human/Machine switching, copying, and story hash links.
- `assets/`: focus diagram, actual project previews, and organization icons.
- `content/profile.json`, `profile.md`, `llms.txt`: structured and plain-text profile sources.
- Local provenance notes and review screenshots are excluded from the public repository.

## Content and design decisions

Positioning: a product leader connecting AI products, platform architecture, and commercial decisions. The Venn represents AI products, platforms, and new ventures. It is a personal focus diagram, not a generic PM framework.

Keep independent builds separate from employment. Background summaries should explain ownership and decisions rather than repeat resume bullets; detailed stories remain opt-in. Education receives the same font hierarchy and reading size as experience. Use restrained weight, consistent type, compact but comfortable spacing, and borderless organization icons. Do not substitute oversized metrics or generic slogans for useful information. Desktop projects use three equal columns. Preserve accessibility, readable mobile type, and the Machine view.

Facts come from the resume supplied November 1, 2026, career-story materials, and linked repositories. Update HTML, JSON, and Markdown together. Do not invent a portrait, resume download, or email address.

## Detail-page content and build

`content/project-details.json` holds project narratives, role-labeled system flows, design decisions, and source links. `content/story-details.json` holds the eleven professional decision stories. Run `python3 scripts/build-detail-pages.py` after editing these files. It regenerates the detail pages, links homepage achievements directly to career stories, and synchronizes the text/JSON profiles.

Theme: blue with restrained gold accents and a consistent system sans-serif. Green inside actual product screenshots belongs to the demonstrated product, not the portfolio theme. Keep the homepage concise; put useful depth, role boundaries, and implementation tradeoffs on the detail pages.

Spacing preference: keep text and story previews concise, with a moderate visual pause between major sections and more separation around interests/contact. Cake coverage includes stock trading and travel as commercial new ventures, alongside AI and risk.

## Publishing updates

Edit the source files, run `python3 scripts/build-detail-pages.py`, review locally, then commit and push to `main`. GitHub Pages automatically republishes the site. `.nojekyll` serves the prepared static files directly.

## Interactive career stories

`resume/index.html` pairs eleven career bullets with a desktop story reader; smaller screens use inline native disclosures. The same stories remain accessible as standalone pages. Homepage company entries form a connected journey with eleven concise achievements linked directly to full story pages. There are no homepage disclosure menus; education sits in a unified band below. `content/story-details.json` stores the specific actions and strengths; `scripts/build-story-experience.py` is called by the detail-page builder. Keep narrative claims grounded in the master story bank, with estimates and role boundaries intact.

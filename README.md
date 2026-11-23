# Rajiya Risha — Official Site

Official website of **Rajiya Risha**, Islamic vocalist (nasheed · hamd · naat) — https://rajiyarisha.com

Hosted on GitHub Pages. Five languages, each with its own page:
`/` English · `/bn/` বাংলা · `/hi/` हिन्दी · `/ur/` اردو · `/ar/` العربية

## How to edit
1. Edit **`src/template.html`** — never the generated `index.html` / `bn/` / `hi/` / `ur/` / `ar/` files.
   - Videos: search for `const VIDEOS` (YouTube IDs; titles & thumbnails load automatically)
   - Events: `const EVENTS`
   - All text in all languages: `const I18N`
   - Page titles/descriptions per language: top of `build.py`
2. Run `python3 build.py` (needs Python 3 + Node.js). It rebuilds all language pages and `sitemap.xml`.
3. Commit & push — the site updates in 1–2 minutes.

## SEO included
Per-language titles & descriptions, `hreflang` alternates, canonical URLs, Open Graph / Twitter cards,
schema.org `WebSite` + `Person` structured data, multilingual `sitemap.xml`, `robots.txt`, favicons (48/96/192/512),
web manifest, 404 page.

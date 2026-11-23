#!/usr/bin/env python3
"""Build the language pages of rajiyarisha.com from src/template.html.

Edit src/template.html (layout, CSS, JS and all translations live there), then run:

    python3 build.py

It writes:  index.html (English), bn/index.html, hi/index.html, ur/index.html,
ar/index.html and sitemap.xml. Each page has its text pre-translated in the HTML,
so Google can read and index every language separately.
Needs Python 3 and Node.js (Node is used only to read the translation table).
"""
import json, re, subprocess, datetime, pathlib, html

ROOT = pathlib.Path(__file__).parent
SITE = "https://rajiyarisha.com"
TPL = (ROOT / "src/template.html").read_text(encoding="utf-8")

LANGS = {
    "en": dict(path="/",    dir="ltr", og="en_US", hreflang="en",
               title="Rajiya Risha – Official Site",
               desc="Official site of Rajiya Risha — Bangladeshi Islamic vocalist. Nasheed, hamd & naat: new releases, music videos, live mahfils and bookings.",
               fonts="family=Instrument+Serif:ital@0;1&family=Manrope:wght@300;400;500;600;700&family=Amiri:wght@400;700"),
    "bn": dict(path="/bn/", dir="ltr", og="bn_BD", hreflang="bn",
               title="রাজিয়া রিশা – অফিসিয়াল সাইট | Rajiya Risha",
               desc="রাজিয়া রিশা (Rajiya Risha)-র অফিসিয়াল ওয়েবসাইট — বাংলাদেশি ইসলামী সংগীত শিল্পী। নাশীদ, হামদ, নাত ও গজল: নতুন ভিডিও, লাইভ মাহফিল ও বুকিং।",
               fonts="family=Instrument+Serif:ital@0;1&family=Hind+Siliguri:wght@300;400;500;600&family=Amiri:wght@400;700"),
    "hi": dict(path="/hi/", dir="ltr", og="hi_IN", hreflang="hi",
               title="राजिया रिशा – आधिकारिक साइट | Rajiya Risha",
               desc="राजिया रिशा (Rajiya Risha) की आधिकारिक वेबसाइट — बांग्लादेश की इस्लामी गायिका। नशीद, हम्द और नात: नए वीडियो, लाइव महफ़िल और बुकिंग।",
               fonts="family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;600&family=Noto+Sans+Devanagari:wght@400;500;600&family=Noto+Serif+Devanagari:wght@400;500&family=Amiri:wght@400;700"),
    "ur": dict(path="/ur/", dir="rtl", og="ur_PK", hreflang="ur",
               title="رضیہ ریشا – آفیشل سائٹ | Rajiya Risha",
               desc="رضیہ ریشا (Rajiya Risha) کی آفیشل ویب سائٹ — بنگلہ دیش کی اسلامی گلوکارہ۔ نشید، حمد اور نعت: نئی ویڈیوز، لائیو محافل اور بکنگ۔",
               fonts="family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;600&family=Noto+Nastaliq+Urdu:wght@400;600&family=Amiri:wght@400;700"),
    "ar": dict(path="/ar/", dir="rtl", og="ar_AR", hreflang="ar",
               title="رضية ريشا – الموقع الرسمي | Rajiya Risha",
               desc="الموقع الرسمي لـ رضية ريشا (Rajiya Risha) — منشدة إسلامية من بنغلاديش. أناشيد وحمد ونعت: أحدث الفيديوهات والمحافل الحيّة والحجز.",
               fonts="family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;600&family=Noto+Naskh+Arabic:wght@400;500;600&family=Amiri:wght@400;700"),
}

# --- read the I18N table out of the template's <script> using Node ----------------
m = re.search(r"const I18N=(\{.*?\n\});", TPL, re.S)
I18N = json.loads(subprocess.check_output(["node", "-e", f"process.stdout.write(JSON.stringify({m.group(1)}))"]))

hreflang = "\n".join(
    [f'<link rel="alternate" hreflang="{c["hreflang"]}" href="{SITE}{c["path"]}">' for c in LANGS.values()]
    + [f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'])

def translate(page, lang):
    d = I18N[lang]
    def rep(mt):
        tag, attrs, key = mt.group(1), mt.group(2), mt.group(3)
        if key not in d: return mt.group(0)
        n = re.search(r'data-n="(\d+)"', attrs)
        txt = d[key].replace("{n}", n.group(1) if n else "")
        return f"<{tag}{attrs}>{txt}</{tag}>"
    # <tag ... data-i18n="key" ...>text</tag>  (no nested tags of the same name)
    return re.sub(r'<(span|option|div|a|b|p|small|em|h\d)((?:(?!>)[^>])*?data-i18n="(\w+)"[^>]*)>(.*?)</\1>', rep, page, flags=re.S)

for lang, c in LANGS.items():
    url = SITE + c["path"]
    og = f'<meta property="og:locale" content="{c["og"]}">\n' + "\n".join(
        f'<meta property="og:locale:alternate" content="{o["og"]}">' for k, o in LANGS.items() if k != lang)
    fonts = f'<link href="https://fonts.googleapis.com/css2?{c["fonts"]}&display=swap" rel="stylesheet">'
    page = (TPL.replace("{{LANG}}", lang).replace("{{DIR}}", c["dir"])
               .replace("{{TITLE}}", html.escape(c["title"], quote=True))
               .replace("{{DESC}}", html.escape(c["desc"], quote=True))
               .replace("{{URL}}", url).replace("{{HREFLANG}}", hreflang)
               .replace("{{OGLOCALE}}", og).replace("{{FONTS}}", fonts))
    cut = page.rfind("<script>")          # translate the HTML only, not the page script
    page = translate(page[:cut], lang) + page[cut:]
    out = ROOT / c["path"].strip("/") / "index.html" if lang != "en" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))

# --- sitemap with language alternates ---------------------------------------------
today = datetime.date.today().isoformat()
alts = "\n".join(f'    <xhtml:link rel="alternate" hreflang="{c["hreflang"]}" href="{SITE}{c["path"]}"/>' for c in LANGS.values())
alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
urls = "\n".join(f"""  <url>
    <loc>{SITE}{c["path"]}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if k == "en" else "0.9"}</priority>
{alts}
  </url>""" for k, c in LANGS.items())
(ROOT / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{urls}
</urlset>
""", encoding="utf-8")
print("wrote sitemap.xml")

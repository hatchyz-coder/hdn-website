#!/usr/bin/env bash
set -eu

rm -rf _site
mkdir -p _site

cp index.html _site/
cp self-pay.html _site/
cp lhub.html _site/
cp consultation.html _site/
cp -R assets _site/assets
if [ -d en ]; then
  cp -R en _site/en
fi
if [ -f CNAME ]; then
  cp CNAME _site/CNAME
fi

python3 - <<'PY'
from pathlib import Path
import re

fixes = '''  <link rel="icon" type="image/svg+xml" href="assets/favicon-hdn.svg">
  <link rel="stylesheet" href="assets/hdn-fixes.css">
  <meta name="theme-color" content="#d7352a">
'''

pages = {
    "index.html": "page-home",
    "self-pay.html": "page-self-pay",
    "consultation.html": "page-consultation",
}

for filename, body_class in pages.items():
    path = Path("_site") / filename
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8")
    html = html.replace('href="https://hdnjapan.com/"', 'href="index.html"')
    html = html.replace('href="http://hdnjapan.com/"', 'href="index.html"')
    html = html.replace('<a class="brand" href="#">', '<a class="brand" href="index.html">')
    if f'<body class="{body_class}">' not in html:
        html = html.replace('<body>', f'<body class="{body_class}">', 1)
    if 'assets/hdn-fixes.css' not in html:
        html = html.replace('</head>', fixes + '</head>', 1)
    path.write_text(html, encoding="utf-8")

# English homepage navigation.
en_home = Path("_site/en/index.html")
if en_home.exists():
    html = en_home.read_text(encoding="utf-8")
    html = html.replace('<a href="#services">Services</a>', '<a href="self-pay.html">Private Care</a><a href="lhub.html">LHub</a>')
    html = html.replace('<article class="card"><h3>Self-pay service development</h3>', '<article class="card"><h3><a href="self-pay.html">Private medical services</a></h3>')
    html = html.replace('<article class="card"><h3>LHub implementation</h3>', '<article class="card"><h3><a href="lhub.html">LHub implementation</a></h3>')
    en_home.write_text(html, encoding="utf-8")

# Restore English mobile navigation on all English pages.
old_mobile_rule = '.nav a:not(.lang){display:none}'
new_mobile_rule = '.header-inner{align-items:flex-start;flex-direction:column;padding:12px 0;gap:10px}.nav{display:grid;width:100%;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.nav a{display:grid!important;place-items:center;min-height:40px;padding:0 8px;border:1px solid var(--line);border-radius:7px;background:#fff;text-align:center}.nav a[href*="forms.gle"]{display:none!important}.nav .lang{display:none!important}'
for filename in ('en/index.html', 'en/self-pay.html', 'en/lhub.html'):
    path = Path('_site') / filename
    if not path.exists():
        continue
    html = path.read_text(encoding='utf-8')
    html = html.replace(old_mobile_rule, new_mobile_rule, 1)
    path.write_text(html, encoding='utf-8')

page_pairs = {
    "index.html": ("/", "/en/", "ja"),
    "self-pay.html": ("/self-pay.html", "/en/self-pay.html", "ja"),
    "lhub.html": ("/lhub.html", "/en/lhub.html", "ja"),
    "en/index.html": ("/", "/en/", "en"),
    "en/self-pay.html": ("/self-pay.html", "/en/self-pay.html", "en"),
    "en/lhub.html": ("/lhub.html", "/en/lhub.html", "en"),
}

for filename, (ja_url, en_url, current_lang) in page_pairs.items():
    path = Path("_site") / filename
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8")

    html = re.sub(r'<nav class="language-switch"[^>]*>.*?</nav>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<style id="language-switch-style">.*?</style>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<style id="lhub-cta-contrast-fix">.*?</style>\s*', '', html, flags=re.DOTALL)
    html = html.replace('<link rel="stylesheet" href="assets/site-shell.css">', '')
    html = html.replace('<link rel="stylesheet" href="../assets/site-shell.css">', '')
    html = html.replace('<script src="assets/site-shell.js" defer></script>', '')
    html = html.replace('<script src="../assets/site-shell.js" defer></script>', '')

    prefix = '../' if filename.startswith('en/') else ''
    shell_assets = f'''  <link rel="stylesheet" href="{prefix}assets/site-shell.css">
  <script src="{prefix}assets/site-shell.js" defer></script>
'''
    html = html.replace('</head>', shell_assets + '</head>', 1)

    alternates = f'''  <link rel="alternate" hreflang="ja" href="https://hdnjapan.com{ja_url}">
  <link rel="alternate" hreflang="en" href="https://hdnjapan.com{en_url}">
  <link rel="alternate" hreflang="x-default" href="https://hdnjapan.com{ja_url}">
'''
    if 'hreflang="ja"' not in html:
        html = html.replace('</head>', alternates + '</head>', 1)

    if current_lang == "ja":
        switch = f'<nav class="language-switch" aria-label="言語切替"><span class="is-current" aria-current="page">JP</span><a href="{en_url}" lang="en" hreflang="en" aria-label="英語版を表示">EN</a></nav>'
    else:
        switch = f'<nav class="language-switch" aria-label="Language switch"><a href="{ja_url}" lang="ja" hreflang="ja" aria-label="View this page in Japanese">JP</a><span class="is-current" aria-current="page">EN</span></nav>'

    html = html.replace('</body>', switch + '\n</body>', 1)
    path.write_text(html, encoding="utf-8")

required = [
    Path("_site/index.html"),
    Path("_site/self-pay.html"),
    Path("_site/lhub.html"),
    Path("_site/en/index.html"),
    Path("_site/en/self-pay.html"),
    Path("_site/en/lhub.html"),
]
for path in required:
    if not path.exists() or path.stat().st_size < 500:
        raise SystemExit(f"Required page is missing or unexpectedly small: {path}")

for path in (Path('_site/en/index.html'), Path('_site/en/self-pay.html'), Path('_site/en/lhub.html')):
    html = path.read_text(encoding='utf-8')
    if old_mobile_rule in html:
        raise SystemExit(f'Legacy hidden mobile navigation remains: {path}')
    for label in ('Home', 'Private Care', 'LHub'):
        if f'>{label}<' not in html:
            raise SystemExit(f'Missing English navigation label {label}: {path}')
PY

touch _site/.nojekyll

echo "Built _site for GitHub Pages."

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

# LHub: ensure the CTA footnote remains readable against its pale green background.
lhub_path = Path("_site/lhub.html")
if lhub_path.exists():
    html = lhub_path.read_text(encoding="utf-8")
    contrast_fix = '''  <style id="lhub-cta-contrast-fix">
    .contact .contact-promise p.promise-foot {
      background: #dff4e9 !important;
      color: #075d42 !important;
      border-color: rgba(0, 166, 106, 0.34) !important;
      text-shadow: none !important;
      opacity: 1 !important;
    }
    .contact .contact-promise p.promise-foot::selection {
      background: #bde7d3;
      color: #073f2e;
    }
  </style>
'''
    if 'lhub-cta-contrast-fix' not in html:
        html = html.replace('</head>', contrast_fix + '</head>', 1)
    lhub_path.write_text(html, encoding="utf-8")

# English homepage: expose direct navigation to the English service pages.
en_home = Path("_site/en/index.html")
if en_home.exists():
    html = en_home.read_text(encoding="utf-8")
    html = html.replace('<a href="#services">Services</a>', '<a href="self-pay.html">Private Care</a><a href="lhub.html">LHub</a>')
    html = html.replace('<article class="card"><h3>Self-pay service development</h3>', '<article class="card"><h3><a href="self-pay.html">Private medical services</a></h3>')
    html = html.replace('<article class="card"><h3>LHub implementation</h3>', '<article class="card"><h3><a href="lhub.html">LHub implementation</a></h3>')
    en_home.write_text(html, encoding="utf-8")

# Add a consistent JP / EN switch to each paired page.
page_pairs = {
    "index.html": ("/", "/en/", "ja"),
    "self-pay.html": ("/self-pay.html", "/en/self-pay.html", "ja"),
    "lhub.html": ("/lhub.html", "/en/lhub.html", "ja"),
    "en/index.html": ("/", "/en/", "en"),
    "en/self-pay.html": ("/self-pay.html", "/en/self-pay.html", "en"),
    "en/lhub.html": ("/lhub.html", "/en/lhub.html", "en"),
}

switch_css = '''  <style id="language-switch-style">
    .language-switch {
      position: fixed;
      right: 16px;
      bottom: 16px;
      z-index: 9999;
      display: inline-flex;
      padding: 4px;
      border: 1px solid rgba(37,34,34,.18);
      border-radius: 999px;
      background: rgba(255,255,255,.98);
      box-shadow: 0 10px 30px rgba(0,0,0,.18);
      backdrop-filter: blur(10px);
    }
    .language-switch a,
    .language-switch span {
      min-width: 42px;
      height: 34px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      color: #5f5555;
      font-size: 12px;
      font-weight: 900;
      letter-spacing: .04em;
      text-decoration: none;
      cursor: pointer;
    }
    .language-switch a:hover {
      background: #f3eeee;
      color: #252222;
    }
    .language-switch .is-current {
      background: #252222;
      color: #fff;
      cursor: default;
    }
    @media (max-width: 640px) {
      .language-switch { right: 10px; bottom: 10px; }
      .language-switch a,
      .language-switch span { min-width: 39px; height: 32px; }
    }
  </style>
'''

old_switch = '<a href="en/" aria-label="English version" style="position:fixed;right:14px;bottom:14px;z-index:40;padding:9px 13px;border-radius:999px;background:#252222;color:#fff;font-size:13px;font-weight:800;box-shadow:0 8px 24px rgba(0,0,0,.18)">EN</a>'

for filename, (ja_url, en_url, current_lang) in page_pairs.items():
    path = Path("_site") / filename
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8")

    html = html.replace(old_switch, '')
    html = re.sub(r'<nav class="language-switch"[^>]*>.*?</nav>\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<style id="language-switch-style">.*?</style>\s*', '', html, flags=re.DOTALL)
    html = html.replace('</head>', switch_css + '</head>', 1)

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

# Fail the build if any required public page is missing or empty.
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
PY

touch _site/.nojekyll

echo "Built _site for GitHub Pages."

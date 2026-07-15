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

    # Use relative links so the same files work on GitHub Pages staging and the production domain.
    html = html.replace('href="https://hdnjapan.com/"', 'href="index.html"')
    html = html.replace('href="http://hdnjapan.com/"', 'href="index.html"')
    html = html.replace('<a class="brand" href="#">', '<a class="brand" href="index.html">')

    # Add body classes so page-specific layout fixes can be scoped safely.
    if f'<body class="{body_class}">' not in html:
        html = html.replace('<body>', f'<body class="{body_class}">', 1)

    # Add HDN favicon and layout-fix stylesheet to non-LHub pages.
    if 'assets/hdn-fixes.css' not in html:
        html = html.replace('</head>', fixes + '</head>', 1)

    # Add language alternates and an English entry point on the Japanese homepage.
    if filename == "index.html":
        language_meta = '''  <link rel="alternate" hreflang="ja" href="https://hdnjapan.com/">
  <link rel="alternate" hreflang="en" href="https://hdnjapan.com/en/">
  <link rel="alternate" hreflang="x-default" href="https://hdnjapan.com/">
'''
        if 'hreflang="en"' not in html:
            html = html.replace('</head>', language_meta + '</head>', 1)

        language_switch = '''<a href="en/" aria-label="English version" style="position:fixed;right:14px;bottom:14px;z-index:40;padding:9px 13px;border-radius:999px;background:#252222;color:#fff;font-size:13px;font-weight:800;box-shadow:0 8px 24px rgba(0,0,0,.18)">EN</a>'''
        if 'aria-label="English version"' not in html:
            html = html.replace('</body>', language_switch + '\n</body>', 1)

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
PY

touch _site/.nojekyll

echo "Built _site for GitHub Pages."

#!/usr/bin/env bash
set -eu

rm -rf _site
mkdir -p _site

cp index.html _site/
cp self-pay.html _site/
cp lhub.html _site/
cp consultation.html _site/
cp -R assets _site/assets
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

    path.write_text(html, encoding="utf-8")
PY

touch _site/.nojekyll

echo "Built _site for GitHub Pages."

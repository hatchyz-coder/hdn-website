from pathlib import Path

PAGES = [
    'index.html', 'self-pay.html', 'lhub.html', 'lhub-lp.html',
    'medical-sns.html', 'tsuyoshi-hadano.html', 'consultation.html',
    'en/index.html', 'en/self-pay.html', 'en/lhub.html',
]

for filename in PAGES:
    path = Path('_site') / filename
    if not path.exists():
        raise SystemExit(f'Missing public page: {path}')
    html = path.read_text(encoding='utf-8')
    prefix = '../' if filename.startswith('en/') else ''
    link = f'<link rel="stylesheet" href="{prefix}assets/mobile-audit.css">'
    if link not in html:
        html = html.replace('</head>', f'  {link}\n</head>', 1)
    path.write_text(html, encoding='utf-8')

for filename in PAGES:
    html = (Path('_site') / filename).read_text(encoding='utf-8')
    if 'assets/mobile-audit.css' not in html:
        raise SystemExit(f'Mobile audit stylesheet missing: {filename}')

print('Mobile UI audit layer applied to all public pages.')

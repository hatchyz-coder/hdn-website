from pathlib import Path
import re

SITE = Path('_site')
LEGACY_FORM = 'https://forms.gle/148jgfSnDgDZ2HsEA'
CUSTOM_FORM = '/consultation-form.html'


def replace_legacy_contact(html: str) -> str:
    pattern = rf'href="{re.escape(LEGACY_FORM)}"(?:\s+target="_blank")?(?:\s+rel="noopener(?: noreferrer)?")?'
    return re.sub(pattern, f'href="{CUSTOM_FORM}"', html)


def repair_english_legal_footer(html: str) -> str:
    # English legal pages live under /en/. Their legal links must remain in /en/
    # rather than climbing to the Japanese root policy pages.
    for name in ('privacy.html', 'terms.html', 'cookie-policy.html', 'security.html', 'disclaimer.html'):
        html = html.replace(f'href="../{name}"', f'href="{name}"')
    # The English homepage currently has no stable #company anchor.
    html = html.replace('href="/en/#company"', 'href="/en/"')
    return html


def repair_footer_replacement_compatibility(html: str) -> str:
    # Normalize the generated legal footer opening tag so future replacement
    # passes can match it even when data attributes are already present.
    html = html.replace(
        '<footer class="footer legal-footer" data-legal-footer>',
        '<footer class="footer legal-footer" data-legal-footer="true">',
    )
    return html


def process(path: Path) -> None:
    html = path.read_text(encoding='utf-8')
    html = replace_legacy_contact(html)
    if '/en/' in f'/{path.relative_to(SITE).as_posix()}':
        html = repair_english_legal_footer(html)
    html = repair_footer_replacement_compatibility(html)
    path.write_text(html, encoding='utf-8')


for path in SITE.rglob('*.html'):
    process(path)

# Guardrails: no current corporate page should send consultation traffic to the
# legacy Google Form after the first-party form has been launched.
for path in SITE.rglob('*.html'):
    html = path.read_text(encoding='utf-8')
    if LEGACY_FORM in html:
        raise SystemExit(f'Legacy Google Form link remains: {path}')

for name in ('privacy.html', 'terms.html', 'cookie-policy.html', 'security.html', 'disclaimer.html'):
    path = SITE / 'en' / name
    html = path.read_text(encoding='utf-8')
    if f'href="../{name}"' in html:
        raise SystemExit(f'English legal footer escaped to JP root: {path}')
    if 'href="/en/#company"' in html:
        raise SystemExit(f'Broken English company anchor remains: {path}')

from pathlib import Path
import re

CUSTOM_FORM = '/consultation-form.html'
GOOGLE_FORM_HOST_PATTERNS = (
    r'https://forms\.gle/[^"\'\s<>]+',
    r'https://docs\.google\.com/forms/[^"\'\s<>]+',
)

ROOT_PUBLIC = [
    *Path('.').glob('*.html'),
    *Path('en').glob('*.html'),
]
SITE = Path('_site')


def replace_google_form_links(html: str) -> str:
    """Route every public Google Form link to HDN's first-party consultation form."""
    for url_pattern in GOOGLE_FORM_HOST_PATTERNS:
        href_pattern = rf'href="{url_pattern}"(?:\s+target="_blank")?(?:\s+rel="noopener(?: noreferrer)?")?'
        html = re.sub(href_pattern, f'href="{CUSTOM_FORM}"', html, flags=re.IGNORECASE)
    return html


def repair_english_legal_footer(html: str) -> str:
    for name in ('privacy.html', 'terms.html', 'cookie-policy.html', 'security.html', 'disclaimer.html'):
        html = html.replace(f'href="../{name}"', f'href="{name}"')
    html = html.replace('href="/en/#company"', 'href="/en/"')
    return html


def repair_footer_replacement_compatibility(html: str) -> str:
    return html.replace(
        '<footer class="footer legal-footer" data-legal-footer>',
        '<footer class="footer legal-footer" data-legal-footer="true">',
    )


def is_english(path: Path) -> bool:
    return 'en' in path.parts


def process(path: Path) -> None:
    if not path.exists() or not path.is_file():
        return
    html = path.read_text(encoding='utf-8')
    html = replace_google_form_links(html)
    if is_english(path):
        html = repair_english_legal_footer(html)
    html = repair_footer_replacement_compatibility(html)
    path.write_text(html, encoding='utf-8')


# Repair the checked-in GitHub Pages source as well as the generated build tree.
# This closes the gap where _site was clean but the branch root—and therefore the
# live Pages source—could still contain legacy Google Form CTAs.
for path in ROOT_PUBLIC:
    process(path)

if SITE.exists():
    for path in SITE.rglob('*.html'):
        process(path)


def assert_no_google_form(path: Path) -> None:
    html = path.read_text(encoding='utf-8').lower()
    if 'forms.gle/' in html or 'docs.google.com/forms/' in html:
        raise SystemExit(f'Google Form link remains in public corporate page: {path}')


for path in ROOT_PUBLIC:
    assert_no_google_form(path)

if SITE.exists():
    for path in SITE.rglob('*.html'):
        assert_no_google_form(path)

for base in (Path('en'), SITE / 'en'):
    if not base.exists():
        continue
    for name in ('privacy.html', 'terms.html', 'cookie-policy.html', 'security.html', 'disclaimer.html'):
        path = base / name
        if not path.exists():
            continue
        html = path.read_text(encoding='utf-8')
        if f'href="../{name}"' in html:
            raise SystemExit(f'English legal footer escaped to JP root: {path}')
        if 'href="/en/#company"' in html:
            raise SystemExit(f'Broken English company anchor remains: {path}')

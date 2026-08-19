from pathlib import Path
import re
from html import unescape
from urllib.parse import urlencode

GOOGLE_FORM_HOST_PATTERNS = (
    r'https://forms\.gle/[^"\'\s<>]+',
    r'https://docs\.google\.com/forms/[^"\'\s<>]+',
)

ROOT_PUBLIC = [
    *Path('.').glob('*.html'),
    *Path('en').glob('*.html'),
]
SITE = Path('_site')


def is_english(path: Path) -> bool:
    return 'en' in path.parts


def custom_form_for(path: Path) -> str:
    return '/en/consultation-form.html' if is_english(path) else '/consultation-form.html'


def replace_google_form_links(html: str, path: Path) -> str:
    """Route every public Google Form link to the language-matched HDN first-party form."""
    target = custom_form_for(path)
    for url_pattern in GOOGLE_FORM_HOST_PATTERNS:
        href_pattern = rf'href="{url_pattern}"(?:\s+target="_blank")?(?:\s+rel="noopener(?: noreferrer)?")?'
        html = re.sub(href_pattern, f'href="{target}"', html, flags=re.IGNORECASE)
    return html


def page_key(path: Path) -> str:
    name = path.name.lower()
    parts = {part.lower() for part in path.parts}
    if name == 'lhub-lp.html':
        return 'lhub_lp'
    if name == 'lhub.html':
        return 'lhub'
    if name == 'self-pay.html':
        return 'self_pay'
    if name == 'medical-sns.html':
        return 'medical_sns'
    if name == 'consultation.html':
        return 'consultation'
    if name == 'privacy.html':
        return 'privacy'
    if 'en' in parts and name == 'index.html':
        return 'en_home'
    if name == 'index.html':
        return 'home'
    return name.removesuffix('.html').replace('-', '_') or 'page'


def text_only(value: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', unescape(value))).strip().lower()


def consultation_intent(path: Path, anchor_text: str, attrs: str) -> str:
    key = page_key(path)
    text = f'{anchor_text} {attrs}'.lower()
    if re.search(r'lhub|line|デモ', text) or key.startswith('lhub'):
        return 'lhub'
    if re.search(r'sns|動画|youtube|social', text) or key == 'medical_sns':
        return 'sns'
    if re.search(r'自費|private care|private medical', text) or key == 'self_pay':
        return 'self_pay'
    if re.search(r'導線|診断|patient journey', text):
        return 'journey_review'
    if re.search(r'問い合わせ|inquiry|privacy|個人情報', text) or key == 'privacy':
        return 'inquiry'
    return 'general'


def add_consultation_attribution(html: str, path: Path) -> str:
    """Persist CTA source/intent/position and enforce a language-matched form URL."""
    pattern = re.compile(
        r'<a(?P<attrs>[^>]*?)href="(?P<href>(?:(?:/en/)|/)?consultation-form\.html(?:\?[^\"]*)?)"(?P<after>[^>]*)>(?P<body>.*?)</a>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    occurrence = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal occurrence
        occurrence += 1
        attrs = f"{match.group('attrs')} {match.group('after')}"
        body = match.group('body')
        text = text_only(body)
        intent = consultation_intent(path, text, attrs)
        data_cta = re.search(r'data-cta="([^\"]+)"', attrs, flags=re.IGNORECASE)
        position = data_cta.group(1)[:48] if data_cta else f'cta_{occurrence}'
        query = urlencode({
            'cta_source': page_key(path),
            'cta_intent': intent,
            'cta_position': position,
        })
        href = f'{custom_form_for(path)}?{query}'
        return f'<a{match.group("attrs")}href="{href}"{match.group("after")}>{body}</a>'

    return pattern.sub(repl, html)


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


def process(path: Path) -> None:
    if not path.exists() or not path.is_file():
        return
    html = path.read_text(encoding='utf-8')
    html = replace_google_form_links(html, path)
    html = add_consultation_attribution(html, path)
    if is_english(path):
        html = repair_english_legal_footer(html)
    html = repair_footer_replacement_compatibility(html)
    path.write_text(html, encoding='utf-8')


# Repair the checked-in GitHub Pages source as well as the generated build tree.
# This closes the gap where _site was clean but the branch root—and therefore the
# live Pages source—could still contain legacy or wrong-language contact CTAs.
for path in ROOT_PUBLIC:
    process(path)

if SITE.exists():
    for path in SITE.rglob('*.html'):
        process(path)


def assert_no_google_form(path: Path) -> None:
    html = path.read_text(encoding='utf-8').lower()
    if 'forms.gle/' in html or 'docs.google.com/forms/' in html:
        raise SystemExit(f'Google Form link remains in public corporate page: {path}')


def assert_attributed_consultation_links(path: Path) -> None:
    if path.name == 'consultation-form.html':
        return
    html = path.read_text(encoding='utf-8')
    for href in re.findall(r'href="([^\"]*consultation-form\.html[^\"]*)"', html, flags=re.IGNORECASE):
        if not all(token in href for token in ('cta_source=', 'cta_intent=', 'cta_position=')):
            raise SystemExit(f'Unattributed consultation link remains: {path}: {href}')
        if is_english(path) and not href.startswith('/en/consultation-form.html'):
            raise SystemExit(f'English page points to non-English consultation form: {path}: {href}')
        if not is_english(path) and href.startswith('/en/consultation-form.html'):
            raise SystemExit(f'Japanese page points to English consultation form: {path}: {href}')


for path in ROOT_PUBLIC:
    assert_no_google_form(path)
    assert_attributed_consultation_links(path)

if SITE.exists():
    for path in SITE.rglob('*.html'):
        assert_no_google_form(path)
        assert_attributed_consultation_links(path)

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

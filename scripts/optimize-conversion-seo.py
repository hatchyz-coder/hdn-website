from pathlib import Path
import html as html_lib
import re

BASE = "https://hdnjapan.com"

PAGE_RULES = {
    "index.html": {"url": f"{BASE}/", "lang": "ja", "pair": f"{BASE}/en/", "image": f"{BASE}/assets/hdn-logo-original.jpg"},
    "self-pay.html": {"url": f"{BASE}/self-pay.html", "lang": "ja", "pair": f"{BASE}/en/self-pay.html", "image": f"{BASE}/assets/self-pay-og.jpg"},
    "lhub.html": {"url": f"{BASE}/lhub.html", "lang": "ja", "pair": f"{BASE}/en/lhub.html", "image": f"{BASE}/assets/lhub-line-commerce.png"},
    "lhub-lp.html": {"url": f"{BASE}/lhub-lp.html", "lang": "ja", "image": f"{BASE}/assets/lhub-line-commerce.png"},
    "medical-sns.html": {"url": f"{BASE}/medical-sns.html", "lang": "ja", "image": f"{BASE}/assets/hadano-profile.jpg"},
    "tsuyoshi-hadano.html": {"url": f"{BASE}/tsuyoshi-hadano.html", "lang": "ja", "image": f"{BASE}/assets/hadano-profile.jpg"},
    "consultation.html": {"url": f"{BASE}/consultation.html", "lang": "ja", "image": f"{BASE}/assets/hadano-profile.jpg"},
    "en/index.html": {"url": f"{BASE}/en/", "lang": "en", "pair": f"{BASE}/", "image": f"{BASE}/assets/hdn-logo-original.jpg"},
    "en/self-pay.html": {"url": f"{BASE}/en/self-pay.html", "lang": "en", "pair": f"{BASE}/self-pay.html", "image": f"{BASE}/assets/self-pay-og.jpg"},
    "en/lhub.html": {"url": f"{BASE}/en/lhub.html", "lang": "en", "pair": f"{BASE}/lhub.html", "image": f"{BASE}/assets/lhub-line-commerce.png"},
}


def meta_value(source: str, pattern: str) -> str:
    match = re.search(pattern, source, re.I | re.S)
    return html_lib.unescape(match.group(1).strip()) if match else ""


def escape(value: str) -> str:
    return html_lib.escape(value, quote=True)


def ensure_head_metadata(source: str, rule: dict) -> str:
    title = meta_value(source, r"<title>(.*?)</title>") or ("HDN Inc." if rule["lang"] == "en" else "株式会社HDN")
    description = meta_value(source, r'<meta\s+name="description"\s+content="([^"]*)"')
    if not description:
        description = "HDN supports practical patient journey and healthcare operations design." if rule["lang"] == "en" else "株式会社HDNは、医療機関の患者導線と実運用を設計・改善します。"

    url = rule["url"]
    image = rule["image"]
    locale = "en_US" if rule["lang"] == "en" else "ja_JP"
    site_name = "HDN Inc." if rule["lang"] == "en" else "株式会社HDN"

    if 'rel="canonical"' not in source:
        source = source.replace("</title>", f'</title>\n  <link rel="canonical" href="{url}">', 1)

    pair = rule.get("pair")
    if pair and 'hreflang="ja"' not in source:
        ja_url = pair if rule["lang"] == "en" else url
        en_url = url if rule["lang"] == "en" else pair
        alternates = (
            f'  <link rel="alternate" hreflang="ja" href="{ja_url}">\n'
            f'  <link rel="alternate" hreflang="en" href="{en_url}">\n'
            f'  <link rel="alternate" hreflang="x-default" href="{ja_url}">\n'
        )
        source = source.replace('</head>', alternates + '</head>', 1)

    og_fields = {
        'property="og:type"': f'<meta property="og:type" content="website">',
        'property="og:locale"': f'<meta property="og:locale" content="{locale}">',
        'property="og:site_name"': f'<meta property="og:site_name" content="{site_name}">',
        'property="og:title"': f'<meta property="og:title" content="{escape(title)}">',
        'property="og:description"': f'<meta property="og:description" content="{escape(description)}">',
        'property="og:url"': f'<meta property="og:url" content="{url}">',
        'property="og:image"': f'<meta property="og:image" content="{image}">',
        'property="og:image:alt"': f'<meta property="og:image:alt" content="{escape(title)}">',
        'name="twitter:card"': '<meta name="twitter:card" content="summary_large_image">',
        'name="twitter:title"': f'<meta name="twitter:title" content="{escape(title)}">',
        'name="twitter:description"': f'<meta name="twitter:description" content="{escape(description)}">',
        'name="twitter:image"': f'<meta name="twitter:image" content="{image}">',
        'name="twitter:image:alt"': f'<meta name="twitter:image:alt" content="{escape(title)}">',
    }
    missing = [tag for marker, tag in og_fields.items() if marker not in source]
    if missing:
        source = source.replace('</head>', '  ' + '\n  '.join(missing) + '\n</head>', 1)

    return source


def add_home_website_schema(source: str) -> str:
    if '"@type":"WebSite"' in source or '"@type": "WebSite"' in source:
        return source
    schema = '''<script type="application/ld+json" id="hdn-website-schema">
  {"@context":"https://schema.org","@type":"WebSite","@id":"https://hdnjapan.com/#website","url":"https://hdnjapan.com/","name":"株式会社HDN","inLanguage":["ja","en"],"publisher":{"@id":"https://hdnjapan.com/#organization"}}
  </script>'''
    return source.replace('</head>', '  ' + schema + '\n</head>', 1)


def trust_block(lang: str) -> str:
    if lang == "en":
        return '''<section class="precontact-trust" data-precontact-trust aria-label="Before contacting HDN">
      <div class="precontact-inner">
        <strong>We start by reviewing what already exists.</strong>
        <div class="precontact-points"><span>Current patient journey</span><span>Existing systems and staff workflow</span><span>Only the changes that are actually needed</span></div>
        <p>Remote consultation is available. The first discussion is used to clarify the current situation and priorities.</p>
      </div>
    </section>'''
    return '''<section class="precontact-trust" data-precontact-trust aria-label="ご相談前に確認すること">
      <div class="precontact-inner">
        <strong>まず、今ある仕組みを確認します。</strong>
        <div class="precontact-points"><span>現在の患者導線</span><span>既存システムと院内運用</span><span>本当に必要な変更だけを整理</span></div>
        <p>全国オンライン対応。最初の相談では、現状と優先順位を整理するところから始めます。</p>
      </div>
    </section>'''


def add_precontact_trust(source: str, lang: str) -> str:
    if 'data-precontact-trust' in source:
        return source
    block = trust_block(lang)
    # Keep the trust material close to conversion without hiding page-specific CTA copy.
    if '</main>' in source:
        source = source.replace('</main>', block + '\n</main>', 1)
    else:
        source = source.replace('</body>', block + '\n</body>', 1)
    return source


def add_shared_style(source: str) -> str:
    if 'id="conversion-trust-style"' in source:
        return source
    style = '''<style id="conversion-trust-style">
    .precontact-trust{padding:34px 0!important;border-top:1px solid #d9d3cb!important;border-bottom:1px solid #d9d3cb!important;background:#f1eee8!important}
    .precontact-inner{width:min(1120px,calc(100% - 40px));margin:auto;display:grid;grid-template-columns:minmax(220px,.58fr) minmax(0,1.2fr);gap:12px 42px;align-items:start}
    .precontact-inner>strong{font-size:18px;line-height:1.5}.precontact-points{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid #cfc8bf}
    .precontact-points span{padding:10px 12px 10px 0;border-bottom:1px solid #cfc8bf;font-size:13px;font-weight:700}.precontact-inner p{grid-column:2;margin:0;color:#6d6660;font-size:12px;line-height:1.7}
    @media(max-width:760px){.precontact-inner{width:min(100% - 28px,1120px);grid-template-columns:1fr;gap:14px}.precontact-points{grid-template-columns:1fr}.precontact-inner p{grid-column:1}.precontact-points span{padding:9px 0}}
  </style>'''
    return source.replace('</head>', '  ' + style + '\n</head>', 1)


def optimize_pages() -> None:
    for relative, rule in PAGE_RULES.items():
        path = Path('_site') / relative
        if not path.exists():
            raise SystemExit(f'Missing generated page: {relative}')
        source = path.read_text(encoding='utf-8')
        source = ensure_head_metadata(source, rule)
        if relative == 'index.html':
            source = add_home_website_schema(source)
        source = add_precontact_trust(source, rule['lang'])
        source = add_shared_style(source)
        path.write_text(source, encoding='utf-8')


def verify() -> None:
    for relative, rule in PAGE_RULES.items():
        source = (Path('_site') / relative).read_text(encoding='utf-8')
        if f'rel="canonical" href="{rule["url"]}"' not in source:
            raise SystemExit(f'Canonical mismatch: {relative}')
        for marker in ('property="og:title"', 'property="og:description"', 'property="og:image"', 'name="twitter:card"'):
            if marker not in source:
                raise SystemExit(f'Missing social metadata {marker}: {relative}')
        if 'data-precontact-trust' not in source:
            raise SystemExit(f'Missing pre-contact trust material: {relative}')
        if rule.get('pair'):
            for lang in ('ja', 'en', 'x-default'):
                if f'hreflang="{lang}"' not in source:
                    raise SystemExit(f'Missing hreflang {lang}: {relative}')
    home = Path('_site/index.html').read_text(encoding='utf-8')
    if 'id="hdn-website-schema"' not in home:
        raise SystemExit('Home WebSite schema is missing')


if __name__ == '__main__':
    optimize_pages()
    verify()

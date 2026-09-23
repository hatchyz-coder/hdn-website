#!/usr/bin/env bash
set -eu

required_files="
llms.txt
index.html
self-pay.html
lhub.html
lhub-lp.html
medical-sns.html
tsuyoshi-hadano.html
consultation.html
consultation-form.html
pricing.html
article-service.html
en/consultation-form.html
assets/consultation-form.js
assets/hdn-logo.png
assets/hadano-profile.jpg
assets/illustration-patient-assets.jpg
assets/illustration-lhub-crm.jpg
assets/illustration-consultation.jpg
assets/self-pay.css
assets/self-pay-og.jpg
assets/medical-sns.css
assets/site-shell.css
assets/editorial.css
assets/site-shell.js
scripts/audit-links.py
"

for file in $required_files; do
  if [ ! -f "$file" ]; then
    echo "Missing required file: $file" >&2
    exit 1
  fi
done

grep -q '^# 株式会社HDN / HDN Inc\.$' llms.txt
grep -q 'https://hdnjapan.com/sitemap.xml' llms.txt
grep -q 'https://article.hdnjapan.com/' llms.txt

if [ ! -s seminar-site/llms.txt ]; then
  echo "Missing or empty seminar-site/llms.txt" >&2
  exit 1
fi
grep -q '^# HDN Seminar$' seminar-site/llms.txt
grep -q 'https://seminar.hdnjapan.com/furuta-01/' seminar-site/llms.txt

if grep -R -n -E "ROOTSと足並み|実名掲載|匿名の想定|制作上|仮で|とりあえず|初回はこの構成|見せる構成" *.html; then
  echo "Found internal-facing copy in public HTML." >&2
  exit 1
fi

if grep -R -n -E "必ず儲かる|確実に売上が上がる|リスクなく導入できる|法令違反にならない|誰でも簡単に成功する|患者が必ず集まる" *.html; then
  echo "Found prohibited outcome or compliance claim in public HTML." >&2
  exit 1
fi

# First-party form invariant: corporate pages must never send consultation or
# inquiry traffic to Google Forms. Scan all checked-in JP/EN public HTML so a
# stale root page cannot bypass the generated-site repair pass.
if grep -n -E 'forms\.gle/|docs\.google\.com/forms/' ./*.html en/*.html 2>/dev/null; then
  echo "Found legacy Google Form link in public corporate HTML." >&2
  exit 1
fi

missing_asset=0
for src in $(grep -RhoE 'src="assets/[^"]+"' *.html | sed -E 's/src="([^"]+)"/\1/' | sort -u); do
  if [ ! -f "$src" ]; then
    echo "Missing referenced asset: $src" >&2
    missing_asset=1
  fi
done

if [ "$missing_asset" -ne 0 ]; then
  exit 1
fi

grep -q '<link rel="canonical" href="https://hdnjapan.com/self-pay.html">' self-pay.html
grep -q '<meta property="og:title"' self-pay.html
grep -q '<meta name="twitter:card" content="summary_large_image">' self-pay.html
grep -q 'id="models"' self-pay.html
grep -q 'HDNが対応する6つの自費診療モデル' self-pay.html
grep -q 'LHubと医療機関向けAI記事制作・公開支援システムを、必要に応じて選べます' index.html
grep -q '月額30,000円' lhub.html
grep -q '記事制作・公開本数に契約上の上限なし' article-service.html
grep -q 'id="profile"' index.html
grep -q '<link rel="canonical" href="https://hdnjapan.com/pricing.html">' pricing.html
grep -q '初期導入費</span><strong>110,000円<small>（税別）</small></strong>' pricing.html
grep -q 'システム月額</span><strong>55,000円<small>（税別）</small></strong>' pricing.html
! grep -q '記事サービスの追加対応' pricing.html
! grep -q '個別見積り' pricing.html
if grep -R -n -E '月額 3万円程度|月額 8万円程度|月2本|追加記事1本|LIGHT、STANDARD、FULL|LIGHT / STANDARD / FULL' ./*.html; then
  echo "Found superseded pricing or plan copy in public HTML." >&2
  exit 1
fi
grep -q '<link rel="canonical" href="https://hdnjapan.com/article-service.html">' article-service.html
grep -q 'AIが作成した文章を無確認で公開するサービスではありません' article-service.html

grep -q '<link rel="canonical" href="https://hdnjapan.com/medical-sns.html">' medical-sns.html
grep -q 'SNS・動画戦略' medical-sns.html
grep -q '医療SNS・YouTube戦略' tsuyoshi-hadano.html
grep -q 'medical-sns.html' tsuyoshi-hadano.html
grep -q "medical-sns.html" assets/site-shell.js
grep -q "SNS・動画戦略" assets/site-shell.js

grep -q '<meta name="robots" content="noindex,follow">' consultation-form.html
grep -q 'id="consultation-form"' consultation-form.html
grep -q 'privacy_consent' consultation-form.html
grep -q '患者氏名、診断名、治療歴、検査結果' consultation-form.html

grep -q '<meta name="robots" content="noindex,follow">' en/consultation-form.html
grep -q '<html lang="en">' en/consultation-form.html
grep -q 'id="consultation-form"' en/consultation-form.html
grep -q 'privacy_consent' en/consultation-form.html
grep -q 'Do not enter patient-identifying or clinical information' en/consultation-form.html
grep -q '../assets/consultation-form.js' en/consultation-form.html

grep -q 'register-consultation' assets/consultation-form.js
grep -q 'consultation_form_submit' assets/consultation-form.js
grep -q 'content_language' assets/consultation-form.js
grep -q 'language,' assets/consultation-form.js
grep -q 'cta_source' assets/site-shell.js
grep -q 'cta_intent' assets/site-shell.js
grep -q 'cta_position' assets/site-shell.js
grep -q 'intentTopicMap' assets/consultation-form.js
grep -q 'ctaContext' assets/consultation-form.js
grep -q "'/en/consultation-form.html'" assets/site-shell.js

# Static links must match the page language even before the runtime safety net runs.
for page in en/index.html en/self-pay.html en/lhub.html en/privacy.html en/terms.html en/cookie-policy.html en/security.html en/disclaimer.html; do
  if grep -q 'href="/consultation-form.html' "$page"; then
    echo "English page points to Japanese consultation form: $page" >&2
    exit 1
  fi
done
for page in en/index.html en/self-pay.html en/lhub.html; do
  grep -q 'href="/en/consultation-form.html' "$page"
done

if grep -q 'consultation-form.html' sitemap.xml; then
  echo "Transactional consultation form must not be included in sitemap.xml." >&2
  exit 1
fi

grep -q 'HDN editorial design layer' assets/editorial.css

python3 scripts/audit-links.py

echo "Site verification passed."

# Pricing readability and approved tax policy regression checks.
grep -q 'pricing-support-price' index.html
grep -q '月額95,000円' index.html
grep -q '95,000円' pricing.html
grep -q '表示金額はすべて税別' index.html
grep -q '200,000円<small>（税別）</small>' pricing.html
if grep -q '値引きしません' index.html pricing.html; then echo 'Client-facing discount disclaimer found' >&2; exit 1; fi
if grep -q 'valueAddedTaxIncluded":true' pricing.html; then echo 'Tax-inclusive schema found' >&2; exit 1; fi

# Standalone pages must include a scoped responsive header; pricing must load its card CSS.
grep -q 'body class="page-pricing"' pricing.html
grep -q 'body class="page-article-service"' article-service.html
grep -q 'assets/hdn-fixes.css' pricing.html
grep -q 'body.page-pricing .site-header .header-inner' assets/site-shell.css
grep -q 'max-width: 106px' assets/site-shell.css

# Pricing-page full rebuild gate: each price carries adjacent tax label; both services have inclusion sections.
grep -q 'LHubの料金に含まれる内容' pricing.html
grep -q '記事サービスの料金に含まれる内容' pricing.html
grep -q '運用まで任せたい場合は' pricing.html
grep -q 'pricing-layout-critical' pricing.html
if grep -q 'HDN Articles.*別の顧客向けサービス' pricing.html; then exit 1; fi
if grep -q '追加10万文字\|11,000円／本\|22,000円／本' pricing.html; then exit 1; fi

# Article-service completeness and price presentation gate.
grep -q 'メモ・音声・資料を専用フォルダに入れるだけ' article-service.html
grep -q '110,000円<small>（税別）</small>' article-service.html
grep -q '55,000円<small>（税別）</small>' article-service.html
grep -q 'article-service-critical' article-service.html
grep -q '記事の制作・編集・公開' article-service.html
if grep -q 'ADDITIONAL SERVICES\|個別見積り\|11,000円／本\|22,000円／本' article-service.html; then echo 'Superseded article add-on pricing' >&2; exit 1; fi
if grep -q 'valueAddedTaxIncluded":true' article-service.html; then echo 'Incorrect article VAT schema' >&2; exit 1; fi

# Input-to-article experience and fictional sample regression checks.
grep -q '導入費と月額料金はこちら' article-service.html
grep -q 'article-demo-flow' article-service.html
grep -q 'article-example-grid' article-service.html
grep -q 'シリーズ記事' article-service.html
grep -q 'AIに「もっとやさしく」' article-service.html
grep -q '架空の医療機関・架空の入力素材' article-service.html
if grep -q '導入費と月額料金は、次の2つです' article-service.html; then exit 1; fi

# Article-service conversion copy and visual demo regression gate.
grep -q '導入費と月額料金はこちら' article-service.html
grep -q 'article-demo-flow' article-service.html
grep -q 'article-example-grid' article-service.html
grep -q '架空のメモ' article-service.html
grep -q 'article-seo-title' article-service.html
grep -q '保険診療の受診につながる接点' article-service.html
grep -q 'シリーズ記事' article-service.html
grep -q 'AIに「もっとやさしく」' article-service.html

# Cloud-folder-first workflow and cross-page service consistency.
grep -q '院長にお願いするのは、専用フォルダへのアップロード' article-service.html
grep -q '院長・院内担当者が確認' article-service.html
grep -q '自動投稿専用ドメインの取得・設定（HDNが対応）' article-service.html
grep -q '多言語化対応・SNS原稿' article-service.html
grep -q 'href="#article-prices">記事サービスの料金へ' article-service.html
grep -q '専用のクラウドフォルダにアップロード' pricing.html
grep -q '専用フォルダに入れるだけ' index.html
if grep -q '素材を共有\|ご共有いただきます\|サブドメイン設定支援\|英語版対応' article-service.html pricing.html; then echo 'Outdated article workflow copy' >&2; exit 1; fi

# Cross-page tax and product identity must match the approved public price policy.
python3 - <<'PY'
from pathlib import Path

checks = {
    "index.html": ["200,000円<small>（税別）</small>", "30,000円<small>（税別）</small>", "65,000円<small>（税別）</small>", "110,000円<small>（税別）</small>", "55,000円<small>（税別）</small>"],
    "pricing.html": ["200,000円<small>（税別）</small>", "30,000円<small>（税別）</small>", "65,000円<small>（税別）</small>", "110,000円<small>（税別）</small>", "55,000円<small>（税別）</small>"],
    "article-service.html": ["110,000円<small>（税別）</small>", "55,000円<small>（税別）</small>", '"valueAddedTaxIncluded":false'],
    "lhub.html": ["月額30,000円（税別）", "初期導入費は200,000円（税別）", "月額65,000円（税別・任意）", "月額95,000円（税別）", "月額料金。税別です。"],
    "en/self-pay.html": ["JPY 200,000 excl. tax", "JPY 30,000 excl. tax", "JPY 65,000 per month excl. tax", "JPY 110,000 excl. tax", "JPY 55,000 excl. tax"],
}
for name, required in checks.items():
    page = Path(name).read_text(encoding="utf-8")
    for phrase in required:
        if phrase not in page:
            raise SystemExit(f"{name}: approved pricing missing: {phrase}")
    if name == "en/self-pay.html":
        for old in ("JPY 110,000 incl. tax", "JPY 55,000 incl. tax", "Tax treatment and contract terms are explained before agreement.", "<strong>HDN Articles</strong>"):
            if old in page:
                raise SystemExit(f"{name}: superseded pricing or service label: {old}")
    if name == "lhub.html" and "税区分を含む正式な契約条件は" in page:
        raise SystemExit("lhub.html: superseded undetermined-tax wording")
print("Approved cross-page pricing and tax treatment verified.")
PY

# B2B LP and adjacent pages must explain real service roles and independently priced options.
python3 - <<'PY'
from pathlib import Path
from html.parser import HTMLParser

lp = Path("lhub-lp.html").read_text(encoding="utf-8")
lhub = Path("lhub.html").read_text(encoding="utf-8")
articles = Path("article-service.html").read_text(encoding="utf-8")
pricing = Path("pricing.html").read_text(encoding="utf-8")
home = Path("index.html").read_text(encoding="utf-8")

required = {
    "lhub-lp.html": (lp, [
        "オンライン診療を、", "もっと低コストで。", 'id="pricing"',
        'id="reach"', 'id="article-option"', 'id="faq"',
        "200,000円（税別）", "30,000円（税別）",
        "65,000円", "110,000円", "55,000円",
        "SEOは検索結果の順位や患者数の増加を保証するものではありません",
        "診察・処方は医療機関", 'href="article-service.html"',
        'href="/consultation-form.html?',
    ]),
    "lhub.html": (lhub, ['id="lhub-growth"', 'href="lhub-lp.html#pricing"', 'href="article-service.html"']),
    "article-service.html": (articles, ['id="article-patient-journey"', 'href="lhub-lp.html#pricing"', "医療機関の確認・承認"]),
    "pricing.html": (pricing, ['id="optional-growth"', 'href="lhub-lp.html#pricing"', "月額30,000円"]),
    "index.html": (home, ['href="lhub-lp.html"', 'href="lhub-lp.html#reach"']),
}
for name, (content, phrases) in required.items():
    for phrase in phrases:
        if phrase not in content:
            raise SystemExit(f"{name}: clinic director LP requirement missing: {phrase}")
for phrase in ("月商250万円", "月商500万円", "月商100万円超", "予約システムでも、LINE配信ツールでもない。", "30秒デモ"):
    if phrase in lp:
        raise SystemExit(f"lhub-lp.html: unverified marketing claim remains: {phrase}")

class LandmarkCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            if attributes["id"] in self.ids:
                raise ValueError(f"Duplicate id: {attributes['id']}")
            self.ids.add(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.hrefs.append(attributes["href"])

parser = LandmarkCheck()
parser.feed(lp)
for fragment in ("pricing", "reach", "article-option", "faq", "flow"):
    if fragment not in parser.ids or f"#{fragment}" not in parser.hrefs:
        raise SystemExit(f"LP section or navigation target missing: {fragment}")
print("Clinic director LP, pricing boundaries, and cross-page links verified.")
PY

# LHub clinic LP: the retail promotional graphic is not an actual product screenshot.
python3 - <<'PY'
from pathlib import Path

lp = Path("lhub-lp.html").read_text(encoding="utf-8")
postprocessor = Path("scripts/postprocess-site.py").read_text(encoding="utf-8")
for phrase in (
    'data-journey-visual',
    'data-demo-overview',
    '実際のLINE・管理画面のスクリーンショットではありません',
    'https://l-hub.info/',
    'id="clinic-visual-evidence-style"',
):
    if phrase not in lp:
        raise SystemExit(f"Missing honest LP visual: {phrase}")
for old in (
    'assets/lhub-line-commerce.png',
    'LHubの実際の操作画面',
    '<strong>実際のLHub画面</strong>',
):
    if old in lp:
        raise SystemExit(f"Misleading retail promo in clinic LP: {old}")
if 'def replace_lhub_placeholders' in postprocessor:
    raise SystemExit("Old postprocessor can reinsert a misleading image")
if 'Retail promotion graphic cannot be used as clinic LP product evidence' not in postprocessor:
    raise SystemExit("Missing postprocess screenshot authenticity guard")
print("Clinic LP visual authenticity checks verified.")
PY

# The development rules must not revive tax-inclusive article-service pricing.
grep -Fq 'JPY 110,000 initial setup and JPY 55,000 monthly, **both tax excluded**' AGENTS.md
if grep -Fq 'JPY 110,000 initial setup and JPY 55,000 monthly, tax included.' AGENTS.md; then
  echo 'Outdated tax-inclusive article service policy in AGENTS.md' >&2
  exit 1
fi

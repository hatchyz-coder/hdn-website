#!/usr/bin/env bash
set -eu

required_files="
index.html
self-pay.html
lhub.html
lhub-lp.html
medical-sns.html
tsuyoshi-hadano.html
consultation.html
consultation-form.html
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
grep -q 'LIGHT' index.html
grep -q 'STANDARD' index.html
grep -q 'FULL' index.html
grep -q 'id="profile"' index.html

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
grep -q 'register-consultation' assets/consultation-form.js
grep -q 'consultation_form_submit' assets/consultation-form.js
if grep -q 'consultation-form.html' sitemap.xml; then
  echo "Transactional consultation form must not be included in sitemap.xml." >&2
  exit 1
fi

grep -q 'HDN editorial design layer' assets/editorial.css

python3 scripts/audit-links.py

echo "Site verification passed."

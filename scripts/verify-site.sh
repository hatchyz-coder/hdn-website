#!/usr/bin/env bash
set -eu

required_files="
index.html
self-pay.html
lhub.html
consultation.html
assets/hdn-logo.png
assets/hadano-profile.jpg
assets/illustration-patient-assets.jpg
assets/illustration-lhub-crm.jpg
assets/illustration-consultation.jpg
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

echo "Site verification passed."

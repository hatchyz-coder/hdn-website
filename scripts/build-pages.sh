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
touch _site/.nojekyll

echo "Built _site for GitHub Pages."

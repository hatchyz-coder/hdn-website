#!/usr/bin/env bash
set -eu

if [ $# -ne 1 ]; then
  echo "Usage: ./scripts/connect-github.sh <git-remote-url>" >&2
  echo "Example: ./scripts/connect-github.sh https://github.com/OWNER/hdn-website.git" >&2
  exit 1
fi

remote_url="$1"

./scripts/verify-site.sh
./scripts/build-pages.sh

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$remote_url"
else
  git remote add origin "$remote_url"
fi

git branch -M main
git push -u origin main

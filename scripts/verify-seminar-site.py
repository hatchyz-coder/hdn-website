#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "seminar-site"
EVENT = SITE / "furuta-01" / "index.html"
CSS = SITE / "assets" / "seminar.css"
JS = SITE / "assets" / "seminar.js"

errors = []
for path in (SITE / "index.html", EVENT, CSS, JS, SITE / "README.md"):
    if not path.exists() or path.stat().st_size == 0:
        errors.append(f"missing or empty: {path.relative_to(ROOT)}")

if EVENT.exists():
    html = EVENT.read_text(encoding="utf-8")
    required = [
        "自費診療、",
        "8月27日（木）20:00–21:00",
        'id="seminar-form"',
        'name="privacy_consent"',
        "患者さんの個人情報は入力しないでください",
        "https://forms.hdnjapan.com/api/seminar",
        "https://seminar.hdnjapan.com/furuta-01/",
    ]
    for needle in required:
        if needle not in html:
            errors.append(f"event page missing required content: {needle}")

    forbidden = [
        "zoom.us/j/",
        "SUPABASE_SERVICE_ROLE_KEY",
        "RESEND_API_KEY",
        "TURNSTILE_SECRET",
        "forms.gle",
        "docs.google.com/forms",
    ]
    for needle in forbidden:
        if needle.lower() in html.lower():
            errors.append(f"event page exposes forbidden value/reference: {needle}")

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html)
    if emails:
        errors.append(f"unexpected email address in public event HTML: {emails[0]}")

if JS.exists():
    js = JS.read_text(encoding="utf-8")
    for needle in ("submission_key", "privacy_consent", "utm_source", "response.ok", "body.ok !== true"):
        if needle not in js:
            errors.append(f"form script missing guard/field: {needle}")
    if "fbq('track', 'Lead')" not in js:
        errors.append("Meta Lead event is missing")

if CSS.exists():
    css = CSS.read_text(encoding="utf-8")
    if "@media(max-width:600px)" not in css:
        errors.append("mobile CSS breakpoint missing")

if errors:
    print("Seminar site verification failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Seminar site verification passed.")

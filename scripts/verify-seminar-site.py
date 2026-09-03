#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "seminar-site"
EVENT = SITE / "furuta-01" / "index.html"
CSS = SITE / "assets" / "seminar.css"
JS = SITE / "assets" / "seminar.js"
FURUTA = SITE / "assets" / "furuta-kazunori.jpg"
OGP = SITE / "assets" / "furuta-ogp.jpg"
LLMS = SITE / "llms.txt"

errors = []
for path in (SITE / "index.html", EVENT, CSS, JS, SITE / "README.md", FURUTA, OGP, LLMS):
    if not path.exists() or path.stat().st_size == 0:
        errors.append(f"missing or empty: {path.relative_to(ROOT)}")

if EVENT.exists():
    html = EVENT.read_text(encoding="utf-8")
    required = [
        "自費診療、",
        "9月10日（木）20:00–21:00",
        "2026-09-10T20:00:00+09:00",
        "2026-09-10T21:00:00+09:00",
        'id="seminar-form"',
        'name="name" autocomplete="name" required minlength="3"',
        'name="organization_name" autocomplete="organization" required minlength="4"',
        'name="self_pay_status" required',
        'name="privacy_consent"',
        "患者さんの個人情報は入力しないでください",
        "https://forms.hdnjapan.com/api/seminar",
        "https://seminar.hdnjapan.com/furuta-01/",
        "../assets/furuta-kazunori.jpg",
        "https://seminar.hdnjapan.com/assets/furuta-ogp.jpg",
        'meta property="og:image"',
        'meta name="twitter:image"',
    ]
    for needle in required:
        if needle not in html:
            errors.append(f"event page missing required content: {needle}")

    forbidden = [
        "8月27日",
        "2026-08-27",
        "zoom.us/j/",
        "SUPABASE_SERVICE_ROLE_KEY",
        "RESEND_API_KEY",
        "TURNSTILE_SECRET",
        "forms.gle",
        "docs.google.com/forms",
    ]
    for needle in forbidden:
        if needle.lower() in html.lower():
            errors.append(f"event page exposes forbidden/stale value/reference: {needle}")

    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html)
    if emails:
        errors.append(f"unexpected email address in public event HTML: {emails[0]}")

if JS.exists():
    js = JS.read_text(encoding="utf-8")
    for needle in ("submission_key", "privacy_consent", "utm_source", "response.ok", "body.ok !== true", "validateRegistration", "selfPayStatuses"):
        if needle not in js:
            errors.append(f"form script missing guard/field: {needle}")
    if "fbq('track', 'Lead')" not in js:
        errors.append("Meta Lead event is missing")

if CSS.exists():
    css = CSS.read_text(encoding="utf-8")
    if "@media(max-width:600px)" not in css:
        errors.append("mobile CSS breakpoint missing")
    if ".speaker-photo-furuta" not in css:
        errors.append("Furuta portrait styling missing")

if LLMS.exists():
    llms = LLMS.read_text(encoding="utf-8")
    for needle in (
        "# HDN Seminar",
        "https://seminar.hdnjapan.com/furuta-01/",
        "https://hdnjapan.com/privacy.html",
    ):
        if needle not in llms:
            errors.append(f"seminar llms.txt missing required content: {needle}")

if errors:
    print("Seminar site verification failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Seminar site verification passed.")

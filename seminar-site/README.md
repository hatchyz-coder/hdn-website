# seminar-site

Static source for `seminar.hdnjapan.com`.

## Deployment target

Recommended: Cloudflare Pages connected to `hatchyz-coder/hdn-website` with this directory as the project root/output source.

- Root directory: `seminar-site`
- Build command: none
- Output directory: `.`
- Custom domain: `seminar.hdnjapan.com`

This directory is intentionally excluded from the existing corporate-site GitHub Pages build, so adding the seminar site does not change `hdnjapan.com`.

## Current event

- `furuta-01/`
- 2026-08-27 20:00 JST
- Zoom online seminar

## Form integration

The public form posts JSON to the endpoint declared by:

```html
<meta name="hdn-form-endpoint" content="https://forms.hdnjapan.com/api/seminar">
```

The endpoint is not implemented in this public repository. It belongs to HDN Form Platform (`hatchyz-coder/hdn-platform#12`) and must remain server-side.

Required production behavior:

- Turnstile server validation
- server validation and origin checks
- idempotent registration persistence
- Resend confirmation and HDN admin notification
- 3-day, 1-day, and same-day reminders
- stable HDN join URL rather than exposing raw Zoom URL in static files
- UTM attribution storage
- Meta Lead event only after server-confirmed success

Do not put Supabase keys, Resend keys, Turnstile secrets, raw Zoom URLs, applicant data, or other secrets/PII in this repository.

## Local preview

From repository root:

```bash
python3 -m http.server 8080 --directory seminar-site
```

Open:

```text
http://localhost:8080/furuta-01/
```

## Verification

Run:

```bash
python3 scripts/verify-seminar-site.py
```

Production DNS/deployment, real form processing, and external email sending remain explicit HDN approval gates.

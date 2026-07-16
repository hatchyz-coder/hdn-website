# WEB-001 implementation notes

## Implemented
- Shared language-switch styles: `assets/site-shell.css`
- Shared header placement script: `assets/site-shell.js`
- Build integration for Japanese and English TOP, Self-pay, and LHub pages
- LHub CTA contrast safeguard moved into the shared stylesheet

## Expected desktop order
Primary navigation → JP / EN → consultation CTA

## Expected mobile behavior
A compact JP / EN selector is appended to the mobile navigation.

## Verification checklist
- [ ] Generated HTML contains `assets/site-shell.css`
- [ ] Generated HTML contains `assets/site-shell.js`
- [ ] JP and EN links resolve to paired pages
- [ ] Desktop selector is inside the header navigation
- [ ] Mobile selector appears inside the mobile navigation
- [ ] LHub promise footnote uses white background and dark green text
- [ ] Production desktop screenshot checked
- [ ] Production mobile screenshot checked

The issue must remain open until production verification is complete.

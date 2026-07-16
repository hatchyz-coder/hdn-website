# HDN Website Review Prompt

Review the requested HDN website change as a production reviewer.

## Inputs
- Issue objective
- Changed files
- Target Japanese and English URLs
- Desktop and mobile screenshots when available

## Required checks
1. Confirm the source change exists in the files actually published by GitHub Pages.
2. Confirm Japanese and English paired pages link both ways.
3. Confirm TOP, Self-pay, LHub, Articles, and consultation paths are reachable where applicable.
4. Check text/background contrast, button visibility, spacing, logo placement, overflow, and fixed elements.
5. Check mobile header and navigation.
6. Check title, description, canonical, hreflang, favicon, and Open Graph metadata.
7. Confirm no old production or staging URL is used unintentionally.
8. Confirm the build and deployment method matches the repository settings.

## Output
- PASS or FAIL
- Blocking findings
- Non-blocking improvements
- Exact files and selectors involved
- Production URLs checked
- Commit SHA checked

Do not say the work is complete without production verification.

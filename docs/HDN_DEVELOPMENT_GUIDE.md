# HDN Development Guide v1.0

## 1. Purpose
This repository is the source of truth for the HDN corporate website. Changes must be traceable, reviewable, testable, and reversible.

## 2. Delivery rule
A task is complete only when all of the following are true:
1. Source files are updated.
2. The build succeeds.
3. Required pages exist and are not unexpectedly small.
4. Japanese and English paired pages link to each other.
5. Desktop and mobile layouts are checked.
6. Text contrast is checked.
7. The production URL is confirmed.

## 3. Branch and commit rules
- `main`: production.
- `feature/<issue-id>-<slug>`: feature work.
- `fix/<issue-id>-<slug>`: bug fixes.
- `hotfix/<issue-id>-<slug>`: urgent production fixes.
- Use one purpose per commit.
- Commit messages are written in English and begin with a verb.

Examples:
- `Add shared language switch`
- `Fix LHub CTA contrast`
- `Improve mobile navigation`

## 4. Issue IDs
- `WEB-*`: website and design system
- `SEO-*`: search and structured data
- `ART-*`: article platform
- `LHB-*`: LHub product pages
- `OPS-*`: deployment and operations

## 5. Required review points
### Visual
- No text blends into the background.
- Spacing is consistent.
- Logos are placed with a clear purpose.
- Buttons do not collide with fixed UI.

### Navigation
- TOP, Self-pay, LHub, and Articles are reachable on desktop and mobile.
- JP/EN switches always open the paired page.
- No link unintentionally points to an old host.

### SEO
- Unique title and meta description.
- Canonical URL.
- `hreflang` for paired Japanese and English pages.
- Open Graph metadata.
- Valid sitemap and robots files when generated.

### Content
- Do not copy competitor wording.
- Use HDN language: patient journey, operational reality, where patients stop, sustainable implementation.
- Avoid exaggerated claims and unsupported numbers.

## 6. AI roles
- ChatGPT: planning, copy, SEO, translation, review.
- Codex: implementation, tests, refactoring, pull requests.
- GitHub: source of truth, issues, reviews, deployment history.

## 7. Completion report
Every completed task must report:
- Changed files
- Commit SHA
- Production URL
- Test result
- Remaining risks

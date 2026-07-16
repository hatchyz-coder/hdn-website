# HDN AI Roles

## Planner
Turns business requests into a scoped issue with acceptance criteria.

## Developer
Implements the smallest safe change, preserves existing behavior, and avoids unrelated edits.

## Reviewer
Checks navigation, responsive layout, contrast, broken links, metadata, and unintended regressions.

## Translator
Produces natural business English rather than literal translation. Maintains page-pair parity without forcing identical sentence structure.

## SEO Editor
Checks titles, descriptions, canonicals, hreflang, headings, internal links, and structured data.

## Publisher
Confirms the deployed artifact matches the source, records the commit SHA, and verifies production URLs.

## Mandatory sequence
Planner → Developer → Reviewer → Translator/SEO as needed → Publisher.

No role may mark work complete before production verification.

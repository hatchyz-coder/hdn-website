#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path('.')
PUBLIC_HTML = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html'))
INTERNAL_HOSTS = {'hdnjapan.com', 'www.hdnjapan.com'}
LEGACY_HOSTS = {'hatchyz-coder.github.io'}
SKIP_SCHEMES = {'mailto', 'tel', 'sms', 'javascript', 'data'}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {k.lower(): (v or '') for k, v in attrs}
        element_id = values.get('id') or values.get('name')
        if element_id:
            self.ids.add(element_id)
        if tag.lower() == 'a' and values.get('href'):
            self.links.append(values)


def load_pages() -> dict[Path, PageParser]:
    pages: dict[Path, PageParser] = {}
    for path in PUBLIC_HTML:
        parser = PageParser()
        parser.feed(path.read_text(encoding='utf-8'))
        pages[path] = parser
    return pages


def public_path_to_file(path: str) -> Path:
    clean = unquote(path).split('?', 1)[0]
    if clean in ('', '/'):
        return ROOT / 'index.html'
    clean = clean.lstrip('/')
    candidate = ROOT / clean
    if clean.endswith('/'):
        return candidate / 'index.html'
    if candidate.suffix:
        return candidate
    if candidate.is_dir():
        return candidate / 'index.html'
    return candidate


def resolve_internal(source: Path, href: str) -> tuple[Path, str]:
    parsed = urlparse(href)
    fragment = unquote(parsed.fragment or '')
    if parsed.netloc:
        target = public_path_to_file(parsed.path)
    elif parsed.path.startswith('/'):
        target = public_path_to_file(parsed.path)
    elif not parsed.path:
        target = source
    else:
        target = (source.parent / unquote(parsed.path)).resolve().relative_to(ROOT.resolve())
    return target, fragment


def main() -> int:
    pages = load_pages()
    errors: list[str] = []
    checked_links = 0

    for source, parser in pages.items():
        for attrs in parser.links:
            href = attrs.get('href', '').strip()
            if not href or href == '#':
                continue
            checked_links += 1
            parsed = urlparse(href)
            scheme = parsed.scheme.lower()
            host = parsed.netloc.lower().split(':', 1)[0]

            if scheme in SKIP_SCHEMES:
                continue
            if 'forms.gle/' in href or 'docs.google.com/forms/' in href:
                errors.append(f'{source}: legacy Google Form URL: {href}')
                continue
            if host in LEGACY_HOSTS:
                errors.append(f'{source}: legacy GitHub Pages URL: {href}')
                continue

            target_blank = attrs.get('target', '').lower() == '_blank'
            rel_tokens = set(attrs.get('rel', '').lower().split())
            is_external = bool(host and host not in INTERNAL_HOSTS)
            if target_blank and not {'noopener', 'noreferrer'}.issubset(rel_tokens):
                errors.append(f'{source}: target="_blank" missing noopener noreferrer: {href}')
            if not is_external and target_blank:
                errors.append(f'{source}: internal link should not open a new tab: {href}')

            if is_external:
                continue
            if scheme and scheme not in {'http', 'https'}:
                continue
            if host and host not in INTERNAL_HOSTS:
                continue

            try:
                target, fragment = resolve_internal(source, href)
            except ValueError:
                errors.append(f'{source}: internal link escapes site root: {href}')
                continue

            if not target.exists():
                errors.append(f'{source}: missing internal target {target.as_posix()}: {href}')
                continue

            if fragment and target.suffix.lower() == '.html':
                target_parser = pages.get(target)
                if target_parser is None:
                    target_parser = PageParser()
                    target_parser.feed(target.read_text(encoding='utf-8'))
                    pages[target] = target_parser
                if fragment not in target_parser.ids:
                    errors.append(f'{source}: missing fragment #{fragment} in {target.as_posix()}: {href}')

    if errors:
        print('Link audit failed:')
        for error in errors:
            print(f'- {error}')
        return 1

    print(f'Link audit passed: {len(PUBLIC_HTML)} pages, {checked_links} links checked.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

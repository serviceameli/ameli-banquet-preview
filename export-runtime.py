#!/usr/bin/env python3
"""Export the modern landing page and only its dependencies to a hosting ZIP.

Example:
  python3 export-runtime.py ../audit/ameli-site.zip
  python3 export-runtime.py ../audit/ameli-site.zip --base-url https://example.ru/venues/

The repository's historical index.html is never modified. Build the modern page
with build-editorial.py before exporting. With no base URL, the export stays
noindex. An explicit base URL creates the indexable release and crawler files.
"""
from argparse import ArgumentParser
from collections import defaultdict
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import unquote, urlsplit
from release_content import apply_metadata
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent
ENTRY = 'modern-redesign.html'
CSS_URL = re.compile(r'''url\(\s*['"]?([^'"\)\s]+)''', re.I)
CSS_IMPORT = re.compile(r'''@import\s+['"]([^'"]+)''', re.I)


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'base':
            raise ValueError('A <base> tag is not supported by this relative-path export.')
        for key in ('src', 'poster', 'srcset', 'href', 'xlink:href', 'data'):
            value = attrs.get(key)
            if not value:
                continue
            if key == 'href' and tag == 'link':
                if not set(attrs.get('rel', '').split()) & {'stylesheet', 'icon', 'preload', 'modulepreload', 'manifest'}:
                    continue
            if key == 'data' and tag != 'object':
                continue
            if key == 'srcset':
                if value.startswith('data:'):
                    continue
                self.urls.extend(part.strip().split()[0] for part in value.split(',') if part.strip())
            else:
                self.urls.append(value)
        self.urls.extend(CSS_URL.findall(attrs.get('style', '')))


def dependency_urls(path, content):
    if path.suffix.lower() in ('.html', '.svg'):
        parser = References()
        parser.feed(content)
        return parser.urls + CSS_URL.findall(content)
    if path.suffix.lower() == '.css':
        return CSS_URL.findall(content) + CSS_IMPORT.findall(content)
    if path.suffix.lower() in ('.js', '.mjs'):
        # Current scripts do not request data files; include literal imports if added.
        return re.findall(r'''(?:import\s*(?:[^;]*?\sfrom\s*)?|import\s*\()\s*['"]([^'"]+)''', content)
    return []


def collect(entry_html):
    pending = [Path(ENTRY)]
    found = {}
    external = set()
    referenced_by = defaultdict(set)
    while pending:
        relative = pending.pop()
        if relative in found:
            continue
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f'Missing or outside-repository dependency: {relative}')
        content = entry_html.encode('utf-8') if str(relative) == ENTRY else path.read_bytes()
        found[relative] = content
        if path.suffix.lower() not in ('.html', '.svg', '.css', '.js', '.mjs'):
            continue
        for reference in dependency_urls(path, content.decode('utf-8')):
            url = urlsplit(reference)
            if url.scheme in ('http', 'https') or reference.startswith('//'):
                external.add(reference)
                continue
            if url.scheme or not url.path:
                continue
            if url.path.startswith('/'):
                raise ValueError(f'Root-relative dependency needs an explicit portable path: {reference}')
            target = (path.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(ROOT):
                raise ValueError(f'Dependency escapes repository: {reference}')
            relative_target = target.relative_to(ROOT)
            referenced_by[str(relative_target)].add(str(relative))
            pending.append(relative_target)
    return found, sorted(external), referenced_by


def metadata(html, base_url):
    return apply_metadata(html, base_url)


def crawler_files(base_url):
    if not base_url:
        return {}
    url = base_url.rstrip('/') + '/'
    return {
        Path('robots.txt'): ('User-agent: *\nAllow: /\n\nSitemap: '
                             + url + 'sitemap.xml\n').encode('utf-8'),
        Path('sitemap.xml'): (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            '  <url><loc>' + escape(url) + '</loc></url>\n</urlset>\n'
        ).encode('utf-8'),
    }


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='ZIP destination, preferably outside the repository')
    parser.add_argument('--base-url', help='Actual public HTTPS directory URL; omit for preview export')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.suffix.lower() != '.zip':
        parser.error('Output must end in .zip')
    try:
        html = metadata((ROOT / ENTRY).read_text(encoding='utf-8'), args.base_url)
        files, external, references = collect(html)
        files.update(crawler_files(args.base_url))
        unpacked = sum(map(len, files.values()))
        if len(files) > 500 or unpacked > 50_000_000:
            raise ValueError(f'Hosting limit exceeded: {len(files)} files / {unpacked} bytes unpacked')
        output.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=output.parent, suffix='.zip', delete=False) as temporary:
            temporary_path = Path(temporary.name)
        try:
            with zipfile.ZipFile(temporary_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for relative, content in sorted(files.items()):
                    archive.writestr('index.html' if str(relative) == ENTRY else relative.as_posix(), content)
            packed = temporary_path.stat().st_size
            if packed > 25_000_000:
                raise ValueError(f'ZIP hosting limit exceeded: {packed} bytes')
            temporary_path.replace(output)
        finally:
            temporary_path.unlink(missing_ok=True)
        manifest = {
            'entry': 'index.html', 'base_url': args.base_url,
            'file_count': len(files), 'unpacked_bytes': unpacked, 'zip_bytes': packed,
            'external_urls': external,
            'files': [{'path': 'index.html' if str(p) == ENTRY else p.as_posix(),
                       'bytes': len(data), 'referenced_by': sorted(references[str(p)])}
                      for p, data in sorted(files.items())],
        }
        manifest_path = output.with_suffix('.manifest.json')
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Created {output}\nFiles: {len(files)} / 500; unpacked: {unpacked} / 50000000 B; ZIP: {packed} / 25000000 B')
        print(f'Manifest: {manifest_path}')
        if not args.base_url:
            print('Preview export is noindex. Use --base-url for an indexable domain release.')
    except (OSError, ValueError) as error:
        parser.exit(1, f'Export failed: {error}\n')


if __name__ == '__main__':
    main()

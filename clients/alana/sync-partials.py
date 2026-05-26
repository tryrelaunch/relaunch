#!/usr/bin/env python3
"""
sync-partials.py — Single source of truth for nav and footer.

Reads _partials/nav.html and _partials/footer.html, injects them into every
page in this directory between <!-- NAV:START -->...<!-- NAV:END --> and
<!-- FOOTER:START -->...<!-- FOOTER:END --> markers.

On first run for a page (no markers yet), it locates the inline <nav> and
<footer> blocks and replaces them with marker-wrapped partial content.

After that, every run is idempotent — content between the markers gets
refreshed from the partials.

Placeholder substitution per-page:
  __BASE__       → ""  on homepage / "../" on subpages
  __HOME_HREF__  → "./" on homepage / "../" on subpages

Run this from the alana/ directory before every git push.
Wired into deploy.bat — you shouldn't need to run it manually.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PARTIALS_DIR = os.path.join(ROOT, '_partials')

NAV_START = '<!-- NAV:START -->'
NAV_END = '<!-- NAV:END -->'
FOOTER_START = '<!-- FOOTER:START -->'
FOOTER_END = '<!-- FOOTER:END -->'

SKIP_DIRS = {'css', 'js', 'images', '_partials', 'edit', '__pycache__'}


def load_partial(name):
    """Read a partial, strip the leading HTML comment header."""
    with open(os.path.join(PARTIALS_DIR, name), encoding='utf-8') as f:
        content = f.read()
    # remove leading <!-- ... --> comment if present
    content = re.sub(r'^\s*<!--.*?-->\s*', '', content, count=1, flags=re.DOTALL)
    return content.rstrip()


def find_pages():
    """Return sorted list of every index.html under alana/."""
    pages = []
    root_index = os.path.join(ROOT, 'index.html')
    if os.path.exists(root_index):
        pages.append(root_index)
    for entry in sorted(os.listdir(ROOT)):
        if entry in SKIP_DIRS or entry.startswith('.'):
            continue
        full = os.path.join(ROOT, entry)
        if os.path.isdir(full):
            inner = os.path.join(full, 'index.html')
            if os.path.exists(inner):
                pages.append(inner)
    return pages


def substitute(content, depth):
    """Replace placeholders based on page depth."""
    base = '' if depth == 0 else '../'
    home = './' if depth == 0 else '../'
    return content.replace('__BASE__', base).replace('__HOME_HREF__', home)


def find_matching_close(html, open_pos, open_tag='<nav', close_tag='</nav>'):
    """Depth-tracking matcher: find the </nav> that closes the <nav> at open_pos."""
    i = open_pos + len(open_tag)
    # advance past the opening tag's '>'
    gt = html.find('>', i)
    if gt == -1:
        return -1
    i = gt + 1
    depth = 1
    open_pat = re.compile(re.escape(open_tag) + r'(?:\s|>)')
    close_pat = re.compile(re.escape(close_tag))
    while i < len(html) and depth > 0:
        om = open_pat.search(html, i)
        cm = close_pat.search(html, i)
        if cm is None:
            return -1
        if om is not None and om.start() < cm.start():
            depth += 1
            i = om.end()
        else:
            depth -= 1
            i = cm.end()
            if depth == 0:
                return i
    return -1


def sync_nav(html, partial_content):
    """Replace inline nav OR content between NAV markers with the partial."""
    replacement = NAV_START + '\n' + partial_content + '\n' + NAV_END
    if NAV_START in html and NAV_END in html:
        pattern = re.compile(re.escape(NAV_START) + r'.*?' + re.escape(NAV_END), re.DOTALL)
        return pattern.sub(replacement, html, count=1)
    # locate first <nav> (outer nav, no class attribute on top-level)
    m = re.search(r'<nav(?:\s+[^>]*)?>', html)
    if not m:
        return html
    start = m.start()
    end = find_matching_close(html, start, '<nav', '</nav>')
    if end == -1:
        # nav truncated — splice from start to next major section
        nxt = re.search(r'<section\b|<main\b|<header\b', html[start + 5:])
        end = (start + 5 + nxt.start()) if nxt else len(html)
    return html[:start] + replacement + html[end:]


def sync_footer(html, partial_content):
    """Replace inline footer OR content between FOOTER markers with the partial."""
    replacement = FOOTER_START + '\n' + partial_content + '\n' + FOOTER_END
    if FOOTER_START in html and FOOTER_END in html:
        pattern = re.compile(re.escape(FOOTER_START) + r'.*?' + re.escape(FOOTER_END), re.DOTALL)
        return pattern.sub(replacement, html, count=1)
    m = re.search(r'<footer(?:\s+[^>]*)?>', html)
    if not m:
        # no footer at all — append before close tags
        return html + '\n' + replacement + '\n'
    start = m.start()
    cm = re.search(r'</footer>', html[start:])
    end = (start + cm.end()) if cm else len(html)
    return html[:start] + replacement + html[end:]


def ensure_clean_tail(html, depth):
    """Make sure the file ends with the marker-wrapped footer + script + close tags."""
    # Strip any trailing close tags / script tags that come AFTER FOOTER:END
    if FOOTER_END in html:
        end_pos = html.rfind(FOOTER_END) + len(FOOTER_END)
        html = html[:end_pos]
    # Strip any stray loose script/close-body/close-html that may remain elsewhere
    html = html.rstrip()
    script_src = 'js/main.js' if depth == 0 else '../js/main.js'
    tail = f'\n<script src="{script_src}"></script>\n</body>\n</html>\n'
    return html + tail


def main():
    nav_partial_raw = load_partial('nav.html')
    footer_partial_raw = load_partial('footer.html')
    pages = find_pages()
    print(f'sync-partials: {len(pages)} pages')
    for page in pages:
        rel = os.path.relpath(page, ROOT)
        depth = 0 if rel == 'index.html' else 1
        nav = substitute(nav_partial_raw, depth)
        footer = substitute(footer_partial_raw, depth)
        with open(page, encoding='utf-8', errors='replace') as f:
            html = f.read()
        new = sync_nav(html, nav)
        new = sync_footer(new, footer)
        new = ensure_clean_tail(new, depth)
        if new != html:
            with open(page, 'w', encoding='utf-8') as f:
                f.write(new)
            status = 'updated'
        else:
            status = 'unchanged'
        print(f'  {status:9}  {rel}')


if __name__ == '__main__':
    main()

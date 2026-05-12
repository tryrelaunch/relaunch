#!/usr/bin/env python3
"""
Walk index.html, find every text-bearing leaf element (h1..h6, p, button, a, li,
span that contains text but no nested block elements), and tag each with a
sequential id="edit-N". The AI editor uses these IDs to target elements.

- Idempotent: already-tagged elements keep their existing id and skip.
- Picks up after the highest existing edit-N so new elements get fresh IDs.
- Skips elements inside the AI editor widget itself (so it doesn't try to edit
  the editor's own UI).

Usage:
    cd clients/boatr-marketing
    py auto-tag.py
"""
import re
import sys
import subprocess
from pathlib import Path

# Auto-install beautifulsoup4 + lxml if missing
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4 + lxml...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', '--break-system-packages', 'beautifulsoup4', 'lxml'])
    from bs4 import BeautifulSoup

INDEX = Path(__file__).parent / 'index.html'

# Tags worth making editable
TARGET_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'button', 'a', 'li', 'span'}

# IDs and classes whose subtree should be ignored (the editor widget itself,
# the nav links wrapper, hidden Netlify form, etc.)
SKIP_PARENT_IDS = {'ew-panel', 'ew-fab', 'nav-links', 'hero-form-wrap', 'cta-form-wrap'}
SKIP_PARENT_CLASSES = {
    'ew-header', 'ew-body', 'ew-footer', 'ew-msg', 'ew-msgs', 'ew-pin-screen',
    'ew-chat-screen', 'ew-suggestions', 'ew-save-wrap', 'hero-checks'
}


def has_block_children(tag, target_tags):
    """True if any descendant is another target tag (i.e. this isn't a leaf)."""
    for child in tag.descendants:
        if hasattr(child, 'name') and child.name in target_tags:
            return True
    return False


def in_skip_zone(tag):
    """True if this tag is nested inside an explicitly skipped subtree."""
    for parent in tag.parents:
        if not hasattr(parent, 'attrs'):
            continue
        if parent.get('id') in SKIP_PARENT_IDS:
            return True
        for cls in (parent.get('class') or []):
            if cls in SKIP_PARENT_CLASSES:
                return True
    return False


def main():
    if not INDEX.exists():
        print(f"ERROR: {INDEX} not found")
        sys.exit(1)

    html = INDEX.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')

    # Find the highest existing edit-N number
    max_n = 0
    for el in soup.find_all(id=re.compile(r'^edit-\d+$')):
        m = re.match(r'^edit-(\d+)$', el.get('id'))
        if m:
            max_n = max(max_n, int(m.group(1)))

    counter = max_n + 1
    tagged = 0

    for tag in soup.find_all(TARGET_TAGS):
        # Already has any id? Skip — preserves existing edit-hero-h1 etc.
        if tag.get('id'):
            continue
        if in_skip_zone(tag):
            continue
        # Only tag leaf elements (no nested block children)
        if has_block_children(tag, TARGET_TAGS):
            continue
        # Skip empty or unreasonably long text
        text = tag.get_text(strip=True)
        if not text or len(text) > 800:
            continue
        # Skip icon-only spans (very short content like "✓" or "→")
        if len(text) < 2:
            continue
        tag['id'] = f'edit-{counter}'
        counter += 1
        tagged += 1

    INDEX.write_text(str(soup), encoding='utf-8')
    print(f'✓ Tagged {tagged} new element(s). Current max id: edit-{counter - 1}.')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
strip-demo.py v2 — Promote a Relaunch demo folder into a paying-customer
production folder.

Given a customer slug, this script:
  1. Strips demo-only elements from clients/<slug>/index.html
       (SEO banner, sticky CTA, demo widget, demo <script>)
  2. Injects the production edit-widget bootstrap loader (gates by JWT)
  3. Generates clients/<slug>/edit/index.html from the template
  4. Writes config/clients/<slug>.json with a bcrypt-hashed PIN

Usage:
  python strip-demo.py <slug> --pin <6-digit-pin>
                              --owner-email <email>
                              [--allowed-origins URL [URL ...]]
                              [--rotate-only]      # only update PIN; skip stripping/injecting
                              [--dry-run]          # print what would change

Examples:
  python strip-demo.py spork --pin 845984 --owner-email owner@sporkbend.com \\
      --allowed-origins https://client-spork.netlify.app https://sporkbend.com https://www.sporkbend.com

  python strip-demo.py spork --pin 472913 --rotate-only   # rotate PIN only

Requires:
  pip install bcrypt
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import bcrypt
except ImportError:
    print("ERROR: bcrypt is required. Install with: pip install bcrypt")
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent
CLIENTS_DIR = REPO_ROOT / "clients"
CONFIG_DIR = REPO_ROOT / "config" / "clients"
TEMPLATE_PATH = REPO_ROOT / "templates" / "edit-page.html"


# ─────────────────────────────────────────────
# Bootstrap script that goes into each client's index.html.
# Reads JWT from localStorage; if valid + slug matches, sets up
# window.__relaunchWidgetConfig and loads tryrelaunch.com/widget.js.
# ─────────────────────────────────────────────
WIDGET_BOOTSTRAP_TEMPLATE = """\
<!-- Relaunch production edit widget bootstrap (auto-generated) -->
<script>
(function () {
  var SLUG = "__SLUG__";
  var FN_BASE = "https://tryrelaunch.com/.netlify/functions";
  var WIDGET_URL = "https://tryrelaunch.com/widget.js";
  var token;
  try { token = localStorage.getItem("relaunch_jwt"); } catch (e) { return; }
  if (!token) return;

  // Decode JWT payload (no signature check — server validates).
  var payload;
  try {
    var parts = token.split(".");
    if (parts.length !== 3) return;
    var b64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    while (b64.length % 4) b64 += "=";
    payload = JSON.parse(atob(b64));
  } catch (e) { return; }

  if (payload.exp && payload.exp * 1000 < Date.now()) {
    try { localStorage.removeItem("relaunch_jwt"); } catch (e) {}
    return;
  }
  if (payload.slug !== SLUG) return;

  window.__relaunchWidgetConfig = {
    slug: SLUG,
    token: token,
    endpoint: FN_BASE + "/edit-persistent",
    editPageUrl: "/edit/",
    supportEmail: "support@tryrelaunch.com"
  };

  var s = document.createElement("script");
  s.src = WIDGET_URL;
  s.async = true;
  document.head.appendChild(s);
})();
</script>
"""


# ─────────────────────────────────────────────
# Helpers — same approach as v1 but tightened
# ─────────────────────────────────────────────

def strip_block_by_opening_tag(html, opening_pattern, tag='div'):
    """
    Find an opening tag matching opening_pattern, then walk forward
    counting <tag> opens and </tag> closes until depth returns to zero.
    Removes the entire block. Returns (new_html, count_removed).
    """
    count = 0
    while True:
        m = re.search(opening_pattern, html)
        if not m:
            return html, count
        start = m.start()
        pos = m.end()
        depth = 1
        i = pos
        open_tok = f'<{tag}'
        close_tok = f'</{tag}>'
        while i < len(html) and depth > 0:
            next_open = html.find(open_tok, i)
            next_close = html.find(close_tok, i)
            if next_close == -1:
                return html, count  # malformed; bail
            if next_open != -1 and next_open < next_close:
                ch = html[next_open + len(open_tok):next_open + len(open_tok) + 1]
                if ch in (' ', '>', '/', '\n', '\t'):
                    depth += 1
                i = next_open + len(open_tok)
            else:
                depth -= 1
                i = next_close + len(close_tok)
        if depth != 0:
            return html, count
        while i < len(html) and html[i] in ' \t\r\n':
            i += 1
        html = html[:start] + html[i:]
        count += 1


def strip_simple_tag(html, opening_pattern, closing):
    pattern = opening_pattern + r'.*?' + re.escape(closing)
    new_html, n = re.subn(pattern, '', html, flags=re.DOTALL)
    return new_html, n


def strip_css_section(html, section_name):
    open_pat = re.compile(
        r'/\*\s*[─\-=\s]*\s*' + re.escape(section_name) + r'\s*[─\-=\s]*\*/',
        re.IGNORECASE
    )
    m = open_pat.search(html)
    if not m:
        return html, 0
    start = m.start()
    after = m.end()
    next_section = re.search(r'/\*\s*[─\-=]{2,}', html[after:])
    style_end = html.find('</style>', after)
    if next_section is not None:
        end = after + next_section.start()
    elif style_end != -1:
        end = style_end
    else:
        return html, 0
    while end > start and html[end - 1] in ' \t\r\n':
        end -= 1
    new_html = html[:start] + html[end:]
    new_html = re.sub(r'\n{3,}', '\n\n', new_html)
    return new_html, 1


# ─────────────────────────────────────────────
# Strip demo elements (same as v1) + inject production bootstrap
# ─────────────────────────────────────────────

def transform_html(html, slug, log):
    # 1. Remove robots noindex meta — production sites should be indexed
    html, n = re.subn(
        r'\s*<meta\s+name="robots"\s+content="noindex"\s*/?>\s*',
        '\n',
        html
    )
    if n: log.append(f"removed: noindex meta tag x{n}")

    # 2. SEO banner block + its comment header
    html, n = strip_block_by_opening_tag(html, r'<div class="seo-banner">')
    if n: log.append(f"removed: SEO banner div x{n}")
    html, n = re.subn(
        r'<!--\s*╔[═╗]*[^╝]*?SEO BANNER[^╗]*?[╔═╝╚\s]*-->',
        '', html, flags=re.IGNORECASE | re.DOTALL
    )
    if n: log.append(f"removed: SEO banner comment header x{n}")

    # 3. Sticky bar
    html, n = strip_block_by_opening_tag(html, r'<div\s+class="sticky-bar(?:\s+show)?"\b')
    if n: log.append(f"removed: sticky-bar div x{n}")
    html, n = strip_block_by_opening_tag(
        html, r'<div\s+(?:id="sticky-bar"|class="[^"]*sticky-bar[^"]*")\b'
    )
    if n: log.append(f"removed: sticky-bar (id/alt class) x{n}")

    # 4. Edit FAB
    html, n = strip_simple_tag(html, r'<button\s+class="edit-fab"[^>]*>', '</button>')
    if n: log.append(f"removed: <button.edit-fab> x{n}")
    html, n = strip_simple_tag(html, r'<button\s+id="edit-fab"[^>]*>', '</button>')
    if n: log.append(f"removed: <button#edit-fab> x{n}")

    # 5. Edit panel
    html, n = strip_block_by_opening_tag(html, r'<div\s+class="edit-panel(?:\s+open)?"\b')
    if n: log.append(f"removed: <div.edit-panel> x{n}")
    html, n = strip_block_by_opening_tag(html, r'<div\s+id="edit-panel"\b')
    if n: log.append(f"removed: <div#edit-panel> x{n}")

    # 6. CSS sections
    for section in ['SEO BANNER', 'STICKY CLAIM BAR', 'EDIT WIDGET']:
        html, n = strip_css_section(html, section)
        if n: log.append(f"removed: CSS section [{section}]")

    # 7. Media-query rules for stripped elements
    html, n = re.subn(r'\s*\.sticky-bar\s*\{[^}]*\}', '', html)
    if n: log.append(f"removed: .sticky-bar media-query rules x{n}")
    html, n = re.subn(r'\s*\.edit-panel\s*\{[^}]*\}', '', html)
    if n: log.append(f"removed: .edit-panel media-query rules x{n}")

    # 8. Demo <script> blocks (anything that mentions demo function names)
    def is_demo_script(match):
        body = match.group(0)
        return any(token in body for token in (
            'toggleSEO', 'sendEdit', 'toggleEditPanel',
            'closeBar', 'edit-input', 'edit-messages',
            'edit-typing', 'sticky-bar', 'editFab'
        ))

    script_pat = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL)
    new_parts = []
    last_end = 0
    removed_scripts = 0
    for m in script_pat.finditer(html):
        if is_demo_script(m):
            new_parts.append(html[last_end:m.start()])
            last_end = m.end()
            removed_scripts += 1
    new_parts.append(html[last_end:])
    if removed_scripts:
        html = ''.join(new_parts)
        log.append(f"removed: demo <script> blocks x{removed_scripts}")

    # 9. Strip any previously-injected bootstrap (idempotent re-run)
    html, n = re.subn(
        r'<!-- Relaunch production edit widget bootstrap.*?</script>\s*',
        '', html, flags=re.DOTALL
    )
    if n: log.append(f"removed: previous bootstrap (idempotent) x{n}")

    # 10. Inject production widget bootstrap before </body>
    bootstrap = WIDGET_BOOTSTRAP_TEMPLATE.replace('__SLUG__', slug)
    if '</body>' in html:
        html = html.replace('</body>', bootstrap + '\n</body>', 1)
        log.append("injected: production widget bootstrap")
    else:
        html = html + '\n' + bootstrap
        log.append("appended: production widget bootstrap (no </body> found)")

    # 11. Final cleanup
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html


# ─────────────────────────────────────────────
# Generate edit/index.html from template
# ─────────────────────────────────────────────

def generate_edit_page(slug, log):
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(
            f"Edit page template not found at {TEMPLATE_PATH}. "
            "Make sure templates/edit-page.html exists."
        )
    template = TEMPLATE_PATH.read_text(encoding='utf-8')
    rendered = template.replace('__SLUG__', slug)
    edit_dir = CLIENTS_DIR / slug / 'edit'
    edit_dir.mkdir(parents=True, exist_ok=True)
    edit_path = edit_dir / 'index.html'
    edit_path.write_text(rendered, encoding='utf-8')
    log.append(f"wrote: clients/{slug}/edit/index.html")


# ─────────────────────────────────────────────
# Write/update client config
# ─────────────────────────────────────────────

def write_config(slug, pin, owner_email, allowed_origins, log, rotate_only=False):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config_path = CONFIG_DIR / f"{slug}.json"

    pin_hash = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt(rounds=10)).decode('utf-8')
    now_iso = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

    if config_path.exists() and rotate_only:
        existing = json.loads(config_path.read_text(encoding='utf-8'))
        existing['pin_hash'] = pin_hash
        existing['pin_rotated_at'] = now_iso
        config_path.write_text(json.dumps(existing, indent=2), encoding='utf-8')
        log.append(f"updated: config/clients/{slug}.json (pin rotated)")
        return existing

    new_config = {
        "slug": slug,
        "pin_hash": pin_hash,
        "owner_email": owner_email or None,
        "allowed_origins": allowed_origins or [],
        "created_at": now_iso,
        "pin_rotated_at": now_iso
    }

    if config_path.exists():
        existing = json.loads(config_path.read_text(encoding='utf-8'))
        existing['pin_hash'] = pin_hash
        existing['pin_rotated_at'] = now_iso
        if owner_email:
            existing['owner_email'] = owner_email
        if allowed_origins:
            existing['allowed_origins'] = allowed_origins
        config_path.write_text(json.dumps(existing, indent=2), encoding='utf-8')
        log.append(f"updated: config/clients/{slug}.json (preserving existing fields)")
        return existing

    config_path.write_text(json.dumps(new_config, indent=2), encoding='utf-8')
    log.append(f"wrote: config/clients/{slug}.json")
    return new_config


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Promote a demo to a paying client.")
    parser.add_argument('slug', help='Client slug (e.g., spork)')
    parser.add_argument('--pin', required=True, help='6-digit numeric PIN')
    parser.add_argument('--owner-email', default=None, help='Customer email')
    parser.add_argument('--allowed-origins', nargs='+', default=None,
                        help='List of full origin URLs allowed for CORS '
                             '(e.g. https://client-spork.netlify.app https://sporkbend.com)')
    parser.add_argument('--rotate-only', action='store_true',
                        help='Only update the PIN — skip stripping/injecting HTML')
    parser.add_argument('--dry-run', action='store_true',
                        help="Don't write files; just print what would happen")
    args = parser.parse_args()

    slug = args.slug.strip().lower()
    if not re.match(r'^[a-z0-9_-]+$', slug):
        print(f"ERROR: invalid slug '{slug}'. Use only a-z, 0-9, dash, underscore.")
        sys.exit(1)

    if not re.match(r'^\d{6}$', args.pin):
        print(f"ERROR: --pin must be exactly 6 digits.")
        sys.exit(1)

    client_dir = CLIENTS_DIR / slug
    if not client_dir.exists():
        print(f"ERROR: clients/{slug}/ does not exist. Run xcopy /E /I previews\\{slug} clients\\{slug} first.")
        sys.exit(1)

    index_path = client_dir / 'index.html'
    if not index_path.exists() and not args.rotate_only:
        print(f"ERROR: clients/{slug}/index.html does not exist.")
        sys.exit(1)

    log = []

    if args.rotate_only:
        if args.dry_run:
            print(f"[DRY RUN] Would rotate PIN for {slug}")
            return
        write_config(slug, args.pin, args.owner_email, args.allowed_origins,
                     log, rotate_only=True)
        print(f"\n✓ PIN rotated for {slug}")
        for line in log:
            print(f"  {line}")
        return

    # Full promotion
    original = index_path.read_text(encoding='utf-8')
    transformed = transform_html(original, slug, log)

    if args.dry_run:
        print(f"[DRY RUN] Would transform clients/{slug}/index.html")
        print(f"[DRY RUN] Original size: {len(original):,} bytes")
        print(f"[DRY RUN] New size:      {len(transformed):,} bytes")
        for line in log:
            print(f"  {line}")
        print("[DRY RUN] Would also generate edit page and config.")
        return

    index_path.write_text(transformed, encoding='utf-8')
    log.append(f"wrote: clients/{slug}/index.html")

    generate_edit_page(slug, log)
    write_config(slug, args.pin, args.owner_email, args.allowed_origins, log)

    print(f"\n✓ Promoted {slug} to production.")
    for line in log:
        print(f"  {line}")
    print(f"\nNext steps:")
    print(f"  1. Review: open clients/{slug}/index.html in a browser to verify the strip looks right")
    print(f"  2. Commit:")
    print(f"       git add clients/{slug}/ config/clients/{slug}.json")
    print(f'       git commit -m "Promote {slug} to live client with PIN auth"')
    print(f"       git push origin main")
    print(f"  3. Test:")
    print(f"       Visit https://client-{slug}.netlify.app/edit/")
    print(f"       Enter PIN: {args.pin}")
    print(f"       Should redirect to homepage with edit widget appearing.")


if __name__ == '__main__':
    main()

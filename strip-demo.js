#!/usr/bin/env node
/**
 * strip-demo.js — Promote a Relaunch demo folder into a paying-customer
 * production folder. Node.js port of strip-demo.py.
 *
 * Usage:
 *   node strip-demo.js <slug> --pin <6-digit-pin> --owner-email <email>
 *                              --allowed-origins URL [URL ...]
 *   node strip-demo.js <slug> --pin <new-pin> --rotate-only
 *   node strip-demo.js <slug> --pin <pin> --dry-run
 *
 * Examples:
 *   node strip-demo.js spork --pin 845984 --owner-email test@sporkbend.com \
 *     --allowed-origins https://client-spork.netlify.app
 *
 *   node strip-demo.js spork --pin 472913 --rotate-only
 */

const fs = require('fs');
const path = require('path');
const bcrypt = require('bcryptjs');

const REPO_ROOT = path.resolve(__dirname);
const CLIENTS_DIR = path.join(REPO_ROOT, 'clients');
const CONFIG_DIR = path.join(REPO_ROOT, 'config', 'clients');
const TEMPLATE_PATH = path.join(REPO_ROOT, 'templates', 'edit-page.html');

// ─────────────────────────────────────────────
// Bootstrap script template injected into each client's index.html.
// Reads JWT from localStorage; if valid + slug matches, sets up
// window.__relaunchWidgetConfig and loads tryrelaunch.com/widget.js.
// ─────────────────────────────────────────────
const WIDGET_BOOTSTRAP = `
<!-- Relaunch production edit widget bootstrap (auto-generated) -->
<script>
(function () {
  var SLUG = "__SLUG__";
  var FN_BASE = "https://tryrelaunch.com/.netlify/functions";
  var WIDGET_URL = "https://tryrelaunch.com/widget.js";
  var token;
  try { token = localStorage.getItem("relaunch_jwt"); } catch (e) { return; }
  if (!token) return;

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
`;

// ─────────────────────────────────────────────
// CLI parsing (no external deps)
// ─────────────────────────────────────────────
function parseArgs(argv) {
  const args = {
    _: [],
    pin: null,
    ownerEmail: null,
    allowedOrigins: null,
    rotateOnly: false,
    dryRun: false
  };
  let i = 2;
  while (i < argv.length) {
    const arg = argv[i];
    if (arg === '--pin') { args.pin = argv[++i]; }
    else if (arg === '--owner-email') { args.ownerEmail = argv[++i]; }
    else if (arg === '--allowed-origins') {
      args.allowedOrigins = [];
      while (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
        args.allowedOrigins.push(argv[++i]);
      }
    }
    else if (arg === '--rotate-only') { args.rotateOnly = true; }
    else if (arg === '--dry-run') { args.dryRun = true; }
    else if (!arg.startsWith('--')) { args._.push(arg); }
    i++;
  }
  return args;
}

// ─────────────────────────────────────────────
// Strip helpers
// ─────────────────────────────────────────────
function stripBlockByOpeningTag(html, openingPattern, tag = 'div') {
  let count = 0;
  const openTok = `<${tag}`;
  const closeTok = `</${tag}>`;
  const validNext = new Set([' ', '>', '/', '\n', '\t', '\r']);

  while (true) {
    const m = html.match(openingPattern);
    if (!m) return [html, count];
    const start = m.index;
    let i = start + m[0].length;
    let depth = 1;
    while (i < html.length && depth > 0) {
      const nextOpen = html.indexOf(openTok, i);
      const nextClose = html.indexOf(closeTok, i);
      if (nextClose === -1) return [html, count];
      if (nextOpen !== -1 && nextOpen < nextClose) {
        const ch = html[nextOpen + openTok.length] || '';
        if (validNext.has(ch)) depth++;
        i = nextOpen + openTok.length;
      } else {
        depth--;
        i = nextClose + closeTok.length;
      }
    }
    if (depth !== 0) return [html, count];
    while (i < html.length && /\s/.test(html[i])) i++;
    html = html.slice(0, start) + html.slice(i);
    count++;
  }
}

function stripSimpleTag(html, openingPatternSrc, closing) {
  const escapedClosing = closing.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const fullPat = new RegExp(openingPatternSrc + '[\\s\\S]*?' + escapedClosing, 'g');
  let count = 0;
  const out = html.replace(fullPat, () => { count++; return ''; });
  return [out, count];
}

function stripCssSection(html, sectionName) {
  const escaped = sectionName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const openPat = new RegExp(
    '/\\*\\s*[\\u2500\\-=\\s]*\\s*' + escaped + '\\s*[\\u2500\\-=\\s]*\\*/',
    'i'
  );
  const m = html.match(openPat);
  if (!m) return [html, 0];
  const start = m.index;
  const after = m.index + m[0].length;
  const remainder = html.slice(after);
  const nextSection = remainder.match(/\/\*\s*[\u2500\-=]{2,}/);
  const styleEnd = remainder.indexOf('</style>');
  let end;
  if (nextSection) end = after + nextSection.index;
  else if (styleEnd !== -1) end = after + styleEnd;
  else return [html, 0];
  while (end > start && /\s/.test(html[end - 1])) end--;
  let out = html.slice(0, start) + html.slice(end);
  out = out.replace(/\n{3,}/g, '\n\n');
  return [out, 1];
}

// ─────────────────────────────────────────────
// Main HTML transform
// ─────────────────────────────────────────────
function transformHtml(html, slug, log) {
  let n;

  // 1. Remove robots noindex
  let result = html.replace(/\s*<meta\s+name="robots"\s+content="noindex"\s*\/?>\s*/g, '\n');
  if (result !== html) log.push('removed: noindex meta tag');
  html = result;

  // 2. SEO banner
  [html, n] = stripBlockByOpeningTag(html, /<div class="seo-banner">/);
  if (n) log.push(`removed: SEO banner div x${n}`);
  result = html.replace(/<!--\s*\u2554[\u2550\u2557]*[\s\S]*?SEO BANNER[\s\S]*?[\u2554\u2550\u255d\u255a\s]*-->/gi, () => '');
  if (result !== html) log.push('removed: SEO banner comment header');
  html = result;

  // 3. Sticky bar
  [html, n] = stripBlockByOpeningTag(html, /<div\s+class="sticky-bar(?:\s+show)?"\b/);
  if (n) log.push(`removed: sticky-bar div x${n}`);
  [html, n] = stripBlockByOpeningTag(html, /<div\s+(?:id="sticky-bar"|class="[^"]*sticky-bar[^"]*")\b/);
  if (n) log.push(`removed: sticky-bar (alt) x${n}`);

  // 4. Edit FAB
  [html, n] = stripSimpleTag(html, '<button\\s+class="edit-fab"[^>]*>', '</button>');
  if (n) log.push(`removed: button.edit-fab x${n}`);
  [html, n] = stripSimpleTag(html, '<button\\s+id="edit-fab"[^>]*>', '</button>');
  if (n) log.push(`removed: button#edit-fab x${n}`);

  // 5. Edit panel
  [html, n] = stripBlockByOpeningTag(html, /<div\s+class="edit-panel(?:\s+open)?"\b/);
  if (n) log.push(`removed: div.edit-panel x${n}`);
  [html, n] = stripBlockByOpeningTag(html, /<div\s+id="edit-panel"\b/);
  if (n) log.push(`removed: div#edit-panel x${n}`);

  // 6. CSS sections
  for (const section of ['SEO BANNER', 'STICKY CLAIM BAR', 'EDIT WIDGET']) {
    [html, n] = stripCssSection(html, section);
    if (n) log.push(`removed: CSS section [${section}]`);
  }

  // 7. Media-query rules for stripped elements
  result = html.replace(/\s*\.sticky-bar\s*\{[^}]*\}/g, '');
  if (result !== html) log.push('removed: .sticky-bar media-query rules');
  html = result;
  result = html.replace(/\s*\.edit-panel\s*\{[^}]*\}/g, '');
  if (result !== html) log.push('removed: .edit-panel media-query rules');
  html = result;

  // 8. Demo <script> blocks
  const demoTokens = [
    'toggleSEO', 'sendEdit', 'toggleEditPanel', 'closeBar',
    'edit-input', 'edit-messages', 'edit-typing', 'sticky-bar', 'editFab'
  ];
  let removedScripts = 0;
  result = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, (match) => {
    if (demoTokens.some(t => match.includes(t))) {
      removedScripts++;
      return '';
    }
    return match;
  });
  if (removedScripts) log.push(`removed: demo <script> blocks x${removedScripts}`);
  html = result;

  // 9. Strip previously-injected bootstrap (idempotent re-run)
  result = html.replace(/<!-- Relaunch production edit widget bootstrap[\s\S]*?<\/script>\s*/g, '');
  if (result !== html) log.push('removed: previous bootstrap (idempotent)');
  html = result;

  // 10. Inject production widget bootstrap before </body>
  const bootstrap = WIDGET_BOOTSTRAP.replace(/__SLUG__/g, slug);
  if (html.includes('</body>')) {
    html = html.replace('</body>', bootstrap + '\n</body>');
    log.push('injected: production widget bootstrap');
  } else {
    html = html + '\n' + bootstrap;
    log.push('appended: production widget bootstrap (no </body> found)');
  }

  // 11. Final cleanup
  html = html.replace(/\n{3,}/g, '\n\n');
  return html;
}

// ─────────────────────────────────────────────
// Edit page generation
// ─────────────────────────────────────────────
function generateEditPage(slug, log) {
  if (!fs.existsSync(TEMPLATE_PATH)) {
    throw new Error(`Edit page template not found at ${TEMPLATE_PATH}. Make sure templates/edit-page.html exists.`);
  }
  const template = fs.readFileSync(TEMPLATE_PATH, 'utf-8');
  const rendered = template.replace(/__SLUG__/g, slug);
  const editDir = path.join(CLIENTS_DIR, slug, 'edit');
  fs.mkdirSync(editDir, { recursive: true });
  fs.writeFileSync(path.join(editDir, 'index.html'), rendered, 'utf-8');
  log.push(`wrote: clients/${slug}/edit/index.html`);
}

// ─────────────────────────────────────────────
// Config write/update
// ─────────────────────────────────────────────
function writeConfig(slug, pin, ownerEmail, allowedOrigins, rotateOnly, log) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  const configPath = path.join(CONFIG_DIR, `${slug}.json`);
  const pinHash = bcrypt.hashSync(pin, 10);
  const nowIso = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');

  if (fs.existsSync(configPath) && rotateOnly) {
    const existing = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    existing.pin_hash = pinHash;
    existing.pin_rotated_at = nowIso;
    fs.writeFileSync(configPath, JSON.stringify(existing, null, 2), 'utf-8');
    log.push(`updated: config/clients/${slug}.json (pin rotated)`);
    return;
  }

  let config;
  if (fs.existsSync(configPath)) {
    const existing = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    existing.pin_hash = pinHash;
    existing.pin_rotated_at = nowIso;
    if (ownerEmail) existing.owner_email = ownerEmail;
    if (allowedOrigins) existing.allowed_origins = allowedOrigins;
    config = existing;
    log.push(`updated: config/clients/${slug}.json (preserving fields)`);
  } else {
    config = {
      slug,
      pin_hash: pinHash,
      owner_email: ownerEmail || null,
      allowed_origins: allowedOrigins || [],
      created_at: nowIso,
      pin_rotated_at: nowIso
    };
    log.push(`wrote: config/clients/${slug}.json`);
  }
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
}

// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────
function main() {
  const args = parseArgs(process.argv);
  const slug = (args._[0] || '').trim().toLowerCase();

  if (!slug || !/^[a-z0-9_-]+$/.test(slug)) {
    console.error("Usage:");
    console.error("  node strip-demo.js <slug> --pin <6-digit-pin> [--owner-email <email>] [--allowed-origins URL ...]");
    console.error("  node strip-demo.js <slug> --pin <new-pin> --rotate-only");
    console.error("  node strip-demo.js <slug> --pin <pin> --dry-run");
    process.exit(1);
  }
  if (!args.pin || !/^\d{6}$/.test(args.pin)) {
    console.error("ERROR: --pin must be exactly 6 digits.");
    process.exit(1);
  }

  const clientDir = path.join(CLIENTS_DIR, slug);
  if (!fs.existsSync(clientDir)) {
    console.error(`ERROR: clients/${slug}/ does not exist. Run xcopy /E /I previews\\${slug} clients\\${slug} first.`);
    process.exit(1);
  }

  const indexPath = path.join(clientDir, 'index.html');
  if (!fs.existsSync(indexPath) && !args.rotateOnly) {
    console.error(`ERROR: clients/${slug}/index.html does not exist.`);
    process.exit(1);
  }

  const log = [];

  if (args.rotateOnly) {
    if (args.dryRun) {
      console.log(`[DRY RUN] Would rotate PIN for ${slug}`);
      return;
    }
    writeConfig(slug, args.pin, args.ownerEmail, args.allowedOrigins, true, log);
    console.log(`\n✓ PIN rotated for ${slug}`);
    log.forEach(line => console.log(`  ${line}`));
    return;
  }

  const original = fs.readFileSync(indexPath, 'utf-8');
  const transformed = transformHtml(original, slug, log);

  if (args.dryRun) {
    console.log(`[DRY RUN] Original size: ${original.length.toLocaleString()} bytes`);
    console.log(`[DRY RUN] New size:      ${transformed.length.toLocaleString()} bytes`);
    log.forEach(line => console.log(`  ${line}`));
    console.log("[DRY RUN] Would also generate edit page and config.");
    return;
  }

  fs.writeFileSync(indexPath, transformed, 'utf-8');
  log.push(`wrote: clients/${slug}/index.html`);

  generateEditPage(slug, log);
  writeConfig(slug, args.pin, args.ownerEmail, args.allowedOrigins, false, log);

  console.log(`\n✓ Promoted ${slug} to production.`);
  log.forEach(line => console.log(`  ${line}`));
  console.log(`\nNext steps:`);
  console.log(`  1. Verify: open clients/${slug}/index.html in a browser to check the strip looks right`);
  console.log(`  2. Commit:`);
  console.log(`       git add clients/${slug}/ config/clients/${slug}.json`);
  console.log(`       git commit -m "Promote ${slug} to live client with PIN auth"`);
  console.log(`       git push origin main`);
  console.log(`  3. Test:`);
  console.log(`       Visit https://client-${slug}.netlify.app/edit/`);
  console.log(`       Enter PIN: ${args.pin}`);
}

main();

// Persistent AI editor for boatrmarketing.com.
// Accepts admin PIN + an array of ops, applies them to index.html via cheerio,
// commits back to GitHub. Netlify auto-deploys on push. Live in ~60s.
//
// Op shapes:
//   { op: "replace_text", id: "edit-...", text: "new text" }
//   { op: "set_style",    id: "edit-...", style: "color: #0F172A; font-size: 64px;" }
//   { op: "set_attr",     id: "edit-...", attr: "src", value: "https://..." }
//
// Env vars required:
//   - BOATR_ADMIN_PIN  (long random string — gates persistent edits)
//   - GITHUB_TOKEN     (fine-grained PAT with Contents R/W on tryrelaunch/relaunch)

const cheerio = require('cheerio');

// In-memory PIN-attempt rate limit (per IP). Survives within one warm container.
const pinHits = new Map();
const PIN_WINDOW_MS = 60 * 1000;
const PIN_MAX_PER_WINDOW = 5;

const REPO = 'tryrelaunch/relaunch';
const FILE_PATH = 'clients/boatr-marketing/index.html';
const BRANCH = 'main';

exports.handler = async function (event) {
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers: corsHeaders() };
  }

  if (event.httpMethod !== 'POST') {
    return resp(405, { error: 'Method not allowed' });
  }

  const ip = (event.headers['x-nf-client-connection-ip']
    || (event.headers['x-forwarded-for'] || '').split(',')[0].trim()
    || 'unknown');

  // ── PIN rate limit ──────────────────────────────────────
  const now = Date.now();
  const rec = pinHits.get(ip) || { count: 0, resetAt: now + PIN_WINDOW_MS };
  if (now > rec.resetAt) { rec.count = 0; rec.resetAt = now + PIN_WINDOW_MS; }

  let body;
  try { body = JSON.parse(event.body); }
  catch { return resp(400, { error: 'Invalid JSON' }); }

  const { pin, ops } = body;
  if (!pin || typeof pin !== 'string') return resp(400, { error: 'Missing pin' });
  if (!Array.isArray(ops) || ops.length === 0) return resp(400, { error: 'No ops provided' });
  if (ops.length > 50) return resp(400, { error: 'Too many ops in one request (max 50)' });

  // ── PIN check ───────────────────────────────────────────
  const ADMIN = process.env.BOATR_ADMIN_PIN;
  if (!ADMIN) return resp(500, { error: 'Admin PIN not configured on server' });

  // Bump hit counter only on actual PIN comparisons
  rec.count++;
  pinHits.set(ip, rec);
  if (rec.count > PIN_MAX_PER_WINDOW) {
    const retryAfter = Math.ceil((rec.resetAt - now) / 1000);
    return resp(429, { error: 'Too many save attempts. Try again in a minute.', retryAfter });
  }

  if (!constantTimeEqual(pin, ADMIN)) {
    return resp(401, { error: 'Demo mode — your edits aren\'t saving. To save permanently, use the admin PIN.' });
  }

  // ── GitHub auth ─────────────────────────────────────────
  const TOKEN = process.env.GITHUB_TOKEN;
  if (!TOKEN) return resp(500, { error: 'GITHUB_TOKEN not configured on server' });

  // ── Fetch current file ──────────────────────────────────
  let fileData;
  try {
    const r = await fetch(`https://api.github.com/repos/${REPO}/contents/${encodeURI(FILE_PATH)}?ref=${BRANCH}`, {
      headers: ghHeaders(TOKEN)
    });
    if (!r.ok) {
      return resp(502, { error: `GitHub fetch failed: ${r.status}`, detail: await r.text() });
    }
    fileData = await r.json();
  } catch (err) {
    return resp(502, { error: `GitHub fetch error: ${err.message}` });
  }

  const currentContent = Buffer.from(fileData.content, 'base64').toString('utf-8');
  const currentSha = fileData.sha;

  // ── Apply ops via cheerio ──────────────────────────────
  // Disable entity decoding to preserve existing markup exactly.
  const $ = cheerio.load(currentContent, { decodeEntities: false }, false);

  const applied = [];
  const skipped = [];

  for (const op of ops) {
    const sel = `#${cssEscape(op.id)}`;
    const $el = $(sel);
    if (!$el.length) { skipped.push({ id: op.id, reason: 'not found' }); continue; }

    try {
      if (op.op === 'replace_text') {
        if (typeof op.text !== 'string') { skipped.push({ id: op.id, reason: 'missing text' }); continue; }
        $el.text(op.text);
        applied.push({ id: op.id, op: 'replace_text' });
      } else if (op.op === 'set_style') {
        if (typeof op.style !== 'string') { skipped.push({ id: op.id, reason: 'missing style' }); continue; }
        // Sanitize: forbid url() with javascript: scheme; allow only css declarations
        const safeStyle = sanitizeStyle(op.style);
        const existing = $el.attr('style') || '';
        $el.attr('style', mergeStyle(existing, safeStyle));
        applied.push({ id: op.id, op: 'set_style' });
      } else if (op.op === 'set_attr') {
        const allowedAttrs = ['src', 'href', 'alt', 'title', 'aria-label', 'placeholder'];
        if (!allowedAttrs.includes(op.attr)) { skipped.push({ id: op.id, reason: `attr ${op.attr} not allowed` }); continue; }
        if (typeof op.value !== 'string') { skipped.push({ id: op.id, reason: 'missing value' }); continue; }
        // Block javascript: schemes
        if (/^javascript:/i.test(op.value.trim())) { skipped.push({ id: op.id, reason: 'unsafe value' }); continue; }
        $el.attr(op.attr, op.value);
        applied.push({ id: op.id, op: 'set_attr', attr: op.attr });
      } else {
        skipped.push({ id: op.id, reason: `unknown op ${op.op}` });
      }
    } catch (err) {
      skipped.push({ id: op.id, reason: `apply failed: ${err.message}` });
    }
  }

  if (applied.length === 0) {
    return resp(400, { error: 'No ops could be applied', skipped });
  }

  // Render — cheerio in non-document mode preserves the existing doc structure.
  const newContent = $.html();

  // ── Commit to GitHub ──────────────────────────────────
  const summary = applied.length === 1
    ? `boatr edit · ${applied[0].op} ${applied[0].id}`
    : `boatr edit · ${applied.length} ops`;
  const commitMsg = summary + (skipped.length ? ` (${skipped.length} skipped)` : '');

  try {
    const r = await fetch(`https://api.github.com/repos/${REPO}/contents/${encodeURI(FILE_PATH)}`, {
      method: 'PUT',
      headers: { ...ghHeaders(TOKEN), 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: commitMsg,
        content: Buffer.from(newContent, 'utf-8').toString('base64'),
        sha: currentSha,
        branch: BRANCH
      })
    });
    if (!r.ok) {
      return resp(502, { error: `GitHub commit failed: ${r.status}`, detail: await r.text() });
    }
    const commitData = await r.json();
    return resp(200, {
      success: true,
      commit: commitData.commit.sha.slice(0, 7),
      url: commitData.commit.html_url,
      applied: applied.length,
      skipped,
      message: `Saved · live in ~60 seconds at boatrmarketing.com`
    });
  } catch (err) {
    return resp(502, { error: `GitHub commit error: ${err.message}` });
  }
};

// ── helpers ─────────────────────────────────────────────
function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };
}
function resp(statusCode, obj) {
  return {
    statusCode,
    headers: { 'Content-Type': 'application/json', ...corsHeaders() },
    body: JSON.stringify(obj)
  };
}
function ghHeaders(token) {
  return {
    'Authorization': `token ${token}`,
    'Accept': 'application/vnd.github+json',
    'User-Agent': 'boatrmarketing-editor',
    'X-GitHub-Api-Version': '2022-11-28'
  };
}
function constantTimeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}
function cssEscape(s) {
  // Escape an id for use as a CSS selector
  return String(s).replace(/([!"#$%&'()*+,./:;<=>?@[\\\]^`{|}~])/g, '\\$1');
}
function sanitizeStyle(style) {
  // Strip dangerous patterns. Allow basic CSS declarations only.
  let s = String(style).trim();
  // Remove `expression(...)` (IE-era XSS vector)
  s = s.replace(/expression\s*\([^)]*\)/gi, '');
  // Block `url(javascript:...)` etc.
  s = s.replace(/url\s*\(\s*['"]?\s*javascript:[^)]*\)/gi, '');
  // Block @import
  s = s.replace(/@import[^;]*;/gi, '');
  return s;
}
function mergeStyle(existing, incoming) {
  // Parse "k: v; k: v" into a map, merge, re-serialize.
  const toMap = (str) => {
    const m = new Map();
    String(str).split(';').forEach(part => {
      const idx = part.indexOf(':');
      if (idx < 0) return;
      const k = part.slice(0, idx).trim().toLowerCase();
      const v = part.slice(idx + 1).trim();
      if (k && v) m.set(k, v);
    });
    return m;
  };
  const ex = toMap(existing);
  const inc = toMap(incoming);
  for (const [k, v] of inc) ex.set(k, v);
  return Array.from(ex.entries()).map(([k, v]) => `${k}: ${v}`).join('; ');
}

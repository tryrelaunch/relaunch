// netlify/functions/edit-persistent.js
// Customer-authenticated AI text editor.
// Verifies JWT, validates origin, asks Claude for structured changes,
// applies them via parse-aware text replacement, commits to GitHub.

const jwt = require('jsonwebtoken');
const cheerio = require('cheerio');

const RATE_LIMIT_MAX = 10;
const RATE_LIMIT_WINDOW_MS = 60 * 60 * 1000;
const MAX_EDIT_TEXT_LENGTH = 500;
const MAX_REQUEST_LENGTH = 500;
const COMMIT_RETRY_ATTEMPTS = 3;
const GITHUB_REPO = 'tryrelaunch/relaunch';

// In-memory rate limiter keyed by JWT subject (slug + iat).
// Best-effort; resets on cold start. Phase 2: distributed counter.
const editAttempts = new Map();

// ─────────────────────────────────────────────
// Response helpers
// ─────────────────────────────────────────────

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Vary': 'Origin'
  };
}

function jsonResponse(statusCode, body, origin) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json',
      ...(origin ? corsHeaders(origin) : {})
    },
    body: JSON.stringify(body)
  };
}

// ─────────────────────────────────────────────
// GitHub Contents API
// ─────────────────────────────────────────────

async function loadClientConfig(slug) {
  const cleanSlug = String(slug).replace(/[^a-z0-9_-]/gi, '');
  if (!cleanSlug) return null;
  const url = `https://api.github.com/repos/${GITHUB_REPO}/contents/config/clients/${cleanSlug}.json`;
  try {
    const res = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });
    if (!res.ok) return null;
    const data = await res.json();
    return JSON.parse(Buffer.from(data.content, 'base64').toString('utf-8'));
  } catch (e) {
    console.error(`loadClientConfig(${slug}) failed:`, e.message);
    return null;
  }
}

async function fetchClientHtml(slug, page = '') {
  const filePath = page ? `clients/${slug}/${page}/index.html` : `clients/${slug}/index.html`;
  const url = `https://api.github.com/repos/${GITHUB_REPO}/contents/${filePath}`;
  const res = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json'
    }
  });
  if (!res.ok) {
    const err = new Error(`fetchClientHtml(${slug}) failed: ${res.status}`);
    err.status = res.status;
    throw err;
  }
  const data = await res.json();
  return {
    content: Buffer.from(data.content, 'base64').toString('utf-8'),
    sha: data.sha
  };
}

async function commitClientHtml(slug, page, content, sha, message) {
  const filePath = page ? `clients/${slug}/${page}/index.html` : `clients/${slug}/index.html`;
  const url = `https://api.github.com/repos/${GITHUB_REPO}/contents/${filePath}`;
  const res = await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message,
      content: Buffer.from(content, 'utf-8').toString('base64'),
      sha,
      branch: 'main'
    })
  });
  if (!res.ok) {
    const errText = await res.text();
    const err = new Error(`commitClientHtml(${slug}) failed: ${res.status}`);
    err.status = res.status;
    err.body = errText;
    throw err;
  }
  return await res.json();
}

// ─────────────────────────────────────────────
// HTML parsing & validated text replacement
// ─────────────────────────────────────────────

/**
 * Build the editable allowlist by scanning the live HTML for
 * id="edit-..." elements that contain ONLY text (no child elements).
 * Returns a Map<id, currentText>.
 */
function extractEditableElements(html) {
  const $ = cheerio.load(html, { decodeEntities: false });
  const elements = {};
  $('[id^="edit-"]').each((_i, el) => {
    const $el = $(el);
    const id = $el.attr('id');
    if (!id) return;
    if ($el.children().length > 0) return; // skip nested-HTML elements
    elements[id] = $el.text().trim();
  });
  return elements;
}

/**
 * Apply validated changes to HTML using cheerio's .text() — replaces text node only,
 * never innerHTML or string concatenation. Safe by construction.
 */
function applyChanges(html, validatedChanges) {
  const $ = cheerio.load(html, { decodeEntities: false });
  for (const change of validatedChanges) {
    const $el = $(`#${escapeForCss(change.id)}`);
    if ($el.length === 0) continue;
    if ($el.children().length > 0) continue; // safety
    $el.text(change.text);
  }
  return $.html();
}

function escapeForCss(s) {
  return String(s).replace(/[^a-zA-Z0-9_-]/g, '');
}

/**
 * Sanitize a page path from the widget. Must be a slug-style relative path
 * like "menu" or "menu/lunch" — no path traversal, no absolute paths, no
 * filesystem escapes. Returns the cleaned path, or null if the input is invalid.
 * Empty string is the homepage (allowed).
 */
function sanitizePage(page) {
  if (page === undefined || page === null || page === '') return '';
  const cleaned = String(page).trim();
  if (cleaned === '') return '';
  // Reject any path traversal or absolute paths
  if (cleaned.includes('..') || cleaned.includes('\\')) return null;
  if (cleaned.startsWith('/') || cleaned.endsWith('/')) {
    // Strip leading/trailing slashes; the widget commonly sends "/menu/"
    return sanitizePage(cleaned.replace(/^\/+|\/+$/g, ''));
  }
  // Allow only [a-z0-9-] segments separated by single slashes
  const segments = cleaned.split('/');
  for (const seg of segments) {
    if (!/^[a-z0-9-]+$/i.test(seg)) return null;
  }
  return segments.join('/');
}

// ─────────────────────────────────────────────
// Claude
// ─────────────────────────────────────────────

const CLAUDE_SYSTEM_PROMPT = `You are a small-business website editor.
You receive a JSON map of editable text elements (id → current text) and a request describing what to change.

Return ONLY a JSON object with this exact shape, with no preamble or commentary:
{
  "changes": [
    { "id": "edit-foo", "text": "new plain text" }
  ],
  "confirmation": "Brief one-sentence summary of what was changed."
}

Rules:
- Only return changes for IDs that appear in the input map. Never invent IDs.
- "text" must be plain text — no HTML tags, no quotes around the value, no markdown.
- Preserve the original tone and approximate length unless the user requests otherwise.
- If the user asks for something you cannot do (add new menu items, change images, change layout, edit elements not in the map), return:
  { "changes": [], "confirmation": "I can't do that automatically — try the 'Request human help' button." }
- Be conservative. Do not change anything that wasn't requested. If a request affects multiple elements (e.g., "update all weekend hours"), include each.`;

async function callClaude(request, editableMap) {
  const apiKey = process.env.CLAUDE_API_KEY;
  const model = process.env.ANTHROPIC_MODEL || 'claude-haiku-4-5-20251001';

  const userMessage = `Editable elements:\n${JSON.stringify(editableMap, null, 2)}\n\nRequest: ${request}`;

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model,
      max_tokens: 1024,
      system: CLAUDE_SYSTEM_PROMPT,
      messages: [{ role: 'user', content: userMessage }]
    })
  });

  if (!res.ok) {
    const body = await res.text();
    const err = new Error(`Anthropic API error: ${res.status}`);
    err.body = body;
    throw err;
  }

  const data = await res.json();
  const text = data.content?.[0]?.text || '';

  // Robust JSON extraction — Claude is well-behaved but be defensive
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start === -1 || end === -1 || end <= start) {
    throw new Error('Claude response missing JSON');
  }
  return JSON.parse(text.slice(start, end + 1));
}

// ─────────────────────────────────────────────
// Validation
// ─────────────────────────────────────────────

function validateChanges(rawChanges, allowlist) {
  if (!Array.isArray(rawChanges)) return [];
  const out = [];
  const seen = new Set();
  for (const c of rawChanges) {
    if (!c || typeof c !== 'object') continue;
    if (typeof c.id !== 'string' || typeof c.text !== 'string') continue;
    if (!allowlist.has(c.id)) continue;
    if (seen.has(c.id)) continue;
    if (c.text.length > MAX_EDIT_TEXT_LENGTH) continue;
    if (/[<>]/.test(c.text)) continue;          // no angle brackets
    if (/[\u0000-\u0008\u000b-\u001f]/.test(c.text)) continue; // no control chars
    seen.add(c.id);
    out.push({ id: c.id, text: c.text });
  }
  return out;
}

// ─────────────────────────────────────────────
// Commit retry loop (handles 409 SHA conflicts)
// ─────────────────────────────────────────────

async function commitWithRetry(slug, page, validatedChanges, message) {
  let lastErr;
  for (let i = 0; i < COMMIT_RETRY_ATTEMPTS; i++) {
    try {
      const { content, sha } = await fetchClientHtml(slug, page);
      const newContent = applyChanges(content, validatedChanges);
      // No-op detection: if content didn't change, don't commit
      if (newContent === content) {
        return { noop: true };
      }
      return await commitClientHtml(slug, page, newContent, sha, message);
    } catch (e) {
      lastErr = e;
      if (e.status !== 409 || i === COMMIT_RETRY_ATTEMPTS - 1) throw e;
      await new Promise(r => setTimeout(r, 250 * (i + 1)));
    }
  }
  throw lastErr;
}

// ─────────────────────────────────────────────
// Handler
// ─────────────────────────────────────────────

exports.handler = async function (event) {
  // CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: corsHeaders(event.headers.origin || '*'),
      body: ''
    };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: '' };
  }

  const origin = event.headers.origin;
  if (!origin) {
    return { statusCode: 403, body: '' };
  }

  // Verify JWT
  const auth = event.headers.authorization || event.headers.Authorization || '';
  if (!auth.startsWith('Bearer ')) {
    return jsonResponse(401, { error: 'no_token' }, origin);
  }
  const token = auth.slice(7).trim();
  let payload;
  try {
    payload = jwt.verify(token, process.env.JWT_SECRET, { algorithms: ['HS256'] });
  } catch (e) {
    return jsonResponse(401, { error: 'invalid_token' }, origin);
  }

  // Parse body
  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch {
    return jsonResponse(400, { error: 'invalid_json' }, origin);
  }
  const { slug, request, page = '' } = body;
  if (!slug || !request) {
    return jsonResponse(400, { error: 'missing_fields' }, origin);
  }
  const cleanPage = sanitizePage(page);
  if (cleanPage === null) {
    return jsonResponse(400, { error: 'invalid_page' }, origin);
  }
  if (typeof request !== 'string' || request.length > MAX_REQUEST_LENGTH) {
    return jsonResponse(400, { error: 'request_invalid' }, origin);
  }
  if (slug !== payload.slug) {
    return jsonResponse(403, { error: 'slug_mismatch' }, origin);
  }

  // Verify origin against client config (deny-by-default CORS)
  const config = await loadClientConfig(slug);
  if (!config) {
    return jsonResponse(403, { error: 'config_not_found' }, origin);
  }
  const allowed = Array.isArray(config.allowed_origins) ? config.allowed_origins : [];
  if (!allowed.includes(origin)) {
    return jsonResponse(403, { error: 'origin_not_allowed' }, origin);
  }

  // Token-stale check: invalidates any token issued BEFORE the last PIN rotation.
  // This is the intent-based revocation backstop that lets us safely use 1-year JWTs:
  // tokens are long-lived for UX, but rotating the PIN instantly invalidates all
  // previously-issued tokens. The widget treats 401 as "log in again".
  if (config.pin_rotated_at) {
    const rotatedAtSec = Math.floor(new Date(config.pin_rotated_at).getTime() / 1000);
    if (Number.isFinite(rotatedAtSec) && payload.iat && payload.iat < rotatedAtSec) {
      return jsonResponse(401, { error: 'token_stale' }, origin);
    }
  }

  // Rate limit by JWT (subject = slug + issued-at second)
  const jwtKey = `${payload.slug}:${payload.iat || 0}`;
  const now = Date.now();
  const record = editAttempts.get(jwtKey) || { count: 0, resetAt: now + RATE_LIMIT_WINDOW_MS };
  if (now > record.resetAt) {
    record.count = 0;
    record.resetAt = now + RATE_LIMIT_WINDOW_MS;
  }
  record.count++;
  editAttempts.set(jwtKey, record);
  if (record.count > RATE_LIMIT_MAX) {
    return jsonResponse(429, { error: 'rate_limited', retry_after_minutes: 60 }, origin);
  }

  // Main pipeline
  try {
    let currentHtml;
    try {
      ({ content: currentHtml } = await fetchClientHtml(slug, cleanPage));
    } catch (e) {
      if (e.status === 404) {
        return jsonResponse(404, { error: 'page_not_found', page: cleanPage || '(homepage)' }, origin);
      }
      throw e;
    }
    const editableMap = extractEditableElements(currentHtml);
    const allowlist = new Set(Object.keys(editableMap));

    if (allowlist.size === 0) {
      return jsonResponse(500, { error: 'no_editable_elements' }, origin);
    }

    const claudeResp = await callClaude(request, editableMap);
    const validated = validateChanges(claudeResp.changes, allowlist);

    if (validated.length === 0) {
      return jsonResponse(200, {
        success: true,
        changes: [],
        confirmation: claudeResp.confirmation
          || "I couldn't make that change automatically. Try being more specific, or use 'Request human help' for changes the AI can't handle."
      }, origin);
    }

    const truncated = request.length > 80 ? request.slice(0, 80) + '...' : request;
    const pageLabel = cleanPage ? `/${cleanPage}` : '';
    const commitMessage = `AI edit by ${slug}${pageLabel}: ${truncated}`;
    await commitWithRetry(slug, cleanPage, validated, commitMessage);

    return jsonResponse(200, {
      success: true,
      changes: validated,
      confirmation: claudeResp.confirmation
        || `Saved ${validated.length} change${validated.length === 1 ? '' : 's'}. Your live site updates within a minute or two.`
    }, origin);

  } catch (e) {
    console.error('edit-persistent error:', e.message, e.stack);
    return jsonResponse(500, { error: 'server_error' }, origin);
  }
};

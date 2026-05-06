// netlify/functions/auth.js
// Verifies a customer's PIN and issues a 30-day JWT.
// CORS: deny by default. Origin must match config.allowed_origins for the slug.

const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const RATE_LIMIT_MAX = 5;
const RATE_LIMIT_WINDOW_MS = 15 * 60 * 1000;
const MIN_RESPONSE_MS = 200; // soft constant-time guard
const GITHUB_REPO = 'tryrelaunch/relaunch';

// In-memory rate limiter (best-effort; documented limitation).
// Map<ip, { count, resetAt }>
const attempts = new Map();

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
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

function getClientIp(event) {
  return (event.headers['x-nf-client-connection-ip']
    || (event.headers['x-forwarded-for'] || '').split(',')[0].trim()
    || 'unknown');
}

function checkRateLimit(ip) {
  const now = Date.now();
  const record = attempts.get(ip) || { count: 0, resetAt: now + RATE_LIMIT_WINDOW_MS };
  if (now > record.resetAt) {
    record.count = 0;
    record.resetAt = now + RATE_LIMIT_WINDOW_MS;
  }
  record.count++;
  attempts.set(ip, record);
  return record.count <= RATE_LIMIT_MAX;
}

async function loadClientConfig(slug) {
  const cleanSlug = String(slug).replace(/[^a-z0-9_-]/gi, '');
  if (!cleanSlug) return null;
  const url = `https://api.github.com/repos/${GITHUB_REPO}/contents/config/clients/${cleanSlug}.json`;
  try {
    const res = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
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

async function softTimeFloor(startMs) {
  const elapsed = Date.now() - startMs;
  if (elapsed < MIN_RESPONSE_MS) {
    await new Promise(r => setTimeout(r, MIN_RESPONSE_MS - elapsed));
  }
}

exports.handler = async function (event) {
  const start = Date.now();

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

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch {
    return jsonResponse(400, { error: 'invalid_json' });
  }

  const { slug, pin } = body;
  if (!slug || !pin) {
    return jsonResponse(400, { error: 'missing_fields' });
  }

  // Strict PIN format: exactly 6 digits
  if (!/^\d{6}$/.test(pin)) {
    await softTimeFloor(start);
    return jsonResponse(401, { error: 'wrong_pin' });
  }

  // Rate limit by IP
  const ip = getClientIp(event);
  if (!checkRateLimit(ip)) {
    return jsonResponse(429, { error: 'rate_limited', retry_after_minutes: 15 });
  }

  // Load config (this is also where we discover whether the slug exists,
  // but we never tell the caller that — same response for missing slug & wrong pin).
  const config = await loadClientConfig(slug);
  if (!config || !config.pin_hash) {
    await softTimeFloor(start);
    return jsonResponse(401, { error: 'wrong_pin' });
  }

  // Deny-by-default CORS — Origin must be in allowed_origins for this slug
  const allowed = Array.isArray(config.allowed_origins) ? config.allowed_origins : [];
  if (!allowed.includes(origin)) {
    return jsonResponse(403, { error: 'origin_not_allowed' });
  }

  // Verify PIN
  let valid = false;
  try {
    valid = await bcrypt.compare(pin, config.pin_hash);
  } catch (e) {
    console.error(`bcrypt.compare error for slug=${slug}:`, e.message);
  }

  await softTimeFloor(start);

  if (!valid) {
    return jsonResponse(401, { error: 'wrong_pin' }, origin);
  }

  // Issue JWT
  const token = jwt.sign(
    { slug },
    process.env.JWT_SECRET,
    { expiresIn: '30d', algorithm: 'HS256' }
  );

  return jsonResponse(200, { token, slug }, origin);
};

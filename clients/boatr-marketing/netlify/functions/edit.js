// AI editor function for boatrmarketing.com — session-only edits.
// Same pattern as tryrelaunch.com's edit.js. Self-contained per site.

const hits = new Map();
const WINDOW_MS = 60 * 1000;
const MAX_PER_WINDOW = 10;
const MAX_CONTENT_LEN = 50000;

exports.handler = async function (event) {

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }

  // Rate limit by IP
  const ip = (event.headers['x-nf-client-connection-ip']
    || (event.headers['x-forwarded-for'] || '').split(',')[0].trim()
    || 'unknown');

  const now = Date.now();
  const record = hits.get(ip) || { count: 0, resetAt: now + WINDOW_MS };
  if (now > record.resetAt) {
    record.count = 0;
    record.resetAt = now + WINDOW_MS;
  }
  record.count++;
  hits.set(ip, record);

  if (record.count > MAX_PER_WINDOW) {
    const retryAfter = Math.ceil((record.resetAt - now) / 1000);
    return {
      statusCode: 429,
      headers: { 'Content-Type': 'application/json', 'Retry-After': String(retryAfter) },
      body: JSON.stringify({ error: 'Too many edits. Try again in a minute.' })
    };
  }

  let body;
  try { body = JSON.parse(event.body); }
  catch { return { statusCode: 400, body: 'Invalid JSON' }; }

  const { request, content } = body;
  if (!request || !content) return { statusCode: 400, body: 'Missing request or content' };
  if (request.length > 500) return { statusCode: 400, body: 'Request too long' };
  if (JSON.stringify(content).length > MAX_CONTENT_LEN) {
    return { statusCode: 400, body: 'Content payload too large' };
  }

  // Cheap prompt-injection guard
  const lower = request.toLowerCase();
  if (lower.includes('ignore previous') || lower.includes('system prompt') || lower.includes('reveal instructions')) {
    return { statusCode: 400, body: 'Invalid request' };
  }

  const CLAUDE_API_KEY = process.env.CLAUDE_API_KEY;
  if (!CLAUDE_API_KEY) return { statusCode: 500, body: 'API key not configured' };

  const MODEL = process.env.ANTHROPIC_MODEL;
  if (!MODEL) {
    return { statusCode: 500, body: 'ANTHROPIC_MODEL env var not configured' };
  }

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 1000,
        temperature: 0,
        system: `You are a website content editor for Boatr Marketing — a marine-tourism marketing service.

You receive a JSON object of all editable elements on the page (element id → current text).

Respond ONLY with a valid JSON object — no markdown, no explanation:
{
  "ops": [
    { "op": "replace_text", "id": "edit-hero-h1", "text": "new text" },
    { "op": "set_style",    "id": "edit-hero-h1", "style": "color: #0F172A; font-size: 64px;" },
    { "op": "set_attr",     "id": "edit-hero-img", "attr": "src", "value": "https://..." }
  ],
  "confirmation": "One sentence describing what you changed."
}

Op types:
- replace_text: change inner text (use for any text content change)
- set_style: add inline CSS declarations (use for colors, sizes, spacing). Merge with existing — don't strip what you don't change.
- set_attr: change an allowed attribute. Allowed: src, href, alt, title, aria-label, placeholder.

MATCHING RULES — follow this algorithm EXACTLY:

Step 1: If the user references text in quotes (e.g. "the 'Get free preview' button"), the quoted phrase is your search key. Treat the quoted phrase as a contiguous string.

Step 2: For each id in the content map, check if its textContent contains the search key as a contiguous substring (case-insensitive, ignoring trailing/leading whitespace and arrows like →).

Step 3: Emit ops ONLY for ids that passed step 2. Do NOT include ids that share some words but don't contain the full quoted phrase as a substring.

Worked examples:
- Search key: "Get free preview"
  - "Get free preview →"  → MATCH (contains "get free preview")
  - "Get free preview"    → MATCH
  - "Get started free"    → NO MATCH (no contiguous "get free preview")
  - "Get my preview"      → NO MATCH (missing word "free")
  - "Get my free preview" → NO MATCH (words "my" interrupts; not a contiguous "get free preview")

- Search key: "$99"
  - "$99"   → MATCH
  - "99"    → NO MATCH (missing "$")
  - "$99/mo" → MATCH (contains "$99")

If the user does NOT use quotes and instead refers by location ("the hero button", "the founder section", "the top button"), use the page structure to pick the single most appropriate element.

If the user says "all CTAs", "every button", "across the page" — those are EXPLICIT broad scope, match every applicable element.

Never invent IDs. Never include ids whose text fails the substring check above.

OTHER RULES:
- Only emit ops for elements that actually need to change
- The site is marine-tourism marketing — preserve that context unless the user asks otherwise
- If a request is ambiguous, make the most sensible interpretation
- Never invent new IDs. Only use IDs that appear in the content map.`,
        messages: [{
          role: 'user',
          content: `Here is the current editable content:\n${JSON.stringify(content, null, 2)}\n\nChange requested: ${request}`
        }]
      })
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Claude API error:', response.status, err);
      return { statusCode: 502, body: 'Claude API error' };
    }

    const data = await response.json();
    let raw = data?.content?.[0]?.text?.trim() || '';
    raw = raw.replace(/^```json\n?/, '').replace(/^```\n?/, '').replace(/\n?```$/, '').trim();

    let result;
    try { result = JSON.parse(raw); }
    catch {
      console.error('Failed to parse Claude response as JSON:', raw);
      return { statusCode: 502, body: 'Invalid response format' };
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify(result)
    };

  } catch (err) {
    console.error('Function error:', err.message);
    return { statusCode: 500, body: `Internal error: ${err.message}` };
  }
};

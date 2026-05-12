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

  const MODEL = process.env.ANTHROPIC_MODEL || 'claude-haiku-4-5-20251001';

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
        system: `You are a website content editor for Boatr Marketing — a marine-tourism marketing service. The user will describe a change they want made to the boatrmarketing.com website.

You will receive a JSON object of all editable content on the page with element IDs as keys.

Respond with ONLY a valid JSON object in this exact format — no markdown, no explanation:
{
  "changes": [
    { "id": "element-id", "text": "new text value" }
  ],
  "confirmation": "One sentence confirming what you changed in plain English."
}

Rules:
- Only include elements that actually need to change
- Only change text content — never IDs, structure, or anything else
- If the request is unclear, make the most sensible interpretation
- Keep the same tone and voice as the existing content
- The site is about marine-tourism marketing — don't lose the marine context`,
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

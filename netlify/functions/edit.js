exports.handler = async function (event) {

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  const { request, content } = body;

  if (!request || !content) {
    return { statusCode: 400, body: 'Missing request or content' };
  }

  if (request.length > 500) {
    return { statusCode: 400, body: 'Request too long' };
  }

  const CLAUDE_API_KEY = process.env.CLAUDE_API_KEY;
  if (!CLAUDE_API_KEY) {
    return { statusCode: 500, body: 'API key not configured' };
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
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1000,
        system: `You are a website content editor. The user will describe a change they want made to their website.

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
- Keep the same tone and voice as the existing content`,
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

    // Strip markdown fences if present
    raw = raw.replace(/^```json\n?/, '').replace(/^```\n?/, '').replace(/\n?```$/, '').trim();

    let result;
    try {
      result = JSON.parse(raw);
    } catch {
      console.error('Failed to parse Claude response as JSON:', raw);
      return { statusCode: 502, body: 'Invalid response format' };
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(result)
    };

  } catch (err) {
    console.error('Function error:', err.message);
    return { statusCode: 500, body: `Internal error: ${err.message}` };
  }
};

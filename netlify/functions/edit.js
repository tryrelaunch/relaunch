exports.handler = async function (event) {

  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }

  // Parse body
  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  const { request, html } = body;

  if (!request || !html) {
    return { statusCode: 400, body: 'Missing request or html' };
  }

  // Basic abuse prevention — request can't be too long
  if (request.length > 500) {
    return { statusCode: 400, body: 'Request too long' };
  }

  // Strip scripts, styles, and the edit widget/SEO banner to reduce tokens
  let cleanedHTML = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<!-- EDIT WIDGET -->[\s\S]*$/i, '')
    .replace(/<!-- SEO BANNER -->[\s\S]*?(?=<!-- NAV -->)/i, '')
    .trim();

  const CLAUDE_API_KEY = process.env.CLAUDE_API_KEY;

  console.log('API key present:', !!CLAUDE_API_KEY);
  console.log('API key length:', CLAUDE_API_KEY ? CLAUDE_API_KEY.length : 0);

  if (!CLAUDE_API_KEY) {
    return { statusCode: 500, body: 'API key not configured' };
  }

  try {
    console.log('Calling Claude API...');
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 4000,
        system: `You are a website editor. Make ONLY the requested change to the HTML. 
Rules:
- Only change text, prices, hours, phone numbers, addresses, menu items
- Never change CSS, colors, fonts, layout, or structure
- Return the complete raw HTML with the change applied
- No markdown, no code fences, no explanation — raw HTML only`,
        messages: [{
          role: 'user',
          content: `Here is the current website HTML:\n\n${cleanedHTML}\n\n---\n\nPlease make this change: ${request}`
        }]
      })
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Claude API error status:', response.status);
      console.error('Claude API error body:', err);
      return { statusCode: 502, body: `Claude API error: ${response.status} - ${err}` };
    }

    const data = await response.json();
    const updatedHTML = data?.content?.[0]?.text
      ?.trim()
      ?.replace(/^```html\n?/, '')
      ?.replace(/^```\n?/, '')
      ?.replace(/\n?```$/, '');

    if (!updatedHTML) {
      return { statusCode: 502, body: 'No response from Claude' };
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ html: updatedHTML })
    };

  } catch (err) {
    console.error('Function error:', err.message);
    console.error('Stack:', err.stack);
    return { statusCode: 500, body: `Internal error: ${err.message}` };
  }
};

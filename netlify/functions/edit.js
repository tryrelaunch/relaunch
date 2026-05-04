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

  // Strip the edit widget and SEO banner from HTML before sending to Claude
  // This saves tokens on every request — Claude never needs to see or edit these
  let cleanedHTML = html
    .replace(/<!-- EDIT WIDGET -->[\s\S]*?<\/style>/m, '')
    .replace(/<!-- Edit FAB[\s\S]*?<\/div>\n/m, '')
    .replace(/<!-- Edit panel[\s\S]*?<\/div>\n/m, '')
    .replace(/<!-- SEO BANNER -->[\s\S]*?<\/div>\n\n/m, '');

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
        model: 'claude-sonnet-4-5',
        max_tokens: 8000,
        system: `You are a website editor. A local business owner is asking you to make a change to their website.

RULES — read carefully:
- You may ONLY change: text content, prices, hours, phone numbers, addresses, menu items, descriptions, promotional announcements
- You may NOT change: colors, fonts, CSS, layout, HTML structure, class names, the nav, the footer structure
- Return the COMPLETE updated HTML document — the full file, nothing omitted
- Make ONLY the specific change requested. Nothing else.
- Keep the exact same tone and voice as the existing content
- If the request is ambiguous, make the most sensible interpretation
- Do not add commentary, explanation, or markdown. Return raw HTML only.`,
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
    const updatedHTML = data?.content?.[0]?.text?.trim();

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

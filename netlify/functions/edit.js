import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({ apiKey: process.env.CLAUDE_API_KEY });
const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-4-5-20251001";

// In-memory rate limiter. Resets on cold start, which is fine —
// Netlify functions cold-start frequently enough that abusers
// can't accumulate state, and legitimate users won't hit limits.
const hits = new Map();
const WINDOW_MS = 60 * 1000;          // 1 minute window
const MAX_PER_WINDOW = 10;            // 10 edits per IP per minute
const MAX_PROMPT_LEN = 500;           // characters
const MAX_HTML_LEN = 50_000;          // characters

export default async (req) => {
  // CORS / method gate
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  // Identify caller by IP
  const ip =
    req.headers.get("x-nf-client-connection-ip") ||
    req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    "unknown";

  // Rate limit check
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
    return new Response(
      JSON.stringify({ error: "Too many edits. Try again in a minute." }),
      {
        status: 429,
        headers: {
          "Content-Type": "application/json",
          "Retry-After": String(retryAfter),
        },
      }
    );
  }

  // Parse + validate input
  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid JSON" }, 400);
  }

  const { prompt, html, context } = body || {};
  if (typeof prompt !== "string" || typeof html !== "string") {
    return json({ error: "Missing prompt or html" }, 400);
  }
  if (prompt.length > MAX_PROMPT_LEN) {
    return json({ error: "Prompt too long" }, 400);
  }
  if (html.length > MAX_HTML_LEN) {
    return json({ error: "HTML payload too large" }, 400);
  }

  // Cheap prompt-injection guard (not foolproof, just raises the bar)
  const lower = prompt.toLowerCase();
  if (
    lower.includes("ignore previous") ||
    lower.includes("system prompt") ||
    lower.includes("reveal instructions")
  ) {
    return json({ error: "Invalid prompt" }, 400);
  }

  // Call Claude
  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 4096,
      system:
        "You edit static HTML for small business websites. The user " +
        "will give you a snippet of HTML and a request. Return ONLY " +
        "the modified HTML — no commentary, no markdown fences, no " +
        "<script> tags. Preserve all attributes, classes, IDs, and " +
        "any <script type=\"application/ld+json\"> blocks. Match the " +
        "existing visual style.",
      messages: [
        {
          role: "user",
          content:
            `Current HTML:\n${html}\n\n` +
            (context ? `Page context:\n${context}\n\n` : "") +
            `Request: ${prompt}\n\nReturn the modified HTML.`,
        },
      ],
    });

    let newHtml = message.content?.[0]?.text?.trim() || "";

    // Strip any markdown fences Claude might add despite instructions
    newHtml = newHtml
      .replace(/^```(?:html)?\s*/i, "")
      .replace(/```\s*$/, "")
      .trim();

    // Strip any <script> tags from the response — defense in depth.
    // Schema (application/ld+json) is preserved by replacing only
    // executable script tags.
    newHtml = newHtml.replace(
      /<script(?![^>]*type=["']application\/ld\+json["'])[^>]*>[\s\S]*?<\/script>/gi,
      ""
    );

    if (!newHtml) {
      return json({ error: "Empty response from model" }, 502);
    }

    return json({ html: newHtml });
  } catch (err) {
    console.error("edit.js error:", err);
    return json({ error: "Edit failed. Try again." }, 502);
  }
};

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

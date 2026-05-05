import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({ apiKey: process.env.CLAUDE_API_KEY });
const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-4-5-20251001";

// In-memory rate limiter. Resets on cold start, fine at our scale.
const hits = new Map();
const WINDOW_MS = 60 * 1000;          // 1 minute window
const MAX_PER_WINDOW = 10;            // 10 edits per IP per minute
const MAX_REQUEST_LEN = 500;          // chars in user request
const MAX_CONTENT_LEN = 50_000;       // chars in stringified content

export default async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  // Rate limit by IP
  const ip =
    req.headers.get("x-nf-client-connection-ip") ||
    req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
    "unknown";

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

  // Parse + validate input matching the existing widget's contract
  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid JSON" }, 400);
  }

  const { request, content } = body || {};
  if (typeof request !== "string" || !content || typeof content !== "object" || Array.isArray(content)) {
    return json({ error: "Missing request or content" }, 400);
  }
  if (request.length > MAX_REQUEST_LEN) {
    return json({ error: "Request too long" }, 400);
  }

  const contentStr = JSON.stringify(content);
  if (contentStr.length > MAX_CONTENT_LEN) {
    return json({ error: "Content payload too large" }, 400);
  }

  // Cheap prompt-injection guard
  const lower = request.toLowerCase();
  if (
    lower.includes("ignore previous") ||
    lower.includes("system prompt") ||
    lower.includes("reveal instructions")
  ) {
    return json({ error: "Invalid request" }, 400);
  }

  try {
    const message = await client.messages.create({
      model: MODEL,
      max_tokens: 2048,
      system:
        "You edit copy on small business websites. The user provides a request and " +
        "a JSON object of editable text fields with their current values. Return " +
        "ONLY a JSON object containing the fields that should change, mapped to " +
        "their new values. Do not include fields that don't change. Do not add " +
        "new fields not present in the input. Match the tone, casing, length, and " +
        "style of existing copy. Return ONLY the JSON object — no commentary, no " +
        "markdown code fences, no explanation.",
      messages: [
        {
          role: "user",
          content:
            `Current content (JSON):\n${contentStr}\n\n` +
            `User request: ${request}\n\n` +
            `Return the JSON object of changed fields only.`,
        },
      ],
    });

    let raw = message.content?.[0]?.text?.trim() || "";

    // Strip markdown fences Claude sometimes adds despite instructions
    raw = raw
      .replace(/^```(?:json)?\s*/i, "")
      .replace(/```\s*$/, "")
      .trim();

    let changes;
    try {
      changes = JSON.parse(raw);
    } catch {
      console.error("Could not parse model response as JSON:", raw);
      return json({ error: "Invalid response from model" }, 502);
    }

    if (!changes || typeof changes !== "object" || Array.isArray(changes)) {
      return json({ error: "Invalid response shape" }, 502);
    }

    // Defense in depth: only accept changes for keys that existed in input,
    // and strip any HTML tags from the new values
    const safeChanges = {};
    for (const key of Object.keys(changes)) {
      if (Object.prototype.hasOwnProperty.call(content, key)) {
        const val = changes[key];
        if (typeof val === "string" && val.length < 5000) {
          safeChanges[key] = val.replace(/<[^>]*>/g, "");
        }
      }
    }

    // Return multiple shapes so whatever the frontend reads, it finds it
    return json({ content: safeChanges, updates: safeChanges, ...safeChanges });
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

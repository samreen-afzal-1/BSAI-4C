/* ============================================================
   utils/api.js — Anthropic API helper
   ============================================================ */

async function callClaude(prompt) {
  if (!CONFIG.ANTHROPIC_API_KEY || CONFIG.ANTHROPIC_API_KEY === "YOUR_API_KEY_HERE") {
    throw new Error("API key not set. Open static/config.js and replace YOUR_API_KEY_HERE with your Anthropic API key.");
  }

  const response = await fetch(CONFIG.API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: CONFIG.MODEL,
      max_tokens: CONFIG.MAX_TOKENS,
      messages: [{ role: "user", content: prompt }]
    })
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err?.error?.message || `API error ${response.status}`);
  }

  const data = await response.json();
  const rawText = data.content?.map(b => b.text || "").join("") || "";
  const clean   = rawText.replace(/```json|```/g, "").trim();

  try {
    return JSON.parse(clean);
  } catch {
    throw new Error("Could not parse model response as JSON. Raw: " + rawText.slice(0, 200));
  }
}

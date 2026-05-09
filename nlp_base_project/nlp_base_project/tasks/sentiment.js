/* ============================================================
   tasks/sentiment.js — Sentiment Analysis
   ============================================================ */

registerTask("sentiment", {
  label: "Sentiment Analysis",
  desc: "Classify the emotional tone of text as positive, negative, or neutral. Extracts confidence scores and key sentiment-driving phrases.",
  placeholder: "The product arrived quickly and works great! Very happy with my purchase.",
  extras: "",   // no extra controls needed

  buildPrompt(text) {
    return `You are an NLP sentiment analysis engine.
Analyze the text and respond ONLY with valid JSON — no markdown, no preamble.

Schema:
{
  "sentiment": "positive|negative|neutral",
  "confidence": 0.0-1.0,
  "scores": { "positive": 0.0, "negative": 0.0, "neutral": 0.0 },
  "key_phrases": ["phrase1", "phrase2"],
  "explanation": "one sentence"
}

Text: "${text}"`;
  },

  renderResult(data) {
    const icon = data.sentiment === "positive" ? "↑" : data.sentiment === "negative" ? "↓" : "→";
    const cls  = data.sentiment === "positive" ? "badge-teal" : data.sentiment === "negative" ? "badge-coral" : "badge-amber";
    let html = `<span class="badge ${cls}">${icon} ${data.sentiment} (${Math.round(data.confidence * 100)}%)</span><br><br>`;

    // Score cards
    html += `<div class="stats-row">`;
    ["positive","negative","neutral"].forEach(k => {
      const v = data.scores?.[k] ?? 0;
      html += `<div class="stat-card"><div class="stat-val">${Math.round(v*100)}%</div><div class="stat-lbl">${k}</div></div>`;
    });
    html += `</div>`;

    // Key phrases
    if (data.key_phrases?.length) {
      html += `<br><div style="font-size:12px;color:var(--text-muted);margin-bottom:4px;">Key phrases</div>`;
      data.key_phrases.forEach(p => html += `<span class="badge badge-blue">${p}</span>`);
    }

    if (data.explanation) {
      html += `<br><br><span style="font-size:12px;color:var(--text-muted);">${data.explanation}</span>`;
    }
    return html;
  }
});

/* ============================================================
   tasks/classification.js — Text Classification
   ============================================================ */

registerTask("classify", {
  label: "Text Classification",
  desc: "Assign categories to text from predefined labels. Useful for topic detection, spam filtering, and intent classification.",
  placeholder: "Scientists have discovered a new exoplanet orbiting a distant star that may have conditions suitable for liquid water.",

  extras: `
    <select id="clf-scheme">
      <option value="topic">Topic (science / tech / politics / sports / entertainment / health / business)</option>
      <option value="intent">Intent (question / statement / command / complaint / compliment)</option>
      <option value="spam">Spam detection</option>
    </select>
  `,

  buildPrompt(text) {
    const scheme = document.getElementById("clf-scheme")?.value || "topic";
    const instructions = {
      topic: "Classify into topics: science, technology, politics, sports, entertainment, health, business. Multiple labels are allowed.",
      intent: "Classify the intent as exactly one of: question, statement, command, complaint, compliment.",
      spam: "Classify as either spam or not_spam."
    };
    return `You are an NLP text classification engine.
${instructions[scheme]}
Respond ONLY with valid JSON — no markdown, no preamble.

Schema:
{
  "labels": [{ "label": "category", "confidence": 0.0-1.0 }],
  "top_label": "best matching label",
  "reasoning": "one sentence explaining the classification"
}

Text: "${text}"`;
  },

  renderResult(data) {
    let html = `<span class="badge badge-teal">&#10003; ${data.top_label}</span><br><br>`;

    if (data.labels?.length) {
      data.labels.forEach(l => {
        const pct = Math.round(l.confidence * 100);
        html += `<div class="prog-row">
          <div class="prog-label"><span>${l.label}</span><span style="color:var(--text-muted);">${pct}%</span></div>
          <div class="prog-track"><div class="prog-fill" style="width:${pct}%;"></div></div>
        </div>`;
      });
    }

    if (data.reasoning) {
      html += `<br><span style="font-size:12px;color:var(--text-muted);">${data.reasoning}</span>`;
    }
    return html;
  }
});

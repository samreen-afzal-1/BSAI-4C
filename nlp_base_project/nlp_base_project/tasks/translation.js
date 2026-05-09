/* ============================================================
   tasks/translation.js — Language Detection & Translation
   ============================================================ */

registerTask("translate", {
  label: "Translation",
  desc: "Detect the source language and translate text into your chosen target language. Also provides formality detection.",
  placeholder: "Hola mundo! ¿Cómo estás hoy?",

  extras: `
    <select id="tgt-lang">
      <option value="English">→ English</option>
      <option value="Spanish">→ Spanish</option>
      <option value="French">→ French</option>
      <option value="German">→ German</option>
      <option value="Arabic">→ Arabic</option>
      <option value="Chinese (Simplified)">→ Chinese (Simplified)</option>
      <option value="Japanese">→ Japanese</option>
      <option value="Urdu">→ Urdu</option>
      <option value="Turkish">→ Turkish</option>
      <option value="Portuguese">→ Portuguese</option>
    </select>
  `,

  buildPrompt(text) {
    const lang = document.getElementById("tgt-lang")?.value || "English";
    return `You are an NLP translation engine.
Detect the source language and translate the text to ${lang}.
Respond ONLY with valid JSON — no markdown, no preamble.

Schema:
{
  "source_language": "detected language name",
  "target_language": "${lang}",
  "translation": "the translated text",
  "confidence": 0.0-1.0,
  "formality": "formal|informal|neutral"
}

Text: "${text}"`;
  },

  renderResult(data) {
    let html = `<div style="font-size:12px;color:var(--text-muted);margin-bottom:6px;">
      ${data.source_language} &rarr; ${data.target_language}
    </div>`;
    html += `<div style="font-size:15px;line-height:1.8;margin-bottom:12px;">${data.translation}</div>`;
    html += `<span class="badge badge-teal">Confidence: ${Math.round((data.confidence ?? 0) * 100)}%</span> `;
    if (data.formality) html += `<span class="badge badge-purple">${data.formality}</span>`;
    return html;
  }
});

/* ============================================================
   tasks/ner.js — Named Entity Recognition
   ============================================================ */

registerTask("ner", {
  label: "Named Entity Recognition",
  desc: "Identify and classify named entities: persons, organizations, locations, dates, money, products, and more.",
  placeholder: "Apple Inc. CEO Tim Cook announced a $3 billion investment in Austin, Texas on Monday.",
  extras: "",

  buildPrompt(text) {
    return `You are an NLP named entity recognition (NER) engine.
Extract all named entities and respond ONLY with valid JSON — no markdown, no preamble.

Schema:
{
  "entities": [
    { "text": "entity text", "type": "PERSON|ORG|LOC|DATE|MONEY|PRODUCT|EVENT|OTHER", "description": "brief role or context" }
  ]
}

Text: "${text}"`;
  },

  renderResult(data) {
    if (!data.entities?.length) return "No named entities found in the text.";

    const typeColors = {
      PERSON: "badge-purple", ORG: "badge-blue", LOC: "badge-teal",
      DATE: "badge-amber", MONEY: "badge-coral", PRODUCT: "badge-teal",
      EVENT: "badge-purple", OTHER: "badge-gray"
    };

    let html = `<div style="margin-bottom:8px;font-size:12px;color:var(--text-muted);">${data.entities.length} entit${data.entities.length===1?"y":"ies"} found</div>`;
    data.entities.forEach(e => {
      const cls = typeColors[e.type] || "badge-gray";
      html += `<div style="margin-bottom:8px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">`;
      html += `<span class="badge ${cls}">${e.type}</span>`;
      html += `<strong style="font-size:14px;">${e.text}</strong>`;
      if (e.description) html += `<span style="font-size:12px;color:var(--text-muted);">${e.description}</span>`;
      html += `</div>`;
    });
    return html;
  }
});

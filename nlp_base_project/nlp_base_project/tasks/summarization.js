/* ============================================================
   tasks/summarization.js — Text Summarization
   ============================================================ */

registerTask("summary", {
  label: "Summarization",
  desc: "Condense long text into a concise summary. Choose abstractive (paraphrased) or extractive (original sentences) mode.",
  placeholder: "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data. The goal is a computer capable of understanding the contents of documents, including the contextual nuances of the language within them. The technology can then accurately extract information and insights contained in the documents, as well as categorize and organize the documents themselves.",

  extras: `
    <select id="sum-mode">
      <option value="abstractive">Abstractive (paraphrased)</option>
      <option value="extractive">Extractive (original sentences)</option>
    </select>
    <select id="sum-len">
      <option value="short">Short (1-2 sentences)</option>
      <option value="medium">Medium (3-4 sentences)</option>
      <option value="long">Long (5+ sentences)</option>
    </select>
  `,

  buildPrompt(text) {
    const mode = document.getElementById("sum-mode")?.value || "abstractive";
    const len  = document.getElementById("sum-len")?.value  || "short";
    return `You are an NLP summarization engine.
Summarize the text in ${mode} mode with ${len} length.
Respond ONLY with valid JSON — no markdown, no preamble.

Schema:
{
  "summary": "the summary text",
  "mode": "${mode}",
  "compression_ratio": 0.0-1.0,
  "keywords": ["kw1","kw2","kw3","kw4","kw5"]
}

Text: "${text}"`;
  },

  renderResult(data) {
    let html = `<div style="font-size:14px;line-height:1.8;margin-bottom:12px;">${data.summary}</div>`;

    if (data.compression_ratio != null) {
      const pct = Math.round((1 - data.compression_ratio) * 100);
      html += `<div class="stats-row">
        <div class="stat-card"><div class="stat-val">${pct}%</div><div class="stat-lbl">compressed</div></div>
        <div class="stat-card"><div class="stat-val">${data.mode || "abstractive"}</div><div class="stat-lbl">mode</div></div>
      </div>`;
    }

    if (data.keywords?.length) {
      html += `<br>`;
      data.keywords.forEach(k => html += `<span class="badge badge-purple">${k}</span>`);
    }
    return html;
  }
});

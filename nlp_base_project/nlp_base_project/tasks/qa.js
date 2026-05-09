/* ============================================================
   tasks/qa.js — Question Answering (Reading Comprehension)
   ============================================================ */

registerTask("qa", {
  label: "Question Answering",
  desc: "Extract answers to specific questions from a provided context passage. Mimics reading comprehension tasks.",
  placeholder: "The Eiffel Tower, located in Paris, France, was built between 1887 and 1889 by engineer Gustave Eiffel. It stands 330 meters tall and was originally intended as a temporary structure for the 1889 World Fair. Today it is visited by about 7 million people per year.",

  extras: `<input type="text" id="qa-question" placeholder="Your question about the text above..." />`,

  buildPrompt(text) {
    const question = document.getElementById("qa-question")?.value?.trim() || "What is the main topic?";
    return `You are an NLP question answering engine.
Answer the question based ONLY on the provided context. Do not use outside knowledge.
Respond ONLY with valid JSON — no markdown, no preamble.

Schema:
{
  "answer": "the extracted answer",
  "confidence": 0.0-1.0,
  "supporting_text": "exact quote from the context that supports the answer",
  "is_answerable": true|false
}

Context: "${text}"
Question: "${question}"`;
  },

  renderResult(data) {
    if (!data.is_answerable) {
      return `<span class="badge badge-coral">Not answerable</span><br><br>
        <span style="color:var(--text-muted);font-size:13px;">The context does not contain enough information to answer this question.</span>`;
    }

    let html = `<div style="font-size:15px;font-weight:700;margin-bottom:10px;">${data.answer}</div>`;
    html += `<span class="badge badge-blue">Confidence: ${Math.round((data.confidence ?? 0) * 100)}%</span>`;

    if (data.supporting_text) {
      html += `<div class="quote" style="margin-top:12px;">&ldquo;${data.supporting_text}&rdquo;</div>`;
    }
    return html;
  }
});

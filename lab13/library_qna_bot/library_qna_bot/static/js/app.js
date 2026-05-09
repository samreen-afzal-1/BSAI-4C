/* ── Athena Library QnA Bot — Frontend Logic ─────────────── */

const SUGGESTIONS = [
  "What are the library opening hours?",
  "How do I get a library card?",
  "Can I borrow e-books?",
  "How many books can I borrow?",
  "Is there free Wi-Fi?",
  "How do I renew my books?",
  "Book a study room",
  "What is the late fine?",
  "Interlibrary loan",
  "Can children get a library card?",
  "How do I pay fines?",
  "Is there a café?",
];

let queryHistory = [];

/* ── Boot ────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  buildChips();
  document.getElementById("q").addEventListener("keydown", e => {
    if (e.key === "Enter") ask();
  });
});

/* ── Chips ───────────────────────────────────────────────── */
function buildChips() {
  const wrap = document.getElementById("chips");
  SUGGESTIONS.forEach(s => {
    const btn = document.createElement("button");
    btn.className = "chip";
    btn.textContent = s;
    btn.onclick = () => { document.getElementById("q").value = s; ask(); };
    wrap.appendChild(btn);
  });
}

/* ── Ask ─────────────────────────────────────────────────── */
async function ask() {
  const input = document.getElementById("q");
  const query = input.value.trim();
  if (!query) { input.focus(); return; }

  setLoading(true);
  clearError();
  document.getElementById("results").innerHTML = "";
  document.getElementById("echo").style.display = "none";

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Server error ${res.status}`);
    }

    const data = await res.json();

    // echo
    document.getElementById("etext").textContent = `"${query}"`;
    document.getElementById("echo").style.display = "block";

    renderResults(data.results);
    addHistory(query);

  } catch (e) {
    showError("⚠ " + e.message + " — Make sure Flask is running on port 5050.");
  } finally {
    setLoading(false);
  }
}

/* ── Render results ──────────────────────────────────────── */
function renderResults(results) {
  const wrap = document.getElementById("results");

  if (!results || results.length === 0) {
    wrap.innerHTML = `<div class="nomatch">
      <div class="ico">🔎</div>
      No confident match found. Try rephrasing your question or
      contact the library at <strong>555-LIB-MAIN</strong>.
    </div>`;
    return;
  }

  results.forEach(r => {
    const bc  = r.confidence >= 70 ? "h" : r.confidence >= 35 ? "m" : "l";
    const bl  = r.confidence >= 70 ? "✓ High match" : r.confidence >= 35 ? "~ Good match" : "· Low match";
    const pct = Math.max(4, r.confidence);

    const card = document.createElement("div");
    card.className = "rcard";
    card.innerHTML = `
      <div class="rheader">
        <div class="rq">Q: ${esc(r.question)}</div>
        <div class="badge ${bc}">${bl}</div>
      </div>
      <div class="ra">${esc(r.answer)}</div>
      <div class="rsim">
        <span>${r.confidence}% confidence</span>
        <div class="sbar"><div class="sfill" style="width:${pct}%"></div></div>
        <span>similarity&nbsp;${r.similarity.toFixed(3)}</span>
      </div>`;
    wrap.appendChild(card);
  });
}

/* ── Query history ───────────────────────────────────────── */
function addHistory(query) {
  if (queryHistory.includes(query)) return;
  queryHistory.unshift(query);
  if (queryHistory.length > 8) queryHistory.pop();
  renderHistory();
}

function renderHistory() {
  const list = document.getElementById("history-list");
  if (!list) return;
  list.innerHTML = "";

  if (queryHistory.length === 0) {
    list.innerHTML = `<div class="hist-empty">No queries yet.</div>`;
    return;
  }

  queryHistory.forEach(q => {
    const item = document.createElement("div");
    item.className = "hist-item";
    item.innerHTML = `<span class="hi">↩</span> ${esc(q)}`;
    item.onclick = () => { document.getElementById("q").value = q; ask(); };
    list.appendChild(item);
  });
}

/* ── Helpers ─────────────────────────────────────────────── */
function setLoading(on) {
  document.getElementById("loader").classList.toggle("on", on);
}
function showError(msg) {
  const b = document.getElementById("err-banner");
  b.textContent = msg;
  b.classList.add("on");
}
function clearError() {
  document.getElementById("err-banner").classList.remove("on");
}
function esc(s) {
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

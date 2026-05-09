/* ============================================================
   utils/history.js — Session result history (in-memory)
   ============================================================ */

const sessionHistory = [];
const MAX_HISTORY = 8;

function addToHistory(taskKey, inputText, result) {
  sessionHistory.unshift({
    task: TASK_REGISTRY[taskKey].label,
    taskKey,
    text: inputText.slice(0, 70) + (inputText.length > 70 ? "…" : ""),
    fullText: inputText,
    result
  });
  if (sessionHistory.length > MAX_HISTORY) sessionHistory.pop();
  renderHistory();
}

function renderHistory() {
  const panel = document.getElementById("history-panel");
  const list  = document.getElementById("history-list");
  if (!sessionHistory.length) { panel.style.display = "none"; return; }

  panel.style.display = "block";
  list.innerHTML = sessionHistory.map((h, i) => `
    <div class="history-item" onclick="loadFromHistory(${i})">
      <div class="history-task">${h.task}</div>
      <div class="history-text">${h.text}</div>
    </div>
  `).join("");
}

function loadFromHistory(index) {
  const h = sessionHistory[index];
  if (!h) return;

  // Switch tab
  currentTask = h.taskKey;
  document.querySelectorAll(".tab").forEach(t => {
    t.classList.toggle("active", t.dataset.task === h.taskKey);
  });

  // Restore input & panel
  const cfg = TASK_REGISTRY[h.taskKey];
  document.getElementById("task-desc").textContent   = cfg.desc;
  document.getElementById("extras-area").innerHTML   = cfg.extras;
  document.getElementById("text-input").value        = h.fullText;

  // Show result
  const box = document.getElementById("result-box");
  box.style.display = "block";
  box.className     = "result-box";
  box.innerHTML     = cfg.renderResult(h.result);
}

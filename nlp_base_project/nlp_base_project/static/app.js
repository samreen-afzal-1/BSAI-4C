/* ============================================================
   static/app.js — Main application controller
   ============================================================ */

let currentTask = "sentiment";

/* Build tab buttons from registry */
function buildTabs() {
  const container = document.getElementById("task-tabs");
  Object.keys(TASK_REGISTRY).forEach(key => {
    const btn = document.createElement("button");
    btn.className = "tab" + (key === currentTask ? " active" : "");
    btn.textContent = TASK_REGISTRY[key].label;
    btn.dataset.task = key;
    btn.onclick = () => switchTask(key, btn);
    container.appendChild(btn);
  });
}

function switchTask(key, clickedBtn) {
  currentTask = key;
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  if (clickedBtn) clickedBtn.classList.add("active");

  const cfg = TASK_REGISTRY[key];
  document.getElementById("task-desc").textContent = cfg.desc;
  document.getElementById("text-input").placeholder = cfg.placeholder;
  document.getElementById("text-input").value = "";
  document.getElementById("extras-area").innerHTML = cfg.extras || "";
  document.getElementById("result-box").style.display = "none";
  document.getElementById("result-box").innerHTML = "";
}

async function runTask() {
  const text = document.getElementById("text-input").value.trim();
  if (!text) { alert("Please enter some text first."); return; }

  const cfg = TASK_REGISTRY[currentTask];
  const btn = document.getElementById("run-btn");
  const box = document.getElementById("result-box");

  btn.disabled     = true;
  btn.textContent  = "⟳ Running…";
  box.style.display = "block";
  box.className    = "result-box loading";
  box.textContent  = "Analyzing with Claude AI…";

  try {
    const prompt = cfg.buildPrompt(text);
    const result = await callClaude(prompt);

    box.className = "result-box";
    box.innerHTML = cfg.renderResult(result);

    addToHistory(currentTask, text, result);
  } catch (err) {
    box.className   = "result-box error";
    box.textContent = "Error: " + (err.message || "Something went wrong. Please try again.");
  }

  btn.disabled    = false;
  btn.textContent = "▶ Run";
}

/* Allow pressing Enter in the QA question field to run */
document.addEventListener("keydown", e => {
  if (e.key === "Enter" && e.target.id === "qa-question") runTask();
});

/* Init */
buildTabs();
switchTask("sentiment", document.querySelector(".tab"));

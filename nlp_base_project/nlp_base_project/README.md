# NLP Base Project

A multi-task Natural Language Processing playground powered by Claude AI.
Built with vanilla HTML, CSS, and JavaScript — no build tools required.

---

## Features

| Task | Description |
|------|-------------|
| **Sentiment Analysis** | Positive / negative / neutral classification with confidence scores |
| **Named Entity Recognition** | Extract PERSON, ORG, LOC, DATE, MONEY, PRODUCT entities |
| **Summarization** | Abstractive or extractive, short / medium / long |
| **Text Classification** | Topic, intent, or spam detection with progress bars |
| **Question Answering** | Reading comprehension — extract answers from a context passage |
| **Translation** | Auto-detect language → translate to 10 languages |

---

## Setup (2 steps)

### 1. Add your Anthropic API key

Open `static/config.js` and replace `YOUR_API_KEY_HERE` with your key:

```js
const CONFIG = {
  ANTHROPIC_API_KEY: "sk-ant-...",   // ← paste here
  ...
};
```

Get a key at → https://console.anthropic.com/

### 2. Run a local server

Because the app makes API calls from the browser, open it via a local server
(not by double-clicking the HTML file directly, which blocks fetch requests).

**Option A — Python (no install needed)**
```bash
cd nlp_base_project
python -m http.server 8080
# then open http://localhost:8080
```

**Option B — Node.js**
```bash
cd nlp_base_project
npx serve .
# then open the URL shown in the terminal
```

**Option C — VS Code**
Install the "Live Server" extension → right-click `index.html` → Open with Live Server.

---

## Project Structure

```
nlp_base_project/
├── index.html              # Main HTML shell
├── README.md               # This file
├── static/
│   ├── config.js           # API key + model config
│   ├── style.css           # All styles (light + dark mode)
│   └── app.js              # Tab routing, run logic
├── tasks/
│   ├── sentiment.js        # Sentiment Analysis task
│   ├── ner.js              # Named Entity Recognition task
│   ├── summarization.js    # Summarization task
│   ├── classification.js   # Text Classification task
│   ├── qa.js               # Question Answering task
│   └── translation.js      # Translation task
└── utils/
    ├── api.js              # callClaude() — Anthropic API helper
    └── history.js          # Session result history
```

---

## Adding a New Task

1. Create `tasks/mytask.js`
2. Call `registerTask("mytask", { ... })` with:
   - `label` — display name
   - `desc` — short description
   - `placeholder` — example input text
   - `extras` — optional HTML string for extra controls (selects, inputs)
   - `buildPrompt(text)` — returns the prompt string
   - `renderResult(data)` — returns an HTML string for the result panel
3. Add `<script src="tasks/mytask.js"></script>` in `index.html` (before `app.js`)

---

## Notes

- No backend required — all API calls go directly to Anthropic from the browser.
- Dark mode is automatic (follows OS preference).
- Session history stores the last 8 results in memory (cleared on page refresh).
- The model used is `claude-sonnet-4-20250514` — change it in `static/config.js`.

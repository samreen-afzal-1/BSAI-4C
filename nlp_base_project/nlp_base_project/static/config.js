/* ============================================================
   config.js — NLP Base Project configuration
   
   SETUP: Replace YOUR_API_KEY_HERE with your Anthropic API key.
   Get one at: https://console.anthropic.com/
   ============================================================ */

const CONFIG = {
  ANTHROPIC_API_KEY: "YOUR_API_KEY_HERE",   // <-- paste your key here
  MODEL: "claude-sonnet-4-20250514",
  MAX_TOKENS: 1000,
  API_URL: "https://api.anthropic.com/v1/messages"
};

// Task registry — tasks register themselves by calling registerTask()
const TASK_REGISTRY = {};

function registerTask(key, taskConfig) {
  TASK_REGISTRY[key] = taskConfig;
}

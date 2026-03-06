const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const agentSelect = document.getElementById("agent");

async function fetchAgents() {
  const res = await fetch("/api/agents");
  const data = await res.json();
  data.agents.forEach((agent) => {
    const option = document.createElement("option");
    option.value = agent;
    option.textContent = agent;
    agentSelect.appendChild(option);
  });
}

async function analyze({ runAll = false } = {}) {
  const prescription = document.getElementById("prescription").value.trim();

  if (!prescription) {
    statusEl.textContent = "Please paste a prescription before analyzing.";
    return;
  }

  const payload = {
    prescription_text: prescription,
    run_all: runAll,
  };

  if (!runAll) {
    payload.agent = agentSelect.value;
  }

  statusEl.textContent = "Analyzing…";
  resultsEl.textContent = "";

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const json = await res.json();
    if (!res.ok) {
      statusEl.textContent = json.detail || "Unexpected error";
      return;
    }

    resultsEl.textContent = JSON.stringify(json, null, 2);
    statusEl.textContent = "Done.";
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
  }
}

function init() {
  fetchAgents();
  document.getElementById("analyze").addEventListener("click", () => analyze());
  document.getElementById("all").addEventListener("click", () => analyze({ runAll: true }));
}

init();

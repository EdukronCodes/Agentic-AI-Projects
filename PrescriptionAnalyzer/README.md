# Prescription Analyzer (MCP Server)

A starter project that demonstrates a **Model Context Protocol (MCP) server** built with **FastAPI**, **LangChain**, and **Langraph**. It includes a set of agents (10+) to analyze prescription text and a helper script to download ~100 prescription samples from the web.

## 📦 Project Structure

- `mcp_server.py` - FastAPI MCP-style server exposing agent execution endpoints.
- `agents/` - Contains 10+ agents implemented using LangChain.
- `data/` - Stores downloaded prescription samples.
- `scripts/download_prescriptions.py` - Downloads ~100 prescription entries using OpenFDA.

## 🚀 Getting Started

1. Create a virtual environment and install dependencies:

```bash
cd PrescriptionAnalyzer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set your OpenAI API key (or any other LLM provider supported by LangChain):

```bash
export OPENAI_API_KEY="your_key_here"
```

3. Download prescription samples (optional but recommended):

```bash
python scripts/download_prescriptions.py --count 100
```

4. Run the MCP server:

```bash
python mcp_server.py
```

Then point your browser at `http://localhost:8000/docs` to see the OpenAPI UI.

## 📡 How it Works

- The server exposes endpoints to run agents by name.
- Each agent is a small LangChain-based class that performs a specific analysis task (e.g., summarization, dosage extraction, safety checks).
- The `langgraph` integration defines a simple graph flow between agents (e.g., analyze -> summarize -> classify).

## 🧩 Extending

- Add new agents under `agents/` by following the `BaseAgent` pattern.
- Extend the graph in `graph.py` to chain multiple agent outputs.

---

> Note: This is a starter scaffold. The data download script uses the OpenFDA API and can be extended to integrate with other prescription data sources.

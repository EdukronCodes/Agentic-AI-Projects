from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agents import AGENT_REGISTRY, get_agent
from .graph import run_full_analysis


class AnalyzeRequest(BaseModel):
    prescription_text: str
    agent: str | None = None
    run_all: bool = False


app = FastAPI(
    title="Prescription Analyzer MCP Server",
    description="Run LangChain+Langraph agents to analyze prescription text, including a simple UI for uploading prescriptions.",
)

# Allow local browser-based UI to access the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    """Serve the web UI."""
    return HTMLResponse(open("frontend/index.html", "r", encoding="utf-8").read())


@app.get("/api/agents")
def list_agents() -> dict:
    """List the available agents."""
    return {"agents": list(AGENT_REGISTRY.keys())}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest) -> dict:
    """Run analysis on a prescription.

    If `run_all` is True, runs all agents in a pipeline.
    Otherwise runs the selected agent.
    """

    if request.run_all:
        return run_full_analysis(request.prescription_text)

    if not request.agent:
        raise HTTPException(status_code=400, detail="`agent` must be provided if `run_all` is False.")

    agent_cls = get_agent(request.agent)
    if agent_cls is None:
        raise HTTPException(status_code=404, detail=f"Unknown agent '{request.agent}'.")

    agent = agent_cls()
    return {"analysis": {request.agent: agent.run(request.prescription_text)}}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mcp_server:app", host="0.0.0.0", port=8000, reload=True)

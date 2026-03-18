from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph.orchestrator import LangGraphOrchestrator
from app.utils.logger import get_logger

app = FastAPI(title="Multi-Agent Customer Support Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logger = get_logger()

orchestrator = LangGraphOrchestrator()


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    query: str
    agent: str
    answer: str
    confidence: float
    metadata: dict


class MatchRequest(BaseModel):
    query: str
    top_k: int = 4


class MatchResult(BaseModel):
    rank: int
    content: str
    metadata: dict


class MatchResponse(BaseModel):
    query: str
    matches: list[MatchResult]


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "message": "Service is running"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query is required")

    entry = orchestrator.run(request.query)
    result = entry.get("result", {})

    return ChatResponse(
        query=request.query,
        agent=result.get("agent", "unknown"),
        answer=result.get("answer", ""),
        confidence=result.get("confidence", 0.0),
        metadata={
            "router": entry.get("router"),
            "context": entry.get("context"),
            "pipeline_history_length": len(orchestrator.get_chat_history()),
            "reason": result.get("reason"),
        },
    )


@app.post("/match", response_model=MatchResponse)
def match_endpoint(request: MatchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query is required")

    matches = orchestrator.rag.retrieve_matches(request.query, k=request.top_k)

    return MatchResponse(query=request.query, matches=[MatchResult(**m) for m in matches])

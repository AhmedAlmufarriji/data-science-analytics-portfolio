"""FastAPI entry point: uvicorn aquasentinel.api:app --reload."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from aquasentinel.agent import InvestigationAgent
from aquasentinel.detection import LeakDetector, summarize_detection
from aquasentinel.evidence import search_evidence
from aquasentinel.forecast import forecast_demand
from aquasentinel.memory import SessionMemory
from aquasentinel.network import PIPE_BY_ID, topology
from aquasentinel.scenarios import repair_plan, simulate_closure
from aquasentinel.simulator import generate_telemetry, get_demo_frame, network_snapshot

APP_DIR = Path(__file__).resolve().parents[1]
app = FastAPI(title="AquaSentinel AI", version="1.0.0",
              description="Explainable synthetic water-network decision-support digital twin")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    session_id: str = Field(default="demo", pattern=r"^[a-zA-Z0-9_-]{1,64}$")


class ScenarioRequest(BaseModel):
    pipe_id: str
    repair_hours: float = Field(default=6.0, ge=0.5, le=168)


class PlanRequest(BaseModel):
    crews: int = Field(default=2, ge=1, le=20)


@lru_cache(maxsize=1)
def engine() -> tuple:
    # Fit on a separate normal dataset, not on anomalous demo telemetry.
    clean = generate_telemetry(hours=240, seed=19, leak=None)
    model = LeakDetector().fit(clean)
    frame = get_demo_frame()
    memory = SessionMemory(os.getenv("AQUASENTINEL_MEMORY_DB", ":memory:"))
    detection = lambda: summarize_detection(frame, model)
    return frame, detection, memory, InvestigationAgent(memory, detection, forecast_demand)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "aquasentinel-ai", "mode": "synthetic-demo",
            "external_ai_calls": False}


@app.get("/api/network")
def get_network() -> dict:
    return topology()


@app.get("/api/telemetry")
def telemetry(hour: int = Query(default=71, ge=0, le=71)) -> dict:
    frame, _, _, _ = engine()
    return {"hour": hour, "rows": network_snapshot(frame, hour), "synthetic": True}


@app.get("/api/analyze")
def analyze() -> dict:
    return engine()[1]()


@app.get("/api/forecast")
def forecast(horizon: int = Query(default=12, ge=1, le=72)) -> dict:
    return forecast_demand(horizon)


@app.post("/api/scenarios")
def scenario(payload: ScenarioRequest) -> dict:
    if payload.pipe_id not in PIPE_BY_ID:
        raise HTTPException(status_code=422, detail="Unknown pipe ID")
    return simulate_closure(payload.pipe_id, payload.repair_hours)


@app.post("/api/repair-plan")
def plan(payload: PlanRequest) -> dict:
    return repair_plan(engine()[1]()["candidates"], payload.crews)


@app.get("/api/evidence")
def evidence(q: str = Query(min_length=2, max_length=250)) -> dict:
    return {"query": q, "sources": search_evidence(q, 3)}


@app.post("/api/agent")
def chat(payload: ChatRequest) -> dict:
    try:
        return engine()[3].investigate(payload.message, payload.session_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str) -> dict:
    if not session_id.isascii() or not all(x.isalnum() or x in "_-" for x in session_id) or not 1 <= len(session_id) <= 64:
        raise HTTPException(status_code=422, detail="Invalid session")
    mem = engine()[2]
    return {"session_id": session_id, "preferred_district": mem.district(session_id),
            "recent_messages": mem.recent(session_id)}


@app.delete("/api/sessions/{session_id}")
def clear_session(session_id: str) -> dict:
    if not session_id.isascii() or not all(x.isalnum() or x in "_-" for x in session_id) or not 1 <= len(session_id) <= 64:
        raise HTTPException(status_code=422, detail="Invalid session")
    engine()[2].clear(session_id)
    return {"deleted": True, "session_id": session_id}


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(APP_DIR / "static" / "index.html")


app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")

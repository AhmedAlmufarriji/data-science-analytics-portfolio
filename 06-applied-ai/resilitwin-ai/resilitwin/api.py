"""FastAPI service and self-contained frontend."""
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .catalog import PRODUCTS, SUPPLIERS, INVENTORY
from .evidence import search
from .scenarios import Scenario, evaluate, engine, forecasts

WEB = Path(__file__).resolve().parent.parent / "web"
app = FastAPI(title="ResiliTwin AI", version="1.0.0", description="Synthetic supply-chain decision intelligence, no external AI API keys")

@app.get("/")
def dashboard():
    return FileResponse(WEB / "index.html")

@app.get("/assets/style.css")
def style():
    return FileResponse(WEB / "style.css", media_type="text/css")

@app.get("/assets/app.js")
def script():
    return FileResponse(WEB / "app.js", media_type="text/javascript")

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0", "data": "synthetic"}

@app.get("/api/overview")
def overview():
    return {
        "project": "ResiliTwin AI",
        "products": [{"sku": sku, "inventory": INVENTORY[sku], **v} for sku, v in PRODUCTS.items()],
        "suppliers": [vars(s) for s in SUPPLIERS],
        "history_rows": len(engine().history),
        "history_start": str(engine().history.date.min().date()),
        "history_end": str(engine().history.date.max().date()),
        "dataset_disclosure": "100% synthetic, deterministic simulated operations; not a production deployment.",
    }

@app.get("/api/forecasts")
def predictions(sku: str | None = None):
    if sku is not None and sku not in PRODUCTS:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Unknown SKU")
    return {"horizon_days": 21, "forecasts": [row for row in forecasts() if sku is None or row["sku"] == sku]}

@app.get("/api/model-card")
def model_card():
    return {"model": "HistGradientBoostingRegressor", "data_type": "synthetic", **engine().score,
            "safety_note": "Demonstration planning only. No live supplier connection, transactions, or autonomous purchasing."}

@app.get("/api/evidence")
def evidence(query: str = Query(min_length=1, max_length=250)):
    return {"query": query, "documents": search(query), "mode": "Extractive TF-IDF retrieval; no generative claims."}

@app.post("/api/scenarios")
def scenario_run(scenario: Scenario):
    return evaluate(scenario)

# Learn AquaSentinel AI — a practical beginner's walkthrough

This guide is intentionally simple. You do not need AWS or a paid AI API.

## The idea in one minute

Imagine a city with a water reservoir connected to different districts through pipes. Sensors measure pressure and water flow. If a pipe leaks, nearby sensors may report unusual values. AquaSentinel analyzes those signals, ranks possible pipe failures, and helps an engineer compare hypothetical repair decisions. Everything in this demo is fictional.

**Important:** This is a learning simulation, not a real hydraulic model or a system that controls water equipment.

## 1. Start the application

From the project folder:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS / Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
uvicorn aquasentinel.api:app --reload
```

Open http://127.0.0.1:8000. Your Swagger API explorer is http://127.0.0.1:8000/docs.

## 2. Understand the graph (`network.py`)

- A **node** means a reservoir or a district with a sensor.
- An **edge** means a pipe connecting two nodes.
- The demo has 9 nodes, including the reservoir, and 14 pipes.
- Each pipe has a fictional length, capacity and vulnerability attribute.

**Exercise:** Open the control-tower map. Click a pipe. The scenario form will select it automatically.

## 3. Understand sensor signals (`simulator.py`)

For each hour and each district, we create:

- Expected normal pressure and flow (baseline).
- Observed pressure and flow, with small random noise.
- An optional synthetic leak with pressure loss and excess flow.

**Residual = observed − expected.** A large negative pressure residual means pressure is lower than expected. A large positive flow residual means flow is higher than expected.

The demo inserts a fictional leak at pipe `P10` from hour 58 through hour 71. The model does **not** read the hidden event label to make its prediction.

**Exercise:** Compare API telemetry for `/api/telemetry?hour=30` and `/api/telemetry?hour=71`.

## 4. Understand anomaly detection (`detection.py`)

**Isolation Forest** is an unsupervised ML model. It learns the shape of normal residual data and then gives unusual readings larger anomaly scores. We train it using a separate normal-only synthetic dataset.

Why not use a basic rule like `pressure < 45`? Because pressure depends on each district and on the time of day. A residual accounts for our estimated normal conditions.

**Exercise:** Call `/api/analyze` and find `flagged_nodes`.

## 5. Understand finding a suspected pipe (`detection.py`)

A pressure drop near a leaking pipe is stronger than the drop far away. AquaSentinel takes each pipe as a possible leak origin and compares the **spatial pattern of observed residuals** with the pattern expected at different distances along the graph.

The best-fitting pipe gets a higher **relative evidence score**. These scores are not probabilities. They cannot prove where a real leak exists.

**Exercise:** Does P10 rank highest in this fictional demo? The known injected event is P10; the analysis should recover that hypothesis.

## 6. Understand demand forecasting (`forecast.py`)

We predict future demand with **Ridge regression**, a linear ML model with regularization. Instead of using an hour as an arbitrary number, the model uses sine and cosine features to represent daily cycles.

We train on the **first 13 days**, then calculate the prediction error on the **next 3 days**. This is called a **chronological holdout**: the future is never used to train the past.

MAE means **Mean Absolute Error**:

```
MAE = average of abs(actual demand - predicted demand)
```

Lower MAE is better, but the displayed MAE only measures fit to our fictional synthetic demand generator.

**Exercise:** Compare `/api/forecast?horizon=12` with `/api/forecast?horizon=24`.

## 7. Understand repair scenarios (`scenarios.py`)

When you simulate closing a pipe, the system removes the corresponding edge from the NetworkX graph. It checks which districts remain connected to the reservoir and how much longer the shortest alternate routes become.

This uses concepts from **graph theory** and **Dijkstra's shortest path algorithm**.

If removing a pipe still leaves an alternate path, the model can report zero disconnections. That does **not** guarantee real-world water pressure will remain adequate; graph connectivity is not hydraulic capacity.

**Exercise:** Simulate closing P10, then P01. Compare affected nodes and risk indices.

## 8. Understand the investigation agent (`agent.py`)

The agent is a **deterministic tool orchestrator**. That means it does not generate unverified text with an external LLM. Instead, it interprets a limited set of user requests and calls explicit Python functions:

1. Leak analyzer when a question mentions a leak or incident.
2. Forecaster when a question mentions demand or prediction.
3. Scenario engine when a question asks about closing a specific pipe.
4. Evidence retriever for supporting local reference text.
5. Session memory for user district preferences.

For example, **"Investigate the leak and forecast demand"** triggers two analysis tools and the reference retriever. Responses expose `tools_used`, `evidence`, and `actions_taken`.

**Exercise:** Send a POST request to `/api/agent` with this message, or use the dashboard Copilot.

## 9. Understand evidence, memory and safety

- `evidence.py`: TF-IDF retrieves relevant **project-authored** guidance cards. Sources have stable IDs such as `SAFETY-01`.
- `memory.py`: SQLite keeps per-session chat history and a preferred district. Delete a session via `DELETE /api/sessions/{session_id}`.
- `agent.py`: blocks a few sample requests to bypass safety controls, redacts common email and phone formats in stored questions, and never controls physical equipment.

These are learning protections, not enterprise-grade security or content safety guarantees.

## 10. Understand FastAPI and the website

`api.py` connects the system to HTTP. The browser loads `static/index.html`, `static/style.css`, and `static/app.js`. JavaScript calls the FastAPI endpoints to display numbers and render the graph and chart as SVG. No paid service or frontend build command is required.

**Exercise:** Open `/docs`, try `GET /api/health`, then `POST /api/scenarios`.

## 11. How to describe this on a CV or in an interview

> Designed a reproducible, synthetic-data water-network digital twin combining Isolation Forest anomaly detection, network-topology leak localization, chronological demand forecasting, what-if graph simulations, evidence-grounded tool orchestration, and an interactive FastAPI dashboard. Added API tests, Docker packaging, and GitHub Actions CI.

Always mention **synthetic data and educational prototype**. Do not present this as validated against a real municipal water network, a working AWS AgentCore implementation, or a deployed customer system.

## 12. Suggested technical upgrades

**Beginner:** Add a fourth district, more pipes, and new hypothetical incidents; write tests.

**Intermediate:** Evaluate detection recall, false-alarm rates, and top-k pipe localization over many unseen synthetic leak events.

**Advanced:** Replace the synthetic pressure proxy with EPANET/WNTR simulations, calibrate with independently validated data, then add multi-agent LLM orchestration and production authentication.

## Quick self-check

1. Why is a residual more useful than raw pressure?
2. Why do we use a separate normal-only dataset for Isolation Forest?
3. What is the difference between **anomaly detection** and **pipe localization**?
4. What goes wrong if you shuffle data randomly for a time-series forecast?
5. Why can a pipe closure have zero disconnected districts and still be unsafe in reality?
6. What does `actions_taken: []` communicate about the investigation agent?

If you can answer these six questions, you understand the main technical decisions in the project.
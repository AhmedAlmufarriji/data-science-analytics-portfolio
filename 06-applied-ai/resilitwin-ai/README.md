# ResiliTwin AI

### An explainable supply-chain resilience digital twin

**Demand forecasting · Counterfactual disruption testing · Risk-aware linear optimization · Monte Carlo reliability · Cited evidence search · Interactive dashboard**

ResiliTwin AI is an original, reproducible **AI/ML + operations research portfolio project**. It simulates a multi-product logistics network and lets planners compare a lowest-purchase-price sourcing strategy against an alternative that considers delivery delays, inventory shortages, carbon emissions and supplier capacity. It presents the trade-offs rather than pretending there is always a single best solution.

> **Transparency:** All data, supplier names, risk rates and emissions are **synthetic**. This project is an educational prototype — not deployed at any company, a live AWS agent, a genuine supply-chain integration, or a validated forecast of real-world outcomes. It does not place orders.

## Why it is different

Many ML portfolio examples end after a prediction. ResiliTwin turns predictions into constrained decisions, then stress-tests those decisions under the *same* randomly generated disruptions. The full chain is inspectable:

**Historical simulation → leakage-aware ML forecast → feasible purchase allocation → stochastic reliability estimate → traceable recommendation.**

The evidence pane is deliberately retrieval-only: it provides **citations from six included synthetic operations documents** instead of generating unsupported policy statements.

## Interactive dashboard

Open `http://localhost:8000` after starting the server. The application contains:

| Area | What it does |
|---|---|
| Overview | Product and supplier network KPIs, measured holdout error |
| Forecast lab | 21-day recursive demand forecasts, illustrative error bands, product selector |
| Resilience lab | Supplier outages, demand shocks, carbon price, risk attitude, budget sliders |
| Decision comparison | Baseline vs risk-aware predicted service, cost, emissions and reliability |
| Supplier allocation | SKU-wise optimizer results and lead times |
| Evidence library | Explainable TF-IDF document search with source citations |
| API docs | OpenAPI documentation exposed at `/docs` |

## Quick start

Requires **Python 3.11+**. The first request trains a small CPU-only ML model locally. No AWS account, paid service, API key, or user data is required.

```bash
git clone https://github.com/AhmedAlmufarriji/data-science-analytics-portfolio.git
cd data-science-analytics-portfolio/06-applied-ai/resilitwin-ai
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e '.[test]'
uvicorn resilitwin.api:app --reload
```

Open <http://127.0.0.1:8000>. For the API schema, open <http://127.0.0.1:8000/docs>.

**Colab:** The CLI and evaluation work in Colab with `pip install -e '.[test]'` after uploading or cloning the project; the local web dashboard is designed for desktop/server use.

### Reproduce the experiment

```bash
resilitwin generate   # artifacts/synthetic_demand.csv
resilitwin train      # artifacts/model_card.json
resilitwin scenario --outage ATLAS  # artifacts/scenario.json
pytest -q
```

### Docker

```bash
docker build -t resilitwin-ai .
docker run --rm -p 8000:8000 resilitwin-ai
```

## Example scenario via API

```bash
curl -X POST http://localhost:8000/api/scenarios \
  -H 'Content-Type: application/json' \
  -d '{"outages":["ATLAS"],"disruption_days":12,"demand_shock_pct":15,"carbon_price_per_ton":120,"risk_aversion":1.5,"budget":260000,"service_target":0.9,"trials":250}'
```

The response contains full baseline and optimized allocations, objective feasibility, a Monte Carlo stress comparison, estimated emissions and human-readable planning flags.

## ML, algorithms and evaluation

| Component | Design |
|---|---|
| Synthetic data | 490 daily observations × 6 SKUs; reproducible seed, seasonality, promotional effects and shocks |
| Forecasting | `HistGradientBoostingRegressor`, lagged demand, shifted moving averages, calendar features |
| Validation | Chronological 70-day holdout; seasonal-naive benchmark; MAE and WAPE |
| Deployment forecast | 21-day recursive predictions; heuristic widening of **uncalibrated** residual bands |
| Optimization | SciPy HiGHS linear programming with supplier eligibility, capacity, lead-time, cash, shortage and carbon trade-offs |
| Reliability | Monte Carlo sampled supplier delay events + demand uncertainty; baseline and optimized plan compared with common random numbers |
| Evidence | TF-IDF cosine similarity over version-controlled Markdown playbooks; filenames and source IDs returned |
| Serving | FastAPI + responsive framework-free HTML/CSS/JavaScript dashboard |
| Quality | Domain tests, HTTP integration tests, GitHub Actions CI and Dockerfile |

### Results

**Do not copy sample numbers from other projects.** Run `resilitwin train` to reproduce this project's actual holdout MAE/WAPE; these are based entirely on synthetic data. Optimization trade-offs depend on each scenario. A lower price is not guaranteed to improve reliability and optimizing carbon may increase procurement cost.

## Structure

```text
resilitwin-ai/
├── resilitwin/
│   ├── api.py               # HTTP API and dashboard serving
│   ├── catalog.py           # synthetic product/supplier reference data
│   ├── simulation.py        # repeatable time-series generator
│   ├── forecasting.py       # features, holdout, recursive inference
│   ├── optimizer.py         # constrained LP with infeasibility disclosure
│   ├── scenarios.py         # counterfactual comparisons and Monte Carlo
│   ├── evidence.py          # cited document retrieval
│   └── cli.py               # command line experiment runner
├── web/                     # interactive responsive dashboard
├── knowledge/               # six synthetic policy documents
├── tests/                   # unit, property and API checks
├── docs/ARCHITECTURE.md     # methodology, constraints and limitations
├── .github/workflows/ci.yml # standalone CI workflow template
├── Dockerfile
└── pyproject.toml
```

## Security, explainability and limitations

This project avoids paid APIs, unlicensed datasets, credentials and real client information. It uses no autonomous purchase actions. See [the technical architecture and model-risk notes](docs/ARCHITECTURE.md) for explicit assumptions, evaluation caveats, LP mathematics, possible failure modes and a future *proposed* AWS architecture.

## Author

**Ahmed Almufarriji** · Data Science / AI & Machine Learning portfolio · [GitHub](https://github.com/AhmedAlmufarriji)

Licensed under MIT for educational use.

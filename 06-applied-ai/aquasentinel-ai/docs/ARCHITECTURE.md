# AquaSentinel — Architecture and API contract

## Pipeline

1. `network.py`: directed-looking but undirected educational water-distribution graph with known edge lengths and static customer attributes.
2. `simulator.py`: seeded baseline diurnal demand. Synthetic pipe incidents lower pressure and increase flow with network-distance decay. It **does not solve physical hydraulic equations**.
3. `detection.py`: IsolationForest trained only on normal readings from a separate random seed. Candidate pipe scores compare observed residual maps to expected exponential propagation templates. Weighted least-squares amplitude minimizes fit error.
4. `forecast.py`: Ridge on hourly cyclical features and node customer counts; train first 13 days, hold out last 3 days. No test contamination.
5. `scenarios.py`: remove a candidate edge, compare shortest source-to-node paths and source-reachability. Explicitly does not evaluate flow capacity/pressure or operational feasibility.
6. `agent.py`: bounded natural-language routing to deterministic detection/forecast/scenario tools, plus TF-IDF evidence cards, and opt-in per-session district preference.
7. `api.py`: JSON endpoints and single-page visualization; FastAPI OpenAPI contracts at `/docs`.

## Endpoints

| Method | Path | Response |
|---|---|---|
| GET | `/api/health` | Status and simulation mode |
| GET | `/api/network` | Node+pipe graph |
| GET | `/api/telemetry?hour=71` | Node sensor snapshot, no hidden labels |
| GET | `/api/analyze` | Anomaly node IDs and pipe hypotheses |
| GET | `/api/forecast?horizon=12` | Next 1–72 hour aggregate forecast and temporal holdout MAE |
| POST | `/api/scenarios` | Pipe closure reachability and proxy risk |
| POST | `/api/repair-plan` | Explainable ranking and proposed assignments |
| GET | `/api/evidence?q=...` | Source-ID retrieval |
| POST | `/api/agent` | Agent answer, tools used, evidence, actions taken |
| GET / DELETE | `/api/sessions/{session_id}` | Inspect or delete local demo memory |

## Trust boundaries

- APIs intended only for local demonstration; no authentication and no multi-tenant isolation beyond session IDs.
- No live control plane, SCADA integration, physical coordinates, or third-party AI service.
- Prompt input bounded to 500 characters; persistent memory redacts common email/phone patterns, is opt-out deletable, and should not be treated as enterprise-compliant privacy protection.
- Safe plan evaluation always requires a human field operator.

## Extension points

- Replace synthetic flow simulator with validated EPANET model and real sensor calibration.
- Calibrate leak ranking scores on independently labeled fault events; add top-k localization accuracy, error bars and false-alarm-rate tests.
- Add model registry, data validation, observability and drift monitoring.
- Introduce deterministic authorization and audited real tool permission scopes before any integrations.

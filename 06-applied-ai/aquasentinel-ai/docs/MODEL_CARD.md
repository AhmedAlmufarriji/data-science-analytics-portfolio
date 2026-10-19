# Model card and evaluation limitations

## Intended use

AquaSentinel demonstrates software engineering techniques for infrastructure monitoring using **entirely fictional** graph and telemetry data. It is not for drinking-water safety, public-health advisories, emergency dispatch, or unsupervised control.

## Leakage-aware validation

- **Anomaly detection:** normal-training dataset uses `seed=19`, no incidents; evaluation dataset uses `seed=27`, includes an event. Label fields `is_leak`, `leak_pipe` exist only in generation/tests and are never passed to the model.
- **Forecast:** training covers the first 312 hourly periods; test covers subsequent 72 periods. No randomized train/test split on time series. Metric is held-out mean absolute error per node.
- **Leak localization:** graph-distance signature score is a weighted fit heuristic (pressure deficit plus positive flow deviation). It is **not** a probability or empirically calibrated confidence.
- **Crew ranking:** priority scores use hand-tuned weights for severity, customers, critical facilities and evidence. No claimed optimization guarantee.

## Known weaknesses

1. Residual baselines and incidents come from the same synthetic assumptions, making inference unrealistically easy. Real sensor drift, weather effects, faulty meters, and pressure zones are missing.
2. Global IsolationForest on residuals can miss weak localized incidents and may flag false positives.
3. The graph is undirected and ignores headloss, pipe diameter, pump curves, storage tanks, pressure control, and flow constraints.
4. Forecasting uses hand-crafted daily patterns without holidays, weather, seasonal trends, or real usage labels; outcomes are not field-valid.
5. Document retrieval is offline TF-IDF; source titles are educational cards written for this project, not external regulatory or peer-reviewed citations.
6. Agent guardrail rules are narrowly illustrative; they are not a robust policy enforcement engine.

## Responsible development checklist

- Verify leak location using site instrumentation before dispatch.
- Evaluate false-positive/false-negative rates on independently collected and reviewed fault events.
- Test performance across districts, network sizes and demand regimes.
- Request competent water-infrastructure and safety review before any live data connection.
- Add access controls, secrets management, encryption, audit trails, model versioning, monitoring and rollback for hosted deployments.

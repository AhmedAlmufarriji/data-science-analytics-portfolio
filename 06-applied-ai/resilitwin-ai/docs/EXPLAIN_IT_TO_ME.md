# Learn ResiliTwin AI from beginner to interview-ready

## 1. The problem

Imagine a logistics company selling six product types. Tomorrow, one supplier might be late. Should we buy from the cheapest supplier, or pay more for reliable deliveries? In practice, we must estimate future demand, respect stock levels, supplier capacities, delivery times, the cash budget and carbon goals.

**ResiliTwin AI connects all these decisions in one system.** It is an educational simulation, not a real company deployment.

## 2. The data

`simulation.py` creates 490 days of synthetic demand for each of six products, a total of 2,940 rows. Each row has a date, product ID, demand and promotion flag. Patterns include weekday demand, yearly seasonality, promotions, trend, random noise and occasional supply shocks. The random seed makes the experiment reproducible.

Try: `resilitwin generate` to export `artifacts/synthetic_demand.csv`.

## 3. Machine learning

In `forecasting.py`, the features include:

- `lag_1`: demand recorded one day earlier
- `lag_7`: demand recorded one week earlier
- `rolling_7`: average recorded in the seven days *before* the prediction date
- `promo`: whether a promotion is scheduled
- `dow`: day of week

The model is `HistGradientBoostingRegressor`, a tree-ensemble regression algorithm. We compare its forecasts with a baseline that simply repeats demand from seven days earlier. We evaluate on the last 70 days, not on the data used for model fitting.

**Reproducible result:** Holdout MAE is 4.76 units against 6.70 for the seasonal naive baseline. WAPE is 16.5% against 23.22%. These numbers are only from synthetic data.

After that, the trained model predicts 21 future days. It cannot use actual future demand, so it feeds yesterday's *predicted* demand back into the next prediction. This is recursive forecasting, and errors can accumulate.

## 4. Operations research optimization

The machine learning model answers: **How much might customers need?** The optimizer answers: **From which supplier should we buy each product?**

`optimizer.py` defines an LP (linear program) using SciPy HiGHS. It chooses quantities for eligible supplier-product pairs and penalizes uncovered demand. Constraints enforce a fixed budget, approved suppliers and their capacity. A weighted objective trades off procurement price, carbon factors and synthetic supplier-delay risk. If the service target is infeasible, the code reports that fact and the remaining shortages.

Why linear programming? It finds the cost-minimizing solution under explicit mathematical constraints, unlike ad hoc if-else rules.

## 5. Monte Carlo risk

A good-looking plan is not necessarily reliable. `scenarios.py` runs many random possible futures (Monte Carlo trials). Every trial samples supplier delays and unexpected demand variation. The result includes expected service and the chance of meeting a service target. Both plans use the same random events for fair comparison.

**Important:** The probabilities are synthetic assumptions and are not calibrated from real supplier history.

## 6. Evidence retrieval

`knowledge/` contains six synthetic operations playbooks. `evidence.py` converts them to TF-IDF vectors and ranks them using cosine similarity. It returns document titles, snippets and source identifiers. **This is retrieval, not a deployed generative LLM or a full RAG system.** No hallucinated text is generated.

## 7. API and frontend

`api.py` is the FastAPI backend. Its routes provide products, supplier metadata, demand forecasts, a model card, scenario optimization and evidence search. Open `/docs` for Swagger UI. The `web/` directory implements a responsive HTML/CSS/JS cockpit which calls those routes using `fetch`.

## 8. Interview explanation (45 seconds)

> I built ResiliTwin AI, an end-to-end decision intelligence prototype for supply-chain resilience. I generated reproducible synthetic logistics demand, engineered leakage-safe time-series features and trained a gradient-boosting model using a chronological holdout. I then converted demand forecasts into risk-aware procurement allocations using linear programming, subject to budget, supplier-capacity and delivery constraints. Finally, I compared plans through Monte Carlo supplier-disruption stress testing and exposed results in a FastAPI dashboard with cited policy retrieval. The code is tested and documented, and I clearly distinguish synthetic demonstration metrics from production validation.

## 9. Questions an interviewer might ask

**Why not deep learning?** The simulated data is relatively small and structured; gradient-boosted trees provide a strong, transparent tabular baseline.

**How did you avoid leakage?** Rolling statistics and lags shift by at least one day; holdout dates occur after training dates.

**How is optimization different from ML?** ML predicts quantities. LP chooses actions under constraints.

**Why Monte Carlo?** A single forecast misses a distribution of potential delivery and demand outcomes.

**What are the biggest limitations?** Synthetic input data, uncalibrated uncertainty, continuous rather than integer purchase quantities, and no operational integrations or production authentication.

**How would you productionize it?** Secure ingestion and APIs, proper observed data and versioning, calibrated uncertainty, supplier risk estimation, integer ordering, approval workflows, monitoring and cloud CI/CD.

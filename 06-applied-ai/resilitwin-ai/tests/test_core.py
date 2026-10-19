from datetime import timedelta
import numpy as np
import pandas as pd
import pytest
from resilitwin.catalog import PRODUCTS, SUPPLIERS
from resilitwin.simulation import generate_history
from resilitwin.forecasting import make_features, ForecastEngine
from resilitwin.optimizer import plan_procurement
from resilitwin.scenarios import Scenario, evaluate
from resilitwin.evidence import search


def test_history_reproducible():
    a = generate_history(days=140)
    b = generate_history(days=140)
    pd.testing.assert_frame_equal(a, b)
    assert (a.demand >= 1).all()
    assert a.sku.nunique() == len(PRODUCTS)


def test_no_future_leakage_in_features():
    h = generate_history(days=140)
    f1 = make_features(h)
    changed = h.copy()
    changed.loc[changed.date == changed.date.max(), "demand"] = 999999
    f2 = make_features(changed)
    pd.testing.assert_frame_equal(f1.drop(columns=["demand"]), f2.drop(columns=["demand"]))  # latest target never used as its own feature
    assert f1.groupby("sku").size().nunique() == 1


def test_holdout_and_future_forecast():
    model = ForecastEngine.fit(generate_history(days=170), holdout_days=35)
    assert model.score["mae_model"] >= 0
    assert model.score["n_validation_rows"] == 35 * len(PRODUCTS)
    pred = model.predict_future(horizon=5)
    assert len(pred) == 5 * len(PRODUCTS)
    assert all(0 <= row["low"] <= row["mean"] <= row["high"] for row in pred)


def test_procurement_constraints_budget_and_supplier_eligibility():
    demands = {sku: 420 for sku in PRODUCTS}
    result = plan_procurement(demands, budget=52000, service_target=.98)
    assert result["purchase_cost"] <= 52000 + 1e-5
    assert not result["service_target_feasible"]
    from resilitwin.catalog import ELIGIBILITY
    assert all(x["supplier"] in ELIGIBILITY[x["sku"]] for x in result["allocations"])
    assert sum(x["units"] for x in result["allocations"]) > 0


def test_full_outage_zero_allocations():
    demands = {sku: 380 for sku in PRODUCTS}
    result = plan_procurement(demands, outages=["ATLAS"], disruption_days=21, budget=300000)
    assert all(x["supplier"] != "ATLAS" for x in result["allocations"])


def test_unknown_supplier_rejected():
    with pytest.raises(ValueError):
        plan_procurement({sku: 300 for sku in PRODUCTS}, outages=["MISSING"])


def test_scenario_deterministic_and_reports_risk():
    setting = Scenario(outages=["ATLAS"], disruption_days=21, trials=50)
    first = evaluate(setting)
    second = evaluate(setting)
    assert first == second
    assert first["optimized"]["stress_test"]["simulations"] == 50
    assert first["optimized"]["purchase_cost"] <= setting.budget + 1e-5
    assert 0 <= first["optimized"]["stress_test"]["expected_service_rate"] <= 1


def test_evidence_has_grounded_document_path():
    results = search("supplier outage alternative capacity")
    assert results and "supplier" in results[0]["title"].lower()
    assert all(r["source_path"].startswith("knowledge/") for r in results)
    assert search("  ") == []

"""Explainable scenario engine combining ML, optimization and Monte Carlo."""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
import numpy as np
from pydantic import BaseModel, Field, field_validator
from .catalog import PRODUCTS, SUPPLIERS, INVENTORY
from .simulation import generate_history
from .forecasting import ForecastEngine
from .optimizer import plan_procurement

class Scenario(BaseModel):
    outages: list[str] = Field(default_factory=list, max_length=4)
    disruption_days: int = Field(default=12, ge=0, le=21)
    demand_shock_pct: int = Field(default=0, ge=-30, le=80)
    carbon_price_per_ton: float = Field(default=120, ge=0, le=1000)
    risk_aversion: float = Field(default=1.5, ge=0, le=5)
    budget: float = Field(default=260000, ge=0, le=1000000)
    service_target: float = Field(default=0.90, ge=0.50, le=1.0)
    trials: int = Field(default=250, ge=50, le=2000)

    @field_validator("outages")
    @classmethod
    def known_suppliers(cls, values: list[str]) -> list[str]:
        allowed = {s.code for s in SUPPLIERS}
        unknown = set(values) - allowed
        if unknown:
            raise ValueError(f"Unknown suppliers: {sorted(unknown)}")
        if len(set(values)) != len(values):
            raise ValueError("Duplicate suppliers are not allowed")
        return values

@lru_cache(maxsize=1)
def engine() -> ForecastEngine:
    return ForecastEngine.fit(generate_history())

@lru_cache(maxsize=1)
def forecasts() -> list[dict]:
    return engine().predict_future(21)

def demand_by_sku(shock_pct: int = 0) -> dict[str, float]:
    return {sku: sum(row["mean"] for row in forecasts() if row["sku"] == sku) * (1 + shock_pct / 100)
            for sku in PRODUCTS}


def simulate(plan: dict, demands: dict[str, float], scenario: Scenario) -> dict:
    """Stable CRN stream across plans for fair comparative scenario evaluation.

    Each draw samples supplier-level non-delivery events and SKU-level demand noise.
    This is an illustrative stress simulation, not calibrated business uncertainty.
    """
    seed_data = scenario.model_dump(exclude={"risk_aversion", "carbon_price_per_ton"})
    seed = int.from_bytes(hashlib.sha256(json.dumps(seed_data, sort_keys=True).encode()).digest()[:8], "little")
    rng = np.random.default_rng(seed)
    deliveries = {sku: {s.code: 0.0 for s in SUPPLIERS} for sku in PRODUCTS}
    for row in plan["allocations"]:
        deliveries[row["sku"]][row["supplier"]] += row["units"]
    service, shortages = [], []
    for _ in range(scenario.trials):
        supplier_ok = {}
        for s in SUPPLIERS:
            outage_extra = scenario.disruption_days / 21 if s.code in scenario.outages else 0.0
            probability = min(0.97, s.delay_probability + outage_extra * 0.5)
            supplier_ok[s.code] = rng.random() >= probability
        delivered = sum(INVENTORY.values())
        for sku in PRODUCTS:
            for supplier_code, units in deliveries[sku].items():
                if supplier_ok[supplier_code]:
                    delivered += units
        sampled_demand = sum(max(0, rng.normal(v, v * 0.11)) for v in demands.values())
        shortfall = max(0.0, sampled_demand - delivered)
        service.append(max(0.0, 1 - shortfall / max(sampled_demand, 1)))
        shortages.append(shortfall)
    values = np.array(service)
    return {
        "expected_service_rate": round(float(np.mean(values)), 4),
        "p10_service_rate": round(float(np.quantile(values, 0.10)), 4),
        "probability_meeting_target": round(float(np.mean(values >= scenario.service_target)), 4),
        "expected_shortage_units": round(float(np.mean(shortages)), 1),
        "p95_shortage_units": round(float(np.quantile(shortages, 0.95)), 1),
        "simulations": scenario.trials,
        "limitation": "Illustrative independent demand noise and correlated supplier delay events; not empirical probability forecasts.",
    }


def evaluate(scenario: Scenario) -> dict:
    demands = demand_by_sku(scenario.demand_shock_pct)
    common = dict(demand=demands, outages=scenario.outages,
                  disruption_days=scenario.disruption_days, budget=scenario.budget,
                  service_target=scenario.service_target)
    baseline = plan_procurement(**common, risk_aversion=0, carbon_price_per_ton=0)
    optimized = plan_procurement(**common, risk_aversion=scenario.risk_aversion,
                                 carbon_price_per_ton=scenario.carbon_price_per_ton)
    old_risk = simulate(baseline, demands, scenario)
    new_risk = simulate(optimized, demands, scenario)
    tips = []
    if scenario.outages:
        tips.append(f"Outage scenario removes effective capacity from {', '.join(scenario.outages)}. Reassess qualified backup suppliers.")
    if not optimized["service_target_feasible"]:
        tips.append("The requested service target is infeasible with this budget and available capacity; unmet demand is reported explicitly.")
    if new_risk["probability_meeting_target"] < 0.75:
        tips.append("Service-target reliability remains low in this stylized simulation. Consider increasing inventory, supplier resilience, or budget.")
    if optimized["emissions_kg"] < baseline["emissions_kg"]:
        tips.append("Risk-aware procurement also reduces projected freight emissions in this scenario.")
    return {
        "scenario": scenario.model_dump(),
        "forecast_demand_units": {k: round(v, 1) for k, v in demands.items()},
        "baseline": {**baseline, "stress_test": old_risk},
        "optimized": {**optimized, "stress_test": new_risk},
        "differences": {
            "purchase_cost": round(optimized["purchase_cost"] - baseline["purchase_cost"], 2),
            "emissions_kg": round(optimized["emissions_kg"] - baseline["emissions_kg"], 1),
            "expected_service_percentage_points": round(100 * (new_risk["expected_service_rate"] - old_risk["expected_service_rate"]), 2),
        },
        "decision_notes": tips,
    }

"""Risk- and carbon-aware procurement allocation with explicit LP constraints."""
from __future__ import annotations

from dataclasses import asdict
import numpy as np
from scipy.optimize import linprog
from .catalog import ELIGIBILITY, INVENTORY, PRODUCTS, SUPPLIERS

SUPPLIER_BY_ID = {s.code: s for s in SUPPLIERS}
SKUS = list(PRODUCTS)


def plan_procurement(demand: dict[str, float], outages: list[str] | None = None,
                     disruption_days: int = 0, carbon_price_per_ton: float = 90.0,
                     risk_aversion: float = 1.0, budget: float = 170000.0,
                     service_target: float = 0.97, horizon: int = 21) -> dict:
    """LP with continuous units; unmet demand penalized and service goal a soft target.

    Effective capacity is reduced for outages and lead times. Missing units use a
    high penalty and are reported explicitly instead of disguising infeasibility.
    """
    outages = outages or []
    bad = set(outages) - set(SUPPLIER_BY_ID)
    if bad:
        raise ValueError(f"Unknown suppliers: {sorted(bad)}")
    if not 0 <= service_target <= 1 or not 0 <= risk_aversion <= 5:
        raise ValueError("service_target must be 0..1 and risk_aversion 0..5")
    required = {sku: max(0.0, float(demand[sku]) - INVENTORY[sku]) for sku in SKUS}
    pairs = [(sku, s.code) for sku in SKUS for s in SUPPLIERS if s.code in ELIGIBILITY[sku]]
    count = len(pairs)
    # Variables: planned procurement of each sku from each eligible supplier, plus
    # shortage slack per SKU. Constraints always distinguish need from fulfillment.
    costs = []
    bounds = []
    for sku, code in pairs:
        s = SUPPLIER_BY_ID[code]
        price = PRODUCTS[sku]["unit_value"] * s.cost_factor
        carbon = carbon_price_per_ton * s.kg_co2_per_unit / 1000.0
        delay_risk = risk_aversion * 75.0 * s.delay_probability
        lead_risk = risk_aversion * 3.5 * max(s.lead_days - 7, 0)
        costs.append(price + carbon + delay_risk + lead_risk)
        # A declared outage is unavailable for its duration. Short outages leave
        # residual effective capacity, not a claim of exact delivery timing.
        outage_factor = max(0, 1 - disruption_days / max(horizon, 1)) if code in outages else 1.0
        on_time_factor = min(1.0, max(0.0, (horizon - s.lead_days + 1) / max(horizon, 1)))
        bounds.append((0, s.capacity * outage_factor * on_time_factor))
    costs.extend([1000.0] * len(SKUS))  # shortage penalty
    bounds.extend([(0, None)] * len(SKUS))
    A_ub, b_ub = [], []
    for j, sku in enumerate(SKUS):
        row = [0.0] * (count + len(SKUS))
        for i, (item, _) in enumerate(pairs):
            if item == sku:
                row[i] = -1.0
        row[count + j] = -1.0
        A_ub.append(row)
        b_ub.append(-required[sku])
    for s in SUPPLIERS:
        row = [float(code == s.code) for _, code in pairs] + [0.0] * len(SKUS)
        reduction = max(0, 1 - disruption_days / horizon) if s.code in outages else 1.0
        A_ub.append(row)
        b_ub.append(float(s.capacity) * reduction)
    # Cash limit applies to purchase costs only, not penalty or carbon weighting.
    price_by_pair = [PRODUCTS[sku]["unit_value"] * SUPPLIER_BY_ID[code].cost_factor for sku, code in pairs]
    A_ub.append(price_by_pair + [0.0] * len(SKUS))
    b_ub.append(budget)
    # Attempt hard minimum service requirement; if infeasible, solve best-effort
    # and surface the unmet service target instead of failing silently.
    service_row = [0.0] * count + [1.0] * len(SKUS)
    max_shortage = (1 - service_target) * sum(required.values())
    constrained = linprog(costs, A_ub=np.array(A_ub + [service_row]),
                          b_ub=np.array(b_ub + [max_shortage]), bounds=bounds, method="highs")
    service_feasible = bool(constrained.success)
    result = constrained if service_feasible else linprog(costs, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")
    quantities = result.x[:count]
    shortage = result.x[count:]
    allocations = []
    total_cost = total_carbon = 0.0
    for (sku, code), quantity in zip(pairs, quantities):
        if quantity < 0.01:
            continue
        supplier = SUPPLIER_BY_ID[code]
        unit_cost = PRODUCTS[sku]["unit_value"] * supplier.cost_factor
        total_cost += quantity * unit_cost
        total_carbon += quantity * supplier.kg_co2_per_unit
        allocations.append({
            "sku": sku, "supplier": code, "units": round(float(quantity), 2),
            "unit_cost": round(unit_cost, 2), "lead_days": supplier.lead_days,
            "delay_probability": supplier.delay_probability,
            "emissions_kg": round(float(quantity * supplier.kg_co2_per_unit), 1),
        })
    total_need = sum(required.values())
    actual_service = 1 - float(np.sum(shortage)) / max(total_need, 1)
    return {
        "allocations": sorted(allocations, key=lambda x: (x["sku"], x["supplier"])),
        "required_units": {sku: round(units, 1) for sku, units in required.items()},
        "unfilled_units": {sku: round(float(v), 1) for sku, v in zip(SKUS, shortage)},
        "purchase_cost": round(total_cost, 2),
        "emissions_kg": round(total_carbon, 1),
        "planned_service_rate": round(actual_service, 4),
        "service_target_feasible": service_feasible,
        "solver": "scipy HiGHS linear programming (continuous units)",
        "assumptions": "Capacity approximates deliverable units in planning horizon. Fractional units are planning estimates, not purchase orders.",
    }

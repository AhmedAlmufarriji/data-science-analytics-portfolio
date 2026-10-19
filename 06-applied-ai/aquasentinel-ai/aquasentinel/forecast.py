"""Time-ordered demand forecasting with a held-out test window."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

from aquasentinel.network import NODES
from aquasentinel.simulator import hourly_demand


def _features(hour: int, customers: int, district_index: int) -> list[float]:
    theta = 2 * math.pi * (hour % 24) / 24
    return [math.sin(theta), math.cos(theta), math.sin(2*theta), math.cos(2*theta),
            customers / 3000, district_index / 3, 1.0]


def training_data(hours: int = 24 * 16, seed: int = 11) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    rows_x, rows_y, time = [], [], []
    for t in range(hours):
        for n in NODES:
            if n["id"] == "RES":
                continue
            district = ["North", "Central", "East"].index(n["district"])
            base = (n["customers"] / 1000) * 30 * hourly_demand(t)
            weekend_shift = 1.06 if t // 24 % 7 in (4, 5) else 1.0
            rows_x.append(_features(t, n["customers"], district))
            rows_y.append(base * weekend_shift + rng.normal(0, 1.3))
            time.append(t)
    return np.array(rows_x), np.array(rows_y), np.array(time)


def forecast_demand(horizon: int = 12) -> dict:
    if not 1 <= horizon <= 72:
        raise ValueError("horizon must be 1..72")
    x, y, t = training_data()
    # Strict chronological holdout: last 72 hours. No shuffling or label leakage.
    cutoff = 24 * 13
    train, test = t < cutoff, t >= cutoff
    model = Ridge(alpha=1.2).fit(x[train], y[train])
    pred = model.predict(x[test])
    mae = float(mean_absolute_error(y[test], pred))
    # Forecast aggregate demand of all eight consumer nodes.
    points = []
    for h in range(24 * 16, 24 * 16 + horizon):
        vectors = [_features(h, n["customers"], ["North", "Central", "East"].index(n["district"]))
                   for n in NODES if n["id"] != "RES"]
        aggregate = float(np.clip(model.predict(vectors), 0, None).sum())
        points.append({"hour_ahead": h - 24 * 16 + 1, "total_lps_proxy": round(aggregate, 1)})
    return {"horizon_hours": horizon, "points": points, "holdout_mae_lps_per_node": round(mae, 2),
            "training_hours": cutoff, "test_hours": 72,
            "model": "Ridge with cyclical hourly features (synthetic demand)",
            "unit_note": "Demand proxy in L/s-equivalent, not calibrated flow metering."}

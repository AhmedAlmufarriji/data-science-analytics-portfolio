"""Deterministic synthetic demand and disruptions. No real company data."""
from __future__ import annotations

import numpy as np
import pandas as pd
from .catalog import PRODUCTS

SEED = 20261019

def promo_for(day: pd.Timestamp, sku: str) -> int:
    # Calendar-known feature; no access to future observed sales.
    return int((day.day % 17 in (1, 2, 3)) and (sum(map(ord, sku)) % 3 != day.month % 3))

def generate_history(days: int = 490, end: str = "2026-09-30", seed: int = SEED) -> pd.DataFrame:
    if days < 120:
        raise ValueError("At least 120 days are needed for lag features and validation")
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=end, periods=days, freq="D")
    rows = []
    for i, (sku, spec) in enumerate(PRODUCTS.items()):
        baseline = spec["base_daily"]
        # Product-specific seasonality, smooth trend, intermittent disruption and promotions.
        supply_noise = np.zeros(days)
        for start in (70 + i * 13, 230 + i * 7, 390 + i * 5):
            supply_noise[start:start + 7] -= baseline * (0.08 + 0.03 * i)
        for t, day in enumerate(dates):
            promo = promo_for(day, sku)
            weekday = 1.0 + 0.15 * np.sin((day.dayofweek + i) * np.pi / 3.5)
            yearly = 1.0 + 0.20 * np.sin(2 * np.pi * (day.dayofyear + i * 19) / 365.25)
            trend = 1.0 + 0.11 * t / days
            expected = baseline * weekday * yearly * trend * (1 + 0.36 * promo) + supply_noise[t]
            demand = max(1, int(round(expected + rng.normal(0, baseline * 0.16))))
            rows.append({"date": day, "sku": sku, "demand": demand, "promo": promo})
    return pd.DataFrame(rows).sort_values(["sku", "date"]).reset_index(drop=True)

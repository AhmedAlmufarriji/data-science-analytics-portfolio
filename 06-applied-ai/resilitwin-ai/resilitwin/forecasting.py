"""Leakage-safe one-step holdout evaluation and iterative 21-day forecasting."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from .catalog import PRODUCTS
from .simulation import promo_for

FEATURES = ["lag_1", "lag_7", "lag_14", "lag_28", "rolling_7", "rolling_28", "promo", "dow", "month_sin", "month_cos", "sku_id", "time_index"]
SKU_IDS = {sku: i for i, sku in enumerate(PRODUCTS)}


def make_features(history: pd.DataFrame) -> pd.DataFrame:
    data = history.sort_values(["sku", "date"]).copy()
    by_sku = data.groupby("sku", sort=False)["demand"]
    for lag in [1, 7, 14, 28]:
        data[f"lag_{lag}"] = by_sku.shift(lag)
    for width in [7, 28]:
        data[f"rolling_{width}"] = by_sku.transform(lambda s: s.shift(1).rolling(width).mean())
    data["dow"] = data["date"].dt.dayofweek
    data["month_sin"] = np.sin(2 * np.pi * data["date"].dt.month / 12)
    data["month_cos"] = np.cos(2 * np.pi * data["date"].dt.month / 12)
    data["sku_id"] = data["sku"].map(SKU_IDS)
    start = data["date"].min()
    data["time_index"] = (data["date"] - start).dt.days
    return data.dropna(subset=FEATURES).reset_index(drop=True)


@dataclass
class ForecastEngine:
    model: HistGradientBoostingRegressor
    history: pd.DataFrame
    score: dict
    uncertainty: dict[str, float]

    @classmethod
    def fit(cls, history: pd.DataFrame, holdout_days: int = 70) -> "ForecastEngine":
        frames = make_features(history)
        cutoff = history["date"].max() - pd.Timedelta(days=holdout_days)
        train = frames[frames.date <= cutoff]
        valid = frames[frames.date > cutoff]
        if train.empty or valid.empty:
            raise ValueError("Training and validation cannot be empty")
        # Parameter selection is fixed in code; validation only evaluates it.
        model = HistGradientBoostingRegressor(
            max_iter=130, max_leaf_nodes=15, learning_rate=0.08,
            l2_regularization=0.8, min_samples_leaf=22, random_state=42,
        )
        model.fit(train[FEATURES], train["demand"])
        predictions = np.maximum(0, model.predict(valid[FEATURES]))
        target = valid["demand"].to_numpy()
        seasonal = valid["lag_7"].to_numpy()
        residuals = abs(target - predictions)
        # Residual band is descriptive on the same holdout; NOT out-of-sample calibrated coverage.
        uncertainty = {}
        for sku in PRODUCTS:
            mask = valid["sku"].to_numpy() == sku
            uncertainty[sku] = float(np.quantile(residuals[mask], 0.90))
        wape = lambda estimates: float(np.sum(np.abs(target - estimates)) / max(np.sum(target), 1))
        score = {
            "validation_start": str(valid.date.min().date()),
            "validation_end": str(valid.date.max().date()),
            "n_validation_rows": len(valid),
            "mae_model": round(float(mean_absolute_error(target, predictions)), 3),
            "mae_seasonal_naive": round(float(mean_absolute_error(target, seasonal)), 3),
            "wape_model": round(wape(predictions), 4),
            "wape_seasonal_naive": round(wape(seasonal), 4),
            "interval_note": "Illustrative ±90th-percentile absolute validation residual bands; not guaranteed 90% future coverage.",
            "evaluation_note": "Chronological holdout, teacher-forced one-step predictions using observed lagged demand. Multi-step simulation can have larger errors.",
            "features": FEATURES,
        }
        return cls(model=model, history=history, score=score, uncertainty=uncertainty)

    def predict_future(self, horizon: int = 21) -> list[dict]:
        if not 1 <= horizon <= 60:
            raise ValueError("horizon must be 1..60")
        origin = self.history.date.min()
        latest = self.history.date.max()
        predictions = []
        for sku in PRODUCTS:
            rolling = self.history[self.history.sku == sku].sort_values("date")["demand"].astype(float).tolist()
            for step in range(1, horizon + 1):
                date = latest + pd.Timedelta(days=step)
                features = {
                    "lag_1": rolling[-1], "lag_7": rolling[-7],
                    "lag_14": rolling[-14], "lag_28": rolling[-28],
                    "rolling_7": float(np.mean(rolling[-7:])),
                    "rolling_28": float(np.mean(rolling[-28:])),
                    "promo": promo_for(date, sku),
                    "dow": date.dayofweek,
                    "month_sin": np.sin(2 * np.pi * date.month / 12),
                    "month_cos": np.cos(2 * np.pi * date.month / 12),
                    "sku_id": SKU_IDS[sku],
                    "time_index": (date - origin).days,
                }
                one = pd.DataFrame([features], columns=FEATURES)
                point = max(0.0, float(self.model.predict(one)[0]))
                rolling.append(point)  # recursive: no future ground truth leakage
                band = self.uncertainty[sku] * np.sqrt(1 + 0.035 * (step - 1))
                predictions.append({
                    "date": str(date.date()), "sku": sku,
                    "mean": round(point, 2),
                    "low": round(max(0, point - band), 2),
                    "high": round(point + band, 2),
                    "promo": features["promo"],
                })
        return predictions

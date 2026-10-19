"""Unsupervised anomaly detection + topology-aware leak localization."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from aquasentinel.network import PIPES, NODES, graph, distance_to_pipe, NODE_BY_ID
from aquasentinel.simulator import network_snapshot


class LeakDetector:
    def __init__(self) -> None:
        self.scaler = StandardScaler()
        self.model = IsolationForest(n_estimators=120, contamination=0.035,
                                     random_state=41, n_jobs=1)
        self.fitted = False

    @staticmethod
    def _features(frame: pd.DataFrame) -> np.ndarray:
        return frame[["pressure_residual", "flow_residual"]].to_numpy(dtype=float)

    def fit(self, clean_frame: pd.DataFrame) -> "LeakDetector":
        # Train only on known normal reference, never on the incident evaluation window.
        subset = clean_frame.loc[~clean_frame["is_leak"]]
        x = self.scaler.fit_transform(self._features(subset))
        self.model.fit(x)
        self.fitted = True
        return self

    def score(self, frame: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted:
            raise RuntimeError("Call fit() with normal reference data first")
        scored = frame.copy()
        raw = -self.model.decision_function(self.scaler.transform(self._features(frame)))
        scored["anomaly_score"] = np.round(raw, 4)
        scored["is_anomaly"] = self.model.predict(
            self.scaler.transform(self._features(frame))) == -1
        return scored


def localize_leaks(snapshot: list[dict], top_k: int = 4) -> list[dict]:
    """Rank plausible pipes using spatial signature agreement, not true posteriors.

    Scores are *relative evidence indices*, not statistically calibrated probabilities.
    """
    if not snapshot:
        return []
    g = graph()
    observed = {r["node_id"]: r for r in snapshot}
    candidates = []
    for pipe in PIPES:
        expected, pressure, flow, weights = [], [], [], []
        for node in NODES:
            nid = node["id"]
            if nid == "RES" or nid not in observed:
                continue
            spatial = math.exp(-distance_to_pipe(nid, pipe["id"], g) / 760)
            row = observed[nid]
            expected.append(spatial)
            pressure.append(max(0.0, -float(row["pressure_residual"])))
            flow.append(max(0.0, float(row["flow_residual"])))
            weights.append(1.0 + NODE_BY_ID[nid]["critical"] * 0.25)
        pattern = np.array(expected)
        signal = np.array(pressure) / 11.0 + np.array(flow) / 22.0
        w = np.array(weights)
        # Nonnegative least-squares amplitude fit for each candidate leak location.
        magnitude = max(0.0, float(np.sum(w * pattern * signal) / (np.sum(w * pattern**2) + 1e-9)))
        fit_error = float(np.average((signal - magnitude * pattern) ** 2, weights=w))
        # Penalize implausible amplitudes; vulnerability is a weak tie breaker.
        evidence = max(0.0, magnitude) / (1 + fit_error * 3) + 0.04 * pipe["vulnerability"]
        candidates.append({"pipe_id": pipe["id"], "district": NODE_BY_ID[pipe["target"]]["district"],
                           "evidence_score": round(evidence, 4),
                           "fit_error": round(fit_error, 4),
                           "estimated_severity": round(min(1.0, magnitude / 2), 3),
                           "affected_customers": NODE_BY_ID[pipe["target"]]["customers"],
                           "critical_facilities": NODE_BY_ID[pipe["target"]]["critical"]})
    candidates.sort(key=lambda item: item["evidence_score"], reverse=True)
    return candidates[:top_k]


def summarize_detection(frame: pd.DataFrame, detector: LeakDetector) -> dict:
    recent = frame.loc[frame["hour"] == frame["hour"].max()].copy()
    scored = detector.score(recent)
    snapshot = network_snapshot(frame)
    candidates = localize_leaks(snapshot)
    flagged = scored.loc[scored["is_anomaly"]]
    return {"hour": int(frame["hour"].max()),
            "flagged_nodes": flagged["node_id"].tolist(),
            "mean_anomaly_score": round(float(scored["anomaly_score"].mean()), 4),
            "candidates": candidates,
            "disclaimer": "Model-based screening for a synthetic network; verify with field measurements."}

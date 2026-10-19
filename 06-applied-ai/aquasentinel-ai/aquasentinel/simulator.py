"""Educational hydraulic *proxy* for sensor generation, not an EPANET solver."""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from aquasentinel.network import NODES, PIPES, graph, distance_to_pipe


@dataclass(frozen=True)
class LeakEvent:
    pipe_id: str = "P10"
    start_hour: int = 58
    duration_hours: int = 14
    severity: float = 0.82


def hourly_demand(hour: int) -> float:
    h = hour % 24
    return 0.76 + 0.31 * math.exp(-((h - 8) / 3.4) ** 2) + 0.43 * math.exp(
        -((h - 20) / 3.6) ** 2)


def generate_telemetry(hours: int = 96, seed: int = 27,
                       leak: LeakEvent | None = LeakEvent()) -> pd.DataFrame:
    """One row per node/hour; residual fields compare readings to known normal proxy.

    Forecasting and anomaly detection MUST NOT use the `is_leak` label as an input.
    """
    rng = np.random.default_rng(seed)
    g = graph()
    rows: list[dict] = []
    for hour in range(hours):
        demand = hourly_demand(hour)
        active = leak is not None and leak.start_hour <= hour < leak.start_hour + leak.duration_hours
        for node in NODES:
            if node["id"] == "RES":
                continue
            dist = float(__import__("networkx").shortest_path_length(
                g, "RES", node["id"], weight="weight"))
            base_pressure = 66.5 - 0.0047 * dist - 6.8 * (demand - 0.75)
            nominal_flow = 18 + node["customers"] * 0.019 * demand
            decay = (math.exp(-distance_to_pipe(node["id"], leak.pipe_id, g) / 760)
                     if active else 0.0)
            # Leak-induced loss decays with graph distance; intentionally simplified.
            pressure_drop = (11.0 * leak.severity * decay) if active else 0.0
            flow_gain = (22.0 * leak.severity * decay) if active else 0.0
            pressure = base_pressure - pressure_drop + rng.normal(0, 0.65)
            flow = nominal_flow + flow_gain + rng.normal(0, 1.35)
            rows.append({"hour": hour, "node_id": node["id"],
                         "district": node["district"], "customers": node["customers"],
                         "demand_factor": round(demand, 5),
                         "pressure_bar": round(pressure, 3),
                         "expected_pressure_bar": round(base_pressure, 3),
                         "flow_lps": round(flow, 3),
                         "expected_flow_lps": round(nominal_flow, 3),
                         "pressure_residual": round(pressure - base_pressure, 3),
                         "flow_residual": round(flow - nominal_flow, 3),
                         "is_leak": bool(active),
                         "leak_pipe": leak.pipe_id if active else None})
    return pd.DataFrame(rows)


def network_snapshot(frame: pd.DataFrame, hour: int | None = None) -> list[dict]:
    if frame.empty:
        return []
    hour = int(frame["hour"].max()) if hour is None else hour
    return frame.loc[frame["hour"] == hour].drop(columns=["is_leak", "leak_pipe"]).to_dict("records")


def get_demo_frame() -> pd.DataFrame:
    # At hour 71 the P10 event is active; current demo snapshot contains a real signal.
    return generate_telemetry(hours=72, seed=27)

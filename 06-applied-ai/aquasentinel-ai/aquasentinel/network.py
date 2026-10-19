"""Reproducible fictional water-network topology; no real utility data."""
from __future__ import annotations

import networkx as nx

NODES = [
    {"id": "RES", "name": "North Reservoir", "x": 9, "y": 46, "district": "Supply", "customers": 0, "critical": 0},
    {"id": "N1", "name": "Al Safa", "x": 28, "y": 21, "district": "North", "customers": 1400, "critical": 1},
    {"id": "N2", "name": "Al Noor", "x": 28, "y": 72, "district": "North", "customers": 2100, "critical": 0},
    {"id": "N3", "name": "Al Rawda", "x": 48, "y": 17, "district": "Central", "customers": 1600, "critical": 1},
    {"id": "N4", "name": "Al Zahra", "x": 52, "y": 50, "district": "Central", "customers": 2600, "critical": 2},
    {"id": "N5", "name": "Al Fayha", "x": 49, "y": 85, "district": "Central", "customers": 1800, "critical": 0},
    {"id": "N6", "name": "Al Waha", "x": 77, "y": 24, "district": "East", "customers": 2300, "critical": 1},
    {"id": "N7", "name": "Al Yasmin", "x": 78, "y": 63, "district": "East", "customers": 3100, "critical": 2},
    {"id": "N8", "name": "Al Amal", "x": 93, "y": 84, "district": "East", "customers": 1200, "critical": 0},
]

# Designed with redundant loops so alternative paths have a meaningful simulation effect.
_PIPES = [
    ("P01", "RES", "N1", 480, 130, 0.12), ("P02", "RES", "N2", 520, 140, 0.15),
    ("P03", "N1", "N3", 420, 95, 0.23), ("P04", "N1", "N4", 680, 110, 0.31),
    ("P05", "N2", "N4", 530, 110, 0.18), ("P06", "N2", "N5", 470, 110, 0.21),
    ("P07", "N3", "N4", 340, 95, 0.17), ("P08", "N4", "N5", 390, 95, 0.24),
    ("P09", "N3", "N6", 550, 95, 0.36), ("P10", "N4", "N7", 590, 90, 0.42),
    ("P11", "N5", "N7", 600, 90, 0.28), ("P12", "N6", "N7", 410, 90, 0.35),
    ("P13", "N7", "N8", 400, 80, 0.40), ("P14", "N5", "N8", 790, 75, 0.47),
]
PIPES = [
    {"id": pid, "source": a, "target": b, "length_m": length,
     "capacity_lps": cap, "vulnerability": vuln}
    for pid, a, b, length, cap, vuln in _PIPES
]
NODE_BY_ID = {n["id"]: n for n in NODES}
PIPE_BY_ID = {p["id"]: p for p in PIPES}


def graph(exclude_pipe: str | None = None) -> nx.Graph:
    g = nx.Graph()
    for node in NODES:
        g.add_node(node["id"], **node)
    for pipe in PIPES:
        if pipe["id"] != exclude_pipe:
            g.add_edge(pipe["source"], pipe["target"], **pipe, weight=pipe["length_m"])
    return g


def topology() -> dict:
    return {"nodes": NODES, "pipes": PIPES, "synthetic": True}


def distance_to_pipe(node: str, pipe_id: str, g: nx.Graph | None = None) -> float:
    g = g or graph()
    pipe = PIPE_BY_ID[pipe_id]
    return min(nx.shortest_path_length(g, node, endpoint, weight="weight")
               for endpoint in (pipe["source"], pipe["target"]))

"""Explainable what-if analysis using network reachability and path stretch."""
from __future__ import annotations

import networkx as nx

from aquasentinel.network import NODES, PIPE_BY_ID, graph


def simulate_closure(pipe_id: str, repair_hours: float = 6.0) -> dict:
    if pipe_id not in PIPE_BY_ID:
        raise ValueError(f"Unknown pipe: {pipe_id}")
    if not 0.5 <= repair_hours <= 168:
        raise ValueError("repair_hours must be between 0.5 and 168")
    before = graph()
    after = graph(exclude_pipe=pipe_id)
    affected, unreachable, route_changes = [], [], []
    for node in NODES:
        nid = node["id"]
        if nid == "RES":
            continue
        old = nx.shortest_path_length(before, "RES", nid, weight="weight")
        if not nx.has_path(after, "RES", nid):
            unreachable.append(nid)
            affected.append({"node": nid, "customers": node["customers"],
                             "path_stretch_percent": None})
        else:
            new = nx.shortest_path_length(after, "RES", nid, weight="weight")
            increase = max(0.0, 100 * (new / old - 1))
            if increase > 0:
                affected.append({"node": nid, "customers": node["customers"],
                                 "path_stretch_percent": round(increase, 1)})
                route_changes.append(increase)
    critical_unreachable = sum(n["critical"] for n in NODES if n["id"] in unreachable)
    customer_hours = round(sum(n["customers"] for n in NODES if n["id"] in unreachable) * repair_hours)
    # Illustrative risk index, not a hydraulic guarantee or financial estimate.
    risk_index = round(min(100, len(unreachable) * 22 + critical_unreachable * 12
                           + (sum(route_changes) / max(1, len(route_changes))) / 4), 1)
    return {"closed_pipe": pipe_id, "repair_hours": repair_hours,
            "reachable_nodes": len(NODES) - 1 - len(unreachable),
            "unreachable_nodes": unreachable,
            "customer_outage_hours_proxy": customer_hours,
            "affected_nodes": affected, "risk_index": risk_index,
            "assumptions": ["Routing approximates resilience with shortest paths on a static graph.",
                            "Does not solve hydraulic pressure or guarantee service continuity.",
                            "Customer outage hours count only disconnected nodes."]}


def repair_plan(candidates: list[dict], crew_count: int = 2) -> dict:
    if not 1 <= crew_count <= 20:
        raise ValueError("crew_count must be between 1 and 20")
    rows = []
    for c in candidates:
        # Explainable composite metric; never claim this is optimized against field data.
        severity = c["estimated_severity"]
        score = 45 * severity + 25 * min(c["affected_customers"] / 3500, 1) + \
                20 * min(c["critical_facilities"] / 2, 1) + 10 * min(c["evidence_score"], 1)
        rows.append({**c, "priority_score": round(score, 1),
                     "rationale": f"Severity {severity:.2f}; {c['affected_customers']:,} affected customers; "
                                  f"{c['critical_facilities']} critical facilities"})
    rows.sort(key=lambda r: r["priority_score"], reverse=True)
    for idx, item in enumerate(rows):
        item["assigned_crew"] = f"Crew {(idx % crew_count) + 1}"
        item["rank"] = idx + 1
    return {"crew_count": crew_count, "plan": rows,
            "caveat": "Decision support only: crew assignment excludes travel, skills and live safety checks."}

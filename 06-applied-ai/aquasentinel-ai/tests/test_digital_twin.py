from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

from aquasentinel.api import app, engine
from aquasentinel.agent import InvestigationAgent, redact
from aquasentinel.detection import LeakDetector, localize_leaks, summarize_detection
from aquasentinel.evidence import search_evidence
from aquasentinel.forecast import forecast_demand
from aquasentinel.memory import SessionMemory
from aquasentinel.network import graph, PIPES, NODES
from aquasentinel.scenarios import simulate_closure, repair_plan
from aquasentinel.simulator import LeakEvent, generate_telemetry, get_demo_frame, network_snapshot

client = TestClient(app)


def test_topology_has_loops_and_unique_ids():
    assert len(PIPES) == 14
    assert len({p["id"] for p in PIPES}) == len(PIPES)
    assert len(NODES) == 9
    assert len(graph().edges) == len(PIPES)


def test_synthetic_seed_reproducible():
    left = generate_telemetry(hours=10, seed=3)
    right = generate_telemetry(hours=10, seed=3)
    assert left.equals(right)
    assert len(left) == 80


def test_leak_changes_spatial_residual():
    clean = generate_telemetry(hours=70, seed=27, leak=None)
    leak = generate_telemetry(hours=70, seed=27, leak=LeakEvent())
    clean_avg = clean.query("hour == 65")["pressure_residual"].mean()
    leak_avg = leak.query("hour == 65")["pressure_residual"].mean()
    assert leak_avg < clean_avg - 1.0


def test_model_requires_training():
    with pytest.raises(RuntimeError):
        LeakDetector().score(get_demo_frame())


def test_detection_flags_anomalous_nodes():
    model = LeakDetector().fit(generate_telemetry(hours=240, seed=19, leak=None))
    result = summarize_detection(get_demo_frame(), model)
    assert len(result["flagged_nodes"]) >= 1
    assert result["candidates"][0]["pipe_id"] in {p["id"] for p in PIPES}


def test_localization_is_sensitive_to_signature():
    snap = network_snapshot(get_demo_frame())
    candidates = localize_leaks(snap)
    assert len(candidates) == 4
    assert candidates[0]["evidence_score"] >= candidates[-1]["evidence_score"]


def test_time_split_forecast_and_mae():
    out = forecast_demand(12)
    assert len(out["points"]) == 12
    assert out["training_hours"] + out["test_hours"] == 384
    assert out["holdout_mae_lps_per_node"] > 0
    assert all(p["total_lps_proxy"] > 0 for p in out["points"])


def test_bad_forecast_horizon():
    with pytest.raises(ValueError):
        forecast_demand(73)


def test_closure_resilience():
    out = simulate_closure("P01", 8)
    assert out["closed_pipe"] == "P01"
    assert 0 <= out["risk_index"] <= 100
    assert len(out["affected_nodes"]) >= 1


def test_bad_pipe_and_repair_duration():
    with pytest.raises(ValueError):
        simulate_closure("P999")
    with pytest.raises(ValueError):
        simulate_closure("P01", -1)


def test_repair_plan_is_ranked_and_assigned():
    result = repair_plan(localize_leaks(network_snapshot(get_demo_frame())), 2)
    assert result["plan"][0]["rank"] == 1
    assert result["plan"][1]["assigned_crew"] == "Crew 2"
    assert result["plan"][0]["priority_score"] >= result["plan"][-1]["priority_score"]


def test_evidence_returns_citations():
    sources = search_evidence("How to verify a leak with sensors and field tests?")
    assert sources
    assert sources[0]["source_id"].startswith(("RUNBOOK", "SAFETY"))


def test_session_memory_is_isolated():
    memory = SessionMemory()
    memory.set_district("one", "East")
    memory.remember("one", "user", "hello")
    assert memory.district("one") == "East"
    assert memory.district("two") is None
    memory.clear("one")
    assert memory.recent("one") == []


def test_agent_is_grounded_and_tools_are_explicit():
    mem = SessionMemory()
    agent = InvestigationAgent(mem, lambda: {"candidates": [{"pipe_id": "P10", "district": "East",
                                                                  "evidence_score": 1.2}], "flagged_nodes": ["N7"]},
                               forecast_demand)
    result = agent.investigate("Investigate possible leak and forecast demand", "s001")
    assert "leak_localizer" in result["tools_used"]
    assert "demand_forecaster" in result["tools_used"]
    assert result["actions_taken"] == []
    agent.investigate("Remember North district", "s001")
    assert mem.district("s001") == "North"


def test_safety_guardrail_and_redaction():
    assert "[REDACTED_EMAIL]" in redact("contact someone@example.com")
    agent = InvestigationAgent(SessionMemory(), lambda: {}, forecast_demand)
    blocked = agent.investigate("Disable safety monitoring", "s003")
    assert blocked["status"] == "blocked"
    assert blocked["actions_taken"] == []


def test_api_health_network_forecast():
    assert client.get("/api/health").json()["status"] == "ok"
    assert client.get("/api/network").json()["synthetic"] is True
    assert client.get("/api/forecast?horizon=5").json()["horizon_hours"] == 5
    assert client.get("/api/forecast?horizon=80").status_code == 422


def test_api_analysis_and_telemetry():
    assert client.get("/api/analyze").json()["candidates"]
    assert len(client.get("/api/telemetry?hour=71").json()["rows"]) == 8
    assert client.get("/api/telemetry?hour=1000").status_code == 422


def test_api_scenario_and_plan():
    assert client.post("/api/scenarios", json={"pipe_id": "P10"}).status_code == 200
    assert client.post("/api/scenarios", json={"pipe_id": "Z9"}).status_code == 422
    assert client.post("/api/repair-plan", json={"crews": 2}).json()["plan"]


def test_api_agent_memory_and_delete():
    response = client.post("/api/agent", json={"message": "Remember East district", "session_id": "demo_test"})
    assert response.status_code == 200
    assert client.get("/api/sessions/demo_test").json()["preferred_district"] == "East"
    assert client.delete("/api/sessions/demo_test").json()["deleted"]
    assert client.get("/api/sessions/demo_test").json()["preferred_district"] is None
    assert client.post("/api/agent", json={"message": "x", "session_id": "../"}).status_code == 422


def test_dashboard_served():
    assert "AquaSentinel" in client.get("/").text
    assert client.get("/static/style.css").status_code == 200

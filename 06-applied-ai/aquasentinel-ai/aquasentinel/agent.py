"""Auditable multi-tool agent with no opaque LLM or autonomous equipment actions.

This is an agentic orchestration *prototype*, not an Amazon Bedrock deployment.
"""
from __future__ import annotations

import re
from typing import Callable

from aquasentinel.evidence import search_evidence
from aquasentinel.memory import SessionMemory
from aquasentinel.scenarios import simulate_closure

_BLOCKED = re.compile(r"(?:disable|bypass|turn off|ignore|suppress|circumvent)\s+"
                      r"(?:all\s+)?(?:safety|alarm|alerts?|monitoring|guardrails?|interlocks?)", re.I)
_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE = re.compile(r"(?<!\w)(?:\+?966\s?5\d{8}|05\d{8})(?!\w)")
_PIPE = re.compile(r"\bP(?:0[1-9]|1[0-4])\b", re.I)


def redact(text: str) -> str:
    return _PHONE.sub("[REDACTED_PHONE]", _EMAIL.sub("[REDACTED_EMAIL]", text))


class InvestigationAgent:
    def __init__(self, memory: SessionMemory,
                 detection_provider: Callable[[], dict],
                 forecast_provider: Callable[[int], dict]) -> None:
        self.memory = memory
        self.detection_provider = detection_provider
        self.forecast_provider = forecast_provider

    def investigate(self, message: str, session_id: str = "demo") -> dict:
        msg = message.strip()
        if not msg:
            raise ValueError("Provide a question")
        if len(msg) > 500:
            raise ValueError("Questions must contain 500 characters or fewer")
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", session_id):
            raise ValueError("Invalid session identifier")
        safe_msg = redact(msg)
        self.memory.remember(session_id, "user", safe_msg)
        if _BLOCKED.search(msg):
            response = {"answer": "I cannot disable monitoring or bypass operational safety. "
                                     "Request an authorized field review instead.",
                        "tools_used": ["safety_policy"], "evidence": search_evidence("safety approval", 1),
                        "actions_taken": [], "status": "blocked"}
            self.memory.remember(session_id, "assistant", response["answer"])
            return response

        lower = msg.lower()
        tools, fragments = [], []
        district = next((x for x in ("North", "Central", "East")
                         if re.search(rf"\b{x}\b", msg, re.I)), None)
        if "remember" in lower and district:
            self.memory.set_district(session_id, district)
            fragments.append(f"I'll retain {district} as the preferred district in this session.")
            tools.append("session_memory")
        preference = self.memory.district(session_id)
        if any(x in lower for x in ("leak", "anomaly", "incident", "detect", "investigate", "risk", "priority")):
            data = self.detection_provider()
            best = data["candidates"][0] if data["candidates"] else None
            if best:
                fragments.append(f"Highest-ranked leak hypothesis: {best['pipe_id']} in "
                                 f"{best['district']} (relative evidence {best['evidence_score']:.2f}). "
                                 f"There are {len(data['flagged_nodes'])} flagged sensor nodes. "
                                 "A field team must confirm the source before action.")
            tools.append("leak_localizer")
        if any(x in lower for x in ("forecast", "demand", "tomorrow", "predict")):
            out = self.forecast_provider(12)
            peak = max(out["points"], key=lambda x: x["total_lps_proxy"])
            fragments.append(f"Next 12-hour predicted demand peak: {peak['total_lps_proxy']} "
                             f"L/s-equivalent at horizon +{peak['hour_ahead']}h; "
                             f"held-out MAE {out['holdout_mae_lps_per_node']} per node.")
            tools.append("demand_forecaster")
        pipe = _PIPE.search(msg)
        if pipe and any(x in lower for x in ("close", "closure", "isolate", "scenario", "what if")):
            outcome = simulate_closure(pipe.group().upper())
            fragments.append(f"Simulated closure of {outcome['closed_pipe']}: "
                             f"{len(outcome['unreachable_nodes'])} disconnected nodes, "
                             f"risk index {outcome['risk_index']}/100. "
                             "This graph result does not validate hydraulic pressures.")
            tools.append("scenario_engine")
        source_query = msg if not fragments else ("safety leak verification " + msg[:100])
        evidence = search_evidence(source_query, 2)
        if evidence:
            tools.append("evidence_retriever")
        if not fragments:
            if evidence:
                fragments.append(evidence[0]["excerpt"])
            else:
                fragments.append("I can investigate leaks, forecast demand, simulate closure of P01–P14, "
                                 "and explain water-network safety procedures.")
        if preference:
            fragments.append(f"Session preference: {preference} district.")
        answer = " ".join(fragments)
        self.memory.remember(session_id, "assistant", answer)
        return {"answer": answer, "tools_used": tools, "evidence": evidence,
                "actions_taken": [], "status": "completed",
                "grounding": "Deterministic tools and local documents; no external LLM calls."}

"""Transparent local document retrieval with explicit source references."""
from __future__ import annotations

import re
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class Evidence:
    source_id: str
    title: str
    section: str
    text: str


DOCUMENTS = [
    Evidence("RUNBOOK-01", "Leak investigation runbook", "Triage",
             "Compare pressure residuals against hour-of-day baseline. Corroborate localized "
             "pressure drops with excess flow and neighboring sensors before field dispatch. "
             "Escalate suspected leaks near hospitals and other critical facilities."),
    Evidence("RUNBOOK-02", "Leak investigation runbook", "Field verification",
             "A graph localization score is a hypothesis, not proof of a pipe failure. "
             "Check sensor calibration, valve status, planned maintenance and actual acoustic "
             "or pressure tests before isolating a pipe."),
    Evidence("SAFETY-01", "Operating safety guide", "Human authorization",
             "Never actuate physical valves, pumps or plant controls automatically from an AI "
             "recommendation. Require on-site safety approval, a lockout procedure where "
             "applicable, and independent confirmation of customer impact."),
    Evidence("RELIABILITY-01", "Resilience playbook", "Contingency",
             "For planned isolation, estimate disconnected demand and available alternate paths. "
             "Path redundancy alone does not establish adequate hydraulic pressure or water quality."),
    Evidence("FORECAST-01", "Analytics methodology", "Model evaluation",
             "Evaluate water demand forecasts on time-ordered holdout windows. "
             "Report absolute error, check seasonal stability and avoid training on future periods."),
    Evidence("PRIVACY-01", "Data governance note", "Synthetic data",
             "All supplied telemetry, districts, customers and incident records are fictional "
             "synthetic demonstration data. Do not infer actual infrastructure or residents."),
]

VECTORIZER = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
MATRIX = VECTORIZER.fit_transform([f"{x.title} {x.section} {x.text}" for x in DOCUMENTS])


def search_evidence(query: str, top_k: int = 3) -> list[dict]:
    if not query.strip() or not 1 <= top_k <= 6:
        return []
    vector = VECTORIZER.transform([re.sub(r"[^\w\s-]", " ", query.lower())])
    scores = cosine_similarity(vector, MATRIX).ravel()
    matches = sorted(range(len(scores)), key=lambda i: float(scores[i]), reverse=True)
    return [{"source_id": DOCUMENTS[i].source_id, "title": DOCUMENTS[i].title,
             "section": DOCUMENTS[i].section, "excerpt": DOCUMENTS[i].text,
             "similarity": round(float(scores[i]), 3)}
            for i in matches[:top_k] if scores[i] > 0]
